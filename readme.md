# GeoSoftII_NDVI_Process
### Geosoftware II Project WiSe 2020/21
---

## Table of contents
[1. Overview](#overview) \
[2. Installation](#install) \
[3. Scope of functionalities](#functionalities)  \
[4. Examples of use](#use) \
[5. Appendix](#annex)

\
<a name="overview"><h3>Overview</h3></a>
This project is a part for a new [openEO](https://openeo.org/) backend driver working with [Pangeo Software Stack](https://pangeo.io/).

The goal is to examine the datacubes provided by the [Dataserver](https://github.com/GeoSoftII2020-21/GeoSoftII_DataServer) for the NDVI.
In doing so, the user story: "Sentinel2 Datensatz um Münster auf NDVI untersuchen" of the requirements specification is implemented.

In addition, there is a [Docker Repository](https://hub.docker.com/repository/docker/felixgi1516/geosoft2_ndvi_process), which is linked to this and from which the service can be obtained as an image after completion. And then is used locally as a container.

\
<a name="install"><h3>Installation</h3></a>
The installation and execution is possible exclusively provided within the framework of the *[docker-compose.yml](https://github.com/GeoSoftII2020-21/GeoSoftII_Projekt/blob/Docker-compose/docker-compose.yml)*.
```docker
docker-compose up
```
\
<a name="use"><h3>Scope of functionalities</h3></a>
The monthly mean NDVI calculations are triggered via the central method 'start', which takes 2 parameters:

`data` A datacube in netCDF format containing all available Sentinel2-data of one month. The datacube must have the dimensions 'lon', 'lat' and 'time' and the data variables 'nir' and 'red'.

`bb_EPSG4326` A bounding box with four values in EPSG:4326 : [min Longitude, min Latitude, max Longitude, max Latitude]. For example [7, 51.5, 8, 52.2] for an area containing the city of Münster. This parameter is optional. If this parameter isn't specified the mean will be calculated over the whole spatial dimension of the dataset.

First, the monthly mean-value of all red and all nir values is calculated seperately. After that, the calculated red and nir values are inserted in the following NDVI-formula: (nir - red) / (nir + red). For doing so, calculations can be executed by using dask optionally. 

#### API endpoints

- POST /doJob/{job_id}` Receives a job which is being processed.
- GET /jobstatus` Returns a JSON with the job status.

\
<a name="use"><h3>Examples of use</h3></a>

![NDVI June 2020 Münster](https://github.com/GeoSoftII2020-21/GeoSoftII_NDVI_Process/blob/master/images/NDVI_June_%202020.svg)
(This picture is externally visualized with QGIS and is not an output of the calculation. )

\
<a name="annex"><h3>Appendix</h3></a>

#### Technologies
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
