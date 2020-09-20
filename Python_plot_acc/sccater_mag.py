import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import csv
x=[]
y=[]
z=[]
results = []
index = 0
with open("data.csv") as csvfile:
    reader = csv.reader(csvfile, quoting=csv.QUOTE_NONNUMERIC) # zmiana str -> float
    for row in reader: # linia to lista
        x.append(row[1])
        y.append(row[2])
        z.append(row[3])
        index += 1
print(index)
print("Liczba wierszy dla X:  ",len(x))
print("Liczba wierszy dla Y:  ",len(y))
print("Liczba wierszy dla Z:  ",len(z))
#print(type(results))
# 3D  plot
fig1 = plt.figure(num=None, figsize=(6, 5))
ax1 = fig1.add_subplot(111,projection='3d')
ax1.grid(True)
ax1.view_init(elev=20, azim=-135)
ax1.scatter(x,y,z, s=1)
fig1.suptitle('Kalibracja magnetometru - surowe dane')
ax1.set_xlabel('Mx [uT]')
ax1.set_ylabel('My [uT]')
ax1.set_zlabel('Mz [uT]')

# 2D plots
fig2 = plt.figure(num=None, figsize=(15, 5))
fig2.suptitle('Kalibracja magnetometru - surowe dane')
ax21 = fig2.add_subplot(131)
ax22 = fig2.add_subplot(132)
ax23 = fig2.add_subplot(133)

#
ax21.plot(x,y,'k.')
ax21.set_xlabel('Mx [uT]')
ax21.set_ylabel('My [uT]')
ax21.axis('equal')
ax21.grid(True, which='both')
#
ax22.plot(x,z,'r.')
ax22.set_xlabel('Mx [uT]')
ax22.set_ylabel('Mz [uT]')
ax22.axis('equal')
ax22.grid(True, which='both')

#
ax23.plot(y,z,'g.')
ax23.set_xlabel('My [uT]')
ax23.set_ylabel('Mz [uT]')
ax23.axis('equal')
ax23.grid(True, which='both')

#
fig1.tight_layout()
fig2.tight_layout()
#plt.show()

# Usuwanie przesuniecia
x_off = 0
y_off = 0
z_off = 0
x_kal = x
y_kal = y
z_kal = z
## Pozyskanie  offsetow  na kazdej osi
x_off = 0.5*(max(x) + min(x))
y_off = 0.5*(max(y) + min(y))
z_off = 0.5*(max(z) + min(z))

## korekcja
x_kal[:] = [i - x_off for i in x_kal]
y_kal[:] = [i - y_off for i in y_kal]
z_kal[:] = [i - z_off for i in z_kal]
# Wyswietlanie wynikow
# 3D  plot
fig3 = plt.figure(num=None, figsize=(6, 5))
ax3 = fig3.add_subplot(111,projection='3d')
ax3.grid(True)
ax3.view_init(elev=20, azim=-135)
ax3.scatter(x_kal,y_kal,z_kal)
fig3.suptitle('Kalibracja magnetometru - po kalibracji, krok 1')
ax3.set_xlabel('Mx [uT]')
ax3.set_ylabel('My [uT]')
ax3.set_zlabel('Mz [uT]')
# 2D plots
fig4 = plt.figure(num=None, figsize=(15, 5))
fig4.suptitle('Kalibracja magnetometru - po kalibracji, krok 1')
ax41 = fig4.add_subplot(131)
ax42 = fig4.add_subplot(132)
ax43 = fig4.add_subplot(133)

#
ax41.plot(x_kal,y_kal,'k.')
ax41.set_xlabel('Mx [uT]')
ax41.set_ylabel('My [uT]')
ax41.axis('equal')
ax41.grid(True, which='both')
#
ax42.plot(x_kal,z_kal,'r.')
ax42.set_xlabel('Mx [uT]')
ax42.set_ylabel('Mz [uT]')
ax42.axis('equal')
ax42.grid(True, which='both')

#
ax43.plot(y_kal,z_kal,'g.')
ax43.set_xlabel('My [uT]')
ax43.set_ylabel('Mz [uT]')
ax43.axis('equal')
ax43.grid(True,which='both')

#
fig3.tight_layout()
fig4.tight_layout()
plt.show()

#Krok drugi