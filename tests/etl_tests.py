import pandas as pd
import numpy as np
from mylescgthomaspy.etl import impute_missing_values

data = {
    'Age': [25, 27, 29, np.nan, 31, np.nan, 28],
    'Gender': ['Male', 'Female', 'Female', 'Male', np.nan, 'Female', 'Male']
}
df = pd.DataFrame(data)
na_values_before = df.isna().sum().sum()
assert na_values_before == 3

imputed_df = impute_missing_values(df)
na_values_after = imputed_df.isna().sum().sum()
assert na_values_after == 0