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



def analyze_face(urlImage, mode):
    # # happy
    # urlImage = 'https://raw.githubusercontent.com/Microsoft/ProjectOxford-ClientSDK/master/Face/Windows/Data/detection3.jpg'
    # # face not detected (side view)
    # urlImage = 'http://static.businessinsider.com/image/53b5e16669bedda46e0122cb/image.jpg'
    # # sad
    
    headers = dict()
    headers['Ocp-Apim-Subscription-Key'] = _key
    headers['Content-Type'] = 'application/json'

    json = {'url': urlImage}
    data = None
    params = None

    result = processRequest(json, data, headers, params)

    if result is not None:
        if mode == 'test':
            print("face found")
            print(result)
            arr = np.asarray(bytearray(requests.get(urlImage).content), dtype=np.uint8)
            # img = cv2.cvtColor(cv2.imdecode(arr, -1), cv2.COLOR_BGR2RGB)
            img = cv2.imdecode(arr, -1)

            drawFace(result, img)

            cv2.imshow("", img)
            cv2.waitKey(0)
    else:
        print("face not found")

    return result    

def draw_emoji(urlImage, faceList):
    imgArr = np.asarray(bytearray(requests.get(urlImage).content), 
                        dtype=np.uint8)
    img = cv2.imdecode(imgArr, -1)

    for face in faceList:
        faceRect = face['faceRectangle']
        emotion = max(face['scores'].items(), 
                      key=operator.itemgetter(1))[0]

        center = (int(faceRect['left'] + (faceRect['width'] / 2)),
                  int(faceRect['top'] + (faceRect['height'] / 2)))

        # emoji = cv2.imread(get_emoji(emotion))
        emoji = cv2.imread('1f62c.png')
        offset = 50
        (width, height) = (faceRect['width']  + offset, 
                           faceRect['height'] + offset)

        print("before", emoji.shape)
        emoji = cv2.resize(emoji, (width, height))
        print("after", emoji.shape)

        xfrom = faceRect['top'] - (offset/2) 
        xto = faceRect['top'] + emoji.shape[1] - (offset/2)
        yfrom = faceRect['left'] - (offset/2) 
        yto = faceRect['left'] + emoji.shape[0] - (offset/2)

        img[xfrom:xto,yfrom:yto] = emoji

        # cv2.imshow("", emoji)
        cv2.imshow("pic", img)

    cv2.waitKey(0)


# Helper functions
def processRequest(json, data, headers, params):
    retries = 0
    result = None

    while True:
        # get response
        resp = requests.request('post', _url, 
                                    json=json, data=data, 
                                    headers=headers, params=params)
        
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

def main(urlImage):
    urlImage = 'https://raw.githubusercontent.com/Microsoft/ProjectOxford-ClientSDK/master/Face/Windows/Data/detection3.jpg'
    faceList = analyze_face(urlImage, 'prod')
    draw_emoji(urlImage, faceList)

if __name__ == "__main__":
    main('')









