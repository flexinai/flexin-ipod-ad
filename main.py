import argparse
import json

import cv2
import mediapipe as mp

from calculate_pose import calculate_pose
from output import handstand


def parse_args():
    parser = argparse.ArgumentParser(description='Testing for Handstand.')
    parser.add_argument('-v','--video', type=str)
    parser.add_argument('-o','--output', type=str, default=None)
    parser.add_argument('-d','--data', type=str, default=None)
    parser.add_argument('--det',type=float, default = 0.5,help='detection confidence')
    parser.add_argument('--track',type=float, default =0.5,help='tracking confidence')
    parser.add_argument('-c','--complexity', type=int, default = 1,help='complexity of the model. options 0,1,2')
    
    return parser.parse_args()

args=parse_args()
mp_pose = mp.solutions.pose
detection_confidence = args.det
tracking_confidence = args.track
complexity = args.complexity
calculateVid = cv2.VideoCapture(args.video)
fps = int(calculateVid.get(cv2.CAP_PROP_FPS))
data = []
outJson = "raw.json"
view = {}

with mp_pose.Pose(
    min_detection_confidence=detection_confidence,
    min_tracking_confidence=tracking_confidence,
    model_complexity=complexity,
    smooth_landmarks = True
) as pose:
    while calculateVid.isOpened():
        success, image = calculateVid.read()

        if not success:
            break

        data.append(calculate_pose(image, pose))
    vid = cv2.VideoCapture(args.video)
    width = int(vid.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(vid.get(cv2.CAP_PROP_FPS))
    codec = cv2.VideoWriter_fourcc('a','v','c','1')
    out = cv2.VideoWriter(args.output, codec, fps, (width, height))
    view['data'] = data

    while vid.isOpened():
        next_frame = vid.get(cv2.CAP_PROP_POS_FRAMES)

        success, image = vid.read()
        if not success:
            break
        image = handstand.draw(image, 'left', pose, (255,0,255), (255,255,0))

        final_frame = image

        if args.output:
            out.write(final_frame)

        final_frame = cv2.resize(final_frame,(0,0),fx = 0.5,fy = 0.5)
        # SHOW THE VIDEO
        cv2.imshow('Pose',final_frame)

        if cv2.waitKey(1) & 0xFF == 27:
            break
    vid.release()
    out.release()
    cv2.destroyAllWindows()

if args.data:
    print(args.data)
    with open(args.data, "w") as outfile:
        outfile.write(json.dumps(view['data'], separators=(',', ':')))
