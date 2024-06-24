## arclim data

arclim data is a simple tool to download, extract and use arclim databases



### installation

arclimdata should be used in a conda env with the following libraries installed: pandas, xarray, rioxarray, rasterio, numpy, requests, tqdm, zipfile

You can create a new conda env with this: `conda create -n arclimdata pandas xarray rioxarray rasterio numpy requests tqdm zipfile -c conda-forge`

Then, clone this repo using `git clone https://github.com/rubcalvo/arclimdata.git`. 

### usage

```
import os
os.chdir("/mnt/d/arclim/") # change dir to where arclimdata.py is located
from arclimdata import arclimdata
folder = "/mnt/d/arclim/" # where arclim data will be stored
arclim = arclimdata(working_dir = folder)
arclim.download_climate_data() # download and extract arclim climate indices geotifs
arclim.climate_indices ## returns a pandas dataframe with information about climate indices
arclim.load_climate_indice(name = 'consecutive_days_over_25C', period = 'future', months = 'annual', format = 'xarray') # return a specific climate index as an xarray object.
```
