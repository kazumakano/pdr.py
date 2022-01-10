# simple_pdr.py
This is Python module to estimate subject's position with step detection based Pedestrian Dead Reckoning.

## Usage
### main.py
You can run with following command.
You can specify config file with `--conf_file` flag.
`config/default.yaml` will be used if unspecified.
```sh
python main.py [--conf_file PATH_TO_CONF_FILE]
```

### prepare_log_pkls.py
You can prepare log pickle files in advance.
You can use them and load log faster when creating instance of `Log` class.

You can run log preparer with following command.
You can specify config file with `--conf_file` flag.
`config/default.yaml` will be used if unspecified.
You can also specify source log file with `--log_file` flag.
```sh
python prepare_log_pkls.py [--conf_file PATH_TO_CONF_FILE] [--log_file PATH_TO_SRC_LOG_FILE]
```
