# Journal API Starter

A FastAPI-based journal API that allows storing and retrieving journal entries using PostgreSQL as the database backend. Code for [Phase 3 captstone](https://learntocloud.guide/phase3) 

## Prerequisites

- Python 3.8+
- PostgreSQL
- pip (Python package manager)

## Environment Setup

1. Clone the repository:

    ```bash
    git clone https://github.com/learntocloud/journal-starter.git
    cd journal-starter
    ```

2. Create a `.env` file with the following variables:

    ``` sh
        POSTGRES_HOST=<database_private_ip>
        POSTGRES_PORT=5432
        POSTGRES_USER=<database_user>
        POSTGRES_PASSWORD=<database_password>
        POSTGRES_DB=<database_name>
        DATABASE_URL=postgresql://<database_user>:<database_password>@<database_private_ip>:5432/<database_name>
    ```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Running the API

Start the FastAPI server:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

## API Endpoints

### GET /entries

Retrieve all journal entries

### POST /entries

Create a new journal entry

```json
{
    "title": "My Entry",
    "content": "Today was a good day",
    "tags": ["daily", "personal"]
}
```

### GET /entries/{entry_id}

Retrieve a specific entry by ID

### PUT /entries/{entry_id}

Update an existing entry

### DELETE /entries/{entry_id}

Delete an entry

## Database Schema

The database uses a single table `entries` with the following structure:

| Column      | Type                     | Description            |
|------------|--------------------------|------------------------|
| id         | UUID                     | Primary key           |
| data       | JSONB                    | Entry content         |
| created_at | TIMESTAMP WITH TIME ZONE | Creation timestamp    |
| updated_at | TIMESTAMP WITH TIME ZONE | Last update timestamp |
