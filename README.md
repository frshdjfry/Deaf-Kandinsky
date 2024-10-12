# Deaf Kandinsky: Multi-Track Music Generation from Film Colors


### Overview
Deaf Kandinsky explores the connection between visual art and music, drawing on Wassily Kandinsky's theory of synesthesia, where colors can evoke corresponding sounds. The project analyzes the dominant colors in film frames to generate multi-track music, applying the 12-tone system to create compositions that reflect the visual dynamics of each scene. 

This approach has been used in experimental films like [*"Deaf Kandinsky (2024)"*](https://vimeo.com/1018871372) and [*"Glaucoma (2023)"*](https://vimeo.com/1017605789), where the soundtrack is directly influenced by the film’s visual elements.

Inspired by Arnold Schoenberg’s 12-tone technique, each note in the chromatic scale is treated equally, and a tone row is selected. The row can be transformed in several ways:
- **Prime**: The original form of the tone row.
- **Inversion**: Reverses the intervals between notes.
- **Retrograde**: Plays the tone row backward.
- **Retrograde-Inversion**: Plays the row backward with inverted intervals.


## How to Use the Project

The project consists of three scripts:
1. `frame_extractor.py`: Extracts individual frames from a movie.
2. `image_processing.py`: Processes each frame to detect the colors and timing information.
3. `note_gen.py`: Generates MIDI music based on the color data extracted from the frames.


## Requirements

- Python 3.x
- Libraries:
  - `opencv-python` (`cv2`)
  - `pretty_midi`
  - `mido`
  - `numpy`
  - `scenedetect`

Install the required libraries by running:
```
pip install opencv-python pretty_midi mido numpy scenedetect
```

### Step 1: Frame Extraction with `frame_extractor.py`

The first step is to extract frames from a movie. Each frame will later be analyzed to determine its color content.

#### Command Example
```
python frame_extractor.py input_video.mp4 output_frames_directory
```

- **input_video.mp4**: The path to the movie file from which you want to extract frames.
- **output_frames_directory**: The directory where the extracted frames will be saved.

### Step 2: Image Processing with `image_processing.py`

Once the frames are extracted, this script processes each frame to detect dominant colors, along with timing and segmentation information.

#### Command Example
```
python image_processing.py extracted_frames_directory output_data.json
```

- **extracted_frames_directory**: The directory containing the extracted frames from the previous step.
- **output_data.json**: The JSON file where the color and timing data will be saved for further processing.

### Step 3: MIDI Generation with `note_gen.py`

After the color and timing data has been generated, this script uses the 12-tone system to compose MIDI music. The music is based on the detected colors and the timing information from each frame. It randomly chooses between using the tone row, inversion, retrograde, and retrograde-inversion, as well as random note durations.

#### Command Example
```
python note_gen.py output_data.json --output generated_music.mid
```

- **output_data.json**: The JSON file containing color and timing information (from Step 2).
- **--output generated_music.mid**: The optional parameter to specify the output MIDI file. If not provided, it will default to `output.mid`.

## License
This project is released under the MIT License. See the LICENSE file for more details.
