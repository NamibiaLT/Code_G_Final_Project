from collections import defaultdict
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
from parse_kaggle import get_cleaned_dataframe
from wordcloud import WordCloud


STOPWORDS = set(stopwords.words('english') +
                ['das', 'es', 'en', 'de', 'la', 'ne', 'ist', 'pour', 'ma', 'vie', 'ce', 'la', 'mir', 'high', 'ever',
                 'fa', 'un', 'bon', 'belle', 'mos', 'NaN', 'travail', 'den', 'die', 'gestion', 'un', 'ist', 'one',
                 'start', 'oft', 'bom', 'sind', 'um', 'sur', 'tout', 'bonne', 'na', 'york', 'id', 'dont', 'also', 'inn',
                 'warehouse', 'place', 'bien', 'name', 'many', 'large', 'none', 'let', 'work', 'company', 'lot', 'job',
                 'working', 'associate', 'two', 'lots', 'put', 'dtype', 'mon', 'se', 'summary_cleaned', 'wo', 'nach',
                 'leuk', 'accountant', 'sometimes', 'kind', 'bas', 'bid', 'salle', 'pendant', 'theres', 'bout',
                 'changement', 'fo', 'encore', 'longue', 'yo', 'th', 'nous', 'welt', 'petit', 'par', 'sie', 'cadre'])


def get_wordclouds_for_companies(df=None, fields=['summary_cleaned', 'pros_cleaned', 'cons_cleaned'],
                                 company_filter=None, width=1000, height=1000):
    """
    Generate word clouds for each of the reviews for each of the companies in the dataframe
    Args:
        df (pd.df): Dataframe to use for analysis. If none, will generate from employee_reviews.csv
        fields (list):  optional list of review fields to generate wordclouds for. Options = 'summary_cleaned',
        'pros_cleaned', 'cons_cleaned'. Defaults to all three.
        company_filter (list): optional list of companies to limit analysis to. Defaults to None
        width (int): optional width param for wordcloud
        height (int): optional height param for wordcloud
    Return:
        A collections.defaultdict object of structure:

            defaultdict(<class 'dict'>,
            {'cons_cleaned': {'amazon': <wordcloud.wordcloud.WordCloud object at 0x13b2cdf98>,
                              'apple': <wordcloud.wordcloud.WordCloud object at 0x1409ab8d0>,
                              'facebook': <wordcloud.wordcloud.WordCloud object at 0x144b2f7f0>,
                              'google': <wordcloud.wordcloud.WordCloud object at 0x116ecd4a8>,
                              'microsoft': <wordcloud.wordcloud.WordCloud object at 0x116ecd550>,
                              'netflix': <wordcloud.wordcloud.WordCloud object at 0x14eee5278>},
             'pros_cleaned': {'amazon': <wordcloud.wordcloud.WordCloud object at 0x144c8def0>,
                              'apple': <wordcloud.wordcloud.WordCloud object at 0x14c51ca58>,
                              'facebook': <wordcloud.wordcloud.WordCloud object at 0x143c4df60>,
                              'google': <wordcloud.wordcloud.WordCloud object at 0x131c57080>,
                              'microsoft': <wordcloud.wordcloud.WordCloud object at 0x120ffa518>,
                              'netflix': <wordcloud.wordcloud.WordCloud object at 0x144d54e10>},
             'summary_cleaned': {'amazon': <wordcloud.wordcloud.WordCloud object at 0x13944c5c0>,
                                 'apple': <wordcloud.wordcloud.WordCloud object at 0x143595588>,
                                 'facebook': <wordcloud.wordcloud.WordCloud object at 0x13a4ad400>,
                                 'google': <wordcloud.wordcloud.WordCloud object at 0x119b7b828>,
                                 'microsoft': <wordcloud.wordcloud.WordCloud object at 0x144d615f8>,
                                 'netflix': <wordcloud.wordcloud.WordCloud object at 0x14612cda0>}})

    """
    # If no dataframe is provided, generate from employee_reviews.csv
    if df is None:
        df = get_cleaned_dataframe()
    companies = list(company_filter) if company_filter else [company for company in df['company'].unique()]
    wordclouds = defaultdict(dict)
    for field in fields:
        for company in companies:
            wordclouds[field][company] = WordCloud(
                width=width,
                height=height,
                stopwords=STOPWORDS
            ).generate(str(df[df['company'] == company][field]))
    return wordclouds


def save_images(wordcloud_dict):
    """
    Save wordcloud images to ./images/ folder. Format of filename is {company}_{field}.jpg
    """
    for field in wordcloud_dict.keys():
        for company in wordcloud_dict[field].keys():

            plt.imshow(wordcloud_dict[field][company], interpolation='bilinear')
            plt.axis('off')
            plt.tight_layout(pad=0)
            plt.savefig(f'../../backend/static/images/{company}_{field}.jpg')


if __name__ == "__main__":
    """
    Generate word clouds and save the images to the images/ folder in the current working directory
    >>> python generate_wordcloud.py
    """
    wordclouds = get_wordclouds_for_companies()
    save_images(wordclouds)
