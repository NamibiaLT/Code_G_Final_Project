import datetime as dt
import numpy as np
import pandas as pd
from string import punctuation, digits
from zipfile import ZipFile

PUNCTUATION_MAPPING = str.maketrans("", "", punctuation)
DIGIT_MAPPING = str.maketrans("", "", digits)


def extract_review_data():
    zipfile = ZipFile('google-amazon-facebook-employee-reviews.zip')
    zipfile.extractall()


def add_position_and_employment_status(df, company_filter=None):
    """
    Return relevant fields. Add new columns for position and whether employee is
    currently employed from job title col.

    Args:
        df (pd.df): pandas dataframe
        company_filter (list): optional, list of companies to limit analysis to. Defaults to None

    Returns:
        pandas dataframe with `current_employee` and `position` pulled out as separate fields

    """
    df['current_employee'] = df['job-title'].str.split('-').str[0]
    df['position'] = df['job-title'].str.replace('&amp,', '&').str.split('-').str[1]
    if company_filter:
        return df[df['company'].isin(company_filter)]
    else:
        return df


def parse_datetime(dates):
    """
    Convert date strings into a pandas PeriodArray/Index object

    Args:
        dates (pd.Series): Series of dates in the format ' %b %d, %Y'. Example: ' Dec 11, 2018'

    Returns:
        pd.Series of data type period, in the format '%Y-%m'. Example: 2018-12

    """

    return pd.to_datetime(dates, format=' %b %d, %Y', errors='coerce').dt.to_period('M')


def clean_strings(value, ops):
    """
    Perform a list of operations on a string

    Args:
        value (str): string to clean
        ops (list): list of operations/functions to perform

    Return:
        Cleaned value
    """

    for function in ops:
        value = function(value)
    return value


def remove_punctuation(value):
    """
    Remove punctuation from string. Punctuation comes from string.punctuation
    """
    return str(value).translate(PUNCTUATION_MAPPING) if pd.notnull(value) else value


def remove_digits(value):
    """
    Remove digits from string. Digits come from string.digits
    """
    return str(value).translate(DIGIT_MAPPING) if pd.notnull(value) else value


def clean_columns_for_nlp(df, columns):
    """
    Prepare & clean data for natural language processing (NLP). This includes removing punctuation & digits,
    lowercasing strings, and converting the `date` field into a parsable date object

    Args:
        df (pd.df): pandas dataframe
        columns (list): list of columns to process for NLP

    Returns:
        Pandas dataframe that has been processed for NLP
    """

    clean_ops = [str.strip, remove_punctuation, remove_digits, str.lower]
    for column in columns:
        # Need to make a new column for the following columns, leaving original data separate
        if column in ['pros', 'cons', 'advice-to-mgmt']:
            new_col = column + '_cleaned'
            df[new_col] = df[column].apply(lambda x: clean_strings(x, clean_ops) if pd.notnull(x) else x)
        else:
            df[column] = df[column].apply(lambda x: clean_strings(x, clean_ops) if pd.notnull(x) else x)
    df['dates'] = parse_datetime(df['dates'])
    return df


def filter_out_null(df, column):
    """
    Returns a pandas dataframe that has missing data removed. `Company` and `dates` are included in output in addition
    to the specified `column` argument

    Args:
        df (pd.df): pandas dataframe
        column (string): the column of interest for analysis

    Returns:
        a pandas dataframe with null values removed. Columsn = `column`, company, and dates

    Example:
        >>> for col in ['advice-to-mgmt','overall-ratings', 'work-balance-stars', 'culture-values-stars', \
        'comp-benefit-stars', 'senior-mangemnet-stars']:
                print(f'{col} : {len(filter_out_null(reviews, col))}')
        advice-to-mgmt : 37693
        overall-ratings : 67529
        work-balance-stars : 60369
        culture-values-stars : 53983
        comp-benefit-stars : 60368
        senior-mangemnet-stars : 59754

    """
    return df[df[column].notnull()][['company', 'dates', column]]


def get_cleaned_dataframe():
    """
    Puts all the functions together and returns a cleaned dataframe
    :return:
    """
    extract_review_data()
    reviews = pd.read_csv('employee_reviews.csv', index_col=0, na_values=['None', 'none'])
    reviews = add_position_and_employment_status(reviews)
    reviews = clean_columns_for_nlp(reviews, ['summary', 'pros', 'cons', 'advice-to-mgmt'])
    return reviews


if __name__ == "__main__":
    """
    Run on command line to output csv of cleaned employee_reviews data. Ready for import into pandas
    >>> python parse_kaggle.py
    """
    cleaned_df = get_cleaned_dataframe()
    cleaned_df.to_csv('employee_reviews.cleaned.csv', index=False)


