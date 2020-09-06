# -*- coding: utf-8 -*-
"""
Created on Thu Feb 13 21:28:55 2020

@author: Pankaja Suganda
"""

#from firebase import firebase
#import cv2 as cv
##import numpy as np
#from matplotlib import pyplot as plt
##import csv as csv_
#from DMonitor import Monitoring_Data as Monitor


#
#firebase = firebase.FirebaseApplication('https://automated-green-house-fae2e.firebaseio.com/', None)
#data =  { 'Area': data_.Area,
#          'Date':data_.Date,
#          'Height':data_.Height,
#          'Humidity':data_.Humidity,
#          'ImageUri':data_.ImageUri,
#          'Light':data_.Light,
#          'Moisture':data_.Moisture,
#          'RefArea':data_.RefArea,
#          'RefHeight':data_.RefHeight,
#          'RefWidth':data_.RefWidth,
#          'Temperature':data_.Temperature,
#          'Width':data_.Width,
#          }

#result = firebase.post('https://automated-green-house-fae2e.firebaseio.com//Monitoring/',data)



#plt.subplot(221),plt.imshow(img),plt.title('Input')
#
#test = Monitor('fifth')
#test1 = Monitor('second')
#test.WriteData()
#test.saveImage()
#print (test.DataArr)
#print (test.AreaPres)


#test1.WriteData()

#plt.subplot(121),plt.imshow(test.CurrentImg),plt.title('Raw')
#plt.subplot(122),plt.imshow(test.img_frame),plt.title('Processed')



#
#config = {
#    "apiKey":"AIzaSyD8mXYzH4C9_Ar57VfS0Hdi9JontdYFF-g", #get api key from firebase
#    "authDomain":"", #firebase app auth url 
#    "databaseURL": "https://automated-green-house-fae2e.firebaseio.com/", #add yout db url from firebase where your data is gonna store 
#    "storageBucket": "" #storage bucket url from firebase storage 
#}
#
#firebase = pyrebase.initialize_app(config)
#db = firebase.database()
#storage = firebase.storage()
#
#file=os.path.basename('image1.jpg') #image1.jpg is local storage image
#storage.child(storage_path+"image1.jpg").put(file)
#image_url= storage.child(storage_path+"image1.jpg").get_url(1)
#print(image_url)
#data = {"created_date_time":str(datetime.datetime.now()), "image_url":image_url}


#from google.cloud import storage
#from firebase import firebase
#import firebase_admin
#from firebase_admin import credentials
#import pyrebase
#cred = credentials.Certificate("C:/Users/Pankaja Suganda/Desktop/automated-green-house-fae2e-firebase-adminsdk-ckk2l-92a29a7479.json")
#firebase_admin.initialize_app(cred)
#firebase = firebase.FirebaseApplication('https://automated-green-house-fae2e.firebaseio.com/')
#client = storage.Client()
#bucket = client.bucket('automated-green-house-fae2e.firebaseio.com')
#imageBlob = bucket.blob("/")
#imagePaths = "C:/Users/Pankaja Suganda/Test/Gree House/IMG_20191228_150827_2.jpg"
##imageBlob.upload_from_filename(imagePaths)
#
#config = { "apiKey": "AIzaSyD8mXYzH4C9_Ar57VfS0Hdi9JontdYFF-g",
#           "authDomain": "automated-green-house-fae2e.firebaseio.com",
#           "databseURL": "https://automated-green-house-fae2e.firebaseio.com",
#           "projectId": "automated-green-house-fae2e",
#           "storageBucket": "automated-green-house-fae2e.firebaseio.com"}
#
#ffirebase = pyrebase.initialize_app(config)
#db = firebase.database()
#storage_ = firebase.storage()
#storage.child("/image1.jpg").put(imagePaths)
#image_url= storage_.child("/image1.jpg").get_url(1)
#print(image_url)


#!/usr/bin/env python3
import tkinter as tk
import gaugelib


win = tk.Tk()
#a5 = tk.PhotoImage(file="test1.jpg")
#win.tk.call('wm', 'iconphoto', win._w, a5)
win.title("Ardiotech Raspberry Pi Version 2.0")
#win.geometry("800x400+0+0")
win.resizable(width=True, height=True)
win.configure(bg='white')

gaugeTem = gaugelib.DrawGauge2(
    win,
    max_value=100,
    min_value=0,
    size=300,
    bg_col='red',
    unit = "°C",bg_sel = 2)
gaugeTem.pack(side=tk.LEFT)
gaugeTem.set_value(50)

from PIL import ImageTk, Image


canvas_width = 300
canvas_height = 300
#canvas = tk.Canvas(win, 
#           width=canvas_width, 
#           height=canvas_height)
#canvas.pack(side=tk.LEFT)

#image = Image.open('test5.jpg')
#image = image.resize((canvas_width, canvas_height), Image.ANTIALIAS)
#
#png = ImageTk.PhotoImage(image) # Just an example 
#canvas.create_image(0, 0, image = png, anchor = "nw")

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

x=np.array ([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
v= np.array ([16,16.31925,17.6394,16.003,17.2861,17.3131,19.1259,18.9694,22.0003,22.81226])
p= np.array ([16.23697,     17.31653,     17.22094,     17.68631,     17.73641 ,    18.6368,
            19.32125,     19.31756 ,    21.20247  ,   22.41444   ,  22.11718  ,   22.12453])

#plt.plot(p, range(2 +max(x)),color='red')

plt.suptitle ("Estimation Grid", fontsize=16)
plt.ylabel("Y", fontsize=14)
plt.xlabel("X", fontsize=14)

f = Figure(figsize=(5,5), dpi=100)
a = f.add_subplot(111)
a.plot([1,2,3,4,5,6,7,8],[5,6,1,3,8,9,3,5])
f.legend('x')

canvas = FigureCanvasTkAgg(f, win)
canvas.get_tk_widget().pack()



#gaugeHum = gaugelib.DrawGauge2(
#    win,
#    max_value=100,
#    min_value=0,
#    size=300,
#    bg_col='Blue',
#    unit = "%MC",bg_sel = 2)
#gaugeHum.pack(side=tk.LEFT)
#gaugeHum.set_value(60)
#
#gaugeMoi = gaugelib.DrawGauge2(
#    win,
#    max_value=100,
#    min_value=0,
#    size=300,
#    bg_col='Green',
#    unit = "%MC",bg_sel = 2)
#gaugeMoi.pack(side=tk.LEFT)
#gaugeMoi.set_value(60)
#
#gaugeLight = gaugelib.DrawGauge2(
#    win,
#    max_value=100,
#    min_value=0,
#    size=300,
#    bg_col='Yellow',
#    unit = "%MC",bg_sel = 2)
#gaugeLight.pack(side=tk.LEFT)
#gaugeLight.set_value(60)
#p2 = gaugelib.DrawGauge2(
#    win,
#    max_value=100.0,
#    min_value= 0.0,
#    size=200,
#    bg_col='black',
#    unit = "Humid %",bg_sel = 2)
#p2.pack(side=RIGHT)
#
#p3 = gaugelib.DrawGauge3(
#    win,
#    max_value=100.0,
#    min_value= 0.0,
#    size=200,
#    bg_col='black',
#    unit = "Humid %",bg_sel = 1)
#p3.pack()
#p4 = gaugelib.DrawGauge3(
#    win,
#    max_value=100.0,
#    min_value= 0.0,
#    size=200,
#    bg_col='black',
#    unit = "Humid %",bg_sel = 2)
#p4.pack()

#read_every_second()
tk.mainloop()















    