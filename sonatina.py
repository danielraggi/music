#!/usr/bin/env python3
"""
Sonatina in C Major, "Fur meine liebe Nichte"
(For My Dear Niece)

In the style of W.A. Mozart

Key Mozartean features employed:
  - Scalar 16th-note runs connecting melodic anchor points
  - Written-out trills and turns (mordents)
  - Appoggiaturas (accented non-chord tones resolving stepwise)
  - Varied left-hand textures (Alberti, broken octaves, bass+chord, walking bass)
  - Galant schemata: Prinner (descending 6-5-4-3), Do-Re-Mi openings
  - Cadential 6/4 chords, secondary dominants
  - "Sighing" appoggiatura pairs
  - Sequences (melodic patterns repeated at different pitch levels)
  - Grace notes and ornamental figuration
  - Dynamic shaping within phrases

Structure (Allegretto grazioso, 4/4, C major):
  Exposition  mm. 1-24:   First theme (C), transition, second theme (G), closing
  Development mm. 25-36:  Motivic fragmentation through minor keys, retransition
  Recap       mm. 37-56:  Both themes in C
  Coda        mm. 57-62:  Brilliant closing
"""

import mido
from mido import MidiFile, MidiTrack, Message, MetaMessage

# ─── Duration constants (ticks, 480 ticks per quarter note) ───

TPB = 480
W  = TPB * 4       # whole note
DH = TPB * 3       # dotted half
H  = TPB * 2       # half
DQ = TPB + TPB//2   # dotted quarter
Q  = TPB           # quarter
E  = TPB // 2      # eighth
S  = TPB // 4      # sixteenth
T  = TPB // 6      # triplet eighth (not used much, but available)

# ─── MIDI pitch constants ───

C2, D2, E2, F2, G2, A2, B2 = 36, 38, 40, 41, 43, 45, 47
C3, D3, E3, F3, G3, A3, B3 = 48, 50, 52, 53, 55, 57, 59
C4, D4, E4, F4, G4, A4, B4 = 60, 62, 64, 65, 67, 69, 71
C5, D5, E5, F5, G5, A5, B5 = 72, 74, 76, 77, 79, 81, 83
C6, D6 = 84, 86

# Accidentals
Cs3, Cs4, Cs5 = 49, 61, 73
Eb3, Eb4, Eb5 = 51, 63, 75
Fs3, Fs4, Fs5 = 54, 66, 78
Gs3, Gs4, Gs5 = 56, 68, 80
Bb3, Bb4, Bb5 = 58, 70, 82
Ab4, Ab5 = 68, 80  # enharmonic with G# but conceptually different

R = None  # rest

# ─── Velocity levels ───
FF  = 100
F   = 88
MF  = 76
MP  = 66
P   = 54
PP  = 44

# ─── Note / rest constructors ───

def n(pitch, dur, vel=MF):
    return (pitch, dur, vel)

def rest(dur):
    return (R, dur, 0)


# ─── LH pattern generators ───

