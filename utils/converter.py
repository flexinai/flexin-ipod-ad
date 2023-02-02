import cv2
import argparse
import time

# function written by Ben Chuanlong Du: https://www.legendu.net/en/blog/python-opencv-python/
# removes sound for some reason?
def video_to_mp4(
    input, output, fps: int = 0, frame_size: tuple = (), fourcc: str = "H264"
):
    print(input, type(input))
    vidcap = cv2.VideoCapture(input)
    if not fps:
        fps = round(vidcap.get(cv2.CAP_PROP_FPS))
    success, arr = vidcap.read()
    if not frame_size:
        height, width, _ = arr.shape
        frame_size = width, height
    writer = cv2.VideoWriter(
        output,
        apiPreference=0,
        fourcc=cv2.VideoWriter_fourcc(*fourcc),
        fps=fps,
        frameSize=frame_size,
    )

    print(f"converting '{input}' ...")

    while True:
        if not success:
            break
        writer.write(arr)
        success, arr = vidcap.read()
    writer.release()
    vidcap.release()
    print(f"...finished conversion: {output}")

# code written by me
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i','--input', type=str)
    parser.add_argument('-o','--output', type=str, default=None)

    args = parser.parse_args()

    print(type(args.input))
    video_to_mp4(args.input, args.output)

if __name__ == "__main__":
    main()