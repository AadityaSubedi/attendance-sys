from numpy import asarray
from os import listdir
from os.path import isdir
from keras.models import load_model
from sklearn import datasets
from .helper_functions import get_embedding,extract_face

from numpy import load, concatenate,savez_compressed
from numpy import where, delete
from flask import current_app as app
import pickle
from sklearn.svm import SVC
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import Normalizer

def train_model(trainX, trainy):
  # normalize input vectors
  in_encoder = Normalizer(norm="l2")
  trainX = in_encoder.transform(trainX)
  # label encode targets
  out_encoder = LabelEncoder()
  out_encoder.fit(trainy)
  trainy = out_encoder.transform(trainy)
  
  #fit model
  model = SVC(kernel="linear", probability=True)
  model.fit(trainX, trainy)
  # save the model to disk
  filename = f'model.sav'
  pickle.dump(model, open(filename, 'wb'))
  print("model updated successfully")


# load images and extract faces for all images in a directory
def load_faces(directory):
  faces = list()
  # enumerate files
  for filename in listdir(directory):
    # path
    path = directory + filename
    # get face
    face = extract_face(path)
    assert face.size, f"Failed to extract face from {path}"
    # store
    faces.append(face)
  return faces

# load a dataset that contains one subdir for each class that in turn contains images
def load_new_dataset(directory, trained_classes):
  X, y = list(), list()
  # enumerate folders, on per class
  for subdir in listdir(directory):
    if subdir in trained_classes:
      continue
    # path
    path = directory + subdir + "/"
    # skip any files that might be in the dir
    if not isdir(path):
      continue
    # load all faces in the subdirectory
    faces = load_faces(path)
    
    # create labels
    labels = [subdir for _ in range(len(faces))]
    # summarize progress
    print(">loaded %d examples for class: %s" % (len(faces), subdir))
    # store
    X.extend(faces)
    y.extend(labels)
  return asarray(X), asarray(y)

from os import listdir
from numpy import where
def get_deleted_classes(directory,trained_classes):
  current_dirs = set()
    # enumerate folders, on per class
  for subdir in listdir(directory):
    # path
    path = directory + subdir + "/"
    # skip any files that might be in the dir
    if not isdir(path):
          continue
    current_dirs.add(subdir)

  deleted_classes = trained_classes - current_dirs
  return deleted_classes


def get_new_embeddings(trainX):
      # convert each face in the train set to an embedding
    # load the facenet model
  model = load_model(f"facenet_keras.h5")
  print("Loaded Model")
  newTrainX = list()
  for face_pixels in trainX:
    embedding = get_embedding(model, face_pixels)
    newTrainX.append(embedding)
  newTrainX = asarray(newTrainX)
  print(newTrainX.shape)
  # convert each face in the test set to an embedding

  return newTrainX

def updated_train():
      
  datasets_dir = f"uploads/datasets/"

  # load dataset
  data = load(f"datasets-embeddings.npz")
  trainX, trainy= data["arr_0"], data["arr_1"]
  print(f"Dataset: train={trainX.shape} ")

  trained_classes = set(trainy)

    # load train dataset
  new_trainX, new_trainy = load_new_dataset(datasets_dir, trained_classes)
  print(new_trainX.shape, new_trainy.shape)


  # get new_embeddings 
  new_trainX = get_new_embeddings(new_trainX)
  print(new_trainX.shape, type(new_trainX))

  # concatenate trainX and new_trainX
  updated_trainX =trainX
  updated_trainy =trainy
  if new_trainX.size :
        # append 
    updated_trainX = concatenate((trainX, new_trainX))
    updated_trainy = concatenate((trainy, new_trainy))
  print("updated data: ",updated_trainX.shape, updated_trainy.shape)


  



  # delete 
  deleted_classes = get_deleted_classes(datasets_dir, trained_classes)
  for del_class in deleted_classes:
    indices_train = where(updated_trainy==del_class)[0]
    updated_trainX= delete(updated_trainX, indices_train, axis=0)
    updated_trainy= delete(updated_trainy, indices_train, axis=0)


    

   

  
  # update incase of any changes only 
  if  new_trainX.size or deleted_classes :
    # save compressed 
    savez_compressed(f"datasets-embeddings.npz", updated_trainX, updated_trainy)
    # retrain the model with updated data
    train_model(updated_trainX, updated_trainy)

if __name__ == "__main__":
  updated_train()