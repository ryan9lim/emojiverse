#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
from get_emoji import get_emoji
from azure.storage.blob import BlockBlobService
from azure.storage.blob import PublicAccess
from azure.storage.blob import ContentSettings
import time 
import requests
import cv2
import operator
import numpy as np 
import matplotlib.pyplot as plt
import base64
import time

# Variables
_urlImgAPI = 'https://api.projectoxford.ai/emotion/v1.0/recognize'
_urlVidAPI = 'https://api.projectoxford.ai/emotion/v1.0/recognizeinvideo'
_imgKey = '56abb73c70d649c395df24fe8c5f0d01'
_vidKey = '6d733f1bc1e14010ac21969564926a56'
_maxNumRetries = 10
_filename = 'user_image.png'
_cloudPath = 'https://emojiverse2.blob.core.windows.net/imgstore/img'
block_blob_service = None

def emojify(imageData, numPics):
    # urlImage = 'https://raw.githubusercontent.com/Microsoft/ProjectOxford-ClientSDK/master/Face/Windows/Data/detection3.jpg'
    # urlImage = 'https://lh3.googleusercontent.com/lfQG0dOFvrE3b27b4OvEX4q6OkO5HKYM01Lzu4_E9nRBtMkMmgjBNQJLt3qXB6tpGgtYp-iC_j1GIGx4JpUVFzBCX-z15aArZm7h2PK8GsHz81uFMZ8girwdyYhdxvCj-mEplPUvoeHIgMnGUNsFXTGF3xs5fOtkuWkPglKi7UxSI-XL4eKYLeAYdLmQTA43jP9QULIQG84W99DbmL3KB5t5AarXAQ7bFVBIjz605JU5MDjT9MjFVWsTSmmF6ydVa3VXYhVohLULZU03PpRrcd3V7PAGS3_HstvvauDkQhv5evrS9U78eRewXWE1BDWXh5nQIdAKNxmhCTPOrMXCz3Kwe7_OAjxciYO0FkZY-bh5ZE8pnagOaCTe0BSL7eb1k1y8nvn7bnWizZR4z4hUu0Kd5_BGCaDjJq5cYyC7gVE4PmfKzc_wiGCO41Oz4Z_7TNzOo-oFsZ_EcKCPElOAKfT4qLH3mGQM3cn45po8DcK5e8-ppAN1Y08kAPWUB3k8driLB14hBs09a0mOT6m5InbyIQWxWgqKDeuUXHobCxpbmKIJCq8jHwGZUSsvqI2uwV2Ss3bkdqwZR51Dt1vHwilfTHhSc58o3Cef7S5aZgD51pmG=w1558-h1166-no'
    # analyze_video()

    #----------------IMAGE----------------#
    fh = open(_filename, 'wb')
    # print(type(imageData))
    fh.write(base64.b64decode(imageData))
    # print(base64.b64decode(imageData))
    fh.close()

    # img = cv2.imread('./user_image.png')
    # img = cv2.resize(img, (int(0.7 * img.shape[1]), int(0.7 * img.shape[0])))
    # cv2.imwrite(_filename, img)
    # cv2.imshow("img", img)

    # print("before cloud")
    pushToCloud('./' + _filename, numPics)
    # print("after cloud")

    faceList = analyze_face(_cloudPath + str(numPics) + '.png', 'prod')

    #----------------NEW (Push result to cloud)
    filename = draw_emoji(_cloudPath + str(numPics) + '.png', faceList, numPics)
    return filename
    #----------------OLD
    # emojifiedImage = draw_emoji(_cloudPath + str(numPics) + '.png', faceList)
    # return encodeImage


    # cv2.imshow("emojified", emojifiedImage)
    # encodeImage = base64.urlsafe_b64encode(emojifiedImage)
    # encodeImage = base64.decodestring(encodeImage)
    #----------------VIDEO----------------#
    # analyze_video()
    # return 0

def analyze_face(urlImage, mode):    
    headers = dict()
    headers['Ocp-Apim-Subscription-Key'] = _imgKey
    headers['Content-Type'] = 'application/json'

    json = {'url': urlImage}
    data = None
    params = None

    result = processImgRequest(json, _urlImgAPI, data, headers, params)

    if result is not None:
        if mode == 'test':
            print("face found")
            # print(result)

            # img = cv2.imread(_filename)
            # drawFace(result, img)
            # cv2.imshow("", img)
            # cv2.waitKey(0)
    else:
        print("face not found")

    return result    

