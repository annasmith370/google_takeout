# Google Takeout :bento:
Control & visualize google takeout data

## Setup

Requirements:
* [poetry](https://python-poetry.org/docs/)
* Python 3.6.5+

[Follow Google's instructions](https://support.google.com/accounts/answer/3024190?hl=en) for requesting and downloading account data for all accounts and products of interest (This could take several days). Select 2GB `.zip` files, and copy all of them to the [data/raw](google_takeout/data/raw) directory.


## Running

To create the virtual environment:

```bash
$ make venv
```

To stage & prepare data after it has been copied to `data/raw`:
```bash
$ make data
```

Specific analysis and visualization options available by product  

## Accessing your data
After the data is staged, it will be available in a <Postgres/SQLite> database accessible via 

```bash
$ make shell_sql
```

Following is a quick summary of the database contents. A full entity relationship diagram is available [here](TODO)

## By Product

### Google Fit

Raw daily activities:
* `fit_activities_activity`: rawfile, activity_num, Sport, Id, Notes
* `fit_activities_lap`: rawfile, activity_num, lap_num, DistanceMeters, TotalTimeSeconds, Calories, Intensity, TriggerMethod
* `fit_activities_trackpoint`: rawfile, activity_num, lap_num, trackpoint_num, Distance, Time, AltitudeMeters
* `fit_activities_position`: rawfile, activity_num, lap_num, trackpoint_num,  Latitude, Longitude,