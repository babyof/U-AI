"""
Google Vision API Tutorial with a Raspberry Pi and Raspberry Pi Camera.  See more about it here:  https://www.dexterindustries.com/howto/use-google-cloud-vision-on-the-raspberry-pi/

Use Google Cloud Vision on the Raspberry Pi to take a picture with the Raspberry Pi Camera and classify it with the Google Cloud Vision API.   First, we'll walk you through setting up the Google Cloud Platform.  Next, we will use the Raspberry Pi Camera to take a picture of an object, and then use the Raspberry Pi to upload the picture taken to Google Cloud.  We can analyze the picture and return labels (what's going on in the picture), logos (company logos that are in the picture) and faces.

This script uses the Vision API's label detection capabilities to find a label
based on an image's content.

"""

import argparse
import base64
#import picamera
import json

#add
import io
import os

#from googleapiclient import discovery
#from oauth2client.client import GoogleCredentials

#add
from google.cloud import vision
from google.cloud.vision import types

def takephoto():
    camera = picamera.PiCamera()
    camera.capture('image.jpg')

def getText(isLabel):
    takephoto() # First take a picture
    """Run a label request on a single image"""
    
#the Parameter that is configure if it is label or other things
# isLabel = 0
    client = vision.ImageAnnotatorClient()
    file_name = os.path.join(os.path.dirname(__file__),'image.PNG')

    with open(file_name, 'rb') as image_file:
    	content = image_file.read()

    image = types.Image(content = content)
    if isLabel:
   	 response = client.label_detection(image=image)
   	 labels = response.label_annotations

   	 Result = "what is "+labels[0].description+"?"
   	 print(Result)
    else:
         response = client.face_detection(image=image)
         faces = response.face_annotations

# Names of likelihood from google.cloud.vision.enums
         likelihood_name = ('UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE',
	                          'LIKELY', 'VERY_LIKELY')
         print('Faces:')

         for face in faces:
             print(face.anger_likelihood)
             print(type(face.anger_likelihood))
              
             if face.anger_likelihood > 3:
                 print('anger: {}'.format(likelihood_name[face.anger_likelihood]))
                 Result = "I feel angry"
                 break;
             if face.joy_likelihood > 3:
                 print('joy: {}'.format(likelihood_name[face.joy_likelihood]))
                 Result = "I feel joy"
                 break;
             if face.surprise_likelihood > 3:
                 print('surprise: {}'.format(likelihood_name[face.surprise_likelihood]))
                 Result = "I feel surprise"
             """
             vertices = (['({},{})'.format(vertex.x, vertex.y)
		   	 for vertex in face.bounding_poly.vertices])

             print('face bounds: {}'.format(','.join(vertices)))
	     """
         print(Result)
    return Result
	     
if __name__ == '__main__':

    main(1)
