from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import (QMainWindow, QDialogButtonBox, QComboBox, QVBoxLayout, QGridLayout, QGroupBox, QDialog, QPushButton, QListWidget, QSplitter, QFileDialog, QWidget, QFormLayout, QLabel, QLineEdit)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
import pyqtgraph as pg 
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

class Dialogo(QtWidgets.QWidget):
    enviar_datos = QtCore.pyqtSignal(int)
    NumGridRows = 3
    NumButtons = 4
    def createFormGroupBox(self):
        self.formGroupBox = QtWidgets.QGroupBox("Asignar variables")
        self.varQComboBox = QtWidgets.QComboBox()
        self.varQComboBox.addItem('f(α)')
        self.varQComboBox.addItem('α')
        self.varQComboBox.addItem('t(q)')
        self.varQComboBox.addItem('h(q)')
        self.varQComboBox.addItem('q')
        self.nombreQLineEdit = QtWidgets.QLineEdit()
        layout = QtWidgets.QFormLayout()
        layout.addRow(QtWidgets.QLabel("Nombre del archivo:"), self.nombreQLineEdit)
        layout.addRow(QtWidgets.QLabel("Variable:"), self.varQComboBox)
        self.formGroupBox.setLayout(layout)
    def __init__(self):
        QtWidgets.QDialog.__init__(self)        
        self.resize(300, 300)
        self.createFormGroupBox()
        buttonBox = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.send_clicked)
        buttonBox.rejected.connect(self.close)
        mainLayout = QtWidgets.QVBoxLayout()
        mainLayout.addWidget(self.formGroupBox)
        mainLayout.addWidget(buttonBox)
        self.setLayout(mainLayout)
    def send_clicked(self):
        self.enviar_datos.emit(str(self.varQComboBox.currentIndex()))
        self.close()


#%%
#%%
class PLOT(QMainWindow):
    def __init__(self):      
        super().__init__()
        self.initUI()
#--------------------- Funciones DFA #-------------------------------------------------------------------------------        
#%%
    def load_DFA_fn(self):
        self.nombreSenial1= QFileDialog.getOpenFileName(None, 'Open file', '/home')
        data = pd.read_csv(self.nombreSenial1[0],sep='\t', header=None)
        data = np.asarray(data)
        data = np.transpose(data)
        self.log_n  = data[2]
        self.log_fn = data[3]
        self.plot1.plot(self.log_n,self.log_fn,symbol='o',pen = 'r')
#%%
    def load_DFA_h(self):
        self.plot1.clear()
        self.nombreSenial1 = QFileDialog.getOpenFileName(None, 'Open file', '/home')
        data = pd.read_csv(self.nombreSenial1[0],sep='\t', header=None)
        data = np.asarray(data)
        self.data = np.transpose(data)
        self.fn = data[0]
        self.h  = data[1]
#%%
    def plot_one(self):
        # x axis    
        self.plot1.setLabel('bottom', 'h', color='k',**{'font-size':'12pt'})
        self.plot1.getAxis('bottom').setPen(pg.mkPen(color='k', width=1))
        # Y1 axis   
        self.plot1.setLabel('left', 'f(n)_max', color='k',**{'font-size':'12pt'})
        self.plot1.getAxis('left').setPen(pg.mkPen(color='k', width=1))
        if(int(self.num_txt.text()) - 1 == 0):
            self.plot1.plot(self.h, self.fn, symbol='o', pen = None)
        else:
            datos = np.transpose(self.data)
            i = int(self.num_txt.text()) - 1
            potencial = datos[i]
            self.plot1.plot(potencial,symbol = 'o', pen = None)
#%%
    def plotclear1(self):
        self.plot1.clear()     
