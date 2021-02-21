from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (QMainWindow, QVBoxLayout, QPushButton, QSplitter
                             ,QFileDialog, QLabel, QWidget, QFormLayout
                             ,QLineEdit, QComboBox, QGroupBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from sklearn.metrics import r2_score
from modules.Dialog import Dialog

from pandas import (read_csv, DataFrame)
from numpy import (asarray, transpose, arange, log10, vectorize, 
                   zeros, cumsum, mean, polyfit, polyval, sqrt)
from math import exp
from pathlib import Path

import matplotlib.pyplot as plt
import pyqtgraph as pg 

class DFA(QMainWindow):
    def __init__(self):      
        super(DFA,self).__init__()
        self.initUI()
#%%
    def cargarSenial1(self):
        self.aux = False
        self.list3.clear()
        self.plot1.clear()
        self.list_DFA.clear()
        self.txth1.clear()
        self.txtr1.clear()
        self.nombreSenial= QFileDialog.getOpenFileNames(None, 'Open file(s)', '/home')
        self.rutas = self.nombreSenial[0]
        
        self.dialog = Dialog(str(len(self.rutas))+' Files(s) loaded','open.png')
        self.dialog.show()
        self.list3.addItem('')
        for i in range(len(self.rutas)):
            names=str.split(self.rutas[i],"/")
            t=len(names)
            nombre= names[t-1]
            self.list3.addItem(nombre)
            
        if(len(self.rutas)==0):
            self.btnDFA1.setEnabled(False)
            self.lbl_num_files.setStyleSheet("color : red; ")
            self.lbl_num_files.setText("Files loaded: "+str(len(self.rutas)))
        else:
            self.lbl_num_files.setStyleSheet("color : blue; ")
            self.lbl_num_files.setText("Files loaded: "+str(len(self.rutas)))
        self.aux = True 
        self.btnDFA1.setEnabled(True)
        self.txtm1.setEnabled(True)
#%% 
    def DFA1(self): 
        self.txth1.setEnabled(True)
        self.plot1.clear()
        self.list_DFA.clear()
        self.h = []
        self.fn = []
        self.s = []
        self.R = []
        order = int(self.txtm1.text())
        nombres_archivos = []
        
        
        for i in range(len(self.rutas)):
            data = read_csv(self.rutas[i], sep='\t', header = None )
            lineas= data.shape[1]
            if(lineas == 1):
                self.y1 = asarray(data[0])
            elif(lineas == 2):
                self.y1 = asarray(data[1])
            names = str.split(self.rutas[i],"/")
            t = len(names)
            nombre= names[t-1]
            names = str.split(self.rutas[i],nombre)
            nam   = str.split(nombre,'.')
  
            RUTA =  names[0] + '/DFA/'
            path = Path(RUTA)
            path.mkdir(parents = True,exist_ok = True)
            
            xn = arange(0, 135, 1)
            func = vectorize(lambda x: int(10.1*exp(0.0866 * x)))
            n = func(xn)
            self.s1 = []
            for j in range(len(n)):
                if(n[j]<=int(len(self.y1)/4)):
                    self.s1.append(n[j]) 
            self.fn1 = zeros(len(self.s1))
            for l in range(len(self.s1)):
                n_1= self.s1[l]
                N = len(self.y1)
                n = int(N/n_1)
                N1 = int(n_1*n)
                y = zeros((N))
                Yn = zeros((N))
                fitcoef = zeros((n,order+1))
                y = cumsum((self.y1-mean(self.y1)))
                x_aux = zeros(int(n_1))
                for i in range(int(n_1)):
                    x_aux[i] = i
                for j in range(n):
                    y_aux = y[int(j*n_1):int(j*n_1+n_1)]
                    fitcoef[j] = polyfit(x_aux,y_aux,order)
                for j in range(n):
                    Yn[int(j*n_1):int(j*n_1+n_1)] = polyval(fitcoef[j],x_aux)
                sum1    = sum(pow(transpose(y)-Yn,2))/N1
                self.fn1[l]   = sqrt(sum1)

            self.h1 = round(polyfit(log10(self.s1), log10(self.fn1),1)[0],4) 
            self.fn.append(log10(self.fn1))
            self.s.append(log10(self.s1))
            self.h.append(self.h1)
            
            plt.figure()
            plt.title(nam[0], fontsize = 15)
            plt.grid(True)
            plt.plot(self.y1)
            plt.savefig(RUTA + nam[0]+' Serie.png', dpi = 300)
            plt.close()
            
            
            datos = []
            datos.append(log10(self.s1))
            datos.append(log10(self.fn1))
            datos = transpose(asarray(datos))

            datos = DataFrame(datos)
            datos.to_csv(RUTA + nam[0]+' ln(F) vs ln(n).txt',header = None, index = False, sep='\t')
            rutaSave = RUTA
            nombres_archivos.append(nam[0]+':')
            
            if(len(self.rutas)!=0):
                ajuste = []
                b = polyfit(log10(self.s1), log10(self.fn1),1)[1]  
                for i in range(len(self.s1)):
                    ajuste.append(self.h1*log10(self.s1[i])+b)
                rcuadrada = round(r2_score(log10(self.fn1), ajuste),4)
                self.R.append(rcuadrada)
                
            plt.figure()
            plt.grid(True)
            plt.title(nam[0], fontsize = 15)
            plt.xlabel('Ln(n)', fontsize = 10)
            plt.ylabel('Ln(F(n))', fontsize = 10)
            plt.plot(log10(self.s1), log10(self.fn1), label = 'Original')
            plt.plot(log10(self.s1), ajuste, label = 'Adjust')
            plt.legend()
            plt.savefig(RUTA + nam[0]+' ln(F) vs ln(n).png', dpi = 300)
            plt.close()
            
        self.R = asarray(self.R) 
        self.h = asarray(self.h)
        self.list_DFA.addItem('')
        for i in range(len(self.rutas)):
            names=str.split(self.rutas[i],"/")
            t=len(names)
            nombre= names[t-1]
            self.list_DFA.addItem(nombre)
         
        datos_R = []
        datos_R.append(nombres_archivos) 
        datos_R.append(self.R)   
        datos_R = transpose(asarray(datos_R))
        datos_R = DataFrame(datos_R)
        datos_R.to_csv(rutaSave+'R^2.txt', header = None, index = False, sep = '\t')
        
        datos_h = []
        datos_h.append(nombres_archivos) 
        datos_h.append(self.h)   
        datos_h = transpose(asarray(datos_h))
        datos_h = DataFrame(datos_h)
        datos_h.to_csv(rutaSave+'Hurst Exponent.txt', header = None, index = False, sep = '\t')       
         
        self.dialog = Dialog('Done!!','Icons\listo.png')
        self.dialog.show()
        
#%%
    def plots(self):
        if(self.aux == True):
            self.plot1.clear()
            i= self.list3.currentIndex()-1
            if(len(self.rutas)!=0):            
                data = read_csv(self.rutas[i],sep='\t', header=None)
                lineas= data.shape[1]
                if(lineas == 1):
                    self.y = asarray(data[0])
                elif(lineas == 2):
                    self.y = asarray(data[1])
                self.plot1.setLabel('bottom',color='k', **{'font-size':'14pt'})
                self.plot1.getAxis('bottom').setPen(pg.mkPen(color='k', width=1))
                # Y1 axis   
                self.plot1.setLabel('left',color='k', **{'font-size':'14pt'})
                self.plot1.getAxis('left').setPen(pg.mkPen(color='k', width=1))
                names=str.split(self.rutas[i],"/")
                t=len(names)
                nombre= names[t-1]
                self.plot1.setTitle(nombre)
                self.plot1.plot(self.y,pen='k')
                
#%%
    def plots_DFA(self):
        if(self.aux == True):
            self.plot1.clear()
            i= self.list_DFA.currentIndex()-1
            if(len(self.rutas)!=0):   
                self.plot1.setLabel('bottom',"ln(n)",color='k', **{'font-size':'14pt'})
                self.plot1.getAxis('bottom').setPen(pg.mkPen(color='k', width=1))
                # Y1 axis   
                self.plot1.setLabel('left',"ln(F(n))",color='k', **{'font-size':'14pt'})
                self.plot1.getAxis('left').setPen(pg.mkPen(color='k', width=1))
                names=str.split(self.rutas[i],"/")
                t=len(names)
                nombre= names[t-1]
                self.plot1.setTitle(nombre)
                self.plot1.plot(self.s[i],self.fn[i], symbol='o')
                self.txtr1.setText(str(self.R[i]))
                self.txth1.setText(str(self.h[i]))
        
#%% 
    def initUI(self):
        pg.setConfigOption('background', 'w')
        params = {
                'figure.figsize': [4, 4],
                'figure.dpi': 300,
                'savefig.dpi': 300
           }
        plt.rcParams.update(params)
###############################################################################
########Variables Globales ####################################################
############################################################################### 
        self.setWindowTitle('Detrended Analysis Fluctuation')
        self.setWindowIcon(QIcon("Icons\DFA.ico"))
        self.resize(1000, 600)
        self.ruta = None
        self.nombreSenial1=''
        self.x=[]
        self.y1=[]
        self.h1=[]

        contain   = QSplitter(Qt.Horizontal)
        botones   = QtWidgets.QVBoxLayout()
        graficos  = QVBoxLayout()
        results1  = QFormLayout()
        results2  = QFormLayout()
        results3  = QFormLayout()
        results4  = QFormLayout()
        group_box_files    = QGroupBox("Load file(s)")
        group_box_settings = QGroupBox("Settings")
        group_box_plots    = QGroupBox("Plots")
        group_box_values   = QGroupBox("Values")
        #################################################################
        ##     Elementos del layout botones
        #################################################################
        self.btnLoadSig1 = QPushButton('Load signal')
        self.btnLoadSig1.clicked.connect(self.cargarSenial1)
        self.btnLoadSig1.setStyleSheet("font-size: 18px")
        
        lblm1 = QLabel("P adjust degree: ")  
        lblm1.setStyleSheet("font-size: 18px")
        self.txtm1 = QLineEdit('1')
        self.txtm1.setEnabled(False)
        self.txtm1.setStyleSheet("font-size: 18px")
        
        lblh1 = QLabel("Hurst exponent h: ")
        lblh1.setStyleSheet("font-size: 18px")
        self.txth1 = QLineEdit('')
        self.txth1.setEnabled(False)
        
        lblr1 = QLabel("R^2: ")
        lblr1.setStyleSheet("font-size: 18px")
        self.txtr1 = QLabel('')
        
        self.lbl_num_files = QLabel("Files loaded: ")
        self.lbl_num_files.setStyleSheet("font-size: 18px")
             
        self.btnDFA1 = QPushButton('DFA')
        self.btnDFA1.clicked.connect(self.DFA1)
        self.btnDFA1.setStyleSheet("font-size: 18px")
        self.btnDFA1.setEnabled(False)
                      
        lbl_file = QLabel("File: ")
        lbl_file.setStyleSheet("font-size: 18px")
        
        self.list3 = QComboBox()
        self.list3.currentIndexChanged.connect(self.plots)
        
        lbl_DFA = QLabel("DFA: ")
        lbl_DFA.setStyleSheet("font-size: 18px")
        
        self.list_DFA = QComboBox()
        self.list_DFA.currentIndexChanged.connect(self.plots_DFA)
        
        #################################################################
        ##     Colocar elementos en layout botones
        #################################################################
        results1.addRow(self.btnLoadSig1)  
        results1.addRow(self.lbl_num_files)
        group_box_files.setLayout(results1)
        
        results2.addRow(lblm1, self.txtm1)
        group_box_settings.setLayout(results2)
        
        results3.addRow(lbl_file, self.list3)
        results3.addRow(lbl_DFA, self.list_DFA)
        group_box_plots.setLayout(results3)
        
        results4.addRow(lblh1, self.txth1)
        results4.addRow(lblr1, self.txtr1)
        group_box_values.setLayout(results4)
        
        botones.addWidget(group_box_files)
        botones.addWidget(group_box_settings)
        botones.addWidget(group_box_plots)
        botones.addWidget(group_box_values)
        botones.addWidget(self.btnDFA1)
        #################################################################
        ##     Colocar elementos en layout graficos
        #################################################################
        
        self.plot1=pg.PlotWidget()
        self.plot1.setLabel('bottom',color='k', **{'font-size':'14pt'})
        self.plot1.getAxis('bottom').setPen(pg.mkPen(color='k', width=1))
        self.plot1.setLabel('left',color='k', **{'font-size':'14pt'})
        self.plot1.getAxis('left').setPen(pg.mkPen(color='k', width=1))
        self.plot1.showGrid(1,1,0.2)
        graficos.addWidget(self.plot1)
        
        bot = QWidget()
        bot.setLayout(botones)
        gra = QWidget()
        gra.setLayout(graficos)
        
        contain.addWidget(bot)
        contain.addWidget(gra)
        self.setCentralWidget(contain)
