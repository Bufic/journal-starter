#!/bin/bash
apt update -y
apt install -y postgresql postgresql-contrib

sed -i "s/#listen_addresses = 'localhost'/listen_addresses = '*'/" /etc/postgresql/*/main/postgresql.conf
echo "host all all 0.0.0.0/0 md5" >> /etc/postgresql/*/main/pg_hba.conf

sudo -u postgres psql -c "CREATE USER ${db_user} WITH PASSWORD '${db_password}';"
sudo -u postgres psql -c "CREATE DATABASE ${db_name};"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE ${db_name} TO ${db_user};"

systemctl restart postgresql
