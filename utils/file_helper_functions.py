import os
import uuid
from io import BytesIO

from flask import current_app as app
from PIL import Image
from werkzeug.datastructures import FileStorage
from database import DB
from . import helper_functions as hf


def save_image(file: FileStorage, dir="profilePic", subdir="") -> str:
    """
    Checks if the file is valid and saves it.
    Args:
        file (FileStorage): A file uploaded to flask obtained from request.files
    Returns:
        str: The filename of the saved file if its valid else assertion error is thrown
    """

    assert file.filename, "No image selected."
    extension = hf.is_image(file.filename)
    if subdir:
        directory = os.path.join(os.getcwd(), app.config["UPLOAD_FOLDER"], dir,subdir)

    else:
        directory = os.path.join(os.getcwd(), app.config["UPLOAD_FOLDER"], dir)

    # !Create the directory if it doesn't exist
    os.makedirs(directory, exist_ok=True)
    filename = f"{uuid.uuid4()}.{extension}"
    imageFileBytes = BytesIO(file.stream.read())
    image = Image.open(imageFileBytes)
    image.save(os.path.join(directory, filename), quality=50)
    return filename


def remove_image(filename: str):
    try:
        pass
    #! TODO: Remove the image from dropbox

    except FileNotFoundError:
        print("ERROR: Uploaded file accidentally removed")
