import pandas as pd
import ee

def GEE_data_extraction(start, end, desired_temporal_reolution, geometry_type, collection_id, geometry, scale, get_param, target_param, desired_product):

    n_temporal_sections = end.difference(start, desired_temporal_reolution).toInt()  # number of days, months or years
    temporal_section_starts = ee.List.sequence(0, n_temporal_sections.subtract(1)).map(lambda m: start.advance(m, desired_temporal_reolution))


    def sampling_based_on_temporal_resolution(start_date):
        start_date = ee.Date(start_date)
        next_temporal_section = start_date.advance(1, desired_temporal_reolution)  # exclusive end for filterDate

        if geometry_type == 'polygon':

            composite_img = (ee.ImageCollection(collection_id)
                        .filterBounds(geometry)
                        .filterDate(start_date, next_temporal_section)  # [start, next_month)
                        .mean()
                        .clip(geometry))

            value = composite_img.reduceRegion(
            reducer=ee.Reducer.mean(),
            geometry=geometry,
            scale=scale,
            bestEffort=True).get(get_param)  # band name

            # Return a feature with date string and value (mm/day)
            return ee.Feature(None, {
            'date': start_date.format('YYYY-MM'),
            'env_variable': value
            })

        elif geometry_type == 'point':

            value = (ee.ImageCollection(collection_id)
                        .filterBounds(geometry)
                        .filterDate(start_date, next_temporal_section)  # [start, next_month)
                        .mean()).reduceRegion(reducer=ee.Reducer.first(), geometry=geometry, scale=scale,bestEffort=True).get(get_param)

            # Return a feature with date string and value (mm/day)
            return ee.Feature(None, {
            'date': start_date.format('YYYY-MM'),
            'env_variable': value
            })

    fc = ee.FeatureCollection(temporal_section_starts.map(sampling_based_on_temporal_resolution))


    dates  = fc.aggregate_array('date').getInfo()
    values = fc.aggregate_array('env_variable').getInfo()

    # if it is temperature return to Celisius from Kelvin
    if target_param == 'T' and desired_product == 'ERA5':
        values = [x - 273.15 for x in values]
        
    df = pd.DataFrame(data={"date": dates, "env_variable": values})

    return df
