import numpy as np
from pydub import AudioSegment
import os
from typing import Union

def add_noise_to_wav(
    input_wav_path: Union[str, bytes, os.PathLike],
    output_wav_path: Union[str, bytes, os.PathLike],
    noise_level_db: float = -20
) -> None:
    """
    Adds Gaussian noise to a WAV audio file and saves the result.

    Args:
        input_wav_path: Path to the input WAV file.
        output_wav_path: Path to save the noisy WAV file.
        noise_level_db: Desired noise level in decibels (dBFS).
    """
    audio = AudioSegment.from_wav(input_wav_path)
    samples = np.array(audio.get_array_of_samples()).astype(np.float32)

    noise = np.random.normal(0, 1, len(samples))
    noise = noise / np.max(np.abs(noise))

    noise_audio = AudioSegment(
        (noise * (2**(audio.sample_width*8-1)-1)).astype(np.int16).tobytes(),
        frame_rate=audio.frame_rate,
        sample_width=audio.sample_width,
        channels=audio.channels
    )
    noise_audio = noise_audio - noise_audio.dBFS + noise_level_db

    mixed = audio.overlay(noise_audio)
    mixed.export(output_wav_path, format="wav")

def add_noise_to_audio_dir(
    synthesized_audio_dir: Union[str, bytes, os.PathLike],
    output_dir: Union[str, bytes, os.PathLike]
) -> None:
    """
    Adds noise to all WAV files in a directory and saves them to an output directory.

    Args:
        synthesized_audio_dir: Directory containing input WAV files.
        output_dir: Directory to save noisy WAV files.
    """
    os.makedirs(output_dir, exist_ok=True)

    for file in os.listdir(synthesized_audio_dir):
        if not file.endswith(".wav"):
            print(f"Warning: Skipping non-wav file: {file}")
            continue

        noise_level = np.random.normal(loc=-20, scale=5)

        add_noise_to_wav(
            os.path.join(synthesized_audio_dir, file),
            os.path.join(output_dir, file),
            noise_level_db=noise_level,
        )
