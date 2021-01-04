import xarray as xr
import dask

def prepareData(fname):
    
    data = xr.open_dataset(fname)
    #print(data)
    red = data.red #'''should contain all available red's (from the same Tile)in one xarray'''
    #print(red)
    nir = data.nir #'''should contain all available nir's (from the same Tile) in one xarray'''
    #print(nir)
    
    # TODO filter data
    
    return red, nir
	
def calculate(red, nir, fname_output=None, sumNir=None, sumRed=None):
    
    if len(red) == 0 or len(nir) == 0:
        raise ValueError ('red or nir is empty')
        
    i = 1
    if sumRed is None:
        sumRed = red[0]
        
    if sumNir is None:    
        sumNir = nir[0]
        
    
        
    while i < len(red):
        #summerize all reds and nirs
        sumRed = sumRed + red[i]

        sumNir = sumNir+nir[i]

        i += 1

    
    #monthly mean
    sumRed = sumRed/len(red)
    sumNir = sumNir/len(nir)


    #Calculate ndvi
    denominator = (sumNir+sumRed).astype(float) 
    #assert (denominator != 0).all(), 'Denominator is 0'

    ndvi = (sumNir.astype(float)-sumRed.astype(float))/denominator
    print(type(ndvi))
    
    if fname_output is not None:
        # save calculated NDVI as NetCDF
        ndvi = ndvi.to_netcdf(path=fname_output)
        
    
    print(ndvi)
    return ndvi
	
def calculate_with_dask(red, nir, fname_output):
    sumRed = dask.delayed(red[0])
    sumNir = dask.delayed(nir[0])
    ndvi = calculate(red, nir,fname_output, sumNir, sumRed)
    ndvi.compute()