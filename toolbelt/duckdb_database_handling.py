"""DuckDB handling"""

import logging
import time
from itertools import cycle
from pathlib import Path
from shutil import get_terminal_size
from threading import Thread
from time import sleep

import duckdb


class Loader:
    """Loader
    """
    def __init__(self, desc="Loading...", end="Done!", timeout=0.1):
        """
        A loader-like context manager

        Args:
            desc (str, optional): The loader's description. Defaults to "Loading...".
            end (str, optional): Final print. Defaults to "Done!".
            timeout (float, optional): Sleep time between prints. Defaults to 0.1.
        """
        self.desc = desc
        self.end = end
        self.timeout = timeout

        self._thread = Thread(target=self._animate, daemon=True)
        self.steps = ["⢿", "⣻", "⣽", "⣾", "⣷", "⣯", "⣟", "⡿"]
        self.done = False

    def start(self):
        """start
        """
        self._thread.start()
        return self

    def _animate(self):
        for c in cycle(self.steps):
            if self.done:
                break
            print(f"\r{self.desc} {c}", flush=True, end="")
            sleep(self.timeout)

    def __enter__(self):
        self.start()

    def stop(self):
        """stop"""
        self.done = True
        cols = get_terminal_size((80, 20)).columns
        print("\r" + " " * cols, end="", flush=True)
        print(f"\r{self.end}", flush=True)

    def __exit__(self, exc_type, exc_value, tb):
        # handle exceptions with those variables ^
        self.stop()

logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')


def database_exists(db_path:Path)-> bool:
    """Check if the database already exists

    :param db_path: Database path
    :type db_path: Path
    """
    if db_path.exists() :
        logging.info("The base already exists, no new base will be created.")
    return db_path.exists()

def create_database(db_path:Path)-> None:
    """Create database

    :param db_path: Database path
    :type db_path: Path
    """
    try :
        connection = duckdb.connect(str(db_path))
        connection.close()
        logging.info(f"{db_path} database has been created.")
    except Exception as e :
        logging.error(e)

def execute_query_on_db(sql:str, db_path:Path, query_name, spatial:bool = False)-> None:
    """Execute SQL query on database

    :param sql: SQL Query
    :type sql: str
    :param db_path: Database path
    :type db_path: Path
    """

    start_time = time.time()
    logging.info(f"Start : {query_name}")

    loader = Loader("Execution in progress...", "Execution completed !", 0.05).start()
    try:
        with duckdb.connect(str(db_path)) as con:
            if spatial : 
                con.execute("INSTALL spatial ; LOAD spatial ;")
            con.execute(sql)
    except Exception as e:
        logging.error(e)
    loader.stop()

    end_time = time.time()
    elapsed_time = end_time - start_time
    logging.info(f"During {round(elapsed_time, 2)} sec")