"""Fetches data from the Pirate Weather API."""

import threading

import requests

from pirateweather.models import Forecast


def load_forecast(
    key,
    lat,
    lng,
    time=None,
    units="us",
    lang="en",
    lazy=False,
    callback=None,
    extend=None,
    version=1,
    icon="darksky",
):
    """Build the request url and loads some or all of the needed json depending on lazy is True.

    inLat:  The latitude of the forecast
    inLong: The longitude of the forecast
    time:   A datetime.datetime object representing the desired time of
           the forecast. If no timezone is present, the API assumes local
           time at the provided latitude and longitude.
    units:  A string of the preferred units of measurement, "us" is
            default. also ca,uk,si is available
    lang:   Return summary properties in the desired language
    lazy:   Defaults to false.  The function will only request the json
            data as it is needed. Results in more requests, but
            probably a faster response time (I haven't checked)
    extend: If set to hourly the API will hourly data for 168 hours instead
            of the standard 48 hours.
    version: If set to 2 the API will return fields that were not part of the Dark Sky API.
    icon: If set to pirate the API will return icons which aren't apart of the default Dark Sky icon set
    """

    if time is None:
        url = (
            f"https://api.pirateweather.net/forecast/{key}/{lat},{lng}"
            f"?units={units}&lang={lang}&extend={extend}&version={version}&icon={icon}"
        )
    else:
        url_time = time.replace(
            microsecond=0
        ).isoformat()  # API returns 400 for microseconds
        url = (
            f"https://timemachine.pirateweather.net/forecast/{key}/{lat},{lng},{url_time}"
            f"?units={units}&lang={lang}"
        )

    if lazy is True:
        baseURL = "{}&exclude={}".format(
            url,
            "minutely,currently,hourly,daily,alerts,flags",
        )
    else:
        baseURL = url

    return manual(baseURL, callback=callback)


def manual(requestURL, callback=None):
    """Manually construct the URL for an API call used by load_forecast OR by users."""

    if callback is None:
        return get_forecast(requestURL)
    thread = threading.Thread(target=load_async, args=(requestURL, callback))
    thread.start()
    return None


def get_forecast(requestURL):
    """Get the forecast from the Pirate Weather API."""

    pirateweather_reponse = requests.get(requestURL, timeout=60)
    pirateweather_reponse.raise_for_status()

    json = pirateweather_reponse.json()
    headers = pirateweather_reponse.headers

    return Forecast(json, pirateweather_reponse, headers)


def load_async(url, callback):
    """Get the forecast from the Pirate Weather API asynchronously."""

    callback(get_forecast(url))
