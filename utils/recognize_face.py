from keras.models import load_model
from .helper_functions import extract_face, get_embedding
from matplotlib import pyplot
from numpy import expand_dims
from sklearn.svm import SVC
import pickle
from numpy import load
from sklearn.preprocessing import LabelEncoder
from mtcnn.mtcnn import MTCNN
import cv2
from utils import constants as c 
path_to_image ="Tour (67).JPG"


## predict the face of own image





# facenet model
# load the facenet model
fn_model = load_model(c.path_to_facenet_model)
print("Loaded Model")

# load dataset
data = load(c.path_to_face_embeddings)
trainX, trainy, testX, testy = data["arr_0"], data["arr_1"], data["arr_2"], data["arr_3"]
print(f"Dataset: train={trainX.shape} test={testX.shape} ")

# label encode targets
out_encoder = LabelEncoder()
out_encoder.fit(trainy)
trainy = out_encoder.transform(trainy)
testy = out_encoder.transform(testy)


#  load the saved model
model = pickle.load(open(c.path_to_saved_model, 'rb'))







# get extract_face from image
face = extract_face(path_to_image) 
# get embedding vector of face
face_embedded = get_embedding(fn_model, face)
# prediction for the face
samples = expand_dims(face_embedded, axis=0)
yhat_class = model.predict(samples)
yhat_prob = model.predict_proba(samples)
#get name 
class_index = yhat_class[0]
class_probability = yhat_prob[0,class_index] * 100
predict_names = out_encoder.inverse_transform(yhat_class)
print("Predicted: %s (%.3f)" % (predict_names[0], class_probability))
# plot for fun
pyplot.imshow(face)
title = "%s (%.3f)" % (predict_names[0], class_probability)
pyplot.title(title)
pyplot.show()



