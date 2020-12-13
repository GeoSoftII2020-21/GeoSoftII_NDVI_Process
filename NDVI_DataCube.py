import xarray
import rasterio as rio


'''define import path and concrete files'''
R60_a = 'S2B_MSIL2A_20200612T064629_N0214_R020_T39NXJ_20200612T110440.SAFE\GRANULE\L2A_T39NXJ_A017063_20200612T070244\IMG_DATA\R60m'
R60_b = 'S2A_MSIL2A_20200613T103031_N0214_R108_T32UMC_20200613T111252.SAFE\GRANULE\L2A_T32UMC_A025988_20200613T103506\IMG_DATA\R60m'
R60_c = 'S2B_MSIL2A_20190605T100039_N0212_R122_T33TTG_20190605T143319.SAFE\GRANULE\L2A_T33TTG_A011731_20190605T100530\IMG_DATA\R60m'
# Open b4 and b8
b4a = rio.open(R60_a + '/T39NXJ_20200612T064629_B04_60m.jp2')
b8a = rio.open(R60_a + '/T39NXJ_20200612T064629_B8A_60m.jp2')


b4b = rio.open(R60_b + '/T32UMC_20200613T103031_B04_60m.jp2')
b8b = rio.open(R60_b + '/T32UMC_20200613T103031_B8A_60m.jp2')

b4c = rio.open(R60_c + '/T33TTG_20190605T100039_B04_60m.jp2')
b8c = rio.open(R60_c + '/T33TTG_20190605T100039_B8A_60m.jp2')

# read Red(b4) and NIR(b8) as arrays
red_a = b4a.read()
nir_a = b8a.read()

red_b = b4b.read()
nir_b = b8b.read()

red_c = b4c.read()
nir_c = b8c.read()


'''convert bands to xarray'''

dataset = xarray.DataArray(data=[[red_a, nir_a],[red_b, nir_b],[red_c, nir_c]])
print(dataset)

'''save as NetCDF'''
dataset.to_netcdf('datacube.nc', 'w', format='NETCDF4')
