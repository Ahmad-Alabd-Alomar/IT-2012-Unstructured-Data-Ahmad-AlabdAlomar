import os
import logging
from pydub import AudioSegment

def process_audio_files(audio_dir="data/raw/audio", output_dir="data/processed/audio"):
    """Lab 7: Trims, converts, concatenates, and applies effects to audio files."""
    logging.info("--- Processing Audio Files ---")
    
    files = [f for f in os.listdir(audio_dir) if os.path.isfile(os.path.join(audio_dir, f))]
    if not files:
        logging.warning("No audio files found to process.")
        return [], None

    audio_clips = []
    # TASK 1: Load & Inspect
    for file in files:
        path = os.path.join(audio_dir, file)
        try:
            clip = AudioSegment.from_file(path)
            logging.info(f"Loaded {file}: Duration={len(clip)/1000}s, Channels={clip.channels}, FrameRate={clip.frame_rate}Hz")
            audio_clips.append((file, clip))
        except Exception as e:
            logging.error(f"Failed to load {file}: {e}")

    if not audio_clips: return [], None

    name1, clip1 = audio_clips[0]
    
    # TASK 2: Trim audio (first 5 seconds)
    trimmed = clip1[:5000]
    trim_path = os.path.join(output_dir, f"trimmed_{name1}.wav")
    trimmed.export(trim_path, format="wav")
    logging.info(f"Trimmed audio saved to {trim_path}")

    # TASK 5: Convert Format
    convert_path = os.path.join(output_dir, f"converted_{os.path.splitext(name1)[0]}.mp3")
    clip1.export(convert_path, format="mp3", bitrate="192k")
    logging.info(f"Converted audio saved to {convert_path}")

    # TASK 3 & 4: Concatenate & Effects (Requires at least 2 clips)
    if len(audio_clips) >= 2:
        name2, clip2 = audio_clips[1]
        clip2 = clip2.set_frame_rate(clip1.frame_rate).set_channels(clip1.channels)
        concat_clip = clip1 + clip2
        
        # TASK 4: Adjust volume (+dB AND -dB) and fade
        louder_part = concat_clip[:5000] + 5  # +5 dB
        quieter_part = concat_clip[5000:] - 5 # -5 dB
        effect_clip = louder_part + quieter_part
        effect_clip = effect_clip.fade_in(2000).fade_out(2000)
        
        effect_path = os.path.join(output_dir, "concatenated_with_effects.wav")
        effect_clip.export(effect_path, format="wav")
        logging.info(f"Concatenated & effect audio saved to {effect_path}")

    # Return standard files for Task 8, and the longest file for Task 10 (Chunking)
    longest_file = max(audio_clips, key=lambda item: len(item[1]))[0]
    
    return [os.path.join(audio_dir, files[0])], os.path.join(audio_dir, longest_file)