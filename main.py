import sys
from PyQt5.QtWidgets import (QMainWindow, QApplication, QStatusBar,QFileDialog,
                             QWidget,  QSplitter, QPushButton, QVBoxLayout, QToolBar,
                             QMenuBar, QAction, QFormLayout, QLabel, QLineEdit)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

from modules.DFA import DFA
from modules.MDFA import MDFA
import pyqtgraph as pg  
import numpy as np
import pandas as pd
#%%
class Principal(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()
        
    def DFA_boton(self):
        self.DFAWindow = DFA()
        self.DFAWindow.show()
    def MFDFA_boton(self):
        self.MFDFAWindow = MDFA()
        self.MFDFAWindow.show()

#%%
    def cargarSenial(self):
        self.plot1.clear()
        self.nombreSenial= QFileDialog.getOpenFileName(None, 'Open file', '/home')
        self.ruta = self.nombreSenial[0]
        if(len(self.ruta)!=0):
            print(self.nombreSenial)
            datos = pd.read_csv(self.ruta,sep='\t', header=None)
            lineas= datos.shape[1]
            if(lineas == 1):
                self.y = np.asarray(datos[0])
            elif(lineas == 2):
                self.y = np.asarray(datos[1])
            self.plot1.setLabel('bottom',color='k', **{'font-size':'14pt'})
            self.plot1.getAxis('bottom').setPen(pg.mkPen(color='k', width=1))
            # Y1 axis   
            self.plot1.setLabel('left',color='k', **{'font-size':'14pt'})
            self.plot1.getAxis('left').setPen(pg.mkPen(color='k', width=1))
            names=str.split(self.nombreSenial[0],"/")
            t=len(names)
            self.nombre= names[t-1]
            self.plot1.setTitle(self.nombre)
            self.plot1.plot(self.y,pen='k')
            self.btnIniciar.setEnabled(True)
#%%
    def enabledButtons(self):
        self.btnAdd.setEnabled(True)
        self.btnEnd.setEnabled(True)
        self.txtns.setEnabled(True)
        self.plot1.addItem(self.lr)
        self.btnIniciar.setEnabled(False)
        
#%%      
    def addInterval(self):
        self.contador  = int(self.txtns.text())
        regionSelected = self.lr.getRegion()
        ini = int(regionSelected[0])
        fin = int(regionSelected[1])
        self.duracion.append(self.y[ini:fin])
        self.duracion=np.transpose(self.duracion)
        df = pd.DataFrame(self.duracion)
        names = str.split(self.nombreSenial[0],self.nombre)
        nam   = str.split(self.nombre,'.')
        df.to_csv(names[0]+nam[0]+'_seg_'+str(self.contador)+'.txt',index=False,sep='\t', header = None, mode = 'w') 
        self.duracion = []        
        linea1= pg.InfiniteLine(pos= ini, angle=90, movable=False)
        linea2= pg.InfiniteLine(pos= fin, angle=90, movable=False)
        self.plot1.addItem(linea1)
        self.plot1.addItem(linea2)
        self.lr.setRegion([fin,fin+6000])

#%%
    def reboot(self):
        self.contador=0
        self.valorContador.setText("")

#%% 
    def initUI(self):
        pg.setConfigOption('background', 'w')
        self.setWindowTitle('PyMFDFA')
        self.setWindowIcon(QIcon("Icons\multifractal.ico"))
        self.resize(1000, 600)
        ##################################################################
        ### Barra de Herramientas 
        ##################################################################
        self.barra_estado = QStatusBar()
        self.setStatusBar(self.barra_estado)
        
        barra_herr = QToolBar("Toolbar")
        self.addToolBar(barra_herr)
        
        barra_menu = QMenuBar()
        self.setMenuBar(barra_menu)
        
        abrir_action = QAction(QIcon('Icons/open.png'), 'Load Signal', self)
        abrir_action.setToolTip('Load Signal')
        abrir_action.setStatusTip('Load signal to segment')
        abrir_action.triggered.connect(self.cargarSenial)
        barra_herr.addAction(abrir_action)
        barra_herr.addSeparator()
        
        DFA_action = QAction(QIcon('Icons/DFA.ico'), 'Detrended Analysis Fluctuation', self)
        DFA_action.setToolTip('Detrended Analysis Fluctuation')
        DFA_action.setStatusTip('Detrended Analysis Fluctuation')
        DFA_action.triggered.connect(self.DFA_boton)
        barra_herr.addAction(DFA_action)
        
        MDFA_action = QAction(QIcon('Icons/multifractal.ico'), 'Multifractal Detrended Analysis Fluctuation', self)
        MDFA_action.setToolTip('Multifractal Detrended Analysis Fluctuation')
        MDFA_action.setStatusTip('Multifractal Detrended Analysis Fluctuation')
        MDFA_action.triggered.connect(self.MFDFA_boton)
        barra_herr.addAction(MDFA_action)
        #################################################################
        ##     Definición de variables globales
        #################################################################
        self.ruta = None
        self.nombreSenial=''
        self.x=[]
        self.y=[]
        self.suspiros = []
        self.duracion = []
        self.intervalos = []
        self.contador=0
        self.ini = 0 
        self.fin = 0
        #################################################################
        ##     Definición de elementos contenedores
        #################################################################
        contain=QSplitter(Qt.Horizontal)
        graficos = QVBoxLayout()
        botones = QVBoxLayout()
        results  = QFormLayout()
        #################################################################
        ##     Elementos del layout botones
        #################################################################
        #Region for segment in signal
        self.lr = pg.LinearRegionItem([0,6000])
        self.valorContador = QLabel('')
        
        self.btnIniciar = QPushButton('Start segmentation')
        self.btnIniciar.clicked.connect(self.enabledButtons)
        self.btnIniciar.setEnabled(False)
        self.btnIniciar.setStyleSheet("font-size: 20px")

        self.btnAdd = QPushButton('Add segment')
        self.btnAdd.clicked.connect(self.addInterval)
        self.btnAdd.setEnabled(False)
        self.btnAdd.setStyleSheet("font-size: 20px")
        
        self.btnEnd = QPushButton('Restart segmentation')
        self.btnEnd.clicked.connect(self.reboot)
        self.btnEnd.setEnabled(False)
        self.btnEnd.setStyleSheet("font-size: 20px")

        txtnumseg  = QLabel("Segment number")
        txtnumseg.setStyleSheet("font-size: 20px")
        self.txtns = QLineEdit("")
        self.txtns.setEnabled(False)
        self.txtns.setStyleSheet("font-size: 20px")
        #################################################################
        ##     Elementos del layout graficos
        #################################################################
        self.plot1=pg.PlotWidget()
        self.plot1.setLabel('bottom',color='k', **{'font-size':'20pt'})
        self.plot1.getAxis('bottom').setPen(pg.mkPen(color='k', width=1))
        self.plot1.setLabel('left',color='k', **{'font-size':'20pt'})
        self.plot1.getAxis('left').setPen(pg.mkPen(color='k', width=1))
        self.plot1.showGrid(1,1,0.2)
        graficos.addWidget(self.plot1)
        #################################################################
        ##     Colocar elementos en layout botones
        #################################################################
        botones.addWidget(self.btnIniciar)
        botones.addWidget(self.btnAdd)
        results.addRow(txtnumseg, self.txtns)
        botones.addLayout(results)        
        #################################################################
        ##     Colocar elementos en layout graficos
        ################################################################
        bot = QWidget()
        bot.setLayout(botones)
        gra = QWidget()
        gra.setLayout(graficos)

        contain.addWidget(bot)
        contain.addWidget(gra)
        self.setCentralWidget(contain)
        self.show()
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Principal()
    sys.exit(app.exec_())
        
        
        