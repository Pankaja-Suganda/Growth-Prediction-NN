
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 22 10:48:07 2020

@author: Pankaja Suganda
"""
import cv2 as cv
import numpy as np
import csv as csv_
import datetime as date
from picamera.array import PiRGBArray
from picamera import PiCamera
from smbus import SMBus
import time
import pyrebase

bus = SMBus(1)
slaveAddress = 0x12

Temperature_Index = 1
Humidity_Index = 2
Light_Index = 3
Heat_Index = 4
moisture_index = 5

def StringToBytes(val):
    retVal =""
    for c in val:
        if not (c==255) :
             retVal= retVal+(chr(c))
    return retVal


def readVal(index):
    bus.write_byte(slaveAddress,index)
    time.sleep(0.05)
    d = bus.read_i2c_block_data(slaveAddress,index,12)
    return StringToBytes(d)
    
class Monitoring_Data:
    def __init__(self):
        filepath = "/home/pi/Desktop/Green House/DataMonitor.csv"
        with open(filepath) as file:
            self.ID = sum(1 for line in file)
        file.close()
        self.ImageUri = None
#        self.RefArea
        today = date.datetime.now()
        self.DateTime = today.strftime("%Y/%m/%d_%H:%M")
        self.ImgProg()
        self.SensorData()
        self.DataAsArray()
        self.saveImage()
        self.WriteData()
        self.uploadImgToFirebase()
        
       
    def ImgProg(self):
        self.Takeimg()
        ref_lower = np.array([0,0,0]) 
        ref_upper = np.array([2,2,2])
        plant_lower = np.array([60, 60, 25]) 
        plant_upper = np.array([115, 255,255])
        self.Takeimg()
    
#         self.img_frame = self.CurrentImg
    
        hsv = cv.bilateralFilter(self.img_frame,9,75,75)
        #color fillering
#         hsv = self.img_frame
        
        ref = cv.inRange(hsv, ref_lower, ref_upper)
        plant = cv.inRange(hsv, plant_lower, plant_upper)
        #Reference 
        canny_ref = cv.Canny(ref, 100, 200)
        _,contours_ref, hierarchy_ref = cv.findContours(canny_ref, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        #Assigning to private variables
        x,y,self.RefWidth,self.RefHeight = cv.boundingRect(contours_ref[0])
        #draw  Reference Rectangle on Img_Frme
        cv.rectangle(self.img_frame,(x,y),(x+self.RefWidth,y+self.RefHeight),(255,0,0),4)
        #plant   
        dilatation_size = 15
        erosion_size = 14
        canny_plant = cv.Canny(plant, 10, 10)
        #plant dilatation
        element = cv.getStructuringElement(cv.MORPH_ELLIPSE, (2*dilatation_size + 1, 2*dilatation_size+1), (dilatation_size, dilatation_size))
        dilatation_dst = cv.dilate(canny_plant, element)
        #plant erosion
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
        cv.drawContours(self.img_frame, contours_plant, index, (0,0,255),2)
        x,y,self.Width,self.Height = cv.boundingRect(contours_plant[index])
        cv.rectangle(self.img_frame,(x,y),(x+self.Width,y+self.Height),(255,255,0),4)
        self.AreaPres = '{:.2f}'.format(((cv.contourArea(contours_plant[index]))/(self.Width*self.Height))*100)
        print('process Finished')
        
    def SensorData(self):
        self.Humidity = readVal(Humidity_Index)
        self.Temperature = readVal(Temperature_Index)
        self.Moisture = readVal(moisture_index)
        self.Light = readVal(Light_Index)
        
    def Takeimg(self):
        print ('Take img for Processing')
#         filepath = "/home/pi/Desktop/Green House/IMG_20191228_150801_1.jpg"
        filepath = "/home/pi/Desktop/Green House/test5.jpg"
#         filepath = "C:/Users/Pankaja Suganda/Test/Gree House/test5.jpg"
#         camera = PiCamera()
#         rawCapture = PiRGBArray(camera)
#         camera.start_preview()
#         time.sleep(5)
#         camera.capture(rawCapture,format="rgb")
#         image = rawCapture.array
#         camera.stop_preview()
        
        self.CurrentImg = cv.imread(filepath)
        self.img_frame = cv.imread(filepath)
#         cv.imwrite('/home/pi/Desktop/Green House/Plant Images/PPPPlant.jpg', image) 
    
    
    def DataAsArray(self):
        self.DataArr = np.array([self.ID,
                                self.DateTime,
                                self.Height,
                                self.Width,
                                self.AreaPres,
                                self.RefHeight,
                                self.RefWidth,
                                self.ImageUri,
                                self.Light,
                                self.Temperature,
                                self.Humidity,
                                self.Moisture])
        print (self.DataArr)
    def saveImage(self):
        cv.imwrite('/home/pi/Desktop/Green House/Plant Images/Plant_'+str(self.ID)+'.jpg', self.CurrentImg) 
        cv.imwrite('/home/pi/Desktop/Green House/Plant Images/Procssed_Plant_Image.jpg',self.img_frame) 
    
    def WriteData(self):
        filepath = "/home/pi/Desktop/Green House/DataMonitor.csv"
        fieldnames = ['ID','DateTime','Height','Width','AreaPresentage','RefHeight','RefWidth','ImageUri','Light','Temperature','Humidity','Moisture']
        with open(filepath,'a+',newline='') as myfile:
            writer = csv_.DictWriter(myfile,fieldnames)
#            writer.writeheader() ## Headers Write to the CSV
            writer.writerow({'ID': self.DataArr[0], 
                             'DateTime': self.DataArr[1],
                             'Height': self.DataArr[2], 
                             'Width': self.DataArr[3],
                             'AreaPresentage' : self.DataArr[4], 
                             'RefHeight': self.DataArr[5], 
                             'RefWidth': self.DataArr[6],
                             'ImageUri': self.DataArr[7], 
                             'Light': self.DataArr[8],
                             'Temperature': self.DataArr[9], 
                             'Humidity': self.DataArr[10], 
                             'Moisture': self.DataArr[11]})
        myfile.close()
    
    def uploadImgToFirebase(self):
        print ('firebase Uploading')
        config = {"apiKey":"AIzaSyD8mXYzH4C9_Ar57VfS0Hdi9JontdYFF-g",
                  "authDomain": "automated-green-house-fae2e.firebaseio.com",
                  "databaseURL": "https://automated-green-house-fae2e.firebaseio.com",
                  "projectId": "automated-green-house-fae2e",
                  "storageBucket": "automated-green-house-fae2e.appspot.com"}
        firebase = pyrebase.initialize_app(config)
        database = firebase.database()
        storage = firebase.storage()
        resultX = storage.child("Plant_"+str(self.ID)+".jpg").put("/home/pi/Desktop/Green House/Plant Images/Plant_"+str(self.ID)+".jpg")
        print (resultX['downloadTokens'])
        imageUrl = storage.child("Plant_"+str(self.ID)+".jpg").get_url(resultX['downloadTokens'])
        data = {'Area': self.DataArr[4],
                'Date': self.DataArr[1],
                'Height': self.DataArr[2],
                'Humidity': self.DataArr[10],
                'ImageUri': imageUrl,
                'Light': self.DataArr[8],
                'Moisture': self.DataArr[11],
                'RefArea': self.DataArr[0],
                'RefHeight': self.DataArr[5],
                'RefWidth': self.DataArr[6],
                'Temperature': self.DataArr[9],
                'Width':self.DataArr[3]}
        result = database.child("Monitoring").push(data)
        print (result)

# c = Monitoring_Data()
    
    
