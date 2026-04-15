import os
import logging
from faster_whisper import WhisperModel
from pydub import AudioSegment

def transcribe_media(audio_paths):
    """Lab 7: Transcribes short audio files and extracted video audio."""
    logging.info("--- Starting Faster-Whisper Transcription ---")
    if not audio_paths: return []

    model = WhisperModel("base", device="cpu", compute_type="int8")
    transcripts = []

    for path in audio_paths:
        if not os.path.exists(path): continue
        logging.info(f"Transcribing short file: {path}")
        
        try:
            segments, info = model.transcribe(path, beam_size=5)
            print(f"\n--- Transcription Output: {os.path.basename(path)} ---")
            
            full_text = ""
            segment_data = []
            
            for segment in segments:
                line = f"[{segment.start:.2f}s - {segment.end:.2f}s] {segment.text}"
                print(line)  # TASK 8: Print segments with timestamps for ReadMe
                full_text += segment.text + " "
                segment_data.append({"start": segment.start, "end": segment.end, "text": segment.text})
            
            transcripts.append({
                "source_file": os.path.basename(path),
                "source_path": path,
                "model": "faster-whisper-base",
                "language": info.language,
                "duration_s": info.duration,
                "full_text": full_text.strip(),
                "segments": segment_data
            })
        except Exception as e:
            logging.error(f"Transcription failed for {path}: {e}")

    return transcripts

def transcribe_long_audio_chunked(audio_path, chunk_length_ms=30000):
    """TASK 10: Transcribe a longer audio file using chunking strategy (30s chunks)."""
    if not os.path.exists(audio_path): return None
    logging.info(f"--- Chunking and transcribing long audio: {audio_path} ---")
    
    model = WhisperModel("base", device="cpu", compute_type="int8")
    audio = AudioSegment.from_file(audio_path)
    
    # Slice the audio into chunks
    chunks = [audio[i:i + chunk_length_ms] for i in range(0, len(audio), chunk_length_ms)]
    
    full_text = ""
    all_segments = []
    current_time_offset = 0.0
    detected_lang = "unknown"

    print(f"\n--- Chunked Transcription Output: {os.path.basename(audio_path)} ---")
    
    for i, chunk in enumerate(chunks):
        chunk_path = f"data/processed/audio/temp_chunk_{i}.wav"
        chunk.export(chunk_path, format="wav")
        
        segments, info = model.transcribe(chunk_path, beam_size=5)
        detected_lang = info.language
        
        for segment in segments:
            # Adjust timestamps so they match the original long file
            start = segment.start + current_time_offset
            end = segment.end + current_time_offset
            print(f"[{start:.2f}s - {end:.2f}s] {segment.text}")
            full_text += segment.text + " "
            all_segments.append({"start": start, "end": end, "text": segment.text})
        
        current_time_offset += (len(chunk) / 1000.0)
        os.remove(chunk_path) # Clean up temp files

    return {
        "source_file": os.path.basename(audio_path),
        "source_path": audio_path,
        "model": "faster-whisper-chunked",
        "language": detected_lang,
        "duration_s": len(audio)/1000.0,
        "full_text": full_text.strip(),
        "segments": all_segments
    }