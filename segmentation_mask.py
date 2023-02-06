import cv2
import mediapipe as mp
import numpy as np
import argparse
import pathlib
import webcolors

mp_segmentation = mp.solutions.selfie_segmentation.SelfieSegmentation

def main():
    
    parser = argparse.ArgumentParser()

    parser.add_argument('-i','--input', type=str)
    parser.add_argument('-o','--output', type=str, default=None)
    parser.add_argument('-b', '--background', type=str)
    parser.add_argument('-p', '--person', type=str)
    parser.add_argument('-t', '--threshold', type=float)
    parser.add_argument('-l', '--thresholdlimit', type=int)

    args = parser.parse_args()

    def handle_thresholds(input, threshold_x10, limit, output):
        for i in range(1,limit,1):
            if limit == 2:
                threshold = round(threshold_x10*0.1, 2)
            else:
                threshold = round(i*0.1, 2)
            split_inpath = input.split('/')
            split_outpath = output.split('/')[:-1]
            if '.' in split_outpath:
                out_dir = '/'.join(split_outpath) + '/'
            else:
                out_dir = args.output
            video_name = split_inpath[-1][:-4]
            threshold_notation = str(threshold).replace('.', 'pt')
            
            print(f"processing {video_name}.mp4 with a threshold of {threshold} ...")

            vid = cv2.VideoCapture(input)

            width = int(vid.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
            fps = int(vid.get(cv2.CAP_PROP_FPS))
            codec = cv2.VideoWriter_fourcc('a','v','c','1')
            out = cv2.VideoWriter(f'{out_dir}{video_name}_silhouette_{threshold_notation}.mp4', codec, fps, (width, height))

            segment_video(vid, out, threshold, args.background, args.person)
            print(f'Video saved to: {out_dir}{video_name}_silhouette_{threshold_notation}.mp4')
    
    split_input = args.input.split('/')
    if '.' in split_input[-1]:
        # pass one video to threshold handling, after limit is set below
        video = args.input
    else:
        # prepare directory for loop to pass each video tothreshold handling, after limit is set below
        in_dir = str(args.input)
        if args.input[-1] != "/":
            in_dir = in_dir + "/"
        input_path = pathlib.Path(in_dir).glob('*.mp4')

    out_dir = str(args.output)
    if args.output[-1] != "/":
        out_dir = out_dir + "/"

    if args.thresholdlimit == None:
    # process video(s) with one threshold passed by user (or default of 0.1)
        limit = 2
        if args.threshold == None:
            threshold_x10 = 1
            print("\nYou entered no threshold and no limit")
        else:
            threshold_x10 = args.threshold  
            print(f"\nYou entered a threshold of {threshold_x10} but no limit")
            print("Using a limit of", limit-1)
    else:
    # process video(s) with a threshold for every 0.1 up to limit passed
        if args.thresholdlimit > 9:
            limit = 10
        else:
            limit = args.thresholdlimit + 1
            threshold_x10 = limit # unnecessary but function requires a parameter for threshold_x10
    
    if '.' in split_input[-1]:
        handle_thresholds(video, threshold_x10, limit, args.output)
    else:
        for video in input_path:
            print("Using a limit of", limit-1)
            print(in_dir, video)

            handle_thresholds(str(video), threshold_x10, limit, args.output)
           
def segment_video(vid, out, threshold, bg='white', person='black'):

    # need error handling for colors (mispellings, if they choose a black background and don't specifiy the person)
    if bg == None:
        BG_COLOR = (255,255,255)
    else:
        BG_COLOR = webcolors.name_to_rgb(bg, spec=u'css3')
    
    if person == None:
        FG_COLOR = (0,0,0)
    else:
        FG_COLOR = webcolors.name_to_rgb(person, spec=u'css3')

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

            person = results.segmentation_mask

            # cv2.imshow('Segmentation Mask', person)
            # print(person)

            # after processing, so you can change the color?
            image.flags.writeable = True
            # cv2.COLOR_RGB2BGR convert order of colors from how cv2 arranges them back to RGB
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR) 

            # threshold = value between 0 and 1, example code used 0.1
            condition = np.stack((person,) * 3, axis=-1) > threshold
            # axis=0: operands could not be broadcast together with shapes (3,1280,720) (1280,720,3) (1280,720,3)
            if bg_image is None:
                bg_image = np.zeros(image.shape, dtype=np.uint8)
                bg_image[:] = BG_COLOR
            output_image = np.where(condition, image, bg_image)
            # output_image = np.where(condition, person, bg_image)
            # ...operands could not be broadcast together with shapes (1280,720,3) (1280,720) (1280,720,3)

            silhouette = cv2.bitwise_not(output_image)
            silhouette = np.ones(silhouette.shape, dtype=np.uint8) # all black
            silhouette[:] = FG_COLOR # red comes out blue here due to RGB / BGR
            silhouette_image = np.where(condition, silhouette, bg_image)
            silhouette_image = cv2.cvtColor(silhouette_image, cv2.COLOR_BGR2RGB)
            cv2.imshow("preview", silhouette_image)
            out.write(silhouette_image)
            
            # UNCOMMENT TO GET IMAGE OF PERSON INSTEAD OF SOLID COLOR SILHOUETTE
            # out.write(output_image)
            # out.write(person)
            # cv2.imshow("Mediapipe Segmentation Mask", output_image)

            if cv2.waitKey(1) & 0xFF == 27:
                break
    vid.release()


if __name__ == "__main__":
    main()

