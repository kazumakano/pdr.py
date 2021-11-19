import argparse
from glob import iglob
import script.parameter as param
from script.log import Log
from script.parameter import set_params


def prepare_log_pkls(src_file: str) -> None:
    if src_file is None:
        for src_file in iglob(param.ROOT_DIR + "log/*.csv"):
            Log(file_name=src_file).export_to_pkl(src_file)

    else:
        Log(file_name=src_file).export_to_pkl(src_file)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", help="specify your config file", metavar="PATH_TO_CONFIG_FILE")
    parser.add_argument("--src_file", help="specify sourse file", metavar="PATH_TO_SRC_FILE")
    args = parser.parse_args()

    set_params(args.config)

    prepare_log_pkls(args.src_file)
