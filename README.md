# Weather Data API

A Dockerized Python-Flask-PostgreSQL application for fetching weather data from Meteostat API

## Installation in local environment

Install [docker](https://docs.docker.com/install)

Install [docker-compose](https://docs.docker.com/compose/install/)

Run the following command in the root directory

```bash
docker-compose up
```
If some changes are made to file; please run following command first
```bash
docker-compose build
```
## Documentation
Please refer the documentation published [here](https://documenter.getpostman.com/view/15982446/TzXxkyd1#e1fa0124-d65b-4da5-9274-e9f4a15a8deb) to learn to use this API.

## Contributing
Pull requests are more than welcome. For major changes, please open an issue first to discuss what you would like to change.

## App contains three endpoints to pull data from Meteostat API
#### Historical data fetches all the available data and stores into db
1. /load_historical_data/<stationID=10382>
#### Load daily data loads data into db for a given station id and only of oneday once  
2. /load_daily_data/<stationID=10382>
#### This will give JSON response of the average air temperature for the month of February for the "Berlin / Tegel" 
#### weather station across all available years   
3. /berlin_tegel_station_data/

### Note:
This endpoints will run on port 90.
e.g //localhost:<u><b><i>90</b></u>/berlin_tegel_station_data/
Hope you find this helpful

## License
[MIT](https://choosealicense.com/licenses/mit/)
