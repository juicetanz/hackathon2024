import pandas as pd
import numpy as np

from sklearn.metrics import classification_report
from sklearn import metrics
import warnings
warnings.filterwarnings('ignore')

crops = pd.read_csv('flaskr/templates/cropprediction/Crop_recommendation.csv')

crops['label'].unique()

acc = []
model = []
features = crops[['N', 'P','K','temperature', 'humidity', 'ph', 'rainfall']]
target = crops['label']

from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(features,target,test_size = 0.3,random_state =2)

from sklearn.neighbors import KNeighborsClassifier
knn = KNeighborsClassifier()

knn.fit(x_train,y_train)

predicted_values = knn.predict(x_test)

x = metrics.accuracy_score(y_test, predicted_values)
acc.append(x)
model.append('K Nearest Neighbours')
print("KNN Accuracy is: ", (x*100), "%")

#Print Train Accuracy
knn_train_accuracy = knn.score(x_train,y_train)
#Print Test Accuracy
knn_test_accuracy = knn.score(x_test,y_test)


def run_suggestion(N, P, K, temperature, humidity, ph, rainfall):
    x_values = np.array([[N, P, K, temperature, humidity, ph, rainfall]])
    x_data = pd.DataFrame(x_values, columns = ['N','P','K','temperature','humidity','ph','rainfall'])
    ans = knn.predict_proba(x_data)

    t = {}
    for idx, d in enumerate(ans[0]):
        if d > 0:
            t[knn.classes_[idx]] = d
    return t
