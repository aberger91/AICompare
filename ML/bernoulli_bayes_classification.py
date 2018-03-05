from sklearn.naive_bayes import BernoulliNB
from sklearn.model_selection import train_test_split
from sklearn import metrics
import numpy as np
import enum

from make_arff import create_and_load_arff
ARFF_PATH = 'data.arff'

def main():
    data, meta = create_and_load_arff(ARFF_PATH) 
    authors = list(meta['_author_'][1])
    li_data = data.tolist()

    data = [ np.array(x[1:], dtype=int) for x in li_data ]
    targets = [ np.int(authors.index(x[0].decode())) for x in li_data ]  # enumerate this
    x_train, x_test, y_train, y_test = train_test_split(data, targets, test_size=0.2)

    clf = BernoulliNB(binarize=None).fit(x_train, y_train)
    print(authors)
    print(clf.__class__.__name__)

    predictions = clf.predict(x_test)

    report = metrics.classification_report(y_test, predictions)
    accuracy = metrics.accuracy_score(y_test, predictions)
    confusion = metrics.confusion_matrix(y_test, predictions)

    print(report)
    print('Accuracy: ', accuracy)
    print(authors)
    print('Confusion Matrix: ')
    print(confusion)


if __name__ == '__main__':
    main()

