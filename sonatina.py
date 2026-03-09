#!/usr/bin/env python3
"""
Sonatina in C Major, "Für meine liebe Nichte"
(For My Dear Niece)

In the style of W.A. Mozart

A charming, pedagogical sonatina in sonata form.
Single movement: Allegretto grazioso (♩= 108)

Structure:
  Exposition (mm. 1-20):  First theme in C, transition, second theme in G
  Development (mm. 21-28): Motivic work through minor keys
  Recapitulation (mm. 29-48): Both themes in C
  Coda (mm. 49-52): Gentle closing flourish
"""

import mido
from mido import MidiFile, MidiTrack, Message, MetaMessage

# ─── Duration constants (ticks, 480 ticks per quarter note) ───

TPB = 480
W  = TPB * 4      # whole
DH = TPB * 3      # dotted half
H  = TPB * 2      # half
DQ = TPB + TPB//2  # dotted quarter
Q  = TPB          # quarter
E  = TPB // 2     # eighth
S  = TPB // 4     # sixteenth

# ─── MIDI pitch constants ───

C3, D3, E3, F3, G3, A3, B3 = 48, 50, 52, 53, 55, 57, 59
C4, D4, E4, F4, G4, A4, B4 = 60, 62, 64, 65, 67, 69, 71
C5, D5, E5, F5, G5, A5, B5 = 72, 74, 76, 77, 79, 81, 83
C6 = 84
Fs3, Fs4, Fs5 = 54, 66, 78   # F-sharps for the G major sections
Bb3, Bb4 = 58, 70             # B-flats (for development)
R = None  # rest

# ─── Velocity levels (expression) ───

FF  = 95
F   = 85
MF  = 75
MP  = 65
P   = 55
PP  = 48

# ─── Note / rest constructors ───

def n(pitch, dur, vel=MF):
    return (pitch, dur, vel)

def rest(dur):
    return (R, dur, 0)


# ─── Alberti bass generator ───

def alberti(bottom, middle, top, dur=W, vel=PP):
    """Classic Alberti bass: bottom-top-middle-top in eighth notes."""
    notes = []
    pattern = [bottom, top, middle, top]
    num_eighths = dur // E
    for i in range(num_eighths):
        notes.append(n(pattern[i % 4], E, vel))
    return notes


# ─── Broken chord for cadences ───

def broken_chord(pitches, dur_each, vel=MP):
    return [n(p, dur_each, vel) for p in pitches]


# ─── Track builder ───

def notes_to_track(notes, track, channel=0):
    """Convert [(pitch, duration, velocity), ...] to MIDI messages on a track."""
    pending_time = 0
    for pitch, dur, vel in notes:
        if pitch is None:
            pending_time += dur
        else:
            track.append(Message('note_on', note=pitch, velocity=vel,
                                 time=pending_time, channel=channel))
            track.append(Message('note_off', note=pitch, velocity=0,
                                 time=dur, channel=channel))
            pending_time = 0


# ═══════════════════════════════════════════════════════════════════
#  THE MUSIC — Right Hand (melody) and Left Hand (accompaniment)
# ═══════════════════════════════════════════════════════════════════

rh = []  # right hand notes
lh = []  # left hand notes

# ───────────────────────────────────────────────
#  EXPOSITION — First Theme (mm. 1-8, C major)
# ───────────────────────────────────────────────

# m1 (I): Gentle opening — a singing, stepwise melody
rh += [n(E5,E,MP), n(D5,E,MP), n(C5,Q,MF), n(E5,Q,MF), n(G5,Q,MF)]
lh += alberti(C3, E3, G3)

# m2 (V): Answering phrase, descending
rh += [n(F5,Q,MF), n(E5,Q,MP), n(D5,H,MP)]
lh += alberti(G3, B3, D4)

# m3 (IV): Rising again with warmth
rh += [n(E5,E,MP), n(F5,E,MP), n(G5,Q,MF), n(A5,Q,F), n(G5,Q,MF)]
lh += alberti(F3, A3, C4)

# m4 (V → half cadence): Graceful descent to half cadence
rh += [n(G5,Q,MF), n(F5,E,MP), n(E5,E,MP), n(D5,H,MP)]
lh += alberti(G3, B3, D4)

# m5 (I): Consequent phrase begins — echo of m1
rh += [n(C5,E,MP), n(D5,E,MP), n(E5,Q,MF), n(G5,Q,MF), n(C6,Q,F)]
lh += alberti(C3, E3, G3)

