import pandas as pd

# path to file here


def add_position_and_employment_status(df):
    """
    Return relevant fields. Add new columns for position and whether employee is
    currently employed from job title col.
    """
    df['current_employee'] = df['job-title'].str.split('-').str[0]
    df['position'] = df['job-title'].str.split('-').str[1]
    return df[['company', 'summary', 'current_employee', 'position', 'pros', 'cons', 'advice-to-mgmt',
               'overall-ratings', 'work-balance-stars', 'culture-values-stars', 'comp-benefit-stars',
               'senior-mangemnet-stars']]


if __name__ == "__main__":
    reviews = pd.read_csv('../input/employee_reviews.csv', index_col=0)
    reviews = add_position_and_employment_status(reviews)
