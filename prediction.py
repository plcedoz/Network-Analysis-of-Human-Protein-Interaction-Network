import numpy as np
import pandas as pd
import matplotlib
#%matplotlib inline
import matplotlib.pyplot as plt

from validation_import import get_ref_genes
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegressionCV
from sklearn.metrics import accuracy_score
from sklearn.metrics import average_precision_score
from sklearn.metrics import f1_score
from sklearn.metrics import recall_score
from sklearn.metrics import roc_auc_score
from sklearn.metrics import roc_curve
from sklearn.metrics import precision_recall_curve


def get_labels(node_names):
    
    labels = []
    for source in ['cancer', 'drugbank', 'mendelian']:
        ref_genes = get_ref_genes(source=source)
        labels.append(np.array([node in ref_genes for node in node_names]).astype(int))
    labels = np.asarray(labels).T
    labels = pd.DataFrame(data=labels, index=node_names, columns=['cancer', 'drugbank', 'mendelian'])
    
    return labels


def train_model(features, labels, source="mendelian"): 

    X_train, X_test, labels_train, labels_test = train_test_split(features, labels, test_size=0.33)
    y_train = labels_train[source]
    y_test = labels_test[source]
    model = LogisticRegressionCV(Cs=20, penalty='l2')
    model.fit(X_train, y_train)
    y_score = model.predict_proba(X_test)[:,1]
    y_pred = model.predict(X_test)
    
    return y_test, y_pred, y_score

    
def get_metrics(y_test, y_pred, y_score, source="mendelian"):

    accuracy = accuracy_score(y_test, y_pred, normalize=True, sample_weight=None)
    avg_precision = average_precision_score(y_test, y_score)
    f1 = f1_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    auc = roc_auc_score(y_test, y_score)

    print ("\nStatistics for %s (ratio of positive examples = %0.2f):\n"%(source, np.mean(y_test)))
    print ("Accuracy = %0.2f"%accuracy)
    print ("Average precision = %0.2f"%avg_precision)
    print ("F1 score = %0.2f"%f1)
    print ("Recall = %0.2f"%recall)
    print ("AUC = %0.2f"%auc)

    fpr, tpr, thresholds = roc_curve(y_test, y_score)
    precision, recall, thresholds = precision_recall_curve(y_test, y_score)

    plt.figure()
    plt.subplot(121)
    plt.plot(fpr, tpr)
    plt.xlabel("fpr")
    plt.ylabel("tpr")
    plt.title("ROC curve %s"%source)
    plt.subplot(122)
    plt.plot(recall, precision)
    plt.xlabel("recall")
    plt.ylabel("precision")
    plt.title("PR curve %s"%source)
    plt.savefig("output/metrics_%s"%source)
    
    
    