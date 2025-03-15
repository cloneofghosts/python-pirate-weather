"""Test the Pirate Weather library."""

import os
import unittest
from datetime import datetime

import pytest
import requests
import responses

import pirateweather


class EndToEnd(unittest.TestCase):
    """Test the Pirate Weather library."""

    def setUp(self):
        """Set up the API key, location and time for the tests."""

        self.api_key = os.environ.get("PIRATEWEATHER_API_KEY")
        self.lat = 52.370235
        self.lng = 4.903549
        self.time = datetime(2015, 2, 27, 6, 0, 0)
        self.extend = "hourly"
        self.version = 2

    def test_with_time(self):
        """Test querying the TimeMachine API endpoint."""

        forecast = pirateweather.load_forecast(
            self.api_key, self.lat, self.lng, time=self.time
        )
        assert forecast.response.status_code == 200

    def test_with_language(self):
        """Test querying the API endpoint with a set language."""

        forecast = pirateweather.load_forecast(
            self.api_key, self.lat, self.lng, time=self.time, lang="de"
        )
        # Unfortunately the API doesn't return anything which
        # states the language of the response. This is the best we can do...
        assert forecast.response.status_code == 200
        assert forecast.response.url.find("lang=de") >= 0

    def test_without_time(self):
        """Test querying the API endpoint."""

        forecast = pirateweather.load_forecast(self.api_key, self.lat, self.lng)
        assert forecast.response.status_code == 200

    def test_extend(self):
        """Test querying the API endpoint."""

        forecast = pirateweather.load_forecast(
            self.api_key, self.lat, self.lng, units="us", extend=self.extend
        )
        hourl_data = forecast.hourly()

        assert forecast.response.status_code == 200
        assert len(hourl_data.data) == 169

    def test_version(self):
        """Test querying the API endpoint."""

        forecast = pirateweather.load_forecast(
            self.api_key, self.lat, self.lng, units="us", version=2
        )

        assert forecast.response.status_code == 200
        assert forecast.response.url.find("version=2") >= 0

    def test_version_data_point(self):
        """Test querying the API endpoint."""

        forecast = pirateweather.load_forecast(
            self.api_key, self.lat, self.lng, units="us", version=2
        )
        fc_cur = forecast.currently()

        assert forecast.response.status_code == 200
        assert fc_cur.fireIndex

    def test_flags(self):
        """Test the data returned by the flags block."""

        forecast = pirateweather.load_forecast(self.api_key, self.lat, self.lng)
        flags = forecast.flags()

        assert len(flags.sources) == 3
        assert len(flags.sourceTimes) == 2
        assert flags.nearestStation == 0
        assert flags.units == "us"
        assert flags.sourceTimes.get("gfs")

    def test_invalid_key(self):
        """Test querying the API endpoint with a invalid API key."""

        self.api_key = "foo"

        try:
            pirateweather.load_forecast(self.api_key, self.lat, self.lng)

            pytest.fail(
                "The previous line did not throw an exception"
            )  # the previous line should throw an exception
        except requests.exceptions.HTTPError:
            assert pytest.raises(requests.exceptions.HTTPError)

    def test_invalid_param(self):
        """Test querying the API endpoint with an invalid parameter."""

        self.lat = ""

        try:
            pirateweather.load_forecast(self.api_key, self.lat, self.lng)

            pytest.fail(
                "The previous line did not throw an exception"
            )  # the previous line should throw an exception
        except requests.exceptions.HTTPError:
            assert pytest.raises(requests.exceptions.HTTPError)


