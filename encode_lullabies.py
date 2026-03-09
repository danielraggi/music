#!/usr/bin/env python3
"""
Encode classical lullabies as MIDI from score knowledge.
For pieces that couldn't be downloaded from online sources.

Each piece is encoded as a simple piano arrangement — melody + basic accompaniment.
"""

import mido
from mido import MidiFile, MidiTrack, Message, MetaMessage

# ─── Duration constants (ticks, 480 ticks per quarter note) ───
TPB = 480
W  = TPB * 4       # whole note
DH = TPB * 3       # dotted half
H  = TPB * 2       # half
DQ = TPB + TPB//2  # dotted quarter
Q  = TPB           # quarter
DE = Q + Q//2      # dotted eighth (not standard name, = 3/4 of quarter... actually dotted eighth = E + S)
E  = TPB // 2      # eighth
S  = TPB // 4      # sixteenth

# Dotted eighth = E + S = 360 ticks
DOT_E = E + S

# ─── MIDI pitch helpers ───
def p(name):
    """Convert note name like 'C4', 'Bb3', 'F#5' to MIDI number."""
    notes = {'C':0,'D':2,'E':4,'F':5,'G':7,'A':9,'B':11}
    i = 0
    base = notes[name[0]]
    i = 1
    if len(name) > 2 or (len(name) == 2 and not name[1].isdigit()):
        if name[1] == '#' or name[1] == 's':
            base += 1
            i = 2
        elif name[1] == 'b':
            base -= 1
            i = 2
    octave = int(name[i:])
    return base + (octave + 1) * 12

R = None  # rest

# ─── Velocity levels ───
FF = 100; F = 88; MF = 76; MP = 66; P = 54; PP = 44

# ─── Note constructors ───
def n(pitch, dur, vel=MF):
    if isinstance(pitch, str):
        pitch = p(pitch)
    return (pitch, dur, vel)

def rest(dur):
    return (R, dur, 0)

def notes_to_track(notes, track, channel=0):
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

def save_piece(filename, title, tempo_bpm, time_num, time_den, key, rh, lh):
    mid = MidiFile(ticks_per_beat=TPB)
    meta = MidiTrack()
    mid.tracks.append(meta)
    meta.append(MetaMessage('track_name', name=title, time=0))
    meta.append(MetaMessage('set_tempo', tempo=mido.bpm2tempo(tempo_bpm), time=0))
    meta.append(MetaMessage('time_signature', numerator=time_num, denominator=time_den, time=0))
    meta.append(MetaMessage('key_signature', key=key, time=0))
    meta.append(MetaMessage('end_of_track', time=0))

    rh_track = MidiTrack()
    mid.tracks.append(rh_track)
    rh_track.append(MetaMessage('track_name', name='Melody', time=0))
    rh_track.append(Message('program_change', program=0, time=0))
    notes_to_track(rh, rh_track, channel=0)
    rh_track.append(MetaMessage('end_of_track', time=0))

    lh_track = MidiTrack()
    mid.tracks.append(lh_track)
    lh_track.append(MetaMessage('track_name', name='Accompaniment', time=0))
    lh_track.append(Message('program_change', program=0, time=0))
    notes_to_track(lh, lh_track, channel=1)
    lh_track.append(MetaMessage('end_of_track', time=0))

    mid.save(filename)
    print(f"  Saved: {filename}")