#-------------------------- Funciones para el MFDFA #-------------------------------------------------------------
#%%
#    def asignar(self, variable):
#        if(int(variable)==0):
#            self.fα = np.asarray(pd.read_csv(self.direccion_actual, sep='\t', header=None))
#        elif(int(variable)==1):
#            self.α = np.asarray(pd.read_csv(self.direccion_actual, sep='\t', header=None))
#        elif(int(variable)==2):
#            self.t = np.asarray(pd.read_csv(self.direccion_actual, sep='\t', header=None))
#        elif(int(variable)==3):
#            self.Hq = np.asarray(pd.read_csv(self.direccion_actual, sep='\t', header=None))
#        elif(int(variable)==4):
#            self.q = np.asarray(pd.read_csv(self.direccion_actual, sep='\t', header=None))
    
            
        
#%%
    def load_f(self):
        self.datos  = QFileDialog.getOpenFileNames(None, 'Abrir archivos', '/home')
        self.direcciones = self.datos[0]
        for i in range(len(self.direcciones)):
            self.dialogo.nombreQLineEdit.setText(self.direcciones[i])
            self.direccion_actual = self.direcciones[i]
            self.dialogo.setWindowTitle("Abrir archivo: "+str(i+1)+" "+ "de "+str(len(self.direcciones)))
            self.dialogo.exec_()
#            self.asignar()
#%%
    def plot1(self):
        symbolS = self.colortxt.text()
        # x axis    
        self.plot2.setLabel('bottom', 'α',color='k',**{'font-size':'12pt'})
        self.plot2.getAxis('bottom').setPen(pg.mkPen(color='k', width=1))
        # Y1 axis   
        self.plot2.setLabel('left', 'f(α)',color='k', **{'font-size':'12pt'})
        self.plot2.getAxis('left').setPen(pg.mkPen(color='k', width=1))
        if(int(self.num_graftxt.text())==0):
            self.plot2.clear()
            for i in range(len(self.fα)):
                self.plot2.plot(self.α[i],self.fα[i],pen=None, symbol='o', symbolSize=symbolS)
        else:
            i = int(self.num_graftxt.text()) - 1
            self.plot2.plot(self.α[i],self.fα[i],pen=None, symbol='o', symbolSize=symbolS)
            
#%%
    def plot2(self):
        symbolS = self.colortxt.text()
        self.plot2.setLabel('bottom', 'q',color='k',**{'font-size':'12pt'})
        self.plot2.getAxis('bottom').setPen(pg.mkPen(color='k', width=1))
        # Y1 axis   
        self.plot2.setLabel('left', 't(q)',color='k', **{'font-size':'12pt'})
        self.plot2.getAxis('left').setPen(pg.mkPen(color='k', width=1))
        if(int(self.num_graftxt.text())==0):   
            self.plot2.clear()
            for i in range(len(self.t)):
                self.plot2.plot(self.q[i],self.t[i],pen=None,symbol='o',symbolSize=symbolS)
        else:
            i = int(self.num_graftxt.text()) - 1
            self.plot2.plot(self.q[i],self.t[i],pen=None, symbol='o', symbolSize=symbolS)
#%%
    def plot3(self):
        symbolS = self.colortxt.text()
        self.plot2.setLabel('bottom', 'q',color='k',**{'font-size':'12pt'})
        self.plot2.getAxis('bottom').setPen(pg.mkPen(color='k', width=1))
        # Y1 axis   
        self.plot2.setLabel('left', 'h(q)',color='k', **{'font-size':'12pt'})
        self.plot2.getAxis('left').setPen(pg.mkPen(color='k', width=1))
        if(int(self.num_graftxt.text())==0):   
            self.plot2.clear()
            for i in range(len(self.Hq)):
                self.plot2.plot(self.q[i],self.Hq[i],pen=None,symbol='o',symbolSize=symbolS)
        else:
            i = int(self.num_graftxt.text()) - 1
            self.plot2.plot(self.q[i],self.Hq[i],pen=None, symbol='o', symbolSize=symbolS)
#%%        
    def plotclear(self):
        self.plot2.clear()
