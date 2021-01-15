import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 
#import ndvi

from ndvi import calculate, prepareData, calculate_with_dask
import xarray as xr
import os
import pytest


def test_calculate():
    '''nominator is zero'''
    assert all(calculate(xr.DataArray([[1, 2]]), xr.DataArray([[1, 2]])) == xr.DataArray([[0.0, 0.0]]))

    '''NC-file sucessfully created '''
    calculate(xr.DataArray([[1, 2]]), xr.DataArray([[1, 2]]), "calculatedNDVI.nc")
    assert os.path.exists("calculatedNDVI.nc")

    '''negative denominator'''
    assert all(calculate(xr.DataArray([[-2, -2]]), xr.DataArray([[1, 1]])) == xr.DataArray([[-3.0, -3.0]]))

    '''calculation with regular values'''
    assert all(calculate(xr.DataArray([[4, 2]]), xr.DataArray([[1, 3]])) == xr.DataArray([[-0.6, 0.2]]))

    '''no bands in input (no data available in timeframe)'''
    with pytest.raises(ValueError):
        calculate(xr.DataArray([]), xr.DataArray([]))


fname = r"..\Datacube\Datadatacube_2020-06-01_T32UMC_R20.nc"

def test_prepareData():
    '''test for valid return'''
    assert type(prepareData(fname)) is not None

def test_calculate_with_dask():
    '''test for valid return'''
    assert calculate_with_dask(xr.DataArray([[1,2]]),xr.DataArray([[1,2]])) is not None
