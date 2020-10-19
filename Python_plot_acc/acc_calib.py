import matplotlib.pyplot as plt
import numpy as np
from numpy.linalg import eig, inv
from mpl_toolkits.mplot3d import Axes3D
import csv
#####################################################################################
'''
Wczytuje odczyty z akcelerometru i skaluje je w celu wykonania kalibracji
'''
def standaryzacja(loc_v):
    '''

    :param loc_v:   wektor ktorego nalezy wyznaczyc wsp standaryzacji
    :return:        krotka: (do odjecia, do podzielenia)
    '''
    # ekstrema
    v_min = min(loc_v)
    v_max = max(loc_v)
    # standaryzacja

    sub = 0.5 * (v_min + v_max)
    div = 0.5 * (v_max - v_min)/9.81
    return sub, div

#####################################################################################
############################       GLOWNY PROGRAM       #############################
#####################################################################################
x_raw=[]
y_raw=[]
z_raw=[]
results = []
index = 0
# Otwarcie pliku
with open("data.csv") as csvfile:
    reader = csv.reader(csvfile, quoting=csv.QUOTE_NONNUMERIC) # zmiana str -> float
    for row in reader: # linia to lista
        x_raw.append(row[1])
        y_raw.append(row[2])
        z_raw.append(row[3])
        index += 1
print("Odczytano {} wierszy z pliku data.csv".format(index))
# Wyswietlenie surowych danych
fig1 = plt.figure(num=None, figsize=(15, 5))
fig1.suptitle('Kalibracja akcelerometru - surowe dane')
ax1 = fig1.add_subplot(111)

#
index = range(len(x_raw))
ax1.plot(index, x_raw ,'go', label=' - kierunek x',markersize = 2)
ax1.plot(index, y_raw ,'ro', label=' - kierunek y',markersize = 2)
ax1.plot(index, z_raw ,'ko', label=' - kierunek z', markersize = 2)
ax1.set_xlabel('Nr. pomiaru [-]')
ax1.set_ylabel('Odczyt [-]')
ax1.grid(True, which='both')
ax1.legend()
#
fig1.tight_layout()


# wyznaczenie wspolczynnikow
coef_x, div_x = standaryzacja(x_raw)
print('Wpółczynniki kalibracyjne dla x: x - (   ',str(round(coef_x,4)),'   )  / (   ',str(round(div_x,4)),'   )')
coef_y, div_y = standaryzacja(y_raw)
print('Wpółczynniki kalibracyjne dla y: y - (   ',str(round(coef_y,4)),'   )  / (   ',str(round(div_y,4)),'   )')
coef_z, div_z = standaryzacja(z_raw)
print('Wpółczynniki kalibracyjne dla z: z - (   ',str(round(coef_z,4)),'   )  / (   ',str(round(div_z,4)),'   )')

#standaryzacja
x_stand = [(item - coef_x)/div_x for item in x_raw]
y_stand = [(item - coef_y)/div_y for item in y_raw]
z_stand = [(item - coef_z)/div_z for item in z_raw]

#wyswietlenie danych po standaryzacji
fig2 = plt.figure(num=None, figsize=(15, 5))
fig2.suptitle('Kalibracja akcelerometru - skalibrowane')
ax2 = fig2.add_subplot(111)
ax2.plot(index, x_stand, 'go', label=' - kierunek x', markersize = 2)
ax2.plot(index, y_stand, 'ro', label=' - kierunek y', markersize = 2)
ax2.plot(index, z_stand, 'ko', label=' - kierunek z', markersize = 2)
ax2.set_xlabel('Nr. pomiaru [-]')
ax2.set_ylabel('Przyśpieszenie [m/s^2]')

ax2.grid(True, which='both')
#
fig2.tight_layout()
ax2.legend()
plt.show()