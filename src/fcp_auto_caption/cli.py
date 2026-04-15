#!/usr/bin/env python3

import argparse
import xml.etree.ElementTree as ET

from . import detect_speech
from . import subtitles_manager
from fcp_io import fcpxml_io
from pathlib import Path
import shutil

def main():

    # Define possible arguments
    parser = argparse.ArgumentParser(description="Automatically generate captions (srt file) for FCP Projects.")
    parser.add_argument("filepath", help="Absolute filepath of target video (required)")
    # track
    parser.add_argument("--track", type=int, help="Audio track to use in 0:a:x. Note that, in FCP, when exporting a Project as a multitrack Quicktime movie, audio tracks occupy tracks ahead of video (unlike OBS).")
    # model
    parser.add_argument("--model", type=str, default='turbo', help="Whisper model to use")
    # language
    parser.add_argument("--language", type=str, default='ko', help="Target language to transcribe. ISO 639-1.")
    # translate
    parser.add_argument("--translate", action='append', type=str, help="Translate to other languages. ISO 639-1. ex: en,sp,ru,jp,cn,ge,fr")
    # output
    parser.add_argument("--affix", type=str, default='captions_', help="affix to modify the output filename")
    # save
    parser.add_argument("--save", action='store_true', help="Save to file or just print output?")
    # debug
    parser.add_argument("--debug", action='store_true', help="(experimental) display debug messages.")

    args = parser.parse_args()

    filepath = fcpxml_io.clean_filepath(args.filepath)

    if args.debug:
        print("Entering debug mode...")

    # For a better result, you need a multitrack video with the speech to be transcribed separated from other music and effects. Say that's in [0:a:0]
    
    # First, YouTube doesn't understand multitrack audio, so create a mov file that mixes (merges) multi audio tracks
    if args.track:
        detect_speech.merge_audio(filepath=filepath, debug=args.debug)

    # Second, extract the audio track you want to transcribe.
    af = detect_speech.extract_audio(filepath=filepath, track, track=args.track, debug=args.debug)

    # Third, transcribe.
    detect_speech.transcribe(filepath=af, model=args.model, language=args.language, debug=args.debug)

    manage_subtitles.move_to_subtitles()
    srt = Path(f'./subtitles/{af.stem}.srt').read_text(encoding='utf-8')

    # Fourth, improve the transcription.
    context = Path('./subtitles/context.md').read_text(encoding='utf-8')
    srt = manage_subtitles.context_provision(srt=srt, context=context, debug=args.debug)

    if args.save:
        filepath = Path(filepath)
        parent = filepath.parent
        name = filepath.name
        output = parent / (args.affix+name+'.srt')
        with open(f"{output}", 'w') as f:
            f.write(srt)
        output = parent / (args.affix+name+'.txt')
        text = subtitles_manager.srt2txt(srt=srt)
        with open(f"{output}", 'w') as f:
            f.write(text)

    # If specified to translate the transcribed text, do it here.
    for lang in args.translate:
        translated_text = detect_speech.translate(text=text, source_language=args.language, target_language=lang, debug=args.debug)
        translated_srt = subtitles_manager.txt2srt(txt=translated_text, srt=srt)
        if args.save:
            output = parent / (args.affix+name+f'_{lang}'+'.srt')
            with open(f"{output}", 'w') as f:
                f.write(translated_srt)
            output = parent / (args.affix+name+f'_{lang}'+'.txt')
            with open(f"{output}", 'w') as f:
                f.write(translated_text)

if __name__ == "__main__":
    main()
