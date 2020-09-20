#!/usr/bin/env python
#przetlumaczyc komentarze, zmienic struktura <-----------------------------------------------------------------
from datetime import datetime
import serial
import struct
import numpy as np
import copy
import time


class serialPlot:
    #Klasa serialPlot. Do obslugi komunikacji
    def __init__(self, serialPort='COM9', serialBaud=38400, dataNumBytes=2, numVariables=1):
        self.port = serialPort      #definicja portu
        self.baud = serialBaud      #definicja predkosci transmisji
        self.dataNumBytes = dataNumBytes
        self.numVariables = numVariables
        self.rawData = bytearray(numVariables * dataNumBytes)
        self.dataType = None
        if dataNumBytes == 2:
            self.dataType = 'h'     # 2 byte integer
        elif dataNumBytes == 4:
            self.dataType = 'f'     # 4 byte float
        self.dataBlock = []
        self.data = []
        for i in range(numVariables):
            self.data.append([])

        print('Próba nawiązania połączenia z: ' + str(serialPort) + ' przy ' + str(serialBaud) + ' BAUD.')
        try:
            self.serialConnection = serial.Serial(serialPort, serialBaud, timeout=4)
            print('Połączono z ' + str(serialPort) + ' przy ' + str(serialBaud) + ' BAUD.')
        except:
            print("Nieudane połączenie " + str(serialPort) + ' przy ' + str(serialBaud) + ' BAUD.')

    def getSerialData(self, t):
        #odbieranie danych, t - czas probkowania
        self.serialConnection.reset_input_buffer()
        startTime = datetime.now()

        while (datetime.now() - startTime).total_seconds() < t:
            self.serialConnection.readinto(self.rawData)    #pobranie danych z portu
            self.dataBlock.append(self.rawData[:])          #dodanie danych

        print("Rejestracja danych przez %d sek"%t)
        self.close()
        print("Przetwarzanie danych")

        for i in range(len(self.dataBlock)):
            for j in range(self.numVariables):
                byteData = self.dataBlock[i][(j * self.dataNumBytes):((j + 1) * self.dataNumBytes)]
                value, = struct.unpack(self.dataType, byteData)
                self.data[j].append(copy.copy(value))
        print("Eksport danych...")
        csvData = np.flip(np.array(self.data), 1).transpose()
        np.savetxt('magnetometr.csv', csvData, delimiter=',', fmt='%i')
        print("Zakończono akwizycję danych. Plik: magnetometr.csv")

    def close(self):
        self.serialConnection.close()
        print('Rozłączono...')


def main():
    portName = 'COM9'
    baudRate = 115200
    dataNumBytes = 2        # liczba bajtów na jedną zmienną
    numVariables = 9        # liczba odbieranych danych
    s = serialPlot(portName, baudRate, dataNumBytes, numVariables)   # inicjacja obiektu klasy serialPlot
    time.sleep(2)
    s.getSerialData(60)


if __name__ == '__main__':
    main()