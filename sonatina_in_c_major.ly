\version "2.24.0"

\header {
  title = "Sonatina in C Major"
  subtitle = "Für meine liebe Nichte"
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
  e''8 d''8 c''4 e''4 g''4   f''4 e''4 d''2   e''8 f''8 g''4 a''4 g''4   g''4 f''8 e''8 d''2   c''8 d''8 e''4 g''4 c'''4   a''4 g''4 f''4 e''4   d''4 e''8 f''8 e''4 d''4   c''2 r2   g''4 e''8 f''8 g''4 a''4   b''4 a''4 g''4 fis''4   g''8 a''8 b''4 a''4 fis''4   g''2 r2   b'8 c''8 d''4 g''4 d''4   e''4 d''4 c''4 b'4   d''8 e''8 fis''4 a''4 fis''4   g''4 fis''8 e''8 d''2   b''4 a''8 g''8 a''4 fis''4   e''4 g''4 fis''4 e''4   d''8 e''8 fis''8 g''8 a''4 fis''4   g''2 r2   g''4 fis''8 e''8 d''4 b'4   e''4 d''4 c''4 b'4   c''8 d''8 e''4 a''4 e''4   f''4 e''4 d''4 c''4   b'8 c''8 d''4 g''4 f''4   e''4 f''8 e''8 d''4 b'4   c''4 d''4 e''4 f''4   g''4 f''8 e''8 d''2   e''8 d''8 c''4 e''4 g''4   f''4 e''4 d''2   e''8 f''8 g''4 a''4 g''4   g''4 f''8 e''8 d''2   c''8 d''8 e''4 g''4 c'''4   a''4 g''4 f''4 e''4   d''4 e''8 f''8 e''4 d''4   c''2 r2   g''4 e''8 f''8 g''4 a''4   a''4 g''4 f''4 e''4   f''8 g''8 a''4 g''4 e''4   d''2 r2   e'8 f'8 g'4 c''4 g'4   a'4 g'4 f'4 e'4   g'8 a'8 b'4 d''4 b'4   c''4 b'8 a'8 g'2   e''4 d''8 c''8 d''4 b'4   a'4 c''4 b'4 a'4   g'8 a'8 b'8 c''8 d''4 b'4   c''2 r2   e''4 c''4 e''4 g''4   a''4 f''4 g''4 d''4   e''8 d''8 c''8 d''8 e''4 g''4   c''2 r2  
  \bar "|."
}

left = \relative {
  \clef bass
  \global
  c8 g8 e8 g8 c8 g8 e8 g8   g8 d'8 b8 d'8 g8 d'8 b8 d'8   f8 c'8 a8 c'8 f8 c'8 a8 c'8   g8 d'8 b8 d'8 g8 d'8 b8 d'8   c8 g8 e8 g8 c8 g8 e8 g8   f8 c'8 a8 c'8 f8 c'8 a8 c'8   d8 a8 f8 a8 g8 d'8 b8 d'8   c4 e4 g4 c'4   c8 g8 e8 g8 c8 g8 e8 g8   a8 e'8 c'8 e'8 d8 a8 fis8 a8   d8 a8 fis8 a8 d8 a8 fis8 a8   g4 b4 d'4 r4   g8 d'8 b8 d'8 g8 d'8 b8 d'8   c8 g8 e8 g8 c8 g8 e8 g8   g8 d'8 b8 d'8 g8 d'8 b8 d'8   d8 a8 fis8 a8 d8 a8 fis8 a8   g8 d'8 b8 d'8 g8 d'8 b8 d'8   c8 g8 e8 g8 c8 g8 e8 g8   d8 a8 fis8 a8 d8 a8 fis8 a8   g4 b4 d'4 r4   g8 d'8 b8 d'8 e8 b8 g8 b8   e8 b8 g8 b8 e8 b8 g8 b8   a8 e'8 c'8 e'8 a8 e'8 c'8 e'8   d8 a8 f8 a8 d8 a8 f8 a8   g8 d'8 b8 d'8 g8 d'8 b8 d'8   g8 f'8 b8 f'8 g8 f'8 b8 f'8   g4 g4 g4 g4   g4 g4 g2   c8 g8 e8 g8 c8 g8 e8 g8   g8 d'8 b8 d'8 g8 d'8 b8 d'8   f8 c'8 a8 c'8 f8 c'8 a8 c'8   g8 d'8 b8 d'8 g8 d'8 b8 d'8   c8 g8 e8 g8 c8 g8 e8 g8   f8 c'8 a8 c'8 f8 c'8 a8 c'8   d8 a8 f8 a8 g8 d'8 b8 d'8   c4 e4 g4 c'4   c8 g8 e8 g8 c8 g8 e8 g8   f8 c'8 a8 c'8 f8 c'8 a8 c'8   d8 a8 f8 a8 g8 d'8 b8 d'8   g4 b4 d'4 r4   c8 g8 e8 g8 c8 g8 e8 g8   f8 c'8 a8 c'8 f8 c'8 a8 c'8   c8 g8 e8 g8 c8 g8 e8 g8   g8 d'8 b8 d'8 g8 d'8 b8 d'8   c8 g8 e8 g8 c8 g8 e8 g8   f8 c'8 a8 c'8 f8 c'8 a8 c'8   g8 d'8 b8 d'8 g8 d'8 b8 d'8   c4 e4 g4 r4   c4 e4 g4 c'4   f4 a4 g4 b4   c8 g8 e8 g8 c8 g8 e8 g8   c2 r2  
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
