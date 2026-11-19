"""Build the curated CSV lexicon of Biblical Hebrew locative verbs from
Doron & Dubnov (2017), 'The locative alternation in Biblical (and Modern) Hebrew'.

Sources inside DoronDubnov_revised.pdf:
- Causative (Hif'il) lists: Section 4.1, p. 13 (38 A, 7 A/B, 3 B)
- Intensive (Pi'el) lists: Section 6.1, pp. 22-23 (12 A, 7 A/B, 15 B)
- Simple (Pa'al) lists: Footnote 33, p. 23 (45 [46 printed incl. אסר] A, 31 A/B, 19 B)
- Path-ambiguous verbs: Table 1, p. 11 & Section 6.2, p. 26
- Locatum-incorporating B verbs: Section 6.2, pp. 25-26

Outputs:
- data/curated/doron_dubnov_177_verbs.csv
"""

from __future__ import annotations

import csv
from pathlib import Path

OUT_PATH = Path("data/curated/doron_dubnov_177_verbs.csv")

# Tuple schema:
# (lemma_bh_unvoc, lemma_bh_voc, mh_lemmas, gloss, paper_class, template, direction, notes)
VERBS: list[tuple[str, str, str, str, str, str, str, str]] = [
    # =========================================================================
    # A VERBS — Causative (Hif'il): 38 verbs (Section 4.1, p. 13)
    # =========================================================================
    ("הרים", "הרים", "הרים", "raise", "A", "Causative", "putting", ""),
    ("העלה", "העלה", "העלה", "bring up", "A", "Causative", "both", "Table 1 path verb; Table 3"),
    ("הוריד", "הוריד", "הוריד", "bring down", "A", "Causative", "both", "Table 1 path verb; Table 3"),
    ("הביא", "הביא", "הביא", "bring in", "A", "Causative", "both", "Table 1 path verb; Ex (20)"),
    ("הגיש", "הגיש", "הגיש", "bring", "A", "Causative", "putting", "Table 3"),
    ("הטיל", "הטיל", "הטיל", "cast", "A", "Causative", "both", "Table 1 path verb"),
    ("הקים", "הקים", "הקים", "raise", "A", "Causative", "putting", ""),
    ("הניח", "הניח", "הניח", "let rest/let stay", "A", "Causative", "putting", "Table 3"),
    ("השאיר", "השאיר", "השאיר", "let remain", "A", "Causative", "putting", "Table 3"),
    ("הפיץ", "הפיץ", "הפיץ", "scatter", "A", "Causative", "both", "Table 1 path verb; Table 3"),
    ("העמיד", "העמיד", "העמיד", "station", "A", "Causative", "putting", "Table 3"),
    ("הציב", "הציב", "הציב", "position", "A", "Causative", "putting", "Table 3"),
    ("הציג", "הציג", "הציג", "set", "A", "Causative", "putting", ""),
    ("הטביע", "הטביע", "הטביע", "sink", "A", "Causative", "putting", "Table 3"),
    ("הושיב", "הושיב", "הושיב", "seat", "A", "Causative", "putting", "fn 17"),
    ("השכיב", "השכיב", "השכיב", "lay", "A", "Causative", "putting", "fn 17"),
    ("הדביק", "הדביק", "הדביק", "cling/join", "A", "Causative", "putting", "Table 3"),
    ("החביא", "החביא", "החביא", "hide", "A", "Causative", "putting", ""),
    ("הסתיר", "הסתיר", "הסתיר", "hide", "A", "Causative", "putting", ""),
    ("הליט", "הליט", "הליט", "cover", "A", "Causative", "putting", ""),
    ("הניס", "הניס", "הניס", "chase", "A", "Causative", "removal", ""),
    ("האביד", "האביד", "האביד", "make extinct", "A", "Causative", "removal", "Table 3"),
    ("הבדיל", "הבדיל", "הבדיל", "separate", "A", "Causative", "removal", "Table 3"),
    ("החסיר", "החסיר", "החסיר", "omit", "A", "Causative", "removal", "Table 3"),
    ("העביר", "העביר", "העביר", "pass/take out", "A", "Causative", "both", "Table 1 path verb; Table 3"),
    ("המיש", "המיש", "המיש", "move away", "A", "Causative", "removal", "Table 3"),
    ("העתיק", "העתיק", "העתיק", "move away", "A", "Causative", "removal", "Table 3"),
    ("הגלה", "הגלה", "הגלה", "deport", "A", "Causative", "both", "Table 1 path verb; Table 3; Ex (6)"),
    ("השליך", "השליך", "השליך", "throw away", "A", "Causative", "both", "Table 1 path verb"),
    ("הדיח", "הדיח", "הדיח", "expel/drive away", "A", "Causative", "both", "Table 1 path verb; Table 3"),
    ("הוציא", "הוציא", "הוציא", "bring out", "A", "Causative", "both", "Table 1 path verb; Table 3"),
    ("הכרית", "הכרית", "הכרית", "cut off", "A", "Causative", "removal", ""),
    ("הרחיק", "הרחיק", "הרחיק", "remove", "A", "Causative", "removal", ""),
    ("הזיל", "הזיל", "הזיל", "drip", "A", "Causative", "removal", "Table 3"),
    ("הפיל", "הפיל", "הפיל", "make fall", "A", "Causative", "removal", "Table 3"),
    ("הטה", "הטה", "הטה", "divert", "A", "Causative", "both", "Table 1 path verb; Table 3"),
    ("הסב", "הסב", "הסב", "turn", "A", "Causative", "both", "Table 1 path verb"),
    ("הסיע", "הסיע", "הסיע", "bring/move away", "A", "Causative", "removal", "Table 3"),
    # =========================================================================
    # A VERBS — Intensive (Pi'el): 12 verbs (Section 6.1, p. 23)
    # =========================================================================
    ("ידה", "יִדָּה", "יידה|ידה", "cast/shoot", "A", "Intensive", "putting", ""),
    ("שכן", "שִׁכֵּן", "שיכן|שכן", "make dwell", "A", "Intensive", "putting", "fn 16"),
    ("קבץ", "קִבֵּץ", "קיבץ|קבץ", "collect", "A", "Intensive", "both", "Table 1 path verb"),
    ("פזר", "פִּזֵּר", "פיזר|פזר", "scatter", "A", "Intensive", "putting", ""),
    ("זרה", "זֵרָה", "זרה", "disperse", "A", "Intensive", "putting", "Ex (1)"),
    ("נתק", "נִתֵּק", "ניתק|נתק", "tear/disconnect", "A", "Intensive", "removal", ""),
    ("בלע", "בִּלַּע", "בילע|בלע", "swallow/destroy", "A", "Intensive", "removal", ""),
    ("מלט", "מִלֵּט", "מילט|מלט", "rescue", "A", "Intensive", "removal", ""),
    ("פלט", "פִּלֵּט", "פילט|פלט", "save", "A", "Intensive", "removal", ""),
    ("גרש", "גֵּרֵשׁ", "גירש|גרש", "drive out", "A", "Intensive", "removal", "Ex (2)"),
    ("חלץ", "חִלֵּץ", "חילץ|חלץ", "rescue", "A", "Intensive", "removal", ""),
    ("נשל", "נִשֵּׁל", "נישל|נשל", "dislodge", "A", "Intensive", "removal", "fn 16, fn 34, fn 39 (alternates in MH)"),
    # =========================================================================
    # A VERBS — Simple (Pa'al): 45 stated / 46 printed incl. אסר (fn 33, p. 23)
    # =========================================================================
    ("אסר", "אסר", "אסר", "bind/harness", "A", "Simple", "putting", "Paper erratum: printed in fn 33 A-Simple (making 46 vs 45 stated) AND in Ex (33) p.17 as A/B verb"),
    ("אצר", "אצר", "אצר", "gather/store up", "A", "Simple", "putting", ""),
    ("גלל", "גלל", "גלל", "roll", "A", "Simple", "putting", "fn 37 (manner verb)"),
    ("זרה", "זרה", "זרה", "blow off", "A", "Simple", "putting", "fn 7 (winnow)"),
    ("זרק", "זרק", "זרק", "toss/sprinkle", "A", "Simple", "both", "Table 1 path verb"),
    ("טבל", "טבל", "טבל", "dip", "A", "Simple", "putting", "fn 16"),
    ("טמן", "טמן", "טמן", "hide", "A", "Simple", "putting", ""),
    ("יצק", "יצק", "יצק", "pour", "A", "Simple", "putting", ""),
    ("לחץ", "לחץ", "לחץ", "push", "A", "Simple", "putting", ""),
    ("מרח", "מרח", "מרח", "spread", "A", "Simple", "putting", ""),
    ("נטע", "נטע", "נטע", "plant", "A", "Simple", "putting", ""),
    ("נטש", "נטש", "נטש", "abandon", "A", "Simple", "putting", ""),
    ("נפח", "נפח", "נפח", "blow", "A", "Simple", "putting", "Ex (3)"),
    ("נסך", "נסך", "נסך", "pour", "A", "Simple", "putting", ""),
    ("נתן", "נתן", "נתן", "put/give", "A", "Simple", "putting", "Ex (5)"),
    ("סחב", "סחב", "סחב", "drag", "A", "Simple", "putting", "fn 37 (manner verb)"),
    ("עזב", "עזב", "עזב", "leave", "A", "Simple", "putting", ""),
    ("פרש", "פרש", "פרש|פרס", "stretch out", "A", "Simple", "putting", ""),
    ("צפן", "צפן", "צפן", "hide", "A", "Simple", "putting", ""),
    ("צרר", "צרר", "צרר", "wrap", "A", "Simple", "putting", ""),
    ("קבר", "קבר", "קבר", "bury", "A", "Simple", "putting", ""),
    ("קרם", "קרם", "קרם", "cover with skin", "A", "Simple", "putting", "fn 16"),
    ("קשר", "קשר", "קשר", "tie", "A", "Simple", "putting", ""),
    ("שלח", "שלח", "שלח", "send", "A", "Simple", "putting", "Simple template; Intensive שִׁלַּח is A/B"),
    ("תלה", "תלה", "תלה", "hang", "A", "Simple", "putting", "printed 'hand' in fn 33 typo"),
    ("תקע", "תקע", "תקע", "drive in", "A", "Simple", "putting", ""),
    ("גנב", "גנב", "גנב", "steal", "A", "Simple", "removal", ""),
    ("גרע", "גרע", "גרע", "take/lessen", "A", "Simple", "removal", ""),
    ("דלה", "דלה", "דלה", "draw water", "A", "Simple", "removal", ""),
    ("הדף", "הדף", "הדף", "push", "A", "Simple", "removal", ""),
    ("חבל", "חבל", "חבל", "seize a pledge", "A", "Simple", "removal", ""),
    ("חלץ", "חלץ", "חלץ", "withdraw/bare", "A", "Simple", "removal", ""),
    ("כרת", "כרת", "כרת", "cut off", "A", "Simple", "removal", ""),
    ("לקח", "לקח", "לקח", "take", "A", "Simple", "removal", ""),
    ("לקט", "לקט", "לקט|ליקט", "gather", "A", "Simple", "removal", ""),
    ("מלק", "מלק", "מלק", "pinch off", "A", "Simple", "removal", ""),
    ("מצה", "מצה", "מצה|מיצה", "wring/drain", "A", "Simple", "both", "Table 1 path verb"),
    ("משה", "משה", "משה", "draw out", "A", "Simple", "removal", ""),
    ("נסח", "נסח", "נסח", "uproot", "A", "Simple", "removal", "fn 5"),
    ("נשא", "נשא", "נשא", "bring/carry", "A", "Simple", "removal", "Ex (69)"),
    ("פדה", "פדה", "פדה", "buy out/redeem", "A", "Simple", "removal", ""),
    ("קבץ", "קבץ", "קבץ", "collect", "A", "Simple", "both", "Table 1 path verb"),
    ("קטף", "קטף", "קטף", "collect/pluck", "A", "Simple", "removal", ""),
    ("שאב", "שאב", "שאב", "draw water", "A", "Simple", "removal", ""),
    ("שלף", "שלף", "שלף", "pull off", "A", "Simple", "removal", ""),
    ("שפך", "שפך", "שפך", "spill", "A", "Simple", "removal", ""),
    # =========================================================================
    # A/B VERBS — Causative (Hif'il): 7 verbs (Section 4.1, p. 13)
    # =========================================================================
    ("הלביש", "הלביש", "הלביש", "clothe", "A/B", "Causative", "putting", "Ex (29)"),
    ("הזה", "הזה", "היזה|הזה", "sprinkle", "A/B", "Causative", "putting", "Ex (30); MH Frame A only (§8.2)"),
    ("המטיר", "המטיר", "המטיר", "rain upon", "A/B", "Causative", "putting", "Ex (32)"),
    ("הסיר", "הסיר", "הסיר", "remove", "A/B", "Causative", "removal", "Ex (4),(35); MH Frame A only (§8.2)"),
    ("הפשיט", "הפשיט", "הפשיט", "strip", "A/B", "Causative", "removal", "Ex (52); alternates in MH (§8.2)"),
    ("הריק", "הריק", "הריק|רוקן", "empty", "A/B", "Causative", "removal", "Ex (51); MH counterpart רוקן alternates (§8.2)"),
    ("הקצה", "הקצה", "הקצה", "scrape off", "A/B", "Causative", "removal", "Ex (47)"),
    # =========================================================================
    # A/B VERBS — Intensive (Pi'el): 7 verbs (Section 6.1, p. 23)
    # =========================================================================
    ("מלא", "מִלֵּא", "מילא|מלא", "fill", "A/B", "Intensive", "putting", "Ex (10), fn 10, fn 13, fn 34; alternates in MH"),
    ("גלח", "גִּלַּח", "גילח|גלח", "shave", "A/B", "Intensive", "removal", "Ex (39)"),
    ("חטא", "חִטֵּא", "חיטא|חטא", "purify", "A/B", "Intensive", "removal", ""),
    ("נקה", "נִקָּה", "ניקה|נקה", "acquit/clean", "A/B", "Intensive", "removal", "Ex (46); alternates in MH (§8.2)"),
    ("כבס", "כִּבֵּס", "כיבס|כבס", "wash", "A/B", "Intensive", "removal", "Ex (45)"),
    ("פנה", "פִּנָּה", "פינה|פנה", "clear", "A/B", "Intensive", "removal", "Ex (34); alternates in MH (§8.2)"),
    ("שלח", "שִׁלַּח", "שילח|שלח", "send", "A/B", "Intensive", "both", "Ex (17),(31); Table 1 path verb"),
    # =========================================================================
    # A/B VERBS — Simple (Pa'al): 31 verbs (fn 33, p. 23)
    # =========================================================================
    ("אסף", "אסף", "אסף", "gather", "A/B", "Simple", "both", "Table 1 path verb; Ex (36); MH Frame A only (§8.2)"),
    ("זרע", "זרע", "זרע", "sow", "A/B", "Simple", "putting", "Ex (23); alternates in MH (§8.2)"),
    ("חבש", "חבש", "חבש", "wrap", "A/B", "Simple", "putting", ""),
    ("טח", "טח", "טח", "plaster", "A/B", "Simple", "putting", "Ex (24)"),
    ("ירה", "ירה", "ירה", "shoot", "A/B", "Simple", "putting", "Ex (26); MH Frame A only (§8.2)"),
    ("משח", "משח", "משח", "anoint", "A/B", "Simple", "putting", "Ex (25); alternates in MH (§8.2)"),
    ("סכך", "סכך", "סכך|סיכך", "thatch", "A/B", "Simple", "putting", "Ex (28)"),
    ("עמס", "עמס", "עמס|העמיס", "load", "A/B", "Simple", "putting", "Ex (27)"),
    ("רגם", "רגם", "רגם", "stone", "A/B", "Simple", "putting", "Ex (11)"),
    ("שם", "שם", "שם", "put", "A/B", "Simple", "putting", "Ex (5),(21),(22); MH Frame A only (§8.2)"),
    ("שת", "שת", "שת", "set", "A/B", "Simple", "putting", "fn 9"),
    ("ארה", "ארה", "ארה", "gather/pluck", "A/B", "Simple", "removal", ""),
    ("בזז", "בזז", "בזז", "plunder", "A/B", "Simple", "removal", "Ex (48); alternates in MH (§8.2)"),
    ("בצר", "בצר", "בצר", "gather grapes", "A/B", "Simple", "removal", "Ex (37)"),
    ("גזז", "גזז", "גזז", "shear", "A/B", "Simple", "removal", "Ex (38)"),
    ("גזל", "גזל", "גזל", "rob", "A/B", "Simple", "removal", "Ex (49); MH Frame A only (§8.2)"),
    ("חשך", "חשך", "חשך", "spare", "A/B", "Simple", "removal", "Ex (54); MH Frame A only (§8.2)"),
    ("חשף", "חשף", "חשף", "bare", "A/B", "Simple", "removal", ""),
    ("ינק", "ינק", "ינק", "suck", "A/B", "Simple", "removal", ""),
    ("ירש", "ירש", "ירש", "get/inherit", "A/B", "Simple", "removal", ""),
    ("מחה", "מחה", "מחה", "wipe", "A/B", "Simple", "removal", "Ex (43); MH Frame A only (§8.2)"),
    ("מנע", "מנע", "מנע", "withhold", "A/B", "Simple", "removal", "Ex (13); alternates in MH (§8.2)"),
    ("מרט", "מרט", "מרט", "pluck", "A/B", "Simple", "removal", "Ex (40)"),
    ("עצר", "עצר", "עצר", "stop", "A/B", "Simple", "removal", "Ex (53)"),
    ("עשק", "עשק", "עשק", "exploit", "A/B", "Simple", "removal", "Ex (50)"),
    ("פרק", "פרק", "פרק", "rescue/unload", "A/B", "Simple", "removal", "Ex (12); alternates in MH (§8.2)"),
    ("קצר", "קצר", "קצר", "harvest", "A/B", "Simple", "removal", ""),
    ("רחץ", "רחץ", "רחץ", "wash", "A/B", "Simple", "removal", "Ex (41); alternates in MH (§8.2)"),
    ("רפא", "רפא", "ריפא|רפא", "heal/cure", "A/B", "Simple", "removal", "Ex (44), fn 28 (mostly Intensive); alternates in MH"),
    ("שטף", "שטף", "שטף", "flow over/rinse", "A/B", "Simple", "removal", "Ex (42); manner verb; alternates in MH (§8.1-8.2)"),
    ("שדד", "שדד", "שדד", "rob/devastate", "A/B", "Simple", "removal", ""),
    # =========================================================================
    # B VERBS — Causative (Hif'il): 3 verbs (Section 4.1, p. 13)
    # =========================================================================
    ("האכיל", "האכיל", "האכיל", "feed", "B", "Causative", "putting", "Table 4 mereological"),
    ("השקה", "השקה", "השקה", "water", "B", "Causative", "putting", "Table 4 mereological"),
    ("הנעיל", "הנעיל", "הנעיל", "put footwear on someone", "B", "Causative", "putting", "mereological"),
    # =========================================================================
    # B VERBS — Intensive (Pi'el): 15 verbs (Section 6.1, p. 22)
    # =========================================================================
    ("חפה", "חִפָּה", "חיפה|חפה", "panel/overlay", "B", "Intensive", "putting", "mereological"),
    ("צפה", "צִפָּה", "ציפה|צפה", "overlay/coat", "B", "Intensive", "putting", "Ex (7); mereological"),
    ("קרה", "קֵרָה", "קירה|קרה", "roof with beams", "B", "Intensive", "putting", "mereological"),
    ("כסה", "כִּסָּה", "כיסה|כסה", "cover", "B", "Intensive", "putting", "Ex (59); mereological"),
    ("עטר", "עִטֵּר", "עיטר|עטר", "crown", "B", "Intensive", "putting", "Ex (64), fn 36; locatum-incorporated"),
    ("רפד", "רִפֵּד", "ריפד|רפד", "lay (a bed)", "B", "Intensive", "putting", "mereological"),
    ("גשם", "גִּשֵּׁם", "גישם|גשם", "rain", "B", "Intensive", "putting", "Ex (63); locatum-incorporated"),
    ("ישב", "יִשֵּׁב", "יישב|ישב", "populate", "B", "Intensive", "putting", "mereological"),
    ("דשן", "דִּשֵּׁן", "דישן|דשן", "oil/take away fatty ashes", "B", "Intensive", "both", "Ex (67); locatum-incorporated"),
    ("סקל", "סִקֵּל", "סיקל|סקל", "hurl stones/clear of stones", "B", "Intensive", "both", "Ex (66); locatum-incorporated"),
    ("שרש", "שֵׁרֵשׁ", "שירש|שרש", "take/lose root", "B", "Intensive", "both", "Ex (68), fn 5; locatum-incorporated"),
    ("טמא", "טִמֵּא", "טימא|טמא", "defile", "B", "Intensive", "putting", "Ex (60); mereological"),
    ("טהר", "טִהֵר", "טיהר|טהר", "cleanse/purify", "B", "Intensive", "removal", "Ex (57), fn 32; mereological"),
    ("קדש", "קִדֵּשׁ", "קידש|קדש", "sanctify/cleanse", "B", "Intensive", "removal", "Ex (56); mereological"),
    ("חסר", "חִסֵּר", "חיסר|חסר", "deprive", "B", "Intensive", "removal", "Ex (8),(55); mereological"),
    # =========================================================================
    # B VERBS — Simple (Pa'al): 19 verbs (fn 33, p. 23)
    # =========================================================================
    ("אזר", "אזר", "אזר", "gird", "B", "Simple", "putting", "Table 4 mereological"),
    ("גדר", "גדר", "גדר|גידר", "fence up", "B", "Simple", "putting", "Ex (65), fn 36; locatum-incorporated"),
    ("חגר", "חגר", "חגר", "gird", "B", "Simple", "putting", "Table 4 mereological; fn 38 (alternates in MH)"),
    ("טען", "טען", "טען", "load", "B", "Simple", "putting", ""),
    ("כחל", "כחל", "כחל", "put on makeup", "B", "Simple", "putting", "Ex (61); locatum-incorporated"),
    ("כפר", "כפר", "כפר", "tar", "B", "Simple", "putting", "Ex (61b); locatum-incorporated"),
    ("נעל", "נעל", "נעל", "put on footwear", "B", "Simple", "putting", "mereological"),
    ("סך", "סך", "סך", "anoint", "B", "Simple", "putting", ""),
    ("סבב", "סבב", "סבב|סובב", "surround", "B", "Simple", "putting", "Table 4 mereological"),
    ("ספן", "ספן", "ספן", "cover", "B", "Simple", "putting", "mereological"),
    ("סתם", "סתם", "סתם", "shut/obstruct", "B", "Simple", "putting", ""),
    ("עדה", "עדה", "עדה", "adorn", "B", "Simple", "putting", "Table 4 mereological"),
    ("עטה", "עטה", "עטה", "mantle", "B", "Simple", "putting", "mereological"),
    ("רבד", "רבד", "רבד", "prepare a couch", "B", "Simple", "putting", "mereological"),
    ("שך", "שך", "שך", "hedge", "B", "Simple", "putting", "fn 36"),
    ("גמל", "גמל", "גמל", "wean", "B", "Simple", "removal", "Ex (58); mereological"),
    ("זמר", "זמר", "זמר|זימר", "prune", "B", "Simple", "removal", ""),
    ("זר", "זר", "זר", "squeeze", "B", "Simple", "removal", ""),
    ("שחט", "שחט", "שחט|סחט", "squeeze", "B", "Simple", "removal", "BH orthography שחט = MH סחט"),
]


