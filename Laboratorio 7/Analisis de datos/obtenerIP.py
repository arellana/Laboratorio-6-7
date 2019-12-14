from parspyfunc import parspy
from filtpyfunc_v2 import filtpy
from matplotlib import pyplot as plt
import numpy as np
import scipy.signal as sp

#%%
filename='*\170327prn10seg1.dat'
for i in range(len(filename)-3):
    if filename[i:i+3] == 'prn':
        fecha = filename[i-6:i]

angElev, angAzim, intensidad, sat = parspy(filename, ploteo = False, guardar = False)

angElev_filt, intensidad_filt = filtpy(angElev, angAzim, intensidad, sat, 1.9, ploteo=True, guardar=False)

ang_curvas = np.linspace(7,23,452)

comienzo = angElev_filt[0]
if comienzo > 7:
    for i in range(len(ang_curvas)):
        if (ang_curvas[i]-comienzo) < 0.01:
            c = i
            sampleo = len(ang_curvas[c:])
else:
    comienzo = 7
    sampleo = 452

final = angElev_filt[-1]
if final < 23:
    for i in range(len(ang_curvas)):
        if (ang_curvas[i]-final) < 0.07:
            d = i
            sampleo = len(ang_curvas[c:d])
else:
    final = 23

for i in range(len(angElev_filt)):
    if (angElev_filt[i]-comienzo) < 0.01:
        a = i
    elif (angElev_filt[i]-final) < 0.01:
        b = i

angElev_filt1 = angElev_filt[a:b+1]
intensidad_filt1 = intensidad_filt[a:b+1]

print('')
print(fecha, str(sat))
print('primer angulo:  ',comienzo)
print('ultimo angulo:  ',angElev_filt1[-1])
print('sampleo:  ',sampleo)

intensidad_r, angElev_r = sp.resample(intensidad_filt1,sampleo, angElev_filt1)

plt.figure()
plt.plot(angElev_filt1,intensidad_filt1,'o')
plt.plot(angElev_r,intensidad_r, 'ro')
plt.xlabel('ángulo de elevación')
plt.ylabel('intensidad')
plt.title('prn'+str(sat))

np.savetxt(fecha+'prn'+str(sat)+'_'+'filt.txt', np.transpose([angElev_r,intensidad_r]), delimiter = ',')

