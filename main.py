import sys
from PyQt5.QtWidgets import (QMainWindow, QApplication, QStatusBar,QFileDialog,
                             QWidget,  QSplitter, QPushButton, QVBoxLayout, QToolBar,
                             QMenuBar, QAction, QFormLayout, QLabel
                             ,QLineEdit, QComboBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QIntValidator

from modules.DFA import DFA
from modules.MDFA import MDFA
from modules.Dialog import Dialog
import pyqtgraph as pg  

from numpy import (asarray, transpose,arange,where)
from pandas import (read_csv, DataFrame)
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
        self.txt_total.setText('')
        self.lbl_inicio.setText('')
        self.lbl_final.setText('')
        self.seg_pos.clear()
        self.btnIniciar.setEnabled(True)
        self.plot1.clear()
        self.nombreSenial= QFileDialog.getOpenFileName(None, 'Open file', '/home')
        if(len(self.nombreSenial[0])!=0):
            print(self.nombreSenial)
            datos = read_csv(self.nombreSenial[0],sep='\t', header=None)
            lineas= datos.shape[1]
            if(lineas == 1):
                self.y = asarray(datos[0])
                self.y_auto = datos[0]
            elif(lineas == 2):
                self.y = asarray(datos[1])
                self.y_auto = datos[1]
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
            self.btnauto.setEnabled(True)
#%%
    def localizacion(self):
        if(self.aux == True):
            i = self.seg_pos.currentIndex()
            if(i == 0):
                self.lbl_inicio.setText('ini')
                self.lbl_final.setText('end')
            else:
                self.lbl_inicio.setText(str(self.inicio[i-1]))
                self.lbl_final.setText(str(self.final[i-1]))
#%%
    def colocar(self):
        inicio = int(self.lbl_inicio.text())
        final  = int(self.lbl_final.text())
        if(self.aux2 == True):
            self.lr.setRegion([inicio,final])

#%% 
    def autoseg(self):
        self.aux == False
        self.inicio = []
        self.final  = []
        self.seg_pos.clear()
        self.seg_pos.addItem('')
        def group_consecutives(vals, step=1):
            run = []
            result = [run]
            expect = None
            for v in vals:
                if (v == expect) or (expect is None):
                    run.append(v)
                else:
                    run = [v]
                    result.append(run)
                expect = v + step
            return result
        if(len(self.txt_umbral.text())!=0 and len(self.txt_basal.text())!=0 and len(self.txt_ancho.text())!=0 
           and len(self.txt_separacion.text())!=0):
            umbral     = float(self.txt_umbral.text())
            basal      = float(self.txt_basal.text())
            ancho      = float(self.txt_ancho.text())
            separacion = float(self.txt_separacion.text())        
            y = self.y_auto
            
            loc_x = []
            for i in range(len(y)):
                if(y[i]>umbral):
                    loc_x.append(i) 
                    
            pico_range = group_consecutives(loc_x)        
            
            loc_x1 = []
            for i in range(len(pico_range)):
                aux  = pico_range[i]
                pico = list(y[aux])
                pos_aux = pico.index(max(pico))
                loc_x1.append(aux[pos_aux])
                    
            loc = []
            loc.append(loc_x[0])
            for i in range(1,len(loc_x1)):
                if(loc_x1[i]-loc_x1[i-1]>ancho):
                    loc.append(loc_x1[i])
                    
            ini = []
            end = []        
            for i in range(len(loc)):
                if(loc[0]>2*separacion ):
                    x_ini   = arange(loc[i]-separacion,loc[i])
                    y_ini   = y[x_ini]
                    
                    x_end   = arange(loc[i],loc[i] + separacion)
                    y_end   = y[x_end]
                    
                    donde_ini = where(y_ini <= min(y_ini) + basal)[0]
                    donde_fin = where(y_end <= min (y_ini) + basal)[0]
                                
                    if(len(donde_fin)!=0 and len(donde_ini)!=0 ):
                        ini.append(x_ini[max(donde_ini)])
                        end.append(x_end[min(donde_fin)]) 
                elif(loc[0]<separacion):
                    x_ini   = arange(0,loc[i])
                    y_ini   = y[x_ini]
                    
                    x_end   = arange(loc[i],loc[i] + separacion)
                    y_end   = y[x_end]
                    
                    donde_ini = where(y_ini <= min(y_ini) + basal)[0]
                    donde_fin = where(y_end <= min (y_ini) + basal)[0]
                                
                    if(len(donde_fin)!=0 and len(donde_ini)!=0 ):
                        ini.append(x_ini[max(donde_ini)])
                        end.append(x_end[min(donde_fin)]) 
                        
                elif(len(y) - (loc[len(loc)-1] + separacion) < 0 ):
                    x_ini   = arange(loc[i]-separacion,loc[i])
                    y_ini   = y[x_ini]
                    
                    x_end   = arange(loc[i],len(y))
                    y_end   = y[x_end]
                    
                    donde_ini = where(y_ini <= min(y_ini) + basal)[0]
                    donde_fin = where(y_end <= min (y_ini) + basal)[0]
                                
                    if(len(donde_fin)!=0):
                        ini.append(x_ini[max(donde_ini)])
                        end.append(x_end[min(donde_fin)]) 
            ini = list(set(ini))
            end = list(set(end))
            ini = list(sorted(ini))
            end = list(sorted(end))
            names = str.split(self.nombreSenial[0],self.nombre)
            nam   = str.split(self.nombre,'.') 
    
            for i in range(len(ini)):
                self.seg_pos.addItem(str(i+1))
                self.inicio.append(int(ini[i]))
                self.final.append(int(end[i]))
                data = DataFrame(y[int(ini[i]):int(end[i])])
                data.to_csv(names[0]+nam[0]+'_seg_'+ str(i+1) +'.txt',sep ='\t', header = None, index = False)
            self.aux = True
            self.txt_total.setText(str(len(self.inicio)))
            self.btn_loc.setEnabled(True)
            self.btnauto.setEnabled(False)
        elif(len(self.txt_umbral.text())!=0 or len(self.txt_basal.text())!=0 or len(self.txt_ancho.text())!=0 
           or len(self.txt_separacion.text())!=0):
            self.dialogo_error = Dialog('Error: Missing value ','Icons\error.png')
            self.dialogo_error.show()
        elif(len(self.txt_umbral.text())!=0 and len(self.txt_basal.text())!=0 and len(self.txt_ancho.text())!=0 
           and len(self.txt_separacion.text())!=0):
            self.dialogo_error = Dialog('Error: Missing value ','Icons\error.png')
            self.dialogo_error.show()
            
#%%
    def enabledButtons(self):
        self.btnAdd.setEnabled(True)
        self.txtns.setEnabled(True)
        self.plot1.addItem(self.lr)
        self.btnIniciar.setEnabled(False)
        self.aux2 = True
#%%      
    def addInterval(self):
        duracion = []
        contador = 0
        if(len(self.txtns.text())==0):
            self.dialogo_error = Dialog('A segment number must be type() = int ','Icons\error.png')
            self.dialogo_error.show()
        else:
            contador  = int(self.txtns.text())
            regionSelected = self.lr.getRegion()
            ini = int(regionSelected[0])
            fin = int(regionSelected[1])
            duracion.append(self.y[ini:fin])
            duracion = transpose(duracion)
            df = DataFrame(duracion)
            names = str.split(self.nombreSenial[0],self.nombre)
            nam   = str.split(self.nombre,'.')
            df.to_csv(names[0]+nam[0]+'_seg_'+str(contador)+'.txt',index=False,sep='\t', header = None, mode = 'w') 
            duracion = []        
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
        self.nombreSenial = ''
        self.y = []
        self.aux = 0
        self.aux2 = False
        #################################################################
        ##     Definición de elementos contenedores
        #################################################################
        contain = QSplitter(Qt.Horizontal)
        graficos = QVBoxLayout()
        botones  = QVBoxLayout()
        results2 = QFormLayout()
        results3 = QFormLayout()
        results  = QFormLayout()
        #################################################################
        ##     Elementos del layout botones
        #################################################################
        #Region for segment in signal
        self.lr = pg.LinearRegionItem([0,6000])
        
        btnLoadSig = QPushButton('Load signal')
        btnLoadSig.clicked.connect(self.cargarSenial)
        btnLoadSig.setStyleSheet("font-size: 18px")
        
        self.btnIniciar = QPushButton('Start segmentation')
        self.btnIniciar.clicked.connect(self.enabledButtons)
        self.btnIniciar.setEnabled(False)
        self.btnIniciar.setStyleSheet("font-size: 18px")

        self.btnAdd = QPushButton('Add segment')
        self.btnAdd.clicked.connect(self.addInterval)
        self.btnAdd.setEnabled(False)
        self.btnAdd.setStyleSheet("font-size: 18px")
        
        txtnumseg  = QLabel("Segment num:")
        txtnumseg.setStyleSheet("font-size: 18px")
                
        validator = QIntValidator()
        validator.setRange(100,999)  
        
        self.txtns = QLineEdit()
        self.txtns.setValidator(validator)
        self.txtns.setEnabled(False)
        
        lbl_umbral = QLabel('Upper threshold:')
        lbl_umbral.setStyleSheet("font-size: 18px")
        self.txt_umbral = QLineEdit()
        
        lbl_basal = QLabel('Lower threshold')
        lbl_basal.setStyleSheet("font-size: 18px")
        self.txt_basal = QLineEdit()
        
        lbl_ancho = QLabel('Segment width ')
        lbl_ancho.setStyleSheet("font-size: 18px")
        self.txt_ancho = QLineEdit()
        
        lbl_separacion = QLabel('Distance:')
        lbl_separacion.setStyleSheet("font-size: 18px")
        self.txt_separacion = QLineEdit()
        
        self.btnauto = QPushButton('Start auto-segmentation')
        self.btnauto.clicked.connect(self.autoseg)
        self.btnauto.setStyleSheet("font-size: 18px")
        self.btnauto.setEnabled(False)
        
        lbl_total = QLabel('# of segments:')
        lbl_total.setStyleSheet('font-size: 18px')
        
        self.txt_total = QLabel()
        self.txt_total.setStyleSheet('font-size: 18px')
        
        lbl_file = QLabel('Segment: ')
        lbl_file.setStyleSheet("font-size: 18px")
        self.seg_pos = QComboBox()
        self.seg_pos.currentIndexChanged.connect(self.localizacion)
        
        self.lbl_inicio = QLabel()
        self.lbl_inicio.setStyleSheet("font-size: 18px")
        self.lbl_final = QLabel()
        self.lbl_final.setStyleSheet("font-size: 18px")
        
        self.btn_loc = QPushButton('Find segment')
        self.btn_loc.setStyleSheet("font-size: 18px")
        self.btn_loc.clicked.connect(self.colocar)
        self.btn_loc.setEnabled(False)
        
        lbl_autoseg = QLabel("Auto-Segmentation")
        lbl_autoseg.setStyleSheet("font-size: 20px")
        #################################################################
        ##     Elementos del layout graficos
        #################################################################
        self.plot1=pg.PlotWidget()
        self.plot1.setLabel('bottom',color='k', **{'font-size':'16pt'})
        self.plot1.getAxis('bottom').setPen(pg.mkPen(color='k', width=1))
        self.plot1.setLabel('left',color='k', **{'font-size':'16pt'})
        self.plot1.getAxis('left').setPen(pg.mkPen(color='k', width=1))
        self.plot1.showGrid(1,1,0.2)
        graficos.addWidget(self.plot1)
        #################################################################
        ##     Colocar elementos en layout botones
        #################################################################
        botones.addWidget(btnLoadSig)
        botones.addWidget(self.btnIniciar)
        results.addRow(txtnumseg, self.txtns)
        results.addRow(self.btnAdd)
        botones.addLayout(results)     
        
        results2.addRow(lbl_autoseg)
        results2.addRow(lbl_umbral, self.txt_umbral)
        results2.addRow(lbl_basal , self.txt_basal)
        results2.addRow(lbl_ancho , self.txt_ancho)
        results2.addRow(lbl_separacion, self.txt_separacion)
        botones.addLayout(results2)        
        botones.addWidget(self.btnauto)
        results3.addRow(lbl_total,self.txt_total)
        results3.addRow(lbl_file,self.seg_pos)
        results3.addRow(self.lbl_inicio,self.lbl_final)
        results3.addRow(self.btn_loc)
        botones.addLayout(results3)
        #################################################################
        ##     Colocar elementos en la ventana
        #################################################################        
        bot = QWidget()
        bot.setLayout(botones)
        gra = QWidget()
        gra.setLayout(graficos)

        contain.addWidget(gra)
        contain.addWidget(bot)
        self.setCentralWidget(contain)
        self.show()
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Principal()
    sys.exit(app.exec_())
        
        
        