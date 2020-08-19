//  Odczytywanie wartosci i wysylanie do PC
//  Maciej Zawartka


// Zmienne
unsigned long czas_ostatni = 0;
long napetle = 5000;
int d1, d2, d3;
//------------------------
void setup() {
  Serial.begin(38400);
  czas_ostatni = micros();   // pomiar czasu
}
//------------------------
void loop() {
  if (micros() - czas_ostatni >= napetle){
    d1 = analogRead(A0);
    d2 = analogRead(A1);
    d3 = analogRead(A2);;
    sendmessage(&d1, &d2, &d3);
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
