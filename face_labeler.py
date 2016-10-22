#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import time 
import requests
import cv2
import operator
import numpy as np 
import matplotlib.pyplot as plt 
from get_emoji import get_emoji
from PIL import Image

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
    img = cv2.imdecode(imgArr, 1)

    b, g, r = cv2.split(img)
    # b = b.astype(np.float)
    # g = g.astype(np.float)
    # r = r.astype(np.float)

    a = np.ones((img.shape[0], img.shape[1])).astype(np.uint8) #creating a dummy alpha channel image.

    img = cv2.merge((b, g, r, a))

    for face in faceList:
        faceRect = face['faceRectangle']
        emotion = max(face['scores'].items(), 
                      key=operator.itemgetter(1))[0]

        center = (int(faceRect['left'] + (faceRect['width'] / 2)),
                  int(faceRect['top'] + (faceRect['height'] / 2)))

        path = './png/'
        emoji = cv2.imread(path + get_emoji(emotion), -1)
        # emoji = cv2.imread('1f62c.png', -1)
        (b,g,r,a) = cv2.split(emoji)

        offset = int(0.45 * faceRect['width'])

        (width, height) = (faceRect['width']  + offset, 
                           faceRect['height'] + offset)

        emoji = cv2.resize(emoji, (width, height))

        yfrom = int(faceRect['top'] - (offset/2))
        yto   = int(faceRect['top'] + emoji.shape[1] - (offset/2))
        xfrom = int(faceRect['left'] - (offset/2))
        xto   = int(faceRect['left'] + emoji.shape[0] - (offset/2))

        for c in range(0,3):
            img[yfrom:yto, xfrom:xto, c] = emoji[:,:,c] * (emoji[:,:,3]/255.0) +  img[yfrom:yto, xfrom:xto, c] * (1.0 - emoji[:,:,3]/255.0)


        # # alpha = np.ones((emoji.shape[0],emoji.shape[1])) #* 50
        # # emojiRGBA = cv2.merge((b,g,r,alpha))
        # # print("test")



        # img[xfrom:xto,yfrom:yto] = emoji

        # cv2.imshow("pic", img)
        # cv2.waitKey(0)

    cv2.imwrite('test.jpg', img)


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
    # print(get_emoji('happiness'))
    # urlImage = 'https://raw.githubusercontent.com/Microsoft/ProjectOxford-ClientSDK/master/Face/Windows/Data/detection3.jpg'
    urlImage = 'https://lh3.googleusercontent.com/lfQG0dOFvrE3b27b4OvEX4q6OkO5HKYM01Lzu4_E9nRBtMkMmgjBNQJLt3qXB6tpGgtYp-iC_j1GIGx4JpUVFzBCX-z15aArZm7h2PK8GsHz81uFMZ8girwdyYhdxvCj-mEplPUvoeHIgMnGUNsFXTGF3xs5fOtkuWkPglKi7UxSI-XL4eKYLeAYdLmQTA43jP9QULIQG84W99DbmL3KB5t5AarXAQ7bFVBIjz605JU5MDjT9MjFVWsTSmmF6ydVa3VXYhVohLULZU03PpRrcd3V7PAGS3_HstvvauDkQhv5evrS9U78eRewXWE1BDWXh5nQIdAKNxmhCTPOrMXCz3Kwe7_OAjxciYO0FkZY-bh5ZE8pnagOaCTe0BSL7eb1k1y8nvn7bnWizZR4z4hUu0Kd5_BGCaDjJq5cYyC7gVE4PmfKzc_wiGCO41Oz4Z_7TNzOo-oFsZ_EcKCPElOAKfT4qLH3mGQM3cn45po8DcK5e8-ppAN1Y08kAPWUB3k8driLB14hBs09a0mOT6m5InbyIQWxWgqKDeuUXHobCxpbmKIJCq8jHwGZUSsvqI2uwV2Ss3bkdqwZR51Dt1vHwilfTHhSc58o3Cef7S5aZgD51pmG=w1558-h1166-no'
    faceList = analyze_face(urlImage, 'prod')
    draw_emoji(urlImage, faceList)

if __name__ == "__main__":
    main('')









