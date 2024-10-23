import sklearn
from sklearn.utils import shuffle
from sklearn.neighbors import KNeighborsClassifier
import pandas as pd
import numpy as np
from sklearn import linear_model, preprocessing

data = pd.read_csv("car.data")

prep = preprocessing.LabelEncoder()

buying = prep.fit_transform(list(data["buying"]))
maint = prep.fit_transform(list(data["maint"]))
door = prep.fit_transform(list(data["door"]))
person = prep.fit_transform(list(data["persons"]))
lug_boot = prep.fit_transform(list(data["lug_boot"]))
safety = prep.fit_transform(list(data["safety"]))
cls = prep.fit_transform(list(data["class"]))

predict = "class"

X = list(zip(buying, maint, door, person, lug_boot, safety))
Y = list(cls)

x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(X, Y, test_size=0.1)

model = KNeighborsClassifier(n_neighbors=9)

model.fit(x_train, y_train)

acc = model.score(x_test, y_test)
print(acc)
predicted = model.predict(x_test)
names = ["unacc", "acc", "good", "vgood"]

for x in range(len(predicted)):
    print("Predicted: ", names[predicted[x]], "Data: ", x_test[x], "Actual: ", names[y_test[x]])
    n = model.kneighbors([x_test[x]], 9, True)