# m6 (IV): Lyrical descent
rh += [n(A5,Q,MF), n(G5,Q,MF), n(F5,Q,MP), n(E5,Q,MP)]
lh += alberti(F3, A3, C4)

# m7 (ii → V): Pre-cadential motion
rh += [n(D5,Q,MP), n(E5,E,MP), n(F5,E,MF), n(E5,Q,MF), n(D5,Q,MP)]
lh += alberti(D3, F3, A3, dur=H) + alberti(G3, B3, D4, dur=H)

# m8 (I): Perfect authentic cadence — arrival
rh += [n(C5,H,F), rest(H)]
lh += [n(C3,Q,MF), n(E3,Q,MP), n(G3,Q,MP), n(C4,Q,MP)]

# ───────────────────────────────────────────────
#  EXPOSITION — Transition (mm. 9-12)
# ───────────────────────────────────────────────

# m9 (I): Energetic figure launching the transition
rh += [n(G5,Q,MF), n(E5,E,MP), n(F5,E,MP), n(G5,Q,MF), n(A5,Q,F)]
lh += alberti(C3, E3, G3)

# m10 (vi → applied dominant): Passing through A minor, introducing F#
rh += [n(B5,Q,F), n(A5,Q,MF), n(G5,Q,MF), n(Fs5,Q,MF)]
lh += alberti(A3, C4, E4, dur=H) + alberti(D3, Fs3, A3, dur=H)

# m11 (V/V → V): Dominant of G major
rh += [n(G5,E,MF), n(A5,E,MF), n(B5,Q,F), n(A5,Q,MF), n(Fs5,Q,MF)]
lh += alberti(D3, Fs3, A3)

# m12 (V = G): Arrival on G — breath before second theme
rh += [n(G5,H,F), rest(H)]
lh += [n(G3,Q,MF), n(B3,Q,MP), n(D4,Q,MP), rest(Q)]

# ───────────────────────────────────────────────
#  EXPOSITION — Second Theme (mm. 13-20, G major)
#  More lyrical and tender — "for his niece"
# ───────────────────────────────────────────────

# m13 (I of G): Sweet, singing melody
rh += [n(B4,E,P), n(C5,E,P), n(D5,Q,MP), n(G5,Q,MF), n(D5,Q,MP)]
lh += alberti(G3, B3, D4, vel=PP)

# m14 (IV of G = C): Gentle answer
rh += [n(E5,Q,MP), n(D5,Q,MP), n(C5,Q,P), n(B4,Q,P)]
lh += alberti(C3, E3, G3, vel=PP)

# m15 (I of G): Rising with tenderness
rh += [n(D5,E,P), n(E5,E,MP), n(Fs5,Q,MF), n(A5,Q,MF), n(Fs5,Q,MP)]
lh += alberti(G3, B3, D4, vel=PP)

# m16 (V of G = D): Delicate half cadence
rh += [n(G5,Q,MF), n(Fs5,E,MP), n(E5,E,P), n(D5,H,P)]
lh += alberti(D3, Fs3, A3, vel=PP)

# m17 (I of G): Second phrase — a little ornamental turn
rh += [n(B5,Q,MF), n(A5,E,MP), n(G5,E,MP), n(A5,Q,MF), n(Fs5,Q,MP)]
lh += alberti(G3, B3, D4, vel=PP)

# m18 (IV of G): Flowing
rh += [n(E5,Q,MP), n(G5,Q,MF), n(Fs5,Q,MP), n(E5,Q,MP)]
lh += alberti(C3, E3, G3, vel=PP)

# m19 (V of G): Cadential flourish
rh += [n(D5,E,MP), n(E5,E,MP), n(Fs5,E,MF), n(G5,E,MF), n(A5,Q,F), n(Fs5,Q,MF)]
lh += alberti(D3, Fs3, A3, vel=PP)

# m20 (I of G): Peaceful close of exposition
rh += [n(G5,H,MF), rest(H)]
lh += [n(G3,Q,MP), n(B3,Q,PP), n(D4,Q,PP), rest(Q)]

# ───────────────────────────────────────────────
#  DEVELOPMENT (mm. 21-28)
#  Shadows and light — fragments of the first theme
#  wander through minor keys before finding home
# ───────────────────────────────────────────────

# m21 (G → em): First theme fragment, darkening
rh += [n(G5,Q,MF), n(Fs5,E,MP), n(E5,E,MP), n(D5,Q,MP), n(B4,Q,P)]
lh += alberti(G3, B3, D4, dur=H) + alberti(E3, G3, B3, dur=H)

