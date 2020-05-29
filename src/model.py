import numpy as np
import pickle
from clean_data import get_model_data
from sklearn.metrics import accuracy_score, recall_score, precision_score, roc_curve, roc_auc_score
from sklearn.ensemble import RandomForestClassifier


class MyModel():
    
    def __init__(self):
        self.model = RandomForestClassifier()
        self.X = None
        self.y = None
        self._accuracy = None
        self._precision = None
        self._recall = None
        self._tpr = None
        self._fpr = None
        self._auc = None

    def fit(self, X, y):
        self.X = X.copy()
        self.y = y.copy()
        self.model.fit(X,y)

    def predict_proba(self, X):
        return self.model.predict_proba(X)
    
    def predict(self, X):
        return self.model.predict(X)
    
    def get_metrics(self, X, y):
        self._accuracy = self.model.score(X, y)
        self._precision = precision_score(y, self.predict(X))
        self._recall = recall_score(y, self.predict(X))
        self._auc = roc_auc_score(y, self.predict_proba(X)[:,1])
        self._fpr, self._tpr, _ = roc_curve(y, self.predict_proba(X)[:,1])
        

if __name__ == '__main__':
    X_train, X_test, y_train, y_test = get_model_data('./data/data.json')
    model = MyModel()
    model.fit(X_train, y_train)
    model.get_metrics(X_test, y_test)
    
    print('model accuracy:  ', model._accuracy)
    print('model precision: ', model._precision)
    print('model recall:    ', model._recall)
    print('model auc score: ', model._auc)
    
    with open('./model/model.pkl', 'wb') as f:
        # Write the model to a file.
        pickle.dump(model, f)