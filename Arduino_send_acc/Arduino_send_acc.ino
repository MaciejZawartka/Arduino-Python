//  Odczytywanie wartosci i wysylanie do PC
//  Maciej Zawartka

//MPU9250 - bilbioteka Border Flight Systems
#include "MPU9250.h"


// Zmienne
unsigned long czas_ostatni = 0;
long napetle = 5000;
MPU9250 IMU(Wire,0x68); //obiekt MPU9250 pod adresem 0x68
int status;
double d1, d2, d3;
double roll, pitch, yaw;

//Konfiguracja
void setup() {
  Serial.begin(38400);
  status = IMU.begin();
  if (status < 0){
    Serial.println("Niepolaczono z IMU");
    Serial.print("Status:   ");
    Serial.println(status);
    while(1) {} //pauza
    }

  //Konfiguaracja IMU
  IMU.setAccelRange(MPU9250::ACCEL_RANGE_4G);
  //IMU.setGyroRange(MPU9250::GYRO_RANGE_500DPS);
  IMU.setDlpfBandwidth(MPU9250::DLPF_BANDWIDTH_20HZ); //filtr dolnoprzeustowy, wbudowany
  IMU.setSrd(19);   //czestotliwosc wynikow (1000/(1+srd)) [Hz]
  czas_ostatni = micros();   // pomiar czasu
}
//Petla glowna
void loop() {
  if (micros() - czas_ostatni >= napetle){
    IMU.readSensor();
    d1 = IMU.getAccelX_mss(); //[ms]00
    d2 = IMU.getAccelY_mss();
    d3 = IMU.getAccelZ_mss();

    roll = (double)(atan2(d2, d3)) * 180 / 3.1415 ; // [stopnie]
    pitch =(double)(atan2(-d1, sqrt(d2*d2 + d3*d3))) * 180 / 3.1415 ;
    yaw = 0;
    sendmessage(&d1, &d2, &d3);
    //sendmessage(&roll, &pitch, &yaw);
    czas_ostatni = micros();
  }
}

void sendmessage(int* data1, int* data2, int* data3){
  byte* byteData1 = (byte*)(data1);
  byte* byteData2 = (byte*)(data2);
  byte* byteData3 = (byte*)(data3);
  byte buff[6] = {byteData1[0], byteData1[1],
                 byteData2[0], byteData2[1],
                 byteData3[0], byteData3[1]};
  Serial.write(buff, 6);
  }

void sendmessage(double* data1, double* data2, double* data3){
  byte* byteData1 = (byte*)(data1);
  byte* byteData2 = (byte*)(data2);
  byte* byteData3 = (byte*)(data3);
  byte buf[12] = {byteData1[0], byteData1[1], byteData1[2], byteData1[3],
                 byteData2[0], byteData2[1], byteData2[2], byteData2[3],
                 byteData3[0], byteData3[1], byteData3[2], byteData3[3]};
  Serial.write(buf, 12);
}