# ═══════════════════════════════════════════════════
#  1. Mozart - Wiegenlied K.350  (3/4, F major)
#     "Schlafe, mein Prinzchen, schlaf ein"
# ═══════════════════════════════════════════════════
def encode_mozart_wiegenlied():
    BAR = Q * 3  # 3/4 time
    rh = []
    lh = []

    # Melody: "Schlafe, mein Prinzchen, schlaf ein"
    # This lullaby is in 3/4, key of F major, gentle rocking feel.
    # The melody is simple and stepwise.

    # Phrase 1: "Schlafe, mein Prinzchen, schlaf ein"
    # F  F  A | Bb  A  G | F  F  A | Bb  A  G |
    rh += [n('F4',Q,MP), n('F4',Q,MP), n('A4',Q,MP)]
    lh += [n('F3',Q,PP), n('A3',Q,PP), n('C4',Q,PP)]

    rh += [n('Bb4',Q,MP), n('A4',Q,MP), n('G4',Q,MP)]
    lh += [n('F3',Q,PP), n('A3',Q,PP), n('C4',Q,PP)]

    rh += [n('F4',Q,MP), n('F4',Q,MP), n('A4',Q,MP)]
    lh += [n('F3',Q,PP), n('A3',Q,PP), n('C4',Q,PP)]

    rh += [n('Bb4',Q,MP), n('A4',Q,MP), n('G4',Q,P)]
    lh += [n('C3',Q,PP), n('E3',Q,PP), n('G3',Q,PP)]

    # Phrase 2: "Es ruhn Schäfchen und Vögelchen nun"
    # F  G  A | Bb  A  G | F  A  C5 | Bb  A  G |
    rh += [n('F4',Q,MP), n('G4',Q,MP), n('A4',Q,MP)]
    lh += [n('F3',Q,PP), n('A3',Q,PP), n('C4',Q,PP)]

    rh += [n('Bb4',Q,MF), n('A4',Q,MP), n('G4',Q,MP)]
    lh += [n('Bb2',Q,PP), n('D3',Q,PP), n('F3',Q,PP)]

    rh += [n('F4',Q,MP), n('A4',Q,MP), n('C5',Q,MF)]
    lh += [n('F3',Q,PP), n('A3',Q,PP), n('C4',Q,PP)]

    rh += [n('Bb4',Q,MP), n('A4',Q,MP), n('G4',Q,P)]
    lh += [n('C3',Q,PP), n('E3',Q,PP), n('G3',Q,PP)]

    # Phrase 3: "Garten und Wiese verstummt"
    # A  Bb  C5 | Bb  A  G | A  Bb  C5 | Bb  A  G |
    rh += [n('A4',Q,MP), n('Bb4',Q,MP), n('C5',Q,MF)]
    lh += [n('F3',Q,PP), n('A3',Q,PP), n('C4',Q,PP)]

    rh += [n('Bb4',Q,MP), n('A4',Q,MP), n('G4',Q,MP)]
    lh += [n('C3',Q,PP), n('E3',Q,PP), n('G3',Q,PP)]

    rh += [n('A4',Q,MP), n('Bb4',Q,MP), n('C5',Q,MF)]
    lh += [n('F3',Q,PP), n('A3',Q,PP), n('C4',Q,PP)]

    rh += [n('Bb4',Q,MP), n('A4',Q,MP), n('G4',Q,P)]
    lh += [n('C3',Q,PP), n('E3',Q,PP), n('G3',Q,PP)]

    # Phrase 4: return of opening - "Schlafe, mein Prinzchen, schlaf ein"
    rh += [n('F4',Q,MP), n('F4',Q,MP), n('A4',Q,MP)]
    lh += [n('F3',Q,PP), n('A3',Q,PP), n('C4',Q,PP)]

    rh += [n('Bb4',Q,MP), n('A4',Q,MP), n('G4',Q,MP)]
    lh += [n('C3',Q,PP), n('E3',Q,PP), n('G3',Q,PP)]

    rh += [n('A4',Q,P), n('G4',Q,P), n('F4',DQ,P), rest(E)]
    lh += [n('F3',Q,PP), n('C3',Q,PP), n('F3',DQ,PP), rest(E)]

    save_piece('lullabies/mozart/mozart_wiegenlied_k350.mid',
               'Mozart - Wiegenlied K.350', 80, 3, 4, 'F', rh, lh)


