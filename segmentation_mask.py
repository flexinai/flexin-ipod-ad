import cv2
import mediapipe as mp
import numpy as np
import argparse
import pathlib

mp_segmentation = mp.solutions.selfie_segmentation.SelfieSegmentation


def main():
    
    parser = argparse.ArgumentParser()

    parser.add_argument('-v','--video', type=str)
    parser.add_argument('-o','--output', type=str, default=None)

    parser.add_argument('-i','--input', type=str)
    parser.add_argument('-l', '--thresholdlimit', type=str)

    args = parser.parse_args()
    
    if args.video:
    # https://google.github.io/mediapipe/solutions/selfie_segmentation.html
        vid = cv2.VideoCapture(args.video)
        print(args.video, type(args.video))
        width = int(vid.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = int(vid.get(cv2.CAP_PROP_FPS))
        codec = cv2.VideoWriter_fourcc('a','v','c','1')
        out = cv2.VideoWriter(args.output, codec, fps, (width, height))
        threshold = 0.1 # create arg to pass for threshold?
        segment_video(vid, out, threshold)

    if args.input:
        in_dir = str(args.input)
        if args.input[-1] != "/":
            in_dir = in_dir + "/"
        input_path = pathlib.Path(in_dir).glob('*.mp4')

        out_dir = str(args.output)
        if args.output[-1] != "/":
            out_dir = out_dir + "/"

        for video in input_path:
            if args.thresholdlimit:
                limit = int(args.thresholdlimit) + 1
            else:
                limit = 10
            for i in range(1,limit,1):
                threshold = round(i*0.1, 1)

                split_path = str(video).split('/')
                video_name = split_path[-1][:-4]
                video_path = str(video)

                print(f"processing {video_name}.mp4 with a threshold of {threshold} ...")

                vid = cv2.VideoCapture(video_path)

                width = int(vid.get(cv2.CAP_PROP_FRAME_WIDTH))
                height = int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
                fps = int(vid.get(cv2.CAP_PROP_FPS))
                codec = cv2.VideoWriter_fourcc('a','v','c','1')

                out = cv2.VideoWriter(f'{out_dir}{video_name}_0pt{round(threshold*10)}.mp4', codec, fps, (width, height))

                segment_video(vid, out, threshold)


def segment_video(vid, out, threshold):
    BG_COLOR = (255,255,255)
    FG_COLOR = (0,0,0)

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

            # threshold = 0.4 # value between 0 and 1, example code used 0.1
            condition = np.stack((results.segmentation_mask,) * 3, axis=-1) > threshold
            if bg_image is None:
                bg_image = np.zeros(image.shape, dtype=np.uint8)
                bg_image[:] = BG_COLOR
                # fg_image = image
                # fg_image[:] = FG_COLOR
            # output_image = np.where(condition, fg_image, bg_image)
            output_image = np.where(condition, image, bg_image)

            out.write(output_image)
            cv2.imshow("Mediapipe Segmentation Mask", output_image)
            if cv2.waitKey(1) & 0xFF == 27:
                break
    vid.release()


if __name__ == "__main__":
    main()

