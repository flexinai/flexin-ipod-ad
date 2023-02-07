# demo

# instructions

create virtual environment and activate it

run `pip install -r requirements.txt`

create silhouette videos by running `segmentation_mask.py` and passing in input path of the video or videos, and the output path to save the silhouette versions in, plus other options with defaults if they are not included:

- input path: `-i` or `--input`
- output path: `-o` or `--output`
- color name for background: `-b` or `--background` (default white)
- color name for person's silhouette: `-p` or `--person` (default black)
- enter threshold 1-9 (converted to 0.1 - 0.9) to adjust the segmentation between the person and the background: `-t` or `--threshold` (default 1)
- threshold limit for output of multiple videos with a threshold difference of 1 between them: `-l` or `--thresholdlimit` (default 1 video output per video input)
- seconds in video to switch background color on, separated by - : `-s` or `--switch`
- alternate background color to switch with the first color: `-a` or `altbackground`

to segment all videos in a Desktop folder called `my_videos` to a folder in this repo called `video_output` in black and white, an example could be:

- `python segmentation_mask.py -i ~/Desktop/my_videos/ -o ./video_output/`
- `python segmentation_mask.py -i ~/Desktop/my_videos -o ./video_output`

to segment one particular video in that folder examples could be:

- `python segmentation_mask.py -i ~/Desktop/my_videos/handstand.mp4 -o ./video_output/ -b aqua -p black -t 1.5`

  (video will be saved as `./video_output/handstand_silhouette_0pt15.mp4`)

- `python segmentation_mask.py -i ~/Desktop/my_videos/handstand.mp4 -o ./video_output/ -b aqua -p black -l 3`

  (videos will be saved as `./video_output/handstand_silhouette_0pt1.mp4`, `handstand_silhouette_0pt2.mp4`, `handstand_silhouette_0pt3.mp4`)

- `python segmentation_mask.py -i ~/Desktop/my_videos/handstand.mp4 -o ./video_output/ -b aqua -p black -s 0.7-3.58-5-7-9 -a fuchsia`

  (change between aqua and fuchsia at 0.7 seconds, 3.6 seconds (rounds from 3.58), 5 seconds, 7 seconds, and 9 seconds)

## overview

**summary**  
apple once made a visual style of ads that had a colorful background with a black silhouette of a dancer in the foreground. creating a similar effect using the blazepose model is what this demo is about. the demo shows the subject of the video as a silhouette in the foreground, the background of the video as a solid color. the demo shows the result of applying the effect to videos of athletes doing handstands and other more impossible skills.

**resources**

