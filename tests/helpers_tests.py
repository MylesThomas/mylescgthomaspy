import pandas as pd
import numpy as np
from mylescgthomaspy.helpers import flatten_multi_level_columns

# Creating a sample DataFrame with multi-level columns
columns = pd.MultiIndex.from_tuples([
    ('A', 'foo'), ('A', 'bar'), ('B', 'foo'), ('B', 'bar')
])
data = np.random.randn(4, 4)
df = pd.DataFrame(data, columns=columns)

# Flatten columns
df_flattened = flatten_multi_level_columns(df.copy(), separator='_')

assert isinstance(df.columns, pd.MultiIndex)
assert not isinstance(df_flattened.columns, pd.MultiIndex)
assert isinstance(df_flattened.columns, pd.Index)
assert list(df_flattened.columns) == ['A_foo', 'A_bar', 'B_foo', 'B_bar']
