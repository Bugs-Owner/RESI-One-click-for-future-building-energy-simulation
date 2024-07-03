from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from .Data_Generation import weather
import os
import pkg_resources
import matplotlib.pyplot as plt
import matplotlib.dates as dates

#Get_token_ready
def authorize():
    creds = None
    credentials_path = pkg_resources.resource_filename(__name__, 'credentials.json')
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', scopes=['https://www.googleapis.com/auth/drive'])
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                credentials_path,
                scopes=['https://www.googleapis.com/auth/drive'],
                redirect_uri='http://localhost:8501/'
            )
            creds = flow.run_local_server(port=8501)
        # with open('token.json', 'w') as token:
        #     token.write(creds.to_json())

    service = build('drive', 'v3', credentials=creds)
    print('Welcome to RSEI, you have successfully accessed.')
    print('Data processing might take 30-50s, please wait')
    return service

class TemperaturePlotter:
    def __init__(self, city, time_span):
        self.city = city
        self.time_span = time_span
        self.wea=None
    def query(self, service):
        wea = weather()
        wea.connect(service)
        wea.get_input(city_name=self.city, span=self.time_span)
        wea.get_geocode()
        wea.get_threshold()
        wea.get_file_name()
        wea.get_drive_data()
        wea.get_extreme_wea()
        wea.get_heatwave()
        self.wea=wea

    def plot_temperature_distribution(self):
        feature = "Dry Bulb Temperature"
        fig, ax = plt.subplots(1, 1, figsize=(6.5, 3), dpi=300, constrained_layout=True)
        timindex = self.wea.All_df[:8760].index
        for i in range(10):
            select = self.wea.All_df[8760 * i:8760 * (i + 1)]
            ax.plot_date(timindex, select[feature], linestyle='-', linewidth=1, markersize=0.1, color='gray')
        ax.plot_date(timindex, self.wea.TMY_df[feature], linestyle='-', linewidth=0.6,
                     markersize=0.08, color='#F2A71B', label="Typical Meteorological Year")
        ax.plot_date(timindex, select[feature], linestyle='-', linewidth=1, markersize=0.1, color='gray',
                     label="10 Years Temperature Distribution")
        ax.plot_date(timindex, self.wea.EWY_df[feature], linestyle='-', linewidth=1.2,
                     markersize=0.08, color='red', label="Extreme Warm Year")
        ax.plot_date(timindex, self.wea.ECY_df[feature], linestyle='-', linewidth=1.2,
                     markersize=0.08, color='blue', label="Extreme Cold Year")
        leg = ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.26), ncol=2, fontsize=11, frameon=False)
        for i in leg.legend_handles:
            i.set_linewidth(1)
        ax.set_ylabel('Temperature[°C]', fontsize=16, fontweight='bold')
        ax.tick_params(axis='both', which='minor', labelsize=11)
        ax.tick_params(axis='both', which='major', labelsize=11)
        ax.xaxis.set_major_locator(dates.MonthLocator(interval=1))
        ax.xaxis.set_major_formatter(dates.DateFormatter('%b'))
        ax.margins(x=0)
        plt.show()

def query(city, time_span, sce):
    """

    :param city: I have integrated this function with Google Geo Coding API, so it should be capable to query any location inside U.S., and give you the nearest city
    :param time_span: 'Mid-term' and 'Long-term' only
    :param sce: TMY, EWY, ECY and All (Typical meteorological year, Extreme warm year, Extreme cold year, and all raw data)
    :return: epw file and pandas dataframe
    """
    plotter = TemperaturePlotter(city=city, time_span=time_span)
    plotter.query(service=authorize())
    plotter.plot_temperature_distribution()
    if sce != 'All':
        _epw = plotter.wea.outputepw(sce)
    else:
        _epw = plotter.wea.raw_io
    _df = plotter.wea.data_dict['{}_df'.format(sce)]

    return _epw.getvalue(), _df, plotter.wea.heat_wave_events
