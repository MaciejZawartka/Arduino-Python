#!/usr/bin/env python
#Nalezy ustawic numer portu COM
#Nalezy ustawic liczbe bitow na jeden punkt


from threading import Thread
import serial
import time
import collections
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import struct
import copy
import pandas as pd


class serialPlot:
    def __init__(self, serialPort='COM9', serialBaud=38400, plotLength=100, dataNumBytes=2, numPlots=1):
        #nawiazanie polaczenia przez port szeregowy
        self.port = serialPort
        self.baud = serialBaud
        self.plotMaxLength = plotLength
        self.dataNumBytes = dataNumBytes
        self.numPlots = numPlots
        self.rawData = bytearray(numPlots * dataNumBytes)
        self.dataType = None
        if dataNumBytes == 2:
            self.dataType = 'h'  # 2 byte - integer
        elif dataNumBytes == 4:
            self.dataType = 'f'  # 4 byte - float
        self.data = []
        for i in range(numPlots):  # zwraca macierz dla kazdego typu i przechowuje jako liste
            self.data.append(collections.deque([0] * plotLength, maxlen=plotLength))
        self.isRun = True
        self.isReceiving = False
        self.thread = None
        self.plotTimer = 0
        self.previousTimer = 0
        #zapis do pliku csv - pusta tablica
        self.csvData = []

        print('Laczenie z : ' + str(serialPort) + ' przy ' + str(serialBaud) + ' BAUD.')
        try:
            self.serialConnection = serial.Serial(serialPort, serialBaud, timeout=4)
            print('Polaczono z ' + str(serialPort) + ' przy ' + str(serialBaud) + ' BAUD.')
        except:
            print("Nieudane polaczenie z " + str(serialPort) + ' przy ' + str(serialBaud) + ' BAUD.')

    def readSerialStart(self):
        #inicjowanie komunikacji
        #wykorzystywanie thread do operacji w tle
        if self.thread == None:
            self.thread = Thread(target=self.backgroundThread)
            self.thread.start()
            # Warunek rozpoczecia pracy po otrzymaniu wartosci/odczytow
            while self.isReceiving != True:
                time.sleep(0.1)

    def getSerialData(self, frame, lines, lineValueText, lineLabel, timeText):
        #pobieranie danych
        ## OBLICZANIE INTERWALU
        currentTimer = time.perf_counter()  #pomiar czasu dla interwaluf
        self.plotTimer = int((currentTimer - self.previousTimer) * 1000)
        self.previousTimer = currentTimer   #pomiar czasu dla interwalu
        timeText.set_text('Interwał = ' + str(self.plotTimer) + ' [ms]')
        ##
        privateData = copy.deepcopy(
            self.rawData[:])  # so that the 3 values in our plots will be synchronized to the same sample time
        for i in range(self.numPlots):
            data = privateData[(i * self.dataNumBytes):(self.dataNumBytes + i * self.dataNumBytes)]
            value, = struct.unpack(self.dataType, data) #dekodowanie wiadomosci
            self.data[i].append(value)  # dodawanie ostatniej/najnowszej wartosci
            lines[i].set_data(range(self.plotMaxLength), self.data[i])  #rysowanie wykresu
            lineValueText[i].set_text(lineLabel[i] + ' = ' + str(round(value, 2)) + '   [m/s^2]')
            #lineValueText[i].set_text(lineLabel[i] + ' = ' + str(round(value, 2)) + '   [deg]')
        self.csvData.append([self.data[0][-1], self.data[1][-1], self.data[2][-1]])

    def backgroundThread(self):  # odbieranie danych
        time.sleep(1.0)  # czas na otrzymanie
        self.serialConnection.reset_input_buffer()
        while (self.isRun):
            self.serialConnection.readinto(self.rawData)
            self.isReceiving = True
            print(self.rawData)

    def close(self):
        self.isRun = False
        self.thread.join()
        self.serialConnection.close()
        print('Rozłączono...')
        df = pd.DataFrame(self.csvData)
        df.to_csv('data.csv')

def main():
    portName = 'COM6'
    baudRate = 38400        #wartosc wymagana dla odpowiedniej synchronizacji
    maxPlotLength = 500  # liczba pkt na osi poziomej
    dataNumBytes = 4  # liczba bajtow
    numPlots = 3  # liczba wykresow w jednym oknie
    s = serialPlot(portName, baudRate, maxPlotLength, dataNumBytes, numPlots)
    s.readSerialStart()  # background thread

    # plotting starts below
    pltInterval = 50  # odswiezanie animacji
    xmin = 0
    xmax = maxPlotLength
    ymin = -(100)
    ymax = 100
    fig = plt.figure(figsize=(15, 8))
    ax = plt.axes(xlim=(xmin, xmax), ylim=(float(ymin - (ymax - ymin) / 10), float(ymax + (ymax - ymin) / 10)))
    ax.set_title('Akcelerometr - orientacja')
    ax.set_xlabel("Nr próbki [-]")
    ax.set_ylabel("Kąt [deg]")

    #lineLabel = ['roll ', 'pitch ', 'yaw']
    lineLabel = ['X ', 'Y ', 'Z']
    style = ['r-', 'c-', 'b-']  # linestyles dla kazdego z wykresow
    timeText = ax.text(0.70, 0.95, '', transform=ax.transAxes)
    lines = []
    lineValueText = []

    for i in range(numPlots):
        lines.append(ax.plot([], [], style[i], label=lineLabel[i])[0])
        lineValueText.append(ax.text(0.70, 0.90 - i * 0.05, '', transform=ax.transAxes))

    anim = animation.FuncAnimation(fig, s.getSerialData, fargs=(lines, lineValueText, lineLabel, timeText), interval=pltInterval)  # krotka

    #def getSerialData(self, frame, lines, lineValueText, lineLabel, timeText):
    # animacja animacji. (fig, func, fargs, interval)
    # fig - obiekt graficzny
    # func - funkcja wywolywana za kazdym razem
    # fargs - dodatkowe argumenty przekazywane (krotka)

    plt.legend(loc="upper left")
    plt.grid('both', 'both')
    plt.show()

    s.close()


if __name__ == '__main__':
    main()