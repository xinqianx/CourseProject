#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 22 20:59:20 2021

@author: candice
"""

import csv
import module


category = []
keyword = []



tb = module.Category()
tb.deleteall()
with open('category_key_inventory.csv',mode='r', encoding='utf-8-sig') as csvfile:
     reader = csv.reader(csvfile)
     
     for row in reader:

         keyword = ','.join(row[1:])

         result = tb.create(row[0],keyword)
         print(result)
         
