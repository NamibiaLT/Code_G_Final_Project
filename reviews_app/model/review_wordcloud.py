import nltk
import numpy as np
from nltk.corpus import stopwords
from wordcloud import WordCloud
import parse_kaggle as pk
stopwords = stopwords.words('english')
reviews = pk.get_cleaned_dataframe()

#Creating an array from text in columns pros, cons, and advice to management
pros_text = np.array(reviews['pros'])
cons_text = np.array(reviews['cons'])
advice_text = np.array(reviews['advice-to-mgmt'])

# Clean text for wordclouds
# Creating empty lists for iterating over text
pros_cleaned = []
cons_cleaned = []
advice_cleaned = []

# This saves words that arent in the list of stopwords to the cleaned list
for w in pros_text: 
    if w not in stopwords: 
        pros_cleaned.append(w) 

for w in cons_text: 
    if w not in stopwords: 
        cons_cleaned.append(w) 
    
for w in advice_text: 
    if w not in stopwords: 
        advice_cleaned.append(w) 

#The files created from this are pros_wordcloud.jpg, cons_wordcloud.jpg, and advice_wordcloud.jpg

#wordcloud creation for words in the pros column
wordcloud = WordCloud(
    width = 3000,
    height = 2000,
    background_color = 'black').generate(str(pros_cleaned))
fig = plt.figure(
    figsize = (40, 30),
    facecolor = 'k',
    edgecolor = 'k')
plt.imshow(wordcloud, interpolation = 'bilinear')
plt.axis('off')
plt.tight_layout(pad=0)
plt.savefig('pros_wordcloud.jpg')

#wordcloud creation for words in the cons column
wordcloud = WordCloud(
    width = 3000,
    height = 2000,
    background_color = 'black').generate(str(cons_cleaned))
fig = plt.figure(
    figsize = (40, 30),
    facecolor = 'k',
    edgecolor = 'k')
plt.imshow(wordcloud, interpolation = 'bilinear')
plt.axis('off')
plt.tight_layout(pad=0)
plt.savefig('cons_wordcloud.jpg')

#wordcloud creation for words in the advice to management column
wordcloud = WordCloud(
    width = 3000,
    height = 2000,
    background_color = 'black').generate(str(advice_cleaned))
fig = plt.figure(
    figsize = (40, 30),
    facecolor = 'k',
    edgecolor = 'k')
plt.imshow(wordcloud, interpolation = 'bilinear')
plt.axis('off')
plt.tight_layout(pad=0)
plt.savefig('advice_wordcloud.jpg')