# m22 (em): Plaintive descent through E minor
rh += [n(E5,Q,MP), n(D5,Q,P), n(C5,Q,P), n(B4,Q,PP)]
lh += alberti(E3, G3, B3, vel=PP)

# m23 (am): Sequence into A minor — touching moment
rh += [n(C5,E,P), n(D5,E,P), n(E5,Q,MP), n(A5,Q,MF), n(E5,Q,MP)]
lh += alberti(A3, C4, E4, vel=PP)

# m24 (dm): Further into D minor
rh += [n(F5,Q,MF), n(E5,Q,MP), n(D5,Q,P), n(C5,Q,P)]
lh += alberti(D3, F3, A3, vel=PP)

# m25 (G): The clouds part — dominant preparation begins
rh += [n(B4,E,P), n(C5,E,MP), n(D5,Q,MF), n(G5,Q,F), n(F5,Q,MF)]
lh += alberti(G3, B3, D4)

# m26 (G7): Dominant seventh — building anticipation
rh += [n(E5,Q,MF), n(F5,E,MF), n(E5,E,MP), n(D5,Q,MP), n(B4,Q,P)]
lh += alberti(G3, B3, F4)  # G7 chord: G-B-D-F, using F as top

# m27 (G pedal): Dominant pedal — tension building
rh += [n(C5,Q,MP), n(D5,Q,MF), n(E5,Q,MF), n(F5,Q,F)]
lh += [n(G3,Q,MP), n(G3,Q,MP), n(G3,Q,MF), n(G3,Q,MF)]

# m28 (G → C): Release approaching — the retransition
rh += [n(G5,Q,F), n(F5,E,MF), n(E5,E,MF), n(D5,H,MP)]
lh += [n(G3,Q,MF), n(G3,Q,MP), n(G3,H,MP)]

# ───────────────────────────────────────────────
#  RECAPITULATION — First Theme (mm. 29-36, C major)
#  The joy of homecoming
# ───────────────────────────────────────────────

# mm. 29-36 = mm. 1-8 (exact repeat of first theme)

# m29 (I)
rh += [n(E5,E,MP), n(D5,E,MP), n(C5,Q,MF), n(E5,Q,MF), n(G5,Q,MF)]
lh += alberti(C3, E3, G3)

# m30 (V)
rh += [n(F5,Q,MF), n(E5,Q,MP), n(D5,H,MP)]
lh += alberti(G3, B3, D4)

# m31 (IV)
rh += [n(E5,E,MP), n(F5,E,MP), n(G5,Q,MF), n(A5,Q,F), n(G5,Q,MF)]
lh += alberti(F3, A3, C4)

# m32 (V → half cadence)
rh += [n(G5,Q,MF), n(F5,E,MP), n(E5,E,MP), n(D5,H,MP)]
lh += alberti(G3, B3, D4)

# m33 (I)
rh += [n(C5,E,MP), n(D5,E,MP), n(E5,Q,MF), n(G5,Q,MF), n(C6,Q,F)]
lh += alberti(C3, E3, G3)

# m34 (IV)
rh += [n(A5,Q,MF), n(G5,Q,MF), n(F5,Q,MP), n(E5,Q,MP)]
lh += alberti(F3, A3, C4)

# m35 (ii → V)
rh += [n(D5,Q,MP), n(E5,E,MP), n(F5,E,MF), n(E5,Q,MF), n(D5,Q,MP)]
lh += alberti(D3, F3, A3, dur=H) + alberti(G3, B3, D4, dur=H)

# m36 (I): PAC
rh += [n(C5,H,F), rest(H)]
lh += [n(C3,Q,MF), n(E3,Q,MP), n(G3,Q,MP), n(C4,Q,MP)]

# ───────────────────────────────────────────────
#  RECAPITULATION — Modified Transition (mm. 37-40)
#  Stays in C this time
# ───────────────────────────────────────────────

# m37 (I): Similar energy to the original transition
rh += [n(G5,Q,MF), n(E5,E,MP), n(F5,E,MP), n(G5,Q,MF), n(A5,Q,F)]
lh += alberti(C3, E3, G3)

# m38 (IV): Warm subdominant colour
rh += [n(A5,Q,MF), n(G5,Q,MF), n(F5,Q,MP), n(E5,Q,MP)]
lh += alberti(F3, A3, C4)

# m39 (ii → V): Cadential preparation
rh += [n(F5,E,MP), n(G5,E,MF), n(A5,Q,MF), n(G5,Q,MF), n(E5,Q,MP)]
lh += alberti(D3, F3, A3, dur=H) + alberti(G3, B3, D4, dur=H)