- [MediaPipe Pose](https://google.github.io/mediapipe/solutions/pose.html)
- hand-drawn rotoscope [gif](https://flexin.io/assets/images/image01.gif?v=50062a09) of Simon Ata doing a 360 degree human flag walk ([source video](https://www.youtube.com/watch?v=z4dUB0GzlN4))
- [ai](https://github.com/myth-software/ai)
- [lambdas](https://github.com/myth-software/lambdas)
- [segmentation mask with mediapipe in touchdesigner](http://www.magicandlove.com/blog/2022/04/15/segmentation-mask-with-mediapipe-in-touchdesigner/) and [script TOP](https://docs.derivative.ca/Script_TOP)

## techniques

**segmentation masking**  
this is the concept that makes a zoom video blur a background and keep the person on the video in focus. the blazepose models calculates the pixels in the video where there is a person or is a background and responds with confidence scores, that response is the segementation mask. while other applications blur background and leave the human untouched, we make the background all one color and the human all another color.

**pose-depdendent temporal landmarking**  
pose-dependent means conditioned upon the subject's orientation, as in, a handstand. temporal landmarking means marking that point in time, whether represented by milliseconds elapsed since the beginning of the video or by the frame of the video. this concept allows us to represent interesting parts of a video.

**flexion, extension, protraction, retraction, and posterior pelvic tilt**  
flexion loosely means motions that bend muscles, like lowering your arm from a raised position is the flexion movement of the arm from the shoulder joint and extension is the opposite, raising your arm from your side to overhead is the extension of the same. protraction loosely means motions that move muscles forwards, starting from the bottom of a pushup then pressing into the floor till there is no more range of motion leaves the body with full protracted shoulders, pressed forward in the direction of the floor and the opposite is retraction, an attempt to touch elbows behind the back results in shoulders pulling backwards behind the body in a retraction. posterior pelvic tilt is discussed often in the aesthetic of balance postures, achieved by appropriately engaging the glutes and the abs in such a manner that the natural curvature of the spine is counter-acted to give the side profile of the back a straight line. the libraries that we are using are not built to understand these concepts, analyze their presence in an image frame, or represent them visually, and they are all important for us as engineers to go after because our software is used by people whose lives and livelihoods are about mastering these techniques.

## deliverables

### final deliverables

- (1) a pose calculation function that goes farther than the current function by returning not only landmark data, segmentation mask data as well.
- (2) a video output function that accepts a video, segmentation mask data, pose-dependent temporal landmarks, and two colors as inputs to return a video that displays the subject in one color, the background in another, and only for the parts of the video that the temporal landmarks indicate are meaningful.
- (3) multiple videos demonstrating the capabilities of deliverables 1 and 2 along with a written description discussing the real-world conditions that produce results.

### intermediate deliverables

- (2a) a video output function that accepts a video and segmentation mask data that returns the person in black and the background in white.
- (2b) a video output function that accepts a video and temporal landmarks that returns the meaningless moments of the video in white and the meaningful moments in black, as in, only solid white or solid black is shown for all pixels in the video.
- (2c) a video output function that accepts a video and two colors and displays the brightest color on the left half of the video and the darkest color the right half of the video.

### immediate deliverables

- (1a) locally output a json file representing pose landmarks by referencing [ai](https://github.com/myth-software/ai) for running code locally and [lambdas/calculates-pose](https://github.com/myth-software/lambdas/tree/main/calculates-pose) for json representations
- (1b) same as 1a, now outputting segmentation mask data as json
- (1c) implement this [tutorial](http://www.magicandlove.com/blog/2022/04/15/segmentation-mask-with-mediapipe-in-touchdesigner/) implementation for modifying video using segmentation mask

## function signatures and types

provided to allow focus, not on form, on implementation of functions

```ts
/**
 * Pose
 * the data provided by blazepose as pose_landmarks
 */
type Pose = {};

/**
 * SegementationMask
 * the data provided by blazepose as segmentation_mask
 */
type SegmentationMask = {};

/**
 * Movement
 * a dict that combines references to all blazepose outputs
 */
type Movement = {
  pose: Pose;
  mask: SegementationMask;
};

/**
 * TemporalLandmark
 * whether frames or timestamps, a representation of the start and end of a
 * moment in the video that matters
 */
type TemporalLandmark = {};

/**
 * Color
 * whether bgr, rgb, hex, a representation of a single color
 */
type Color = {};

/**
 * Configuration
 * an array of moments and a tuple of colors
 */
type Configuration = {
  moments: TemporalLandmark[];
  colors: [Color, Color];
};

/**
 * Video
 * the path or url points to a video
 */
type Video = string;

/**
 * 1a.
 */
function calculatesPose(video: Video): Pose {}
/**
 * 1b.
 */
function calculatesSegmentationMask(video: Video): SegmentationMask {}
/**
 * 1c.
 */
function calculatesSegmentationMask(video: Video): SegmentationMask {}
function outputsTutorial(video: Video, mask: SegmentationMask): Video {}
/**
 * 2a.
 */
function calculatesSegmentationMask(video: Video): SegmentationMask {}
function outputsBlackWhite(video: Video, mask: SegmentationMask): Video {}
/**
 * 2b.
 */
function calculatesSegmentationMask(video: Video): SegmentationMask {}
function outputsMoments(video: Video, moments: TemporalLandmark[]): Video {}
/**
 * 2c.
 */
function calculatesSegmentationMask(video: Video): SegmentationMask {}
function outputsColors(video: Video, colors: [Color, Color]): Video {}
/**
 * 1.
 */
function calculatesMovement(video: Video): Movement {}
/**
 * 2.
 */
function outputsSilhouette(
  video: Video,
  movement: Movement,
  config: Configuration
): Video {}
```
