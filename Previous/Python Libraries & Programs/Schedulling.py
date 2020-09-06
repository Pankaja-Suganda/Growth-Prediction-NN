# -*- coding: utf-8 -*-
"""
Created on Sun Mar  1 13:32:19 2020

@author: Pankaja Suganda
"""
import schedule
import time
from DMonitor import Monitoring_Data as Monitor

class schedules:
    def __init__(self):
        schedule.every().day.at("15:27").do(self.FetchingData)
        schedule.every().day.at("15:28").do(self.FetchingData)
        schedule.every().day.at("15:29").do(self.FetchingData)
        schedule.every().day.at("15:30").do(self.FetchingData)
        schedule.every().day.at("15:31").do(self.FetchingData)
        print ('created')
        
    def FetchingData(self):
        monitor = Monitor()
        print ("Take Data")

s = schedules()

while True:
    schedule.run_pending()
    print ('..')
    time.sleep(1)