def main() -> None:
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    # Sanity-check exact counts against Doron & Dubnov (2017)
    counts: dict[tuple[str, str], int] = {}
    for row in VERBS:
        key = (row[4], row[5])
        counts[key] = counts.get(key, 0) + 1

    expected = {
        ("A", "Causative"): 38,
        ("A", "Intensive"): 12,
        ("A", "Simple"): 46,      # 45 stated in fn 33; 46 printed due to אסר appearing in both Ex (33) and fn 33
        ("A/B", "Causative"): 7,
        ("A/B", "Intensive"): 7,
        ("A/B", "Simple"): 31,
        ("B", "Causative"): 3,
        ("B", "Intensive"): 15,
        ("B", "Simple"): 19,
    }
    assert counts == expected, f"Mismatch in verb counts:\nGot:      {counts}\nExpected: {expected}"

    # Verify unique (lemma_bh_unvoc, template) pairs
    keys = [(r[0], r[5]) for r in VERBS]
    assert len(keys) == len(set(keys)), "Duplicate (lemma, template) entry detected!"

    with OUT_PATH.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "id",
            "lemma_bh_unvoc",
            "lemma_bh_voc",
            "mh_lemmas",
            "gloss",
            "paper_class",
            "cluster_ab_vs_b",
            "template",
            "direction",
            "notes",
        ])
        for idx, (unvoc, voc, mh, gloss, pclass, tmpl, direction, notes) in enumerate(VERBS, start=1):
            cluster = "B" if pclass == "B" else "A/(B)"
            writer.writerow([idx, unvoc, voc, mh, gloss, pclass, cluster, tmpl, direction, notes])

    print(f"Wrote {len(VERBS)} rows to {OUT_PATH}")
    for cls in ("A", "A/B", "B"):
        c_caus = counts[(cls, "Causative")]
        c_int = counts[(cls, "Intensive")]
        c_simp = counts[(cls, "Simple")]
        tot = c_caus + c_int + c_simp
        print(
            f"  Class {cls:<3s}: total={tot:<2d} | "
            f"Causative={c_caus:<2d} ({100*c_caus/tot:4.1f}%) | "
            f"Intensive={c_int:<2d} ({100*c_int/tot:4.1f}%) | "
            f"Simple={c_simp:<2d} ({100*c_simp/tot:4.1f}%)"
        )


if __name__ == "__main__":
    main()