# ═══════════════════════════════════════════════════
#  2. Mozart - Ah! vous dirai-je, Maman K.265
#     (Twinkle Twinkle Star theme + Var. 1)
#     4/4, C major
# ═══════════════════════════════════════════════════
def encode_mozart_twinkle():
    rh = []
    lh = []

    # Theme: Twinkle Twinkle Little Star in C major
    # C C G G | A A G- | F F E E | D D C- |
    # G G F F | E E D- | G G F F | E E D- |
    # C C G G | A A G- | F F E E | D D C- |

    def simple_bass(root, fifth, dur=W):
        """Simple bass: root-fifth-root-fifth in quarters."""
        return [n(root,Q,PP), n(fifth,Q,PP), n(root,Q,PP), n(fifth,Q,PP)]

    # Line 1
    rh += [n('C4',Q,MP), n('C4',Q,MP), n('G4',Q,MP), n('G4',Q,MP)]
    lh += simple_bass('C3','G3')
    rh += [n('A4',Q,MF), n('A4',Q,MF), n('G4',H,MP)]
    lh += simple_bass('F3','C4')
    rh += [n('F4',Q,MP), n('F4',Q,MP), n('E4',Q,MP), n('E4',Q,MP)]
    lh += simple_bass('C3','G3')
    rh += [n('D4',Q,MP), n('D4',Q,MP), n('C4',H,MP)]
    lh += simple_bass('G2','D3')

    # Line 2
    rh += [n('G4',Q,MP), n('G4',Q,MP), n('F4',Q,MP), n('F4',Q,MP)]
    lh += simple_bass('C3','E3')
    rh += [n('E4',Q,MP), n('E4',Q,MP), n('D4',H,MP)]
    lh += simple_bass('G2','B2')
    rh += [n('G4',Q,MP), n('G4',Q,MP), n('F4',Q,MP), n('F4',Q,MP)]
    lh += simple_bass('C3','E3')
    rh += [n('E4',Q,MP), n('E4',Q,MP), n('D4',H,MP)]
    lh += simple_bass('G2','B2')

    # Line 3 (same as line 1)
    rh += [n('C4',Q,MP), n('C4',Q,MP), n('G4',Q,MP), n('G4',Q,MP)]
    lh += simple_bass('C3','G3')
    rh += [n('A4',Q,MF), n('A4',Q,MF), n('G4',H,MP)]
    lh += simple_bass('F3','C4')
    rh += [n('F4',Q,MP), n('F4',Q,MP), n('E4',Q,MP), n('E4',Q,MP)]
    lh += simple_bass('C3','G3')
    rh += [n('D4',Q,MP), n('D4',Q,MP), n('C4',H,MP)]
    lh += [n('G2',Q,PP), n('G2',Q,PP), n('C3',H,PP)]

    # Variation 1: Same melody but with running 16th notes
    # RH plays continuous 16ths around the melody notes
    def var1_measure(mel1, mel2, bass_root, bass_fifth):
        """Variation 1 style: 16th note figuration around melody."""
        rh_notes = []
        lh_notes = []
        for mel in [mel1, mel2]:
            mp = p(mel)
            # 16th note turn around the melody note
            rh_notes += [n(mp, S, MP), n(mp+2, S, P), n(mp, S, P), n(mp-1, S, P),
                         n(mp, S, MP), n(mp+2, S, P), n(mp+4, S, P), n(mp+2, S, P)]
        lh_notes += [n(bass_root, Q, PP), n(bass_fifth, Q, PP),
                     n(bass_root, Q, PP), n(bass_fifth, Q, PP)]
        return rh_notes, lh_notes

    # Var 1, line 1
    r, l = var1_measure('C4','G4','C3','G3'); rh += r; lh += l
    r, l = var1_measure('A4','G4','F3','C4'); rh += r; lh += l
    r, l = var1_measure('F4','E4','C3','G3'); rh += r; lh += l
    r, l = var1_measure('D4','C4','G2','D3'); rh += r; lh += l

    # Var 1, line 2
    r, l = var1_measure('G4','F4','C3','E3'); rh += r; lh += l
    r, l = var1_measure('E4','D4','G2','B2'); rh += r; lh += l
    r, l = var1_measure('G4','F4','C3','E3'); rh += r; lh += l
    r, l = var1_measure('E4','D4','G2','B2'); rh += r; lh += l

    # Var 1, line 3
    r, l = var1_measure('C4','G4','C3','G3'); rh += r; lh += l
    r, l = var1_measure('A4','G4','F3','C4'); rh += r; lh += l
    r, l = var1_measure('F4','E4','C3','G3'); rh += r; lh += l
    # Final bar - end cleanly
    rh += [n('D4',S,MP), n('E4',S,P), n('D4',S,P), n('C#4',S,P),
           n('D4',S,MP), n('E4',S,P), n('F4',S,P), n('E4',S,P),
           n('C4',H,MP)]
    lh += [n('G2',Q,PP), n('G2',Q,PP), n('C3',H,PP)]

    save_piece('lullabies/mozart/mozart_twinkle_variations_k265.mid',
               'Mozart - Ah! vous dirai-je Maman K.265', 108, 4, 4, 'C', rh, lh)


