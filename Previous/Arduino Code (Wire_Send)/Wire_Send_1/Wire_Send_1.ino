#include <Wire.h>
#include <String.h>



double Temperature;
double Humidity;
int i;

byte SLAVE_ADRESS = 0x08;

char temp[10];
char humid[10];

String tmp;
 
char T_data[5];

int index = 0;

void SendData(){

      Humidity=100.4;
      Temperature=45.67;

  tmp = dtostrf(Temperature,5,2,temp);

for(i=0;i++;i<5){
  T_data[i] = tmp[i];
}
  Serial.println(Wire.read(SLAVE_ADRESS));
  Wire.write(T_data[index]);

  ++index;

  if(index >= 5){
    index=0;
  }

}





void setup() {
  

  Wire.begin(SLAVE_ADRESS);

  Wire.onRequest(SendData);

  Serial.begin(9600);



}

void loop() {



}
