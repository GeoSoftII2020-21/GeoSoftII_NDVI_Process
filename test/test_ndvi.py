'''
@author Magdalena Fischer <ma9dalen8: m09fischer@gmail.com>
@author Cornelius Zerwas <neli98: cornelius.zerwas@t-online.de>
'''

import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)


from ndvi2 import calculate, prepareData, calculate_with_dask
import xarray as xr
import os
import pytest
import numpy as np



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


def test_prepareData():
    '''test for valid return'''
    assert type(prepareData(data)) is not None

    red, nir, bb = prepareData(data, bb=[7.54167, 51.880772, 7.760397, 52.051578])
    '''tests if the coordinate transformation is correct'''
    assert bb == [[5748782.569931421, 5767500.019963231], [399621.66574785963, 415000.0260141061]]

    '''testing for valid boundingbox type'''
    assert type(bb == 'list')

    '''testing if the transformed red data is in the required numpy.ndarray formate'''
    assert type(red.data == 'numpy.ndarray')

    '''testing if the transformed nir data is in the required numpy.ndarray formate'''
    assert type(nir.data == 'numpy.ndarray')

def test_calculate_with_dask():
    '''test for valid return'''
    assert calculate_with_dask(xr.DataArray([[1,2]]),xr.DataArray([[1,2]])) is not None
