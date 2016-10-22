#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import time 
import requests
import cv2
import operator
import numpy as np 
import matplotlib.pyplot as plt 

# Variables
_url = 'https://api.projectoxford.ai/emotion/v1.0/recognize'
_key = '56abb73c70d649c395df24fe8c5f0d01'
_maxNumRetries = 10

# Helper functions
def processRequest(json, data, headers, params):
    retries = 0
    result = None

    while True:
        # get response
        resp = requests.request('post', _url, 
                                    json=json, data=data, 
                                    headers=headers, params=params)
        
        print(resp.json())

        # fields
        lenf = 'content-length'
        typef = 'content-type'

        # rate limit exceeded
        if resp.status_code == 429:
            print("Message: %s" % (resp.json()['error']['message']))

            if retries <= _maxNumRetries:
                time.sleep(1)
                retries += 1
                continue
            else:
                print('Error: failed after retrying!')
                break

        # successful call
        elif resp.status_code == 200 or resp.status_code == 201:
            if lenf in resp.headers and int(resp.headers[lenf]) == 0:
                result = None
            elif typef in resp.headers and isinstance(resp.headers[typef], str):
                if 'application/json' in resp.headers[typef].lower():
                    result = resp.json() if resp.content else None
                elif 'image' in resp.headers[typef].lower():
                    result = resp.content

        else:
            print("Error code: %d" % (resp.status_code))
            print("Message: %s" % (resp.json()['error']['message']))

        break

    return result

def drawFace(result, img):
    for face in result:
        faceRect = face['faceRectangle']
        cv2.rectangle(img, (faceRect['left'], 
                            faceRect['top']), 
                           (faceRect['left'] + faceRect['width'], 
                            faceRect['top']  + faceRect['height']), 
                           color=(255,0,0), thickness=5 )

    for face in result:
        faceRect = face['faceRectangle']
        emotion = max(face['scores'].items(), 
                      key=operator.itemgetter(1))[0]

        textToWrite = "%s" % (emotion)
        cv2.putText(img, textToWrite, (faceRect['left'], 
                                       faceRect['top']-10),
                                       cv2.FONT_HERSHEY_SIMPLEX,
                                       0.5, (255,0,0), 1)

def main():
    urlImage = 'https://raw.githubusercontent.com/Microsoft/ProjectOxford-ClientSDK/master/Face/Windows/Data/detection3.jpg'
    headers = dict()
    headers['Ocp-Apim-Subscription-Key'] = _key
    headers['Content-Type'] = 'application/json'

    json = {'url': urlImage}
    data = None
    params = None

    result = processRequest(json, data, headers, params)

    if result is not None:
        print("normal")
        arr = np.asarray(bytearray(requests.get(urlImage).content), dtype=np.uint8)
        # img = cv2.cvtColor(cv2.imdecode(arr, -1), cv2.COLOR_BGR2RGB)
        img = cv2.imdecode(arr, -1)

        drawFace(result, img)

        ig, ax = plt.subplots(figsize=(15,20))
        print(dir(ax))
        cv2.imshow("", img)
        # ax.show(img)

    cv2.waitKey(0)
    return None    

if __name__ == "__main__":
    main()









