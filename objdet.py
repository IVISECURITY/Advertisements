
print("dsdddddd1")
import cv2
print("dsdddddd2")
from camera import VideoStream
print('Inside Objectdet')
import importlib.util
import numpy as np
import time
import json

"""
Load Data From model.json
"""
dataFile = open('/home/pi/Downloads/Advertisements/model.json')
data = json.load(dataFile)
print(data)

  
# Closing file
dataFile.close()
# Camera Stream Properties


STREAM_URL = 'rtsp://admin:xx2317xx2317@10.0.2.18:554/Streaming/Channels/101?transportmode=unicast'
RESOLUTION = (640, 480)
FPS=30
MIN_CONFIDENCE_THRESHOLD = data['threshold']
min_conf_threshold = data['threshold']
resolution = '1280x720'
resW, resH = resolution.split('x')
imW, imH = int(resW), int(resH)

def count_people_tflite():
    # Import TensorFlow libraries
    # If tflite_runtime is installed, import interpreter from tflite_runtime, else import from regular tensorflow
    #print('inside Detection')
    pkg = importlib.util.find_spec('tflite_runtime')
    if pkg:
        from tflite_runtime.interpreter import Interpreter
    else:
        from tensorflow.lite.python.interpreter import Interpreter
        #print('else Detection')
    # Load the label map
    with open('/home/pi/Downloads/Advertisements/tflite_model/labelmap.txt', 'r') as f:
        labels = [line.strip() for line in f.readlines()]

    # Have to do a weird fix for label map if using the COCO "starter model" from
    # https://www.tensorflow.org/lite/models/object_detection/overview
    # First label is '???', which has to be removed.
    if labels[0] == '???':
        del(labels[0])
        
    # Load the Tensorflow Lite model.
    interpreter = Interpreter(model_path='/home/pi/Downloads/Advertisements/tflite_model/detect.tflite')
    interpreter.allocate_tensors()
    
    # Get model details
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    height = input_details[0]['shape'][1]
    width = input_details[0]['shape'][2]

    floating_model = (input_details[0]['dtype'] == np.float32)

    input_mean = 127.5
    input_std = 127.5
    
    # outputs order for TF2 (1, 3, 0), for TF1 (0, 1, 2)
    boxes_idx, classes_idx, scores_idx = 0, 1, 2
    
    # Initialize video stream
    videostream = VideoStream(stream_url=STREAM_URL,resolution=RESOLUTION,framerate=FPS).start()
    time.sleep(1)
    
    #for frame1 in camera.capture_continuous(rawCapture, format="bgr",use_video_port=True):
    while True:
        #print('inside while')
        # Grab frame from video stream
        count=0
        frame1 = videostream.read()
        
       #print("frame read",frame1)
        cv2.imwrite('/home/pi/Downloads/Advertisements/frame.jpg',frame1)
        # Acquire frame and resize to expected shape [1xHxWx3]
        frame = frame1.copy()
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_resized = cv2.resize(frame_rgb, (width, height))
        input_data = np.expand_dims(frame_resized, axis=0)

        # Normalize pixel values if using a floating model (i.e. if model is non-quantized)
        if floating_model:
            input_data = (np.float32(input_data) - input_mean) / input_std

        # Perform the actual detection by running the model with the image as input
        interpreter.set_tensor(input_details[0]['index'],input_data)
        interpreter.invoke()
        
        #print("reached here")

        # Retrieve detection results
        boxes = interpreter.get_tensor(output_details[boxes_idx]['index'])[0] # Bounding box coordinates of detected objects
        classes = list(interpreter.get_tensor(output_details[classes_idx]['index'])[0]) # Class index of detected objects
        scores = list(interpreter.get_tensor(output_details[scores_idx]['index'])[0]) # Confidence of detected objects
        print("scores:",scores) 
        for i in range(len(scores)):
            if ((scores[i] > min_conf_threshold) and (scores[i] <= 1.0)):

                # Get bounding box coordinates and draw box
                # Interpreter can return coordinates that are outside of image dimensions, need to force them to be within image using max() and min()
                ymin = int(max(1,(boxes[i][0] * imH)))
                xmin = int(max(1,(boxes[i][1] * imW)))
                ymax = int(min(imH,(boxes[i][2] * imH)))
                xmax = int(min(imW,(boxes[i][3] * imW)))
                
                cv2.rectangle(frame, (xmin,ymin), (xmax,ymax), (10, 255, 0), 2)

                # Draw label
                object_name = labels[int(classes[i])] # Look up object name from "labels" array using class index
                print(object_name)
                label = '%s: %d%%' % (object_name, int(scores[i]*100)) # Example: 'person: 72%'
                labelSize, baseLine = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2) # Get font size
                label_ymin = max(ymin, labelSize[1] + 10) # Make sure not to draw label too close to top of window
                cv2.rectangle(frame, (xmin, label_ymin-labelSize[1]-10), (xmin+labelSize[0], label_ymin+baseLine-10), (255, 255, 255), cv2.FILLED) # Draw white box to put label text in
                cv2.putText(frame, label, (xmin, label_ymin-7), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2) #
            
        
        # Person count (labelstxt index = 0)
        # persons = len([scores[idx] for idx, val in enumerate(classes) if val == 0]) # total detected persons
        if object_name == 'person':
          
            confidences = [scores[idx] for idx, val in enumerate(classes) if val == 0]
            persons = len([c for c in confidences if c >= MIN_CONFIDENCE_THRESHOLD and object_name == 'person'])
            print("person found",persons)
           
            count = count+1
            cv2.imwrite('/home/pi/Downloads/Advertisements/sample.jpg',frame)
            
            #with open("/home/pi/Downloads/Advertisements/person.txt", "w") as outfile:
            #    outfile.write(object_name+'#'+str(count))
        return persons
        
        
        #cv2.imshow('Object detector', frame)
        

        # Press 'q' to quit
        #if cv2.waitKey(1) == ord('q'):
        #    break

    # Clean up
    #cv2.destroyAllWindows()
    #videostream.stop()
#count_people_tflite()