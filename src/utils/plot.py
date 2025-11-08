import matplotlib.pyplot as plt
import pandas as pd

def plot(df, desired_product, get_param, geometry_type, desired_temporal_reolution):
    df['date'] = pd.to_datetime(df['date'], format='%Y-%m')

    plt.figure(figsize=(15,6))
    plt.plot(df['date'], df['env_variable'], label=f'{get_param}', linewidth=1.8)

    plt.title(f'Average {desired_temporal_reolution}ly of {get_param} from {desired_product} over {geometry_type}')
    plt.xlabel('Date')

    if desired_product == 'CHIRPS' and get_param == 'precipitation':
        unit = 'mm/day'
    elif desired_product == 'ERA5' and get_param == 'skin_temperature':
        unit = 'C'
    elif desired_product == 'ERA5' and get_param == 'total_precipitation_sum':
        unit = 'meters'
    elif desired_product == 'ERA5' and get_param == 'total_evaporation_sum':
        unit = 'meter of water equiavalent'
    else:
        unit = '**** Unknown'

    plt.ylabel(f'{get_param} in [{unit}]')
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.legend()
    plt.tight_layout()
    plt.show()