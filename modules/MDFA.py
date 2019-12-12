from PyQt5.QtWidgets import (QMainWindow,QPushButton, QVBoxLayout, QSplitter, 
                             QCheckBox,QFileDialog ,QLabel, QWidget, QLineEdit, 
                             QFormLayout, QComboBox, QButtonGroup,QRadioButton)
from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon
from modules.Dialog import Dialog

import numpy as np
import pandas as pd
import pyqtgraph as pg
import matplotlib.pyplot as plt
import seaborn as sns
from time import time
import math as math
from numba import jit

@jit(nopython=True, cache=True)
def myfunc(q, Var, Varr, v, Seg, fit, s, ns, SegRev, fitr):
    for nq in range(len(q)):
        Var[v][nq]  = np.power(np.sum(np.power(Seg - fit, 2)) / s[ns], q[nq] / 2)
        Varr[v][nq] = np.power(np.sum(np.power(SegRev - fitr, 2)) / s[ns], q[nq] / 2)
#%%
class MDFA(QMainWindow):
    def __init__(self):      
        super().__init__()
        self.initUI()    
#%% 
    def cargarSenial(self):
        self.aux = False
        self.list3.clear()
        self.list_MDFA.clear()
        self.plot1.clear()
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
            self.lbl_num_files.setStyleSheet("color : red; ")
            self.lbl_num_files.setText("Files loaded: "+str(len(self.rutas)))
        else:
            self.lbl_num_files.setStyleSheet("color : blue; ")
            self.lbl_num_files.setText("Files loaded: "+str(len(self.rutas)))
        self.aux = True 
        self.btnMDFA.setEnabled(True)
#%%
    def plots(self):
        if(self.aux == True):
            self.plot1.clear()
            i= self.list3.currentIndex()-1
            if(len(self.rutas)!=0):            
                data = pd.read_csv(self.rutas[i],sep='\t', header=None)
                lineas= data.shape[1]
                if(lineas == 1):
                    self.y = np.asarray(data[0])
                elif(lineas == 2):
                    self.y = np.asarray(data[1])
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
    def print_val(self):
        print(str(self.plots.checkedId()))                    
        
