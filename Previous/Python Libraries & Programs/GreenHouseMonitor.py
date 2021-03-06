# -*- coding: utf-8 -*-
"""
Created on Sun Feb 23 14:17:30 2020
@author: Pankaja Suganda
"""
import cv2 as cv
import numpy as np
import tkinter as GHMonitor
from tkinter import ttk as widget
from tkinter import messagebox
from gaugelib import DrawGauge2 as Gauge
from PIL import ImageTk, Image
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import csv as reader
#from smbus import SMBus
import time

#bus = SMBus(1)
#slaveAddress = 0x12

Temperature_Index = 1
Humidity_Index = 2
Light_Index = 3
Heat_Index = 4
moisture_index = 5
Pump_On = 6
Pump_Off = 7
Fan_On = 8
Fan_Off = 9
        
        
def imageload(root):
    TImage = Image.open('/home/pi/Desktop/Green House/Plant Images/PlantTest.jpg')
#     Img = TImage.resize((300, 410), Image.ANTIALIAS)
    Imgs = ImageTk.PhotoImage(TImage)
    root.TestImg.create_image(152, 200, image = Imgs)
def getImages(ID):
    print("Id :")
    print (ID)
    SImg = Image.open('Plant Images/Plant_'+ID+'.jpg')
    SImg = SImg.resize((300, 410), Image.ANTIALIAS)
    LImg = SImg.resize((700, 900), Image.ANTIALIAS)
    #        
    SProcimg = Image.open('Plant Images/Procssed_Plant_Image.jpg')
    SProcimg = SProcimg.resize((300, 410), Image.ANTIALIAS)
    LProcimg = SProcimg.resize((700, 900), Image.ANTIALIAS)
    
    TImage = Image.open('/home/pi/Desktop/Green House/Plant Images/PlantTest.jpg')
    TImage = TImage.resize((298, 400), Image.ANTIALIAS)
    Imgs = np.array([ ImageTk.PhotoImage(SImg), ImageTk.PhotoImage(SProcimg), 
                     ImageTk.PhotoImage(LImg), ImageTk.PhotoImage(LProcimg), ImageTk.PhotoImage(TImage)])
    return Imgs

def SaveCData(column,data):
    filepath = "/home/pi/Desktop/Green House/ControlData.csv"
    fieldnames = ['PPTime','Moisture','FTime','STime','TTime','ALength','Awidth','PumpState','FanState']
    x=[]
    with open(filepath,'r') as csvfile:
        readData = reader.DictReader(csvfile)
        for row in readData:
            x=row
    csvfile.close()
    x[column]=data
    with open(filepath,'w') as myfile:
        writer = reader.DictWriter(myfile,fieldnames)
        writer.writeheader() ## Headers Write to the CSV
        writer.writerow(x)
    myfile.close()

    
def TakeCData():
    filepath = "/home/pi/Desktop/Green House/ControlData.csv"
    x=""
    with open(filepath,'r') as csvfile:
        readData = reader.DictReader(csvfile)
        for row in readData:
            x=row
    csvfile.close()
    print (x)
    return x

def CheckTxt(text,index):
    charArr = list(text)
    if (index==0 and not text==''):
        if (len(charArr)==5):
            for i in range(0,len(charArr)):
                if not (i==2) and not (charArr[i].isdigit()):
                    return False
            if (charArr[2]==':'): return True
            else: return False
        else:
            return False

    elif (index==1 and not text==''):
        if(len(charArr)<=5):
            for i in range(0,len(charArr)):
                if not (charArr[i].isdigit()):
                    return False
            return True
        else:
            return False
        
def StringToBytes(val):
    retVal =""
    for c in val:
        if not (c==255) :
             retVal= retVal+(chr(c))
    return retVal


def readVal(index):
#    bus.write_byte(slaveAddress,index)
#    time.sleep(0.05)
#    d = bus.read_i2c_block_data(slaveAddress,index,12)
    return 100#StringToBytes(d),d


class Application(GHMonitor.Frame):
    
    def __init__(self, master=None):
        super().__init__(master)
        ImgArr = np.array(['Icon/SMoisture.png','Icon/Humidity.png','Icon/Light.jpg'])
        self.Units =  ['','','mm','mm',' %','mm','mm',' Lux',' C',' MC%',' M']
        
        self.IconArr = []
        for i in range(len(ImgArr)):
            icon = Image.open(ImgArr[i])
            icon = icon.resize((120, 120), Image.ANTIALIAS)
            self.IconArr.append(ImageTk.PhotoImage(icon))
       
        self.master = master
        self.master.title("Green House Monitor")
