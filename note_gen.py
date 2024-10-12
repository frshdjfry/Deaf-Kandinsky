import json
import math
import random
import pretty_midi
import argparse


class MIDIGenerator:
    def __init__(self, tempo=120, base_note=60):
        self.tone_row = self.generate_tone_row()
        self.tempo = tempo
        self.base_note = base_note
        self.mid = pretty_midi.PrettyMIDI(initial_tempo=tempo)
        self.ticks_per_beat = 480  # Default in pretty_midi
        self.seconds_to_ticks = self.ticks_per_beat * self.tempo // 60
        self.durations = [
            self.ticks_per_beat * 16,
            self.ticks_per_beat * 32,
        ]
        self.octave_range = (2, 5)
        self.channel_instrument_map = {
            'red': 1,
            'blue': 40,
            'green': 70,
            'yellow': 50,
            'orange': 60,
            'purple': 90
        }
        self.track_map = {}  # Maps instruments to their respective tracks

    def add_repeating_notes(self, instrument, note, start_time, duration, octave_shift, velocity=100, probability=0.01):
        if random.random() < probability:
            next_start_time = self.add_note_events(instrument, note, start_time, duration / 2, octave_shift, velocity)
            next_start_time = self.add_note_events(instrument, note, next_start_time, duration / 2, octave_shift, velocity)
            return next_start_time
        else:
            next_start_time = self.add_note_events(instrument, note, start_time, duration, octave_shift, velocity)

        return next_start_time

    def add_note_events(self, instrument, note, start_time, duration, octave_shift, velocity=100):
        note_duration = duration / self.seconds_to_ticks
        note_number = self.base_note + note + (octave_shift * 12)
        note_number = max(0, min(note_number, 127))

        end_time = start_time + note_duration
        midi_note = pretty_midi.Note(velocity=velocity, pitch=note_number, start=start_time, end=end_time)
        instrument.notes.append(midi_note)
        return end_time

    def populate_track(self, track, notes, area, start_time, end_time, density):
        accumulated_time = 0
        base_start_time = start_time

        while accumulated_time < end_time - base_start_time:
            notes_variation = self.get_variation(notes)
            octave_shift = self.randomize_octaves()
            for note in notes_variation:
                duration = self.get_random_duration(area)
                if not self.should_rest(density):
                    next_start_time = self.add_repeating_notes(track, note, start_time, duration, octave_shift)
                else:
                    next_start_time = start_time + (duration / self.seconds_to_ticks)
                accumulated_time += duration / self.seconds_to_ticks
                start_time = next_start_time
                if accumulated_time >= end_time - start_time:
                    break
            if accumulated_time >= end_time - base_start_time:
                break

    def create_track(self, instrument_id):
        if instrument_id not in self.track_map:
            instrument = pretty_midi.Instrument(program=instrument_id)
            self.mid.instruments.append(instrument)
            self.track_map[instrument_id] = instrument
        return self.track_map[instrument_id]

    def generate_tracks(self, data):
        for entry in data:
            track = self.create_track(self.channel_instrument_map[entry['color']])
            self.populate_track(
                track,
                self.get_notes_ad_indices(entry['segments']),
                entry['area'],
                entry.get('start_time', 0),
                entry['end_time'],
                entry.get('percentage', 100) / 100
            )

    def randomize_octaves(self):
        min_octave_shift = max(-2, -(self.base_note // 12))
        max_octave_shift = min(2, (127 - self.base_note) // 12)
        return random.randint(min_octave_shift, max_octave_shift)

    def get_variation(self, row):
        variations = [self.prime, self.inverted, self.retrograde, self.retrograde_inverted]
        return random.choice(variations)(row)

    def prime(self, row):
        return row

    def inverted(self, row):
        return [12 - note for note in row]

    def retrograde(self, row):
        return row[::-1]

    def retrograde_inverted(self, row):
        return [12 - note for note in self.retrograde(row)]

    def get_random_duration(self, area):
        num_durations = len(self.durations)
        midpoint = num_durations / 2
        weights = [(1 / (1 + math.exp(-10 * (area - (i / num_durations))))) for i in range(num_durations)]
        total_weight = sum(weights)
        normalized_weights = [w / total_weight for w in weights]
        selected_duration = random.choices(self.durations, weights=normalized_weights, k=1)[0]
        return selected_duration

    def should_rest(self, density):
        return random.random() > density

    def generate_tone_row(self):
        numbers = []
        while len(numbers) < 12:
            randed = random.randint(0, 11)
            if randed not in numbers:
                numbers.append(randed)
        return list(numbers)

    def get_notes_ad_indices(self, indices):
        return [self.tone_row[index] for index in indices]

    def save_midi(self, filename='output.mid'):
        self.mid.write(filename)


def load_data_from_json(json_file):
    """Reads the exported JSON file and returns the data."""
    with open(json_file, 'r') as f:
        data = json.load(f)
    return data


def parse_arguments():
    """Parses command-line arguments."""
    parser = argparse.ArgumentParser(description="Generate a MIDI file from JSON data.")
    parser.add_argument('json_file', type=str, help="Path to the JSON file containing the data.")
    parser.add_argument('--output', type=str, default='output.mid', help="Output MIDI file path (default: output.mid)")
    return parser.parse_args()


def main():
    args = parse_arguments()
    data = load_data_from_json(args.json_file)

    generator = MIDIGenerator()
    generator.generate_tracks(data)

    generator.save_midi(args.output)
    print(f"MIDI file generated: {args.output}")


if __name__ == "__main__":
    main()