# m40 (V → I): Breath before the second theme returns
rh += [n(D5,H,MP), rest(H)]
lh += [n(G3,Q,MP), n(B3,Q,PP), n(D4,Q,PP), rest(Q)]

# ───────────────────────────────────────────────
#  RECAPITULATION — Second Theme (mm. 41-48, now in C major)
#  The tender melody returns, at home in C
# ───────────────────────────────────────────────

# m41 (I): Second theme transposed to C
rh += [n(E4,E,P), n(F4,E,P), n(G4,Q,MP), n(C5,Q,MF), n(G4,Q,MP)]
lh += alberti(C3, E3, G3, vel=PP)

# m42 (IV): Gentle answer in C
rh += [n(A4,Q,MP), n(G4,Q,MP), n(F4,Q,P), n(E4,Q,P)]
lh += alberti(F3, A3, C4, vel=PP)

# m43 (I): Rising warmth
rh += [n(G4,E,P), n(A4,E,MP), n(B4,Q,MF), n(D5,Q,MF), n(B4,Q,MP)]
lh += alberti(C3, E3, G3, vel=PP)

# m44 (V): Half cadence, gently
rh += [n(C5,Q,MF), n(B4,E,MP), n(A4,E,P), n(G4,H,P)]
lh += alberti(G3, B3, D4, vel=PP)

# m45 (I): Second phrase of second theme in C
rh += [n(E5,Q,MF), n(D5,E,MP), n(C5,E,MP), n(D5,Q,MF), n(B4,Q,MP)]
lh += alberti(C3, E3, G3, vel=PP)

# m46 (IV): Flowing
rh += [n(A4,Q,MP), n(C5,Q,MF), n(B4,Q,MP), n(A4,Q,MP)]
lh += alberti(F3, A3, C4, vel=PP)

# m47 (V → I): Final cadential approach
rh += [n(G4,E,MP), n(A4,E,MP), n(B4,E,MF), n(C5,E,MF), n(D5,Q,F), n(B4,Q,MF)]
lh += alberti(G3, B3, D4, vel=PP)

# m48 (I): Peaceful cadence
rh += [n(C5,H,MF), rest(H)]
lh += [n(C3,Q,MP), n(E3,Q,PP), n(G3,Q,PP), rest(Q)]

# ───────────────────────────────────────────────
#  CODA (mm. 49-52)
#  A gentle closing — like a smile and a bow
# ───────────────────────────────────────────────

# m49 (I): Rising arpeggio — bright and warm
rh += [n(E5,Q,MF), n(C5,Q,MP), n(E5,Q,MF), n(G5,Q,F)]
lh += [n(C3,Q,MP), n(E3,Q,PP), n(G3,Q,PP), n(C4,Q,MP)]

# m50 (IV → V): Subdominant to dominant colour
rh += [n(A5,Q,F), n(F5,Q,MF), n(G5,Q,MF), n(D5,Q,MP)]
lh += [n(F3,Q,MP), n(A3,Q,PP), n(G3,Q,MP), n(B3,Q,PP)]

# m51 (I): Playful closing figure
rh += [n(E5,E,MP), n(D5,E,MP), n(C5,E,P), n(D5,E,P), n(E5,Q,MF), n(G5,Q,MF)]
lh += alberti(C3, E3, G3)

# m52 (I): Final chord — a gentle ending
rh += [n(C5,H,F), rest(H)]
lh += [n(C3,H,MF), rest(H)]


# ═══════════════════════════════════════════════════════════════════
#  GENERATE MIDI FILE
# ═══════════════════════════════════════════════════════════════════

mid = MidiFile(ticks_per_beat=TPB)

# Track 0: Tempo and metadata
meta_track = MidiTrack()
mid.tracks.append(meta_track)
meta_track.append(MetaMessage('track_name', name='Sonatina in C Major', time=0))
meta_track.append(MetaMessage('set_tempo', tempo=mido.bpm2tempo(108), time=0))
meta_track.append(MetaMessage('time_signature', numerator=4, denominator=4, time=0))
meta_track.append(MetaMessage('key_signature', key='C', time=0))
meta_track.append(MetaMessage('text',
    text='Sonatina in C Major, "Fuer meine liebe Nichte" - in the style of W.A. Mozart',
    time=0))
meta_track.append(MetaMessage('end_of_track', time=0))

# Track 1: Right hand (treble)
rh_track = MidiTrack()
mid.tracks.append(rh_track)
rh_track.append(MetaMessage('track_name', name='Right Hand', time=0))
rh_track.append(Message('program_change', program=0, time=0))  # Acoustic Grand Piano
notes_to_track(rh, rh_track, channel=0)
rh_track.append(MetaMessage('end_of_track', time=0))