def alberti(bottom, middle, top, dur=W, vel=PP):
    """Classic Alberti bass: bottom-top-middle-top in eighth notes."""
    notes = []
    pattern = [bottom, top, middle, top]
    for i in range(dur // E):
        notes.append(n(pattern[i % 4], E, vel))
    return notes


def bass_alberti(bass_note, middle, top, dur=W, vel=PP):
    """Bass note on beat 1, then Alberti from beat 2. More varied than pure Alberti."""
    notes = [n(bass_note, Q, vel + 10)]
    pattern = [top, middle, top, middle, top, middle]
    remaining = dur - Q
    for i in range(remaining // E):
        notes.append(n(pattern[i % len(pattern)], E, vel))
    return notes


def bass_chord(bass, chord_pitches, vel=PP):
    """Bass note (quarter) then block chord (quarter) repeated — like a march."""
    notes = []
    # For MIDI we play the chord as an arpeggio since we can't do simultaneous notes
    # in a single voice. We'll use a quick broken chord instead.
    notes.append(n(bass, Q, vel + 12))
    # Arpeggiate the chord quickly
    each = Q // len(chord_pitches)
    for p in chord_pitches:
        notes.append(n(p, each, vel))
    notes.append(n(bass, Q, vel + 12))
    each = Q // len(chord_pitches)
    for p in chord_pitches:
        notes.append(n(p, each, vel))
    return notes


def walking_bass(pitches, dur_each=Q, vel=PP):
    """Walking bass line — each pitch gets the same duration."""
    return [n(p, dur_each, vel + 5) for p in pitches]


# ─── Ornament helpers ───

def trill(main, upper, beats=1, vel=MF):
    """Written-out trill: rapid alternation main-upper in 16th notes."""
    notes = []
    num_notes = (Q * beats) // S
    for i in range(num_notes):
        notes.append(n(main if i % 2 == 0 else upper, S, vel - 5 if i > 0 else vel))
    return notes


def turn(above, main, below, vel=MF):
    """4-note turn figure in 16th notes: above-main-below-main."""
    return [n(above, S, vel), n(main, S, vel-5), n(below, S, vel-5), n(main, S, vel)]


def scale_run(start_pitch, end_pitch, dur_total, vel=MF, scale=None):
    """Scalar run between two pitches. Uses C major scale by default."""
    if scale is None:
        # C major scale MIDI pitches across several octaves
        scale = []
        for octave_base in [36, 48, 60, 72, 84]:
            for interval in [0, 2, 4, 5, 7, 9, 11]:
                scale.append(octave_base + interval)
        scale = sorted(set(scale))

    # Find scale tones between start and end
    if start_pitch <= end_pitch:
        run_notes = [p for p in scale if start_pitch <= p <= end_pitch]
    else:
        run_notes = [p for p in scale if end_pitch <= p <= start_pitch]
        run_notes.reverse()

    if len(run_notes) == 0:
        return [n(start_pitch, dur_total, vel)]

    each_dur = dur_total // len(run_notes)
    if each_dur == 0:
        each_dur = S
    # Adjust last note to fill any remainder
    notes = []
    used = 0
    for i, p in enumerate(run_notes):
        if i == len(run_notes) - 1:
            notes.append(n(p, dur_total - used, vel))
        else:
            notes.append(n(p, each_dur, vel - 3))
            used += each_dur
    return notes


def appoggiatura(app_pitch, main_pitch, total_dur, vel=MF):
    """Appoggiatura: accented non-chord tone resolving to main note.
    The appoggiatura takes half the duration (Mozart convention)."""
    half = total_dur // 2
    return [n(app_pitch, half, vel + 8), n(main_pitch, half, vel)]


def grace(grace_pitch, main_pitch, main_dur, vel=MF):
    """Short grace note (acciaccatura) before main note."""
    grace_dur = S // 2  # very short
    return [n(grace_pitch, grace_dur, vel - 10), n(main_pitch, main_dur - grace_dur, vel)]


# ─── Measure duration checker ───

def check_measure(notes, bar_num, expected=W):
    total = sum(dur for _, dur, _ in notes)
    if total != expected:
        print(f"WARNING: measure {bar_num} has {total} ticks, expected {expected}")
    return notes


# ═══════════════════════════════════════════════════════════════════
#  THE MUSIC
# ═══════════════════════════════════════════════════════════════════

rh = []
lh = []

# G major scale for scalar runs in the second theme / transition
G_MAJOR = []
for ob in [36, 48, 60, 72, 84]:
    for iv in [0, 2, 4, 5, 7, 9, 11]:
        p = ob + iv
        # Replace F with F# in G major
        if p % 12 == 5:  # F natural
            continue
        G_MAJOR.append(p)
    # Add F#
    G_MAJOR.append(ob + 6)
G_MAJOR = sorted(set(G_MAJOR))

# ───────────────────────────────────────────────
#  EXPOSITION — First Theme (mm. 1-8, C major)
#  Bright, elegant, with scalar figurations
#  Modeled on the "singing allegro" style
# ───────────────────────────────────────────────

# m1 (I): Opening — ascending broken chord with a scalar turn
# "Do-Mi-Sol" arpeggio launch, then a graceful turn figure
rh += check_measure([
    n(C5, E, MF), n(E5, E, MF),   # beat 1: rising third
    n(G5, E, F), n(E5, E, MF),     # beat 2: up to G, back
    *turn(F5, E5, D5, MF),          # beat 3: turn on E (F-E-D-E in 16ths)
    n(D5, E, MP), n(C5, E, MP),     # beat 4: settling down
], 1)
lh += check_measure([
    n(C3, Q, MP), n(G3, Q, PP),     # bass note + fifth
    *alberti(C3, E3, G3, dur=H, vel=PP),  # Alberti for beats 3-4
], 1)

# m2 (V7): Answering phrase — descent with appoggiatura
rh += check_measure([
    *appoggiatura(F5, E5, Q, MF),   # beat 1: F→E appoggiatura (sigh!)
    n(D5, Q, MP),                     # beat 2: stepping down
    n(B4, E, MP), n(C5, S, P),       # beat 3: reaching for resolution...
    n(D5, S, MP), n(D5, Q, MP),      # ... with grace, landing on D
], 2)
lh += check_measure(
    alberti(G3, B3, D4, vel=PP), 2
)

# m3 (I): Sequential repetition — same pattern up a step (sequence!)
rh += check_measure([
    n(D5, E, MF), n(F5, E, MF),     # beat 1: rising third from D
    n(A5, E, F), n(F5, E, MF),       # beat 2: up to A, back
    *turn(G5, F5, E5, MF),           # beat 3: turn on F
    n(E5, E, MP), n(D5, E, MP),      # beat 4: settling
], 3)
lh += check_measure([
    n(F3, Q, MP), n(C4, Q, PP),     # IV chord bass
    *alberti(F3, A3, C4, dur=H, vel=PP),
], 3)

# m4 (V): Half cadence with scalar flourish
rh += check_measure([
    n(E5, E, MF), n(D5, E, MP),      # beat 1: stepping down
    *scale_run(C5, G5, Q, MP),        # beat 2: scalar run up C-D-E-F-G (4 16ths + adjustment)
    n(F5, E, MF), n(E5, E, MP),      # beat 3
    n(D5, Q, MP),                     # beat 4: half cadence, landing on D over V
], 4)
lh += check_measure(
    alberti(G3, B3, D4, vel=PP), 4
)

# m5 (I): Consequent phrase — same opening but reaching higher
rh += check_measure([
    n(C5, E, MF), n(E5, E, MF),
    n(G5, E, F), n(C6, E, F),        # beat 2: now reaching up to C6!
    *turn(D6, C6, B5, F),            # beat 3: turn at the peak
    n(A5, E, MF), n(G5, E, MF),      # beat 4: graceful descent begins
], 5)
lh += check_measure([
    n(C3, Q, MP), n(E3, Q, PP),
    *alberti(C3, E3, G3, dur=H, vel=PP),
], 5)

# m6 (IV): Lyrical descent with sighing appoggiaturas
rh += check_measure([
    *appoggiatura(A5, G5, Q, MF),     # beat 1: A→G sigh
    *appoggiatura(F5, E5, Q, MP),     # beat 2: F→E sigh (sequence of sighs!)
    n(D5, Q, MP),                      # beat 3: continuing down
    n(C5, Q, P),                       # beat 4: arriving
], 6)
lh += check_measure(
    alberti(F3, A3, C4, vel=PP), 6
)

# m7 (ii6 → V): Cadential 6/4 approach with written-out trill
rh += check_measure([
    n(D5, E, MP), n(E5, E, MF),       # beat 1: ii chord color
    n(F5, E, MF), n(D5, E, MP),       # beat 2: reaching up, falling back
    *trill(D5, E5, beats=1, vel=MF),   # beat 3: trill on D (cadential trill!)
    n(C5, Q, F),                       # beat 4: resolution to tonic
], 7)
lh += check_measure([
    *alberti(D3, F3, A3, dur=H, vel=PP),   # ii chord
    n(G3, Q, MP), n(C3, Q, MF),            # V → I bass
], 7)

# m8 (I): Cadence — decisive arrival with flourish
rh += check_measure([
    n(E5, Q, F),                           # beat 1: strong tonic
    *scale_run(G5, C5, Q, MF),             # beat 2: scalar flourish down
    n(C5, H, MF),                          # beats 3-4: held tonic
], 8)
lh += check_measure([
    n(C3, Q, MF), n(G3, Q, PP),
    n(C3, H, MP),                          # solid tonic bass
], 8)


# ───────────────────────────────────────────────
#  EXPOSITION — Transition (mm. 9-14)
#  Energetic, with running 16ths and modulation to G
# ───────────────────────────────────────────────

# m9 (I): Forte, energetic — scales in the RH
rh += check_measure([
    *scale_run(C5, G5, H, F),              # beats 1-2: ascending scale run
    n(G5, Q, F),                            # beat 3: arrival
    n(E5, E, MF), n(F5, E, MF),            # beat 4: pickup for next bar
], 9)
lh += check_measure(
    walking_bass([C3, E3, G3, C4], Q, PP), 9  # walking bass ascending
)

# m10 (vi): Surprise! A minor color
rh += check_measure([
    n(G5, E, F), n(A5, E, F),
    n(B5, E, F), n(A5, E, MF),             # beat 2: reaching up
    n(G5, E, MF), n(E5, E, MP),
    n(C5, E, MP), n(E5, E, MF),            # beat 4: arpeggio
], 10)
lh += check_measure(
    alberti(A3, C4, E4, vel=PP), 10
)

# m11 (V/V → V): Introducing F#, dominant of G
rh += check_measure([
    n(D5, E, MF), n(Fs5, E, F),           # beat 1: D-F# — the V/V signal!
    n(A5, E, F), n(Fs5, E, MF),            # beat 2: outlining D major
    *scale_run(G5, D5, Q, MF, G_MAJOR),    # beat 3: scalar descent in G major
    n(D5, Q, MP),                            # beat 4: dominant note
], 11)
lh += check_measure([
    n(D3, Q, MP), n(Fs3, Q, PP),
    n(A3, Q, PP), n(D3, Q, MP),
], 11)

# m12 (V pedal → resolution): Dominant of G — buildup
rh += check_measure([
    *trill(Fs5, G5, beats=1, vel=F),        # beat 1: trill on F# → G
    n(G5, E, F), n(A5, E, F),               # beat 2: burst of energy
    n(B5, E, F), n(A5, E, MF),              # beat 3
    n(G5, Q, MF),                             # beat 4: landing on G
], 12)
lh += check_measure([
    n(D3, Q, MP), n(D3, Q, MP),
    n(D3, Q, MP), n(G3, Q, MF),              # V → I of G
], 12)

# m13 (I of G): Confirm G major with a decisive gesture
rh += check_measure([
    n(G5, E, F), n(B5, E, F),
    n(D6, Q, FF),                             # beat 2: triumphant high D!
    *scale_run(D6, G5, Q, F, G_MAJOR),        # beat 3: cascading down
    n(G5, Q, MF),                              # beat 4: settling
], 13)
lh += check_measure([
    n(G3, Q, MF), n(B3, Q, PP),
    n(D4, Q, PP), n(G3, Q, MP),
], 13)

# m14 (V of G → I): Brief cadential moment before second theme
rh += check_measure([
    n(A5, E, MF), n(Fs5, E, MF),             # beat 1: V of G color
    n(G5, Q, MF),                              # beat 2: resolution
    rest(H),                                    # beats 3-4: breath (silence before lyrical theme)
], 14)
lh += check_measure([
    n(D3, Q, MP), n(G3, Q, MP),
    rest(H),
], 14)


# ───────────────────────────────────────────────
#  EXPOSITION — Second Theme (mm. 15-22, G major)
#  Tender, singing, with galant appoggiaturas
#  "The niece's theme" — sweet and personal
# ───────────────────────────────────────────────

# m15 (I of G): Gentle singing melody — espressivo
rh += check_measure([
    n(B4, DQ, P),                              # beat 1+: held note, singing
    n(A4, E, PP),                              # pickup to beat 2
    n(G4, E, P), n(A4, E, P),                 # beat 3: gentle motion
    n(B4, E, MP), n(D5, E, MP),               # beat 4: opening up
], 15)
lh += check_measure(
    alberti(G3, B3, D4, vel=PP), 15
)

# m16 (I → IV of G): The melody blossoms
rh += check_measure([
    n(D5, DQ, MP),                             # beat 1+: held D
    n(C5, E, P),                               # graceful step down
    *appoggiatura(E5, D5, Q, MP),              # beat 3: E→D appoggiatura (the "sigh")
    n(C5, Q, P),                               # beat 4: descending
], 16)
lh += check_measure([
    *alberti(G3, B3, D4, dur=H, vel=PP),
    *alberti(C3, E3, G3, dur=H, vel=PP),       # IV of G
], 16)

# m17 (I of G): Rising, more passionate
rh += check_measure([
    n(D5, E, MP), n(E5, E, MP),
    n(Fs5, E, MF), n(G5, E, MF),              # beat 2: rising through F#
    n(A5, DQ, F),                               # beat 3+: peak! — held with feeling
    n(G5, E, MF),                               # resolution
], 17)
lh += check_measure(
    alberti(G3, B3, D4, vel=PP), 17
)

# m18 (V of G): Sighing descent with appoggiatura
rh += check_measure([
    *appoggiatura(Fs5, E5, Q, MF),            # beat 1: F#→E sigh
    *appoggiatura(D5, C5, Q, P),              # beat 2: D→C sigh (descending sequence of sighs)
    n(B4, E, P), n(A4, E, PP),                # beat 3: trailing off
    n(A4, Q, PP),                               # beat 4: resting on dominant
], 18)
lh += check_measure([
    *alberti(D3, Fs3, A3, dur=H, vel=PP),      # V of G
    *alberti(D3, Fs3, A3, dur=H, vel=PP),
], 18)

# m19 (I of G): Second phrase — with an ornamental turn
rh += check_measure([
    n(G5, E, MF), n(Fs5, E, MP),              # beat 1: start from high
    n(E5, E, MP), n(D5, E, P),                 # beat 2: gentle descent
    *turn(E5, D5, C5, MP),                     # beat 3: turn on D
    n(B4, Q, P),                                # beat 4: landing softly
], 19)
lh += check_measure(
    alberti(G3, B3, D4, vel=PP), 19
)

# m20 (IV → V of G): Moving toward cadence
rh += check_measure([
    n(C5, Q, P),                                # beat 1: subdominant color
    n(E5, E, MP), n(D5, E, P),                 # beat 2: reaching up and falling
    *trill(Cs5, D5, beats=1, vel=MP),          # beat 3: trill on C# (=leading tone to D, V of G)
    n(D5, Q, MP),                               # beat 4: cadential arrival on D
], 20)
lh += check_measure([
    n(C3, Q, PP), n(E3, Q, PP),                # IV
    n(A3, Q, PP), n(D3, Q, MP),                # ii → V of G
], 20)

# m21 (V → I of G): Cadential resolution with grace
rh += check_measure([
    n(D5, E, MP), n(E5, E, MF),
    n(Fs5, E, MF), n(A5, E, F),                # beat 2: rising to cadential peak
    *trill(A5, B5, beats=1, vel=F),             # beat 3: trill on A before resolution
    n(G5, Q, F),                                 # beat 4: resolution to G! PAC in G major
], 21)
lh += check_measure([
    n(D3, Q, MP), n(D4, Q, PP),
    n(D3, Q, MP), n(G3, Q, MF),                # V → I
], 21)

# m22 (I of G): Closing gesture — confirming G major
rh += check_measure([
    n(B5, E, F), n(G5, E, MF),
    n(D5, E, MF), n(B4, E, MP),               # beat 2: descending arpeggio
    n(G4, Q, MP),                               # beat 3: low arrival
    rest(Q),                                     # beat 4: breath
], 22)
lh += check_measure([
    n(G3, Q, MF), n(D3, Q, PP),
    n(G3, Q, MP), rest(Q),
], 22)


# ───────────────────────────────────────────────
#  EXPOSITION — Closing Theme (mm. 23-24, G major)
#  Brilliant closing figures
# ───────────────────────────────────────────────

# m23 (I of G): Playful closing figure with 16ths
rh += check_measure([
    *scale_run(G4, D5, Q, MF, G_MAJOR),       # beat 1: running up
    *scale_run(D5, G5, Q, F, G_MAJOR),         # beat 2: continuing up!
    n(G5, Q, F),                                # beat 3: top
    *scale_run(G5, D5, Q, MF, G_MAJOR),        # beat 4: running back down
], 23)
lh += check_measure(
    alberti(G3, B3, D4, vel=PP), 23
)

# m24 (V → I of G): Final closing cadence of exposition
rh += check_measure([
    n(D5, E, MF), n(E5, E, MF),
    n(Fs5, E, F), n(G5, E, F),                 # beat 2: approaching cadence
    *trill(Fs5, G5, beats=1, vel=F),            # beat 3: cadential trill
    n(G5, Q, FF),                                # beat 4: final G!
], 24)
lh += check_measure([
    n(D3, Q, MP), n(D4, Q, PP),
    n(D3, Q, MP), n(G3, Q, F),                  # strong V-I cadence
], 24)


# ───────────────────────────────────────────────
#  DEVELOPMENT (mm. 25-36)
#  Dramatic contrast — minor keys, fragmentation,
#  sequences, building tension toward retransition
# ───────────────────────────────────────────────

# m25 (em): Suddenly piano — first theme motive in E minor (dark!)
rh += check_measure([
    n(B4, E, P), n(E5, E, P),                  # m1 motive transposed to E minor
    n(G5, E, MP), n(E5, E, P),
    *turn(F5, E5, D5, P),                       # turn, but now with F natural — minor!
    n(D5, E, P), n(B4, E, PP),
], 25)
lh += check_measure(
    alberti(E3, G3, B3, vel=PP), 25
)

# m26 (em → am): Descending with pathos
rh += check_measure([
    *appoggiatura(C5, B4, Q, MP),              # beat 1: C→B sigh in minor context
    n(A4, Q, P),                                # beat 2: continuing down
    n(G4, E, PP), n(A4, E, P),
    n(B4, E, P), n(C5, E, MP),                 # beat 4: turning upward
], 26)
lh += check_measure([
    *alberti(E3, G3, B3, dur=H, vel=PP),
    *alberti(A3, C4, E4, dur=H, vel=PP),        # shifting to A minor
], 26)

# m27 (am): A minor — sequence of the first theme fragment
rh += check_measure([
    n(A4, E, P), n(C5, E, P),                  # same motive, now from A
    n(E5, E, MP), n(C5, E, P),
    *turn(D5, C5, B4, P),
    n(B4, E, P), n(A4, E, PP),
], 27)
lh += check_measure(
    alberti(A3, C4, E4, vel=PP), 27
)

# m28 (dm): Further descent — D minor
rh += check_measure([
    *appoggiatura(E5, D5, Q, MP),
    n(C5, E, P), n(Bb4, E, P),                 # Bb! — D minor flavor
    n(A4, Q, P),
    n(D5, Q, MP),                               # beat 4: D minor root
], 28)
lh += check_measure(
    alberti(D3, F3, A3, vel=PP), 28
)

# m29 (G7): The clouds begin to part — dominant seventh of C
rh += check_measure([
    n(D5, E, MP), n(F5, E, MF),               # beat 1: D-F — the 7th chord interval
    n(E5, E, MF), n(D5, E, MP),
    n(B4, E, MP), n(D5, E, MF),               # beat 3: bouncing off B (leading tone!)
    n(F5, E, MF), n(D5, E, MP),
], 29)
lh += check_measure([
    n(G3, Q, MP), n(G3, Q, MP),               # G pedal beginning
    n(G3, Q, MP), n(G3, Q, MF),
], 29)

# m30 (G7 cont.): Building intensity — 16th note figurations
rh += check_measure([
    *scale_run(D5, G5, Q, MF),                 # beat 1: scale up
    *scale_run(G5, D5, Q, MF),                 # beat 2: scale down (restless!)
    *scale_run(D5, A5, Q, F),                  # beat 3: scale up further
    *scale_run(A5, D5, Q, F),                  # beat 4: and back
], 30)
lh += check_measure([
    n(G3, Q, MF), n(B3, Q, MP),               # dominant harmony growing
    n(G3, Q, MF), n(F3, Q, MF),               # G7: adding the 7th in the bass!
], 30)

# m31 (G pedal): Dominant pedal — tension
rh += check_measure([
    n(E5, Q, F),                                # beat 1: strong
    n(F5, E, F), n(D5, E, MF),                 # beat 2: 7th-5th of G7
    n(E5, Q, MF),                               # beat 3: insistent
    n(F5, E, MF), n(D5, E, MP),                # beat 4: again!
], 31)
lh += check_measure([
    n(G3, Q, MF), n(G3, Q, MP),
    n(G3, Q, MF), n(G3, Q, MF),               # relentless pedal
], 31)

# m32 (G → C): The retransition — long trill on the leading tone
rh += check_measure([
    *trill(B4, C5, beats=2, vel=F),             # beats 1-2: extended trill on B!
    *trill(D5, E5, beats=1, vel=F),             # beat 3: trill moves up
    n(D5, Q, MF),                               # beat 4: ready to resolve...
], 32)
lh += check_measure([
    n(G3, Q, MF), n(G3, Q, MF),
    n(G3, Q, F), n(G3, Q, F),                  # pedal to the very end
], 32)


# ───────────────────────────────────────────────
#  RECAPITULATION — First Theme (mm. 33-40, C major)
#  The homecoming — with extra brilliance
# ───────────────────────────────────────────────

# m33 (I): Same opening, but now with a forte arrival after the tension
rh += check_measure([
    n(C5, E, F), n(E5, E, F),                  # beat 1: triumphant return!
    n(G5, E, FF), n(E5, E, F),                 # beat 2
    *turn(F5, E5, D5, F),                       # beat 3: familiar turn
    n(D5, E, MF), n(C5, E, MF),                # beat 4
], 33)
lh += check_measure([
    n(C3, Q, F), n(G3, Q, MP),                 # strong bass
    *alberti(C3, E3, G3, dur=H, vel=PP),
], 33)

# m34 (V7): As before but with added grace note
rh += check_measure([
    *grace(F5, E5, Q, MF),                     # beat 1: grace note F→E
    n(D5, Q, MP),                               # beat 2
    n(B4, E, MP), n(C5, S, P),
    n(D5, S, MP), n(D5, Q, MP),
], 34)
lh += check_measure(
    alberti(G3, B3, D4, vel=PP), 34
)

# m35 (I → IV): Sequential rise, as in exposition
rh += check_measure([
    n(D5, E, MF), n(F5, E, MF),
    n(A5, E, F), n(F5, E, MF),
    *turn(G5, F5, E5, MF),
    n(E5, E, MP), n(D5, E, MP),
], 35)
lh += check_measure([
    n(F3, Q, MP), n(C4, Q, PP),
    *alberti(F3, A3, C4, dur=H, vel=PP),
], 35)

# m36 (V): Half cadence — scalar flourish
rh += check_measure([
    n(E5, E, MF), n(D5, E, MP),
    *scale_run(C5, G5, Q, MP),
    n(F5, E, MF), n(E5, E, MP),
    n(D5, Q, MP),
], 36)
lh += check_measure(
    alberti(G3, B3, D4, vel=PP), 36
)

# m37 (I): Consequent — reaching high
rh += check_measure([
    n(C5, E, MF), n(E5, E, MF),
    n(G5, E, F), n(C6, E, F),
    *turn(D6, C6, B5, F),
    n(A5, E, MF), n(G5, E, MF),
], 37)
lh += check_measure([
    n(C3, Q, MP), n(E3, Q, PP),
    *alberti(C3, E3, G3, dur=H, vel=PP),
], 37)

# m38 (IV → V): Sighing appoggiaturas leading to cadence
rh += check_measure([
    *appoggiatura(A5, G5, Q, MF),
    *appoggiatura(F5, E5, Q, MP),
    n(D5, Q, MP),
    n(C5, Q, P),
], 38)
lh += check_measure(
    alberti(F3, A3, C4, vel=PP), 38
)

# m39 (ii6 → V): Cadential trill
rh += check_measure([
    n(D5, E, MP), n(E5, E, MF),
    n(F5, E, MF), n(D5, E, MP),
    *trill(D5, E5, beats=1, vel=MF),
    n(C5, Q, F),
], 39)
lh += check_measure([
    *alberti(D3, F3, A3, dur=H, vel=PP),
    n(G3, Q, MP), n(C3, Q, MF),
], 39)

# m40 (I): Strong cadence — with brilliant scale
rh += check_measure([
    n(E5, Q, F),
    *scale_run(G5, C5, Q, MF),
    n(C5, H, MF),
], 40)
lh += check_measure([
    n(C3, Q, MF), n(G3, Q, PP),
    n(C3, H, MP),
], 40)


# ───────────────────────────────────────────────
#  RECAPITULATION — Transition stays in C (mm. 41-42)
# ───────────────────────────────────────────────

# m41 (I): Brief energetic transition, but staying in C
rh += check_measure([
    *scale_run(C5, G5, H, F),
    n(G5, Q, F),
    n(E5, E, MF), n(F5, E, MF),
], 41)
lh += check_measure(
    walking_bass([C3, E3, G3, C4], Q, PP), 41
)

# m42 (V → I): Quick confirmation of C
rh += check_measure([
    n(G5, E, F), n(A5, E, F),
    n(B5, E, F), n(C6, E, FF),                  # beat 2: triumphant C!
    *scale_run(C6, G5, Q, F),                    # beat 3: showering down
    n(G5, Q, MF),                                 # beat 4: settling
], 42)
lh += check_measure([
    n(G3, Q, MP), n(G3, Q, MP),
    n(G3, Q, MP), n(C3, Q, MF),                  # V → I
], 42)


# ───────────────────────────────────────────────
#  RECAPITULATION — Second Theme (mm. 43-50, now in C major)
#  The tender theme, now in the home key
# ───────────────────────────────────────────────

# m43 (I): Second theme in C — espressivo
rh += check_measure([
    n(E4, DQ, P),
    n(D4, E, PP),
    n(C4, E, P), n(D4, E, P),
    n(E4, E, MP), n(G4, E, MP),
], 43)
lh += check_measure(
    alberti(C3, E3, G3, vel=PP), 43
)

# m44 (I → IV): Blossoming
rh += check_measure([
    n(G4, DQ, MP),
    n(F4, E, P),
    *appoggiatura(A4, G4, Q, MP),
    n(F4, Q, P),
], 44)
lh += check_measure([
    *alberti(C3, E3, G3, dur=H, vel=PP),
    *alberti(F3, A3, C4, dur=H, vel=PP),
], 44)

# m45 (I): Rising with feeling
rh += check_measure([
    n(G4, E, MP), n(A4, E, MP),
    n(B4, E, MF), n(C5, E, MF),
    n(D5, DQ, F),
    n(C5, E, MF),
], 45)
lh += check_measure(
    alberti(C3, E3, G3, vel=PP), 45
)

# m46 (V): Sighing pairs
rh += check_measure([
    *appoggiatura(B4, A4, Q, MF),
    *appoggiatura(G4, F4, Q, P),
    n(E4, E, P), n(D4, E, PP),
    n(D4, Q, PP),
], 46)
lh += check_measure(
    alberti(G3, B3, D4, vel=PP), 46
)

# m47 (I): Second phrase with turn
rh += check_measure([
    n(C5, E, MF), n(B4, E, MP),
    n(A4, E, MP), n(G4, E, P),
    *turn(A4, G4, F4, MP),
    n(E4, Q, P),
], 47)
lh += check_measure(
    alberti(C3, E3, G3, vel=PP), 47
)

# m48 (IV → V): Moving toward cadence
rh += check_measure([
    n(F4, Q, P),
    n(A4, E, MP), n(G4, E, P),
    *trill(Fs4, G4, beats=1, vel=MP),           # trill on F# → G (leading tone of G? No — ornamental trill)
    n(G4, Q, MP),
], 48)
lh += check_measure([
    n(F3, Q, PP), n(A3, Q, PP),
    n(D3, Q, PP), n(G3, Q, MP),
], 48)

# m49 (V → I): Cadential resolution
rh += check_measure([
    n(G4, E, MP), n(A4, E, MF),
    n(B4, E, MF), n(D5, E, F),
    *trill(D5, E5, beats=1, vel=F),
    n(C5, Q, F),                                 # PAC in C!
], 49)
lh += check_measure([
    n(G3, Q, MP), n(G3, Q, MP),
    n(G3, Q, MF), n(C3, Q, F),                  # V → I
], 49)

# m50 (I): Closing gesture of second theme
rh += check_measure([
    n(E5, E, F), n(C5, E, MF),
    n(G4, E, MF), n(E4, E, MP),
    n(C4, Q, MP),
    rest(Q),
], 50)
lh += check_measure([
    n(C3, Q, MF), n(E3, Q, PP),
    n(C3, Q, MP), rest(Q),
], 50)


# ───────────────────────────────────────────────
#  CODA (mm. 51-56)
#  Brilliant and joyful — a final bow
# ───────────────────────────────────────────────

# m51 (I): Running scales — the closing fireworks
rh += check_measure([
    *scale_run(C5, C6, H, F),                   # beats 1-2: big ascending run!
    *scale_run(C6, G5, Q, F),                    # beat 3: cascading down
    n(G5, Q, MF),                                 # beat 4
], 51)
lh += check_measure(
    walking_bass([C3, E3, G3, C4], Q, MP), 51
)

# m52 (IV → I): Plagal color then tonic
rh += check_measure([
    *appoggiatura(A5, G5, Q, F),                 # beat 1: one last sigh
    n(E5, Q, MF),                                 # beat 2
    n(C5, E, MF), n(D5, E, MF),
    n(E5, E, MF), n(G5, E, F),                   # beat 4: pickup for final cadence
], 52)
lh += check_measure([
    n(F3, Q, MP), n(C4, Q, PP),                  # IV
    n(C3, Q, MP), n(C3, Q, MP),                  # I
], 52)

# m53 (V → I): The grand final cadence
rh += check_measure([
    n(A5, Q, F),                                   # beat 1: appoggiatura of sorts
    n(G5, Q, F),                                   # beat 2: resolving
    *trill(Fs5, G5, beats=1, vel=FF),              # beat 3: GRAND cadential trill!!
    n(G5, Q, FF),                                   # beat 4: arrival
], 53)
lh += check_measure([
    n(D3, Q, MF), n(G3, Q, MF),                   # ii → V
    n(G3, Q, F), n(C3, Q, FF),                    # V → I final
], 53)

# m54 (I): Tonic confirmation — three decisive chords (as scale runs)
rh += check_measure([
    *scale_run(C5, G5, Q, FF),                     # beat 1: C chord burst
    n(G5, Q, FF),                                    # beat 2: held
    n(E5, Q, F),                                     # beat 3: softer echo
    n(C5, Q, MF),                                    # beat 4: settling
], 54)
lh += check_measure([
    n(C3, Q, FF), n(C3, Q, FF),
    n(C3, Q, F), n(C3, Q, MF),                     # tonic pillars
], 54)

# m55 (I): Gentle final echo — piano
rh += check_measure([
    n(E5, E, P), n(D5, E, PP),
    n(C5, E, PP), n(D5, E, PP),
    n(E5, Q, P),
    n(C5, Q, P),
], 55)
lh += check_measure([
    n(C3, Q, P), n(G3, Q, PP),
    n(E3, Q, PP), n(C3, Q, P),
], 55)

# m56 (I): Final note — a smile
rh += check_measure([
    n(C5, H, MP),
    rest(H),
], 56)
lh += check_measure([
    n(C3, H, MP),
    rest(H),
], 56)


# ═══════════════════════════════════════════════════════════════════
#  GENERATE MIDI FILE
# ═══════════════════════════════════════════════════════════════════

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
rh_track.append(Message('program_change', program=0, time=0))
notes_to_track(rh, rh_track, channel=0)
rh_track.append(MetaMessage('end_of_track', time=0))

# Track 2: Left hand (bass)
lh_track = MidiTrack()
mid.tracks.append(lh_track)
lh_track.append(MetaMessage('track_name', name='Left Hand', time=0))
lh_track.append(Message('program_change', program=0, time=0))
notes_to_track(lh, lh_track, channel=1)
lh_track.append(MetaMessage('end_of_track', time=0))

midi_path = 'sonatina_in_c_major.mid'
mid.save(midi_path)
print(f"MIDI file saved: {midi_path}")


# ═══════════════════════════════════════════════════════════════════
#  GENERATE LILYPOND FILE
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
            lily_notes.append(' ')
    return ' '.join(lily_notes)


lilypond = f'''\\version "2.24.0"

\\header {{
  title = "Sonatina in C Major"
  subtitle = "Fur meine liebe Nichte"
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

# Print summary
total_bars = 56
duration_seconds = total_bars * 4 * 60 / 108
print(f"\n{'='*55}")
print(f"  Sonatina in C Major")
print(f"  'Fur meine liebe Nichte'")
print(f"  In the style of W.A. Mozart (revised)")
print(f"{'='*55}")
print(f"  Key:       C major")
print(f"  Tempo:     Allegretto grazioso (q = 108)")
print(f"  Time sig:  4/4")
print(f"  Length:    {total_bars} measures")
print(f"  Duration:  ~{duration_seconds:.0f} seconds ({duration_seconds/60:.1f} minutes)")
print(f"  Form:      Sonata form")
print(f"{'='*55}")
print(f"  Mozartean features:")
print(f"    - Scalar 16th-note runs")
print(f"    - Written-out trills at cadences")
print(f"    - Appoggiatura 'sighing' pairs")
print(f"    - Ornamental turns (mordents)")
print(f"    - Grace notes")
print(f"    - Varied LH: Alberti, walking bass, bass+chord")
print(f"    - Sequences (pattern repetition at different pitch levels)")
print(f"    - Galant cadential formulas")
print(f"    - Dynamic shaping within phrases")
print(f"{'='*55}")
print(f"  Files: {midi_path}, {lily_path}")
print(f"{'='*55}")
