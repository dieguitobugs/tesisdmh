# Agregaremos una matriz de confusión para ver los resultados del SVM
print(__doc__)

import itertools
import numpy as np
import matplotlib.pyplot as plt
import csv
from sklearn.externals import joblib
import matplotlib.patches as mpatches

from sklearn import svm, datasets
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
import time


inicio_de_tiempo = time.time()
# import some data to play with
# y = [0, 5, 5, 10, 5, 0,10,10,10,5,5,0,10,10,10,0,5,10,10,0,5]
# X = [[0, 0], [0, 5], [4, 5], [4, 10], [9, 10], [9,19],[3,11],[2,10],[1,10],[5,8],[3,8],[4,3],[3,13],[3,13],[1,12],[0,1],[5,9],[0,10],[4,16],[6,7],[5,5]]


# y = [0,0,0,0,0,0, 0, 0, 0, 0, 5, 5,5,5,5, 10,10,10,10,10,10,10,10,10,10,10,10]
# X = [[0,0],[0,1],[0,3],[0,0.2], [9,19],[0,2], [4,3], [6,2], [0,4], [1,6], [6,12],[7,10],[8,13],[9,10], [4,10], [4,11],[4,12],[3,10],[2,10],[5,16],[4,20],[3,16],[4,10],[2,13],[4,18],[3,14],[4,17]]
X = []
y = []

with open('dataset\\clf_data.csv', 'rt') as clf_data:
    spamreader = csv.reader(clf_data, delimiter=';')
    for row in spamreader:
        X.append([float(row[0]), float(row[1])])
with open('dataset\\clf_know.csv', 'rt') as clf_know:
    spamreader = csv.reader(clf_know, delimiter=';')
    for row in spamreader:
        y.append(float(row[0]))



# X = np.array(X)
# y = np.array(y)

# # Ordenar X
# matrix = np.matrix(np.column_stack((X, y)))
# matrix = matrix[np.argsort(matrix.A[:, 1])]
#
# X = (np.delete(matrix, np.s_[2], axis=1)).tolist()
# y = ((np.delete(matrix, np.s_[0:2], axis=1)).ravel()).tolist()
# y = y[0]

from sklearn.datasets import make_blobs
X=np.array(X)

plt.scatter(X[:,0], X[:,1], c = y, cmap='coolwarm');
tormenta_patch = mpatches.Patch(color='red', label='Tormenta')
lluvia_patch = mpatches.Patch(color='gray', label='Lluvia')
nada_patch = mpatches.Patch(color='blue', label='Nada')
plt.xlabel("Poligonos")
plt.ylabel("Intensidad en base A/100.000")
plt.legend(handles=[tormenta_patch, lluvia_patch, nada_patch])

# plt.show()

# print(y)
class_names = np.array(['Ninguna', 'Lluvia', 'Tormenta'])


X_test = X
y_test = y

# Split the data into a training set and a test set
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0, test_size=0.25)

# Run classifier, using a model that is too regularized (C too low) to see
# the impact on the results
classifier = svm.SVC(kernel='rbf', C=0.5, cache_size=8000, probability=True, class_weight='balanced')
# classifier = joblib.load('modelo.sav')
classifier.fit(X_train, y_train)
y_pred = classifier.predict(X_test)



def plot_confusion_matrix(cm, classes,
                          normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')

    print(cm)

    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, format(cm[i, j], fmt),
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('Datos reales')
    plt.xlabel('Predicción')

# Compute confusion matrix
cnf_matrix = confusion_matrix(y_test, y_pred)
np.set_printoptions(precision=2)

# Plot non-normalized confusion matrix
plt.figure()
plot_confusion_matrix(cnf_matrix, classes=class_names,
                      title='Matriz de confusión, sin normalización')

# Plot normalized confusion matrix
plt.figure()
plot_confusion_matrix(cnf_matrix, classes=class_names, normalize=True,
                      title='Matriz de confusión normalizada')

# Asignamos un tiempo de finalizacion del analisis para saber cuanto demoro
tiempo_final = time.time()
tiempo_transcurrido = tiempo_final - inicio_de_tiempo

print("Tiempo transcurrido " + str(tiempo_transcurrido) + " segundos.")
plt.show()