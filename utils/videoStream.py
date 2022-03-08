# import the necessary packages
from threading import Thread
import cv2
import time

# import the necessary packages
from threading import Thread
import cv2
class WebcamVideoStream:
    def __init__(self, src=0, time=5):
		# initialize the video camera stream and read the first frame
		# from the stream
        self.stream = cv2.VideoCapture(src)
        (self.grabbed, self.frame) = self.stream.read()
		# initialize the variable used to indicate if the thread should
		# be stopped
        self.stopped = False
        self.time = time*60

    def start(self):
    		# start the thread to read frames from the video stream
        # self.start_time = time.time()
        Thread(target=self.update, args=()).start()
        return self 
    def update(self):
    	# keep looping infinitely until the thread is stopped
        start_time = time.time()
        while True:
    		# if the thread indicator variable is set, stop the thread
            if self.stopped:
                self.stream.release()
                return
    		# otherwise, read the next frame from the stream
            (self.grabbed, self.frame) = self.stream.read()
            # frontend ma stream garne vayesi yo necessary vayena
            cv2.imshow('frame', self.frame)

            # ret, buffer = cv2.imencode('.jpg', self.frame)
            # frame = buffer.tobytes()
            end_time = time.time()
            print(end_time - start_time, self.time )
            if (end_time - start_time) > float(self.time):
                self.stop()
            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.stop()
            # yield (b'--frame\r\n'
            #        b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result




    def read(self):
    	# return the frame most recently read
        return self.frame
    def stop(self):
    	# indicate that the thread should be stopped
        self.stopped = True