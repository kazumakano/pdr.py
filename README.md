# pdr.py
This is Python module to estimate subject position with simple Pedestrian Dead Reckoning.

## Usage
### main.py
You can run with following command.
You can specify config file with `--config` flag.
`config/default.yaml` will be used if no config file is specified.
```sh
python main.py [--config PATH_TO_CONFIG_FILE]
```

### prepare_log_pkls.py
You can prepare log pickle file.
You can use ir in order to load log faster when creating instance of `Log` class.

You can run preparer with following command.
You can specify config file with `--config` flag.
`config/default.yaml` will be used if no config file is specified.
You can also specify source file with `--src_file` flag.
```sh
python prepare_log_pkls.py [--config PATH_TO_CONFIG_FILE] [--src_file PATH_TO_SRC_FILE]
```
