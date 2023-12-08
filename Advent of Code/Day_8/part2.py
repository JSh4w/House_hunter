import numpy as np
import math
from tqdm import tqdm
input=open("Advent of Code/Day_8/input.txt","r").read()
instructions,node_data=input.split("\n\n")


dic={}

    #name=a.split("=")[0].strip()
for a in node_data.split("\n"):
    name=a.split("=")[0].strip()
    left=a.split("=")[1].split(",")[0][2:].strip()
    right=a.split("=")[1].split(",")[1][:-1].strip()
    dic[name]=(left,right)
start=[]
start_last=[]
for a in dic:
    if a[2]=="A":
        start.append(a)
        start_last.append(a[2])
cn_all="A"
sw=0

while cn_all != "Z":
    for a,x in enumerate(start):
        start[a]=dic[x][0 if instructions[0]=="L" else 1]
        start_last[a]=start[a][2]
        sw+=1
    instructions=instructions[1:]+instructions[0]
    if start_last.count("Z")==len(start_last):
        cn_all="Z"
    else:
        print(start)
print(sw)
