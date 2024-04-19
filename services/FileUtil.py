import shutil
from pathlib import Path
from typing_extensions import Buffer

from fastapi import HTTPException
from configs.logger import logger
from exceptions.FileExceptions import folder_already_exists, folder_not_exists, is_not_a_folder, \
    file_already_exists, file_not_exists, is_not_a_file, invalid_base_path


class FileUtil:
    def __init__(self, base_path: str) -> None:
        self.base_folder: str = base_path

    def create_folder(self, path: str) -> Path:
        try:
            self.validate_path(path)
            folder = Path(self.base_folder).joinpath(path)

            if folder.exists():
                raise folder_already_exists

            folder.mkdir(parents=True, exist_ok=True)

            return folder
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def delete_folder(self, path: str) -> None:
        folder = Path(self.base_folder).joinpath(path)

        self.validate_path(path)

        if not folder.exists():
            raise folder_not_exists

        if not folder.is_dir():
            raise is_not_a_folder

        try:
            shutil.rmtree(folder)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def rename_folder(self, path: str, new_name: str) -> Path:
        old_folder = Path(self.base_folder).joinpath(path)

        self.validate_path(path)
        self.validate_path(new_name)

        if not old_folder.exists():
            raise folder_not_exists

        if not old_folder.is_dir():
            raise is_not_a_folder
        try:
            new_folder = old_folder.parent.joinpath(new_name)
            old_folder.rename(new_folder)
            return new_folder
        except Exception as e:
            logger.exception(e)
            raise HTTPException(status_code=500, detail=str(e))

    def move_folder(self, path: str, new_path: str) -> Path:
        self.validate_path(new_path)
        self.validate_path(path)

        old_folder = Path(self.base_folder).joinpath(path)
        new_folder = Path(self.base_folder).joinpath(new_path).joinpath(old_folder.name)

        if not old_folder.exists() or not new_folder.parent.exists():
            raise folder_not_exists

        if not new_folder.parent.is_dir() or not old_folder.is_dir():
            raise is_not_a_folder
        try:
            old_folder.rename(new_folder)
            return new_folder
        except Exception as e:
            logger.exception(e)
            raise HTTPException(status_code=500, detail=str(e))

    def get_folder_tree(self, path: str) -> dict:
        self.validate_path(path)

        folder = Path(self.base_folder).joinpath(path) if not Path(path).is_relative_to(
            self.base_folder) else Path(path)

        if not folder.exists():
            raise folder_not_exists

        if not folder.is_dir():
            raise is_not_a_folder

        content = {}
        for child in folder.iterdir():
            if child.is_dir():
                content[child.name] = self.get_folder_tree(str(child))
        return content

    def get_folder_content(self, path: str) -> list[str]:
        self.validate_path(path)

        folder = Path(self.base_folder).joinpath(path)

        if not folder.exists():
            raise folder_not_exists

        if not folder.is_dir():
            raise is_not_a_folder

        if folder.is_dir():
            content = []
            for child in folder.iterdir():
                content.append(child.name)
            return content

    def create_file(self, path: str, data: Buffer) -> Path:
        self.validate_path(path)

        try:
            file = Path(self.base_folder).joinpath(path)

            if file.exists():
                raise file_already_exists

            file.parent.mkdir(parents=True, exist_ok=True)
            file.write_bytes(data)
            return file
        except Exception as e:
            logger.exception(e)
            raise HTTPException(status_code=500, detail=str(e))

    def rename_file(self, path: str, new_name: str) -> Path:
        self.validate_path(path)
        self.validate_path(new_name)

        old_file = Path(self.base_folder).joinpath(path)

        if not old_file.exists():
            raise file_not_exists

        if not old_file.is_file():
            raise is_not_a_file

        try:
            new_file = old_file.parent.joinpath(new_name)
            old_file.rename(new_file)
            return new_file
        except Exception as e:
            logger.exception(e)
            raise HTTPException(status_code=500, detail=str(e))

    def move_file(self, path: str, new_path: str) -> Path:
        self.validate_path(path)
        self.validate_path(new_path)

        old_file = Path(self.base_folder).joinpath(path)
        new_file = Path(self.base_folder).joinpath(new_path).joinpath(old_file.name)

        if not old_file.exists() or not new_file.parent.exists():
            raise file_not_exists

        if not old_file.is_file():
            raise is_not_a_file
        try:
            old_file.rename(new_file)
            return new_file
        except Exception as e:
            logger.exception(e)
            raise HTTPException(status_code=500, detail=str(e))

    def delete_file(self, path: str) -> None:
        self.validate_path(path)

        file = Path(self.base_folder).joinpath(path)

        if not file.exists():
            raise file_not_exists

        if not file.is_file():
            raise is_not_a_file
        try:
            file.unlink()
        except Exception as e:
            logger.exception(e)
            raise HTTPException(status_code=500, detail=str(e))

    def validate_path(self, path: str) -> None:
        if ".." in Path(path).parts:
            raise invalid_base_path