#%%
    def MDFA(self):
            self.t_inicial = time()
            self.plot1.clear()
            qmax = int(self.txtQmax.text())
            qmin = int(self.txtQmin.text())
            dq   = float(self.txtdQ.text())
            q    = np.arange(qmin,qmax,dq)
            m    = int(self.txtm.text())
            xn   = np.arange(0, 135, 1)
            func = np.vectorize(lambda x: int(10.1*math.exp(0.0866 * x)))
            n = func(xn)
            self.alphas     = np.transpose(np.zeros((len(q)-1,len(self.rutas))))
            self.fespectros = np.transpose(np.zeros((len(q)-1,len(self.rutas))))
            self.qs         = np.transpose(np.zeros((len(q)-1,len(self.rutas))))
            self.taus       = np.transpose(np.zeros((len(q)-1,len(self.rutas))))
            self.hches      = np.transpose(np.zeros((len(q)-1,len(self.rutas))))
            for i in range(len(self.rutas)):
                self.y = np.asarray(pd.read_csv(self.rutas[i], sep='\t', header = None ))
                val = len(self.y) / 4
                s = n[n < val]
                if(self.int_state==0):
                    Y=np.cumsum((self.y-np.mean(self.y)))
                elif(self.int_state==1):
                    Y=np.cumsum((self.y-np.mean(self.y)))
                    Y=np.cumsum((Y-np.mean(Y)))
                YRev = Y
                N=len(Y)
                q=np.arange(qmin,qmax,dq)
                Fq=np.zeros((len(s),len(q)))
                znumb = np.where((q >= -0.1) & (q <= 0.1))[0][-1] - 1
                for ns in range(len(s)):                        
                    Ns=int(N/s[ns])
                    Var=np.zeros((Ns,len(q)))
                    Varr=np.zeros((Ns,len(q)))
                    for v in range(Ns):                                                         
                        SegNumb = np.arange(((v+1)-1)*s[ns],(v+1)*s[ns])
                        Seg     = Y[SegNumb]                                            
                        SegRev  = YRev[SegNumb]                                      
                        poly    = np.polyfit(SegNumb,Seg,m)                                   
                        polyr   = np.polyfit(SegNumb,SegRev,m)                               
                        fit     = np.polyval(poly,SegNumb)                                     
                        fitr    = np.polyval(polyr,SegNumb)        
                        myfunc(q, Var, Varr, v, Seg, fit, s, ns, SegRev, fitr)
                    Var  = np.transpose(Var)
                    Varr = np.transpose(Varr)
                    for nq in range(len(q)):
                        Fq[ns][nq] = pow((sum(Var[:][nq])+sum(Varr[:][nq]))/(2*Ns),1/q[nq])
                    Fq[ns][znumb]  = (Fq[ns][znumb-1]+Fq[ns][znumb+1])/2
                    del(Var,Varr)
                logFq = np.log10(Fq)
                logFq = np.transpose(logFq)
                Hq    = np.zeros(len(q))
                for nq in range(len(q)):
                    P = np.polyfit(np.log10(s),logFq[:][nq],1)
                    if(self.int_state == 0):
                        Hq[nq] = P[0]
                    elif(self.int_state == 1):
                        Hq[nq] = P[0]-1
                t  = q*Hq-1
                α  = np.diff(t)/dq
                Hq = Hq[0:len(Hq)-1]
                t  = t[0:len(t)-1]
                q  = q[0:len(q)-1]       
                ####### α y f(α) #############################################   
                fα = np.zeros(len(t))
                fα = q*α-t
                self.fα  = fα
                self.α   = α
                self.t   = t
                self.Hq  = Hq
                self.q   = q     
                self.btnMDFA.setEnabled(False)
                self.t_final = time()
                self.tiempo  = round(float(self.t_final-self.t_inicial),4)
                self.txttime.setText(str(self.tiempo))
                self.alphas[:][i]     = self.α
                self.fespectros[:][i] = self.fα
                self.taus[:][i]       = self.t
                self.hches[:][i]      = self.Hq
                self.qs[:][i]         = self.q
            self.list_MDFA.addItem('')
            for i in range(len(self.rutas)):
                names  = str.split(self.rutas[i],"/")
                t      = len(names)
                nombre = names[t-1]
                self.list_MDFA.addItem(nombre)
            self.alphas     = np.transpose(self.alphas)
            self.fespectros = np.transpose(self.fespectros)
            self.taus       = np.transpose(self.taus)
            self.hches      = np.transpose(self.hches)
            self.qs         = np.transpose(self.qs)
            self.dialogo_done = Dialog('Done!!','Icons\listo.png')
            self.dialogo_done.show()