# Track 2: Left hand (bass)
lh_track = MidiTrack()
mid.tracks.append(lh_track)
lh_track.append(MetaMessage('track_name', name='Left Hand', time=0))
lh_track.append(Message('program_change', program=0, time=0))  # Acoustic Grand Piano
notes_to_track(lh, lh_track, channel=1)
lh_track.append(MetaMessage('end_of_track', time=0))

midi_path = 'sonatina_in_c_major.mid'
mid.save(midi_path)
print(f"MIDI file saved: {midi_path}")


# ═══════════════════════════════════════════════════════════════════
#  GENERATE LILYPOND FILE (for engraved score)
# ═══════════════════════════════════════════════════════════════════

LILY_NOTE_NAMES = ['c', 'cis', 'd', 'dis', 'e', 'f', 'fis', 'g', 'gis', 'a', 'ais', 'b']

LILY_DURATIONS = {
    W:  '1',
    DH: '2.',
    H:  '2',
    DQ: '4.',
    Q:  '4',
    E:  '8',
    S:  '16',
}


def midi_to_lily(midi_note):
    """Convert MIDI note number to LilyPond note name."""
    note_name = LILY_NOTE_NAMES[midi_note % 12]
    octave_marks = (midi_note // 12) - 4
    if octave_marks > 0:
        note_name += "'" * octave_marks
    elif octave_marks < 0:
        note_name += "," * (-octave_marks)
    return note_name


def dur_to_lily(ticks):
    """Convert tick duration to LilyPond duration string."""
    if ticks in LILY_DURATIONS:
        return LILY_DURATIONS[ticks]
    # Fallback: find closest
    closest = min(LILY_DURATIONS.keys(), key=lambda k: abs(k - ticks))
    return LILY_DURATIONS[closest]


def notes_to_lily(notes, bar_len=W):
    """Convert note list to LilyPond string with bar lines."""
    lily_notes = []
    bar_ticks = 0
    for pitch, dur, vel in notes:
        if pitch is None:
            lily_notes.append(f"r{dur_to_lily(dur)}")
        else:
            lily_notes.append(f"{midi_to_lily(pitch)}{dur_to_lily(dur)}")
        bar_ticks += dur
        if bar_ticks >= bar_len:
            bar_ticks = 0
            # Add a space for readability (LilyPond handles bar lines automatically)
            lily_notes.append(' ')
    return ' '.join(lily_notes)


lilypond = f'''\\version "2.24.0"

\\header {{
  title = "Sonatina in C Major"
  subtitle = "Für meine liebe Nichte"
  composer = "In the style of W.A. Mozart"
  tagline = "Generated with love and a little bit of code"
}}

\\paper {{
  #(set-paper-size "a4")
}}

global = {{
  \\key c \\major
  \\time 4/4
  \\tempo "Allegretto grazioso" 4 = 108
}}

right = \\relative {{
  \\clef treble
  \\global
  {notes_to_lily(rh)}
  \\bar "|."
}}

left = \\relative {{
  \\clef bass
  \\global
  {notes_to_lily(lh)}
  \\bar "|."
}}

\\score {{
  \\new PianoStaff <<
    \\new Staff = "right" \\right
    \\new Staff = "left" \\left
  >>
  \\layout {{ }}
  \\midi {{ }}
}}
'''

lily_path = 'sonatina_in_c_major.ly'
with open(lily_path, 'w') as f:
    f.write(lilypond)
print(f"LilyPond file saved: {lily_path}")

# Print a summary
total_bars = 52
duration_seconds = total_bars * 4 * 60 / 108  # 4 beats per bar at 108 BPM
print(f"\n{'='*50}")
print(f"  Sonatina in C Major")
print(f"  'Für meine liebe Nichte'")
print(f"  In the style of W.A. Mozart")
print(f"{'='*50}")
print(f"  Key:       C major")
print(f"  Tempo:     Allegretto grazioso (♩= 108)")
print(f"  Time sig:  4/4")
print(f"  Length:    {total_bars} measures")
print(f"  Duration:  ~{duration_seconds:.0f} seconds ({duration_seconds/60:.1f} minutes)")
print(f"  Form:      Sonata form (exposition–development–recapitulation–coda)")
print(f"{'='*50}")
print(f"  Files generated:")
print(f"    MIDI:     {midi_path}")
print(f"    LilyPond: {lily_path}")
print(f"{'='*50}")
