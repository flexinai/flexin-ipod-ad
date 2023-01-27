import mediapipe as mp
import json

mp_pose = mp.solutions.pose

def calculate_pose(image, pose):
    results = pose.process(image)

    if (results.pose_landmarks == None):
        return {
            "error": "NO LANDMARKS"
        }

    landmarks = results.pose_landmarks.landmark
    
    landmarks_list = []
    for landmark in results.pose_landmarks.landmark:
        current_landmark = {"x": landmark.x, "y": landmark.y, "z": landmark.z, "visibility": landmark.visibility}
        landmarks_list.append(current_landmark)
    with open("json_output/landmarks_list.json", "w") as outfile:
        json.dump(landmarks_list, outfile, indent=2)

    landmarks_x_y_z_visibility = {}
    for l in mp_pose.PoseLandmark:
      # print(l.name)
      landmarks_x_y_z_visibility[l.name.lower()] = {
          "x": landmarks[l.value].x,
          "y": landmarks[l.value].y,
          "z": landmarks[l.value].z,
          "visibility": landmarks[l.value].visibility,
    }
    # would be nice to extract the filename from args.video or args.output & add to json filename
    with open(f"json_output/landmarks_with_labels.json", "w") as outfile:
      json.dump(landmarks_x_y_z_visibility, outfile, indent=2)
    return landmarks_x_y_z_visibility