# ═══════════════════════════════════════════════════
#  3. Schubert - Wiegenlied D.498  (2/4, Ab major → simplified in G)
#     "Schlafe, schlafe, holder süsser Knabe"
# ═══════════════════════════════════════════════════
def encode_schubert_wiegenlied():
    # Simplified in G major for clarity. 2/4 time, gentle.
    BAR = Q * 2  # 2/4 time
    rh = []
    lh = []

    # "Schlafe, schlafe, holder süsser Knabe"
    # The melody is gentle and rocking, mostly stepwise

    # Phrase 1: "Schlafe, schlafe"
    rh += [n('D4',E,P), n('D4',E,P)]  # pickup
    lh += [rest(Q)]

    rh += [n('G4',Q,MP), n('G4',E,MP), n('A4',E,P)]
    lh += [n('G3',E,PP), n('B3',E,PP), n('D4',E,PP), n('B3',E,PP)]

    rh += [n('B4',Q,MP), n('A4',E,MP), n('G4',E,P)]
    lh += [n('G3',E,PP), n('B3',E,PP), n('D4',E,PP), n('B3',E,PP)]

    # "holder süsser Knabe"
    rh += [n('A4',Q,MP), n('G4',E,MP), n('F#4',E,P)]
    lh += [n('D3',E,PP), n('F#3',E,PP), n('A3',E,PP), n('F#3',E,PP)]

    rh += [n('G4',Q,MP), rest(E), n('D4',E,P)]
    lh += [n('G3',E,PP), n('B3',E,PP), n('D4',E,PP), n('B3',E,PP)]

    # Phrase 2: "Leise wiegt dich deiner Mutter Hand"
    rh += [n('G4',Q,MP), n('G4',E,MP), n('A4',E,P)]
    lh += [n('G3',E,PP), n('B3',E,PP), n('D4',E,PP), n('B3',E,PP)]

    rh += [n('B4',Q,MP), n('A4',E,MP), n('G4',E,P)]
    lh += [n('G3',E,PP), n('B3',E,PP), n('D4',E,PP), n('B3',E,PP)]

    rh += [n('C5',Q,MF), n('B4',E,MP), n('A4',E,P)]
    lh += [n('C3',E,PP), n('E3',E,PP), n('G3',E,PP), n('E3',E,PP)]

    rh += [n('B4',Q,MP), rest(E), n('D4',E,P)]
    lh += [n('G3',E,PP), n('B3',E,PP), n('D4',E,PP), n('B3',E,PP)]

    # Phrase 3: "Sanfter Schlummer, Friede, Ruh"
    rh += [n('G4',Q,MP), n('B4',E,MF), n('A4',E,MP)]
    lh += [n('G3',E,PP), n('B3',E,PP), n('D4',E,PP), n('B3',E,PP)]

    rh += [n('G4',Q,MP), n('F#4',E,MP), n('G4',E,P)]
    lh += [n('D3',E,PP), n('F#3',E,PP), n('A3',E,PP), n('F#3',E,PP)]

    rh += [n('A4',Q,MP), n('G4',E,MP), n('F#4',E,P)]
    lh += [n('D3',E,PP), n('F#3',E,PP), n('A3',E,PP), n('F#3',E,PP)]

    rh += [n('G4',Q,P), rest(Q)]
    lh += [n('G3',Q,PP), rest(Q)]

    save_piece('lullabies/schubert/schubert_wiegenlied_d498.mid',
               'Schubert - Wiegenlied D.498', 66, 2, 4, 'G', rh, lh)


