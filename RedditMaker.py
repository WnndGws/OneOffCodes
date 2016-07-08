# -*- coding: utf-8 -*-
"""
Created on Sat Jun 11 09:02:09 2016

@author: wynand
"""

maxCell = int(input("What is the max Cell? "))
collumn = str(input("What is the collumn? "))
cellCount = [maxCell]

while maxCell > 0:
    maxCell = maxCell - 1
    cellCount.append(maxCell)
    
pasteString = "="

for i in cellCount:
    pasteString = pasteString + '{0}{1}&"+"&'.format(collumn, i)
    
print (pasteString)