import os
import argparse
from azureml.core import Run
import pandas as pd
from sklearn.processing import MinMaxScaler

parser = argparse.ArgumentParser()
parser.add_argument('--input_data', type=str, dest='raw_dataset', help='Raw dataset')
parser.add_argument('--preped_data', type=str, dest='preped_dataset', help='Prepared dataset')
args = parser.parse_args()

saved_dir = args.preped_data
run = Run.get_context()

df = run.input_datasets['raw_dataset'].to_pandas_dataframe()

num_features = ['Pregnancies','PlasmaGlucose','DiastolicBloodPressure',
                'TricepsThickness','SerumInsulin','BMI','DiabetesPedigree']
scaler = MinMaxScaler()
df[num_features] = scaler.fit(df[num_features])

print('saving data to preped_data')
os.makedirs(saved_dir, exist_ok=True)
df.to_csv(os.path.join(saved_dir, 'preped_data.csv'), index=False)
run.complete()
