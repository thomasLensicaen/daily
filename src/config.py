import json
from common import DEFAULT_WD_PATH, DEFAULT_STORAGE_PATH, DEFAULT_BACKUP
import pathlib
from dataclasses import dataclass


@dataclass
class Config:
    work_dir: str
    storage_dir: str
    backup_dir: str

    @staticmethod
    def from_file(path) -> 'Config':
        with open(path, 'r') as fd:
            json_conf: dict = json.load(fd)
        return Config(**json_conf)

    def save(self, config_path: pathlib.Path):
        with open(config_path, 'w') as fd:
            json.dump({'work_dir': self.work_dir,
                       'storage_dir': self.storage_dir,
                       'backup_dir': self.backup_dir}, fd)

    def get_work_dir(self) -> pathlib.Path:
        return pathlib.Path(self.work_dir)

    def get_storage_dir(self) -> pathlib.Path:
        return pathlib.Path(self.storage_dir)

    def get_backup(self) -> pathlib.Path:
        return pathlib.Path(self.backup_dir)

    @classmethod
    def get_default(cls) -> 'Config':
        return Config(DEFAULT_WD_PATH.as_posix(), DEFAULT_STORAGE_PATH.as_posix(), DEFAULT_BACKUP.as_posix())

