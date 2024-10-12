import re
import cv2
import os
import numpy as np
import argparse
import json

# HSV color mappings
color_hsv_mapping = {
    'red': ([0, 120, 70], [10, 255, 255], [160, 120, 70], [180, 255, 255]),
    'blue': ([90, 50, 70], [119, 255, 255]),
    'green': ([36, 50, 70], [89, 255, 255]),
    'yellow': ([15, 120, 70], [35, 255, 255]),
    'orange': ([10, 50, 70], [20, 255, 255]),
    'purple': ([120, 77, 100], [160, 255, 255])
}


def parse_time_from_filename(filename):
    match = re.search(r'frame_(\d+\.*\d*)_(\d+\.\d+).jpg', filename)
    if match:
        frame_id = float(match.group(1))
        time = float(match.group(2))
        return frame_id, time
    else:
        print(f"Could not parse time from filename: {filename}")
        return None, 0


def read_images_from_directory(directory):
    filenames = [f for f in os.listdir(directory) if f.endswith('.jpg')]
    frame_data = [parse_time_from_filename(filename) for filename in filenames]
    frame_data.sort()

    sorted_filenames = [
        f"{int(frame[0])}_{frame[1]:.2f}.jpg" if frame[0].is_integer() else f"{frame[0]}_{frame[1]:.2f}.jpg" for frame
        in frame_data]
    times = [frame[1] for frame in frame_data]
    end_times = times[1:] + [times[-1] + (times[-1] - times[-2])]

    frame_times = [{'filename': sorted_filenames[i], 'start_time': times[i], 'end_time': end_times[i]} for i in
                   range(len(times))]

    result = []
    for frame in frame_times:
        image_path = os.path.join(directory, 'frame_' + frame['filename'])
        img = cv2.imread(image_path)
        if img is not None:
            result.append((img, frame['start_time'], frame['end_time']))
        else:
            print(f"Could not read image at path: {image_path}")
    return result


def extract_regions_by_color(image, just_biggest=True):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    output_regions = {}

    for color, ranges in color_hsv_mapping.items():
        mask = np.zeros(hsv.shape[:2], dtype=np.uint8)
        for i in range(0, len(ranges), 2):
            lower = np.array(ranges[i], dtype=np.uint8)
            upper = np.array(ranges[i + 1], dtype=np.uint8)
            mask += cv2.inRange(hsv, lower, upper)

        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if just_biggest and contours:
            max_area = 0
            biggest_one = None
            for cnt in contours:
                if cv2.contourArea(cnt) > max_area:
                    max_area = cv2.contourArea(cnt)
                    biggest_one = cnt
            contours = [biggest_one]

        output_regions[color] = (mask, contours)

    return output_regions


def save_results_to_json(results, output_file):
    """Saves the results to a JSON file."""
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=4)
    print(f"Results saved to {output_file}")


def load_and_process_images(directory_path):
    images_with_times = read_images_from_directory(directory_path)
    all_result = []

    for img, start_time, end_time in images_with_times:
        color_regions = extract_regions_by_color(img)
        for color, (mask, contours) in color_regions.items():
            if contours:
                merged_regions = group_horizontal_regions(contours)
                draw_bounding_boxes(img, merged_regions)
                segment_mappings = map_boxes_to_segments(merged_regions, img, start_time, end_time, color)
                print(f"Color: {color}, Mappings: {segment_mappings}")
                all_result.extend(segment_mappings)

        cv2.imshow(f'Processed Image', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    return all_result


def main(directory, output_json):
    """Main function to process the directory images and save results to JSON."""
    all_results = load_and_process_images(directory)
    save_results_to_json(all_results, output_json)


def parse_arguments():
    parser = argparse.ArgumentParser(description="Process images in a directory and detect colored regions.")
    parser.add_argument('directory', type=str, help="Directory containing images to process.")
    parser.add_argument('--output_json', type=str, default='results.json', help="Output JSON file to save the results.")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    main(args.directory, args.output_json)
