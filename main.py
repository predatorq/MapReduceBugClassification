import pandas as pd
import numpy as np
import re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from tqdm import trange

issues = pd.read_csv('clear.csv', header=None, sep=',', names=['index', 'title', 'label'], index_col='index')

print(issues[['title','label']].groupby('label')['title'].count().nlargest(15))