# ═══════════════════════════════════════════════════
#  4. Schubert - Ave Maria D.839  (4/4, Bb → simplified in C)
#     The iconic piano intro + vocal melody
# ═══════════════════════════════════════════════════
def encode_schubert_ave_maria():
    rh = []
    lh = []

    # The famous arpeggiated piano pattern + melody
    # Simplified in C major, 4/4, very slow

    def arp_bar(bass, notes_list):
        """Arpeggiated accompaniment pattern — flowing sextuplets simplified as 8ths."""
        lh_notes = [n(bass, Q, PP)]
        for note in notes_list:
            lh_notes.append(n(note, E, PP))
        # Fill to whole bar
        while sum(d for _,d,_ in lh_notes) < W:
            for note in notes_list:
                if sum(d for _,d,_ in lh_notes) >= W:
                    break
                lh_notes.append(n(note, E, PP))
        return lh_notes

    # Piano intro (2 bars of arpeggios)
    rh += [rest(W)]
    lh += arp_bar('C3', ['E3','G3','C4','G3','E3'])

    rh += [rest(W)]
    lh += arp_bar('C3', ['E3','G3','C4','G3','E3'])

    # "Ave Maria" - melody enters
    rh += [n('E4',H,MP), n('E4',Q,MP), n('E4',E,MP), n('F4',E,P)]
    lh += arp_bar('C3', ['E3','G3','C4','G3','E3'])

    rh += [n('E4',DQ,MP), n('D4',E,P), n('D4',H,P)]
    lh += arp_bar('G2', ['D3','G3','B3','G3','D3'])

    rh += [n('D4',H,MP), n('D4',Q,MP), n('D4',E,MP), n('E4',E,P)]
    lh += arp_bar('A2', ['C3','E3','A3','E3','C3'])

    rh += [n('D4',DQ,MP), n('C4',E,P), n('C4',H,P)]
    lh += arp_bar('F2', ['A2','C3','F3','C3','A2'])

    # "Gratia plena"
    rh += [n('C4',H,MP), n('E4',Q,MF), n('G4',E,MF), n('F4',E,MP)]
    lh += arp_bar('C3', ['E3','G3','C4','G3','E3'])

    rh += [n('E4',DQ,MF), n('C5',E,F), n('C5',E,MF), n('B4',E,MP), n('A4',E,MP), n('B4',E,MP)]
    lh += arp_bar('G2', ['D3','G3','B3','G3','D3'])

    rh += [n('A4',H,MP), n('G4',Q,MP), n('F4',Q,P)]
    lh += arp_bar('F2', ['A2','C3','F3','C3','A2'])

    rh += [n('E4',W,P)]
    lh += arp_bar('C3', ['E3','G3','C4','G3','E3'])

    # Closing: "Ave Maria"
    rh += [n('C4',DH,P), rest(Q)]
    lh += [n('C3',Q,PP), n('E3',Q,PP), n('G3',Q,PP), n('C3',Q,PP)]

    save_piece('lullabies/schubert/schubert_ave_maria_d839.mid',
               'Schubert - Ave Maria D.839', 56, 4, 4, 'C', rh, lh)


# ═══════════════════════════════════════════════════
#  5. Chopin - Berceuse Op.57  (6/8, Db → simplified in C)
#     The rocking ostinato bass + ornamental melody
# ═══════════════════════════════════════════════════
def encode_chopin_berceuse():
    rh = []
    lh = []

    # The Berceuse has a famous unchanging bass pattern: tonic-dominant rocking
    # LH: C3 (dotted quarter) G3 (dotted quarter) throughout
    # RH starts simple then becomes increasingly ornamental

    BAR = DQ * 2  # 6/8 time

    def bass_bar():
        return [n('C3',DQ,PP), n('G3',DQ,PP)]

    # Bars 1-4: Simple melody introduction
    rh += [n('E4',DQ,P), n('E4',DQ,P)]
    lh += bass_bar()

    rh += [n('E4',Q,MP), n('F4',E,P), n('E4',DQ,P)]
    lh += bass_bar()

    rh += [n('E4',Q,MP), n('G4',E,MP), n('F4',Q,P), n('E4',E,P)]
    lh += bass_bar()

    rh += [n('D4',DQ,P), n('C4',DQ,P)]
    lh += bass_bar()

    # Bars 5-8: Melody becomes slightly more ornamented
    rh += [n('E4',Q,MP), n('F4',E,P), n('G4',Q,MP), n('A4',E,MP)]
    lh += bass_bar()

    rh += [n('G4',Q,MP), n('F4',E,P), n('E4',Q,P), n('D4',E,P)]
    lh += bass_bar()

    rh += [n('E4',Q,MP), n('G4',E,MP), n('C5',Q,MF), n('B4',E,MP)]
    lh += bass_bar()

    rh += [n('A4',Q,MP), n('G4',E,P), n('E4',DQ,P)]
    lh += bass_bar()

    # Bars 9-12: More ornamentation — 16th notes
    rh += [n('C5',E,MF), n('B4',S,MP), n('C5',S,MP), n('D5',E,MF), n('C5',S,MP), n('B4',S,MP)]
    lh += bass_bar()

    rh += [n('A4',E,MP), n('G4',S,P), n('A4',S,P), n('G4',E,P), n('F4',S,P), n('E4',S,P)]
    lh += bass_bar()

    rh += [n('E4',E,MP), n('G4',S,MP), n('C5',S,MF), n('E5',E,MF), n('D5',S,MF), n('C5',S,MP)]
    lh += bass_bar()

    rh += [n('B4',E,MP), n('A4',S,P), n('G4',S,P), n('E4',DQ,P)]
    lh += bass_bar()

    # Bars 13-16: Peak ornamentation then winding down
    rh += [n('E5',S,MF), n('D5',S,MP), n('C5',S,MP), n('B4',S,MP), n('C5',S,MP), n('D5',S,MP),
           n('E5',S,MF), n('G5',S,F), n('E5',S,MF), n('D5',S,MP), n('C5',S,MP), n('B4',S,MP)]
    lh += bass_bar()

    rh += [n('C5',E,MF), n('A4',S,MP), n('G4',S,P),
           n('E4',E,P), n('D4',S,P), n('C4',S,PP)]
    lh += bass_bar()

    # Gentle ending
    rh += [n('E4',Q,P), n('D4',E,PP), n('C4',DQ,PP)]
    lh += bass_bar()

    rh += [n('C4',DH,PP)]
    lh += [n('C3',DH,PP)]

    save_piece('lullabies/chopin/chopin_berceuse_op57.mid',
               'Chopin - Berceuse Op.57', 58, 6, 8, 'C', rh, lh)


