import os
import random
import re
import subprocess

LOCATIONS = [
    "La Guardia",
    "Denver international",
    "Miami international",
    "Kuala Lumpur international",
    "Hong Kong international",
    "Philadelphia International",
    "London city",
]

PREAMBLE = [
    "Arrival",
    "Arrival ATIS",
]

PHONETIC_ALPHABET = [
    "Alpha",
    "Bravo",
    "Charlie",
    "Delta",
    "Echo",
    "Foxtrot",
    "Golf",
    "Hotel",
    "India",
    "Juliett",
    "Kilo",
    "Lima",
    "Mike",
    "November",
    "Oscar",
    "Papa",
    "Quebec",
    "Romeo",
    "Sierra",
    "Tango",
    "Uniform",
    "Victor",
    "Whiskey",
    "X-ray",
    "Yankee",
    "Zulu",
]

VISIBILITY = [
    "10",
    "5",
    "2",
]

CLOUD_CONDITIONS = [
    "Scattered",
    "Overcast",
    "Vertical visibility",
    "Sky clear",
    "Few clouds",
]

def generate_synthetic_atis_transcript() -> str:
    """
    Generate a synthetic ATIS (Automatic Terminal Information Service) transcript.

    Returns:
        str: A randomly generated ATIS transcript string.
    """
    location = random.choice(LOCATIONS)
    preamble = random.choice(PREAMBLE)
    alphabet = random.choice(PHONETIC_ALPHABET)

    hour = f"{random.randint(0, 23):02d}"
    minute = f"{random.randint(0, 59):02d}"

    template = f"{location} airport {preamble} information {alphabet}. {hour}{minute} Zulu."

    if random.random() > 0.2:
        wind_direction = f"{random.randint(1, 36):02d}"
        wind_speed = max(0, int(random.gauss(10, 5)))
        visibility = random.choice(VISIBILITY)

        template += f" Wind {wind_direction}0 at {wind_speed}. Visibility {visibility}."

    if random.random() > 0.2:
        level_1 = f"{random.randint(1, 9)}"
        level_2 = f"{random.randint(10,19)}"
        condition_1 = random.choice(CLOUD_CONDITIONS)
        condition_2 = random.choice(CLOUD_CONDITIONS)
        
        template += f" {condition_1} at {level_1},000. {level_2},000 {condition_2}."

    temperature = f"{random.randint(-20, 35)}"
    dew_point = f"{random.randint(int(temperature)-15, int(temperature))}"
    altimeter = f"{random.randint(2800, 3200)}"

    template += f" Temperature {temperature}. Dew point {dew_point}. Altimeter {altimeter}."

    template += f" Advise on initial contact, {random.choice(['you have', 'ATIS'])} information {alphabet}."

    return str(template)

def generate_tts_script(transcript: str) -> str:
    """
    Convert a transcript into a TTS-friendly script by formatting numbers and replacing certain words.

    Args:
        transcript (str): The original transcript.

    Returns:
        str: The formatted TTS script.
    """
    def format_thousands(match: re.Match) -> str:
        num = match.group().replace(",", "")
        return " ".join(num[:-3]) + " thousand" if len(num) > 4 else f"{num[0]} thousand"

    # Format thousands (e.g., 3,000 -> 3 thousand, 15,000 -> 1 5 thousand)
    transcript = re.sub(r"\b\d{1,2},000\b", format_thousands, transcript)

    # Format 2, 3, 4 numbers (e.g., 1445 -> 1 4 4 5)
    for digit in range(4, 1, -1):
        # Handle negative numbers: e.g., -10 -> -1 0, -123 -> -1 2 3
        transcript = re.sub(
            rf"-\d{{{digit-1}}}\b",
            lambda m: "-" + " ".join(m.group()[1:]),
            transcript
        )
        # Handle positive numbers
        transcript = re.sub(
            rf"\d{{{digit}}}\b",
            lambda m: " ".join(m.group()),
            transcript
        )

    # Replace all occurrences of '9' with 'Niner'
    transcript = re.sub(r"9", "Niner", transcript)

    return transcript

def synthesize_transcripts(output_dir: str, samples: int) -> None:
    """
    Generate synthetic ATIS transcripts and corresponding audio files using a TTS engine.

    Args:
        output_dir (str): Directory to save the synthesized audio and transcript files.
        samples (int): Number of samples to generate.

    Returns:
        None
    """
    audio_dir = os.path.join(output_dir, "synthesized_audios")
    transcript_dir = os.path.join(output_dir, "transcripts")

    os.makedirs(audio_dir, exist_ok=True)
    os.makedirs(transcript_dir, exist_ok=True)

    for i in range(samples):
        transcript = generate_synthetic_atis_transcript()
        script = generate_tts_script(transcript)

        command = "./dectalk/dist/say"
        command += f" -a \"{script}\""
        command += f" -fo {os.path.join(audio_dir, str(i))}.wav"
        command += f" -s 2 -r 150"

        try:
            os.system(command)
        except Exception as e:
            print(f"Error running command: {e}")
            print("Attempting to remove and reinstall dectalk...")
            os.system("rm -rf ./dectalk")
            os.system("./dec_talk_install.sh")


        with open(os.path.join(transcript_dir, f"{i}.txt"), "w") as f:
            f.write(transcript)

def generate_srt_with_whisper(audio_dir, srt_dir):
    os.makedirs(srt_dir, exist_ok=True)
    audio_files = [f for f in os.listdir(audio_dir) if f.endswith('.wav')]
    for audio_file in audio_files:
        audio_path = os.path.join(audio_dir, audio_file)
        # Call OpenAI Whisper CLI to generate SRT
        subprocess.run([
            "whisper", audio_path,
            "--model", "medium.en",
            "--output_format", "srt",
            "--output_dir", srt_dir
        ], check=True)
