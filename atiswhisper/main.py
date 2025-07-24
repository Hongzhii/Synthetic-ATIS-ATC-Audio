import argparse
import os
from atiswhisper.gemini_api import correct_srts
from atiswhisper.synthesize_data import synthesize_transcripts
from atiswhisper.noise import add_noise_to_audio_dir
from atiswhisper.synthesize_data import generate_srt_with_whisper
import subprocess
import google.generativeai as genai

def main():
    parser = argparse.ArgumentParser(description="ATIS Data Pipeline")
    parser.add_argument("--output_dir", type=str, required=True, help="Output directory (e.g. ./data)")
    parser.add_argument("--generate_srt", action="store_true", help="Generate .srt transcripts using Whisper and correct with Gemini API")
    parser.add_argument("--add_noise", action="store_true", help="Add noise to synthesized audio files")
    parser.add_argument("--samples", type=int, default=50, help="Number of samples to synthesize")
    parser.add_argument("--gemini_correction", action="store_true", help="Apply Gemini correction to generated SRT files")
    args = parser.parse_args()

    # Check if ./dectalk directory exists, if not, run dec_talk_install.sh
    if not os.path.isdir("./dectalk"):
        print("Installing DECtalk synthesizer. This may take a few minutes...")
        subprocess.run(["bash", "scripts/dec_talk_install.sh"], check=True)

    synthesized_audio_dir = os.path.join(args.output_dir, "synthesized_audios")
    transcript_dir = os.path.join(args.output_dir, "transcripts")
    noisy_audio_dir = os.path.join(args.output_dir, "noisy_audio")
    srt_dir = os.path.join(args.output_dir, "srt_files")
    corrected_srt_dir = os.path.join(args.output_dir, "srt_corrected")

    # Step 1: Synthesize transcripts and audio
    synthesize_transcripts(args.output_dir, args.samples)

    # Step 2: Optionally add noise
    if args.add_noise:
        add_noise_to_audio_dir(synthesized_audio_dir, noisy_audio_dir)

    # Step 3: Optionally generate SRTs and correct them
    if args.generate_srt:
        generate_srt_with_whisper(
            synthesized_audio_dir,
            srt_dir
        )
        if args.gemini_correction:
            genai.configure()  # Will use GOOGLE_API_KEY from environment
            gemini_client = genai.GenerativeModel("gemini-2.5-flash")
            correct_srts(
                gemini_client,
                srt_dir,
                transcript_dir,
                corrected_srt_dir
            )

if __name__ == "__main__":
    main()