#%%
    def exportplot2(self):
        nom = QFileDialog.getSaveFileName(None, 'Saving Data in Current Plot')
        exporter = pg.exporters.ImageExporter(self.plot2.plotItem)
        exporter.parameters()['width'] = 100
        exporter.export(nom[0]+'png')

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
###############################################################################
########Variables Globales ####################################################
###############################################################################        
        self.ruta = None
        self.nombreSenial1=[]
        self.nombreSenial=[]
        self.x=[]
        self.y1=[]
        self.y2=[]
        self.h1=[]
        self.h2=[]
        self.fα   = 0
        self.α    = 0
        self.t    = 0
        self.Hq   = 0
        self.q    = 0
       
        contain       = QSplitter(Qt.Vertical)
        contenedor    = QSplitter(Qt.Horizontal)
        botones       = QtWidgets.QVBoxLayout()
        botones2      = QtWidgets.QVBoxLayout()
        titulo1       = QtWidgets.QVBoxLayout()
        titulo2       = QtWidgets.QVBoxLayout()
        graficos      = QSplitter(Qt.Horizontal)
        resultsMFDFA  = QFormLayout()
        resultsDFA    = QFormLayout()
        grupbtn       = QGridLayout()
        grupbtn2      = QGridLayout()
        
        self.dialogo = Dialogo()
