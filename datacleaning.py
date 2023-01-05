import pandas as pd
import numpy as np
import re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from tqdm import trange

# import nltk
# nltk.download('stopwords')
# nltk.download('wordnet')

# read data from csv, the columns are divided by ','
# use column 'index' as the index column
issues = pd.read_csv('info.csv', header=None, sep=',', names=['index', 'url', 'title', 'label'], index_col='index')

# do not use the url column
issues = issues.drop(columns=['url'])

# replace the NaN with 1
issues.fillna('NaN', inplace=True)

for i in trange(len(issues)):
    # only left the english characters
    words = re.sub('[^a-zA-Z]', ' ', issues['title'][i])
    words = (words.lower()).split()
    # drop the stopwords
    words = [w for w in words if w not in set(stopwords.words('english'))]

    # lemmatize(词形还原)
    lemma = WordNetLemmatizer()
    words = [lemma.lemmatize(w) for w in words if len(w) > 1]
    if len(words) < 3:
        issues.drop(index=i, inplace=True)
    else:
        words = ' '.join(words)
        issues['title'][i] = words

issues = issues.reset_index(drop=True)

for i in trange(len(issues)):
    # only left the english characters
    words = issues['label'][i]
    words = (words.lower()).split()

    # lemmatize(词形还原)
    lemma = WordNetLemmatizer()
    words = [lemma.lemmatize(w) for w in words if len(w) > 1]
    words = ' '.join(words)
    issues['label'][i] = words

valid_label = ['content', 'invalid', 'action', 'engineering']

issues['type'] = ['train' for _ in range(len(issues))]
for i in trange(len(issues)):
    if issues['label'][i] not in valid_label:
        issues['label'][i] = 'other'
    if i % 5 == 0:
        issues['type'][i] = 'test'

print(issues[['title', 'label', 'type']].groupby('label')['title'].count().nlargest(5))


issues.to_csv('clear.csv')
