# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df=pd.read_csv("THEMIS_DATA.txt", skiprows=63, skipfooter=3, delim_whitespace=True, 
names=['dt','tm', 'sec', 'bx', 'by', 'bz'])


temp=df[['dt', 'tm']].apply(lambda x: ' '.join(x), axis=1)
df['ut']=pd.to_datetime(temp, format='%d-%m-%Y %H:%M:%S.%f')

df['bt']=np.sqrt(df['bx']**2 + df['by']**2 + df['bz']**2)

plt.figure()
plt.plot(df['ut'], df['bt'], "r-")

"""
plt.plot(df['ut'], df['by'], "b-")
plt.figure()
plt.plot(df['ut'], df['bz'], "g-")
plt.show()
"""