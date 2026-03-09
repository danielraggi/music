#!/bin/sh
#
# Classical Lullabies MIDI Collection — Download Script
#
# Run this on a machine with internet access:
#   chmod +x download_lullabies.sh
#   ./download_lullabies.sh
#
# This script scrapes real .mid URLs from source pages rather than
# guessing URL patterns. It uses piano-midi.de, mfiles.co.uk, and
# bitmidi.com as primary sources.

set -e

BASE_DIR="$(cd "$(dirname "$0")" && pwd)/lullabies"
for d in bach mozart vivaldi handel haydn beethoven brahms schubert schumann chopin; do
    mkdir -p "$BASE_DIR/$d"
done

MANUAL_FILE=$(mktemp)
trap 'rm -f "$MANUAL_FILE"' EXIT

SUCCESS=0
FAIL=0

# Download a .mid file directly, verifying the MThd header
download_direct() {
    url="$1"
    dest="$2"
    desc="$3"

    if [ -f "$dest" ]; then
        echo "  [SKIP] Already exists: $(basename "$dest")"
        SUCCESS=$((SUCCESS + 1))
        return 0
    fi

    echo "  [GET]  $desc"
    if curl -sL --fail --connect-timeout 10 -o "$dest" "$url" 2>/dev/null; then
        if head -c 4 "$dest" 2>/dev/null | grep -q "MThd"; then
            size=$(wc -c < "$dest")
            echo "         OK ($(( size / 1024 ))KB)"
            SUCCESS=$((SUCCESS + 1))
            return 0
        else
            rm -f "$dest"
        fi
    fi
    rm -f "$dest"
    return 1
}

