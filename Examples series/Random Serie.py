import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
import random

x = np.arange(0,50000)
y = []

for i in x:
    y.append(random.randint(0,1000))
    
plt.plot(y)

df = pd.DataFrame(y)
df.to_csv('C:/Users/user/Random Serie.txt', header = None, index= False, sep = '\t')