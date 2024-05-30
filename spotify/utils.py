import json
import os
import csv
from .config import logger

def save_to_json(data, file_path):
    file_path = get_unique_file_path(file_path, '.json')
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)
    logger.info(f"Data saved to {file_path}")

def create_directory(directory_path):
    os.makedirs(directory_path, exist_ok=True)
    logger.info(f"Directory '{directory_path}' created.")

def json_to_csv(json_file_path, csv_file_path):
    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)

    csv_file_path = get_unique_file_path(csv_file_path, '.csv')

    with open(csv_file_path, 'w', newline='') as csv_file:
        if isinstance(data, list):
            if data:
                # Write headers
                keys = data[0].keys()
                writer = csv.DictWriter(csv_file, fieldnames=keys)
                writer.writeheader()
                # Write data
                for entry in data:
                    writer.writerow(entry)
        elif isinstance(data, dict):
            # Write headers
            keys = data.keys()
            writer = csv.DictWriter(csv_file, fieldnames=keys)
            writer.writeheader()
            # Write data
            writer.writerow(data)
    
    logger.info(f"Data converted from {json_file_path} to {csv_file_path}")

def get_unique_file_path(file_path, extension):
    base, ext = os.path.splitext(file_path)
    counter = 1
    while os.path.exists(file_path):
        file_path = f"{base}_{counter}{extension}"
        counter += 1
    return file_path
