
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
parser.add_argument('--input_data', type=str, dest='input_data', help='Input dataset for model')
args = parser.parse_args()

run = Run.get_context()
df = run.input_datsets['input_data'].to_pandas_dataframe()

X_train, y_train, X_test, y_test = train_test_split(df, test_size=.3, random_state=0)

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
fpr, tpr, threshold = roc_curve(y_test, y_score[:,1])
fig, ax = plt.subplots(figsize=(6, 6))
ax.plot([0,1], [0,1], 'k--')
ax.plot(fpr, tpr)
ax.title('ROC curve')
ax.set_xlabel('FPR')
ax.set_ylabel('TPR')
run.log_image(name='roc_curve', plot=fig)

print('Saving model')
os.makedirs('models', exist_ok=True)

model_file_path = os.path.join('models', 'diabetes_model.pkl')
joblib.dump(model, model_file_path)

Model.register(workspace=ws,
              model_path=model_file,
              tags={"training context": "pipeline"},
              properties={'AUC': auc, "ACC": acc},
              model_Path=model_file_path)
run.complete()
