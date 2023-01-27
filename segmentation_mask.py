import cv2
import mediapipe as mp
import numpy as np
import argparse

mp_segmentation = mp.solutions.selfie_segmentation.SelfieSegmentation

def main():
    
    parser = argparse.ArgumentParser()

    parser.add_argument('-v','--video', type=str)
    parser.add_argument('-o','--output', type=str, default=None)

    args = parser.parse_args()
    
    # https://google.github.io/mediapipe/solutions/selfie_segmentation.html
    BG_COLOR = (255,255,255)
    vid = cv2.VideoCapture(args.video)

    width = int(vid.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(vid.get(cv2.CAP_PROP_FPS))
    codec = cv2.VideoWriter_fourcc('a','v','c','1')
    out = cv2.VideoWriter(args.output, codec, fps, (width, height))

    # model info: https://drive.google.com/file/d/1dCfozqknMa068vVsO2j_1FgZkW_e3VWv/preview
    # 0 = general, 144x256, "slower"
    # 1 = landscape, 256x256, "faster"
    with mp_segmentation(model_selection=1) as segmentation:
        bg_image = None
        while vid.isOpened():
            success, image = vid.read()
            if not success:
                print("ignoring empty video")
                break # If loading a video, use 'break' instead of 'continue'.
            # cv2.COLOR_BGR2RGB convert order of colors to how cv2 imread() expects them
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) 
            # took out cv2.flip(image, 1) from sample code that was intended to handle selfie camera

            # To improve performance, optionally mark the image as not writeable to pass by reference.
            image.flags.writeable = False
            results = segmentation.process(image)

            # after processing, so you can change the color?
            image.flags.writeable = True
            # cv2.COLOR_RGB2BGR convert order of colors from how cv2 arranges them back to RGB
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR) 

            # look into this more: To improve segmentation around boundaries, consider applying a joint bilateral filter to "results.segmentation_mask" with "image"
            condition = np.stack((results.segmentation_mask,) * 3, axis=-1) > 0.1
            if bg_image is None:
                bg_image = np.zeros(image.shape, dtype=np.uint8)
                bg_image[:] = BG_COLOR
            output_image = np.where(condition, image, bg_image)

            out.write(output_image)
            cv2.imshow("Mediapipe Segmentation Mask", output_image)
            if cv2.waitKey(1) & 0xFF == 27:
                break
    vid.release()


if __name__ == "__main__":
    main()