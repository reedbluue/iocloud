from fastapi import HTTPException

folder_already_exists = HTTPException(status_code=409, detail="The folder already exists")

file_already_exists = HTTPException(status_code=409, detail="The file already exists")

folder_not_exists = HTTPException(status_code=404, detail="The folder does not exist")

file_not_exists = HTTPException(status_code=404, detail="The file does not exist")

is_not_a_file = HTTPException(status_code=400, detail="The path is not a file")

is_not_a_folder = HTTPException(status_code=400, detail="The path is not a folder")

invalid_base_path = HTTPException(status_code=400, detail="The base path is invalid")
