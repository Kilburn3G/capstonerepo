
"""
Basic script used to preprocessing data and feature extraction
@author: Aydan Jesson, Alex Wilke
"""

import pandas as pdb
import pdb
import os


def loadDataset(filepath):
    ##Loads dataset from CSV
    dfData = pd.read_csv('data.csv')


def main():
    cwd = os.getcwd()
    filename = r'datain\100.csv'
    
    def init():
        pass

    init()
    
    loadDataset(cwd + filename)

main()