import os.path as path
from datetime import datetime
from glob import iglob
from typing import Union
import script.parameter as param
from script.log import Log


def prepare_log_pkls(file: Union[str, None] = None) -> None:
    if file is None:
        for file in iglob(path.join(param.ROOT_DIR, "log/*.csv")):
            Log(datetime(2000, 1, 1), datetime(2100, 1, 1), file).export_to_pkl(file)    # whole log

    else:
        Log(datetime(2000, 1, 1), datetime(2100, 1, 1), file).export_to_pkl(file)

if __name__ == "__main__":
    import argparse
    from script.parameter import set_params

    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--conf_file", help="specify config file", metavar="PATH_TO_CONF_FILE")
    parser.add_argument("-l", "--log_file", help="specify sourse log file", metavar="PATH_TO_SRC_LOG_FILE")
    args = parser.parse_args()

    set_params(args.conf_file)

    prepare_log_pkls(args.log_file)
