# Pirate Weather Wrapper


This is a wrapper for the Pirate Weather API. It allows you to get the weather for any location, now or in the past.

The Basic Use section covers enough to get you going. I suggest also reading the source if you want to know more about how to use the wrapper or what its doing (it's very simple).


## Installation

You should use pip to install python-pirateweather.

* To install pip install python-pirateweather
* To remove pip uninstall python-pirateweather

Simple!

## Requirements

- You need an API key to use it (https://pirateweather.net/en/latest/). Don't worry a key is free.


## Basic Use

Although you don't need to know anything about the Pirate Weather API to use this module, their docs are available at https://pirateweather.net/en/latest/.

To use the wrapper:

```python
	import pirateweather

	api_key = "YOUR API KEY"
	lat = -31.967819
	lng = 115.87718

	forecast = pirateweather.load_forecast(api_key, lat, lng)
```

The ``load_forecast()`` method has a few optional parameters. Providing your API key, a latitude and longitude are the only required parameters.

Use the ``forecast.DataBlockType()`` eg. ``currently()``, ``daily()``, ``hourly()``, ``minutely()`` or ``flags()`` methods to load the data you are after.

These methods return a DataBlock. Except ``currently()`` which returns a DataPoint. The flags data block contains information used to generate your forecast such as the models used, when they were last updated, the nearest station used (currently always returns 0), the units used in your forecast and the version of the Pirate Weather API.

```python
	byHour = forecast.hourly()
	print(byHour.summary)
	print(byHour.icon)
```

The .data attributes for each DataBlock is a list of DataPoint objects. This is where all the good data is :)

```python
	for hourlyData in byHour.data:
		print(hourlyData.temperature)
```

## Advanced

*function* pirateweather.load_forecast(key, latitude, longitude)
---------------------------------------------------

This makes an API request and returns a **Forecast** object (see below).

Parameters:
- **key** - Your API key from https://pirateweather.net/en/latest/.
- **latitude** - The latitude of the location for the forecast
- **longitude** - The longitude of the location for the forecast
- **time** - (optional) A datetime object for the forecast either in the past or future - see How Timezones Work below for the details on how timezones are handled in this library.
- **units** - (optional) A string of the preferred units of measurement, "us" is the default. "us","ca","uk","si" are also available. See the API Docs (https://pirateweather.net/en/latest/API/#units) for exactly what each unit means.
- **lang** - (optional) A string of the desired language. See https://pirateweather.net/en/latest/API/#language for supported languages.
- **lazy** - (optional) Defaults to `false`.  If `true` the function will request the json data as it is needed. Results in more requests, but maybe a faster response time.
- **extend** - (optional) Defaults to `false`. If `"hourly"` the API will hourly data for 168 hours instead of the standard 48 hours.
- **version** - (optional) Defaults to `1`. If set to `2` the API will return fields that were not part of the Dark Sky API.
- **icon** - (optional) Defaults to `darksky`. If set to `pirate` the API will return icons which aren't apart of the default Dark Sky icon set.
- **callback** - (optional) Pass a function to be used as a callback. If used, load_forecast() will use an asynchronous HTTP call and **will not return the forecast object directly**, instead it will be passed to the callback function. Make sure it can accept it.

----------------------------------------------------


*function* pirateweather.manual(url)
----------------------------------------------------
This function allows manual creation of the URL for the Pirate Weather API request.  This method won't be required often but can be used to take advantage of new or beta features of the API which this wrapper does not support yet. Returns a **Forecast** object (see below).

Parameters:
- **url** - The URL which the wrapper will attempt build a forecast from.
- **callback** - (optional) Pass a function to be used as a callback. If used, an asynchronous HTTP call will be used and ``pirateweather.manual`` **will not return the forecast object directly**, instead it will be passed to the callback function. Make sure it can accept it.

----------------------------------------------------


*class* pirateweather.models.Forecast
------------------------------------

The **Forecast** object, it contains both weather data and the HTTP response from Pirate Weather

**Attributes**
- **response**
	- The Response object returned from requests request.get() method. See https://requests.readthedocs.org/en/latest/api/#requests.Response
- **http_headers**
	- A dictionary of response headers. 'X-Forecast-API-Calls' might be of interest, it contains the number of API calls made by the given API key for the month.
- **json**
	- A dictionary containing the json data returned from the API call.

**Methods**
- **currently()**
	- Returns a PirateWeatherDataPoint object
- **minutely()**
	- Returns a PirateWeatherDataBlock object
- **hourly()**
	- Returns a PirateWeatherDataBlock object
- **daily()**
	- Returns a PirateWeatherDataBlock object
- **update()**
	- Refreshes the forecast data by making a new request.

----------------------------------------------------


*class* pirateweather.models.PirateWeatherDataBlock
---------------------------------------------

Contains data about a forecast over time.

**Attributes** *(descriptions taken from the pirateweather.net website)*
- **summary**
	- A human-readable text summary of this data block.
- **icon**
	- A machine-readable text summary of this data block.
- **data**
	- An array of **PirateWeatherDataPoint** objects (see below), ordered by time, which together describe the weather conditions at the requested location over time.

----------------------------------------------------


*class* pirateweather.models.PirateWeatherDataPoint
---------------------------------------------

Contains data about a forecast at a particular time.

Data points have many attributes, but **not all of them are always available**. Some commonly used ones are:

**Attributes** *(descriptions taken from the pirateweather.net website)*
-	**summary**
	- A human-readable text summary of this data block.
-	**icon**
	- A machine-readable text summary of this data block.
-	**time**
	- The time at which this data point occurs.
-	**temperature**
	- (not defined on daily data points): A numerical value representing the temperature at the given time.
-	**precipProbability**
	- A numerical value between 0 and 1 (inclusive) representing the probability of precipitation occurring at the given time.

For a full list of PirateWeatherDataPoint attributes and attribute descriptions, take a look at the Pirate Weather data point documentation (https://pirateweather.net/en/latest/API/#data-point)

----------------------------------------------------


How Timezones Work
------------------
Requests with a naive datetime (no time zone specified) will correspond to the supplied time in the requesting location. If a timezone aware datetime object is supplied, the supplied time will be in the associated timezone.

Returned times eg the time parameter on the currently DataPoint are always in UTC time even if making a request with a timezone. If you want to manually convert to the locations local time, you can use the `offset` and `timezone` attributes of the forecast object.

Typically, would would want to do something like this:

```python
  # Amsterdam
  lat  = 52.370235
  lng  = 4.903549
  current_time = datetime(2015, 2, 27, 6, 0, 0)
  forecast = pirateweather.load_forecast(api_key, lat, lng, time=current_time)
```

Be caerful, things can get confusing when doing something like the below. Given that I'm looking up the weather in Amsterdam (+2) while I'm in Perth, Australia (+8).

```python
  # Amsterdam
  lat  = 52.370235
  lng  = 4.903549

  current_time = datetime.datetime.now()

  forecast = pirateweather.load_forecast(api_key, lat, lng, time=current_time)
```

The result is actually a request for the weather in the future in Amsterdam (by 6 hours) which isn't supported by the Pirate Weather API.

If you're doing lots of queries in the past in different locations, the best approach is to consistently use UTC time. Keep in mind `datetime.datetime.utcnow()` is **still a naive datetime**. To use proper timezone aware datetime objects you will need to use a library like `pytz <http://pytz.sourceforge.net/>`_ 
