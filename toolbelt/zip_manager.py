from zipfile import ZipFile 
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')


def unzip_file(path:Path) -> None :
    """Unzip file
    :param path: Zip path
    :type path: Path
    """
    with ZipFile(str(path), "r") as zip: 
        try : 
            zip.extractall(path=path.parent) 
            logging.info(f"{str(path)}has been successfully unzipped on {str(path.parent)}")
        except Exception as e : 
            logging.warning(f"Error during unzip {str(path)}")