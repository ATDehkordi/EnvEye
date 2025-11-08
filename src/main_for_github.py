import ee
import geemap
import geopandas as gpd
from utils.error_handling import error_handling
from utils.gee import GEE_data_extraction
from utils.plot import plot

################### Login details
service_account = 'example.com' ### provide service mail for GEE
credentials = ee.ServiceAccountCredentials(service_account, 'LoginGEE.json') #### provide LoginGEE json for GEE
ee.Initialize(credentials)


############ Config file

target_param = 'Ev' # 'T' or 'P' or 'Ev'
desired_product = 'ERA5' # 'ERA5' or 'CHIRPS'
geometry_type = 'polygon' #'polygon; or 'point'

# #skane
# geometry = ee.Geometry.Polygon(
#         [[[11.535700421301867, 57.765932013293664],
#           [11.535700421301867, 55.25116340665264],
#           [17.248591046301865, 55.25116340665264],
#           [17.248591046301865, 57.765932013293664]]], None, False);

### From shapefile
# gdf = gpd.read_file('/home/atdehkordi/PHDLund/PythonProjects_github/EnvEye/Sample_shpfiles/TigrisEuphrates/Merged.shp')
gdf = gpd.read_file('/home/atdehkordi/PHDLund/PythonProjects_github/EnvEye/Sample_shpfiles/Nile/Nile_Basin.shp')
geometry = geemap.geopandas_to_ee(gdf)

# a point in urmia
# geometry = ee.Geometry.Point([46.71116186058475, 36.70591114421848])


start = ee.Date('1990-01-01')
end   = ee.Date('2025-01-01')

desired_temporal_reolution = 'month' ### 'day', 'month' or 'year' # there is a date problem with dat and year so recommended to use month

save_csv_path = f'{target_param}_{desired_product}_{geometry_type}_{desired_temporal_reolution}.csv'

########## Process

get_param, scale, collection_id = error_handling(desired_product, geometry_type, desired_temporal_reolution, geometry, target_param)
df = GEE_data_extraction(start, end, desired_temporal_reolution, geometry_type, collection_id, geometry, scale, get_param, target_param, desired_product)
# df.to_csv(save_csv_path, index=False)
plot(df, desired_product, get_param, geometry_type, desired_temporal_reolution)