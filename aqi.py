import pandas as pd
import plotly.graph_objs as go
import streamlit as st

class AirQualityData:
    """
    Class for reading and filtering air quality data.

    Parameters:
        filename (str): The name of the CSV file containing the air quality data.
    """

    def __init__(self, filename):
        self.data = pd.read_csv(filename)

    def filter_cities(self, cities):
        """
        Filters the air quality data to include only the specified cities.

        Parameters:
            cities (list): A list of city names to include in the filtered data.
        """
        self.data = self.data[ self.data['City'].isin(cities) ]

    def get_aqi_by_city(self):
        """
        Returns a dictionary of AQI data for each city in the filtered air quality data.

        Returns:
            aqi_by_city (dict): A dictionary where each key is a city name and each value is a tuple of two lists:
                the dates and AQI values for that city.
        """
        aqi_by_city = {}
        for city in self.data['City'].unique():
            city_data = self.data[ self.data['City'] == city ]
            aqi_by_city[city] = ( city_data['Date'], city_data['AQI'] )
        return aqi_by_city

class AirQualityPlot:
    """
    A class for creating air quality plots.

    Parameters:
        x (list): A list of x-axis values.
        y (list): A list of y-axis values.
        name (str): The name of the plot.
    """

    def __init__(self, x, y, name):
        self.x = x
        self.y = y
        self.name = name

    def plot(self):
        """
        Returns a plotly Scatter object for the air quality data.

        Returns:
            plotly.graph_objs.Scatter: A plotly Scatter object for the air quality data.
        """
        return go.Scatter(x=self.x, y=self.y, name=self.name, mode='lines')


class AirQualityDashboard:
    """
    A class for creating air quality dashboards.

    Parameters:
        data (dict): A dictionary of AQI data for each city to be included in the dashboard.
        plot_title (str): The title of the dashboard.
        x_title (str): The title of the x-axis.
        y_title (str): The title of the y-axis.
        plot_type (str, optional): The type of plot to create. Defaults to 'lines'.
    """

    def __init__(self, data, plot_title, x_title, y_title, plot_type='lines'):
        self.data = data
        self.plot_title = plot_title
        self.x_title = x_title
        self.y_title = y_title
        self.plot_type = plot_type
        self.traces = []

    def add_trace(self, trace):
        """
        Adds a trace to the dashboard.

        Parameters:
            trace (plotly.graph_objs.Scatter): A plotly Scatter object for the air quality data.
        """
        self.traces.append(trace)

    def plot(self):
        """
        Returns a plotly Figure object for the air quality dashboard.

        Returns:
            plotly.graph_objs.Figure: A plotly Figure object for the air quality dashboard.
        """
        fig = go.Figure(data=self.traces)
        fig.update_layout(title=self.plot_title, xaxis_title=self.x_title, yaxis_title=self.y_title)
        return fig
###################

# Asks the user for the input file
filename = st.file_uploader("Choose a CSV file:", type="csv")

# Reads the data from the input file
if filename is not None:
    data = AirQualityData(filename.name)
    data.filter_cities(data.data['City'].unique())
    aqi_by_city = data.get_aqi_by_city()

    # Creates the dashboard and adds traces to it
    dashboard = AirQualityDashboard(aqi_by_city, "Air Quality Dashboard", "Date", "AQI")
    for city, aqi_data in aqi_by_city.items():
        trace = AirQualityPlot(aqi_data[0], aqi_data[1], city).plot()
        dashboard.add_trace(trace)

    # Plots the dashboard
    fig = dashboard.plot()
    st.plotly_chart(fig)