# PostgreSQL Database with FastAPI Interface

This project represents a PostgreSQL database for a library, which includes tables for managing books, patrons, and book checkout records. It was developed as a final project for the **SQL and NoSQL Databases** course at Russian-Armenian University (RAU).

## Description

This project is a FastAPI application designed to interface with a PostgreSQL database. It includes a RESTful API for managing books, patrons, and their interactions through checkouts. The application uses SQLAlchemy for ORM, Alembic for database migrations, and follows a modular structure for easy maintenance and scalability.

## General Structure

```
project-root/
│
├── alembic/                 # Alembic migrations and environment configuration
│   ├── versions/            # Directory containing migration scripts
│   │   ├── 6138998e2403_columns_gin_index.py  # Example migration: GIN index creation
│   │   ├── 1061ecca2c2b_create_tables.py      # Example migration: Table creation
│   │   └── ...
│   └── env.py               # Alembic environment configuration
│
├── app/                     # Main application package
│   ├── api.py               # FastAPI app routes and endpoints
│   ├── data.py              # Module for processing data from 'table_data' directory
│   ├── main.py              # FastAPI app creation and configuration
│   ├── models.py            # SQLAlchemy models defining the database schema
│   ├── session.py           # Database session management
│   └── ...
│
├── table_data/              # Data files for initializing database tables
│   └── ...
│
├── .gitignore               # Specifies intentionally untracked files to ignore
├── README.md                # You are here
└── requirements.txt         # Python dependencies required for the project
```

## Installation

To get started with this project, clone the repository and install the required dependencies:

```bash
git clone https://github.com/mikayelsaghatelyan/rau-database.git
cd project-name
pip install -r requirements.txt
```

## Usage

To run the FastAPI application:

```bash
uvicorn app.main:app --reload
```

This command will start the FastAPI server with auto-reload enabled.

## Database Initialization

Make sure you have PostgreSQL running and accessible. Initialize the database using Alembic:

```bash
alembic upgrade head
```

To seed the database with initial data:

```bash
python app/data.py
```

## Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

Distributed under the GPL License. See `LICENSE` for more information.
