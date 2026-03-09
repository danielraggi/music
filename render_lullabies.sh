#!/bin/sh
# Render all MIDI lullabies to WAV using FluidSynth.
#
# Usage:
#   ./render_lullabies.sh              # render all MIDIs to lullabies_wav/
#   ./render_lullabies.sh --sf2 FILE   # use a custom soundfont
#
# Requirements:
#   - fluidsynth (apt install fluidsynth)
#   - A soundfont (.sf2). Defaults to FluidR3_GM (apt install fluid-soundfont-gm).
#     For best piano sound, use the Salamander Grand Piano:
#       https://musical-artifacts.com/artifacts/7758  (full, ~650MB)
#       https://musical-artifacts.com/artifacts/483   (light, ~25MB)
#     Place it as soundfonts/SalamanderGrandPiano.sf2 and run:
#       ./render_lullabies.sh --sf2 soundfonts/SalamanderGrandPiano.sf2

set -e

# ─── Defaults ───
SOUNDFONT=""
OUTDIR="lullabies_wav"
SAMPLE_RATE=44100
GAIN=1.0

# ─── Parse arguments ───
while [ $# -gt 0 ]; do
    case "$1" in
        --sf2)  SOUNDFONT="$2"; shift 2 ;;
        --out)  OUTDIR="$2"; shift 2 ;;
        --gain) GAIN="$2"; shift 2 ;;
        *)      echo "Unknown option: $1"; exit 1 ;;
    esac
done

# ─── Find soundfont ───
if [ -z "$SOUNDFONT" ]; then
    # Prefer Salamander if available, fall back to FluidR3_GM
    if [ -f "soundfonts/SalamanderGrandPiano.sf2" ]; then
        SOUNDFONT="soundfonts/SalamanderGrandPiano.sf2"
        echo "Using Salamander Grand Piano soundfont"
    elif [ -f "/usr/share/sounds/sf2/FluidR3_GM.sf2" ]; then
        SOUNDFONT="/usr/share/sounds/sf2/FluidR3_GM.sf2"
        echo "Using FluidR3_GM soundfont"
    else
        echo "Error: No soundfont found. Install fluid-soundfont-gm or provide --sf2"
        exit 1
    fi
fi

if [ ! -f "$SOUNDFONT" ]; then
    echo "Error: Soundfont not found: $SOUNDFONT"
    exit 1
fi

# ─── Check fluidsynth ───
if ! command -v fluidsynth >/dev/null 2>&1; then
    echo "Error: fluidsynth not installed. Run: apt install fluidsynth"
    exit 1
fi

# ─── Render ───
count=0
failed=0

find lullabies -name '*.mid' -type f | sort | while read -r midi; do
    # Mirror directory structure: lullabies/bach/foo.mid → lullabies_wav/bach/foo.wav
    rel="${midi#lullabies/}"
    wav_path="$OUTDIR/${rel%.mid}.wav"
    wav_dir="$(dirname "$wav_path")"
    mkdir -p "$wav_dir"

    name="$(basename "$midi" .mid)"

    if [ -f "$wav_path" ] && [ "$wav_path" -nt "$midi" ]; then
        echo "  Skip (up to date): $name"
        continue
    fi

    printf "  Rendering: %-50s" "$name"
    if fluidsynth -ni "$SOUNDFONT" "$midi" -F "$wav_path" -r "$SAMPLE_RATE" -g "$GAIN" >/dev/null 2>&1; then
        # Get file size in human-readable form
        size=$(du -h "$wav_path" | cut -f1)
        echo " → $size"
    else
        echo " FAILED"
    fi
done

echo
echo "Done! WAV files in $OUTDIR/"
echo
echo "To convert to MP3 (requires lame or ffmpeg):"
echo "  find $OUTDIR -name '*.wav' -exec sh -c '"
echo '    ffmpeg -i "$1" -b:a 192k "${1%.wav}.mp3" && rm "$1"'
echo "  ' _ {} \\;"
