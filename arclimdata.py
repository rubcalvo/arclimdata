import xarray as xr
import rioxarray as rioxr
import requests
from tqdm import tqdm
import os
import zipfile
import pandas as pd


class arclimdata:
    """
    A class to manage downloading, extracting, and loading climate data from the Arclim database.

    Attributes:
    working_dir (str): The directory where the data will be downloaded and extracted.
    climate_indices (pd.DataFrame): DataFrame containing climate indices information.
    """

    def __init__(self, working_dir):
        """
        Initializes the ArclimData object with a working directory and loads the climate indices.

        Args:
        working_dir (str): The directory where the data will be downloaded and extracted.
        """
        self.working_dir = working_dir
        self.climate_indices = pd.read_csv(f"{working_dir}arclim_climate_indices.csv")

    def decompress_zip(self, zip_path, extract_to):
        """
        Decompresses a single ZIP file.

        Args:
        zip_path (str): The path to the ZIP file.
        extract_to (str): The directory to extract files to.

        Returns:
        None
        """
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(extract_to)
            print(f"Extracted {zip_path} to {extract_to}")

    def download_climate_data(self):
        """
        Downloads and extracts the Arclim climate data ZIP file to the working directory.

        Returns:
        None
        """

        url = "https://arclim.mma.gob.cl/media/ClimateIndex/geotiff/IndicesClimaticosARCLIM.zip"  # Replace with your file URL
        local_filename = f"{self.working_dir}/IndicesClimaticosARCLIM.zip"  # Replace with your desired local file name
        print(f"Downloading Arclim Climate Database")
        with requests.get(url, stream=True) as response:
            response.raise_for_status()
            total_size = int(response.headers.get("content-length", 0))
            block_size = 8192

            with open(local_filename, "wb") as file, tqdm(
                total=total_size, unit="iB", unit_scale=True
            ) as progress_bar:
                for chunk in response.iter_content(chunk_size=block_size):
                    file.write(chunk)
                    progress_bar.update(len(chunk))

        print(f"Downloaded {local_filename}")

        print("Extracting files")
        zip_files_directory = f"{self.working_dir}/IndicesClimaticosARCLIM/"
        extracted_files_directory = f"{self.working_dir}/IndicesClimaticosARCLIM/"

        # Ensure the extraction directory exists
        os.makedirs(extracted_files_directory, exist_ok=True)
        self.decompress_zip(
            f"{folder}/IndicesClimaticosARCLIM.zip",
            f"{folder}/IndicesClimaticosARCLIM/",
        )
        # Define the directory containing the ZIP files and the directory to extract to

        # Iterate over each ZIP file in the directory and decompress it
        for filename in os.listdir(zip_files_directory):
            if filename.endswith(".zip"):
                zip_path = os.path.join(zip_files_directory, filename)
                self.decompress_zip(zip_path, extracted_files_directory)

    def load_climate_indice(self, name, period, months, format):
        """
        Loads a specific climate index as an xarray object.

        Args:
        name (str): The name of the climate index, must be one of the "Código" in self.climate_indices.
        period (str): The period of the data, must be one of 'present' (1971-2010), 'future' (2035-2065), or 'delta' (difference between future and present).
        months (str): The months or period of interest, must be one of 'jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'ago', 'sep', 'oct', 'nov', 'dec', 'djf', 'mam', 'jja', 'son', 'summer', 'winter', 'annual'.
        format (str): The format of the returned object, currently supports 'xarray'.

        Returns:
        xarray.DataArray: The loaded climate index data as an xarray object.

        Raises:
        AssertionError: If the name, period, or months arguments are not valid.

        """
        if format == "xarray":

            assert name in list(
                self.climate_indices["Código"]
            ), f"{name} is not of ARCLIM Climate Indices. Check self.climate_indices DataFrame."
            assert period in [
                "future",
                "present",
                "delta",
            ], f"period should be one of 'future', 'present' or 'delta'"
            assert months in [
                "jan",
                "feb",
                "mar",
                "apr",
                "may",
                "jan",
                "jul",
                "ago",
                "sep",
                "oct",
                "nov",
                "dec",
                "djf",
                "mam",
                "jja",
                "son",
                "summer",
                "winter",
                "annual",
            ], f"months should be one of 'jan', 'feb', 'mar', 'apr', 'may', 'jan', 'jul', 'ago', 'sep', 'oct', 'nov', 'dec', 'djf', 'mam', 'jja', 'son', 'summer', 'winter' or 'annual'"

            ds = rioxr.open_rasterio(
                f"{self.working_dir}/IndicesClimaticosARCLIM/{name}/{name}_{period}_{months}_latlon.tif"
            )

            return ds