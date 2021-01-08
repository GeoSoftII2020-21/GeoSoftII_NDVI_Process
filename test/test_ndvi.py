#!/usr/bin/env python
# coding: utf-8

# In[1]:


#import ipytest
import pytest
#import import_ipynb


# In[2]:


get_ipython().run_line_magic('load_ext', 'ipython_pytest')


# In[3]:


get_ipython().run_cell_magic('pytest', '', '\nfrom ndvi import calculate\nimport xarray as xr\nimport os\nimport ipytest\nimport pytest\n\n\ndef test_calculate():\n    \'\'\'nominator is zero\'\'\'\n    assert all(calculate(xr.DataArray([[1,2]]),xr.DataArray([[1,2]])) == xr.DataArray([[0.0,0.0]]))\n    \n    \'\'\'NC-file sucessfully created \'\'\'\n    calculate(xr.DataArray([[1,2]]),xr.DataArray([[1,2]]), "calculatedNDVI.nc") \n    assert os.path.exists("calculatedNDVI.nc")\n    \n    \'\'\'negative denominator\'\'\'\n    assert all(calculate(xr.DataArray([[-2,-2]]),xr.DataArray([[1,1]])) == xr.DataArray([[-3.0,-3.0]]))\n    \n    \'\'\'calculation with regular values\'\'\'\n    assert all(calculate(xr.DataArray([[4,2]]),xr.DataArray([[1,3]])) == xr.DataArray([[-0.6,0.2]]))\n    \n    \'\'\'no bands in input (no data available in timeframe)\'\'\'\n    with pytest.raises(ValueError):\n        calculate(xr.DataArray([]),xr.DataArray([]))')


# In[4]:


get_ipython().run_cell_magic('pytest', '', '\nfrom ndvi import prepareData\nimport xarray as xr\nimport os\nimport ipytest\nimport pytest\n\n\ndef test_preapareData():\n    \'\'\'test for valid return\'\'\'\n    assert type(prepareData(r"C:\\Users\\Magdalena\\Documents\\WWU\\geosoft2\\NDVI\\Datacube\\Datadatacube_2020-06-01_T32UMC_R20.nc")) is not None')


# In[5]:


get_ipython().run_cell_magic('pytest', '', "\nfrom ndvi import calculate_with_dask\nimport xarray as xr\nimport os\nimport ipytest\nimport pytest\n\n\ndef test_preapareData():\n    '''test for valid return'''\n    assert calculate_with_dask(xr.DataArray([[1,2]]),xr.DataArray([[1,2]])) is None")


# In[ ]:




