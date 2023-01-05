import pandas as pd
import numpy as np
import re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from tqdm import trange

# import nltk
# nltk.download('stopwords')
# nltk.download('wordnet')

issues = pd.read_csv('info.csv', header=None, sep=',', names=['index', 'url', 'title', 'label'], index_col='index')

issues = issues.drop(columns=['url'])

issues.fillna(1, inplace=True)

for i in trange(len(issues)):
    words = re.sub('[^a-zA-Z]', ' ', issues['title'][i])
    words = (words.lower()).split()
    words = [w for w in words if w not in set(stopwords.words('english'))]

    lemma = WordNetLemmatizer()
    words = [lemma.lemmatize(w) for w in words if len(w) > 1]

    words = ' '.join(words)
    issues['title'][i] = words

issues.to_csv('clear.csv')
