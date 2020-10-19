import matplotlib.pyplot as plt
import numpy as np
from numpy.linalg import eig, inv
from mpl_toolkits.mplot3d import Axes3D
import csv


##############################
def ls_ellipsoid(lx,ly,lz):
    '''
    :param lx:  wektor z odczytami X
    :param ly:  wektor z odczytami Y
    :param lz:  wektor z odczytami Z
    :return:    wspolczynniki podasowanej elipsoidy
    '''
    # dodanie jednego wymiaru macierzy - wymog hstack
    x = lx[:,np.newaxis]
    y = ly[:,np.newaxis]
    z = lz[:,np.newaxis]

    #  Rownanie eplipsoidy:
    #  Ax^2 + By^2 + Cz^2 +  Dxy +  Exz +  Fyz +  Gx +  Hy +  Iz = 1
    J = np.hstack((x*x,y*y,z*z,x*y,x*z,y*z, x, y, z))    #tworzy strukture kazdego wiersza, iterujac po danych
    K = np.ones_like(x) #wektor jednostkowy

    JT       = J.transpose()
    JTJ      = np.dot(JT,J)
    InvJTJ   = np.linalg.inv(JTJ)
    coef     = np.dot(InvJTJ, np.dot(JT,K))  #wspol. wielomianu

    ans = np.append(coef,-1) #przesuniecie jedynki z prawej str. na lewa

    return (ans)
##############################
def polyToParams3D(vector):
    '''

    :param vec:         wektor wspolczynnikow
    :return:            srodek elipsoidy, wzmocnienie osi, macierz rotacji
    '''

    print('\nWspółczynniki: \n',vector)
    # nalezy podzielic przez dwa wyrazy nie na diagonalnej
    Amat=np.array(
    [
    [ vector[0],     vector[3]/2.0, vector[4]/2.0, vector[6]/2.0 ],
    [ vector[3]/2.0, vector[1],     vector[5]/2.0, vector[7]/2.0 ],
    [ vector[4]/2.0, vector[5]/2.0, vector[2],     vector[8]/2.0 ],
    [ vector[6]/2.0, vector[7]/2.0, vector[8]/2.0, vector[9]     ]
    ])

    print('\nAlgebraiczna postać równania: \n',Amat)

    A3=Amat[0:3,0:3]
    A3inv=inv(A3)
    ofs=vector[6:9]/2.0
    center=-np.dot(A3inv,ofs)
    print('\nŚrodek: ',center)



    Tofs=np.eye(4)
    Tofs[3,0:3]=center
    R = np.dot(Tofs,np.dot(Amat,Tofs.T))
    print('\nAlgebraiczna postać po usunięciu odsunięcia: \n',R,'\n')

    R3=R[0:3,0:3]
    R3test=R3/R3[0,0]
    print('Unormowana postać:  \n',R3test)
    s1=-R[3, 3]
    R3S=R3/s1
    (el,ec)=eig(R3S)

    recip=1.0/np.abs(el)
    axes=np.sqrt(recip)
    print('\nWzmocnienie osi" \n',axes  ,'\n')

    inve=inv(ec)
    print('\nMacierz rotacji: \n',inve)
    return (center,axes,inve)
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
# 3D  plot
fig1 = plt.figure(num=None, figsize=(7, 6))
ax1 = fig1.add_subplot(111,projection='3d')
ax1.grid(True)
ax1.view_init(elev=20, azim=-135)
ax1.scatter(x_raw,y_raw,z_raw, s=1)
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
ax21.plot(x_raw,y_raw,'k*', markersize = 2)
ax21.set_xlabel('Mx [uT]')
ax21.set_ylabel('My [uT]')
ax21.axis('equal')
ax21.grid(True, which='both')
#
ax22.plot(x_raw,z_raw,'r*', markersize = 2)
ax22.set_xlabel('Mx [uT]')
ax22.set_ylabel('Mz [uT]')
ax22.axis('equal')
ax22.grid(True, which='both')

#
ax23.plot(y_raw,z_raw,'g*', markersize = 2)
ax23.set_xlabel('My [uT]')
ax23.set_ylabel('Mz [uT]')
ax23.axis('equal')
ax23.grid(True, which='both')

#
fig1.tight_layout()
fig2.tight_layout()


#usuwanie najbardziej odsunietych punktow
avg_x = sum(x_raw)/len(x_raw)
avg_y = sum(y_raw)/len(y_raw)
avg_z = sum(z_raw)/len(z_raw)
for i in range(10):
    x_raw[x_raw.index(max(x_raw))] = avg_x
    y_raw[y_raw.index(max(y_raw))] = avg_y
    z_raw[z_raw.index(max(z_raw))] = avg_z

    x_raw[x_raw.index(min(x_raw))] = avg_x
    y_raw[y_raw.index(min(y_raw))] = avg_y
    z_raw[z_raw.index(min(z_raw))] = avg_z
#konwersja na macierze typu numpy
X_ar = np.array(x_raw)
Y_ar = np.array(y_raw)
Z_ar = np.array(z_raw)

# Metoda namniejszych kwadratow do wpasowania w elipsoide o rownaniu:
#  Ax^2 + By^2 + Cz^2 +  2Dxy +  2Exz +  2Fyz +  2Gx +  2Hy +  2Iz  = 1
# ostatnie wyrazy posiadaja wspolczynnik dwa, leza one poza diagonalna
# nalezy pamietac o podzieleniu na koncu dzialan.

coef = ls_ellipsoid(X_ar, Y_ar, Z_ar)
center,axes,inve = polyToParams3D(coef)

