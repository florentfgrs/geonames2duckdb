"""Zip manager
"""
import logging
from pathlib import Path
from zipfile import ZipFile

logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')


def unzip_file(path:Path) -> None :
    """Unzip file
    :param path: Zip path
    :type path: Path
    """
    with ZipFile(str(path), "r") as zip: 
        try : 
            zip.extractall(path=path.parent) 
            logging.info("{str(path)}has been successfully unzipped on %s", str(path.parent))
        except Exception as e :
            logging.warning("Error during unzip %s : %s", str(path.parent), e)