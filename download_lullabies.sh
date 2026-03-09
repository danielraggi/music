#!/bin/sh
#
# Classical Lullabies MIDI Collection — Download Script
#
# Run this on a machine with internet access:
#   chmod +x download_lullabies.sh
#   ./download_lullabies.sh
#
# Sources: piano-midi.de, mfiles.co.uk, bitmidi.com, kunstderfuge.com, musescore.com
#
# Note: Some sources serve MIDI via page downloads rather than direct links.
#       For those, the script opens the page URL and you download manually.
#       Direct-download links are attempted first with curl.

set -e

BASE_DIR="$(cd "$(dirname "$0")" && pwd)/lullabies"
for d in bach mozart vivaldi handel haydn beethoven brahms schubert schumann chopin; do
    mkdir -p "$BASE_DIR/$d"
done

MANUAL_FILE=$(mktemp)
trap 'rm -f "$MANUAL_FILE"' EXIT

download_midi() {
    url="$1"
    dest="$2"
    desc="$3"

    if [ -f "$dest" ]; then
        echo "  [SKIP] Already exists: $(basename "$dest")"
        return 0
    fi

    echo "  [GET]  $desc"
    if curl -sL --fail --connect-timeout 10 -o "$dest" "$url" 2>/dev/null; then
        # Verify it's actually a MIDI file (starts with MThd)
        if head -c 4 "$dest" 2>/dev/null | grep -q "MThd"; then
            size=$(wc -c < "$dest")
            echo "         OK ($(( size / 1024 ))KB)"
            return 0
        else
            echo "         Not a valid MIDI file, removing"
            rm -f "$dest"
            echo "$desc -> $url" >> "$MANUAL_FILE"
        fi
    else
        echo "         Download failed"
        echo "$desc -> $url" >> "$MANUAL_FILE"
    fi
}

echo "=============================================="
echo "  Classical Lullabies MIDI Collection"
echo "=============================================="
echo ""

# ─────────────────────────────────────────
#  BACH
# ─────────────────────────────────────────
echo "=== BACH ==="

# piano-midi.de has direct .mid links with a known URL pattern
download_midi "http://piano-midi.de/midis/bach/bach_846.mid" \
    "$BASE_DIR/bach/bach_prelude_c_bwv846.mid" \
    "Bach - Prelude in C Major BWV 846"

download_midi "http://piano-midi.de/midis/bach/bach_air.mid" \
    "$BASE_DIR/bach/bach_air_on_g_string_bwv1068.mid" \
    "Bach - Air on the G String BWV 1068"

# These may need manual download from kunstderfuge or musescore
download_midi "https://www.kunstderfuge.com/-/midi/bach/bwv508.mid" \
    "$BASE_DIR/bach/bach_bist_du_bei_mir_bwv508.mid" \
    "Bach - Bist du bei mir BWV 508"

download_midi "https://www.kunstderfuge.com/-/midi/bach/bwv1007_1.mid" \
    "$BASE_DIR/bach/bach_cello_suite1_prelude_bwv1007.mid" \
    "Bach - Cello Suite No.1 Prelude BWV 1007"

download_midi "https://www.kunstderfuge.com/-/midi/bach/bwv1031_2.mid" \
    "$BASE_DIR/bach/bach_siciliano_bwv1031.mid" \
    "Bach - Siciliano from Flute Sonata BWV 1031"

download_midi "https://www.kunstderfuge.com/-/midi/bach/bwv147.mid" \
    "$BASE_DIR/bach/bach_jesu_joy_bwv147.mid" \
    "Bach - Jesu Joy of Man's Desiring BWV 147"

download_midi "https://www.kunstderfuge.com/-/midi/bach/bwv208_9.mid" \
    "$BASE_DIR/bach/bach_sheep_may_safely_graze_bwv208.mid" \
    "Bach - Sheep May Safely Graze BWV 208"

echo ""

# ─────────────────────────────────────────
#  MOZART
# ─────────────────────────────────────────
echo "=== MOZART ==="

download_midi "http://piano-midi.de/midis/mozart/mozart_k265.mid" \
    "$BASE_DIR/mozart/mozart_twinkle_variations_k265.mid" \
    "Mozart - Ah vous dirai-je Maman (Twinkle) K.265"

