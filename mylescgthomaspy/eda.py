import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def generate_eda_plots(df, output_dir=""):
    """
    Generates EDA plots for each column in the DataFrame based on the data type of the column.
    Numeric columns get histograms and boxplots. Categorical columns get count plots.

    Parameters:
    - df (pd.DataFrame): The DataFrame containing the data.

    Returns:
    - None: Plots are displayed using plt.show() and not saved.
    """
    for column in df.columns:
        # Determine the data type of the column
        if pd.api.types.is_numeric_dtype(df[column]):
            # Create histogram for numeric data
            plt.figure(figsize=(10, 5))
            sns.histplot(df[column], kde=True, color='skyblue')
            plt.title(f'Histogram of {column}', fontsize=16, fontweight='bold')
            plt.xlabel(column)
            plt.ylabel('Frequency')
            filename = f"numeric_histogram_{column}.png"
            if output_dir:
                filename = os.path.join(output_dir, filename)
            plt.savefig(filename)
            plt.show()
            plt.close()  # Close the plot to free up memory

            # Create boxplot for numeric data
            plt.figure(figsize=(10, 5))
            sns.boxplot(x=df[column], color='green')
            plt.title(f'Boxplot of {column}', fontsize=16, fontweight='bold')
            plt.xlabel(column)
            plt.ylabel('Value')
            filename = f"numeric_boxplot_{column}.png"
            if output_dir:
                filename = os.path.join(output_dir, filename)
            plt.savefig(filename)
            plt.show()
            plt.close()  # Close the plot to free up memory
        elif pd.api.types.is_categorical_dtype(df[column]) or pd.api.types.is_object_dtype(df[column]):
            # Create count plot for categorical data
            plt.figure(figsize=(10, 5))
            order = df[column].value_counts().index  # Order bars by count
            sns.countplot(x=df[column], order=order, palette='viridis')
            plt.title(f'Count Plot of {column}', fontsize=16, fontweight='bold')
            plt.xlabel(column)
            plt.ylabel('Count')
            plt.xticks(rotation=45)  # Rotate labels if there are many categories
            filename = f"categorical_count_plot_{column}.png"
            if output_dir:
                filename = os.path.join(output_dir, filename)
            plt.savefig(filename)
            plt.show()
            plt.close()  # Close the plot to free up memory

def generate_relationship_plots(df, response, response_type='numeric', output_dir=""):
    """
    Generates plots to analyze the relationship between a specified response variable and other variables in a DataFrame,
    adjusting the plot type based on whether the response variable is numeric or categorical.

    Parameters:
    - df (pd.DataFrame): The DataFrame containing the data.
    - response (str): The column name of the response variable.
    - response_type (str): Type of the response variable ('numeric' or 'categorical').

    Returns:
    - None: Plaots are displayed using plt.show() and not saved.
    """
    for column in df.columns:
        if column != response:
            if response_type == 'numeric':
                # Check if the predictor is numeric
                if pd.api.types.is_numeric_dtype(df[column]):
                    plt.figure(figsize=(10, 6))
                    sns.scatterplot(data=df, x=column, y=response)
                    plt.title(f'Scatter Plot of {response} vs. {column}', fontsize=16, fontweight='bold')
                    plt.xlabel(column)
                    plt.ylabel(response)
                    filename = f"numeric_scatterplot_{column}.png"
                    if output_dir:
                        filename = os.path.join(output_dir, filename)
                    plt.savefig(filename)
                    plt.show()
                    plt.close()

                elif pd.api.types.is_categorical_dtype(df[column]) or pd.api.types.is_object_dtype(df[column]):
                    plt.figure(figsize=(10, 6))
                    sns.boxplot(x=column, y=response, data=df)
                    plt.title(f'Boxplot of {response} by {column}', fontsize=16, fontweight='bold')
                    plt.xlabel(column)
                    plt.ylabel(response)
                    plt.xticks(rotation=45)
                    filename = f"categorical_boxplot_{column}.png"
                    if output_dir:
                        filename = os.path.join(output_dir, filename)
                    plt.savefig(filename)
                    plt.show()
                    plt.close()

            elif response_type == 'categorical':
                # Check if the predictor is numeric
                if pd.api.types.is_numeric_dtype(df[column]):
                    plt.figure(figsize=(10, 6))
                    sns.violinplot(x=response, y=column, data=df)
                    plt.title(f'Violin Plot of {column} by {response}', fontsize=16, fontweight='bold')
                    plt.xlabel(response)
                    plt.ylabel(column)
                    plt.show()
                    filename = f"numeric_violin_plot_{column}.png"
                    if output_dir:
                        filename = os.path.join(output_dir, filename)
                    plt.savefig(filename)
                    plt.show()
                    plt.close()

                elif pd.api.types.is_categorical_dtype(df[column]) or pd.api.types.is_object_dtype(df[column]):
                    # Generate a mosaic plot or a stacked bar chart
                    data_crosstab = pd.crosstab(df[column], df[response], normalize='index')
                    data_crosstab.plot(kind='bar', stacked=True, figsize=(10, 6))
                    plt.title(f'Stacked Bar Plot of {column} by {response}', fontsize=16, fontweight='bold')
                    plt.xlabel(column)
                    plt.ylabel('Proportion')
                    plt.xticks(rotation=45)
                    plt.show()
                    filename = f"categorical_stacked_barplot_{column}.png"
                    if output_dir:
                        filename = os.path.join(output_dir, filename)
                    plt.savefig(filename)
                    plt.show()
                    plt.close()
