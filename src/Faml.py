#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
from pandas import Series,DataFrame


# In[1]:


def find_job(decription,dataframe,*skills):
    num_list = []
    for num in dataframe.index:
        try:
            str_long = decription[str(num)]
        except KeyError:
            str_long = ''
        similar = True
        for skill in skills:
            if skill.lower() not in str_long.lower():
                similar = False
                continue
            else:
                pass
        if similar == True:
            num_list.append(num)
    if len(num_list) == 0:
        return None
    else:
        origin = dataframe.loc[num_list[0],'index']
        num_ret = 0
        for issue in num_list:
            if dataframe.loc[issue,'index'] > origin:
                origin = dataframe.loc[issue,'index']
                num_ret = issue
            else:
                pass
        return [dataframe.loc[num_ret],dataframe.loc[num_ret,'Requirement'].split('\n')]