## Usuwanie przesuniecia / offsetu
x_c = X_ar - center[0]
y_c = Y_ar - center[1]
z_c = Z_ar - center[2]

# 3D  plot
fig3 = plt.figure(num=None, figsize=(7, 6))
ax3 = fig3.add_subplot(111,projection='3d')
ax3.grid(True)
ax3.view_init(elev=20, azim=-135)
ax3.scatter(x_c,y_c,z_c, s=1)
fig3.suptitle('Kalibracja magnetometru - po kalibracji \n usunięcie odsunięcia')
ax3.set_xlabel('Mx [uT]')
ax3.set_ylabel('My [uT]')
ax3.set_zlabel('Mz [uT]')
# 2D plots
fig4 = plt.figure(num=None, figsize=(15, 5))
fig4.suptitle('Kalibracja magnetometru - po kalibracji \n usunięcie odsunięcia')
ax41 = fig4.add_subplot(131)
ax42 = fig4.add_subplot(132)
ax43 = fig4.add_subplot(133)

#
ax41.plot(x_c,y_c,'k*', markersize=2)
ax41.set_xlabel('Mx [uT]')
ax41.set_ylabel('My [uT]')
ax41.axis('equal')
ax41.grid(True, which='both')
#
ax42.plot(x_c,z_c,'r*', markersize=2)
ax42.set_xlabel('Mx [uT]')
ax42.set_ylabel('Mz [uT]')
ax42.axis('equal')
ax42.grid(True, which='both')

#
ax43.plot(y_c,z_c,'g*', markersize=2)
ax43.set_xlabel('My [uT]')
ax43.set_ylabel('Mz [uT]')
ax43.axis('equal')
ax43.grid(True, which='both')

#
fig3.tight_layout()
fig4.tight_layout()


## Rotacja
x_r = np.empty_like(x_c)
y_r = np.empty_like(y_c)
z_r = np.empty_like(z_c)
for i in range(len(x_c)):
    data = np.array([[x_c[i]],[y_c[i]],[z_c[i]]]) #macierz jednostkowego odczytu
    rot = np.dot(inve, data)
    x_r[i] = rot [0]
    y_r[i] = rot [1]
    z_r[i] = rot [2]

# 3D  plot
fig5 = plt.figure(num=None, figsize=(7, 6))
ax5 = fig5.add_subplot(111,projection='3d')
ax5.grid(True)
ax5.view_init(elev=20, azim=-135)
ax5.scatter(x_r,y_r,z_r, s=2)
fig5.suptitle('Kalibracja magnetometru - met. majmniejszych kwadratow')
ax5.set_xlabel('Mx [uT]')
ax5.set_ylabel('My [uT]')
ax5.set_zlabel('Mz [uT]')
# 2D plots
fig6 = plt.figure(num=None, figsize=(15, 5))
fig6.suptitle('Kalibracja magnetometru - met. majmniejszych kwadratow')
ax61 = fig6.add_subplot(131)
ax62 = fig6.add_subplot(132)
ax63 = fig6.add_subplot(133)

#
ax61.plot(x_r,y_r,'k*', markersize=2)
ax61.set_xlabel('Mx [uT]')
ax61.set_ylabel('My [uT]')
ax61.axis('equal')
ax61.grid(True, which='both')
#
ax62.plot(x_r,z_r,'r*', markersize=2)
ax62.set_xlabel('Mx [uT]')
ax62.set_ylabel('Mz [uT]')
ax62.axis('equal')
ax62.grid(True, which='both')

#
ax63.plot(y_r,z_r,'g*', markersize=2)
ax63.set_xlabel('My [uT]')
ax63.set_ylabel('Mz [uT]')
ax63.axis('equal')
ax63.grid(True,which='both')

#
fig5.tight_layout()
fig6.tight_layout()

## normalizacja wzmocnienia
print(axes)
x_r = x_r  / axes[0]

y_r = y_r  / axes[1]

z_r = z_r  / axes[2]

##
# 3D  plot
fig7 = plt.figure(num=None, figsize=(7, 6))
ax7 = fig7.add_subplot(111,projection='3d')
ax7.grid(True)
ax7.view_init(elev=20, azim=-135)
ax7.scatter(x_r,y_r,z_r, s=1)
fig7.suptitle('Kalibracja magnetometru - met. majmniejszych kwadratow\nunormowane')
ax7.set_xlabel('Mx [uT]')
ax7.set_ylabel('My [uT]')
ax7.set_zlabel('Mz [uT]')
# 2D plots
fig8 = plt.figure(num=None, figsize=(15, 5))
fig8.suptitle('Kalibracja magnetometru - met. majmniejszych kwadratow\nunormowane')
ax81 = fig8.add_subplot(131)
ax82 = fig8.add_subplot(132)
ax83 = fig8.add_subplot(133)

#
ax81.plot(x_r,y_r,'k*', markersize=2)
ax81.set_xlabel('Mx [uT]')
ax81.set_ylabel('My [uT]')
ax81.axis('equal')
ax81.grid(True, which='both')
#
ax82.plot(x_r,z_r,'r*', markersize=2)
ax82.set_xlabel('Mx [uT]')
ax82.set_ylabel('Mz [uT]')
ax82.axis('equal')
ax82.grid(True, which='both')

#
ax83.plot(y_r,z_r,'g*', markersize=2)
ax83.set_xlabel('My [uT]')
ax83.set_ylabel('Mz [uT]')
ax83.axis('equal')
ax83.grid(True,which='both')

#
fig7.tight_layout()
fig8.tight_layout()
plt.show()