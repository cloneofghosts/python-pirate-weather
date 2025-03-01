"""Example of how you can fetch data from the TimeMachine Endpoint from the Pirate Weather API."""

# ruff: noqa: T201

from datetime import datetime

import pirateweather


def main():
    """Run load_forecast() with the given lat, lng, and time arguments."""

    api_key = "YOUR API KEY"

    lat = 45.50884
    lng = -73.58781
    epoch = datetime(1998, 1, 4, 17, 0, 0)

    forecast = pirateweather.load_forecast(api_key, lat, lng, time=epoch, units="ca")

    print("===========Currently Data=========")
    print(forecast.currently())

    print("===========Hourly Data=========")
    by_hour = forecast.hourly()

    for hourly_data_point in by_hour.data:
        print(hourly_data_point)

    print("===========Daily Data=========")
    by_day = forecast.daily()

    for daily_data_point in by_day.data:
        print(daily_data_point)


if __name__ == "__main__":
    main()
