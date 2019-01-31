import numpy as np
import pandas as pd
from string import punctuation

MAPPING = str.maketrans("", "", punctuation)


def add_position_and_employment_status(df, company_filter=None):
    """
    Return relevant fields. Add new columns for position and whether employee is
    currently employed from job title col.
    """
    df['current_employee'] = df['job-title'].str.split('-').str[0]
    df['position'] = df['job-title'].str.split('-').str[1]
    new_df = df[['company', 'summary', 'current_employee', 'position', 'pros', 'cons', 'advice-to-mgmt',
                 'overall-ratings', 'work-balance-stars', 'culture-values-stars', 'comp-benefit-stars',
                 'senior-mangemnet-stars']]
    if company_filter:
        return new_df[new_df['company'] == company_filter]
    else:
        return new_df


def standardize_null(df):
    df = df.replace('none',np.NaN)
    return df


def clean_columns_for_nlp(df, columns):
    for column in columns:
        if column in ['pros', 'cons', 'advice-to-mgmt']:
            new_col = column + '_cleaned'
            df[new_col] = df[column].apply(lambda x: str(x).lower())
            df[new_col] = df[new_col].apply(lambda x: str(x).translate(MAPPING))
        else:
            # Lower case
            df[column] = df[column].apply(lambda x: str(x).lower())
            # Remove punctuation
            df[column] = df[column].apply(lambda x: str(x).translate(MAPPING))
    return df


def filter_out_null(df, column):
    return df[df[column].notnull()][['company', column]]


# Create function for null value


if __name__ == "__main__":
    # Todo: Put all of these in one big fxn
    reviews = pd.read_csv('employee_reviews.csv', index_col=0)
    reviews = standardize_null(reviews)
    reviews = add_position_and_employment_status(reviews, 'amazon')
    reviews = clean_columns_for_nlp(reviews, ['summary', 'pros', 'cons', 'advice-to-mgmt'])

    # Pull out a df to do analysis with (Company, star column)
    comp_benefit_stars_notnull = filter_out_null(reviews, 'comp-benefit-stars')

