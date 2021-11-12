from script.log import Log
import argparse
from script.parameter import set_params
from datetime import datetime
import script.parameter as param


def _set_main_params(conf: dict) -> None:
    global FILE_NAME

    FILE_NAME = conf["log_file_name"]

def pdr() -> None:
    log = Log(file_name=param.ROOT_DIR + "log/observed/" + FILE_NAME)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", help="specify your config file", metavar="PATH_TO_CONFIG_FILE")

    conf = set_params(parser.parse_args().config)
    _set_main_params(conf)
    pdr()
