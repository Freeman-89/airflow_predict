import json
import dill
import os
import logging

import pandas as pd

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
    ]
)
path = os.environ.get('PROJECT_PATH', '..')
models_dir = f'{path}/data/models'
jsons_data_path = f'{path}/data/test'
predictions_path = f'{path}/data/predictions'

if not os.path.exists(models_dir):
    logging.error(f"Models directory does not exist: {models_dir}")
if not os.path.exists(jsons_data_path):
    logging.error(f"JSONs data directory does not exist: {jsons_data_path}")
if not os.path.exists(predictions_path):
    logging.error(f"Predictions directory does not exist: {predictions_path}")

def load_model(model_path):
    with open(model_path, "rb") as file:
        model = dill.load(file)
    return model


def get_files_path():
    file_paths = [os.path.join(jsons_data_path, file) for file in os.listdir(jsons_data_path)]
    logging.info(file_paths)
    return file_paths


def predict():
    model = load_model(os.path.join(models_dir, os.listdir(models_dir)[0]))
    files_path = get_files_path()
    data = []
    for file in files_path:
        with open(file, 'r') as f:
            data.append(json.load(f))
    logging.info("Loaded data: %s", data)
    df = pd.DataFrame(data)
    logging.info("DataFrame: \n%s", df.head())
    y = model.predict(df)
    df['predictions'] = y
    for idx, pred in enumerate(y):
        logging.info(
            f"ID: {df['id'].iloc[idx]}, Price: {df['price'].iloc[idx]}, Prediction: {df['predictions'].iloc[idx]}")

    df.to_csv(os.path.join(predictions_path, 'predict.csv'), index=False)


if __name__ == '__main__':
    predict()
