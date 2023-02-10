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
    parser.add_argument('-a', '--altbackground', type=str)
    parser.add_argument('-p', '--person', type=str)
    parser.add_argument('-t', '--threshold', type=float)
    parser.add_argument('-l', '--thresholdlimit', type=int)
    parser.add_argument('-s', '--switch', type=str)
    parser.add_argument('--start_y', type=int)
    parser.add_argument('--start_x', type=int)
    parser.add_argument('--end_y', type=int)
    parser.add_argument('--end_x', type=int)
    # for peter's "sleeves" handstand video with "noise" added using create_noise.py, pass: 
    # --start_y 154 --start_x 170 --end_y 500 --end_x 1200

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

            background = args.background
            if args.background == None:
                background = 'white'
            if args.altbackground == None:
                alt_background = background
            else:
                 alt_background = args.altbackground

            if args.start_y:
                start_y = args.start_y
            else:
                start_y = None
            if args.start_x:
                start_x = args.start_x
            else:
                start_x = None
            if args.end_y:
                end_y = args.end_y
            else:
                end_y =  None
            if args.end_x: 
                end_x = args.end_x
            else:
                end_x = None

            segment_video(vid, out, threshold, args.switch, background, alt_background, args.person, start_y, start_x, end_y, end_x)
            print(f'Video saved to: {out_dir}{video_name}_silhouette_{threshold_notation}.mp4')
    
    split_input = args.input.split('/')
    if '.' in split_input[-1]:
        # pass one video to threshold handling, after limit is set below
        video = args.input
    else:
        # prepare directory for loop to pass each video to threshold handling, after limit is set below
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
           
def segment_video(vid, out, threshold, switch, bg, bg2, person, start_y, start_x, end_y, end_x):
    # get number of images (frames) in video
    frame_total = int(vid.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = int(vid.get(cv2.CAP_PROP_FPS))

    if switch == None:
        switch = "0-0"
    switch_seconds = switch.split('-')
    switch_frame_list = [0]
    for switch in switch_seconds:
        switch = float(switch)
        switch_frame = round(switch, 1) * fps
        switch_frame_list.append(switch_frame)
    switch_frame_list.append(frame_total)

    for value in switch_frame_list:
        if value > frame_total:
            switch_frame_list.remove(value)
        
    bg_colors = [webcolors.name_to_rgb(bg, spec=u'css3'), webcolors.name_to_rgb(bg2, spec=u'css3')]
    # bg_colors = [webcolors.name_to_rgb(bg, spec=u'css3'), webcolors.name_to_rgb(bg2, spec=u'css3'), (255,215,0)] # test rotating in a 3rd color
    BG_COLOR = (255,255,255)
    
    if person == None:
        FG_COLOR = (0,0,0)
    else:
        FG_COLOR = webcolors.name_to_rgb(person, spec=u'css3')

    # model info: https://drive.google.com/file/d/1dCfozqknMa068vVsO2j_1FgZkW_e3VWv/preview
    # 0 = general, 144x256, "slower"
    # 1 = landscape, 256x256, "faster"
    with mp_segmentation(model_selection=1) as segmentation:
        bg_image = None

        frame_index = 0
        switch_frame_index = 1
        bg_color_index = 1
        while vid.isOpened():
            BG_COLOR = bg_colors[bg_color_index]
            frame_index += 1
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
            image.flags.writeable = True

            # cv2.COLOR_RGB2BGR convert order of colors from how cv2 arranges them back to RGB
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR) 

            # threshold = value between 0 and 1, example code used 0.1
            condition = np.stack((person,) * 3, axis=-1) > threshold

            # if bg_image is None: # removed this and un-indented next 2 lines to enable change of background color
            bg_image = np.zeros(image.shape, dtype=np.uint8)

            # attempt to integrate code from exclusion.py - so far has no effect
            if None not in [start_y, start_x, end_y, end_x]:
                # print('running rectangle mask')
                mask = np.zeros(image.shape[:2],np.uint8)
                mask[start_x:end_x,start_y:end_y] = 255
                # image = cv2.bitwise_and(image,image,mask = mask)
                # # draw red rectangle around area
                # line_color= (0, 0, 255)
                # line_thickness = 3
                # cv2.rectangle(image, (start_y, start_x), (end_y, end_x), line_color, line_thickness) 

            bg_image[:] = BG_COLOR
            output_image = np.where(condition, image, bg_image)

            silhouette = cv2.bitwise_not(output_image)
            silhouette = np.ones(silhouette.shape, dtype=np.uint8)
            silhouette[:] = FG_COLOR # red comes out blue here due to RGB / BGR
            
            if frame_index == int(switch_frame_list[switch_frame_index]):
                switch_frame_index += 1
                bg_color_index = switch_frame_index % 2
                # bg_color_index = switch_frame_index % 3 # test rotating in a 3rd color
                BG_COLOR = bg_colors[bg_color_index]

            silhouette_image = np.where(condition, silhouette, bg_image)
            silhouette_image = cv2.cvtColor(silhouette_image, cv2.COLOR_BGR2RGB)

            # # draws red rectangle over tape measure in pushup video
            # y, x, z = silhouette_image.shape
            # print('image dimensions', x, "by", y) # (y,x) in coords below
            # cv2.rectangle(image, start_point, end_point, color, thickness) thickness -1 for solid
            # cv2.rectangle(silhouette_image, (1600,750), (1725, 850), (0, 0, 255), -1)
            
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

