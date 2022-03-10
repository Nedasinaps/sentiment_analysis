import pickle


class SentimentClassifier:
    def __init__(self):
        self.model = pickle.load(open('trained_classifier.pickle', 'rb'))
        self.classes_dict = {0: 'Негативный',
                             1: 'Позитивный',
                             -1: 'ОШИБКА: Что-то пошло не так:('}

    def predict_text(self, text):
        try:
            return self.model.predict([text])[0]
        except Exception:
            print("prediction error")
            return -1

    def get_prediction_message(self, text):
        prediction = self.predict_text(text)
        return self.classes_dict[prediction]


if __name__ == '__main__':
    clf = SentimentClassifier()
    pred = clf.get_prediction_message('Отличная мобила')
    print(pred)
    pred = clf.get_prediction_message('Доволен как слон')
    print(pred)
    pred = clf.get_prediction_message('Редкостная хрень')
    print(pred)
    pred = clf.get_prediction_message('Могли сделать и получше')
    print(pred)
