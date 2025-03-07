import numpy as np
import pandas as pd
from scipy.integrate import odeint

import matplotlib.pyplot as plt
import matplotlib.animation

import cartopy.crs as ccrs
import cartopy.feature as ccfe



# Enable interactive plot
#%matplotlib notebook
#%matplotlib widget

# Constantes 
pi = np.pi
## Radio medio de la Tierra en m
rad = 6.37e6
## Velocidad angular de rotación de la Tierra en rad s^-1
omega = 7.292e-5


print('Programa para graficar la trayectoria de una partícula afectada por el efecto Coriolis.\nRealizada por: Alejandro Jaramillo Moreno\nInstituto de Ciencias de la Atmósfera y Cambio Climático\nUniversidad Nacional Autónoma de México\n2022')

def coriolis_simple(v,tt,rad,omega):
    theta,phi,ux,uy = v
    thetap = ux/(rad*np.cos(phi))
    phip = uy/rad
    uxp = (2.*omega)*np.sin(phi)*uy
    uyp = -(2.*omega)*np.sin(phi)*ux
    return thetap,phip,uxp,uyp

def coriolis_curvature(v,tt,rad,omega):
    theta,phi,ux,uy = v
    thetap = ux/(rad*np.cos(phi))
    phip = uy/rad
    uxp = (2.*omega)*np.sin(phi)*uy+(ux*uy*np.tan(phi)/rad)
    uyp = -(2.*omega)*np.sin(phi)*ux-(ux*ux*np.tan(phi)/rad)
    return thetap,phip,uxp,uyp


def Graficar_Coriolis(init_lat,init_lon,u0,v0,runtime,frames=50):
    lat0 = pi*init_lat/180.
    lon0 = pi*init_lon/180.
    time = runtime*24.*3600.
    # Maximum time point and total number of time points
    delta_t = 60*60
    tt = np.arange(0, time+0.1, delta_t)
    
    f0 = odeint(coriolis_simple,(lon0,lat0,u0,v0),tt,args=(rad,omega))
    theta,phi,ux,uy = f0.T
    df = pd.DataFrame({'longitude':theta*(360./(2.*pi)),'latitude':phi*(360./(2.*pi)),'ux':ux,'uy':uy},index=tt)
    
    f1 = odeint(coriolis_curvature,(lon0,lat0,u0,v0),tt,args=(rad,omega))
    theta,phi,ux,uy = f1.T
    df2 = pd.DataFrame({'longitude':theta*(360./(2.*pi)),'latitude':phi*(360./(2.*pi)),'ux':ux,'uy':uy},index=tt)
    
    longitude = df['longitude'].values
    latitude = df['latitude'].values
    
    longitude_c = df2['longitude'].values
    latitude_c = df2['latitude'].values
    
    fig = plt.figure(figsize=(10,10))
    ax = plt.subplot2grid((1,1),(0,0),projection=ccrs.PlateCarree())

    plt.plot(longitude,latitude,color='black',lw=1.0,ls='--',transform=ccrs.PlateCarree())
    plt.plot(longitude_c,latitude_c,color='red',lw=1.0,ls='--',transform=ccrs.PlateCarree())
    ax.coastlines()
    ax.set_global()
    ax.stock_img()
    plt.show()
    plt.close()
    
    
    
    
    
    plt.rcParams["animation.html"] = "jshtml"
    plt.rcParams['figure.dpi'] = 150  
    plt.ioff()
    fig, ax = plt.subplots(figsize=(3,3),subplot_kw={'projection': ccrs.Orthographic(central_longitude=init_lon, central_latitude=init_lat)})
    ax.set_global()

    def animate(t):
        plt.cla()
        ax.coastlines(lw=0.5)
        ax.stock_img()
        #ax.set_title('{} seconds'.format(tt[i]))
        plt.plot(longitude[:t],latitude[:t],color='black',lw=1.0,ls='--',transform=ccrs.PlateCarree())
        plt.plot(longitude_c[:t],latitude_c[:t],color='red',lw=1.0,ls='--',transform=ccrs.PlateCarree())

    anim = matplotlib.animation.FuncAnimation(fig, animate, frames=frames)
    return anim