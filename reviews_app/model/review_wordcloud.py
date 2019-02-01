from collections import defaultdict
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
from wordcloud import WordCloud
from parse_kaggle import get_cleaned_dataframe


CLEANED_REVIEWS = get_cleaned_dataframe()
COMPANIES = [company for company in CLEANED_REVIEWS['company'].unique()]
STOPWORDS = set(stopwords.words('english') +
                ['das', 'es', 'en', 'de', 'la', 'ne', 'ist', 'pour', 'ma', 'vie', 'ce', 'la', 'mir', 'high', 'ever',
                 'fa', 'un', 'bon', 'belle', 'mos', 'NaN', 'travail', 'den', 'die', 'gestion', 'un', 'ist', 'one',
                 'start', 'oft', 'bom', 'sind', 'um', 'sur', 'tout', 'bonne', 'na', 'york', 'id', 'dont', 'also', 'inn',
                 'warehouse', 'place', 'bien', 'name', 'many', 'large', 'none', 'let', 'work', 'company', 'lot', 'job',
                 'working', 'associate', 'two', 'lots', 'put', 'dtype', 'mon', 'se', 'summary_cleaned', 'wo', 'nach',
                 'leuk', 'accountant', 'sometimes', 'kind', 'bas', 'bid', 'salle', 'pendant', 'theres', 'bout',
                 'changement', 'fo', 'encore', 'longue', 'yo', 'th', 'nous', 'welt', 'petit', 'par', 'sie', 'cadre'])


def get_wordclouds_for_companies(fields):
    df = CLEANED_REVIEWS
    wordclouds = defaultdict(defaultdict)
    for field in fields:
        for company in COMPANIES:
            wordclouds[field][company] = WordCloud(
                width=1000,
                height=1000,
                stopwords=STOPWORDS
            ).generate(str(df[df['company'] == company][field]))
    return wordclouds


def save_images(wordcloud_dict):
    for field in wordcloud_dict.keys():
        for company in wordcloud_dict[field].keys():

            plt.imshow(wordcloud_dict[field][company], interpolation='bilinear')
            plt.axis('off')
            plt.tight_layout(pad=0)
            plt.savefig(f'images/{company}_{field}.jpg')


if __name__ == "__main__":
    """
    Run on command line 
    >>> python review_wordcloud.py
    """
    wordclouds = get_wordclouds_for_companies(['summary_cleaned', 'pros_cleaned', 'cons_cleaned'])
    save_images(wordclouds)