# ═══════════════════════════════════════════════════
#  6. Mozart - Eine kleine Nachtmusik, Romanze K.525
#     (Andante, 2/2, C major in original → C major)
# ═══════════════════════════════════════════════════
def encode_mozart_romanze():
    rh = []
    lh = []

    # The Romanze is in C major, gentle andante
    # Famous singing melody

    # Opening phrase
    rh += [n('C5',Q,P), n('B4',E,PP), n('C5',E,PP)]
    lh += [n('C3',Q,PP), n('E3',Q,PP)]

    rh += [n('D5',Q,MP), n('G4',Q,P)]
    lh += [n('G2',Q,PP), n('B2',Q,PP)]

    rh += [n('E5',Q,MP), n('D5',E,P), n('E5',E,P)]
    lh += [n('C3',Q,PP), n('G3',Q,PP)]

    rh += [n('F5',Q,MF), n('E5',Q,MP)]
    lh += [n('A2',Q,PP), n('C3',Q,PP)]

    # Descending phrase
    rh += [n('D5',Q,MP), n('C5',E,P), n('B4',E,P)]
    lh += [n('G2',Q,PP), n('B2',Q,PP)]

    rh += [n('C5',Q,MP), n('B4',E,P), n('A4',E,PP)]
    lh += [n('C3',Q,PP), n('E3',Q,PP)]

    rh += [n('B4',Q,P), n('A4',E,PP), n('G4',E,PP)]
    lh += [n('D3',Q,PP), n('G3',Q,PP)]

    rh += [n('G4',H,P)]
    lh += [n('G2',H,PP)]

    # Second phrase - more lyrical
    rh += [n('C5',Q,MP), n('D5',E,MP), n('E5',E,MP)]
    lh += [n('C3',Q,PP), n('E3',Q,PP)]

    rh += [n('F5',Q,MF), n('E5',E,MP), n('D5',E,P)]
    lh += [n('F2',Q,PP), n('A2',Q,PP)]

    rh += [n('E5',Q,MF), n('D5',E,MP), n('C5',E,P)]
    lh += [n('G2',Q,PP), n('B2',Q,PP)]

    rh += [n('D5',H,MP)]
    lh += [n('G2',H,PP)]

    # Return and close
    rh += [n('E5',Q,MP), n('D5',E,P), n('C5',E,P)]
    lh += [n('C3',Q,PP), n('G3',Q,PP)]

    rh += [n('D5',Q,MP), n('C5',E,P), n('B4',E,PP)]
    lh += [n('G2',Q,PP), n('D3',Q,PP)]

    rh += [n('C5',H,P)]
    lh += [n('C3',H,PP)]

    save_piece('lullabies/mozart/mozart_eine_kleine_romanze_k525.mid',
               'Mozart - Eine kleine Nachtmusik, Romanze K.525', 72, 2, 2, 'C', rh, lh)


