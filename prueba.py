import argparse
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pdb

nombres = ['a','b','c','d']
lista = []
a = np.linspace(0,1)
b = 2*a
c = 3*a
d = 4*a
x = 50*a
data = [a,b,c,d]
i =0
figure, main_data = plt.subplots()
data_b = main_data.twinx()
data_c = main_data.twinx()
data_d = main_data.twinx()

data_c.tick_params(bottom=False,left=True,right=False,top=False,labelbottom=False,labelleft=True,labelright=False,labeltop=False)

plots = [main_data,data_b,data_c,data_d]

for p in plots:
    lista += p.plot(x,data[i])
    i+=1
    
plt.show(block=True)
plt.savefig("C:\\Users\\1\\Desktop\\Semana_pruebaa\\Prueba-tecnica\\Fika_2023_03_06_143"+"\\Fika_2023_03_06_143",dpi=300,format="png")