import cv2
import numpy as np
import argparse

def main():
    
    parser = argparse.ArgumentParser()

    parser.add_argument('-v','--video', type=str)
    parser.add_argument('-o','--output', type=str, default=None)

    args = parser.parse_args()
    
    vid = cv2.VideoCapture(args.video)

    width = int(vid.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(vid.get(cv2.CAP_PROP_FPS))
    codec = cv2.VideoWriter_fourcc('a','v','c','1')
    out = cv2.VideoWriter(args.output, codec, fps, (width, height))

    # model info: https://drive.google.com/file/d/1dCfozqknMa068vVsO2j_1FgZkW_e3VWv/preview
    # 0 = general, 144x256, "slower"
    # 1 = landscape, 256x256, "faster"
   
    while vid.isOpened():
        success, image = vid.read()
        if not success:
            print("ignoring empty video")
            break 

        y, x, z = image.shape
        print('image dimensions: x:', x, "by y:", y)

        # points are (y, x), thickness -1 for solid
        start_point = (70, 100)
        end_point = (140, 170)
        color= (0, 0, 0)
        thickness = -1
        # 720x1280 (portrait) handstand video at ../add_noise/sleeves.mp4

        # cv2.rectangle(image, (0, 0), (200, 200), (0, 0, 0), -1)
        cv2.rectangle(image, start_point, end_point, color, thickness) 

        out.write(image)
        cv2.imshow("Mediapipe Segmentation Mask", image)
        if cv2.waitKey(1) & 0xFF == 27:
            break
    vid.release()


if __name__ == "__main__":
    main()