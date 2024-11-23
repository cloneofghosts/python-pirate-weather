"""Models used in the Pirate Weather library."""

import datetime

import requests

from pirateweather.utils import UnicodeMixin


class Forecast(UnicodeMixin):
    """Represent the forecast data and provide methods to access weather blocks."""

    def __init__(self, data, response, headers):
        """Initialize the Forecast with data, HTTP response, and headers."""
        self.response = response
        self.http_headers = headers
        self.json = data

        self._alerts = []
        for alertJSON in self.json.get("alerts", []):
            self._alerts.append(Alert(alertJSON))

    def update(self):
        """Update the forecast data by making a new request to the same URL."""
        r = requests.get(self.response.url)
        self.json = r.json()
        self.response = r

    def currently(self):
        """Return the current weather data block."""
        return self._pirateweather_data("currently")

    def minutely(self):
        """Return the minutely weather data block."""
        return self._pirateweather_data("minutely")

    def hourly(self):
        """Return the hourly weather data block."""
        return self._pirateweather_data("hourly")

    def daily(self):
        """Return the daily weather data block."""
        return self._pirateweather_data("daily")

    def offset(self):
        """Return the time zone offset for the forecast location."""
        return self.json["offset"]

    def alerts(self):
        """Return the list of alerts issued for this forecast."""
        return self._alerts

    def _pirateweather_data(self, key):
        """Fetch and return specific weather data (currently, minutely, hourly, daily)."""
        keys = ["minutely", "currently", "hourly", "daily"]
        try:
            if key not in self.json:
                keys.remove(key)
                url = "{}&exclude={}{}".format(
                    self.response.url.split("&")[0],
                    ",".join(keys),
                    ",alerts,flags",
                )

                response = requests.get(url).json()
                self.json[key] = response[key]

            if key == "currently":
                return PirateWeatherDataPoint(self.json[key])
            return PirateWeatherDataBlock(self.json[key])
        except KeyError:
            if key == "currently":
                return PirateWeatherDataPoint()
            return PirateWeatherDataBlock()


class PirateWeatherDataBlock(UnicodeMixin):
    """Represent a block of weather data such as minutely, hourly, or daily summaries."""

    def __init__(self, d=None):
        """Initialize the data block with summary and icon information."""
        d = d or {}
        self.summary = d.get("summary")
        self.icon = d.get("icon")
        self.data = [
            PirateWeatherDataPoint(datapoint) for datapoint in d.get("data", [])
        ]

    def __unicode__(self):
        """Return a string representation of the data block."""
        return f"<PirateWeatherDataBlock instance: {self.summary} with {len(self.data)} PirateWeatherDataPoints>"


class PirateWeatherDataPoint(UnicodeMixin):
    """Represent a single data point in a weather forecast, such as an hourly or daily data point."""

    def __init__(self, d={}):
        """Initialize the data point with timestamp and weather information."""
        self.d = d

        try:
            self.time = datetime.datetime.fromtimestamp(int(d["time"]))
            self.utime = d["time"]
        except KeyError:
            pass

        try:
            sr_time = int(d["sunriseTime"])
            self.sunriseTime = datetime.datetime.fromtimestamp(sr_time)
        except KeyError:
            self.sunriseTime = None

        try:
            ss_time = int(d["sunsetTime"])
            self.sunsetTime = datetime.datetime.fromtimestamp(ss_time)
        except KeyError:
            self.sunsetTime = None

    def __getattr__(self, name):
        """Return the weather property dynamically or return None if missing."""
        try:
            return self.d[name]
        except KeyError:
            return None

    def __unicode__(self):
        """Return a string representation of the data point."""
        return "<PirateWeatherDataPoint instance: " f"{self.summary} at {self.time}>"


class Alert(UnicodeMixin):
    """Represent a weather alert, such as a storm warning or flood alert."""

    def __init__(self, json):
        """Initialize the alert with the raw JSON data."""
        self.json = json

    def __getattr__(self, name):
        """Return the alert property dynamically or return None if missing."""
        try:
            return self.json[name]
        except KeyError:
            return None

    def __unicode__(self):
        """Return a string representation of the alert."""
        return f"<Alert instance: {self.title} at {self.time}>"