# Scrape a page for .mid links matching a grep pattern, download first match
scrape_and_download() {
    page_url="$1"
    pattern="$2"
    dest="$3"
    desc="$4"
    base_url="$5"

    if [ -f "$dest" ]; then
        echo "  [SKIP] Already exists: $(basename "$dest")"
        SUCCESS=$((SUCCESS + 1))
        return 0
    fi

    echo "  [FIND] $desc"
    echo "         Scraping $page_url ..."

    page=$(curl -sL --fail --connect-timeout 10 "$page_url" 2>/dev/null) || {
        echo "         Page fetch failed"
        echo "$desc -> $page_url" >> "$MANUAL_FILE"
        FAIL=$((FAIL + 1))
        return 0
    }

    # Extract .mid URLs matching the pattern
    mid_url=$(echo "$page" | grep -oiE "(href|src)=\"[^\"]*\.mid\"" | grep -oiE "\"[^\"]*\.mid\"" | tr -d '"' | grep -i "$pattern" | head -1)

    if [ -z "$mid_url" ]; then
        echo "         No .mid link matching '$pattern' found on page"
        echo "$desc -> $page_url (search for: $pattern)" >> "$MANUAL_FILE"
        FAIL=$((FAIL + 1))
        return 0
    fi

    # Make relative URLs absolute
    case "$mid_url" in
        http*) full_url="$mid_url" ;;
        /*)    full_url="$base_url$mid_url" ;;
        *)     full_url="$base_url/$mid_url" ;;
    esac

    echo "         Found: $full_url"
    if download_direct "$full_url" "$dest" "$desc"; then
        return 0
    else
        echo "         Download/validation failed"
        echo "$desc -> $full_url" >> "$MANUAL_FILE"
        FAIL=$((FAIL + 1))
        return 0
    fi
}

# Scrape piano-midi.de composer page for a piece
piano_midi_de() {
    composer_page="$1"
    pattern="$2"
    dest="$3"
    desc="$4"
    scrape_and_download "http://piano-midi.de/$composer_page" "$pattern" "$dest" "$desc" "http://piano-midi.de"
}

# Scrape mfiles.co.uk score page
mfiles() {
    score_page="$1"
    pattern="$2"
    dest="$3"
    desc="$4"
    scrape_and_download "https://www.mfiles.co.uk/scores/$score_page" "$pattern" "$dest" "$desc" "https://www.mfiles.co.uk"
}

# Scrape bitmidi.com piece page
bitmidi() {
    piece_slug="$1"
    dest="$2"
    desc="$3"
    scrape_and_download "https://bitmidi.com/$piece_slug" "\.mid" "$dest" "$desc" "https://bitmidi.com"
}

echo "=============================================="
echo "  Classical Lullabies MIDI Collection"
echo "=============================================="
echo ""
echo "Scraping source pages to find real download URLs..."
echo ""

# ─────────────────────────────────────────
#  BACH
# ─────────────────────────────────────────
echo "=== BACH ==="

piano_midi_de "bach.htm" "846" \
    "$BASE_DIR/bach/bach_prelude_c_bwv846.mid" \
    "Bach - Prelude in C Major BWV 846"

piano_midi_de "bach.htm" "air" \
    "$BASE_DIR/bach/bach_air_on_g_string_bwv1068.mid" \
    "Bach - Air on the G String BWV 1068"

mfiles "bist-du-bei-mir.htm" "\.mid" \
    "$BASE_DIR/bach/bach_bist_du_bei_mir_bwv508.mid" \
    "Bach - Bist du bei mir BWV 508"

bitmidi "bach-cello-suite-no-1-prelude-mid" \
    "$BASE_DIR/bach/bach_cello_suite1_prelude_bwv1007.mid" \
    "Bach - Cello Suite No.1 Prelude BWV 1007"

mfiles "bach-siciliano.htm" "\.mid" \
    "$BASE_DIR/bach/bach_siciliano_bwv1031.mid" \
    "Bach - Siciliano from Flute Sonata BWV 1031"

mfiles "jesu-joy-of-mans-desiring.htm" "\.mid" \
    "$BASE_DIR/bach/bach_jesu_joy_bwv147.mid" \
    "Bach - Jesu Joy of Man's Desiring BWV 147"

mfiles "sheep-may-safely-graze.htm" "\.mid" \
    "$BASE_DIR/bach/bach_sheep_may_safely_graze_bwv208.mid" \
    "Bach - Sheep May Safely Graze BWV 208"

echo ""

# ─────────────────────────────────────────
#  MOZART
# ─────────────────────────────────────────
echo "=== MOZART ==="

piano_midi_de "mozart.htm" "k265\|ah.vous" \
    "$BASE_DIR/mozart/mozart_twinkle_variations_k265.mid" \
    "Mozart - Ah vous dirai-je Maman (Twinkle) K.265"

piano_midi_de "mozart.htm" "k545.*2\|545_2\|545.*andante" \
    "$BASE_DIR/mozart/mozart_sonata_k545_andante.mid" \
    "Mozart - Piano Sonata K.545 2nd mvt (Andante)"

piano_midi_de "mozart.htm" "k331.*1\|331_1\|331.*andante" \
    "$BASE_DIR/mozart/mozart_sonata_k331_theme.mid" \
    "Mozart - Piano Sonata K.331 Andante grazioso"

piano_midi_de "mozart.htm" "k545.*1\|545_1\|545.*allegro" \
    "$BASE_DIR/mozart/mozart_sonata_k545_allegro.mid" \
    "Mozart - Piano Sonata K.545 1st mvt (Allegro)"

mfiles "mozart-lullaby-wiegenlied.htm" "\.mid" \
    "$BASE_DIR/mozart/mozart_wiegenlied_k350.mid" \
    "Mozart - Wiegenlied (Lullaby) K.350"

mfiles "eine-kleine-nachtmusik-romanze.htm" "\.mid" \
    "$BASE_DIR/mozart/mozart_eine_kleine_romanze_k525.mid" \
    "Mozart - Eine kleine Nachtmusik, Romanze K.525"

mfiles "ave-verum-corpus.htm" "\.mid" \
    "$BASE_DIR/mozart/mozart_ave_verum_corpus_k618.mid" \
    "Mozart - Ave Verum Corpus K.618"

bitmidi "mozart-lacrimosa-mid" \
    "$BASE_DIR/mozart/mozart_lacrimosa_k626.mid" \
    "Mozart - Lacrimosa from Requiem K.626"

echo ""

# ─────────────────────────────────────────
#  VIVALDI
# ─────────────────────────────────────────
echo "=== VIVALDI ==="

mfiles "vivaldi-winter-largo.htm" "\.mid" \
    "$BASE_DIR/vivaldi/vivaldi_winter_largo_rv297.mid" \
    "Vivaldi - Winter Largo (Four Seasons) RV 297"

bitmidi "the-four-seasons-op8-no-4-rv297-winter-2nd-movement-largo-vivaldi-mid" \
    "$BASE_DIR/vivaldi/vivaldi_winter_largo_rv297_alt.mid" \
    "Vivaldi - Winter Largo (alt source)"

echo ""

# ─────────────────────────────────────────
#  HANDEL
# ─────────────────────────────────────────
echo "=== HANDEL ==="

mfiles "handels-largo-piano.htm" "\.mid" \
    "$BASE_DIR/handel/handel_largo_xerxes_ombra_mai_fu.mid" \
    "Handel - Largo from Xerxes (Ombra mai fu)"

echo ""

# ─────────────────────────────────────────
#  HAYDN
# ─────────────────────────────────────────
echo "=== HAYDN ==="

mfiles "haydn-serenade.htm" "\.mid" \
    "$BASE_DIR/haydn/haydn_serenade_op3no5.mid" \
    "Haydn - Serenade (String Quartet Op.3 No.5)"

echo ""

# ─────────────────────────────────────────
#  BEETHOVEN
# ─────────────────────────────────────────
echo "=== BEETHOVEN ==="

piano_midi_de "beeth.htm" "sonata14.*1\|pathet\|moonlight" \
    "$BASE_DIR/beethoven/beethoven_moonlight_sonata_mvt1.mid" \
    "Beethoven - Moonlight Sonata 1st mvt"

piano_midi_de "beeth.htm" "elise" \
    "$BASE_DIR/beethoven/beethoven_fur_elise.mid" \
    "Beethoven - Fur Elise"

piano_midi_de "beeth.htm" "sonata8.*2\|pathet.*2" \
    "$BASE_DIR/beethoven/beethoven_pathetique_adagio.mid" \
    "Beethoven - Pathetique Sonata, Adagio cantabile"

mfiles "moonlight-movement1.htm" "\.mid" \
    "$BASE_DIR/beethoven/beethoven_moonlight_sonata_mvt1_alt.mid" \
    "Beethoven - Moonlight Sonata (mfiles alt)"

echo ""

# ─────────────────────────────────────────
#  BRAHMS
# ─────────────────────────────────────────
echo "=== BRAHMS ==="

mfiles "brahms-lullaby-wiegenlied.htm" "\.mid" \
    "$BASE_DIR/brahms/brahms_wiegenlied_op49no4.mid" \
    "Brahms - Wiegenlied (Lullaby) Op.49 No.4"

piano_midi_de "brahms.htm" "op117.*1\|117_1\|117.*1" \
    "$BASE_DIR/brahms/brahms_intermezzo_op117no1.mid" \
    "Brahms - Intermezzo Op.117 No.1 (Schlaf sanft mein Kind)"

bitmidi "brahms-lullaby-wiegenlied-piano-mid" \
    "$BASE_DIR/brahms/brahms_wiegenlied_op49no4_alt.mid" \
    "Brahms - Wiegenlied (bitmidi alt)"

echo ""

# ─────────────────────────────────────────
#  SCHUBERT
# ─────────────────────────────────────────
echo "=== SCHUBERT ==="

mfiles "schubert-wiegenlied.htm" "\.mid" \
    "$BASE_DIR/schubert/schubert_wiegenlied_d498.mid" \
    "Schubert - Wiegenlied D.498"

mfiles "ave-maria-schubert.htm" "\.mid" \
    "$BASE_DIR/schubert/schubert_ave_maria_d839.mid" \
    "Schubert - Ave Maria D.839"

piano_midi_de "schubert.htm" "d957.*4\|standchen\|serenade" \
    "$BASE_DIR/schubert/schubert_standchen_serenade_d957.mid" \
    "Schubert - Standchen (Serenade) D.957"

echo ""

# ─────────────────────────────────────────
#  SCHUMANN
# ─────────────────────────────────────────
echo "=== SCHUMANN ==="

piano_midi_de "schumann.htm" "kinderszenen.*7\|traumerei" \
    "$BASE_DIR/schumann/schumann_traumerei_kinderszenen.mid" \
    "Schumann - Traumerei (Kinderszenen No.7)"

mfiles "reverie-traumerei.htm" "\.mid" \
    "$BASE_DIR/schumann/schumann_traumerei_mfiles.mid" \
    "Schumann - Traumerei (mfiles)"

bitmidi "schumann-traumerei-mid" \
    "$BASE_DIR/schumann/schumann_traumerei_bitmidi.mid" \
    "Schumann - Traumerei (bitmidi)"

echo ""

# ─────────────────────────────────────────
#  CHOPIN
# ─────────────────────────────────────────
echo "=== CHOPIN ==="

piano_midi_de "chopin.htm" "op57\|berceuse" \
    "$BASE_DIR/chopin/chopin_berceuse_op57.mid" \
    "Chopin - Berceuse Op.57"

piano_midi_de "chopin.htm" "op9.*2\|nocturne.*9.*2" \
    "$BASE_DIR/chopin/chopin_nocturne_op9no2.mid" \
    "Chopin - Nocturne Op.9 No.2"

piano_midi_de "chopin.htm" "op27.*2\|nocturne.*27.*2" \
    "$BASE_DIR/chopin/chopin_nocturne_op27no2.mid" \
    "Chopin - Nocturne Op.27 No.2"

mfiles "chopin-nocturne-op9-no2.htm" "\.mid" \
    "$BASE_DIR/chopin/chopin_nocturne_op9no2_alt.mid" \
    "Chopin - Nocturne Op.9 No.2 (mfiles)"

echo ""

# ─────────────────────────────────────────
#  SUMMARY
# ─────────────────────────────────────────
echo "=============================================="
echo "  Download Summary"
echo "=============================================="

total=$(find "$BASE_DIR" -name "*.mid" -type f | wc -l)
echo "  Successfully downloaded: $total MIDI files"
echo "  Failed: $FAIL"
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