def analyze_video():
    headers = dict()
    headers['Ocp-Apim-Subscription-Key'] = _vidKey

    json = {}
    data = None
    params = dict()
    params['outputStyle'] = 'aggregate'
    url = _urlVidAPI + '?outputStyle=aggregate'

    opLocation = processVidOpRequest(json, url, data, headers, params)

    json


def draw_emoji(urlImage, faceList, numPics):
    # imgArr = np.asarray(bytearray(requests.get(urlImage).content), 
    #                     dtype=np.uint8)
    # img = cv2.imdecode(imgArr, 1)

    img = cv2.imread('./user_image.png')
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

        (b,g,r,a) = cv2.split(emoji)

        offset = int(0.45 * faceRect['width'])

        (width, height) = (faceRect['width']  + offset, 
                           faceRect['height'] + offset)

        emoji = cv2.resize(emoji, (width, height))

        yfrom = int(faceRect['top'] - (offset/2))
        yfrom = max(0, yfrom)

        yto   = int(faceRect['top'] + emoji.shape[1] - (offset/2))
        yto   = min(img.shape[0], yto)

        ydist = yto - yfrom

        yfrom_emj = 0
        yto_emj = 0
        if yto == img.shape[0]:
            yfrom_emj = 0
            yto_emj = ydist
        elif yfrom == 0:
            yfrom_emj = emoji.shape[0]-ydist
            yto_emj = emoji.shape[0]
        else:
            yfrom_emj = 0
            yto_emj = emoji.shape[0]

        xfrom = int(faceRect['left'] - (offset/2))
        xfrom = max(0, xfrom)

        xto   = int(faceRect['left'] + emoji.shape[0] - (offset/2))
        xto   = min(img.shape[1], xto)

        xdist = xto - xfrom

        xfrom_emj = 0
        xto_emj = 0
        if xto == img.shape[1]:
            xfrom_emj = 0
            xto_emj = xdist
        elif xfrom == 0:
            xfrom_emj = emoji.shape[1]-xdist
            xto_emj = emoji.shape[1]
        else:
            xfrom_emj = 0
            xto_emj = emoji.shape[1]

        print("yto-yfrom", yto-yfrom, "xto-xfrom", xto-xfrom)
        print("yto_emj-yfrom_emj", yto_emj-yfrom_emj, "xto_emj-xfrom_emj", xto_emj-xfrom_emj)

        for c in range(0,3):
            img[yfrom:yto,xfrom:xto,c] = emoji[yfrom_emj:yto_emj,xfrom_emj:xto_emj,c] * (emoji[yfrom_emj:yto_emj,xfrom_emj:xto_emj,3]/255.0) + img[yfrom:yto,xfrom:xto,c] * (1.0 - emoji[yfrom_emj:yto_emj,xfrom_emj:xto_emj,3]/255.0)

    cv2.imwrite('result.jpg', img)

    #-------------------NEW
    # print("before cloud")
    block_blob_service.create_blob_from_path(
        'imgstore',
        'img' + str(numPics) + '.jpg',
        'result.jpg',
        content_settings=ContentSettings(content_type='image/jpg')
    )
    # print("after cloud")
    return ('https://emojiverse2.blob.core.windows.net/imgstore/img' + str(numPics) + '.jpg')

    #------------------OLD
    # return img



# Helper functions
def processImgRequest(json, url, data, headers, params):
    retries = 0
    result = None

    while True:
        # get response
        resp = requests.request('post', url=url,
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

def processVidOpRequest(json, url, data, headers, params):
    retries = 0
    result = None

    while True:
        # get response
        resp = requests.request('post', url=url,
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
        elif resp.status_code == 202:
            result = resp.headers['operation-location']
            # print("header", resp.headers, "json", resp.json, "content", resp.content)

        else:
            print("Error code: %d" % (resp.status_code))
            print("Message: %s" % (resp.json()['error']['message']))

        break

    return result

# def processVidRecogRequest(json, url, data, headers, params):

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

def pushToCloud(localPath, numPics):
    global block_blob_service
    block_blob_service = BlockBlobService(account_name='emojiverse2',
        account_key='bsLnZdnBz5yppDuprvDNlnWNNLAFl4y6vcOiIz23NozQwLIqJQ12AYkqISdc/WyHVV4HYtGv+Y4b25q2JbmN5A==')

    block_blob_service.set_container_acl('imgstore', 
                                         public_access=PublicAccess.Container)

    block_blob_service.create_blob_from_path(
        'imgstore',
        'img' + str(numPics) + '.png',
        _filename,
        content_settings=ContentSettings(content_type='image/png')
    )

    return 0

# emojify(0, 0)
