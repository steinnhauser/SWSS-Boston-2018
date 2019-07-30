import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

"""
c1=b1[b1<=200]
c2=b2[b2<=200]
"""


#####Sunspots for jan-sep##########
df=pd.read_csv("Daily_Sunspots_20070101_20070901.txt", skiprows=66, skipfooter=3, delim_whitespace=True, 
names=['dt','tm', 'sunspots'])
temp=df[['dt', 'tm']].apply(lambda x: ' '.join(x), axis=1)
df['ut']=pd.to_datetime(temp, format='%d-%m-%Y %H:%M:%S.%f')



sunspots=df['sunspots']
t1=df['ut']


plt.subplot(611)
plt.plot(df['ut'], df['sunspots'], label="Sunspots")
plt.ylabel("Number")
plt.legend()


######DST-index for jan-sep##########
df=pd.read_csv("DST_index_2007_jan_sep.txt", skiprows=66, skipfooter=3, delim_whitespace=True, 
names=['dt','tm', 'DST'])
temp=df[['dt', 'tm']].apply(lambda x: ' '.join(x), axis=1)
df['ut']=pd.to_datetime(temp, format='%d-%m-%Y %H:%M:%S.%f')


DST=df['DST']
t2=df['ut']

plt.subplot(612)
plt.plot(df['ut'], abs(df['DST']), label="DST-Index of Earth")
plt.legend()



######STB MAG, p-speed, p-density, p-temp ###########

df=pd.read_csv("STB_data_2007.txt", skiprows=74, skipfooter=3, delim_whitespace=True, 
names=['dt','tm', 'mag', 'spd', 'dns', 'temp'])


temp=df[['dt', 'tm']].apply(lambda x: ' '.join(x), axis=1)
df['ut']=pd.to_datetime(temp, format='%d-%m-%Y %H:%M:%S.%f')

b2=abs(df['mag'])


STB_magnan=len([x for x in df['mag'] if float(x) <=-100000])
#140

"""
df['mag'][df['mag']<=-100000]=np.nan
df['spd'][df['spd']<=-100000]=np.nan
df['dns'][df['dns']<=-100000]=np.nan
df['temp'][df['temp']<=-100000]=np.nan
"""

STB_mag=df['mag']
STB_spd=df['spd']
STB_dns=df['dns']
STB_tmp=df['temp']
t3=df['ut']



plt.subplot(613)
plt.plot(df['ut'], df['mag'], label="Magnetic field")
plt.legend()
plt.subplot(614)
plt.plot(df['ut'], df['spd'], label="Plasma speed")
plt.legend()

plt.subplot(615)
plt.plot(df['ut'], df['dns'], label="Plasma density")
plt.legend()
plt.subplot(616)
plt.plot(df['ut'], df['temp'], label="Plasma temperature")
plt.legend()
plt.figure()



#####ACE magnetic field####
df=pd.read_csv("ACE_data_2007_B.txt", skiprows=59, skipfooter=3, delim_whitespace=True, 
names=['dt','tm', 'Bmag'])
temp=df[['dt', 'tm']].apply(lambda x: ' '.join(x), axis=1)
df['ut']=pd.to_datetime(temp, format='%d-%m-%Y %H:%M:%S.%f')

ACE_Bnan=int(len([x for x in df['Bmag'] if float(x) <=-100000]))
#2
#df['Bmag'][df['Bmag']<=-100000]=np.nan

ACE_B=df['Bmag']
t4=df['ut']


plt.subplot(311)
plt.plot(df['ut'], df['Bmag'], label="|B| for ACE")
plt.legend()


#####ACE REST###########
df=pd.read_csv("ACE_data_2007_rest.txt", skiprows=64, skipfooter=3, delim_whitespace=True, 
names=['dt','tm', 'Pdens', 'Pspe'])
temp=df[['dt', 'tm']].apply(lambda x: ' '.join(x), axis=1)
df['ut']=pd.to_datetime(temp, format='%d-%m-%Y %H:%M:%S.%f')


df['Pdens'][df['Pdens']<=-100000]=np.nan
df['Pspe'][df['Pspe']<=-100000]=np.nan

ACE_dns=df['Pdens']
ACE_spe=df['Pspe']
t5=df['ut']


plt.subplot(312)
plt.plot(df['ut'], df['Pdens'], label="Density for ACE")
plt.legend()
plt.subplot(313)
plt.plot(df['ut'], df['Pspe'], label="Speed for ACE")
plt.legend()
plt.figure()



###DATA WE HAVE###
sunspots  	  				#t1
DST 		 				#t2
STB_mag
STB_spd 
STB_dns 
STB_tmp 					#t3
ACE_B 						#t4
ACE_dns
ACE_spe 					#t5
###           ###

