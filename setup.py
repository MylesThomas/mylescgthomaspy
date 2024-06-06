from setuptools import setup, find_packages

VERSION = '0.0.2'
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
    # install_requires=[],
    install_requires=[line.strip() for line in open("requirements.txt", "r")],
    keywords=KEYWORDS_LIST,
    classifiers= [
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        'License :: OSI Approved :: MIT License',
        "Programming Language :: Python :: 3",
    ]
)
