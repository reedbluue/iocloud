import shutil

from typing_extensions import Buffer

from fastapi import HTTPException
from pathlib import Path
from unittest import TestCase

from exceptions.FileExceptions import folder_not_exists, folder_already_exists, file_not_exists

from services.FileUtil import FileUtil

import pytest

base_path = "teste_folder"


class TestFileUtil(TestCase):
    @pytest.fixture(autouse=True)
    def setup_data(self):
        path = Path(base_path)
        if path.exists():
            shutil.rmtree(path)

    def test_create_folder_success(self):
        # Arrange
        folder_path = "new_folder"
        code_under_test = FileUtil(base_path)

        # Act
        result = code_under_test.create_folder(folder_path)

        # Assert
        assert result.exists()

    def test_create_folder_already_exists(self):
        # Arrange
        folder_path = "existing_folder"
        code_under_test = FileUtil(base_path)

        code_under_test.create_folder(folder_path)

        # Act & Assert
        with pytest.raises(type(folder_already_exists)):
            code_under_test.create_folder(folder_path)

    def test_delete_folder_successfully(self):
        # Create an instance of FileUtil
        file_util = FileUtil(base_path)

        temp_folder = file_util.create_folder("temp_folder")

        # Call the delete_folder method
        file_util.delete_folder("temp_folder")

        # Check if the folder is deleted successfully
        assert not temp_folder.exists()

    def test_rename_folder_successfully(self):
        # Create an instance of FileUtil
        file_util = FileUtil(base_path)

        temp_folder = file_util.create_folder("temp_folder")

        # Rename the folder
        folder_renamed = file_util.rename_folder("temp_folder", "folder_renamed")

        # Check if the folder has been renamed successfully
        assert folder_renamed.exists()
        assert folder_renamed.is_dir()
        assert folder_renamed.name == "folder_renamed"

    def test_create_file_successfully(self):
        file_util = FileUtil(base_path)
        path = "folder/file.txt"
        data = b"Hello, World!"

        # Act
        result = file_util.create_file(path, data)

        # Assert
        assert result.exists()
        assert result.read_bytes() == data

    def test_move_folder_successfully(self):
        file_util = FileUtil(base_path)

        folder_to_move = file_util.create_folder("folder_to_move")

        # Create a temporary destination folder
        file_util.create_folder("destination_folder")

        # Call the move_folder method
        new_folder = file_util.move_folder("folder_to_move", "destination_folder")

        # Check if the folder was moved successfully
        assert folder_to_move.exists() is False and new_folder.exists()

    def test_get_folder_content_success(self):
        file_util = FileUtil(base_path)

        file_util.create_folder("folder1")
        file_util.create_folder("folder2")
        file_util.create_file("file1.txt", b"Hello, World!")

        result = file_util.get_folder_content("")

        assert "folder1" in result and "folder2" in result and "file1.txt" in result

    def test_get_folder_tree_existing_folder(self):
        # Arrange
        folder_path = "existing_folder"

        expected_result = {
            "subfolder": {
                "subsubfolder": {}
            },
            "subfolder2": {}
        }

        file_util = FileUtil(base_path)

        file_util.create_folder(folder_path)
        file_util.create_folder(f"{folder_path}/subfolder")
        file_util.create_folder(f"{folder_path}/subfolder2")
        file_util.create_folder(f"{folder_path}/subfolder/subsubfolder")
        file_util.create_file(f"{folder_path}/file.txt", b"Hello, World!")

        # Act
        result = file_util.get_folder_tree(folder_path)

        # Assert
        assert result == expected_result

    def test_renaming_existing_file_with_valid_name(self):
        file_util = FileUtil(base_path)

        file_util.create_file("test_file.txt", b"Hello, World!")

        # Rename the file
        new_file_path = file_util.rename_file("test_file.txt", "new_file.txt")

        assert not Path(base_path, "test_file.txt").exists()  # The old file should not exist
        assert new_file_path.exists()

    def test_delete_existing_file(self):
        # Arrange
        file_util = FileUtil(base_path)

        # Create the file
        file_util.create_file("file.txt", b"Hello, World!")

        # Act
        file_util.delete_file("file.txt")

        # Assert
        assert not Path(base_path, "file.txt").exists()

    def test_move_existing_file_to_new_valid_path(self):
        # Create an instance of FileUtil
        file_util = FileUtil(base_path)

        file_util.create_file("test_file.txt", b"Hello, World!")
        file_util.create_folder("new_directory")

        new_file_path = file_util.move_file("test_file.txt", "new_directory")

        # Check that the file was moved to the new path
        assert new_file_path == Path(base_path, "new_directory", "test_file.txt")

    def test_deleting_non_existing_folder(self):
        # Arrange
        folder_path = "non_existing_folder"
        file_util = FileUtil(base_path)

        # Act and Assert
        with pytest.raises(type(folder_not_exists)):
            file_util.delete_folder(folder_path)

    def test_renaming_non_existing_folder(self):
        # Arrange
        file_util = FileUtil(base_path)
        path = "non_existing_folder"
        new_name = "new_folder_name"

        # Act and Assert
        with pytest.raises(type(folder_not_exists)):
            file_util.rename_folder(path, new_name)

    def test_move_non_existing_folder(self):
        file_util = FileUtil(base_path)
        with pytest.raises(type(folder_not_exists)):
            file_util.move_folder("non_existing_folder", "new_path")

    def test_get_folder_tree_non_existing_folder(self):
        file_util = FileUtil(base_path)
        non_existing_folder = "non_existing_folder"

        with pytest.raises(type(folder_not_exists)):
            file_util.get_folder_tree(non_existing_folder)

    def test_get_folder_content_non_existing_folder(self):
        file_util = FileUtil(base_path)
        path = "non_existing_folder"

        with pytest.raises(type(folder_not_exists)):
            file_util.get_folder_content(path)

    def test_renaming_non_existing_file(self):
        file_util = FileUtil(base_path)
        path = "non_existing_file.txt"
        new_name = "new_file.txt"

        # Act and Assert
        with pytest.raises(type(file_not_exists)):
            file_util.rename_file(path, new_name)

    def test_move_non_existing_file(self):
        # Arrange
        file_util = FileUtil(base_path)
        path = "non_existing_file.txt"
        new_path = "new_folder/non_existing_file.txt"

        # Act and Assert
        with pytest.raises(type(file_not_exists)):
            file_util.move_file(path, new_path)

    def test_deleting_non_existing_file(self):
        # Arrange
        file_util = FileUtil(base_path)
        path = "non_existing_file.txt"

        # Act and Assert
        with pytest.raises(type(file_not_exists)):
            file_util.delete_file(path)
