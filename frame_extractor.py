import cv2
import os
import argparse
from scenedetect import VideoManager, SceneManager
from scenedetect.detectors import ContentDetector


def initialize_scene_detection(video_path):
    """Initializes the VideoManager and SceneManager for scene detection."""
    video_manager = VideoManager([video_path])
    scene_manager = SceneManager()
    scene_manager.add_detector(ContentDetector())

    video_manager.set_downscale_factor()
    video_manager.start()

    return video_manager, scene_manager


def detect_scenes(video_manager, scene_manager):
    """Detects scenes in the video and returns a list of scenes."""
    scene_manager.detect_scenes(frame_source=video_manager)
    return scene_manager.get_scene_list()


def capture_first_frames(scene_list, video_path, fps):
    """Captures the first frame of each scene and returns them with their start times."""
    cap = cv2.VideoCapture(video_path)
    first_frames = []

    for scene in scene_list:
        start_frame = scene[0].get_frames()
        start_time = start_frame / fps  # Convert frame to seconds

        cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
        ret, frame = cap.read()
        if ret:
            first_frames.append((frame, start_time))  # Append the frame and its start time

    cap.release()
    return first_frames


def extract_first_frames_of_shots(video_path):
    """Extracts the first frame of each detected shot in the video."""
    video_manager, scene_manager = initialize_scene_detection(video_path)
    scene_list = detect_scenes(video_manager, scene_manager)

    fps = cv2.VideoCapture(video_path).get(cv2.CAP_PROP_FPS)  # Get FPS once
    first_frames = capture_first_frames(scene_list, video_path, fps)

    video_manager.release()
    return first_frames


def save_frames_to_disk(frames, output_dir):
    """Saves the extracted frames to disk with filenames based on frame index and timestamp."""
    os.makedirs(output_dir, exist_ok=True)

    for idx, (frame, start_time) in enumerate(frames):
        file_path = os.path.join(output_dir, f"frame_{idx}_{start_time:.2f}.jpg")
        cv2.imwrite(file_path, frame)
        print(f"Saved {file_path}")


def parse_arguments():
    """Parses command-line arguments and returns them."""
    parser = argparse.ArgumentParser(description="Extract first frames of each shot from a video.")

    parser.add_argument('video_path', type=str, help="Path to the input video file.")
    parser.add_argument('output_dir', type=str, help="Directory to save the extracted frames.")

    return parser.parse_args()


# Example usage
if __name__ == "__main__":
    args = parse_arguments()

    frames = extract_first_frames_of_shots(args.video_path)
    save_frames_to_disk(frames, args.output_dir)
