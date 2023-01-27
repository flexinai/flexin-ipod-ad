import cv2
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose


def draw(image, visibile, pose, point_color, connection_color):
    drawing_spec_points = mp_drawing.DrawingSpec(thickness=2, circle_radius=2,color = point_color)
    drawing_spec = mp_drawing.DrawingSpec(thickness=2, circle_radius=2,color = connection_color)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image.flags.writeable = False
    results = pose.process(image)

    #code for pose extraction
    try:
        landmarks = results.pose_landmarks.landmark

        # visibility
        ## nose
        NOSE = landmarks[mp_pose.PoseLandmark.NOSE.value]
        NOSE.visibility = 0

        ## face
        LEFT_EYE =landmarks[mp_pose.PoseLandmark.LEFT_EYE.value]
        LEFT_EYE_INNER =landmarks[mp_pose.PoseLandmark.LEFT_EYE_INNER.value]
        LEFT_EYE_OUTER =landmarks[mp_pose.PoseLandmark.LEFT_EYE_OUTER.value]
        LEFT_EAR =landmarks[mp_pose.PoseLandmark.LEFT_EAR.value]
        MOUTH_LEFT =landmarks[mp_pose.PoseLandmark.MOUTH_LEFT.value]
        RIGHT_EYE = landmarks[mp_pose.PoseLandmark.RIGHT_EYE.value]
        RIGHT_EYE_INNER = landmarks[mp_pose.PoseLandmark.RIGHT_EYE_INNER.value]
        RIGHT_EYE_OUTER = landmarks[mp_pose.PoseLandmark.RIGHT_EYE_OUTER.value]
        RIGHT_EAR = landmarks[mp_pose.PoseLandmark.RIGHT_EAR.value]
        MOUTH_RIGHT = landmarks[mp_pose.PoseLandmark.MOUTH_RIGHT.value]
        LEFT_EYE.visibility = 0
        LEFT_EYE_INNER.visibility = 0
        LEFT_EYE_OUTER.visibility = 0
        LEFT_EAR.visibility = 0
        MOUTH_LEFT.visibility = 0
        RIGHT_EYE.visibility = 0
        RIGHT_EYE_INNER.visibility = 0
        RIGHT_EYE_OUTER.visibility = 0
        RIGHT_EAR.visibility = 0
        MOUTH_RIGHT.visibility = 0
        
        ## torso
        LEFT_KNEE = landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value]
        LEFT_SHOULDER = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
        LEFT_ELBOW = landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value]
        LEFT_HIP = landmarks[mp_pose.PoseLandmark.LEFT_HIP.value]
        RIGHT_KNEE = landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value]
        RIGHT_SHOULDER = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
        RIGHT_ELBOW = landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value]
        RIGHT_HIP = landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value]
        

        ### hand
        LEFT_PINKY = landmarks[mp_pose.PoseLandmark.LEFT_PINKY.value]
        LEFT_INDEX = landmarks[mp_pose.PoseLandmark.LEFT_INDEX.value]
        LEFT_THUMB = landmarks[mp_pose.PoseLandmark.LEFT_THUMB.value]
        LEFT_WRIST = landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value]
        RIGHT_PINKY = landmarks[mp_pose.PoseLandmark.RIGHT_PINKY.value]
        RIGHT_INDEX = landmarks[mp_pose.PoseLandmark.RIGHT_INDEX.value]
        RIGHT_THUMB = landmarks[mp_pose.PoseLandmark.RIGHT_THUMB.value]
        RIGHT_WRIST = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value]
        LEFT_PINKY.visibility = 0
        LEFT_INDEX.visibility = 0
        LEFT_THUMB.visibility = 0
        

        ## foot
        LEFT_FOOT_INDEX = landmarks[mp_pose.PoseLandmark.LEFT_FOOT_INDEX.value]
        LEFT_ANKLE = landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value]
        LEFT_HEEL = landmarks[mp_pose.PoseLandmark.LEFT_HEEL.value]
        RIGHT_FOOT_INDEX = landmarks[mp_pose.PoseLandmark.RIGHT_FOOT_INDEX.value]
        RIGHT_ANKLE = landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value]
        RIGHT_HEEL = landmarks[mp_pose.PoseLandmark.RIGHT_HEEL.value]
        LEFT_FOOT_INDEX.visibility = 0
        LEFT_HEEL.visibility = 0
        RIGHT_FOOT_INDEX.visibility = 0
        RIGHT_HEEL.visibility = 0


        if (visibile == 'left'):
            RIGHT_KNEE.visibility = 0
            RIGHT_SHOULDER.visibility = 0
            RIGHT_ELBOW.visibility = 0
            RIGHT_HIP.visibility = 0
            RIGHT_PINKY.visibility = 0
            RIGHT_INDEX.visibility = 0
            RIGHT_THUMB.visibility = 0
            RIGHT_WRIST.visibility = 0
            RIGHT_ANKLE.visibility = 0
        
        if (visibile == 'right'):
            LEFT_KNEE.visibility = 0
            LEFT_SHOULDER.visibility = 0
            LEFT_ELBOW.visibility = 0
            LEFT_HIP.visibility = 0
            LEFT_PINKY.visibility = 0
            LEFT_INDEX.visibility = 0
            LEFT_THUMB.visibility = 0
            LEFT_WRIST.visibility = 0
            LEFT_WRIST.visibility = 0
            LEFT_ANKLE.visibility = 0
        
    except:
        pass
    
    

    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    mp_drawing.draw_landmarks(
        image, 
        results.pose_landmarks,
        mp_pose.POSE_CONNECTIONS,
        drawing_spec_points,
        connection_drawing_spec=drawing_spec
    )
    return image
