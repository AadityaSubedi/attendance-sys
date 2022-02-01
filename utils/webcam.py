# import the opencv library
import cv2
from PIL import Image
from keras.models import load_model
from numpy import load
from sklearn.preprocessing import LabelEncoder
import pickle
from .constants import (path_to_facenet_model,
                       path_to_saved_model,
                       path_to_face_embeddings)
from .helper_functions import get_faces, get_embedding
from matplotlib import pyplot
from .videoStream import WebcamVideoStream
# facenet model
# load the facenet model
fn_model = load_model(path_to_facenet_model)
print("Loaded Model")
# load dataset
data = load(path_to_face_embeddings)
trainX, trainy, testX, testy = data["arr_0"], data["arr_1"], data["arr_2"], data["arr_3"]
print(f"Dataset: train={trainX.shape} test={testX.shape} ")


# label encode targets
out_encoder = LabelEncoder()
out_encoder.fit(trainy)
trainy = out_encoder.transform(trainy)
testy = out_encoder.transform(testy)

#  load the saved model
model = pickle.load(open(path_to_saved_model, 'rb'))


# define a video capture object
vid = WebcamVideoStream(0).start()


while(not vid.stopped):

    # Capture the video frame
    # by frame
    frame = vid.read()
    # cv2.imshow('frame', frame)


    # detect the faces in the frame
    faces,frame = hf.get_faces(frame, isFrame=True)
    # Display the resulting frame
    # cv2.imshow('frame', frame)

    if not len(faces):
        continue
    # print(faces[0].shape)
    # exit()

    # get embedding vector of face
    face_embeddeds = [hf.get_embedding(fn_model, face) for face in faces]
    # prediction for the faces
    yhat_classes = model.predict(face_embeddeds)
    yhat_prob = model.predict_proba(face_embeddeds)

    #get name 
    i=0
    predict_names = out_encoder.inverse_transform(yhat_classes)
    for yhat_class in yhat_classes:
        class_index = yhat_class
        class_probability = yhat_prob[i,class_index] * 100
        print("Predicted: %s (%.3f)" % (predict_names[i], class_probability))
        i+=1


    