"""
g1=DST
g1[g1<=-100000]=np.nan
g2=STB_mag
g2[g2<=-100000]=np.nan
g3=ACE_B
g3[g3<=-100000]=np.nan

plt.subplot(311)
plt.plot(t1, g1, label="DST data")
plt.title("Magnetic field measurements of the three referance points")
plt.xlabel("Time, Date format YYYYMM")
plt.ylabel("1-Hr DST [nT]")
plt.legend(loc="best")
plt.subplot(312)
plt.plot(t3, g2, label="Stereo-B magnetic field data")
plt.xlabel("Time, Date format YYYYMM")
plt.ylabel("|B| [nT]")
plt.legend(loc="best")
plt.subplot(313)
plt.plot(t4, g3, label="ACE magnetic field data")
plt.xlabel("Time, Date format YYYYMM")
plt.ylabel("|B| [nT]")
plt.legend(loc="best")
plt.show()
"""

#T=20995200 #s
T=243 #d



###INTERPOLATION AND AXES###

N1=int(len(DST))
fs=N1/T
xaxis1=np.fft.fftfreq(N1, 1/fs)
fft_DST=np.fft.fft(DST, N1)



N2=int(len(STB_mag))
fs=N2/T
deltat=1/fs
xaxis2=np.fft.fftfreq(N2, 1/fs)


index=np.linspace(0, N2-1, N2, dtype=int)
y_uten=STB_mag[STB_mag>=-10000000]
a=np.where(STB_mag<=-10000000)
a=a[0]
a=np.ndarray.tolist(a)
index_uten=np.ndarray.tolist(index)


for offf in sorted(a, reverse=True):
    del index_uten[offf]

index=np.asarray(index)
index_uten=np.asarray(index_uten)
STB_mag_=np.interp(index*deltat, index_uten*deltat, y_uten)
STB_mag[STB_mag<=-1000000]=np.nan



plt.subplot(211)
plt.title("Regression of STEREO-B data for Fourier Transformation")
plt.plot(index*deltat, STB_mag, label="Magnetic flux data from STEREO-B")
plt.xlim(100, 120)
plt.xlabel("Time in days")
plt.ylabel("|B| [nT]")
plt.legend()
plt.subplot(212)
plt.plot(index*deltat, STB_mag_, label="Regressed data from STEREO-B")
plt.xlim(100, 120)
plt.xlabel("Time in days")
plt.ylabel("|B| [nT]")
plt.legend()
plt.show()

fft_STB=np.fft.fft(STB_mag_, N2)


N3=int(len(ACE_B))
fs=N3/T
deltat=1/fs
xaxis3=np.fft.fftfreq(N3, 1/fs)


index=np.linspace(0, N3-1, N3, dtype=int)
y_uten=ACE_B[ACE_B>=-10000000]
a=np.where(ACE_B<=-10000000)
a=a[0]
a=np.ndarray.tolist(a)
index_uten=np.ndarray.tolist(index)


for offf in sorted(a, reverse=True):
    del index_uten[offf]

index=np.asarray(index)
index_uten=np.asarray(index_uten)
ACE_B_=np.interp(index*deltat, index_uten*deltat, y_uten)
ACE_B[ACE_B<=-1000000]=np.nan



fft_ACE=np.fft.fft(ACE_B_, N3)

############################

"""
fre = np.linspace(0,1/deltat,N2)
amp = np.zeros(len(fre))
amp = np.abs(fft_DST)
"""

plt.subplot(311)
plt.plot(xaxis1[1:int(N1/2)], fft_DST[1:int(N1/2)], label="DST fft")
plt.legend()
plt.xlabel("Frequency [per day]")
plt.ylabel("Rel. amp.")
plt.xlim(0, 0.5)
plt.title("Fourier Transformations of the three magnetic field data files")
plt.subplot(312)
plt.plot(xaxis2[1:int(N2/2)], fft_STB[1:int(N2/2)], label="STB_B fft")
plt.xlabel("Frequency [per day]")
plt.ylabel("Rel. amp.")
plt.xlim(0, 0.5)
plt.legend()
plt.subplot(313)
plt.plot(xaxis3[1:int(N3/2)], fft_ACE[1:int(N3/2)], label="ACE_B fft")
plt.xlabel("Frequency [per day]")
plt.ylabel("Rel. amp.")
plt.xlim(0, 0.5)
plt.legend()
plt.show()




#todo:
#Compare first months to last months.
#Where is the border though?

#Wavelet transformation to get time-image.
#Will it be much better than the Fourier?

#Between 2007-06 and 2007-07 there is a 
#difference in fourier spectrum similarity
#Is this significant enough to conclude that
#the STEREO-B satellite is far enough away?

