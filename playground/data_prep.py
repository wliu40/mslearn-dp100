import os
import argparse
from azureml.core import Run
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

parser = argparse.ArgumentParser()
parser.add_argument('--input-data', type=str, dest='raw_data', help='Raw dataset')
parser.add_argument('--preped-data', type=str, dest='preped_data', help='Prepared dataset')
args = parser.parse_args()

saved_dir = args.preped_data
run = Run.get_context()

df = run.input_datasets['raw_data'].to_pandas_dataframe()
run.log(name='data shape', value=str(df.shape[0]))

num_features = ['Pregnancies','PlasmaGlucose','DiastolicBloodPressure',
                'TricepsThickness','SerumInsulin','BMI','DiabetesPedigree']

num_cols = ['Pregnancies','PlasmaGlucose','DiastolicBloodPressure','TricepsThickness','SerumInsulin','BMI','DiabetesPedigree']

run.log_list("numerical cols", num_cols)

scaler = MinMaxScaler()
df[num_features] = scaler.fit_transform(df[num_features])

print('saving data to preped_data')
os.makedirs(saved_dir, exist_ok=True)
df.to_csv(os.path.join(saved_dir, 'preped_data.csv'), index=False)
run.complete()