#%%
    def plots_MDFA(self):
        self.alphas2     = np.transpose(self.alphas)
        self.fespectros2 = np.transpose(self.fespectros)
        self.taus2       = np.transpose(self.taus)
        self.hches2      = np.transpose(self.hches)
        self.qs2         = np.transpose(self.qs)
        op = self.plots.checkedId()
        if(op==-2):
            if(self.aux == True):
                self.plot1.clear()
                i= self.list_MDFA.currentIndex()-1
                if(len(self.rutas)!=0):   
                    self.plot1.setLabel('bottom', 'α',color='k',**{'font-size':'14pt'})
                    self.plot1.getAxis('bottom').setPen(pg.mkPen(color='k', width=1))
                    # Y1 axis   
                    self.plot1.setLabel('left', 'f(α)',color='k', **{'font-size':'14pt'})
                    self.plot1.getAxis('left').setPen(pg.mkPen(color='k', width=1))
                    names=str.split(self.rutas[i],"/")
                    t=len(names)
                    nombre= names[t-1]
                    self.plot1.setTitle(nombre)
                    self.plot1.plot(self.alphas2[i], self.fespectros2[i], pen='r', symbol='o', symbolSize = 10)
        elif(op==-3):
            if(self.aux == True):
                self.plot1.clear()
                i= self.list_MDFA.currentIndex()-1
                if(len(self.rutas)!=0):   
                    self.plot1.setLabel('bottom', 'q',color='k', **{'font-size':'14pt'})
                    self.plot1.getAxis('bottom').setPen(pg.mkPen(color='k', width=1))
                    # Y1 axis   
                    self.plot1.setLabel('left', 'τ(q)',color='k', **{'font-size':'14pt'})
                    self.plot1.getAxis('left').setPen(pg.mkPen(color='k', width=1))
                    names=str.split(self.rutas[i],"/")
                    t=len(names)
                    nombre= names[t-1]
                    self.plot1.setTitle(nombre)
                    self.plot1.plot(self.qs2[i], self.taus2[i], pen='r', symbol='o', symbolSize = 10)
                
        elif(op == -4):
            if(self.aux == True):
                self.plot1.clear()
                i= self.list_MDFA.currentIndex()-1
                if(len(self.rutas)!=0):   
                    self.plot1.setLabel('bottom', 'q', color='k',**{'font-size':'14pt'})
                    self.plot1.getAxis('bottom').setPen(pg.mkPen(color='k', width=1))
                    self.plot1.setLabel('left', 'h(q)', color='k',**{'font-size':'14pt'})
                    self.plot1.getAxis('left').setPen(pg.mkPen(color='k', width=1))
                    names=str.split(self.rutas[i],"/")
                    t=len(names)
                    nombre= names[t-1]
                    self.plot1.setTitle(nombre)
                    self.plot1.plot(self.qs2[i], self.hches2[i], pen='r', symbol='o', symbolSize = 10)   
                             
#%%
    def saveFile(self):
        nom = QFileDialog.getSaveFileName(None, 'Saving Data in Current Plot')
        
        writer = pd.ExcelWriter(nom[0] + ".xlsx")

        a = pd.DataFrame(self.alphas)
        a.to_excel(writer, 'Atable', index = False, header = None)
        
        f = pd.DataFrame(self.fespectros)
        f.to_excel(writer, 'Ftable', index = False, header = None)
        
        t = pd.DataFrame(self.taus)
        t.to_excel(writer, 'Ttable', index = False, header = None)
        
        H = pd.DataFrame(self.hches)
        H.to_excel(writer, 'Htable', index = False, header = None)
        
        q = pd.DataFrame(self.qs)
        q.to_excel(writer, 'Qtable', index = False, header = None)
        
        writer.save()
#%%
    def state_check(self, state):
        if(state == Qt.Checked): 
            self.int_state = 1 
        else: 
            self.int_state = 0
