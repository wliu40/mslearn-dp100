
import pandas as pd
import os
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import roc_auc_score, roc_curve
import matplotlib.pyplot as plt
import argparse
import numpy as np
from azureml.core import Run, Model
import joblib

parser = argparse.ArgumentParser()
parser.add_argument('--training-data', type=str, dest='training_data', help='Input dataset for model')
args = parser.parse_args()

training_data_dir = args.training_data

run = Run.get_context()

# !!!!!
# df = run.input_datasets['input_data'].to_pandas_dataframe()
df = pd.read_csv(os.path.join(training_data_dir, 'preped_data.csv'))

features = ['Pregnancies','PlasmaGlucose','DiastolicBloodPressure','TricepsThickness',
            'SerumInsulin','BMI', 'DiabetesPedigree', 'Age']

# Separate features and labels

X, y = df[features].values, df['Diabetic'].values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.3, random_state=0)

model = DecisionTreeClassifier().fit(X_train, y_train)

y_pred = model.predict(X_test)

# ACC
acc = np.average(y_pred==y_test)
run.log(name='acc', value=acc)

# AUC
y_scores = model.predict_proba(X_test)
auc = roc_auc_score(y_test, y_scores[:, 1])
run.log(name='auc', value=auc)

# ROC
fpr, tpr, threshold = roc_curve(y_test, y_scores[:,1])
fig = plt.figure(figsize=(6, 4))
# Plot the diagonal 50% line
plt.plot([0, 1], [0, 1], 'k--')
# Plot the FPR and TPR achieved by our model
plt.plot(fpr, tpr)
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC Curve')
run.log_image(name = "ROC", plot = fig)
plt.show()

print('Saving model')
os.makedirs('models', exist_ok=True)

model_file_path = os.path.join('models', 'diabetes_model.pkl')
joblib.dump(value=model, filename=model_file_path)

Model.register(workspace=run.experiment.workspace,
               model_path=model_file_path,
               model_name='diabetes_model',
               tags={"training context": "pipeline_2"},
               properties={'AUC': np.float(auc), "ACC": np.float(acc)})
run.complete()