#        self.login.enviar_datos.connect(self.asignar)
        
        self.setWindowTitle('Graficar')
        self.setWindowIcon(QIcon("graficar.JPG"))
        #################################################################
        ##     Elementos del layout botones
        ################################################################# 
        
        #---------------- DFA -----------------------------------------
        btnLoadSigDFA = QPushButton('Cargar f(n) y n')
        btnLoadSigDFA.clicked.connect(self.load_DFA_fn)
        btnLoadSigDFA.setStyleSheet("font-size: 12px")
        
        btnLoadchar = QPushButton('Cargar características')
        btnLoadchar.clicked.connect(self.load_DFA_h)
        btnLoadchar.setStyleSheet("font-size: 12px")
        
        self.num_dfatxt = QLabel("")
        self.num_dfatxt.setStyleSheet("font-size: 12px")
        
        self.num_txt = QLineEdit("")
        self.num_txt.setStyleSheet("font-size: 12px")
        
        self.colorDFAtxt = QLineEdit("")
        self.colorDFAtxt.setStyleSheet("font-size: 12px")
        
        btngraf_one = QPushButton('Graficar exponente')
        btngraf_one.clicked.connect(self.plot_one)
        btngraf_one.setStyleSheet("font-size: 12px")
        
        btnClearPlot1 = QPushButton('Limpiar Grafica')
        btnClearPlot1.clicked.connect(self.plotclear1)
        btnClearPlot1.setStyleSheet("font-size: 12px")
        
        #----------- MFDFA ------------------------------------
        
        btnLoadSig_f = QPushButton('Cargar Datos ')
        btnLoadSig_f.clicked.connect(self.load_f)
        btnLoadSig_f.setStyleSheet("font-size: 12px")
             
        self.num_espectxt = QLabel("")
        self.num_espectxt.setStyleSheet("font-size: 12px")
        
        self.num_graftxt = QLineEdit("")
        self.num_graftxt.setStyleSheet("font-size: 12px")
        
        self.colortxt = QLineEdit("")
        self.colortxt.setStyleSheet("font-size: 12px")
        self.colortxt.setInputMask("9")
        self.colortxt.setMaxLength(1)
        
        self.btnF = QPushButton('f(α) Vs α')
        self.btnF.clicked.connect(self.plot1)
        self.btnF.setStyleSheet("font-size: 12px")
        
        self.btnt = QPushButton('τ(q) Vs q')
        self.btnt.clicked.connect(self.plot2)
        self.btnt.setStyleSheet("font-size: 12px")
        
        self.btnh = QPushButton('H(q) Vs q')
        self.btnh.clicked.connect(self.plot3)
        self.btnh.setStyleSheet("font-size: 12px")
   
        btnClearPlot = QPushButton('Limpiar Grafica')
        btnClearPlot.clicked.connect(self.plotclear)
        btnClearPlot.setStyleSheet("font-size: 12px")

        btnGuardar1 = QPushButton('Guardar Grafica')
        btnGuardar1.clicked.connect(self.exportplot2)
        btnGuardar1.setStyleSheet("font-size: 12px")
        
        btnGuardar2 = QPushButton('Exportar Gráfica')
        btnGuardar2.clicked.connect(self.exportplot2)
        btnGuardar2.setStyleSheet("font-size: 12px")
        
        #----------- Elementos de la ventana Dialogo ----------------------
        
        
        
        
        #################################################################
        ##     Colocar elementos en layout botones
        ################################################################# 
        botones.addWidget(btnLoadSigDFA)
        botones.addWidget(btnLoadchar)
        resultsDFA.addRow('Número de datos:', self.num_dfatxt)
        resultsDFA.addRow('Número de exponente:', self.num_txt)
        resultsDFA.addRow('Tamano de símbolo:', self.colorDFAtxt)
        botones.addLayout(resultsDFA)
        botones.addWidget(btngraf_one)
        botones.addWidget(btnClearPlot1)
        grupbtn.addWidget(btnLoadSig_f,0,0)
        grupbtn.addWidget(self.btnF,0,1)
        grupbtn.addWidget(self.btnt,1,0)
        grupbtn.addWidget(self.btnh,1,1)
        resultsMFDFA.addRow('Total de espectros:', self.num_espectxt)
        resultsMFDFA.addRow('Número de espectro:', self.num_graftxt)
        resultsMFDFA.addRow('Tamaño del Símbolo:', self.colortxt)
        grupbtn2.addWidget(btnGuardar2,0,0)
        grupbtn2.addWidget(btnClearPlot,0,1)
        
        botones2.addLayout(grupbtn)
        botones2.addLayout(resultsMFDFA)
        botones2.addLayout(grupbtn2)
        #################################################################
        ##     Colocar elementos en layout graficos
        #################################################################
        self.plot1=pg.PlotWidget(title="Detrended Analysis Fluctuation")
        # x axis    
        self.plot1.setLabel('bottom', '', color='k', **{'font-size':'12pt'})
        self.plot1.getAxis('bottom').setPen(pg.mkPen(color='k', width=1))
        # Y1 axis   
        self.plot1.setLabel('left', '', color='r', **{'font-size':'12pt'})
        self.plot1.getAxis('left').setPen(pg.mkPen(color='k', width=1))
        self.plot1.showGrid(1,1,0.2)
        
        self.plot2=pg.PlotWidget(title="Multifractal Detrended Analysis Fluctuation")
        self.plot2.setLabel('bottom', '', color='k', **{'font-size':'12pt'})
        self.plot2.getAxis('bottom').setPen(pg.mkPen(color='k', width=1))
        # Y1 axis   
        self.plot2.setLabel('left', '', color='r', **{'font-size':'12pt'})
        self.plot2.getAxis('left').setPen(pg.mkPen(color='k', width=1))
        self.plot2.showGrid(1,1,0.2)
        
        graficos.addWidget(self.plot1)
        tit1 = QWidget()
        tit1.setLayout(titulo1)
        bot = QWidget()
        bot.setLayout(botones)
        contenedor.addWidget(bot)
        
        
        graficos.addWidget(self.plot2)
        bot2 = QWidget()
        bot2.setLayout(botones2)
        tit2 = QWidget()
        tit2.setLayout(titulo2)
        contenedor.addWidget(bot2)
        
        contain.addWidget(graficos)
        contain.addWidget(contenedor)
   
        self.setCentralWidget(contain)

        
