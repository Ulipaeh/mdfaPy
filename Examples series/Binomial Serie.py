import matplotlib.pyplot as plt
import pandas as pd 

a = 0.9
N = 50000

xk = []

n_max = 16
n = [] 
for i in range(0,N):
    A   = str.split(bin(i),'0b')[1]
    aux = A.count('1')
    n.append(aux)
     
for k in range(1,N):
    xk.append(pow( a, n[k-1])*pow(1-a, n_max-n[k-1]) )
plt.plot(xk)

df = pd.DataFrame(xk)
df.to_csv('C:/Users/user/Binomial serie.txt', header = None, index= False, sep = '\t')


