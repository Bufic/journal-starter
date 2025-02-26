# AWS VPC and EC2 Setup Guide
- This setup ensures a secure connection between your API and database while enabling efficient deployment and management.

## Create a VPC for a secure Connection between your Database Instance and API instance
- Navigate to the AWS Console and create a Virtual Private Cloud.
- Within the VPC, create two subnets:
  - **Private Subnet** (for the database)
  - **Public Subnet** (for the API)
- Create an Internet Gateway (IGW) for the Public Subnet and attach it to the created VPC.
- Set up a Route Table for the public subnet.
- Associate the Public Subnet with this Route Table.

## Launch the Database EC2 Instance
- Go to **AWS Console → EC2 → Launch Instance**.
- Select **Ubuntu 22.04 LTS** as the AMI.
- Choose **t3.micro** (or **t3.medium** for better performance).

### Configure Storage:
- **Type**: gp3 SSD
- **Size**: 50GB+ (Production)
- **IOPS**: 3000 (default)

## Security Group Settings:
- Allow **SSH (22)**, **PostgreSQL (5432 for internal access)**.
- **Source**: (API server's security group)
- Allow inbound connections **only from the API server**.
- **Port 5432 (PostgreSQL)**
- **Source**: (API server's security group)

### SSH into the Private DB Instance from the API Server
- the API Server will serve as our Bastion Host since we cannot access the private subnet
- ssh into the public api server
```sh
ssh -i ~/Downloads/web_server_key.pem ubuntu@<api-elastic-ip>
```
- Move the Key to the `.ssh/` Directory
```sh
mv ~/web_server_key.pem ~/.ssh/
```
- Set the Correct Permissions
```sh
chmod 400 ~/.ssh/web_server_key.pem
```
- Test SSH Access to the DB Instance
```sh
ssh -i ~/.ssh/web_server_key.pem ubuntu@<db-private-ip>
```

## Create a New Route Table and NAT Gateway for the Private Subnet
- A NAT Gateway is required to download dependencies over the internet, It Allows outbound internet access for package downloads while keeping it private.
- Create a **NAT Gateway** in the public subnet.
- Attach an **Elastic IP** to the NAT Gateway.
- Navigate to **VPC Dashboard** and create a **New Route Table**:
  1. Enter a Name (e.g., "Private Route Table").
  2. Select the VPC where your private subnet resides.
  3. Add a Route to the NAT Gateway.
  4. Edit the Route Table:
     - **Destination**: `0.0.0.0/0` (Route all traffic to the internet)
     - **Target**: Select NAT Gateway from the dropdown.
  5. Associate the Route Table with the private subnet(s).

## Connect to EC2 & Install PostgreSQL
```sh
sudo apt update && sudo apt upgrade -y
sudo apt install postgresql postgresql-contrib -y
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

## Configure PostgreSQL to Accept Connections from only the Public Subnet
- Edit PostgreSQL configuration:
```sh
sudo nano /etc/postgresql/16/main/pg_hba.conf
```
- Add the following line:
```sh
host    all    all    <private-subnet-IPv4-CIDR>   md5
```
- Allow any internal service in your subnet to connect:
```sh
host    <db_name>    <db_user>    <public_subnet_address>   md5
```
- Edit PostgreSQL listening settings:
```sh
sudo nano /etc/postgresql/16/main/postgresql.conf
```
- find the line 
```sh
listen_addresses = 'localhost' 
```
- uncomment it and modify it to
```sh
listen_addresses = '<private-db-ip-address>'
```
- Save and exit (Ctrl+O, Enter, Ctrl+X).
- Restart PostgreSQL:
```sh
sudo systemctl restart postgresql
```

## Create a PostgreSQL User
- Log in as the postgres superuser: 
```sh
sudo -u postgres psql
```
- Create a database, database user, password for the user and Grant admin rights for superuser privileges
```sql
CREATE DATABASE <db_name>;
CREATE USER <name_of_postgres_user> WITH PASSWORD '<password_of_user>';
ALTER USER <name_of_postgres_user> WITH SUPERUSER;
```
- exit
```sh
\q
```
- Login as the new user
```sh
psql -h <db_private_ip> -U <name_of_postgres_user> -d <db_name>
```

## Create a Table Called "Entries"
```sql
CREATE TABLE entries (
    id UUID PRIMARY KEY,
    data JSONB,
    created_at TIMESTAMP WITH TIME ZONE,
    updated_at TIMESTAMP WITH TIME ZONE
);
```

## Security Group Settings for the API Server:
- Allow **port 22 (SSH)** from your IP.
- Allow **port 80/443 (HTTP/HTTPS)** from anywhere (`0.0.0.0/0`).
- Allow **port 8000** (if running FastAPI locally) from anywhere.
- Allow **port 5432 (PostgreSQL)** but only from the database private subnet (eg. `10.0.2.0/24`).
- leave outbound rule as default.

## Launch the API Server EC2 Instance
- Go to **AWS Console → EC2 → Launch Instance**.
```yaml
Name: fastapi-server
AMI: Ubuntu 22.04 LTS
Instance Type: t3.micro
VPC: <your-vpc>
Subnet: <public-subnet>
Auto-assign Public IP: Enabled
Security Group: <Security-group-for-public-api-server>
```

## Assign an Elastic IP to Your API Server EC2 Instance 
- This IP will persist even after stopping and starting the instance

1. Go to **AWS Console** → **EC2**.
2. On the left sidebar, click **Elastic IPs** under **Network & Security**.
3. Click **Allocate Elastic IP address** → Click **Allocate**.
4. Once allocated, select the Elastic IP and click **Associate Elastic IP address**.
5. Choose your **EC2 instance** and **network interface** (should be the default one).
6. Click **Associate**.
7. Now, your public IP will persist even after stopping and starting the instance.

## SSH into the API Server
```sh
ssh -i ~/Downloads/web_server_key.pem ubuntu@<api-elastic-ip>
```

## Clone Your Repository Using SSH
- To clone your repository on your EC2 instance, you need to use one of the following authentication methods:
 **Use a Personal Access Token (PAT) (Recommended for HTTPS)**
 **Use SSH Authentication (Recommended for Servers)**

- Generate SSH key
```sh
ssh-keygen -t rsa -b 4096 -C "<your-github-email>"
```
- Copy the public key:
```sh
cat ~/.ssh/id_rsa.pub
```
- Add the key to GitHub:
  1. Go to **GitHub SSH Keys**.
  2. Click "New SSH key".
  3. Paste the copied key and save.

- Test the connection: you should see a successful authentication now
```sh
ssh -T git@github.com
```
- Clone using SSH URL: replace the placeholder with the correct link
```sh
git clone <repo-ssh-link>
```

## Install Dependencies
```sh
sudo apt update && sudo apt install -y make python3 python3-pip python3-venv
cd journal-starter
python3 -m venv venv
source venv/bin/activate
```
- create a .env file and add the following, replace the placeholder with the actual names and links
```sh
# Postgres settings
POSTGRES_HOST=<replace_with_your_private_ip>
POSTGRES_PORT=5432
POSTGRES_USER=<name_of_postgres_user>
POSTGRES_PASSWORD=<password_of_user>
POSTGRES_DB=<name_of_db>
DATABASE_URL= postgresql://<name_of_postgres_user>:<password_of_user>@<replace_with_your_private_ip>:5432/<name_of_db>
APPLICATIONINSIGHTS_CONNECTION_STRING = "InstrumentationKey=8434363a-5fdc-411e-bb0f-5a9c1b2d272a;IngestionEndpoint=https://eastus2-3.in.applicationinsights.azure.com/;LiveEndpoint=https://eastus2.livediagnostics.monitor.azure.com/;ApplicationId=88b0f9ce-9384-4fb8-a9b0-87029569ea7d"
```

## Ensure FastAPI Listens on All Interfaces
Modify your **Makefile**:
```sh
uvicorn api.main:app --reload --host 0.0.0.0
```

## Run the API
```sh
make install
make run
```
- now you can view your api endpoint on the browser using the elastic ip address and the port number
```
eg. 
http://52.32.59.145:8000/entries
```
## Don't Forget to Remove the NAT Gateway  
Since we are not downloading anything from the internet, you can safely remove the NAT Gateway.  

### Delete the NAT Gateway  
1. Go to **AWS Console** → **VPC** → **NAT Gateways**.  
2. Select your **NAT Gateway** → Click **Delete**.  
3. Confirm the deletion.  

### Update the Route Table for the Private Subnet  
1. Go to **AWS Console** → **VPC** → **Route Tables**.  
2. Find the **private subnet’s route table** (it currently routes traffic via the NAT Gateway).  
3. Remove the route to the **NAT Gateway** (`0.0.0.0/0 → NAT-GW-ID`).  
4. Your **private subnet** should now have **no direct internet access** (which is good for security).  
