import numpy as np
import pandas as pd

from validation_import import get_ref_genes

def get_labels(node_names):
    
    labels = []
    for source in ['cancer', 'drugbank', 'mendelian']:
        ref_genes = get_ref_genes(source=source)
        labels.append(np.array([node in ref_genes for node in node_names]).astype(int))
    labels = np.asarray(labels).T
    labels = pd.DataFrame(data=labels, index=node_names, columns=['cancer', 'drugbank', 'mendelian'])
    return labels

