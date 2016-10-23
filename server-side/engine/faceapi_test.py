#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cognitive_face as CF

# Subscription key for calling Cognitive Face API
KEY = '56abb73c70d649c395df24fe8c5f0d01'
CF.Key.set(KEY)

# Time (in seconds) for sleep between each call to avoid exceeding quota.
# Default to 3 as free subscription have limit of 20 calls per minute.
TIME_SLEEP = 3

img_url = 'https://raw.githubusercontent.com/Microsoft/Cognitive-Face-Windows/master/Data/detection1.jpg'
result = CF.face.detect(img_url)
print(result)