import tkinter as tk
from tkinter import messagebox

def show_popup(message):
    """Show a popup error window and stop execution."""
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    messagebox.showerror("EnvEye Error", message)
    root.destroy()
    raise SystemExit  # Stop the notebook cell right after popup

def error_handling(desired_product, geometry_type, desired_temporal_reolution, geometry, target_param):

  if desired_product not in ['ERA5', 'CHIRPS']:
      show_popup('EnvEye currently supports only ERA5 and CHIRPS products. We do not currently your desired prodcut...')
      raise SystemExit

  if geometry_type not in ['polygon', 'point']:
      show_popup('EnvEye currently supports only point and polygon geometries. We do not currently your desired geometry...')
      raise SystemExit

  if target_param == 'T':
    get_param = 'skin_temperature'
  elif target_param == 'P':
    if desired_product == 'ERA5':
      get_param = 'total_precipitation_sum'
    elif desired_product == 'CHIRPS':
      get_param = 'precipitation'
    else:
      show_popup('EnvEye currently supports only ERA5 and CHIRPS products. We do not currently support your desired prodcut...')
      raise SystemExit
  elif target_param == 'Ev':
    get_param = 'total_evaporation_sum'
  else:
    show_popup('EnvEye currently supports only T (temperature), P (precipitation), and Ev (Evapotranspiration). We do not currently support your desired variable...')
    raise SystemExit

  if desired_product == 'ERA5':
    scale = 11132 # in meters
  elif desired_product == 'CHIRPS':
    scale = 5566 # in meters

  if desired_temporal_reolution not in ['day', 'month', 'year']:
    show_popup('EnvEye currently supports only daily, monthly, and yearly frequencies. We do not currently support your desired frequency...')
    raise SystemExit


  if desired_temporal_reolution == 'day' and desired_product == 'ERA5':
    collection_id = "ECMWF/ERA5_LAND/DAILY_AGGR"
  elif desired_temporal_reolution == 'month' and desired_product == 'ERA5':
    collection_id = "ECMWF/ERA5_LAND/MONTHLY_AGGR"
  elif desired_temporal_reolution == 'year' and desired_product == 'ERA5': # there is no yearly product so it uses monthly data
    collection_id = "ECMWF/ERA5_LAND/MONTHLY_AGGR"
  elif desired_product == 'CHIRPS' and target_param=='P':
    collection_id = 'UCSB-CHG/CHIRPS/DAILY'
  else:
    show_popup('EnvEye could not find a supported product based on your variable and temporal frequancy... Please check the software documentation again')
    raise SystemExit
  
  bounds = geometry.bounds().coordinates().get(0).getInfo()
  lats = [coord[1] for coord in bounds]
  min_lat, max_lat = min(lats), max(lats)

  if min_lat < -50 or max_lat > 50 and desired_product == 'CHIRPS':
      show_popup("CHIRPS only covers latitudes between 50°S and 50°N.\n"
                  "Your selected geometry falls outside this range.")
      raise SystemExit
  
  return get_param, scale, collection_id