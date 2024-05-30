# Instructions

---

# Setup

1. [Python](https://www.python.org/downloads/) installed on your system
2. A [CircleCI](https://circleci.com/signup/) account
3. A [GitHub](https://github.com/) account
4. Accounts at [test.pypi.org](https://test.pypi.org/account/register/) and [pypi.org]()
- test.pypi.org: allows you to try distribution tools and processes without affecting the real index
- pypi.org: 

Note: Authentication app of choice: [Google Authenticator](https://apps.apple.com/us/app/google-authenticator/id388497605)
- Setting up TestPyPI: Google Authenticator -> Add a code -> Scan a QR code -> Enter the 6 digit code at https://test.pypi.org/manage/account/totp-provision

# Creating a Python package

Hundreds of thousands of packages available on [pypi.org](https://pypi.org/). You can search for the functionality you need, or choose from packages that are trending or new.

## Project structure

Choose a location in your system and create a project:

```
python-package (mylescgthomaspy)
├── mylescgthomaspy
│   ├── __init__.py
│   ├── ...
│   └── etl.py
├── .gitignore
└── setup.py

```

The project has:

- A base folder named python-package (you can use any name you prefer, I used mylescgthomaspy for Github reasons)
- A module/library folder named mylescgthomaspy (this is the actual package)
- Python file(s) within the package folder
    - __init__.py
    - data.py
    - eda.py
    - etl.py

Before proceeding, make sure that the module/library folder name is a unique name that is not used by an existing package in the Test Python Package Index [test.pypi.org](https://test.pypi.org/) or the Python Package Index [pypi.org](https://pypi.org/).

With the project created and named, we can begin building functionality.

Copy the following code into the following files:

```py
# ./mylescgthomaspy/data.py
import pandas as pd

def download_nfl_data(years, cols_of_interest):
    data = pd.DataFrame()
    for YEAR in years:  
        i_data = pd.read_csv('https://github.com/nflverse/nflverse-data/releases/download/pbp/' \
                    'play_by_play_' + str(YEAR) + '.csv.gz',
                    compression= 'gzip', low_memory= False)
        # data = data.append(i_data, sort=True)
        data = pd.concat(objs=[data, i_data])
        data = data[cols_of_interest]
        return data

```

```py
# ./mylescgthomaspy/etl.py
import pandas as pd

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

```

```py
# ./mylescgthomaspy/eda.py
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

```

Next, copy this code into __init__.py file:

```py
# ./mylescgthomaspy/__init__.py
from .data import download_nfl_data
from .etl import convert_dtypes
from .eda import generate_eda_plots, generate_relationship_plots

```

Next, create a requirements.txt file (in the root directory) for installing the necessary dependencies.

```py
# ./requirements.txt
pandas
numpy
matplotlib
seaborn
```

This will initialize the package and simplify the imports between modules in the package.

Copy the following code into setup.py, and then update AUTHOR_NAME, AUTHOR_EMAIL_ADDRESS, and KEYWORDS_LIST using your information:

```py
# ./setup.py
from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'A package to assist with machine learning and data science tasks'
LONG_DESCRIPTION = 'A package that makes it easy to get a data science/machine learning project from end-to-end with good software engineering hygiene'

AUTHOR_NAME = "Myles Thomas"
AUTHOR_EMAIL_ADDRESS = "mylescgthomas@gmail.com"
KEYWORDS_LIST = 'data science machine learning'

setup(
    name="mylescgthomaspy",
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    author=AUTHOR_NAME,
    author_email=AUTHOR_EMAIL_ADDRESS,
    license='MIT',
    packages=find_packages(),
    install_requires=[line.strip() for line in open("requirements.txt", "r")],
    keywords=KEYWORDS_LIST,
    classifiers= [
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        'License :: OSI Approved :: MIT License',
        "Programming Language :: Python :: 3",
    ]
)

```

To finish this step, can use the GitHub .gitignore [template for Python](https://github.com/github/gitignore/blob/main/Python.gitignore). Copy the contents into this projects's .gitignore file (in the root directory).

The code should be similar to [this](https://github.com/CIRCLECI-GWP/publish-python-package/tree/setup).

## Setting up Version Control with Github

1. Create a new repository on [Github](https://github.com/new)
- Repository name: mylescgthomaspy (same as root directory AND folder with code files)

2. Option #1: ...or create a new repository on the command line

```bash
cd mylescgthomaspy

echo "# mylescgthomaspy" >> README.md
git init
git add README.md
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/MylesThomas/mylescgthomaspy.git
git push -u origin main
```

You are connected to Github!

## Building the package files

In your terminal (at the root of the project) run:

```
python setup.py sdist bdist_wheel
```

This command creates a source distribution AND a shareable wheel that can be published on [pypi.org](https://pypi.org/).

Location of the files:
- source distribution: C:\Users\Myles\mylescgthomaspy\dist\mylescgthomaspy-0.0.1.tar.gz
- shareable wheel: C:\Users\Myles\mylescgthomaspy\dist\mylescgthomaspy-0.0.1-py3-none-any.whl
    - faster than source distribution, it is built already

To test this (before publishing), create a virtual Python environment and test it out there.

Note: Use a different location to prevent name-clashing between modules.
- Example: C:\Users\Myles

Instructions to test out the package in a virtual environment:
1. Open a new terminal/command prompt
- Should open to C:\Users\Myles

2. Create a new virtual environment/venv named 'env'

```bash
py -m venv env
```

3. Activate the virtual environment/venv:

```bash
.\env\Scripts\activate
```

Notes:
- This is because the python.exe file for the venv is here: C:\Users\Myles\env\Scripts
- There should be a (env) before your calls in the terminal now

4. Then, install the `mylescgthomaspy` package using the wheel distribution:

```bash
pip install C:\Users\Myles\mylescgthomaspy\dist\mylescgthomaspy-0.0.1-py3-none-any.whl
```

Note: Calling `pip list` before and after should look something like this (due to downloading all packages and required dependencies from requirements.txt):

```bash
# Before
(env) C:\Users\Myles>pip list
Package    Version
---------- -------
pip        23.1.2 
setuptools 65.5.0 

# ----------------------------------

# After
(env) C:\Users\Myles>pip list
Package         Version
--------------- -----------
contourpy       1.2.1
cycler          0.12.1
fonttools       4.52.4
kiwisolver      1.4.5
matplotlib      3.9.0
mylescgthomaspy 0.0.1
numpy           1.26.4
packaging       24.0
pandas          2.2.2
pillow          10.3.0
pip             23.1.2
pyparsing       3.1.2
python-dateutil 2.9.0.post0
pytz            2024.1
seaborn         0.13.2
setuptools      65.5.0
six             1.16.0
tzdata          2024.1
```

5. Create a python script file named `test.py` and enter:

```py
# C:\Users\Myles\test.py
import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from mylescgthomaspy.data import download_nfl_data
from mylescgthomaspy.etl import convert_dtypes
from mylescgthomaspy.eda import generate_eda_plots, generate_relationship_plots

SCRIPT_DIR = os.getcwd()
PARENT_DIR = os.path.dirname(SCRIPT_DIR)
INPUT_DIR = os.path.join(PARENT_DIR, "00_INPUT/")
INTER_DIR = os.path.join(PARENT_DIR, "01_INTERMEDIATE/")
OUTPUT_DIR = os.path.join(PARENT_DIR, "02_OUTPUT/")

YEARS_LIST = range(2018, 2020 + 1)

COLS_OF_INTEREST_LIST = [
    "posteam",
#     "defteam",
#     "game_id",
#     "epa",
    "wp",
#     "def_wp",
#     "yardline_100",
#     "passer",
#     "rusher",
#     "receiver",
#     "cpoe",
#     "down",
    "play_type",
#     "series_success",
]

nfl_data = download_nfl_data(YEARS_LIST, COLS_OF_INTEREST_LIST)

print(nfl_data.columns)
print(nfl_data.dtypes)

nfl_data = convert_dtypes(nfl_data)

print(nfl_data.dtypes)

generate_eda_plots(nfl_data)

generate_relationship_plots(nfl_data, 'play_type', response_type='categorical')

print("test completed without error!")
```

Run the script:

```bash
python test.py
```

Our Python package is ready for publishing!

## Publishing the Python package





---

## References

1. [Circle CI Blog - Publishing a Python package](https://circleci.com/blog/publishing-a-python-package/?utm_source=google&utm_medium=sem&utm_campaign=sem-google-dg--uscan-en-dsa-tROAS-auth-nb&utm_term=g_-_c__dsa_&utm_content=&gclid=Cj0KCQjwr82iBhCuARIsAO0EAZyyFRP4uLE-m1VslA7nHWiY9ooZFrwcw48eACHOSiJOPCRpHRGEVSMaAmnvEALw_wcB)
2. [nflfastR Python Guide](https://gist.github.com/Deryck97/dff8d33e9f841568201a2a0d5519ac5e)
3. []()
4. []()
5. []()
6. []()
