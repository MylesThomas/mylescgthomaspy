# Instructions

---

# Setup

1. [Python](https://www.python.org/downloads/) installed on your system
2. A [CircleCI](https://circleci.com/signup/) account
3. A [GitHub](https://github.com/) account
4. Accounts at [test.pypi.org](https://test.pypi.org/account/register/) and [pypi.org](https://pypi.org/)
- test.pypi.org: allows you to try distribution tools and processes without affecting the real index
- pypi.org: affects the real index
    - Setting up TestPyPI: Google Authenticator -> Add a code -> Scan a QR code -> Enter the 6 digit code at https://test.pypi.org/manage/account/totp-provision
    - Setting up PyPI: Google Authenticator -> Add a code -> Scan a QR code -> Enter the 6 digit code at https://pypi.org/manage/account/totp-provision

Notes:
- MAKE SURE to do this action for both TestPyPI and PyPI (!!!)
- Authentication app of choice: [Google Authenticator](https://apps.apple.com/us/app/google-authenticator/id388497605)


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

```bash
python setup.py sdist bdist_wheel
```

This command creates a source distribution AND a shareable wheel that can be published on [pypi.org](https://pypi.org/).

Location of the files:
- source distribution: C:\Users\Myles\mylescgthomaspy\dist\mylescgthomaspy-0.0.1.tar.gz
- shareable wheel: C:\Users\Myles\mylescgthomaspy\dist\mylescgthomaspy-0.0.1-py3-none-any.whl
    - shareable wheel is faster than source distribution, it is built already


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

4. Then, install the `mylescgthomaspy` package using the wheel distribution you created at the start of this section:

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
# OR
python C:\Users\Myles\test.py
```

If you see no errors, our Python package is ready for publishing!

## Publishing the Python package

First, we will first publish our package to test.pypi.org to make sure everything is working.

When we are ready to publish to our package users, we will move on to pypi.org.

Start by installing `twine` and publish to test.pypi.org.

Notes:
- You will be asked to enter your credentials for the site ie. an API token that you can get/add from [here](https://test.pypi.org/manage/account/)
    - To log into test.pypi.org, authenticate using the Google Authenticator app on your phone
    - I created a token called `global_token` with Scope for my entire account

Required: Repeating the above steps, but for PyPI (You will need this setup later for the pypi_publish step)
- https://pypi.org/manage/account/
- Make sure you authenticate via Google Authenticator app on your phone
- Create an API token named `global_token` with Scope for entire account

Optional: Adding a .pypirc file
- Navigate to your user profile in the file explorer: %USERPROFILE%
- Create a file named .pypirc -> copy/paste contents from TestPyPI -> Save As no extension (so that .txt does not get added by your text editor)

Here is what my file looks like right now:

```bash
# C:\Users\Myles\.pypirc
[testpypi]
  username = __token__
  password = pypi- ...

[pypi]
  username = __token__
  password = pypi- ...

```

We can proceed with testing out the package on test.pypi.org to make sure everything is working!

In the root folder: (Make sure you are not using the test environment)

```bash
pip install twine
twine upload --repository testpypi dist/*
```

Note: If it asks for your API Token, when you paste it in, the terminal will not show it on your screen (for security reasons I'd assume). Just paste and press enter.

You can now view your package on test.pypi.org: https://test.pypi.org/project/mylescgthomaspy/0.0.1/

In a separate Python virtual environment, pip install the package.

First, deactivate the terminal that had your first virtual environment open:

```bash
deactivate
rmdir /s /q env
```

Notes:
- The 2nd call MIGHT only work if you are in an Admin command prompt. You can simply remove this folder via the file directory if that is easier.
    - /s: Delete the specified directory AND all subdirectories
    - /q: Run the command in quiet mode ie. don't ask for confirmation

Next, this is what I called from C:\Users\Myles ie. %USERPROFILE%

```bash
py -m venv env
.\env\Scripts\activate

pip install pandas
pip install numpy
pip install matplotlib
pip install seaborn

pip install --index-url https://test.pypi.org/simple mylescgthomaspy
python test.py
```

Notes:
- When you run pip install <package-name>, pip searches for the package files in the official Python Package Index, on pypi.org.
    - We have not published to pypi.org yet, so we need to specify that we are downloading from test.pypi.org
        - --index-url https://test.pypi.org/simple/: This option tells pip to use a custom package index for the installation instead of the default PyPI (Python Package Index). The URL provided (https://test.pypi.org/simple/) points to the TestPyPI server
        - mylescgthomaspy: This is the name of the package that is being installed from TestPyPI

Error warning: TestPyPI had trouble downloading pandas, so I had to `pip install` all of my requirements, after creating the virtual environment, but before downloading `mylescgthomaspy`.

Optional: Publish our package to pypi.org to make sure everything is working
- I did not do this, nor does the reference material, so continue on to automating this process

Success! Now we can automate the publishing process with CircleCI.

## Automating package publishing with CircleCI

CircleCI: Great for automating scripts
- Also great for creating a repeatable process for package publication.

We will create a process that can:
- Upgrade from Test PyPI to PyPI
- Maintain checks (if you include tests)
- Allow credentials to be used only by the pipeline, without sharing with every developer working on the package

To begin, from your root directory, create a folder named `tests`. In it, create a file and name it test_temperature.py.

```bash
mkdir tests
cd tests
echo > test_1.py
```

In tests/test_1.py, enter:

```py
# ./tests/test_1.py
from mylescgthomaspy.data import download_nfl_data

def test_1():
    assert 1 == 1

def test_2():
    assert 2 == 2

def test_nfl_data_exists():
    df = download_nfl_data(range(2018, 2020 + 1), ["posteam", "wp", "play_type"])
    num_rows = df.shape[0]
    assert num_rows > 0

```

Head back to the virtual environment containing our `mylescgthomaspy` package.

Go to the root folder. Pip install pytest, then run the pytest command:

```bash
cd mylescgthomaspy

pip install pytest
pytest
```

All 3 tests should pass successfully. (You should see something like this)

```bash
(env) C:\Users\Myles\mylescgthomaspy>pytest
=============================================== test session starts ===============================================
platform win32 -- Python 3.11.4, pytest-8.2.2, pluggy-1.5.0
rootdir: C:\Users\Myles\mylescgthomaspy
collected 3 items

tests\test_1.py ...                                                                                          [100%]

================================================ 3 passed in 5.95s ================================================ 

(env) C:\Users\Myles\mylescgthomaspy>
```

Next, add a CircleCI configuration file to the project.
- Create a folder named .circleci
- In the new folder, create a file named config.yml

```bash
mkdir .circleci
cd .circleci
echo > config.yml
```

In .circleci/config.yml, copy and paste:

```bash
# ./.circleci/config.yml
version: 2.1
jobs:
  build_test:
    docker:
      - image: cimg/python:3.11.0
    steps:
      - checkout # checkout source code to working directory
      - run:
          command: | # create whl and use pipenv to install dependencies
            python3 setup.py sdist bdist_wheel
            sudo add-apt-repository universe -y
            sudo apt-get update
            sudo apt install -y python3-pip
            sudo pip install pipenv
            pipenv install dist/mylescgthomaspy-0.0.1-py3-none-any.whl # make sure version of mylescgthomaspy is correct with what is currently on your disk in /dist
            pipenv install pytest
      - run:
          command: | # Run test suite
            pipenv run pytest
  test_pypi_publish:
    docker:
      - image: cimg/python:3.11.0
    steps:
      - checkout # checkout source code to working directory
      - run:
          command: | # create whl, install twine and publish to Test PyPI
            python3 setup.py sdist bdist_wheel
            sudo add-apt-repository universe -y
            sudo apt-get update
            sudo apt install -y python3-pip
            sudo pip install pipenv
            pipenv install twine
            pipenv run twine upload --repository testpypi dist/*
  pypi_publish:
    docker:
      - image: cimg/python:3.11.0
    steps:
      - checkout # checkout source code to working directory
      - run:
          command: | # create whl, install twine and publish to PyPI
            python3 setup.py sdist bdist_wheel
            sudo add-apt-repository universe -y
            sudo apt-get update
            sudo apt install -y python3-pip
            sudo pip install pipenv
            pipenv install twine
            pipenv run twine upload dist/*
workflows:
  build_test_publish:
    jobs:
      - build_test
      - test_pypi_publish:
          requires:
            - build_test
          filters:
            branches:
              only:
                - develop
      - pypi_publish:
          requires:
            - build_test
          filters:
            branches:
              only:
                - main
```

Note: Line 15 must be updated to reflect the current version (We are still using mylescgthomaspy version-0.0.1)

This configuration file instructs the pipeline to install the necessary dependencies, run tests, and publish the package.

The workflow part of the configuration specifies filters, the sequence the jobs should be executed in, and their dependencies.

For example:
- the jobs `test_pypi_publish` and `pypi_publish` cannot run if the `build_test` job fails.
- The `test_pypi_publish` and `pypi_publish` jobs run only in the develop and main branches, respectively.

## Connecting the project to CircleCI

First, push your project to Github:

```bash
git add .
git commit -m "Automated package publishing, prepared to connect project to CircleCI"
git push
```

Your repository should be similar to [this](https://github.com/CIRCLECI-GWP/publish-python-package/tree/circleci).

Next, login to your [CircleCI account](https://app.circleci.com/home/).

Note: If you signed up with your GitHub account (which you should), all your repositories will be available on the dashboard. Click 'Set Up Project' next to your `mylescgthomaspy` project.
- Connecting your Github:
    - https://app.circleci.com/home/ -> Top Right User Profile -> User Settings
    - GitHub -> 'Connect' -> Authorize circleci
    - Organizations -> MylesThomas -> Set up a project -> mylescgthomaspy -> 'Set Up Project' -> Fastest
        - repository: mylescgthomaspy
        - branch: main (you have to type this in)

Once the workflow status is done working, you will shortly get an email with the results of this workflow.
- The build_test job will pass, but if you are in either the main or develop branches, expect the build to fail
    - That is because the test_pypi_publish and pypi_publish jobs cannot run yet
        - Test PyPI credentials were expected when we published the package using twine, we could not interact with the terminal while it was running the command in the pipeline.
        - To supply these credentials, we could add flags to the command: twine upload -u USERNAME -p PASSWORD.
            - However, because the config file is tracked by Git, and our Git repository is public, using the flags would be a security risk. We can avoid this risk by creating environment variables.

Let's start by creating environment variables to try and remedy this.

## Creating environment variables

While still on the CircleCI project (mylescgthomaspy), cancel the workflow (if needed) and click Project Settings on the top right part of the page.
- Environment Variables -> Add Environment Variable
    - 1: Name: TWINE_USERNAME; Value: mylesthomas
    - 2: Name: TWINE_PASSWORD; Value: ...

Note: These credentials are the username + password for your account at PyPI.org. (Remember, although we have not pushed to PyPI.org yet, we should have set up an identical account to the TestPyPI.org, which we have already pushed to once)

Next, we will create a change log to track the changes in our package.

### Adding a change log

Head to the root directory and do the following:

```bash
echo > CHANGELOG.md
```

```markdown
# Change Log

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).

## [0.0.2] - 2024-06-06

### Added

- Added PyPI credentials to connect the project to CircleCI

```

To make sure the build succeeds, we also need to bump the version in setup.py to 0.0.2 to match the change log.

```py
# ./setup.py
from setuptools import setup, find_packages

VERSION = '0.0.2'

...

```

One last thing: In order for the build_test to run, you must update the `.circleci/config.yml` to match the VERSION in `setup.py`.
- In line 15, change 0.0.1 to 0.0.2
    - In line 10, `python3 setup.py sdist bdist_wheel` will update the wheel/.whl file in ./dist to reflect the VERSION in `setup.py`

```bash
# ./.circleci/config.yml
...

bdist_wheel
pipenv install dist/mylescgthomaspy-0.0.2-py3-none-any.whl

...

```

Important Note: If you don’t bump the version, the publishing job will fail because you cannot publish the same version twice.

Next, Commit the changes and push to GitHub to trigger a build.

```bash
git add .
git commit -m "Added PyPI credentials, created CHANGELOG, upgraded to version 0.0.2"
git push
```

Head to https://app.circleci.com/pipelines/github/MylesThomas to check and see if your build passes!

## Updating the package

---

## References

1. [Circle CI Blog - Publishing a Python package](https://circleci.com/blog/publishing-a-python-package/?utm_source=google&utm_medium=sem&utm_campaign=sem-google-dg--uscan-en-dsa-tROAS-auth-nb&utm_term=g_-_c__dsa_&utm_content=&gclid=Cj0KCQjwr82iBhCuARIsAO0EAZyyFRP4uLE-m1VslA7nHWiY9ooZFrwcw48eACHOSiJOPCRpHRGEVSMaAmnvEALw_wcB)
2. [nflfastR Python Guide](https://gist.github.com/Deryck97/dff8d33e9f841568201a2a0d5519ac5e)
3. [PyPI - Common questions - API Tokens](https://pypi.org/help/#apitoken)
4. []()
5. []()
6. []()