# ═══════════════════════════════════════════════════
#  7. Mozart - Ave Verum Corpus K.618
#     (Adagio, 4/4, D major → simplified in D)
# ═══════════════════════════════════════════════════
def encode_mozart_ave_verum():
    rh = []
    lh = []

    # Hymn-like, sustained, very slow
    # "Ave, ave verum corpus, natum de Maria virgine"

    rh += [n('F#4',H,P), n('F#4',H,P)]
    lh += [n('D3',H,PP), n('D3',H,PP)]

    rh += [n('E4',H,P), n('D4',H,P)]
    lh += [n('A2',H,PP), n('D3',H,PP)]

    rh += [n('F#4',H,MP), n('A4',H,MP)]
    lh += [n('D3',H,PP), n('F#3',H,PP)]

    rh += [n('G4',W,MP)]
    lh += [n('B2',H,PP), n('E3',H,PP)]

    # "natum de Maria virgine"
    rh += [n('F#4',H,MP), n('G4',H,MP)]
    lh += [n('D3',H,PP), n('E3',H,PP)]

    rh += [n('A4',H,MF), n('B4',H,MF)]
    lh += [n('F#3',H,PP), n('G3',H,PP)]

    rh += [n('A4',H,MP), n('G4',H,P)]
    lh += [n('D3',H,PP), n('B2',H,PP)]

    rh += [n('F#4',W,P)]
    lh += [n('A2',H,PP), n('D3',H,PP)]

    # "Vere passum, immolatum"
    rh += [n('A4',H,MF), n('A4',H,MF)]
    lh += [n('D3',H,PP), n('F#3',H,PP)]

    rh += [n('B4',H,MF), n('A4',H,MP)]
    lh += [n('G3',H,PP), n('D3',H,PP)]

    rh += [n('G4',H,MP), n('F#4',H,P)]
    lh += [n('E3',H,PP), n('A2',H,PP)]

    rh += [n('E4',H,P), n('D4',H,P)]
    lh += [n('A2',H,PP), n('D3',H,PP)]

    # Final "Ave verum"
    rh += [n('D4',W,P)]
    lh += [n('D3',W,PP)]

    save_piece('lullabies/mozart/mozart_ave_verum_corpus_k618.mid',
               'Mozart - Ave Verum Corpus K.618', 52, 4, 4, 'D', rh, lh)


# ═══════════════════════════════════════════════════
#  8. Bach - Bist du bei mir BWV 508
#     (3/4, Eb major → simplified in Eb)
# ═══════════════════════════════════════════════════
def encode_bach_bist_du_bei_mir():
    rh = []
    lh = []

    # "Bist du bei mir, geh ich mit Freuden"
    # 3/4 time, gentle, stepwise melody

    # Pickup
    rh += [n('Bb4',Q,P)]
    lh += [rest(Q)]

    # "Bist du bei mir"
    rh += [n('Eb5',Q,MP), n('D5',Q,MP), n('C5',Q,MP)]
    lh += [n('Eb3',Q,PP), n('G3',Q,PP), n('Bb3',Q,PP)]

    rh += [n('Bb4',DQ,MP), n('C5',E,P), n('D5',Q,P)]
    lh += [n('Eb3',Q,PP), n('G3',Q,PP), n('Bb3',Q,PP)]

    rh += [n('Eb5',Q,MP), n('D5',Q,MP), n('C5',Q,MP)]
    lh += [n('Ab2',Q,PP), n('C3',Q,PP), n('Eb3',Q,PP)]

    rh += [n('Bb4',DH,P)]
    lh += [n('Eb3',Q,PP), n('G3',Q,PP), n('Bb3',Q,PP)]

    # "geh ich mit Freuden"
    rh += [n('Bb4',Q,P), n('C5',Q,MP), n('D5',Q,MP)]
    lh += [n('Eb3',Q,PP), n('G3',Q,PP), n('Bb3',Q,PP)]

    rh += [n('Eb5',Q,MF), n('F5',Q,MF), n('D5',Q,MP)]
    lh += [n('Ab2',Q,PP), n('C3',Q,PP), n('F3',Q,PP)]

    rh += [n('C5',Q,MP), n('Bb4',Q,MP), n('Ab4',Q,P)]
    lh += [n('Bb2',Q,PP), n('D3',Q,PP), n('F3',Q,PP)]

    rh += [n('Bb4',DH,P)]
    lh += [n('Eb3',Q,PP), n('G3',Q,PP), n('Bb3',Q,PP)]

    # Middle section: "zum Sterben und zu meiner Ruh"
    rh += [n('Bb4',Q,P), n('Eb5',Q,MF), n('D5',Q,MP)]
    lh += [n('G3',Q,PP), n('Bb3',Q,PP), n('Eb4',Q,PP)]

    rh += [n('C5',Q,MP), n('Bb4',Q,P), n('Ab4',Q,P)]
    lh += [n('Ab2',Q,PP), n('C3',Q,PP), n('Eb3',Q,PP)]

    rh += [n('G4',Q,P), n('Ab4',Q,P), n('Bb4',Q,MP)]
    lh += [n('Bb2',Q,PP), n('D3',Q,PP), n('F3',Q,PP)]

    rh += [n('Eb4',DH,P)]
    lh += [n('Eb3',DH,PP)]

    # Da capo return: "Bist du bei mir"
    rh += [n('Bb4',Q,P)]
    lh += [rest(Q)]

    rh += [n('Eb5',Q,MP), n('D5',Q,MP), n('C5',Q,MP)]
    lh += [n('Eb3',Q,PP), n('G3',Q,PP), n('Bb3',Q,PP)]

    rh += [n('Bb4',DQ,MP), n('C5',E,P), n('D5',Q,P)]
    lh += [n('Eb3',Q,PP), n('G3',Q,PP), n('Bb3',Q,PP)]

    rh += [n('Eb5',Q,MP), n('D5',Q,MP), n('C5',Q,MP)]
    lh += [n('Ab2',Q,PP), n('C3',Q,PP), n('Eb3',Q,PP)]

    rh += [n('Bb4',DH,P)]
    lh += [n('Eb3',DH,PP)]

    save_piece('lullabies/bach/bach_bist_du_bei_mir_bwv508.mid',
               'Bach - Bist du bei mir BWV 508', 72, 3, 4, 'Eb', rh, lh)


