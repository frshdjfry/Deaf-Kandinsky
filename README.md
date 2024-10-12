# Deaf Kandinsky: Multi-Track Music Generation Based on Frame Colors

Deaf Kandinsky is a project that generates multi-track music based on the colors present in the frames of a movie. It uses the 12-tone system and randomly applies variations such as inversion, retrograde, and retrograde-inversion to create a unique, experimental soundscape for each film. The generated music adapts to the colors in different frames of the film and randomizes note durations to add an experimental feel.

The project consists of three scripts:
1. `frame_extractor.py`: Extracts individual frames from a movie.
2. `image_processing.py`: Processes each frame to detect the colors and timing information.
3. `note_gen.py`: Generates MIDI music based on the color data extracted from the frames.

This approach was used in the short experimental films "Deaf Kandinsky" and "Glaucoma."

## How to Use the Project

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

## Project Overview

### Concept
The project aims to generate multi-track music that is tied to the visual elements of a movie, specifically based on colors in each frame. The result is an evolving soundscape where each track corresponds to a different color, and the music reflects the color dynamics throughout the film.

### 12-Tone System
The project uses the 12-tone technique, popularized by composers like Arnold Schoenberg. In this system, all 12 notes of the chromatic scale are treated as equal, and a tone row (a sequence of the 12 notes) is chosen. This tone row can be manipulated in several ways:
- **Prime**: The original form of the tone row.
- **Inversion**: The intervals between notes are inverted.
- **Retrograde**: The tone row is played backward.
- **Retrograde-Inversion**: The tone row is played backward with inverted intervals.

Each note's duration is also chosen randomly, adding an additional element of experimentation.

### Usage in Experimental Films
This method was applied in two short experimental films, *"Deaf Kandinsky"* and *"Glaucoma"*, where the music's form and evolution were influenced directly by the visual elements of the films.

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
## License
This project is released under the MIT License. See the LICENSE file for more details.
