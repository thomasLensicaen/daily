from config import Config
from common import DEFAULT_CONFIG_PATH, ROOT_DIR
import shutil
import pathlib


def create_default_config():
    default_conf = Config.get_default()
    return default_conf


def initialize(config: Config, config_path: pathlib.Path):
    config.get_work_dir().mkdir(exist_ok=True)
    config.get_storage_dir().mkdir(exist_ok=True)
    config.save(config_path)


def move_binaries(config: Config):
    shutil.copytree(ROOT_DIR.as_posix(), config.get_work_dir().as_posix())


if __name__ == '__main__':
    conf = create_default_config()
    initialize(conf, DEFAULT_CONFIG_PATH)
    move_binaries(conf)