download_midi "http://piano-midi.de/midis/mozart/mozart_k545_2.mid" \
    "$BASE_DIR/mozart/mozart_sonata_k545_andante.mid" \
    "Mozart - Piano Sonata K.545 2nd mvt (Andante)"

download_midi "http://piano-midi.de/midis/mozart/mozart_k331_1.mid" \
    "$BASE_DIR/mozart/mozart_sonata_k331_theme.mid" \
    "Mozart - Piano Sonata K.331 Andante grazioso"

download_midi "http://piano-midi.de/midis/mozart/mozart_k545_1.mid" \
    "$BASE_DIR/mozart/mozart_sonata_k545_allegro.mid" \
    "Mozart - Piano Sonata K.545 1st mvt (Allegro)"

# These are vocal/orchestral — try kunstderfuge
download_midi "https://www.kunstderfuge.com/-/midi/mozart/k350.mid" \
    "$BASE_DIR/mozart/mozart_wiegenlied_k350.mid" \
    "Mozart - Wiegenlied (Lullaby) K.350"

download_midi "https://www.kunstderfuge.com/-/midi/mozart/k525_2.mid" \
    "$BASE_DIR/mozart/mozart_eine_kleine_romanze_k525.mid" \
    "Mozart - Eine kleine Nachtmusik, Romanze K.525"

download_midi "https://www.kunstderfuge.com/-/midi/mozart/k618.mid" \
    "$BASE_DIR/mozart/mozart_ave_verum_corpus_k618.mid" \
    "Mozart - Ave Verum Corpus K.618"

download_midi "https://www.kunstderfuge.com/-/midi/mozart/k626_lacrimosa.mid" \
    "$BASE_DIR/mozart/mozart_lacrimosa_k626.mid" \
    "Mozart - Lacrimosa from Requiem K.626"

echo ""

# ─────────────────────────────────────────
#  VIVALDI
# ─────────────────────────────────────────
echo "=== VIVALDI ==="

download_midi "https://www.kunstderfuge.com/-/midi/vivaldi/rv297_2.mid" \
    "$BASE_DIR/vivaldi/vivaldi_winter_largo_rv297.mid" \
    "Vivaldi - Winter Largo (Four Seasons) RV 297"

echo ""

# ─────────────────────────────────────────
#  HANDEL
# ─────────────────────────────────────────
echo "=== HANDEL ==="

download_midi "https://www.mfiles.co.uk/midi/handels-largo-piano.mid" \
    "$BASE_DIR/handel/handel_largo_xerxes_ombra_mai_fu.mid" \
    "Handel - Largo from Xerxes (Ombra mai fu)"

echo ""

# ─────────────────────────────────────────
#  HAYDN
# ─────────────────────────────────────────
echo "=== HAYDN ==="

download_midi "https://www.kunstderfuge.com/-/midi/haydn/op3n5_2.mid" \
    "$BASE_DIR/haydn/haydn_serenade_op3no5.mid" \
    "Haydn - Serenade (String Quartet Op.3 No.5)"

echo ""

# ─────────────────────────────────────────
#  BEETHOVEN
# ─────────────────────────────────────────
echo "=== BEETHOVEN ==="

download_midi "http://piano-midi.de/midis/beethoven/sonata14_1.mid" \
    "$BASE_DIR/beethoven/beethoven_moonlight_sonata_mvt1.mid" \
    "Beethoven - Moonlight Sonata 1st mvt"

download_midi "http://piano-midi.de/midis/beethoven/elise.mid" \
    "$BASE_DIR/beethoven/beethoven_fur_elise.mid" \
    "Beethoven - Fur Elise"

download_midi "http://piano-midi.de/midis/beethoven/sonata8_2.mid" \
    "$BASE_DIR/beethoven/beethoven_pathetique_adagio.mid" \
    "Beethoven - Pathetique Sonata, Adagio cantabile"

echo ""

# ─────────────────────────────────────────
#  BRAHMS
# ─────────────────────────────────────────
echo "=== BRAHMS ==="

download_midi "https://www.mfiles.co.uk/midi/brahms-lullaby-wiegenlied.mid" \
    "$BASE_DIR/brahms/brahms_wiegenlied_op49no4.mid" \
    "Brahms - Wiegenlied (Lullaby) Op.49 No.4"

