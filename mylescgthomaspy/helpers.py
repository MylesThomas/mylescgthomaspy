import pandas as pd

def flatten_multi_level_columns(df, separator='_'):
    """
    Flatten a DataFrame's multi-level columns to a single level by joining level names.

    Parameters:
        df (pd.DataFrame): DataFrame with multi-level columns.
        separator (str): String to join the column levels.

    Returns:
        pd.DataFrame: DataFrame with a single-level column.
    """
    # Ensure the DataFrame has multi-level columns
    if not isinstance(df.columns, pd.MultiIndex):
        raise ValueError("The DataFrame does not have multi-level columns")

    # Create a new column index by joining the levels of the old index
    df.columns = [''.join([str(level) if str(level) != '' else '' for level in col]).strip() for col in df.columns]

    return df
