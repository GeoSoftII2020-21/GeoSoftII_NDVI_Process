import os
import xarray as xr
import dask
from dask.distributed import Client, LocalCluster

# cluster= LocalCluster()
# client = Client (cluster)
# client


FNAME_DATACUBE = "Datacube\Datadatacube_2020-06-01_T32UMC_R20.nc"
FNAME_OUTPUT = "calculatedNDVI.nc"


def prepareData(fname):
    '''
    Opens data cube and stores all available red and nir bands that are available for a given time horizon.
    Parameter:
    fname : path of data cube
    Return:
    red: includes all red bands of the given time horizon
    nir: includes all nir bands of the given time horizon
    '''

    data = xr.open_dataset(fname)
    '''should contain all available red's (from the same Tile)in one xarray'''
    red = data.red

    '''should contain all available nir's (from the same Tile) in one xarray'''
    nir = data.nir

    # TODO filter data

    return red, nir


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
        # summerize all reds and nirs
        sumRed = sumRed + red[i]

        sumNir = sumNir + nir[i]

        i += 1

    '''calculation of mean value of red and nir values'''
    sumRed = sumRed / len(red)
    sumNir = sumNir / len(nir)

    '''calculation of NDVI'''
    ndvi = (sumNir.astype(float) - sumRed.astype(float)) / (sumNir + sumRed).astype(float)

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
    '''

    '''initialize sumRed and sumNir as dask objects'''
    sumRed = dask.delayed(red[0])
    sumNir = dask.delayed(nir[0])

    '''execution of calculate function'''
    ndvi = calculate(red, nir, fname_output, sumNir, sumRed)

    '''distribution of exercises to available workers '''
    ndvi.compute()
    ndvi_xarray = xr.DataArray()

    '''load ndvi dataset, transformation to xarray'''
    if fname_output is not None:
        ndvi_xarray = xr.open_dataset(fname_output)
        print(type(ndvi_xarray))
    return ndvi_xarray


def start(data):
    red, nir = prepareData(FNAME_DATACUBE)
    calculate_with_dask(red, nir, FNAME_OUTPUT)
    # calculate(red,nir, FNAME_OUTPUT)
    '''remove local file'''
    os.remove(FNAME_OUTPUT)


'''start(data=0)'''