#         self.master.state('zoomed')
        self.pack()
        self.create_widgets()
        self.ValuesUpdate()
    def create_widgets(self):
        #Creating Tabs
        TabParent = widget.Notebook(self.master,height=925,width=1820)
        TabMonitor = widget.Frame(TabParent)
        TabControl = widget.Frame(TabParent)
        TabImage = widget.Frame(TabParent)
        TabParent.add(TabMonitor, text="    Monitoring    ")
        TabParent.add(TabControl, text="    Controlling    ")
        TabParent.add(TabImage, text=  "    Images    ")
        TabParent.pack(fill= 'both',expand=1, )
        TabParent.place(x=90,y=50)
        TabImage.state = GHMonitor.DISABLED
        
        #Draw a verticle and Horizontal Margin
        GHMonitor.Label(self.master,height = '2', width = '10'  ,bg='green').pack(fill=GHMonitor.X)
        GHMonitor.Label(self.master,height = '10', width = '10'  ,bg='dimgrey').pack(side=GHMonitor.LEFT, fill=GHMonitor.Y)
        
        self.Refresh = GHMonitor.Button(self.master,height = '3', width = '6',command=self.ValuesUpdate,bg='light gray', text='Refresh')
        self.Refresh.place(x=3,y=920)
        self.Id = GHMonitor.Label(self.master, text="",fg='white',bg='green')
        self.Id.place(x=0,y=8)
        self.Date = GHMonitor.Label(self.master, text="",fg='white',bg='green')
        self.Date.place(x=1700,y=8)
        
        #Placed a Gauge Farme & Gauges
        GaugeFrame = GHMonitor.LabelFrame(TabMonitor, text="Gauges",height=445,width=450,font = ("Times New Roman",11,"bold"))
        GaugeFrame.place(x=650, y=3)
        
        self.gaugeTem = Gauge(GaugeFrame, max_value=100, min_value=0, size=200, bg_col='red', unit = "C",label="Temperature",bg_sel = 2)
        self.gaugeTem.place( x=5, y=5)
        self.gaugeHum = Gauge(GaugeFrame, max_value=100, min_value=0, size=200, bg_col='Blue', unit = "%MC",label="Humidity",bg_sel = 2)
        self.gaugeHum.place( x=5, y=210)
        self.gaugeMoi = Gauge(GaugeFrame, max_value=100, min_value=0, size=200, bg_col='Green', unit = "%MC",label="Moisture",bg_sel = 2)
        self.gaugeMoi.place( x=210, y=5)
        self.gaugeLight = Gauge(GaugeFrame, max_value=100, min_value=0, size=200, bg_col='Yellow', unit = "Lux",label="Light",bg_sel = 2)
        self.gaugeLight.place(x=210, y=210)
        
        #Placed a Image Farme & Images
        ImageFrame = GHMonitor.LabelFrame(TabMonitor, text="Images", height=445, width=650, font = ("Times New Roman",11,"bold"))
        ImageFrame.place(x=1130, y=3)
        
        self.CurrentImg = GHMonitor.Canvas(ImageFrame, width=300, height=400,bg='green')
        self.CurrentImg.place(x=10, y=10)
        self.ProgImg = GHMonitor.Canvas(ImageFrame, width=300, height=400,bg='green')
        self.ProgImg.place(x=320, y=10)
        
        # place aPlant details
        PlantDframe = GHMonitor.LabelFrame(TabMonitor, text="",height=440,width=300)
        PlantDframe.place(x=10, y=10)
        GHMonitor.Label(PlantDframe, text="Plant Details",bg='orange',height = 3 ,width = 33,
                        font = ("Times New Roman",12,"bold")).place(x=10,y=25)
        
        GHMonitor.Label(PlantDframe, text="Height (mm)",bg='white',height = 2 ,width = 38,
                        font = ("Times New Roman",11,"bold")).place(x=10,y=95)
        self.lblPlantHeight = GHMonitor.Label(PlantDframe, text="Height",bg='white',height = 2 ,width = 33)
        self.lblPlantHeight.place(x=10,y=138)
        
        GHMonitor.Label(PlantDframe, text="Width (mm)",bg='white',height = 2 ,width = 38,
                        font = ("Times New Roman",11,"bold")).place(x=10,y=195)
        self.lblPlantWidth = GHMonitor.Label(PlantDframe, text="Width",bg='white',height = 2 ,width = 33)
        self.lblPlantWidth.place(x=10,y=238)
        
        GHMonitor.Label(PlantDframe, text="Area Persentage(%)",bg='white',height = 2 ,width = 38,
                        font = ("Times New Roman",11,"bold")).place(x=10,y=295)
        self.lblPlantAreaPres = GHMonitor.Label(PlantDframe, text="Width",bg='white',height = 2 ,width = 33)
        self.lblPlantAreaPres.place(x=10,y=338)
        
        # place a Reference details
        RefDframe = GHMonitor.LabelFrame(TabMonitor, text="",height=440,width=300)
        RefDframe.place(x=330, y=10)
        GHMonitor.Label(RefDframe, text="Reference Details",bg='light green',height = 3 ,width = 33,
                        font = ("Times New Roman",12,"bold")).place(x=10,y=25)
        GHMonitor.Label(RefDframe, text="Height (mm), Actual : 20 mm",bg='white',height = 2 ,width = 38,
                        font = ("Times New Roman",11,"bold")).place(x=10,y=95)
        self.lblRefHeight = GHMonitor.Label(RefDframe, text="Height",bg='white',height = 2 ,width = 33)
        self.lblRefHeight.place(x=10,y=138)
        
        GHMonitor.Label(RefDframe, text="Width (mm) , Actual : 20 mm",bg='white',height = 2 ,width = 38,
                        font = ("Times New Roman",11,"bold")).place(x=10,y=195)
        self.lblReftWidth = GHMonitor.Label(RefDframe, text="Width",bg='white',height = 2 ,width = 33)
        self.lblReftWidth.place(x=10,y=238)
        
        GHMonitor.Label(RefDframe, text="Area (%)",bg='white',height = 2 ,width = 38,
                        font = ("Times New Roman",11,"bold")).place(x=10,y=295)
        self.lblRefArea = GHMonitor.Label(RefDframe, text="Width",bg='white',height = 2 ,width = 33)
        self.lblRefArea.place(x=10,y=338)
        
        #Create a Graph
        self.Graphframe = GHMonitor.LabelFrame(TabMonitor, text="Graphs",height=475,width=1770, font = ("Times New Roman",11,"bold"))
        self.Graphframe.place(x=10, y=450)
        self.fig = Figure(figsize=(5,5), dpi=100)
        
        self.graph = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, self.Graphframe)
        self.canvas.get_tk_widget().place(x=20, y=25,height=420,width=1100)
        
        #Graph Controlers
        GHMonitor.Label(self.Graphframe, text="X axis Variable : ", font = ("Times New Roman",12)).place(x=1145,y=20)
        self.CXIcon = GHMonitor.Canvas(self.Graphframe, height = 142,width = 150,bg='light blue')
        self.CXIcon.place(x=1145,y=50)
       
        self.lblCurrentX = GHMonitor.Label(self.Graphframe, text="",bg ="light blue",width=30 ,height=1, anchor = 'w',padx=40,
                                           font = ("Times New Roman",14,"bold"))
        self.lblCurrentX.place(x=1305,y=50)
        self.lblCurrentXVal = GHMonitor.Label(self.Graphframe, text="",bg ="white",width=18 ,height=3 , anchor = 'nw',padx=40,
                                              font = ("MS Serif",18))
        self.lblCurrentXVal.place(x=1305,y=85)
        
        GHMonitor.Label(self.Graphframe, text="Y axis Variable : ", font = ("Times New Roman",12)).place(x=1145,y=220)
        self.CYIcon = GHMonitor.Canvas(self.Graphframe, height = 142,width = 150,bg='orange')
        self.CYIcon.place(x=1145,y=250)
        self.lblCurrentY = GHMonitor.Label(self.Graphframe, text=" ",bg ="orange",width=30 ,height=1, anchor = 'w',padx=40,
                                           font = ("Times New Roman",14,"bold"))
        self.lblCurrentY.place(x=1305,y=250)
        self.lblCurrentYVal = GHMonitor.Label(self.Graphframe, text="",bg ="white",width=18 ,height=3 , anchor = 'nw', padx=40,
                                              font = ("MS Serif",18))
        self.lblCurrentYVal.place(x=1305,y=285)
        
        icon = Image.open('Icon/SMoisture.png')
        icon = icon.resize((120, 120), Image.ANTIALIAS)
        self.XiconSupport = self.CXIcon.create_image(75, 71, image = ImageTk.PhotoImage(icon))
        self.YiconSupport  = self.CYIcon.create_image(75, 71, image = ImageTk.PhotoImage(icon))
        
        self.btnPlot = GHMonitor.Button(self.Graphframe, text="Plot", height = 1, width = 14,
                                        font = ("Times New Roman",11,"bold"), state=GHMonitor.DISABLED)
        self.btnPlot.place(x=1533,y=405)
        self.btnPlot['command'] = self.PlotClick
        self.ComValues = ['ID','DateTime','Height','Width','AreaPresentage','RefHeight','RefWidth','Light','Temperature','Humidity','Moisture']
        self.XaxisCombo = widget.Combobox(self.Graphframe, text = "Select X-axis Parameter",width=42,state='readonly',values=self.ComValues)
        self.XaxisCombo.place(x=1305,y=20)
        self.XaxisCombo.bind("<<ComboboxSelected>>", self.XCombo)
        self.YaxisCombo = widget.Combobox(self.Graphframe, text = "Select Y-axis Parameter",width=42,state=GHMonitor.DISABLED,values=self.ComValues)
        self.YaxisCombo.place(x=1305,y=220)
        self.YaxisCombo.bind("<<ComboboxSelected>>", self.YCombo)
        
        ##Tab Controlling
        self.Pumpframe = GHMonitor.LabelFrame(TabControl, text="Water Pump Setting",height=455,width=800)
        self.Pumpframe.place(x=10, y=5)
        self.PScheframe = GHMonitor.LabelFrame(self.Pumpframe, text="",height=400,width=300)
        self.PScheframe.place(x=480, y=10)
        self.PAframe = GHMonitor.LabelFrame(self.Pumpframe, text="",height=400,width=450)
        self.PAframe.place(x=10, y=10)
        
        #watering System settings
        GHMonitor.Label(self.PScheframe, text="Watering Schedule : ", font = ("Times New Roman",14,"bold")).place(x=10,y=10)
        GHMonitor.Label(self.PScheframe, text="1st Time\t\t: ", font = ("Times New Roman",12)).place(x=10,y=60)
        GHMonitor.Label(self.PScheframe, text="2nd Time\t\t: ", font = ("Times New Roman",12)).place(x=10,y=90)
        GHMonitor.Label(self.PScheframe, text="3rd Time\t\t: ", font = ("Times New Roman",12)).place(x=10,y=120)
        
        self.txtFTime = widget.Entry(self.PScheframe,width = 12)
        self.txtFTime.place(x=160,y=60)
        self.txtSTime = widget.Entry(self.PScheframe,width = 12)
        self.txtSTime.place(x=160,y=90)
        self.txtTTime = widget.Entry(self.PScheframe,width = 12)
        self.txtTTime.place(x=160,y=120)
        
        self.btnsetSche = GHMonitor.Button(self.PScheframe, text="Set", height = 1, width = 10,
                                        font = ("Times New Roman",11,"bold"),command = self.SetWateringSchedule)
        self.btnsetSche.place(x=160,y=160)
        GHMonitor.Label(self.PScheframe, text="Current Schedule : ", font = ("Times New Roman",14,"bold")).place(x=10,y=240)
        self.Sone = GHMonitor.Label(self.PScheframe, text="1st Time    :",font = ("Times New Roman",12))
        self.Sone.place(x=20,y=290)
        self.Stwo = GHMonitor.Label(self.PScheframe, text="2nd Time    :",font = ("Times New Roman",12))
        self.Stwo.place(x=20,y=320)
        self.Sthree = GHMonitor.Label(self.PScheframe, text="3rd Time    :",font = ("Times New Roman",12))
        self.Sthree.place(x=20,y=350)
        
        GHMonitor.Label(self.PAframe, text="Water Amount setting : ", font = ("Times New Roman",12,"bold")).place(x=20,y=10)
        GHMonitor.Label(self.PAframe, text="pump powering time (ms)\t:", font = ("Times New Roman",12)).place(x=40,y=50)
        GHMonitor.Label(self.PAframe, text="Moisture Content\t\t:", font = ("Times New Roman",12)).place(x=40,y=80)
        self.txtPPT = widget.Entry(self.PAframe,width = 12)
        self.txtPPT.place(x=250,y=50)
        self.txtMC = widget.Entry(self.PAframe,width = 12)
        self.txtMC.place(x=250,y=80)
        
        self.btnsetA = GHMonitor.Button(self.PAframe, text="Set", height = 1, width = 10,
                                        font = ("Times New Roman",11,"bold"),command = self.SetPOntime)
        self.btnsetA.place(x=250,y=120)
        GHMonitor.Label(self.PAframe, text="Current Water Amount setting : ", font = ("Times New Roman",12,"bold")).place(x=20,y=200)
        self.CPpower = GHMonitor.Label(self.PAframe, text="pump powering time (ms)\t:", font = ("Times New Roman",12))
        self.CPpower.place(x=40,y=230)
        self.PMoisture = GHMonitor.Label(self.PAframe, text="Moisture Content\t\t:", font = ("Times New Roman",12))
        self.PMoisture.place(x=40,y=260)

        #moisture Sensor testing
        self.TMoisture = GHMonitor.LabelFrame(TabControl, text="",height=250,width=980)
        self.TMoisture.place(x=820, y=15)
        GHMonitor.Label(self.TMoisture, text="Moisture Sensor Testing : ", font = ("Times New Roman",14,"bold")).place(x=20,y=10)
        self.MAnalog = GHMonitor.Label(self.TMoisture, text="Sensor Analog Read\t:\t", font = ("Times New Roman",12))
        self.MAnalog.place(x=40,y=70)
        self.MMapped = GHMonitor.Label(self.TMoisture, text="Sensor Voltage Value\t:\t", font = ("Times New Roman",12))
        self.MMapped.place(x=40,y=100)
        self.MMoisture = GHMonitor.Label(self.TMoisture, text="Moisture Content\t\t:\t", font = ("Times New Roman",12))
        self.MMoisture.place(x=40,y=130)
        GHMonitor.Label(self.TMoisture, text="Sensor Message\t:", font = ("Times New Roman",12,"bold")).place(x=350,y=70)
        self.MError = GHMonitor.Label(self.TMoisture, text="This is Error Message From a Moisture Sensor", font = ("Times New Roman",12))
        self.MError.place(x=520,y=70)
        self.Mtest = GHMonitor.Button(self.TMoisture, text="Test", height = 1, width = 10,
                                        font = ("Times New Roman",11,"bold"),command=self.MoistureSensorTest)
        self.Mtest.place(x=200,y=170)
        
        #Light Sensor testing
        self.TLight = GHMonitor.LabelFrame(TabControl, text="",height=200,width=980)
        self.TLight.place(x=820, y=280)
        GHMonitor.Label(self.TLight, text="Light Sensor Testing : ", font = ("Times New Roman",14,"bold")).place(x=20,y=10)
        self.LLight = GHMonitor.Label(self.TLight, text="Light Intensity\t:", font = ("Times New Roman",12))
        self.LLight.place(x=40,y=80)
        GHMonitor.Label(self.TLight, text="Sensor Message\t:", font = ("Times New Roman",12,"bold")).place(x=350,y=80)
        self.LError = GHMonitor.Label(self.TLight, text="This is Error Message From a Moisture Sensor", font = ("Times New Roman",12))
        self.LError.place(x=520,y=80)
        self.Ltest = GHMonitor.Button(self.TLight, text="Test", height = 1, width = 10,
                                        font = ("Times New Roman",11,"bold"),command=self.LightSensorTest)
        self.Ltest.place(x=200,y=120)
        
        #Temperature & Humidity Sensor Testing
        self.TTemHum = GHMonitor.LabelFrame(TabControl, text="",height=250,width=980)
        self.TTemHum.place(x=820, y=500)
        GHMonitor.Label(self.TTemHum, text="Temperature & Humidity  Sensor Testing : ", font = ("Times New Roman",14,"bold")).place(x=20,y=10)
        self.TTem = GHMonitor.Label(self.TTemHum, text="Temperature\t:", font = ("Times New Roman",12))
        self.TTem.place(x=40,y=80)
        self.THum = GHMonitor.Label(self.TTemHum, text="Humidity\t\t:", font = ("Times New Roman",12))
        self.THum.place(x=40,y=110)
        self.THHeatI = GHMonitor.Label(self.TTemHum, text="Heat Index\t:", font = ("Times New Roman",12))
        self.THHeatI.place(x=40,y=140)
        GHMonitor.Label(self.TTemHum, text="Sensor Message\t:", font = ("Times New Roman",12,"bold")).place(x=350,y=80)
        self.THError = GHMonitor.Label(self.TTemHum, text="This is Error Message From a Moisture Sensor", font = ("Times New Roman",12))
        self.THError.place(x=520,y=80)
        self.THtest = GHMonitor.Button(self.TTemHum, text="Test", height = 1, width = 10,
                                        font = ("Times New Roman",11,"bold"),command=self.TemHumSensorTest)
        self.THtest.place(x=200,y=170)
        
        #Fan and Pump Testing
        self.TFP = GHMonitor.LabelFrame(TabControl, text="",height=150,width=980)
        self.TFP.place(x=820, y=770)
        GHMonitor.Label(self.TFP, text="Pump Testing\t: ", font = ("Times New Roman",14)).place(x=20,y=30)
        GHMonitor.Label(self.TFP, text="Fan Testing\t: ", font = ("Times New Roman",14)).place(x=20,y=90)
        GHMonitor.Label(self.TFP, text="Pump State\s: ", font = ("Times New Roman",14)).place(x=570,y=30)
        GHMonitor.Label(self.TFP, text="Fan State\s\s: ", font = ("Times New Roman",14)).place(x=570,y=90)
        self.TPOnbtn = GHMonitor.Button(self.TFP, text="Pump On", height = 1, width = 10,
                                        font = ("Times New Roman",11,"bold"),command=self.PumpON)
        self.TPOnbtn.place(x=250,y=30)
        self.TPOffbtn = GHMonitor.Button(self.TFP, text="Pump Off", height = 1, width = 10,
                                        font = ("Times New Roman",11,"bold"), command = self.PumpOff)
        self.TPOffbtn.place(x=400,y=30)
        self.PumpState = GHMonitor.Canvas(self.TFP, width=150, height=30,bg='light green')
        self.PumpState.place(x=700,y=30)
        
        self.TFOnbtn = GHMonitor.Button(self.TFP, text="Fan On", height = 1, width = 10,
                                        font = ("Times New Roman",11,"bold"), command =self.FanOn)
        self.TFOnbtn.place(x=250,y=90)
        self.TFOffbtn = GHMonitor.Button(self.TFP, text="Fan Off", height = 1, width = 10,
                                        font = ("Times New Roman",11,"bold"), command=self.FanOff)
        self.TFOffbtn.place(x=400,y=90)
        self.FanState = GHMonitor.Canvas(self.TFP, width=150, height=30,bg='light green')
        self.FanState.place(x=700,y=90)
        
        #Image Testing
        self.TestImage = GHMonitor.LabelFrame(TabControl, text="Camera Testing",height=455,width=800)
        self.TestImage.place(x=10, y=470)
        self.TestImg = GHMonitor.Canvas(self.TestImage, width=300, height=400,bg='green')
        self.TestImg.place(x=10,y=10)
        self.ImgCapture= GHMonitor.Button(self.TestImage, text="Test Image Capture", height = 1, width = 15,
                                        font = ("Times New Roman",11,"bold"), command=self.ImageTest)
        self.ImgCapture.place(x=350,y=10)
        GHMonitor.Label(self.TestImage, text="Image Parameters     :", font = ("Times New Roman",12,"bold")).place(x=350,y=60)
        self.ImgLength = GHMonitor.Label(self.TestImage, text= "Pixel Length  :", font = ("Times New Roman",12))
        self.ImgLength.place(x=360,y=100)
        self.ImgWidth = GHMonitor.Label(self.TestImage, text=  "Pixel Width   :", font = ("Times New Roman",12))
        self.ImgWidth.place(x=360,y=130)
        self.ImgDensity = GHMonitor.Label(self.TestImage, text="Pixel Density :", font = ("Times New Roman",12))
        self.ImgDensity.place(x=360,y=160)
        
        GHMonitor.Label(self.TestImage, text="Reference Parameters     :", font = ("Times New Roman",12,"bold")).place(x=350,y=200)
        self.refLength = GHMonitor.Label(self.TestImage, text= "Plant Height (Pixel)\t: \t\tRef Height  : ", font = ("Times New Roman",12))
        self.refLength.place(x=360,y=240)
        self.refWidth = GHMonitor.Label(self.TestImage, text=  "Plant Height (Pixel)\t: \t\tRef Width  : ", font = ("Times New Roman",12))
        self.refWidth.place(x=360,y=270)

        GHMonitor.Label(self.TestImage, text="Reference Actual Size     :", font = ("Times New Roman",12,"bold")).place(x=350,y=310)
        GHMonitor.Label(self.TestImage, text= "Actual Height\t:", font = ("Times New Roman",12)).place(x=360,y=350)
        GHMonitor.Label(self.TestImage, text=  "Actual Width\t:", font = ("Times New Roman",12)).place(x=360,y=380)
        self.txtImgHgt = widget.Entry(self.TestImage,width = 12)
        self.txtImgHgt.place(x=550,y=350)
        self.txtImgWdt = widget.Entry(self.TestImage,width = 12)
        self.txtImgWdt.place(x=550,y=380)
        
        self.THtest = GHMonitor.Button(self.TestImage, text="Set", height = 1, width = 10,font = ("Times New Roman",11,"bold"))
        self.THtest.place(x=680,y=350)
        self.THtest['command'] = self.SetRefActualSize
        
        self.refHW = GHMonitor.Label(self.TestImage, text=  "", font = ("Times New Roman",9,"bold"))
        self.refHW.place(x=450,y=405)
        
        #Tab Image
        self.LCurrentImg = GHMonitor.Canvas(TabImage, width=700, height=900,bg='green')
        self.LCurrentImg.place(x=10, y=10)
        self.LProgImg = GHMonitor.Canvas(TabImage, width=700, height=900,bg='green')
        self.LProgImg.place(x=730, y=10)
    def ImageTest(self):
        try:
            ref_lower = np.array([0,0,0]) 
            ref_upper = np.array([2,2,2])
            plant_lower = np.array([60, 60, 25]) 
            plant_upper = np.array([115, 255,255])
            img_frame  = cv.imread('/home/pi/Desktop/Green House/Plant Images/test5.jpg')
            
            hsv = cv.bilateralFilter(img_frame,9,75,75)
            #color fillering
            
            ref = cv.inRange(hsv, ref_lower, ref_upper)
            plant = cv.inRange(hsv, plant_lower, plant_upper)
            #Reference 
            canny_ref = cv.Canny(ref, 100, 200)
            _,contours_ref, hierarchy_ref = cv.findContours(canny_ref, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
            #Assigning to private variables
            x,y,RefWidth,RefHeight = cv.boundingRect(contours_ref[0])
            #draw  Reference Rectangle on Img_Frme
            cv.rectangle(img_frame,(x,y),(x+RefWidth,y+RefHeight),(255,0,0),4)
            #plant   
            dilatation_size = 15
            erosion_size = 14
            canny_plant = cv.Canny(plant, 10, 10)
            #plant dilatation
            element = cv.getStructuringElement(cv.MORPH_ELLIPSE, (2*dilatation_size + 1, 2*dilatation_size+1), (dilatation_size, dilatation_size))
            dilatation_dst = cv.dilate(canny_plant, element)
            #plant erosion#plant erosion
            element = cv.getStructuringElement(cv.MORPH_ELLIPSE, (2*erosion_size + 1, 2*erosion_size+1), (erosion_size, erosion_size))
            erosion_dst = cv.erode(dilatation_dst, element)
            _, contours_plant, hierarchy_plant = cv.findContours(erosion_dst, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
            #get largest contour
            area = 0
            index = 0
            for i in range(len(contours_plant)):
    #            cv.drawContours(self.img_frame, contours_plant, i, (0,255,255),2)
                if (area < cv.contourArea(contours_plant[i])):
                    area = cv.contourArea(contours_plant[i])
                    index=i
            #drawing  contours    
            cv.drawContours(img_frame, contours_plant, index, (0,0,255),2)
            x,y,Width,Height = cv.boundingRect(contours_plant[index])
            cv.rectangle(img_frame,(x,y),(x+Width,y+Height),(255,255,0),4)
            AreaPres = '{:.2f}'.format(((cv.contourArea(contours_plant[index]))/(Width*Height))*100)
            
            cv.imwrite('/home/pi/Desktop/Green House/Plant Images/PlantTest.jpg',img_frame)
            DImage = cv.imread('/home/pi/Desktop/Green House/Plant Images/PlantTest.jpg',cv.IMREAD_UNCHANGED)
            
            Dimentions = DImage.shape
            self.ImgLength['text']= "Pixel Height\t:\t"+ str(DImage.shape[0])
            self.ImgWidth['text']=  "Pixel Width\t:\t"+ str(DImage.shape[1])
            self.ImgDensity['text']="Pixel Density\t:\t"+str(DImage.shape[2])
            
            CData = TakeCData()
            self.refLength['text']= "Plant Height ("+str(Height)+")\t:  "+'{:.2f}'.format((Height/RefHeight)*(int(CData['ALength'])))+" mm\tRef Height  :  "+str(RefHeight)
            self.refWidth['text']=  "Plant Width ("+str(Width)+")\t:  "+'{:.2f}'.format((Width/RefWidth)*(int(CData['Awidth'])))+" mm\tRef Width  :  "+str(RefWidth)

            imageload(self)
        except Exception as e:
            messagebox.showerror("Error", str(e))
    def PumpON(self):
        try:
            sensorval,Received = readVal(Pump_On)
            SaveCData('PumpState',str(sensorval))
            self.TPOnbtn['state']=GHMonitor.DISABLED
            self.TPOffbtn['state']=GHMonitor.NORMAL
            self.PumpState['bg']='Green'
        except Exception as e:
            messagebox.showerror("Error", str(e))
        
    def PumpOff(self):
        try:
            sensorval,Received = readVal(Pump_Off)
            SaveCData('PumpState',str(sensorval))
            self.TPOnbtn['state']=GHMonitor.NORMAL
            self.TPOffbtn['state']=GHMonitor.DISABLED
            self.PumpState['bg']='red'
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def FanOn(self):
        try:
            sensorval,Received = readVal(Fan_On)
            SaveCData('FanState',str(sensorval))
            self.TFOnbtn['state']=GHMonitor.DISABLED
            self.TFOffbtn['state']=GHMonitor.NORMAL
            self.FanState['bg']='green'
        except Exception as e:
            messagebox.showerror("Error", str(e))
        
    def FanOff(self):
        try:
            sensorval,Received = readVal(Fan_Off)
            SaveCData('FanState',str(sensorval))
            self.TFOnbtn['state']=GHMonitor.NORMAL
            self.TFOffbtn['state']=GHMonitor.DISABLED
            self.FanState['bg']='red'
        except Exception as e:
            messagebox.showerror("Error", str(e))
        
    def MoistureSensorTest(self):
        try:
            sensorval,Received = readVal(moisture_index)
            self.MAnalog['text'] = "Sensor Analog Read\t:\t"+sensorval
            self.MMapped['text'] = "Sensor Voltage Value\t:\t"+'{:.2f}'.format((float(sensorval)/1024.0)*5.0)+" V"
            self.MMoisture['text'] = "Moisture Content\t\t:\t"+'{:.2f}'.format((float(sensorval)/1024)*100)+" %"
            self.MError['fg']='black'
            self.MError['text'] = "Moisture Sensor Is working properly, I2c Communiaction also \nworking without any error.\n\n Bytes Send From Arduino are :\n"+ str(Received)
        except Exception as e:
            self.MAnalog['text'] = "Sensor Analog Read\t:\t"
            self.MMapped['text'] = "Sensor Voltage Value\t:\t"
            self.MMoisture['text'] = "Moisture Content\t\t:\t"
            self.MError['fg']='red'
            self.MError['text'] = "I2c Communication is Terminated.\n\n Error Message : "+str(e)
        
    def LightSensorTest(self):
        try:
            sensorval,Received = readVal(Light_Index)
            self.LLight['text'] = "Light Intensity\t:\t"+sensorval +" lux"
            self.LError['fg']='black'
            self.LError['text'] = "Light Sensor Is working properly, I2c Communiaction also \nworking without any error. \n\n Bytes Send From Arduino Are : \n"+str(Received)
        except Exception as e:
            self.LLight['text'] = "Light Intensity\t:"
            self.LError['fg']='red'
            self.LError['text'] = "I2c Communication is Terminated.\n\n Error Message : "+str(e)
            
    def TemHumSensorTest(self):
        try:
            tem,tReceived = readVal(Temperature_Index)
            hum,hReceived = readVal(Humidity_Index)
            HeatI,iReceived = readVal(Heat_Index)
            self.TTem['text'] = "Temperature\t:\t"+tem+" Celcius"
            self.THum['text'] = "Humidity\t\t:\t"+hum+" MC%"
            self.THHeatI['text'] = "Heat Index\t:\t"+HeatI
            self.THError['fg']='black'
            self.THError['text'] = "DHT Temperature & Humidity Sensor is working properly,\n I2c Communiaction also working without any error.\n\n Bytes Send From Arduino Are :\nTemperature : "+str(tReceived)+"\nHumidity : "+str(hReceived)+"\nHeat Index : "+str(iReceived)
        except Exception as e:
            self.TTem['text'] = "Temperature\t:\t"
            self.THum['text'] = "Humidity\t\t:\t"
            self.THHeatI['text'] = "Heat Index\t:\t"
            self.THError['fg']='red'
            self.THError['text'] = "I2c Communication is Terminated.\n\n Error Message : "+str(e)
    def SetWateringSchedule(self):
        if(CheckTxt(self.txtFTime.get(),0) and CheckTxt(self.txtSTime.get(),0) and CheckTxt(self.txtTTime.get(),0)):
            SaveCData('FTime',self.txtFTime.get())
            SaveCData('STime',self.txtSTime.get())
            SaveCData('TTime',self.txtTTime.get())
            messagebox.showinfo("Green House Monitor Setting Info", "The watering Schedule of the Plant was Changed as : \nFirst Time : "+self.txtFTime.get()+"\nSecond Time : "
                                +self.txtSTime.get()+"\nThird Time :"+self.txtTTime.get())
            self.ValuesUpdate()
        else:
            messagebox.showerror("Error", "Invalid Time Format, Valid Time Format is (00:00)")
        tem = GHMonitor.StringVar()
        self.txtFTime['textvariable'] = tem
        self.txtSTime['textvariable'] = tem
        self.txtTTime['textvariable'] = tem
        tem.set('')
        
    def SetPOntime(self):
        if(CheckTxt(self.txtPPT.get(),1) and CheckTxt(self.txtMC.get(),1)):
            SaveCData('PPTime',self.txtPPT.get())
            SaveCData('Moisture',self.txtMC.get())
            messagebox.showinfo("Green House Monitor Pump Setting Info", "The Water Pump Settings was Changed as : \nPump Powering Time : "+self.txtPPT.get()+"\nMoisture : "
                                +self.txtMC.get())
            self.ValuesUpdate()
        else:
           messagebox.showerror("Error", "Invalid Setting Time Or Moisture Persentage..")
        tem = GHMonitor.StringVar()
        self.txtPPT['textvariable'] = tem
        self.txtMC['textvariable'] = tem
        tem.set('')
        
    def SetRefActualSize(self):
        if(CheckTxt(self.txtImgHgt.get(),1) and CheckTxt(self.txtImgWdt.get(),1)):
            SaveCData('ALength',self.txtImgHgt.get())
            SaveCData('Awidth',self.txtImgWdt.get())
            messagebox.showinfo("Green House Monitor Reference Size Setting Info", "The Actual Reference Size was Changed as :\nActual Height : "+self.txtImgHgt.get()
                                +"\nActual Width : "+self.txtImgWdt.get())
            self.ValuesUpdate()
        else:
            messagebox.showerror("Error", "Invalid Actual Reference Length Or Width ")
        tem = GHMonitor.StringVar()
        self.txtImgHgt['textvariable'] = tem
        self.txtImgWdt['textvariable'] = tem
        tem.set('')
    
        
    def ImageUpdate(self,Arr):
        
        self.CurrentImg.create_image(152, 200, image = Arr[0])
        self.ProgImg.create_image(152, 200, image = Arr[1])
        self.LCurrentImg.create_image(352, 452, image = Arr[2])
        self.LProgImg.create_image(352, 452, image = Arr[3])
        self.TestImg.create_image(151, 201, image = Arr[4])
            
    def ValuesUpdate(self):
        filepath = "/home/pi/Desktop/Green House/DataMonitor.csv"
        ComValues = np.array(['ID','DateTime','Height','Width','AreaPresentage','RefHeight','RefWidth','ImageUri','Light','Temperature','Humidity','Moisture'])
        LastRow = []
        with open(filepath,'r') as csvfile:
                readData = reader.DictReader(csvfile)
                for row in readData:
                    LastRow.clear()
                    for i in range ((len(ComValues))):
                        LastRow.append(row[ComValues[i]])
        csvfile.close()
        self.lblPlantHeight["text"] = LastRow[2]
        self.lblPlantWidth["text"] = LastRow[3]
        self.lblPlantAreaPres["text"] = LastRow[4]
        self.lblRefHeight["text"] = LastRow[5]
        self.lblReftWidth["text"] = LastRow[6]
        self.lblRefArea["text"] = LastRow[7]
        self.gaugeLight.set_value(float(LastRow[8]))
        self.gaugeTem.set_value(float(LastRow[9]))
        self.gaugeHum.set_value(float(LastRow[10]))
        self.gaugeMoi.set_value(float(LastRow[11]))
        self.CID = LastRow[0]
        self.Id['text'] = 'Current Data ID : '+LastRow[0]
        self.Date['text'] = 'Date & Time : '+LastRow[1]
        imgArr = getImages(LastRow[0])
        self.ImageUpdate(imgArr)
        
        #filling Current Controlling Values
        CData = TakeCData()
        self.Sone['text'] = "1st Time\t\t:\t"+CData['FTime']
        self.Stwo["text"] = "2nd Time\t\t:\t"+CData['STime']
        self.Sthree["text"] = "3rd Time\t\t:\t"+CData['TTime']
        self.CPpower["text"] = "pump powering time\t:\t"+CData['PPTime']+" ms"
        self.PMoisture["text"] = "Moisture Content\t\t:\t"+CData['Moisture']+ " %"
        self.refHW["text"] = "Current Width : "+CData['Awidth']+" mm,  Height : "+CData['ALength']+" mm "
        pState = CData['PumpState']
        fState = CData['FanState']
        if(pState=='1'):
            self.TPOnbtn['state']=GHMonitor.DISABLED
            self.TPOffbtn['state']=GHMonitor.NORMAL
            self.PumpState['bg']='green'
        elif(pState=='0'):
            self.TPOnbtn['state']=GHMonitor.NORMAL
            self.TPOffbtn['state']=GHMonitor.DISABLED
            self.PumpState['bg']='red'
        if(fState=='1'):
            self.TFOnbtn['state']=GHMonitor.DISABLED
            self.TFOffbtn['state']=GHMonitor.NORMAL
            self.FanState['bg']='green'
        elif(fState=='0'):
            self.TFOnbtn['state']=GHMonitor.NORMAL
            self.TFOffbtn['state']=GHMonitor.DISABLED
            self.FanState['bg']='red'
            
        return LastRow
        
    def XCombo(self,event):
        val = self.XaxisCombo.get()
        dataArr = self.ValuesUpdate()
        newArr=[]
        for i in range (len(self.ComValues)):
            if self.ComValues[i] == val:
                imgIndex = i
            else:
                newArr.append(self.ComValues[i])
        self.CXIcon.itemconfig(self.XiconSupport,image=self.IconArr[imgIndex])
        self.YaxisCombo['values'] = newArr
        self.lblCurrentX['text'] = str(val)
        self.lblCurrentXVal['text'] = dataArr[imgIndex] +' '+self.Units[imgIndex]
        self.YaxisCombo['state'] = GHMonitor.NORMAL
        self.XaxisCombo['state'] = GHMonitor.DISABLED
        
    def YCombo(self,event):
        Index = self.ComValues.index(self.YaxisCombo.get())
        dataArr = self.ValuesUpdate()
        self.lblCurrentY['text'] = self.YaxisCombo.get()
        self.CYIcon.itemconfig(self.YiconSupport,image=self.IconArr[Index])
        self.YaxisCombo['state'] = GHMonitor.DISABLED
        self.btnPlot['state'] =  GHMonitor.NORMAL
        self.lblCurrentYVal['text'] = dataArr[Index] + ' '+self.Units[Index]
        
    def PlotClick(self):
        self.YaxisCombo['values'] = self.ComValues
        self.XaxisCombo['values'] = self.ComValues
        self.XaxisCombo['state'] = GHMonitor.NORMAL
        self.GraphPlotting(self.XaxisCombo.get(),self.YaxisCombo.get(),
                           self.Units[self.ComValues.index(self.XaxisCombo.get())],
                           self.Units[self.ComValues.index(self.YaxisCombo.get())])
        
        
    def GraphPlotting(self,XTitle,YTitle,XU,YU):
            filepath = "/home/pi/Desktop/Green House/DataMonitor.csv"
            XData = []
            YData = []
            with open(filepath,'r') as csvfile:
                readData = reader.DictReader(csvfile)
                for row in readData:
                    XData.append(row[XTitle])
                    YData.append(row[YTitle])
            csvfile.close()
            self.graph.clear()
            self.graph.set_title('The Graph Of ' + YTitle+self.LabelAdjust(YU) +' & ' + XTitle+self.LabelAdjust(XU))
            self.graph.set_xlabel(XTitle+self.LabelAdjust(XU))
            self.graph.set_ylabel(YTitle+self.LabelAdjust(YU))
            self.graph.plot(XData,YData,c='r')
            self.graph.fill(XData,YData,c='r', alpha =0.3)
            self.canvas = FigureCanvasTkAgg(self.fig, self.Graphframe)
            self.canvas.get_tk_widget().place(x=20, y=25,height=420,width=1100)
            
    def LabelAdjust(self,unit):
        if(unit==''): return unit
        else:         return ' ('+unit+')'



    
window = GHMonitor.Tk()
app = Application(window)
Imgs = getImages(app.CID)
app.ImageUpdate(Imgs)
app.mainloop()

