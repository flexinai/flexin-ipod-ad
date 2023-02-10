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
   
    while vid.isOpened():
        success, image = vid.read()
        if not success:
            print("ignoring empty video")
            break 
        
        cv2.imshow("before", image)

        max_x, max_y, z = image.shape
        # print('image dimensions: x:', max_x, "by y:", max_y)

        # points are (y, x), thickness -1 for solid
        start_point = (154, 170)
        end_point = (500, 1200)
        # setting for 720x1280 (portrait) handstand video at ../add_noise/sleeves.mp4

        # draw red rectangle around area
        # line_color= (0, 0, 255)
        # line_thickness = 3
        # cv2.rectangle(image, start_point, end_point, line_color, line_thickness) 

        # exclude area outside rectangle
        start_y, start_x = start_point
        end_y, end_x = end_point
        mask = np.zeros(image.shape[:2],np.uint8)
        mask[start_x:end_x,start_y:end_y] = 255
        image = cv2.bitwise_and(image,image,mask = mask)

        out.write(image)
        cv2.imshow("after", image)
        if cv2.waitKey(1) & 0xFF == 27:
            break
    vid.release()

if __name__ == "__main__":
    main()

# https://stackoverflow.com/questions/11492214/opencv-via-python-is-there-a-fast-way-to-zero-pixels-outside-a-set-of-rectangle
# img = cv2.imread('testimg.jpeg')
# start_x = 30
# start_y = 30
# end_x = 200
# end_y = 100

# mask = np.zeros(img.shape[:2],np.uint8)
# mask[start_y:start_y+end_y,start_x:start_x+end_x] = 255
# result = cv2.bitwise_and(img,img,mask = mask)
# cv2.imshow("result", result)