# ═══════════════════════════════════════════════════
#  9. Haydn - Serenade (String Quartet Op.3 No.5)
#     (Andante cantabile, 4/4, F major)
# ═══════════════════════════════════════════════════
def encode_haydn_serenade():
    rh = []
    lh = []

    # The famous "Haydn Serenade" — a sweet, singing violin melody
    # with pizzicato-like accompaniment. Simple and beautiful.

    # Accompaniment: simple repeated quarter notes (pizzicato style)
    def pizz(root, third, fifth):
        return [n(root,Q,PP), n(third,Q,PP), n(fifth,Q,PP), n(third,Q,PP)]

    # Opening melody
    rh += [n('C5',DQ,MP), n('D5',E,P), n('C5',Q,MP), n('A4',Q,P)]
    lh += pizz('F3','A3','C4')

    rh += [n('Bb4',DQ,MP), n('C5',E,P), n('Bb4',Q,MP), n('G4',Q,P)]
    lh += pizz('Bb2','D3','F3')

    rh += [n('A4',DQ,MP), n('Bb4',E,P), n('A4',Q,MP), n('F4',Q,P)]
    lh += pizz('F3','A3','C4')

    rh += [n('G4',H,P), n('F4',H,P)]
    lh += [n('C3',Q,PP), n('E3',Q,PP), n('F3',H,PP)]

    # Second phrase
    rh += [n('C5',DQ,MF), n('D5',E,MP), n('C5',Q,MF), n('A4',Q,MP)]
    lh += pizz('F3','A3','C4')

    rh += [n('Bb4',DQ,MF), n('C5',E,MP), n('Bb4',Q,MF), n('G4',Q,MP)]
    lh += pizz('Bb2','D3','F3')

    rh += [n('A4',Q,MF), n('C5',Q,F), n('Bb4',Q,MF), n('A4',Q,MP)]
    lh += pizz('F3','A3','C4')

    rh += [n('G4',H,MP), n('F4',H,P)]
    lh += [n('C3',Q,PP), n('E3',Q,PP), n('F3',H,PP)]

    # Gentle closing
    rh += [n('F4',Q,P), n('A4',Q,P), n('C5',Q,MP), n('A4',Q,P)]
    lh += pizz('F3','A3','C4')

    rh += [n('G4',H,P), n('F4',H,P)]
    lh += [n('C3',Q,PP), n('E3',Q,PP), n('F3',H,PP)]

    save_piece('lullabies/haydn/haydn_serenade_op3no5.mid',
               'Haydn - Serenade (String Quartet Op.3 No.5)', 66, 4, 4, 'F', rh, lh)


# ═══════════════════════════════════════════════════
#  MAIN
# ═══════════════════════════════════════════════════
if __name__ == '__main__':
    print("Encoding classical lullabies as MIDI...")
    print()

    encode_mozart_wiegenlied()
    encode_mozart_twinkle()
    encode_mozart_romanze()
    encode_mozart_ave_verum()
    encode_schubert_wiegenlied()
    encode_schubert_ave_maria()
    encode_chopin_berceuse()
    encode_bach_bist_du_bei_mir()
    encode_haydn_serenade()

    print()
    print("Done! 9 pieces encoded.")
