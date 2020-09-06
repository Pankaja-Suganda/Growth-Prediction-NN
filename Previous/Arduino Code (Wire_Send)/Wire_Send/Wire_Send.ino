#include <Wire.h>
#include <Arduino.h>]
#include "DHT.h"

#define SLAVE_ADDRESS 0x12
#define TYPE DHT21  
#define TemHumPin 2
#define SoilMoisPin A0   
#define waterPumpPin 13
#define FanPin 11

DHT TemHum(TemHumPin, TYPE);
int flag_int_to_send_to_PI = 0;
int flag_int_received_from_PI = 0;
char WaterPumpState ='0';
char FanState ='0';
byte Iarr[5];
char arr[5];
void setup() {
     Wire.begin(SLAVE_ADDRESS);
     TemHum.begin();
     Wire.onReceive(receiveData);
     Wire.onRequest(sendData);
     Serial.begin(9600);
     flag_int_to_send_to_PI = 1;
     pinMode(waterPumpPin,OUTPUT);
     pinMode(FanPin,OUTPUT);
     digitalWrite(waterPumpPin,LOW);
     digitalWrite(FanPin,LOW);
}

void loop() {
  }

void receiveData(int byteCount) {
  flag_int_received_from_PI = Wire.read();
  Serial.println(flag_int_received_from_PI);
  TakeSensorData(flag_int_received_from_PI);
}

void byteArr(char charArr[]){
  for(int i =0;i<5;i++){
    Iarr[i]=charArr[i];
    }
  }
  
void TakeSensorData(int index){
  String SensorData;
  switch(index){
    case 1:
      SensorData = String(TemHum.readTemperature());
      Serial.println("readTemperature");
      break;
    case 2:
      SensorData = String(TemHum.readHumidity());
      Serial.println("readHumidity");
      break;
    case 3:
      SensorData = String(TemHum.readTemperature());
      Serial.println("Wcater Pump On");
      break;
    case 4:
      SensorData = String(TemHum.computeHeatIndex(TemHum.readTemperature(), TemHum.readHumidity(), false));
      break;
    case 5:
      float  Moisture= analogRead(SoilMoisPin);
      Moisture = map(Moisture,550,0,0,100);
      SensorData = String(Moisture);
      break;
  }
  Serial.println(SensorData);
  SensorData.toCharArray(arr, 6);
  }

void PIDWatering(){
    Serial.println("watering PID ");
  }
  
void sendData() {
  delay(200);
  Serial.println(arr);
  if(0<flag_int_received_from_PI && flag_int_received_from_PI<=5){
    for (int i=0; i<5; i++){
          Wire.write(arr[i]);
        }
  }
  else if(flag_int_received_from_PI==6){
      Wire.write('1');
      digitalWrite(waterPumpPin,HIGH);
    }
  else if(flag_int_received_from_PI==7){
      Wire.write('0');
      digitalWrite(waterPumpPin,LOW);
    }
  else if(flag_int_received_from_PI==8){
      Wire.write('1');
      digitalWrite(FanPin,HIGH);
    }
  else if(flag_int_received_from_PI==9){
      Wire.write('0');
      digitalWrite(FanPin,LOW);
    }
  else if(flag_int_received_from_PI<=10 && flag_int_received_from_PI>=110){
      PIDWatering();
    }
  flag_int_received_from_PI = 0;
}
