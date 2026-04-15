from fcp_io import fcpxml_io
from fcp_marker_trimmer import trim
from fcp_math import arithmetic

import subprocess
from pathlib import Path

import whisper

def merge_audio(filepath, prefix='yt_', debug=False):
    """
    Creates a new video file that mixes all the audio tracks from the source video file.
    """
    filepath = Path(filepath)
    parent = filepath.parent
    name = filepath.name
    output_filepath = parent / (prefix+name)

    cmd = ['ffmpeg', '-i', filepath, '-filter_complex', '"[0:a:0][0:a:1]amix=inputs=2[aout]"', '-map', '0:v', '-map', '"[aout]"', '-c:v', 'copy', '-c:a', 'aac', output_filepath]

    if debug:
        print(f"merge_audio command to run: {cmd}")

    process = subprocess.run(
            cmd,
            stderr=subprocess.PIPE,
            stdout=subprocess.DEVNULL,
            text=True
            )
    output = process.stderr

    #return output
    print(f"⛙ Multitrack audio merge from {name} to {prefix+name} done!")

def extract_audio(filepath, track, debug=False):
    """
    If track is specified, uses ffmpeg to create an m4a file of that track.
    Returns the audio file to work on transcribing.
    """
    output = filepath

    if track:
        filepath = Path(filepath)
        parent = filepath.parent
        stem = filepath.stem
        output = parent / (prefix+stem+'.m4a')
        cmd = ['ffmpeg', '-i', filepath, '-map', f'0:a:{track}', '-acodec', 'copy', output]

    if debug:
        print(f"extract_audio command to run: {cmd}")

    process = subprocess.run(
            cmd,
            stderr=subprocess.PIPE,
            stdout=subprocess.DEVNULL,
            text=True
            )
    output_stderr = process.stderr

    print(f"🫡 Single audio track extraction from {filepath.name} to {output.name} done!")

    return output

def transcribe(filepath, model, language, debug=False):
    af = filepath
    cmd = ['whisper', af]
    if model:
        cmd += ['--model', model]
    if language:
        cmd += ['--language', language]

    if debug:
        print(f"transcribe command to run: {cmd}")

    process = subprocess.run(
            cmd,
            stderr=subprocess.PIPE,
            stdout=subprocess.DEVNULL,
            text=True
            )
    output = process.stderr

    return output

def translate(text, source_language='ko', target_language='en', debug=False):
    """
    future project
    """
    output = text
    return output
