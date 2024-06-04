from itertools import repeat
import multiprocessing
from scipy.io import wavfile
from glob import glob
import os
from tkinter import filedialog

from cheetah.stx import CheetaAnnotationFile, Segment


def main():
    root = filedialog.askdirectory(title="Select root directory of annotations")
    output_path = filedialog.askdirectory(title="Select output directory", mustexist=False)

    os.makedirs(output_path, exist_ok=True)

    wav_filepaths = find_wav_files(root)
    annotation_filepaths = glob(f"{root}/**/*.stxsm", recursive=True)

    with multiprocessing.Pool() as p:
        p.starmap(extract_annotation, zip(annotation_filepaths, repeat(wav_filepaths), repeat(output_path)))


def find_wav_files(root: str):
    wav_filepaths = glob(f"{root}/**/*.wav", recursive=True)
    wav_filepaths += glob(f"{root}/**/*.WAV", recursive=True)
    return {os.path.basename(x): x for x in wav_filepaths}


def extract_annotation(annotation_file: str, wav_paths: dict[str, str], output_path: str):
    annotations = CheetaAnnotationFile.from_stxsm_file(annotation_file)
    wav = load_wav_to_mono(wav_paths[annotations.file_id])
    for segment in annotations.segments:
        file_path = f"{output_path}/{segment.id}.wav"
        wavfile.write(
            file_path,
            annotations.samplerate,
            extract_wav_segment(wav, segment),
        )


def load_wav_to_mono(path: str):
    _, file = wavfile.read(path)
    if file.ndim > 1:  # if there are multiple dimensions (channels) take only the first
        file = file[:, 0]
    return file

def extract_wav_segment(wav_array, segment: Segment, additional=48000):
    start = max(segment.start - additional, 0)
    end = min(segment.start + segment.length + additional, len(wav_array))
    return wav_array[start:end]


if __name__ == "__main__":
    main()