#%%
    def initUI(self):
        pg.setConfigOption('background', 'w')
        params = {
                'figure.figsize': [4, 4],
                'figure.dpi': 300,
                'savefig.dpi': 300
           }
        plt.rcParams.update(params)
        sns.set()
        sns.set_style("white")
        sns.set_palette("muted")
        sns.set_context("paper")
        self.setWindowTitle('Multifractal Detrended Analysis Fluctuation')
        self.setWindowIcon(QIcon("Icons\multifractal.ico"))
        self.resize(1200, 800)
        ########Variables Globales ####################################################
        ###############################################################################        
        self.rutas = None
        self.nombreSenial=''
        self.int_state = 0
        contain  = QSplitter(Qt.Horizontal)
        botones  = QtWidgets.QVBoxLayout()
        graficos = QVBoxLayout()
        results  = QFormLayout()
        #################################################################
        ##     Elementos del layout botones
        ################################################################# 
        font_size = 'font-size: 20px'
        
        self.btnLoadSig = QPushButton('Load signal')
        self.btnLoadSig.clicked.connect(self.cargarSenial)
        self.btnLoadSig.setStyleSheet(font_size)
        self.btnLoadSig.setEnabled(True)        
        
        self.btnMDFA = QPushButton('MFDFA')
        self.btnMDFA.clicked.connect(self.MDFA)
        self.btnMDFA.setStyleSheet(font_size)
        self.btnMDFA.setEnabled(False)
        
        self.btnSavechar = QPushButton('Save data')
        self.btnSavechar.clicked.connect(self.saveFile)
        self.btnSavechar.setStyleSheet(font_size)

        self.txtQmax = QLineEdit('5')
        self.txtQmax.setEnabled(True)
        self.txtQmax.setStyleSheet(font_size)

        self.txtQmin = QLineEdit('-5')
        self.txtQmin.setEnabled(True)
        self.txtQmin.setStyleSheet(font_size)
        
        self.txtdQ = QLineEdit('.1')
        self.txtdQ.setEnabled(True)
        self.txtdQ.setStyleSheet(font_size)
        
        self.txtm = QLineEdit('1')
        self.txtm.setEnabled(True)
        self.txtm.setStyleSheet(font_size)
        
        lbl_check1 = QLabel("Nonstationary ts:")
        lbl_check1.setStyleSheet(font_size)
        self.check1 = QCheckBox()
        self.check1.stateChanged.connect(self.state_check)
        
        self.lbl_num_files = QLabel("Files loaded: ")
        self.lbl_num_files.setStyleSheet(font_size)
        
        lbl_file = QLabel("File: ")
        lbl_file.setStyleSheet("font-size: 18px")
        self.list3 = QComboBox()
        self.list3.currentIndexChanged.connect(self.plots)

        self.lbltime = QLabel("Exe. time:")
        self.lbltime.setStyleSheet(font_size)
        self.txttime = QLabel("")
        self.txttime.setStyleSheet(font_size)
        
        b1 = QRadioButton("f(α) Vs α")
        b1.setStyleSheet(font_size)
        
        b2 = QRadioButton("τ(q) Vs q")
        b2.setStyleSheet(font_size)
        
        b3 = QRadioButton("h(q) Vs q")
        b3.setStyleSheet(font_size)
       
        self.plots = QButtonGroup()
        self.plots.addButton(b1)
        self.plots.addButton(b2)
        self.plots.addButton(b3)
        self.plots.exclusive() 
        self.plots.buttonClicked.connect(self.print_val)
        
        lbl_MDFA = QLabel("MFDFA: ")
        lbl_MDFA.setStyleSheet(font_size)
        
        self.list_MDFA = QComboBox()
        self.list_MDFA.currentIndexChanged.connect(self.plots_MDFA)
        
        #################################################################
        ##     Elementos del layout graficos
        #################################################################
        self.plot1=pg.PlotWidget()
        self.plot1.setLabel('bottom'," ", color='k', **{'font-size':'20pt'})
        self.plot1.getAxis('bottom').setPen(pg.mkPen(color='k', width=1))
        # Y1 axis   
        self.plot1.setLabel('left'," ", color='k', **{'font-size':'20pt'})
        self.plot1.getAxis('left').setPen(pg.mkPen(color='k', width=1))
        self.plot1.showGrid(1,1,0.2)
        #################################################################
        ##     Colocar elementos en layout botones
        #################################################################
        botones.addWidget(self.btnLoadSig)
        results.addRow(self.lbl_num_files)
        results.addRow(lbl_file, self.list3)
        results.addRow(lbl_check1, self.check1)
        results.addRow('Q+:', self.txtQmax)
        results.addRow('Q-:', self.txtQmin)
        results.addRow('dQ:',   self.txtdQ)
        results.addRow('m:',    self.txtm)
        results.addRow(self.lbltime, self.txttime)
        results.addRow(self.btnMDFA) 
        results.addRow(lbl_MDFA, self.list_MDFA)
        results.addRow(b1)
        results.addRow(b2)
        results.addRow(b3)
        results.addRow(self.btnSavechar) 
        botones.addLayout(results)
        #################################################################
        ##     Colocar elementos en layout graficos
        #################################################################
        graficos.addWidget(self.plot1)
        bot = QWidget()
        bot.setLayout(botones)        
        gra = QWidget()
        gra.setLayout(graficos)
        contain.addWidget(bot)
        contain.addWidget(gra)
        self.setCentralWidget(contain)
