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
issues.fillna(1, inplace=True)

for i in trange(len(issues)):
    # only left the english characters
    words = re.sub('[^a-zA-Z]', ' ', issues['title'][i])
    words = (words.lower()).split()
    # drop the stopwords
    words = [w for w in words if w not in set(stopwords.words('english'))]

    # lemmatize
    lemma = WordNetLemmatizer()
    words = [lemma.lemmatize(w) for w in words if len(w) > 1]

    words = ' '.join(words)
    issues['title'][i] = words

issues.to_csv('clear.csv')
