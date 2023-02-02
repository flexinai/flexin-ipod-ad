import cv2
import argparse
import pathlib

# function written by Ben Chuanlong Du: https://www.legendu.net/en/blog/python-opencv-python/
# removes sound for some reason?
def video_to_mp4(
    input, output, fps: int = 0, frame_size: tuple = (), fourcc: str = "H264"
):
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

    print(f"converting '{input}'...")

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

    in_dir = str(args.input)
    if args.input[-1] != "/":
        in_dir = in_dir + "/"

    out_dir = str(args.output)
    if args.output[-1] != "/":
        out_dir = out_dir + "/"

    def process_video(video_path):
        in_path = str(video_path)
        split_path = in_path.split('/')
        video_name = split_path[-1][:-4]
        out_path = f"{out_dir}{video_name}.mp4"
        video_to_mp4(in_path, out_path)
        
    
    input_path_lower = pathlib.Path(in_dir).glob('*.mov')
    input_path_upper = pathlib.Path(in_dir).glob('*.MOV')
    
    for video_path in input_path_lower:
        process_video(video_path)

    for video_path in input_path_upper:
        process_video(video_path)

if __name__ == "__main__":
    main()