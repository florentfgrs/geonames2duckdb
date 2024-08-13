"""Main script
"""
import logging
import tempfile
from pathlib import Path

from toolbelt.download_manager import download_file
from toolbelt.duckdb_database_handling import (create_database,
                                               database_exists,
                                               execute_query_on_db)
from toolbelt.zip_manager import unzip_file

logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')

database_path = Path(".data/geonames.db")

with tempfile.TemporaryDirectory() as temp_dir:
    temp_path = Path(temp_dir)
    logging.info("Temporary directory is using for download and unzip data: %s", str(temp_path))
    temp_zip_path = temp_path / "all.zip"
    ## All link here : https://download.geonames.org/export/dump/

    # Download and unzip
    download_file("https://download.geonames.org/export/dump/allCountries.zip", str(temp_zip_path))
    unzip_file(Path(temp_zip_path))

    # Import in database
    if not database_exists(database_path): 
        create_database(database_path)

    with open("./sql/table_geonames.sql", "r", encoding="utf-8") as file:
        sql_query = file.read()
        sql_query = sql_query.format(csv_path=str(temp_path / "allCountries.txt"))
        execute_query_on_db(sql=sql_query, db_path=database_path, 
                            spatial=True, query_name="Insert geonames from txt to database table")

# Drop file
logging.info("The temporary folder and its contents have been deleted.")
