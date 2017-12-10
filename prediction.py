import numpy as np
import pandas as pd
import matplotlib
#%matplotlib inline
import matplotlib.pyplot as plt
import json

from time import strftime
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
from sklearn.metrics import confusion_matrix

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV


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
    # model = LogisticRegressionCV(Cs=20, penalty='l2')

    model = GridSearchCV(n_jobs = 4,cv = 5, refit = True,estimator=RandomForestClassifier(verbose=0,class_weight ="balanced"),param_grid=
                {"max_depth":[2,4,6],"min_samples_split":[2,4],"max_features":["auto","log2",None],"n_estimators" :[20,50,100]})
    model.fit(X_train, y_train)
    y_score = model.predict_proba(X_test)[:,1]
    y_pred = model.predict(X_test)

    model_info = dict(model_info =str(model),features = list(features.columns))

    return y_test, y_pred, y_score,model_info

    
def get_and_save_metrics(y_test, y_pred, y_score, source="mendelian",model_info = None):

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
    print("Confusion Matrix:")

    cm = confusion_matrix(y_test,y_pred)
    print(cm)
    if model_info is None:
        dico_exportation = dict()
    else:
        dico_exportation = dict(pipeline_info = model_info.copy())
    dico_exportation["cm"] = dict(zip(["tn","fp","fn","tp"],map(int,cm.ravel())))
    dico_exportation["metrics"] = dict()
    dico_exportation["metrics"]["F1"] = f1
    dico_exportation["metrics"]["recall"] = avg_precision
    dico_exportation["metrics"]["precision"] = recall
    dico_exportation["source"] = source
    with open("output/{}_{}.json".format(strftime("%Y_%m_%d_%H_%M"),source), 'w') as fi:
        json.dump(dico_exportation,fp=fi, indent=2)

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
    
    
    