import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 

from ndvi import calculate, prepareData, calculate_with_dask
import xarray as xr
import os
import pytest
import netCDF4


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


data = xr.Dataset(
    {   "red": (("lat", "lon"),
            20 * np.random.rand(4).reshape(2,2),),
        "nir": (("lat", "lon"), np.random.rand(4).reshape(2,2)),},
    coords={"lat": [10, 20], "lon": [150, 160]},
    )
data = data.expand_dims(time=(['2020,11,23','2020,11,24','2020,11,25','2020,11,26']))

#fname = r"..\Datacube\Datadatacube_2020-06-01_T32UMC_R20.nc"

def test_prepareData():
    '''test for valid return'''
    assert type(prepareData(data)) is not None

def test_calculate_with_dask():
    '''test for valid return'''
    assert calculate_with_dask(xr.DataArray([[1,2]]),xr.DataArray([[1,2]])) is not None
