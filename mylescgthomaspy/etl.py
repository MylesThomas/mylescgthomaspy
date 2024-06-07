import pandas as pd
import numpy as np

def convert_dtypes(df):
    """
    Converts columns in a DataFrame to numeric if possible, otherwise to categorical.
    
    Parameters:
    df (pd DataFrame): The DataFrame to convert.
    
    Returns:
    pd.DataFrame: The DataFrame with converted data types.
    """
    for column in df.columns:
        # Attempt to convert each column to numeric
        df[column] = pd.to_numeric(df[column], errors='ignore')
        # If the column is not numeric and is an object, convert it to categorical
        if df[column].dtype == 'object':
            df[column] = df[column].astype('category')
    return df

def impute_missing_values(df, numerical_strategy='mean', categorical_strategy='mode'):
    """
    Impute missing values in a DataFrame using specified strategy.

    Parameters:
    df : pandas.DataFrame
        DataFrame with missing values.
    strategy : str, optional
        Strategy to use for imputing missing values. Options are 'mean', 'median', or 'mode'.

    Returns:
    pandas.DataFrame
        DataFrame with missing values imputed.
    """
    for column in df.columns:
        if df[column].dtype == 'object' or df[column].dtype == 'category':  # Categorical data
            if categorical_strategy == 'mode':
                mode = df[column].mode()[0]
                df[column].fillna(mode, inplace=True)
            else:
                raise ValueError("Mode is the only supported strategy for categorical data.")
        else:  # Numerical data
            if numerical_strategy == 'mean':
                mean = df[column].mean()
                df[column].fillna(mean, inplace=True)
            elif numerical_strategy == 'median':
                median = df[column].median()
                df[column].fillna(median, inplace=True)
            else:
                raise ValueError("Unsupported strategy for numerical data. Choose 'mean' or 'median'.")

    return df
