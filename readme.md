# GeoSoftII_NDVI_Process
### Geosoftware II Projekt WiSe 2020/21
---

## Inhaltsverzeichnis
[1. Übersicht](#overview) \
[2. Installation](#install) \
[3. Anwendung](#use) \
  3.1. Zentrale Funktionalität \
  3.2. API Endpunkte \
[4. Anhang](#annex)

\
<a name="overview"><h3>Übersicht</h3></a>
Dieses Projekt ist ein Teil für einen neuen [openEO](https://openeo.org/) Backenddriver der mit [Pangeo Software Stack](https://pangeo.io/) arbeitet.

Ziel ist die vom [Dataserver](https://github.com/GeoSoftII2020-21/GeoSoftII_DataServer) bereitgestellten Datacubes auf den NDVI zu untersuchen.
Dabei wird konkret die User Story: "Sentinel2 Datensatz um Münster auf NDVI untersuchen" des Pflichtenheftes umgesetzt.

Außerdem gibt es ein [Docker Repository](https://hub.docker.com/repository/docker/felixgi1516/geosoft2_ndvi_process), welches mit diesem verlinkt ist und über das nach Fertigstellung der Service als Image bezogen werden. Und dann als Container lokal genutzt werden kann.

\
<a name="install"><h3>Installation</h3></a>
:warning: _Die folgende Installation ist noch nicht verfügbar. Der Port und ähnliches können sich noch ändern._ 

Die Installation und Ausführung des Containers erfolgt über den Befehl:
```
docker run -p 3000:3000 felixgi1516/geosoft2_ndvi_process
````

\
<a name="use"><h3>Anwendung</h3></a>


#### Zentrale Funktionalität

The monthly mean NDVI calculations are triggered via the central method 'start', which takes 2 parameters:

`data` A datacube in netCDF format containing all available Sentinel2-data of one month. The datacube must have the dimensions 'lon', 'lat' and 'time' and the data variables 'nir' and 'red'.

`bb_EPSG4326` A bounding box with four values in EPSG:4326 : [min Longitude, min Latitude, max Longitude, max Latitude]. For example [7, 51.5, 8, 52.2] for an area containing the city of Münster. This parameter is optional. If this parameter isn't specified the mean will be calculated over the whole spatial dimension of the dataset.

First, the monthly mean-value of all red and all nir values is calculated seperately. After that, the calculated red and nir values are inserted in the following NDVI-formula: (nir - red) / (nir + red). For doing so, calculations can be executed by using dask optionally. 


![NDVI June 2020 Münster](./images/NDVI_June_2020.svg)

#### API Endpunkte
Der Microservice soll über Endpoints aufrufbar sein, leider sind noch keine verfügbar.

:bangbang: Endpoints anlegen und hier dokumentieren

\
<a name="annex"><h3>Anhang</h3></a>


#### Verwendete Software
Software | Version
------ | ------
Flask | 1.1.2
requests | 2.25.0
flask_cors | 3.0.9
xarray | 0.16.2
dask[complete] | 2020.12.0
distributed | 2020.12.0
numpy | 1.19.2
netcdf4 | 1.5.4
pyproj | 2.6.1
numpy | 1.19.2
