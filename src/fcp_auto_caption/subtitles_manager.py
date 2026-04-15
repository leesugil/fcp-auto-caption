
def move_to_subtitles():
    # moving resulting files from Whisper AI to a subfolder
    current_dir = Path('./')
    target_dir = Path('./subtitles')
    target_dir.mkdir(parents=True, exist_ok=True)

    extensions = ['*.json', '*.tsv', '*.srt', '*.vtt', '*.txt']
    for pattern in extensions:
        for filepath in source_dir.glob(pattern):
            destination = target_dir / filepath.name
            shutil.move(str(filepath), str(destination))
            print(f"Moved: {filepath.name}")

def srt2txt(srt):
    """
1
00:00:00,000 --> 00:00:00,980
19화

    """
    output = []
    for i, line in enumerate(srt.splitlines()):
        if (i % 4) == 2:
            output.append(line)
    output = '\n'.join(output)
    return output

def txt2srt(txt, srt):
    output = srt.splitlines()
    text = txt.splitlines()
    assert len(output) == 4*len(text)
    j = 0
    for i in range(len(output)):
        if (i % 4) == 2:
            output[i] = text[j]
            j += 1
    output = '\n'.join(output)
    return output

def context_provision(srt, context, debug=False):
    """
    future project
    """
    output = srt
    return output
