import datetime as dt
import numpy as np
import nltk
import pandas as pd
from reviews_app.model import parse_kaggle as pk
import pytest

from string import punctuation, digits


NON_ENGLISH_REVIEW = 'um es mit den worten eines kollegen auszudrück sehr'


def make_dummy_dataframe():
    companies = ['amazon', 'google', 'facebook']
    job_titles = ['Current Employee - Anonymous Employee', 'Former Employee - Software Engineer', 'Current Employee - Manager']
    company_list = [companies[x] for x in np.random.randint(0, 2, 100)]
    job_title_list = [job_titles[x] for x in np.random.randint(0, 2, 100)]
    dummy_df = pd.DataFrame()
    dummy_df['company'] = company_list
    dummy_df['job-title'] = job_title_list
    return dummy_df


DUMMY_DF = make_dummy_dataframe()


def test_add_position_and_employment_status_no_filter():
    df = pk.add_position_and_employment_status(DUMMY_DF)
    assert isinstance(df, pd.core.frame.DataFrame)
    assert list(df.columns) == ['company', 'job-title', 'current_employee', 'position']


def test_add_position_and_employment_status_single_filter():
    df = pk.add_position_and_employment_status(DUMMY_DF, ['amazon'])
    assert isinstance(df, pd.core.frame.DataFrame)
    assert list(df.columns) == ['company', 'job-title', 'current_employee', 'position']
    assert list(df['company'].unique()) == ['amazon']


def test_add_position_and_employment_status_multiple_filter():
    df = pk.add_position_and_employment_status(DUMMY_DF, ['amazon', 'google'])
    assert isinstance(df, pd.core.frame.DataFrame)
    assert list(df.columns) == ['company', 'job-title', 'current_employee', 'position']
    assert list(df['company'].unique()) == ['amazon', 'google']


def test_add_position_and_employment_status_assert_error():
    """
    Assert error is raised when company filter is not provided as a list
    :return:
    """
    with pytest.raises(TypeError):
        pk.add_position_and_employment_status(DUMMY_DF, 'amazon')


def test_parse_datetime():
    pass