class BasicFunctionality(unittest.TestCase):
    """Test basic functionality of the library."""

    @responses.activate
    def setUp(self):
        """Set up the data to use in the next tests."""

        URL = "https://api.pirateweather.net/forecast/foo/50.0,10.0?units=us&lang=en&extend=None&version=1"
        responses.add(
            responses.GET,
            URL,
            body=open(os.path.join("./fixtures/test.json")).read(),
            status=200,
            content_type="application/json",
            match_querystring=True,
        )

        api_key = "foo"
        lat = 50.0
        lng = 10.0
        self.fc = pirateweather.load_forecast(api_key, lat, lng)

        assert responses.calls[0].request.url == URL

    def test_current_temp(self):
        """Test the current temperature."""

        fc_cur = self.fc.currently()
        assert fc_cur.temperature == 55.81

    def test_datablock_summary(self):
        """Test the hourly summary."""

        hourl_data = self.fc.hourly()
        assert hourl_data.summary == "Drizzle until this evening."

    def test_datablock_icon(self):
        """Test the hourly data point icon."""

        hourl_data = self.fc.hourly()
        assert hourl_data.icon == "rain"

    def test_datablock_not_available(self):
        """Test the minutely data block."""

        minutely = self.fc.minutely()
        assert minutely.data == []

    def test_datapoint_number(self):
        """Test the number of data points returned by the data point."""

        hourl_data = self.fc.hourly()
        assert len(hourl_data.data) == 49

    def test_datapoint_temp(self):
        """Test the first day minumum temperature."""

        daily = self.fc.daily()
        assert daily.data[0].temperatureMin == 50.73

    def test_datapoint_string_repr(self):
        """Test the string representation of the currently data."""

        currently = self.fc.currently()

        assert (
            f"{currently}"
            == "<PirateWeatherDataPoint instance: Overcast at 2014-05-28 04:27:39>"
        )

    def test_datablock_string_repr(self):
        """Test the string representation of the hourly data."""

        hourly = self.fc.hourly()

        assert (
            f"{hourly}"
            == "<PirateWeatherDataBlock instance: Drizzle until this evening. with 49 PirateWeatherDataPoints>"
        )

    def test_datapoint_attribute_not_available(self):
        """Test fetching an invalid property on the daily block."""

        daily = self.fc.daily()
        assert daily.data[0].notavailable is None

    def test_apparentTemperature(self):
        """Test the first hour data block apparent temperature."""

        hourly = self.fc.hourly()
        apprentTemp = hourly.data[0].apparentTemperature

        assert apprentTemp == 55.06

    def test_alerts_length(self):
        """Test the length of the alerts block."""

        alerts = self.fc.alerts()
        assert len(alerts) == 0


class ForecastsWithAlerts(unittest.TestCase):
    """Test basic functionality of the library with alerts."""

    @responses.activate
    def setUp(self):
        """Set up the test data with alerts to use in the next tests."""

        URL = "https://api.pirateweather.net/forecast/foo/50.0,10.0?units=us&lang=en&extend=None&version=1"
        responses.add(
            responses.GET,
            URL,
            body=open(os.path.join("./fixtures/test_with_alerts.json")).read(),
            status=200,
            content_type="application/json",
            match_querystring=True,
        )

        api_key = "foo"
        lat = 50.0
        lng = 10.0
        self.fc = pirateweather.load_forecast(api_key, lat, lng)

    def test_alerts_length(self):
        """Test the length of the alerts block."""

        alerts = self.fc.alerts()
        assert len(alerts) == 2

    def test_alert_title(self):
        """Test the title of the first alert."""

        alerts = self.fc.alerts()
        first_alert = alerts[0]

        assert first_alert.title == "Excessive Heat Warning for Inyo, CA"

    def test_alert_uri(self):
        """Test the first alert URI."""

        alerts = self.fc.alerts()
        first_alert = alerts[0]

        assert (
            first_alert.uri
            == "http://alerts.weather.gov/cap/wwacapget.php?x=CA125159BB3908.ExcessiveHeatWarning.125159E830C0CA.VEFNPWVEF.8faae06d42ba631813492a6a6eae41bc"
        )

    def test_alert_time(self):
        """Test the first alert time."""

        alerts = self.fc.alerts()
        first_alert = alerts[0]

        assert first_alert.time == 1402133400

    def test_alert_property_does_not_exist(self):
        """Test fetching an invalid property on the alerts."""

        alerts = self.fc.alerts()
        first_alert = alerts[0]

        assert first_alert.notarealproperty is None

    def test_alert_string_repr(self):
        """Test the string representation of the currently data."""

        alerts = self.fc.alerts()
        first_alert = alerts[0]

        assert first_alert.time == 1402133400


class BasicManualURL(unittest.TestCase):
    """Test basic URL functionality."""

    @responses.activate
    def setUp(self):
        """Set up the data to use in the next tests."""

        URL = "http://test_url.com/"
        responses.add(
            responses.GET,
            URL,
            body=open(os.path.join("./fixtures/test.json")).read(),
            status=200,
            content_type="application/json",
            match_querystring=True,
        )

        self.forecast = pirateweather.manual("http://test_url.com/")

    def test_current_temp(self):
        """Test the current temperature."""

        fc_cur = self.forecast.currently()
        assert fc_cur.temperature == 55.81

    def test_datablock_summary(self):
        """Test the hourly data block summary."""

        hourl_data = self.forecast.hourly()
        assert hourl_data.summary == "Drizzle until this evening."
