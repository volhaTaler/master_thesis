import matplotlib.pyplot as plt 
import numpy as np
import pandas as pd
import openpyxl
import os

PATH_TO_LOGS = "/home/volha/Desktop/MSc/MSC_data/logs/"
# "/home/volha/Desktop/MSc/master_thesis/logs/"
#"/home/volha/Desktop/MSc/MSC_data/logs/"

results = {0: 0, 1: 0, -1: 0}
zeros = []
ones = []
m_ones = []
total = []
names = []
conds = []

def list_files(dir):
    r = []
    for root, dirs, files in os.walk(dir):
        for name in files:
            r.append(os.path.join(root, name))
    return r

DATAS= []

files = list_files(PATH_TO_LOGS)
print(len(files))
for file in files:
    with open(file, 'r') as f:
        for l in f:
            if l != "\n":
                l = l.split("\t")[-1]
                print ("l: ", l)

                if int(l.strip()) == 0:
                    results[0] = results[0] + 1
                elif int(l.strip()) == 1:
                    results[1] = results[1] + 1
                elif int(l.strip()) == -1:
                    results[-1] = results[-1] + 1
                else:
                    print("UNEXPECTED SYMBOL")

    name = file.split(".txt")[0]
    name = name.split("/")[-1]
    name_parts = name.split("_")
    condition = ""
    for p in name_parts:
        if "cond" in p or "line" in p:
            condition = "  " + condition + p + " "
    zeros.append(results[0])
    ones.append(results[1])
    m_ones.append(results[-1])
    total.append(results[0] + results[1] + results[-1])
    names.append(name)
    conds.append(condition)
    data = pd.DataFrame(list(zip(names, conds, zeros, ones, m_ones, total)), columns=[' Name ', ' Condition ', ' 0 ', ' 1 ', ' -1 ', ' Total '])
    DATAS.append(data)
    results = {0: 0, 1: 0, -1: 0}
    zeros = []
    ones = []
    m_ones = []
    names = []
    conds = []
    total = []
frames = pd.concat(DATAS)
frames.to_excel('social_cues_all2.xlsx', index=False, header=True)




