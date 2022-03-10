import warnings
import pickle
import time
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline

warnings.filterwarnings('ignore')
start = time.time()

# загружаем данные
train = pd.read_csv('train.csv')
# количество отзывов в выборке
print(f'Количество отзывов: {len(train.data)}')
# доля класса 1 в выборке
portion_1 = sum(train.label) / len(train.label)
print(f'Доля класса 1: {portion_1}')

# обучаем модель
pipe_final = Pipeline([('vect', TfidfVectorizer(ngram_range=(1, 3))),
                       ('clf', LinearSVC(C=1, max_iter=10))])
pipe_final.fit(train.data, train.label)
# сохраняем модель
pickle.dump(pipe_final, open('trained_classifier.pickle', 'wb'))

print('DONE for: ' + str(time.time() - start))


