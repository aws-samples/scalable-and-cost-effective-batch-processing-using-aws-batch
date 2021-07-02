import joblib
import sys
import pandas as pd
from pandas import DataFrame

# Read test data
x_test = pd.read_csv(str(sys.argv[1]))
print('Read test data from filesystem..')

# Load model file
loaded_rf = joblib.load("model.joblib")
print('Trained model file loaded..')

# Run predictions
prediction = loaded_rf.predict(x_test)
preds = DataFrame(prediction)

# Save data
preds.to_csv(str(sys.argv[2]))
print('Results sent to filesystem..')
