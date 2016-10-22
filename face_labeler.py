#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cognitive_face as CF

# Subscription key for calling Cognitive Face API
KEY = '715c880fd8b248a1a20d4ffe3a85d509'
CF.Key.set(KEY)

# Time (in seconds) for sleep between each call to avoid exceeding quota.
# Default to 3 as free subscription have limit of 20 calls per minute.
TIME_SLEEP = 3

img_url = 'https://raw.githubusercontent.com/Microsoft/Cognitive-Face-Windows/master/Data/detection1.jpg'
result = CF.face.detect(img_url)
print(result)






# import argparse
# import base64

# from googleapiclient import discovery
# from oauth2client.client import GoogleCredentials

# def main(photo_file):
#     """Run a label request on a single image"""

#     credentials = GoogleCredentials.get_application_default()
#     service = discovery.build('vision', 'v1', credentials=credentials)

#     with open(photo_file, 'rb') as image:
#         image_content = base64.b64encode(image.read())
#         service_request = service.images().annotate(body={
#             'requests': [{
#                 'image': {
#                     'content': image_content.decode('UTF-8')
#                 },
#                 'features': [{
#                     'type': 'LABEL_DETECTION',
#                     # 'type': 'TEXT_DETECTION',
#                     'maxResults': 5
#                 }]
#             }]

#         })
#         response = service_request.execute()
#         label = response['responses'][0]#['textAnnotations'][0]['description']
#         print(label)
#         # print('Found label: %s for %s' % (label, photo_file))


# if __name__ == "__main__":
#     parser = argparse.ArgumentParser()
#     parser.add_argument('image_file', help="The image you\'d like to label.")
#     args = parser.parse_args()
#     main(args.image_file)