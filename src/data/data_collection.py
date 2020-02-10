from io import BytesIO, TextIOWrapper, StringIO
from zipfile import ZipFile
from gzip import GzipFile
from csv import QUOTE_ALL

import pandas as pd
import requests

from src.data import sql_utils

def download_data_and_load_into_sql():
    """
    This function dispatches everything.  It creates a PostgreSQL database with
    the appropriate name, sets up the table schema, downloads all of the files
    containing the data, and loads the data into the database
    """
    sql_utils.create_database_and_tables()
    data_files_dict = collect_all_data_files()
    load_into_sql(data_files_dict)


def collect_all_data_files():
    """
    Create a dictionary with the in-memory file objects associated with all
    database tables
    """
    data_files_dict = {
        "pums_2017": collect_pums_2017_data(),
        "puma_names_2010": collect_puma_names_2010_data(),
        "wa_jobs_2017": collect_wa_jobs_2017_data(),
        "wa_geo_xwalk": collect_wa_geo_xwalk_data(),
        "ct_puma_xwalk": collect_ct_puma_xwalk()
    }
    return data_files_dict


def load_into_sql(data_files_dict):
    """
    Given a dictionary of in-memory file objects, use sql_utils to copy them
    into the database.  Then close all of them.

    Each dictionary value is a tuple containing a CSV file object, then either
    None or some other file to be closed, e.g. a zip file
    """
    sql_utils.copy_csv_files(data_files_dict)

    for csv_file, other_file in data_files_dict.values():
        csv_file.close()
        if other_file:
            other_file.close()


def collect_pums_2017_data():
    """
    Download the 2017 5-year ACS PUMS person-level records for the state of WA
    """
    PUMS_2017_URL = "https://www2.census.gov/programs-surveys/acs/data/pums/2017/5-Year/csv_pwa.zip"
    PUMS_2017_CSV_NAME = "psam_p53.csv"
    return collect_zipfile_data(PUMS_2017_URL, PUMS_2017_CSV_NAME)


def collect_puma_names_2010_data():
    """
    Download the 2010 PUMA names data
    """ 
    PUMA_NAMES_2010_URL = "https://usa.ipums.org/usa/resources/volii/CPUMA0010_PUMA2010_components.xls"
    return collect_xls_data(PUMA_NAMES_2010_URL)


def collect_wa_jobs_2017_data():
    """
    Download the 2017 WA jobs data
    """
    WA_JOBS_2017_URL = "https://lehd.ces.census.gov/data/lodes/LODES7/wa/wac/wa_wac_S000_JT00_2017.csv.gz"
    return collect_gzip_data(WA_JOBS_2017_URL)


def collect_wa_geo_xwalk_data():
    """
    Download the WA geographic crosswalk data
    """
    WA_GEO_XWALK_URL = "https://lehd.ces.census.gov/data/lodes/LODES7/wa/wa_xwalk.csv.gz"
    return collect_gzip_data(WA_GEO_XWALK_URL)


def collect_ct_puma_xwalk():
    """
    Download the census tract to puma geographic crosswalk data
    """
    CT_PUMA_XWALK_URL = "https://www2.census.gov/geo/docs/maps-data/data/rel/2010_Census_Tract_to_2010_PUMA.txt"
    return collect_csv_data(CT_PUMA_XWALK_URL)


def collect_zipfile_data(URL, csv_name):
    """
    Helper function used to collect CSV files contained in .zip archives
    """
    zip_file = download_zipfile(URL)
    csv_file = open_csv_from_zip(zip_file, csv_name)
    # return both so we can safely close them at the end
    return csv_file, zip_file


def collect_gzip_data(URL):
    """
    Helper function used to collect .gz compressed CSV files
    """
    gzip_file = download_gzipfile(URL)
    csv_file = open_csv_from_gzip(gzip_file)
    # return both so we can safely close them at the end
    return csv_file, gzip_file


def collect_xls_data(URL):
    """
    Given a URL for a .xls, load it into memory and convert it into a CSV file
    using Pandas
    """
    # read the data from the remote server
    xls_df = pd.read_excel(URL)
    # make an empty file in memory
    csv_file = StringIO()
    # write to the empty file in CSV format
    xls_df.to_csv(csv_file, index=False, quoting=QUOTE_ALL)
    # return the file pointer to the top of the file, so it can be read from
    csv_file.seek(0)
    # only 1 file needs to be closed, but later code is expecting a tuple
    return csv_file, None


def collect_csv_data(URL):
    """
    Given a URL for an un-compressed CSV, download and open it
    """
    response = requests.get(URL)
    print(f"""Successfully downloaded CSV file
    {URL}
    """)

    content_as_file = BytesIO(response.content)
    csv_file_text = TextIOWrapper(content_as_file, encoding="ISO-8859-1")
    # only 1 file needs to be closed, but later code is expecting a tuple
    return csv_file_text, None


def download_zipfile(URL):
    """
    Given a URL for a .zip, download and unzip the .zip file
    """
    response = requests.get(URL)
    print(f"""Successfully downloaded ZIP file
    {URL}
    """)

    content_as_file = BytesIO(response.content)
    zip_file = ZipFile(content_as_file)
    return zip_file


def download_gzipfile(URL):
    """
    Given a URL for a .gz, download and decompress the .gz file
    """
    response = requests.get(URL)
    print(f"""Successfully downloaded GZIP file
    {URL}
    """)

    content_as_file = BytesIO(response.content)
    decompressed_file = GzipFile(fileobj=content_as_file)
    return decompressed_file


def open_csv_from_zip(zip_file, csv_name):
    """
    Given an unzipped .zip file and the name of a CSV inside of it, 
    extract the CSV and return the relevant file
    """
    csv_file_bytes = zip_file.open(csv_name)
    # it seems we have to open the .zip as bytes, but CSV reader requires text
    csv_file_text = TextIOWrapper(csv_file_bytes, encoding="ISO-8859-1")
    return csv_file_text


def open_csv_from_gzip(gzip_file):
    """
    Given a decompressed CSV .gz file, return the content of the CSV
    """
    csv_file_text = TextIOWrapper(gzip_file, encoding="ISO-8859-1")
    return csv_file_text
