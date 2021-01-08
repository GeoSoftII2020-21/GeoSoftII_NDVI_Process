from NDVI import calculate, prepareData, calculate_with_dask
import xarray as xr
import os
#import ipytest
import pytest


def test_calculate():
    '''nominator is zero'''
    assert all(calculate(xr.DataArray([[1, 2]]), xr.DataArray([[1, 2]])) == xr.DataArray([[0.0, 0.0]]))

    #'''NC-file sucessfully created '''
    calculate(xr.DataArray([[1, 2]]), xr.DataArray([[1, 2]]), "calculatedNDVI.nc")
    assert os.path.exists("calculatedNDVI.nc")

    #'''negative denominator'''
    assert all(calculate(xr.DataArray([[-2, -2]]), xr.DataArray([[1, 1]])) == xr.DataArray([[-3.0, -3.0]]))

    #'''calculation with regular values'''
    assert all(calculate(xr.DataArray([[4, 2]]), xr.DataArray([[1, 3]])) == xr.DataArray([[-0.6, 0.2]]))

    #'''no bands in input (no data available in timeframe)'''
    with pytest.raises(ValueError):
        calculate(xr.DataArray([]), xr.DataArray([]))

def test_preapareData():
    '''test for valid return'''
    assert type(prepareData(r"C:\Users\Magdalena\Documents\WWU\geosoft2\NDVI\Datacube\Datadatacube_2020-06-01_T32UMC_R20.nc")) is not None


def test_preapareData():
    '''test for valid return'''
    assert calculate_with_dask(xr.DataArray([[1,2]]),xr.DataArray([[1,2]])) is None
