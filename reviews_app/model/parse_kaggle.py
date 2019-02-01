import datetime as dt
import numpy as np
import nltk
from nltk.corpus import stopwords, words
import pandas as pd
from string import punctuation, digits
from zipfile import ZipFile

PUNCTUATION_MAPPING = str.maketrans("", "", punctuation)
DIGIT_MAPPING = str.maketrans("", "", digits)
STOPWORDS = stopwords.words('english')
ENGLISH_WORDS = set(words.words())


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
    if company_filter and type(company_filter) != list:
        raise TypeError("Argument company_filter must be a list! For example, ['amazon']")
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


def remove_nonenglish_words(value):
    """
    Remove non-English words from reviews
    """
    return str(' '.join([word for word in value.split() if word in ENGLISH_WORDS]))


def remove_stopwords_from_value(value):
    """
    Remove stopwords from string

    Example:
        >>> remove_stopwords_from_value('not perfect but still the best place in the world to work')
        'perfect still best place world work'

    """
    return str(' '.join([word for word in value.split() if word not in STOPWORDS and word in ENGLISH_WORDS]))


def clean_columns_for_nlp(df, columns, remove_stopwords=False):
    """
    Prepare & clean data for natural language processing (NLP). This includes removing punctuation & digits,
    lowercasing strings, and converting the `date` field into a parsable date object

    Args:
        df (pd.df): pandas dataframe
        columns (list): list of columns to process for NLP
        remove_stopwords (bool): if provided, remove stopwords from columns

    Returns:
        Pandas dataframe that has been processed for NLP
    """

    clean_ops = [str.lower, remove_punctuation, remove_nonenglish_words, remove_digits, str.strip]
    for column in columns:
        # Need to make a new column for the following columns, leaving original data separate
        if column in ['summary', 'pros', 'cons']:
            # If remove_stopwords argument provided, then add this function to list of operations before removing
            # punctuation. Remove `remove_nonenglish_words` operation since this step is included in `remove_stopwords`
            if remove_stopwords:
                clean_ops.insert(1, remove_stopwords_from_value)
                clean_ops.remove(remove_nonenglish_words)
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


def get_cleaned_dataframe(company_filter=None, remove_stopwords=False):
    """
    Puts all the functions together and returns a cleaned dataframe
    Args:
        company_filter (list): if provided, only return data for list of companies provided. Defaults to None.
        remove_stopwords (boolean): if True, remove stopwords from review columns. Defaults to False.

    Return:
        cleaned dataframe
    """
    extract_review_data()
    reviews = pd.read_csv('employee_reviews.csv', index_col=0, na_values=['None', 'none'])
    reviews = add_position_and_employment_status(reviews, company_filter)
    reviews = clean_columns_for_nlp(reviews, ['summary', 'pros', 'cons'], remove_stopwords)
    return reviews


def display_random_review(df, company, field):
    """
    Display a random review given a company and field
    Args:
        df (pd.df): a pandas dataframe containing containing a company and review field
        company (string): One of the following companies: 'google', 'amazon', 'facebook', 'netflix', 'apple', 'microsoft'
        field (string): One of the following fields: 'summary', 'pros', 'cons'

    Returns:
        A random review
    """
    return df[df['company'] == company][field].sample()


if __name__ == "__main__":
    """
    Run on command line to output csv of cleaned employee_reviews data. Ready for import into pandas
    >>> python parse_kaggle.py
    """
    cleaned_df = get_cleaned_dataframe()
    cleaned_df.to_csv('employee_reviews.cleaned.csv', index=False)