download_midi "http://piano-midi.de/midis/brahms/brahms_op117_1.mid" \
    "$BASE_DIR/brahms/brahms_intermezzo_op117no1.mid" \
    "Brahms - Intermezzo Op.117 No.1 (Schlaf sanft mein Kind)"

echo ""

# ─────────────────────────────────────────
#  SCHUBERT
# ─────────────────────────────────────────
echo "=== SCHUBERT ==="

download_midi "http://piano-midi.de/midis/schubert/schubert_d498.mid" \
    "$BASE_DIR/schubert/schubert_wiegenlied_d498.mid" \
    "Schubert - Wiegenlied D.498"

download_midi "http://piano-midi.de/midis/schubert/schubert_d839.mid" \
    "$BASE_DIR/schubert/schubert_ave_maria_d839.mid" \
    "Schubert - Ave Maria D.839"

download_midi "http://piano-midi.de/midis/schubert/schubert_d957_4.mid" \
    "$BASE_DIR/schubert/schubert_standchen_serenade_d957.mid" \
    "Schubert - Standchen (Serenade) D.957"

echo ""

# ─────────────────────────────────────────
#  SCHUMANN
# ─────────────────────────────────────────
echo "=== SCHUMANN ==="

download_midi "http://piano-midi.de/midis/schumann/schumann_kinderszenen_7.mid" \
    "$BASE_DIR/schumann/schumann_traumerei_kinderszenen.mid" \
    "Schumann - Traumerei (Kinderszenen No.7)"

download_midi "http://piano-midi.de/midis/schumann/schumann_kinderszenen.mid" \
    "$BASE_DIR/schumann/schumann_kinderszenen_complete.mid" \
    "Schumann - Kinderszenen (complete)"

echo ""

# ─────────────────────────────────────────
#  CHOPIN
# ─────────────────────────────────────────
echo "=== CHOPIN ==="

download_midi "http://piano-midi.de/midis/chopin/chopin_op57.mid" \
    "$BASE_DIR/chopin/chopin_berceuse_op57.mid" \
    "Chopin - Berceuse Op.57"

download_midi "http://piano-midi.de/midis/chopin/chopin_op9_2.mid" \
    "$BASE_DIR/chopin/chopin_nocturne_op9no2.mid" \
    "Chopin - Nocturne Op.9 No.2"

download_midi "http://piano-midi.de/midis/chopin/chopin_op27_2.mid" \
    "$BASE_DIR/chopin/chopin_nocturne_op27no2.mid" \
    "Chopin - Nocturne Op.27 No.2"

echo ""

# ─────────────────────────────────────────
#  SUMMARY
# ─────────────────────────────────────────
echo "=============================================="
echo "  Download Summary"
echo "=============================================="

total=$(find "$BASE_DIR" -name "*.mid" -type f | wc -l)
echo "  Successfully downloaded: $total MIDI files"
echo ""

if [ -s "$MANUAL_FILE" ]; then
    echo "  The following need manual download:"
    echo ""
    while IFS= read -r item; do
        echo "    - $item"
    done < "$MANUAL_FILE"
    echo ""
    echo "  Manual download sources:"
    echo "    - https://www.kunstderfuge.com (browse by composer)"
    echo "    - https://musescore.com (search, then download MIDI)"
    echo "    - https://bitmidi.com (search by piece name)"
    echo "    - https://www.mfiles.co.uk/classical-midi.htm"
    echo "    - http://piano-midi.de (high-quality piano performances)"
fi

echo ""
echo "  Collection directory: $BASE_DIR"
echo "=============================================="

# List what we got
echo ""
echo "Files by composer:"
for composer in bach mozart vivaldi handel haydn beethoven brahms schubert schumann chopin; do
    count=$(find "$BASE_DIR/$composer" -name "*.mid" -type f 2>/dev/null | wc -l)
    if [ "$count" -gt 0 ]; then
        echo "  $composer/  ($count files)"
        find "$BASE_DIR/$composer" -name "*.mid" -type f -exec basename {} \; | sort | sed 's/^/    /'
    fi
done
