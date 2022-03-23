# log
This is directory for log files of inertial sensors.

## File Name
You can use any file name as long as its extension is `.csv` or `.pkl`.

## Format
CSV and pickle are supported.

### CSV
CSV Log files must have 7 columns; datetime and sensor values of x, y, and z axis for accelerometer and gyroscope.
Datetime must be like `2000-01-01 00:00:00.000000`.
This is default format of datetime Python standard library.

### Pickle
Pickle log must be tuple of array of datetime and sensor values of x, y, and z axis for accelerometer and gyroscope.
