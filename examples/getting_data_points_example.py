"""Example of how you can fetch data from specific data points from the Pirate Weather API."""

# ruff: noqa: T201

import pirateweather


def main():
    """Run load_forecast() with the given lat, lng, and time arguments."""

    api_key = "YOUR API KEY"

    lat = 43.70643
    lng = -79.39864

    forecast = pirateweather.load_forecast(api_key, lat, lng, units="ca", version=2)

    print("===========Currently Data=========")
    current = forecast.currently()
    print(forecast.currently())
    print(f"Current Temperature: {current.temperature}")
    print(f"Current Apparent Temperature: {current.apparentTemperature}")
    print(f"Current Cloud Cover: {current.cloudCover}")
    print(f"Current Fire Index: {current.fireIndex}")

    print("===========Minutely Data=========")
    by_minute = forecast.minutely()
    print(f"Minutely Summary: {by_minute.summary}")

    print("===========Hourly Data=========")
    by_hour = forecast.hourly()
    print(f"Hourly Summary: {by_hour.summary}")

    print(f"Hour 0 Smoke: {by_hour.data[0].smoke}")
    for hourly_data_point in by_hour.data:
        print(
            f"{hourly_data_point.time.strftime('%B %d, %Y UV Index %I %p')}: {hourly_data_point.uvIndex}"
        )

    print("===========Daily Data=========")
    by_day = forecast.daily()
    print(f"Daily Summary: {by_day.summary}")

    print(f"Day 1 Visibility: {by_day.data[1].visibility}")
    for daily_data_point in by_day.data:
        print(
            f"{daily_data_point.time.strftime('%B %d, %Y')} Temperature High: {daily_data_point.temperatureHigh}"
        )


if __name__ == "__main__":
    main()
