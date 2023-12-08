from sqlalchemy import create_engine, exc, text

create_flag = False

db_user = "postgres"
db_password = "1453"
db_host = "localhost"
db_port = "5432"
db_name = "library"
owner_user = "postgres"


if create_flag:
    default_connection_string = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/"
    default_engine = create_engine(default_connection_string, isolation_level="AUTOCOMMIT")

    with default_engine.connect() as connection:
        db_creation_query = text(f"CREATE DATABASE {db_name} WITH OWNER {owner_user}")

        try:
            connection.execute(db_creation_query)
            print(f"Database '{db_name}' created successfully.")

        except exc.ProgrammingError as err:
            print(f"Error creating database '{db_name}': {err}")
