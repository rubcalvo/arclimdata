## arclim data

arclim data is a simple tool to download, extract and use arclim databases



### installation

arclimdata should be used in a conda env with the following libraries installed: pandas, xarray, rioxarray, rasterio, numpy, requests, tqdm, zipfile

You can create a new conda env with this: `conda create -n arclimdata xarray rioxarray rasterio requests tqdm zipfile -c conda-forge`

Then, clone this repo using `git clone https://github.com/rubcalvo/arclimdata.git`. 

### description

#### Class: ArclimData

A class to manage downloading, extracting, and loading climate data from the Arclim database.

##### Attributes:
- `working_dir` (str): The directory where the data will be downloaded and extracted.
- `climate_indices` (pd.DataFrame): DataFrame containing climate indices information.

#### Methods

##### `__init__(self, working_dir)`
Initializes the ArclimData object with a working directory and loads the climate indices.

**Args:**
- `working_dir` (str): The directory where the data will be downloaded and extracted.

##### `decompress_zip(self, zip_path, extract_to)`
Decompresses a single ZIP file.

**Args:**
- `zip_path` (str): The path to the ZIP file.
- `extract_to` (str): The directory to extract files to.

**Returns:**
- `None`

##### `download_climate_data(self)`
Downloads and extracts the Arclim climate data ZIP file to the working directory.

**Returns:**
- `None`

##### `load_climate_indice(self, name, period, months, format)`
Loads a specific climate index as an xarray object.

**Args:**
- `name` (str): The name of the climate index, must be one of the "Código" in `self.climate_indices`.
- `period` (str): The period of the data, must be one of 'present' (1971-2010), 'future' (2035-2065), or 'delta' (difference between future and present).
- `months` (str): The months or period of interest, must be one of 'jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'ago', 'sep', 'oct', 'nov', 'dec', 'djf', 'mam', 'jja', 'son', 'summer', 'winter', 'annual'.
- `format` (str): The format of the returned object, currently supports 'xarray'.

**Returns:**
- `xarray.DataArray`: The loaded climate index data as an xarray object.

**Raises:**
- `AssertionError`: If the name, period, or months arguments are not valid.


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
