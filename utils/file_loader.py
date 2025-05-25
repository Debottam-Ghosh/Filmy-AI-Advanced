import os
import gdown
import pickle

def download_and_load_similarity(file_id, local_path='similarity.pkl'):
    if not os.path.exists(local_path):
        url = f'https://drive.google.com/uc?id={file_id}'
        gdown.download(url, local_path, quiet=False)

    with open(local_path, 'rb') as f:
        return pickle.load(f)
