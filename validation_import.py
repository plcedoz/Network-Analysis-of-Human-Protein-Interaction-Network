import numpy as np
import pandas as pd
import gseapy as gp
import math


def get_cancer(filename="validation_datasets/cancer_gene_census.csv"):
    """
    Extract a gene list from Cancer Gene Census

    """
    cancer_gene_census = pd.read_csv(filename)
    gene_symbols = cancer_gene_census.loc[:,"Gene Symbol"].values.tolist()
    gene_names = cancer_gene_census.loc[:,"Name"].values.tolist()
    gene_string = []
    list_of_synonyms = cancer_gene_census.loc[:,"Synonyms"]
    for synonyms in list_of_synonyms:
        if str(synonyms) != 'nan':        
            for synonym in synonyms.split(','):
                if synonym[:3] == "ENS":
                    gene_string.append(synonym)
    data = {"gene_symbols":gene_symbols, "gene_names":gene_names, "gene_string":gene_string}
    
    return data


def get_mendelian(filename="validation_datasets/mim2gene.txt"):
    """
    Extract a gene list from Online Mendelian Inheritance in Man (OMIM) (omim.org)

    """
    gene_entrez = []
    gene_symbols = []
    gene_string = []
    with open(filename) as f:
        for line in f:
            if len(line.split('\t'))>1:
                if line.split('\t')[1] == "gene":
                    if len(line.split('\t'))>2:
                        gene_entrez.append(line.split('\t')[2])
                        gene_symbols.append(line.split('\t')[3])
                        gene_string.append(line.split('\t')[4])
    data = {"gene_symbols":gene_symbols, "gene_entrez":gene_entrez, "gene_string":gene_string}
    
    return data


def get_drugbank(molecule_type="target", subset="all"):
    """
    Extract a gene list from Drugbank
    
    Args:
        -molecule_type: "carrier", "enzyme", "target", "transporter"
        -subset: "all" or "approved"
        
    """
    data = pd.read_csv("validation_datasets/drugbank_%s_%s_polypeptide_ids.csv/all.csv"%(subset, molecule_type))
    data = data[data["Species"]=="Human"]
    gene_symbols = data["Gene Name"].values.tolist()
    protein_names = data["Name"].values.tolist()
    uniprot_ID = data["UniProt ID"].values.tolist()
    data = {"gene_symbols":gene_symbols, "protein_names":protein_names, "uniprot_ID":uniprot_ID}
    
    return data


def get_ref_genes(source="cancer", molecule_type="target", subset="all"):
    
    if source=="cancer":
        gene_ref = get_cancer()["gene_symbols"]
    if source=="mendelian":
        gene_ref = get_mendelian()["gene_symbols"]
    if source=="drugbank":
        gene_ref = get_drugbank(molecule_type=molecule_type, subset=subset)["gene_symbols"]
    
    return gene_ref
        


