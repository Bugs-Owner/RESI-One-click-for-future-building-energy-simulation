from Google_Drive import get_epw_file_from_drive
from Google_Drive import search_file_by_name
from ast import literal_eval
import requests
import numpy as np
import pandas as pd
import csv
import io


def MAE(Overall, candi):
    return sum(abs(candi-Overall))
def EY(Overall, candi):
    return sum((candi-Overall))

class weather():
    def __init__(self):
        self.api_key='AIzaSyC8RJ9K1h-fZrMDvt_CO83Tw41URWLL4CU'

    def get_input(self, city_name, span):
        self.city_name = city_name
        self.span = span

    def get_geocode(self):
        base_url = "https://maps.googleapis.com/maps/api/geocode/json"
        api_key = self.api_key
        params = {
            "address": self.city_name,
            "key": api_key
        }
        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            result = response.json()
            if result["status"] == "OK":
                self.latitude = result["results"][0]["geometry"]["location"]["lat"]
                self.longitude = (result["results"][0]["geometry"]["location"]["lng"])*(-1)
            else:
                return "Error: API request unsuccessful. Please change your api_key"
        else:
            return "Error: API request unsuccessful. Please change your api_key"

    def get_threshold(self):
        if self.span == 'Mid-term':
            self.yearrange = np.arange(2045, 2055)
            self.monthrange = pd.date_range(start='1/1/2054', end='1/1/2055', freq='MS')
        if self.span == 'Long-term':
            self.yearrange = np.arange(2085, 2095)
            self.monthrange = pd.date_range(start='1/1/2094', end='1/1/2095', freq='MS')


    def get_file_name(self):
        threshold_multiplier = 0  # Start with the initial threshold
        found = False  # Flag to indicate whether a file name has been found
        while not found:
            file_name = {}
            for year in self.yearrange:
                year_min = year
                year_max = year
                lat_min = self.latitude - 0.05 - threshold_multiplier
                lat_max = self.latitude + 0.05 + threshold_multiplier
                long_min = self.longitude - 0.05 - threshold_multiplier
                long_max = self.longitude + 0.05 + threshold_multiplier

                with open('weather.txt', 'r') as f:
                    filelist = [list(literal_eval(line)) for line in f]
                    for file in filelist[0][1:]:
                        Fileyear = int(file.split('_')[2])
                        Filelat = float(file.split('_')[3].split('lat')[1])
                        Filelong = float(file.split('_')[4].split('long')[1].split('epw')[0][:-1]) * -1
                        if year_min <= Fileyear <= year_max \
                                and lat_min <= Filelat <= lat_max \
                                and long_min <= Filelong <= long_max:
                            file_name[year] = file
                            found = True  # Set found to True if any file matches the criteria

            if not file_name:  # If no file is found, increase the threshold
                threshold_multiplier += 0.03  # Increase the threshold by 0.03 each time
            else:
                self.file_name = file_name
                return  # Exit the function once a file is found

        if not self.file_name:
            print("No file found.")

    def connect(self, service):
        self.service = service

    def read_epw_temperature(self):
        temperatures = []
        epw_file_io = get_epw_file_from_drive(service=self.service, file_id=self.file_id)
        with epw_file_io as file:
            reader = csv.reader(io.StringIO(file.read().decode('utf-8')), delimiter=',')
            # Skip the EPW header lines
            for _ in range(8):
                next(reader)
            for row in reader:
                # The dry bulb temperature is the seventh column (index 6)
                temp = float(row[6])
                temperatures.append(temp)
        return temperatures

    def read_epw_to_dataframe(self):
        column_names = [
            "Year", "Month", "Day", "Hour", "Minute", "Data Source and Uncertainty Flags",
            "Dry Bulb Temperature", "Dew Point Temperature", "Relative Humidity",
            "Atmospheric Station Pressure", "Extraterrestrial Horizontal Radiation",
            "Extraterrestrial Direct Normal Radiation", "Horizontal Infrared Radiation Intensity",
            "Global Horizontal Radiation", "Direct Normal Radiation", "Diffuse Horizontal Radiation",
            "Global Horizontal Illuminance", "Direct Normal Illuminance", "Diffuse Horizontal Illuminance",
            "Zenith Luminance", "Wind Direction", "Wind Speed", "Total Sky Cover",
            "Opaque Sky Cover", "Visibility", "Ceiling Height", "Present Weather Observation",
            "Present Weather Codes", "Precipitable Water", "Aerosol Optical Depth", "Snow Depth",
            "Days Since Last Snowfall", "Albedo", "Liquid Precipitation Depth",
            "Liquid Precipitation Quantity"
        ]
        # Read the content from the BytesIO object
        epw_file_io = get_epw_file_from_drive(service=self.service, file_id=self.file_id)
        content = epw_file_io.read().decode('utf-8')
        lines = content.splitlines()
        data = [line.split(',') for line in lines[8:]]  # Skipping header lines
        df = pd.DataFrame(data, columns=column_names)

        # Convert columns to numeric where applicable
        numeric_columns = [col for col in column_names if
                           col not in ["Data Source and Uncertainty Flags", "Present Weather Observation",
                                       "Present Weather Codes"]]

        df[numeric_columns] = df[numeric_columns].apply(pd.to_numeric, errors='coerce')

        return df

    def get_drive_data(self):
        temperatures, epw, raw_io = {}, {}, {}
        for year, filename in self.file_name.items():
            filename=filename[7:]
            self.file_id = search_file_by_name(self.service, filename, "1uf_2XTW8_eXxx-hnK6IoyZyHwWxwtBbA")
            raw_io[year] = get_epw_file_from_drive(service=self.service, file_id=self.file_id)
            temperatures[year] = self.read_epw_temperature()
            epw[year] = self.read_epw_to_dataframe()
        self.raw_io=raw_io
        Tempdf = pd.DataFrame.from_dict(temperatures)
        time_range = pd.date_range(start="{}-01-01".format(self.yearrange[-1]), end="{}-01-01".format(self.yearrange[-1] + 1), freq='H')[:-1]
        Tempdf.index = time_range

        TMY_file, EWY_file, ECY_file = {}, {}, {}
        for m in range(12):
            Mon = (self.monthrange[m] <= Tempdf.index) & (Tempdf.index < self.monthrange[m + 1])
            Tar = Tempdf.loc[Mon].to_numpy()
            Overall = np.zeros(99)
            for percentile in range(1, 100):
                Overall[percentile - 1] = np.percentile(Tar, percentile)
            MAElist, EYlist = [], []
            for candidate in range(10):
                eachmonth = Tar[:, [candidate]]
                candi = np.zeros(99)
                for percentile in range(1, 100):
                    candi[percentile - 1] = np.percentile(eachmonth, percentile)
                MAElist.append(MAE(Overall, candi))
                EYlist.append(EY(Overall, candi))
            TMYidx = pd.Series(MAElist).idxmin()
            EWYidx = pd.Series(EYlist).idxmax()
            ECYidx = pd.Series(EYlist).idxmin()
            TMY_file[m] = Tempdf.loc[Mon].columns[TMYidx]
            EWY_file[m] = Tempdf.loc[Mon].columns[EWYidx]
            ECY_file[m] = Tempdf.loc[Mon].columns[ECYidx]

        self.TMY_file = TMY_file
        self.EWY_file = EWY_file
        self.ECY_file = ECY_file
        self.epw = epw

    def get_extreme_wea(self):
        TMY_epw, EWY_epw, ECY_epw, all_epw = pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame()
        for key, value in self.TMY_file.items():
            mon_q = key + 1
            TMY_epw = pd.concat([TMY_epw, self.epw[value].query("Month==@mon_q")])
        for key, value in self.EWY_file.items():
            mon_q = key + 1
            EWY_epw = pd.concat([EWY_epw, self.epw[value].query("Month==@mon_q")])
        for key, value in self.ECY_file.items():
            mon_q = key + 1
            ECY_epw = pd.concat([ECY_epw, self.epw[value].query("Month==@mon_q")])
        for key, value in self.epw.items():
            epw_ = value
            if key % 4 != 0:
                epw_.index = pd.date_range(start="{}-01-01".format(key), end="{}-01-01".format(key + 1), freq='H')[:-1]
            if key % 4 == 0:
                epw_.index = pd.date_range(start="{}-01-01".format(key + 1), end="{}-01-01".format(key + 2), freq='H')[
                             :-1] - pd.DateOffset(years=1)
            all_epw = pd.concat([all_epw, epw_])

        self.TMY_df = TMY_epw
        self.EWY_df = EWY_epw
        self.ECY_df = ECY_epw
        self.All_df = all_epw

        data_dict = {
            "TMY_df": TMY_epw,
            "EWY_df": EWY_epw,
            "ECY_df": ECY_epw,
            "All_df": all_epw
        }
        self.data_dict=data_dict

    def outputepw(self, type):
        header = []
        data = []
        epw_file_io = get_epw_file_from_drive(service=self.service, file_id=self.file_id)
        content = epw_file_io.read().decode('utf-8').splitlines()
        for i in range(8):
            header.append(content[i])
        for line in content[8:]:
            data.append(line.split(','))

        # Assuming 'TMY_epw.columns' is defined elsewhere and represents the column names
        df_epw = pd.DataFrame(data, columns=self.TMY_df.columns)

        if type == 'TMY':
            df_new_data = self.TMY_df
        elif type == 'EWY':
            df_new_data = self.EWY_df
        elif type == 'ECY':
            df_new_data = self.ECY_df

        for column in df_new_data.columns:
            if column in df_epw.columns:
                df_epw[column] = df_new_data[column]

        # Create a new BytesIO object for the output EPW file
        output_io = io.BytesIO()
        for line in header:
            output_io.write((line + '\n').encode('utf-8'))
        for index, row in df_epw.iterrows():
            output_io.write((','.join(row.astype(str).tolist()) + '\n').encode('utf-8'))
        # Reset the pointer of the output BytesIO object to the beginning
        output_io.seek(0)
        return output_io

