"""Download manager
"""

import logging

import requests
from tqdm import tqdm

logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')

def download_file(url:str, filename)-> None:
    """Download file from url

    :param url: File URL
    :type url: str
    :param filename: Output path of file to be download
    :type filename: str
    """
    response = requests.get(url, stream=True, timeout=60)
    if response.status_code == 200:
        total_size = int(response.headers.get('Content-Length', 0))
        chunk_size = 1024  # 1KB
        with open(filename, 'wb') as file, tqdm(
            desc=filename,
            total=total_size,
            unit='B',
            unit_scale=True,
            unit_divisor=1024,
        ) as bar:
            for data in response.iter_content(chunk_size=chunk_size):
                file.write(data)
                bar.update(len(data))
        logging.info("Downloaded %s successfully.", filename)
    else:
        logging.error("Failed to download the file.")
