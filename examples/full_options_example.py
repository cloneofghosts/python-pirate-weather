"""Example of how you can fetch data using all the API parameters from the Pirate Weather API."""

# ruff: noqa: T201

import pirateweather


def main():
    """Run load_forecast() with the given lat, lng, and time arguments."""

    api_key = "YOUR API KEY"

    lat = -31.967819
    lng = 115.87718

    forecast = pirateweather.load_forecast(
        api_key,
        lat,
        lng,
        units="us",
        lang="fr",
        extend="hourly",
        version=2,
        icon="pirate",
    )

    print("===========Currently Data=========")
    print(forecast.currently())

    print("===========Hourly Data=========")
    by_hour = forecast.hourly()
    print(f"Hourly Summary: {by_hour.summary}")

    for hourly_data_point in by_hour.data:
        print(hourly_data_point)

    print("===========Daily Data=========")
    by_day = forecast.daily()
    print(f"Daily Summary: {by_day.summary}")

    for daily_data_point in by_day.data:
        print(daily_data_point)


if __name__ == "__main__":
    main()
