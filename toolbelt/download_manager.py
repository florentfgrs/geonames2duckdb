import requests
from tqdm import tqdm
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')

def download_file(url, filename):
    response = requests.get(url, stream=True)
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
        logging.info(f"Downloaded {filename} successfully.")
    else:
        logging.error("Failed to download the file.")
