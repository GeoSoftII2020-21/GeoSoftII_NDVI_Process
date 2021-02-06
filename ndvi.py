'''
@author Magdalena Fischer <ma9dalen8: m09fischer@gmail.com>
@author Cornelius Zerwas <neli98: cornelius.zerwas@t-online.de>
'''
import os
import xarray as xr
import dask
from dask import distributed
import numpy as np
import pyproj



FNAME_DATACUBE = "Datacube\cube\datacube_2020-06-01_Merged_R100.nc"
FNAME_OUTPUT = "calculatedNDVI.nc"
''' bb_EPSG32632 = [399621.66574785963,5748782.569931421, 415000.0260141061, 5767500.019963231] leftlong,bottomlat,rightlong,toplat, EPSG:32632'''
bb_EPSG4326=[7.54167,51.880772,7.760397,52.051578]

def prepareData(data, bb = [-999,-999,-999,-999]):
    '''
    selects the data that lays within the bounding box of all available red and nir bands. Converts the input bounding box to required coordinate system.
    Parameter:
    data : input datacube (filtered by time)
    bb: containig the coordinates for the area of interest (EPSG:4326)
    Return:
    red: includes all red bands of the given time horizon within the given bounding box
    nir: includes all nir bands of the given time horizon within the given bounding box
    bb: includes the bounding box with the converted coordinates
    '''

    '''should contain all available reds (from the same Tile) in one xarray'''
    red = data.red
    '''should contain all available nirs (from the same Tile) in one xarray'''
    nir = data.nir
    '''should contain all available latitudes (from the same Tile) in one xarray'''
    lat = data.lat
    '''should contain all available longitudes (from the same Tile) in one xarray'''
    lon = data.lon


    if bb != [-999,-999,-999,-999]:
        '''transfomation from epsg 4326 to epsg 32632'''
        bblat=[bb[1]]
        bblon=[bb[0]]
        bblat.append(bb[3])
        bblon.append(bb[2])

        epsg4326 = pyproj.Proj(init = "epsg:4326")
        epsg32632 = pyproj.Proj(init = "epsg:32632")
        bblon, bblat =pyproj.transform(epsg4326, epsg32632, bblon, bblat)
        bb = [bblat,bblon]

        '''creating boolean mask depending on the given area'''
        latlon_mask = np.logical_not((lat <= bblat[0]) | (lat >= bblat[1]) | (lon <= bblon[0]) | (lon >= bblon[1]))

        '''mapping the mask on the values'''
        nir = nir.where(latlon_mask)
        red = red.where(latlon_mask)
        #print(nir.values)
        print(bb)

    return red, nir, bb


def calculate(red, nir, fname_output=None, sumNir=None, sumRed=None):
    '''
    Calculates NDVI values based on the injected red and nir values. Therefore, the function computes an average of the red and nir values and executes the calculation for this average.
    The result is saved as a NetCDF-File.
    Parameter:
    red : array of all available red bands
    nir : array of all available nir bands
    fname_output : datacube of calculated NDVI (optional)
    sumNir : sum of all nir bands of the given time horizon (optional. If a value (deviating from None) is passed, dask is used for calculation)
    sumRed : sum of all red bands of the given time horizon (optional. If a value (deviating from None) is passed, dask is used for calculation)
    Return:
    ndvi: array with computed NDVI-values
    '''

    '''checks if data input is complete'''
    if len(red) == 0 or len(nir) == 0:
        raise ValueError('red or nir is empty')

    '''prepares sumRed and sumNir variable for further calculations based on whether these are defined initially '''
    if sumRed is None:
        sumRed = red[0]
        
    if sumNir is None:    
        sumNir = nir[0]

    '''iteration through all red and nir bands to summarize them. All red and all nir bands are added separately.'''
    i = 1
    while i < len(red):
        '''summarize all reds and nirs'''
        sumRed = sumRed + red[i]
        sumNir = sumNir + nir[i]

        i += 1
    
    '''calculation of mean value of red and nir values'''
    sumRed = sumRed/len(red)
    sumNir = sumNir/len(nir)

    '''calculation of NDVI'''
    ndvi = (sumNir.astype(float)-sumRed.astype(float))/(sumNir+sumRed).astype(float)

    '''saving of NDVI calculations if path is inserted'''
    if fname_output is not None:
        ndvi = ndvi.to_netcdf(path=fname_output)

    return ndvi

	
def calculate_with_dask(red, nir, fname_output=None):
    '''
    Prepares NDVI calculation to be executed with dask.
    Parameter:
    red : array of all available red bands
    nir : array of all available nir bands
    fname_output : datacube of calculated NDVI (optional)
    Return:
    ndvi_xarray: calculated ndvi (xarray Dataset)
    '''

    '''create dask Cluster'''
    distributed.Client()

    '''initialize sumRed and sumNir as dask objects'''
    sumRed = dask.delayed(red[0])
    sumNir = dask.delayed(nir[0])

    '''execution of calculate function'''
    ndvi = calculate(red, nir, fname_output, sumNir, sumRed)

    '''distribution of exercises to available workers '''
    ndvi.compute()

    return ndvi


def start(data, bb_EPSG4326):
    '''
    for execution of the process
    Parameter:
    data: xarray containing sentinel-2 data (already filtered (time and boundingbox) and merged)
    Return:
    output: calculated ndvi (xarray.Dataset)
    '''

    red, nir, bb = prepareData(data,bb_EPSG4326)
    calculate_with_dask(red, nir, FNAME_OUTPUT)
    #calculate(red,nir, FNAME_OUTPUT)

    '''reload calculated NDVI as xarray'''
    result = xr.open_dataset(FNAME_OUTPUT)
    result.close()

    '''remove local file'''
    os.remove(FNAME_OUTPUT)

    return result


if __name__ == '__main__':
    data = xr.open_dataset(FNAME_DATACUBE, chunks={"time": "auto"})

    '''execute start function'''
    start(data, bb_EPSG4326)
