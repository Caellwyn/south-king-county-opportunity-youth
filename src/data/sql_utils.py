import psycopg2
import pandas as pd
import os

DBNAME = "opportunity_youth"

def create_database_and_tables():
    create_database()
    create_tables()
    print("Successfully created database and all tables")
    print()


def create_database():
    """
    This function assumes that you have an existing database called `postgres`
    without any username/password required to access it.  Then it creates a new
    database called `opportunity_youth`
    """
    # Depending on your local settings, you may need to specify a user and password, e.g.
    # conn = psycopg2.connect(dbname="postgres", user="postgres", password="password")
    conn = psycopg2.connect(dbname="postgres")
    conn.autocommit = True  # it seems this mode is needed to make a db
    conn.set_isolation_level(0)  # also this for dropping db

    # un-comment this line if you already have a database called
    # `opportunity_youth` and you want to drop it
    # execute_sql_script(conn, "01_drop_old_database.sql")
    execute_sql_script(conn, "02_create_new_database.sql")

    conn.close()


def create_tables():
    """
    Composite function that creates all relevant tables in the database
    This creates empty tables with the appropriate schema, then the data
    transfer is performed in the `copy_csv_files` function
    """
    # Depending on your local settings, you may need to specify a user and password, e.g.
    # conn = psycopg2.connect(dbname=DBNAME, user="postgres", password="password")
    conn = psycopg2.connect(dbname=DBNAME)

    create_pums_2017_table(conn)
    create_puma_names_2010_table(conn)
    create_wa_jobs_2017_table(conn)
    create_wa_geo_xwalk_table(conn)
    create_ct_puma_xwalk_table(conn)

    conn.close()


def create_pums_2017_table(conn):
    """
    Create a table for the 2017 5-year persons PUMS data
    """
    execute_sql_script(conn, "03_create_pums_2017_table.sql")


def create_puma_names_2010_table(conn):
    """
    Create a table for the 2010 PUMA names data
    """
    execute_sql_script(conn, "04_create_puma_names_2010_table.sql")


def create_wa_jobs_2017_table(conn):
    """
    Create a table for the 2017 WA jobs data
    """
    execute_sql_script(conn, "05_create_wa_jobs_2017_table.sql")


def create_wa_geo_xwalk_table(conn):
    """
    Create a table for the WA geographic crosswalk data
    """
    execute_sql_script(conn, "06_create_wa_geo_xwalk_table.sql")


def create_ct_puma_xwalk_table(conn):
    """
    Create a table for the census tract to puma geographic crosswalk data
    """
    execute_sql_script(conn, "07_create_ct_puma_xwalk_table.sql")


def copy_csv_files(data_files_dict):
    """
    Composite function that copies all CSV files into the database
    """
    # Depending on your local settings, you may need to specify a user and password, e.g.
    # conn = psycopg2.connect(dbname=DBNAME, user="postgres", password="password")
    conn = psycopg2.connect(dbname=DBNAME)

    for name, files in data_files_dict.items():
        csv_file = files[0]
        # skip the header; this info is already in the table schema
        next(csv_file)
        if name == "pums_2017":
            copy_csv_to_pums_2017_table(conn, csv_file)
        elif name == "puma_names_2010":
            copy_csv_to_puma_names_2010_table(conn, csv_file)
        elif name == "wa_jobs_2017":
            copy_csv_to_wa_jobs_2017_table(conn, csv_file)
        elif name == "wa_geo_xwalk":
            copy_csv_to_wa_geo_xwalk_table(conn, csv_file)
        elif name == "ct_puma_xwalk":
            copy_csv_to_ct_puma_xwalk_table(conn, csv_file)

        print(f"""Successfully loaded CSV file into `{name}` table
        """)

    conn.close()


def copy_csv_to_pums_2017_table(conn, csv_file):
    """
    Copy the CSV contents of the 2017 5-year persons data into the table
    """
    COPY_PUMS_2017 = "08_copy_pums_2017_to_table.psql"
    copy_expert_psql_script(conn, COPY_PUMS_2017, csv_file)


def copy_csv_to_puma_names_2010_table(conn, csv_file):
    """
    Copy the txt contents of the 2010 PUMA names data into the table
    """
    COPY_PUMA_NAMES_2010 = "09_copy_puma_names_2010_to_table.psql"
    copy_expert_psql_script(conn, COPY_PUMA_NAMES_2010, csv_file)


def copy_csv_to_wa_jobs_2017_table(conn, csv_file):
    """
    Copy the csv contents of the 2017 WA jobs data into the table
    """
    COPY_WA_JOBS_2017 = "10_copy_wa_jobs_2017_to_table.psql"
    copy_expert_psql_script(conn, COPY_WA_JOBS_2017, csv_file)


def copy_csv_to_wa_geo_xwalk_table(conn, csv_file):
    """
    Copy the csv contents of the WA geographic crosswalk data into the table
    """
    COPY_WA_GEO_XWALK = "11_copy_wa_geo_xwalk_to_table.psql"
    copy_expert_psql_script(conn, COPY_WA_GEO_XWALK, csv_file)


def copy_csv_to_ct_puma_xwalk_table(conn, csv_file):
    """
    Copy the csv contents of the census tract to puma geographic crosswalk data
    into the table
    """
    COPY_CT_PUMA_XWALK = "12_copy_ct_puma_xwalk_to_table.psql"
    copy_expert_psql_script(conn, COPY_CT_PUMA_XWALK, csv_file)


def execute_sql_script(conn, script_filename):
    """
    Given a DB connection and a file path to a SQL script, open up the SQL
    script and execute it
    """
    file_contents = open_sql_script(script_filename)
    cursor = conn.cursor()
    cursor.execute(file_contents)
    conn.commit()


def open_sql_script(script_filename):
    """
    Given a file path, open the file and return its contents
    We assume that the file path is always inside the sql directory
    """
    dir = os.path.dirname(__file__)
    relative_filename = os.path.join(dir, 'sql', script_filename)

    file_obj = open(relative_filename, 'r')
    file_contents = file_obj.read()
    file_obj.close()

    return file_contents


def copy_expert_psql_script(conn, script_filename, csv_file):
    """
    Given a DB connection and a file path to a PSQL script, open up the PSQL
    script and use it to run copy_expert
    """
    file_contents = open_sql_script(script_filename)
    cursor = conn.cursor()
    cursor.copy_expert(file_contents, csv_file)
    conn.commit()
