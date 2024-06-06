# transformers.py

import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder

# Example of a label encoding transformer function
def label_encode_transformer(X):
    encoded_df = pd.DataFrame(X).copy()
    for col in encoded_df.columns:
        le = LabelEncoder()
        encoded_df[col] = le.fit_transform(encoded_df[col])
    return encoded_df
