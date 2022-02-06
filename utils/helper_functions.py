# function for face detection with mtcnn
from cmath import sin
from PIL import Image
from numpy import asarray
from mtcnn.mtcnn import MTCNN
from numpy import expand_dims
import cv2
# extract a single face from a given photograph
def extract_face(filename, required_size=(160, 160)):
  # load image from file
  image = Image.open(filename)
  # convert to RGB, if needed
  image = image.convert("RGB")
  # convert to array
  pixels = asarray(image)
  # create the detector, using default weights
  detector = MTCNN()
  # detect faces in the image
  results = detector.detect_faces(pixels)

  # if no face detected return None
  if not results:
      return asarray(list())
  # extract the bounding box from the first face
  x1, y1, width, height = results[0]["box"]
  # bug fix
  x1, y1 = abs(x1), abs(y1)
  x2, y2 = x1 + width, y1 + height
  # extract the face
  face = pixels[y1:y2, x1:x2]
  # resize pixels to the model size
  image = Image.fromarray(face)
  image = image.resize(required_size)
  face_array = asarray(image)
  return face_array


# extract  faces from a given photograph
def get_faces(file,isFrame=False, required_size=(160, 160)):
  '''
        file: path to file / frame image
  '''
  if isFrame:
        image= Image.fromarray(file)
  else:
        # load image from file  
        image = Image.open(file)

  # convert to RGB, if needed
  image = image.convert("RGB")
  # convert to array
  pixels = asarray(image)
  # create the detector, using default weights
  detector = MTCNN()
  # detect faces in the image
  results = detector.detect_faces(pixels)
  faces = list()
  for i in range(len(results)):
    # extract the bounding box from the first face
    x1, y1, width, height = results[i]["box"]
    # bug fix
    x1, y1 = abs(x1), abs(y1)
    x2, y2 = x1 + width, y1 + height
    # extract the face
    face = pixels[y1:y2, x1:x2]
    # draw rect over the image 
    cv2.rectangle(pixels,pt1=(x1,y1),pt2=(x2,y2),color=(255,0,0),thickness=2)
    # resize pixels to the model size
    image = Image.fromarray(face)
    image = image.resize(required_size)
    face_array = asarray(image)
    faces.append(face_array)
  return faces, pixels



# get the face embedding for one face
def get_embedding(model, face_pixels):
  # scale pixel values
  face_pixels = face_pixels.astype("float32")
  # standardize pixel values across channels (global)
  mean, std = face_pixels.mean(), face_pixels.std()
  face_pixels = (face_pixels - mean) / std
  # transform face into one sample
  samples = expand_dims(face_pixels, axis=0)
  # make prediction to get embedding
  yhat = model.predict(samples)
  return yhat[0]





  
import json
from typing import AbstractSet, Any, Iterable, Mapping, Optional, Set, Union

from bson.json_util import dumps, loads

JSONType = Mapping[str, Any]


def success(operation: str, msg: str, data: Optional[JSONType] = None) -> JSONType:
    """
    This function returns a formatted dictionary for the successful cases.
    Args:
        operation (str): Operation successfully completed
        msg (str): Sucessful Message
        data (Optional[JSONType], optional): Data to be sent. Defaults to None.
    Returns:
        JSONType: Formatted Dictionary
    """
    return {
        "operation": operation,
        "success": True,
        "message": msg,
        "data": data,
    }


def failure(operation: str, msg: str) -> Mapping[str, Union[str, bool]]:
    """
    This function returns a formatted dictionary for the failure cases, or exceptions.
    Args:
        operation (str): Operation that failed
        msg (str): Failure Message
    Returns:
        Mapping[str, Union[str, bool]]: Formatted Dictionary
    """
    return {
        "operation": operation,
        "success": False,
        "message": msg,
    }



image_extensions = {"png", "jpg", "jpeg", "gif", "bmp", "svg"}

def is_image(filename: str) -> str:
    """
    Checks if the filename if that of a valid image
    Args:
        filename (str): Filename to be checked
    Returns:
        str: Extension of the filename if valid else gives assertion error
    """
    extension = filename.rsplit(".", 1)[-1].lower()
    assert (
        extension in image_extensions
    ), f"Invalid image: {filename}. Allowed extensions: {image_extensions}"
    return extension


pdf_extensions = {"pdf"}

def is_pdf(filename: str) -> str:
    """
    Checks if the filename if that of a valid image
    Args:
        filename (str): Filename to be checked
    Returns:
        str: Extension of the filename if valid else gives assertion error
    """
    extension = filename.rsplit(".", 1)[-1].lower()
    assert (
        extension in pdf_extensions
    ), f"Invalid pdf: {filename}. Allowed extensions: {pdf_extensions}"
    return extension