
"""
Basic script used to preprocessing data and feature extraction
@author: Aydan Jesson, Alex Wilke
"""

import pandas as pd
import pdb
import os


def loadDataset(filepath):
    ##Loads dataset from CSV
    dfData = pd.read_csv(filepath)
    print(dfData)

def main():
    cwd = os.getcwd()
    filename = r'/datain/samples.csv'
    
    def init():
        pass

    init()
    
    loadDataset(cwd + filename)

main()