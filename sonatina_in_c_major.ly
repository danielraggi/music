\version "2.24.0"

\header {
  title = "Sonatina in C Major"
  subtitle = "Fur meine liebe Nichte"
  composer = "In the style of W.A. Mozart"
  tagline = "Generated with love and a little bit of code"
}

\paper {
  #(set-paper-size "a4")
}

global = {
  \key c \major
  \time 4/4
  \tempo "Allegretto grazioso" 4 = 108
}

right = \relative {
  \clef treble
  \global
  c''8 e''8 g''8 e''8 f''16 e''16 d''16 e''16 d''8 c''8   f''8 e''8 d''4 b'8 c''16 d''16 d''4   d''8 f''8 a''8 f''8 g''16 f''16 e''16 f''16 e''8 d''8   e''8 d''8 c''16 d''16 e''16 f''16 g''16 f''8 e''8 d''4   c''8 e''8 g''8 c'''8 d'''16 c'''16 b''16 c'''16 a''8 g''8   a''8 g''8 f''8 e''8 d''4 c''4   d''8 e''8 f''8 d''8 d''16 e''16 d''16 e''16 c''4   e''4 g''16 f''16 e''16 d''16 c''16 c''2   c''8 d''8 e''8 f''8 g''8 g''4 e''8 f''8   g''8 a''8 b''8 a''8 g''8 e''8 c''8 e''8   d''8 fis''8 a''8 fis''8 g''16 fis''16 e''16 d''16 d''4   fis''16 g''16 fis''16 g''16 g''8 a''8 b''8 a''8 g''4   g''8 b''8 d'''4 d'''16 c'''16 b''16 a''16 g''16 g''4   a''8 fis''8 g''4 r2   b'4. a'8 g'8 a'8 b'8 d''8   d''4. c''8 e''8 d''8 c''4   d''8 e''8 fis''8 g''8 a''4. g''8   fis''8 e''8 d''8 c''8 b'8 a'8 a'4   g''8 fis''8 e''8 d''8 e''16 d''16 c''16 d''16 b'4   c''4 e''8 d''8 cis''16 d''16 cis''16 d''16 d''4   d''8 e''8 fis''8 a''8 a''16 b''16 a''16 b''16 g''4   b''8 g''8 d''8 b'8 g'4 r4   g'16 a'16 b'16 c''16 d''16 d''16 e''16 fis''16 g''16 g''4 g''16 fis''16 e''16 d''16   d''8 e''8 fis''8 g''8 fis''16 g''16 fis''16 g''16 g''4   b'8 e''8 g''8 e''8 f''16 e''16 d''16 e''16 d''8 b'8   c''8 b'8 a'4 g'8 a'8 b'8 c''8   a'8 c''8 e''8 c''8 d''16 c''16 b'16 c''16 b'8 a'8   e''8 d''8 c''8 ais'8 a'4 d''4   d''8 f''8 e''8 d''8 b'8 d''8 f''8 d''8   d''16 e''16 f''16 g''16 g''16 f''16 e''16 d''16 d''16 e''16 f''16 g''16 a''16 a''16 g''16 f''16 e''16 d''16   e''4 f''8 d''8 e''4 f''8 d''8   b'16 c''16 b'16 c''16 b'16 c''16 b'16 c''16 d''16 e''16 d''16 e''16 d''4   c''8 e''8 g''8 e''8 f''16 e''16 d''16 e''16 d''8 c''8   f''16 e''4 d''4 b'8 c''16 d''16 d''4   d''8 f''8 a''8 f''8 g''16 f''16 e''16 f''16 e''8 d''8   e''8 d''8 c''16 d''16 e''16 f''16 g''16 f''8 e''8 d''4   c''8 e''8 g''8 c'''8 d'''16 c'''16 b''16 c'''16 a''8 g''8   a''8 g''8 f''8 e''8 d''4 c''4   d''8 e''8 f''8 d''8 d''16 e''16 d''16 e''16 c''4   e''4 g''16 f''16 e''16 d''16 c''16 c''2   c''8 d''8 e''8 f''8 g''8 g''4 e''8 f''8   g''8 a''8 b''8 c'''8 c'''16 b''16 a''16 g''16 g''4   e'4. d'8 c'8 d'8 e'8 g'8   g'4. f'8 a'8 g'8 f'4   g'8 a'8 b'8 c''8 d''4. c''8   b'8 a'8 g'8 f'8 e'8 d'8 d'4   c''8 b'8 a'8 g'8 a'16 g'16 f'16 g'16 e'4   f'4 a'8 g'8 fis'16 g'16 fis'16 g'16 g'4   g'8 a'8 b'8 d''8 d''16 e''16 d''16 e''16 c''4   e''8 c''8 g'8 e'8 c'4 r4   c''16 d''16 e''16 f''16 g''16 a''16 b''16 c'''16 c'''16 b''16 a''16 g''16 g''4   a''8 g''8 e''4 c''8 d''8 e''8 g''8   a''4 g''4 fis''16 g''16 fis''16 g''16 g''4   c''16 d''16 e''16 f''16 g''16 g''4 e''4 c''4   e''8 d''8 c''8 d''8 e''4 c''4   c''2 r2  
  \bar "|."
}

left = \relative {
  \clef bass
  \global
  c4 g4 c8 g8 e8 g8   g8 d'8 b8 d'8 g8 d'8 b8 d'8   f4 c'4 f8 c'8 a8 c'8   g8 d'8 b8 d'8 g8 d'8 b8 d'8   c4 e4 c8 g8 e8 g8   f8 c'8 a8 c'8 f8 c'8 a8 c'8   d8 a8 f8 a8 g4 c4   c4 g4 c2   c4 e4 g4 c'4   a8 e'8 c'8 e'8 a8 e'8 c'8 e'8   d4 fis4 a4 d4   d4 d4 d4 g4   g4 b4 d'4 g4   d4 g4 r2   g8 d'8 b8 d'8 g8 d'8 b8 d'8   g8 d'8 b8 d'8 c8 g8 e8 g8   g8 d'8 b8 d'8 g8 d'8 b8 d'8   d8 a8 fis8 a8 d8 a8 fis8 a8   g8 d'8 b8 d'8 g8 d'8 b8 d'8   c4 e4 a4 d4   d4 d'4 d4 g4   g4 d4 g4 r4   g8 d'8 b8 d'8 g8 d'8 b8 d'8   d4 d'4 d4 g4   e8 b8 g8 b8 e8 b8 g8 b8   e8 b8 g8 b8 a8 e'8 c'8 e'8   a8 e'8 c'8 e'8 a8 e'8 c'8 e'8   d8 a8 f8 a8 d8 a8 f8 a8   g4 g4 g4 g4   g4 b4 g4 f4   g4 g4 g4 g4   g4 g4 g4 g4   c4 g4 c8 g8 e8 g8   g8 d'8 b8 d'8 g8 d'8 b8 d'8   f4 c'4 f8 c'8 a8 c'8   g8 d'8 b8 d'8 g8 d'8 b8 d'8   c4 e4 c8 g8 e8 g8   f8 c'8 a8 c'8 f8 c'8 a8 c'8   d8 a8 f8 a8 g4 c4   c4 g4 c2   c4 e4 g4 c'4   g4 g4 g4 c4   c8 g8 e8 g8 c8 g8 e8 g8   c8 g8 e8 g8 f8 c'8 a8 c'8   c8 g8 e8 g8 c8 g8 e8 g8   g8 d'8 b8 d'8 g8 d'8 b8 d'8   c8 g8 e8 g8 c8 g8 e8 g8   f4 a4 d4 g4   g4 g4 g4 c4   c4 e4 c4 r4   c4 e4 g4 c'4   f4 c'4 c4 c4   d4 g4 g4 c4   c4 c4 c4 c4   c4 g4 e4 c4   c2 r2  
  \bar "|."
}

\score {
  \new PianoStaff <<
    \new Staff = "right" \right
    \new Staff = "left" \left
  >>
  \layout { }
  \midi { }
}
