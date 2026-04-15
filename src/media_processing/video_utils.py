import os
import logging
from moviepy.editor import VideoFileClip

def process_video_files(video_dir="data/raw/video", output_dir="data/processed/video", keyframe_dir="data/processed/keyframes"):
    """Lab 7: Inspects video, extracts audio, and saves keyframes."""
    logging.info("--- Processing Video Files ---")
    
    files = [f for f in os.listdir(video_dir) if f.lower().endswith(('.mp4', '.avi', '.mkv', '.mov'))]
    if not files:
        logging.warning("No video files found.")
        return []

    extracted_audio_paths = []

    for file in files:
        path = os.path.join(video_dir, file)
        try:
            clip = VideoFileClip(path)
            
            # 1. Inspect Properties (Print for ReadMe screenshot)
            print(f"\n--- Video Properties: {file} ---")
            print(f"Duration: {clip.duration} seconds")
            print(f"FPS: {clip.fps}")
            print(f"Resolution: {clip.size}")
            logging.info(f"Video {file}: Duration={clip.duration}s, FPS={clip.fps}, Res={clip.size}")

            # 2. Extract Audio Track
            if clip.audio is not None:
                audio_path = os.path.join(output_dir, f"extracted_audio_{os.path.splitext(file)[0]}.mp3")
                clip.audio.write_audiofile(audio_path, logger=None)
                logging.info(f"Extracted audio saved to {audio_path}")
                extracted_audio_paths.append(audio_path)

            # 3. Extract Keyframes (Every 5 seconds)
            interval = 5
            for t in range(0, int(clip.duration), interval):
                frame_path = os.path.join(keyframe_dir, f"{os.path.splitext(file)[0]}_frame_{t}s.jpg")
                clip.save_frame(frame_path, t=t)
            logging.info(f"Extracted keyframes every {interval}s")
            
            clip.close()
        except Exception as e:
            logging.error(f"Failed to process video {file}: {e}")

    return extracted_audio_paths