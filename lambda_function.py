import sys

sys.path.append("/mnt/efs/packages")
import json

import boto3
import cv2
import mediapipe as mp

from output import handstand
from recode import recode


def lambda_handler(event, context):
    # setup
    # define variables
    mp_pose = mp.solutions.pose
    bucket = "myth-software"
    base_url = 'https://' + bucket +'.s3.us-east-2.amazonaws.com/'
    body = json.loads(event['responsePayload']['body'])
    url = body['resized']
    key = url.split(base_url)[1]
    [filename, extension] = key.split('.')
    parts = filename.split('_')
    parts[0] = 'output'
    output_s3_key = '_'.join(parts) + '.' + extension
    tmp_output = '/tmp/output.webm'
    detection_confidence = 0.5
    tracking_confidence = 0.5
    complexity = 1

    # initalize pose
    with mp_pose.Pose(
        min_detection_confidence=detection_confidence,
        min_tracking_confidence=tracking_confidence,
        model_complexity=complexity,
        smooth_landmarks=True
    ) as pose:
        vid = cv2.VideoCapture(url)
        width = int(vid.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = int(vid.get(cv2.CAP_PROP_FPS))
        codec = cv2.VideoWriter_fourcc('V', 'P', '0', '8')
        out = cv2.VideoWriter(tmp_output, codec,
                                fps, (width, height))
        while vid.isOpened():
            success, image = vid.read()
            if not success:
                break
            image = handstand.draw(image, body['visibility'], pose, (255,255,0), (255,0,255))
            final_frame = image
            out.write(final_frame)
            final_frame = cv2.resize(final_frame, (0, 0), fx=0.5, fy=0.5)
        vid.release()
        out.release()
        # clip the video using ffmpeg
        recode('/opt/bin/ffmpeg', tmp_output, '/tmp/' + output_s3_key)

        # s3 = boto3.client('s3')
        # s3.upload_file(
        #     '/tmp/' + output_s3_key,
        #     "myth-software",
        #     output_s3_key,
        #     ExtraArgs={'ContentType': 'video/mp4'}
        # )

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "success"
        }),
    }
