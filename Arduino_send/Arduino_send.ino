//  Odczytywanie wartosci i wysylanie do PC
//  Maciej Zawartka


// Zmienne
unsigned long czas_ostatni = 0;
long napetle = 5000;

//------------------------
void setup() {
  Serial.begin(38400);
  czas_ostatni = micros();   // pomiar czasu
}
//------------------------
void loop() {
  if (micros() - czas_ostatni >= napetle){
    double val = (analogRead(0) - 512)/512.0;
    sendmessage(&val);
  }
}

void sendmessage(int* data){
  byte* byteData = (byte*)(data);
  Serial.write(byteData,2);
  }

void sendmessage(int* data){
  byte* byteData = (byte*)(data);
  Serial.write(byteData,4);
}
