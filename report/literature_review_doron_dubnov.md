# Literature Review — Part 1: Doron & Dubnov (2017)

> **Reference:** Doron, Edit, and Keren Dubnov. 2017. "The locative alternation in Biblical (and Modern) Hebrew." In *Advances in Biblical Hebrew Linguistics: Data, Methods and Analyses*, edited by Adina Moshavi and Tania Notarius, 321–360. Winona Lake, IN: Eisenbrauns. ([DoronDubnov_revised.pdf](../DoronDubnov_revised.pdf))
>
> **Scope:** Detailed summary of Sections 1–3 (pp. 1–12), plus the empirical verb classification, morphological generalizations, typological account, and diachronic Modern Hebrew claims in Sections 4–9 (pp. 13–31) directly relevant to our computational experiments (§5–§8).

---

## 1. Research Problem & Core Claims (Section 1, pp. 1–3)

Ditransitive **locative verbs** take three semantic arguments:
1. **Agent / Cause** (the *external argument*, realized as subject),
2. **Locatum** (an *internal argument* — the entity undergoing a change in location, concrete or abstract),
3. **Location** (an *internal argument* — the Goal in *verbs of putting*, or the Source in *verbs of removal*).

In many languages, certain locative verbs exhibit the **locative alternation** (Rappaport & Levin 1988; terms *Locatum* and *Location* from Clark & Clark 1979): the two internal arguments alternate between direct object and prepositional (indirect) object:

- **Frame A (Locatum as direct object):** `Agent/Cause  V  Locatum  P+Location`
  - Putting: `מִלֵּא בוֹ מַיִם` (*filled water in it*)
  - Removal: `הֵרִיק מִמֶּנּוּ מַיִם` (*emptied water from it*)
- **Frame B (Location as direct object):** `Agent/Cause  V  Location  P+Locatum`
  - Putting: `מִלֵּא אוֹתוֹ בְּמַיִם` (*filled it with water*)
  - Removal: `הֵרִיק אוֹתוֹ מִמַּיִם` (*emptied it of water*)

### Central Discovery: The Locative Alternation Preposition Identity
Unlike English — which uses distinct prepositions in the two frames (`in/into` vs. `with` for putting; `from` vs. `of` for removal) — Hebrew exhibits a striking syntactic property preserved from Biblical Hebrew (BH) into Modern Hebrew (MH):

> **The Locative Alternation Preposition Identity:** In Hebrew (both BH and MH), verbs that undergo the locative alternation allow the **same preposition** in both alternants — **`ב-` (*b-*)** for verbs of putting, and **`מן / מ-` (*min / mi-*)** for verbs of removal.

While partial preposition identity has been documented for removal verbs in Romance languages (e.g., Spanish *de*) and Arabic (*min*), Doron & Dubnov argue that Hebrew exhibits full preposition identity across *both* putting and removal verbs. They further show (fn. 7) that Frame B `ב-` is **not** the instrumental preposition *with* (unlike Instrument `ב-`, Locatum `ב-` cannot co-occur with Location `ב-`, can elide when its complement is indefinite, and appears in non-instrumental depictive adjuncts).

Doron & Dubnov's three main objectives in the paper are:
1. Uncover the **semantic and morphological factors** that distinguish alternating BH locative verbs from non-alternating ones.
2. Derive **Preposition Identity** from a deeper typological property of BH: its classification as a **verb-framed language** (Talmy 1985, 1991, 2000) combined with the **symmetry** of stative prepositions `ב-` and `מן`.
3. Demonstrate that **Modern Hebrew inherits** both Preposition Identity and the underlying BH verb classification, supporting the historical continuity of MH syntax from BH (against Wexler 1990).

---

## 2. Locative Verbs in Biblical Hebrew (Section 2, pp. 3–7)

### Database & Methodology (fn. 5)
Doron & Dubnov compiled a database of **177 ditransitive locative verbs** from Even-Shoshan's concordance (1982) denoting a change, preservation, or prevention of location (allowing both concrete and abstract/metaphoric arguments, as well as passive and middle diathesis forms since both target the direct object and thus distinguish Frame A from Frame B). Each verb had to be attested with both internal arguments explicitly in the Hebrew Bible (either together in one verse, or across Frame A and Frame B verses). Because BH is a finite corpus, **partial frames** (where the PP is omitted, or the direct object is elided with a discourse antecedent) still diagnose the frame via which argument serves as direct object / passive subject.

### Three Verb Classes
| Class | Name | Permitted Frame(s) | BH Count | Core Examples |
| :--- | :--- | :--- | :---: | :--- |
| **A verbs** | Non-alternating Frame A | Frame A only (`V Locatum P+Location`) | **95** | `זֵרָה` (disperse), `גֵּרֵשׁ` (drive out), `הֵפִיץ` (scatter), `הִנִּיחַ` (put/rest), `הִגְלָה` (deport) |
| **A/B verbs** | Alternating verbs | Both Frame A & Frame B | **45** | `מִלֵּא` (fill), `רָגַם` (stone), `שָׂם` (put), `פָּרַק` (rescue/unload), `מָנַע` (withhold), `הֵרִיק` (empty) |
| **B verbs** | Non-alternating Frame B | Frame B only (`V Location P+Locatum`) | **37** | `צִפָּה` (coat/overlay), `כִּסָּה` (cover), `חִסֵּר` (deprive), `טִהֵר` (purify), `קִדֵּשׁ` (cleanse) |

*(Methodological note from our digitization: in footnote 33, p. 23, the authors state 45 Simple A verbs and 31 Simple A/B verbs, but print `אסר` ("bind/harness") at the start of the Simple A list—making 46 printed Simple A entries—even though `אסר` is analyzed as an A/B verb in Example (33), p. 17. Our curated lexicon preserves this note explicitly.)*

---

## 3. Syntactic Analysis of Alignment Alternation (Section 3, pp. 7–12)

Inspired by small-clause analyses of locative verbs (Hoekstra 2004; Hale & Keyser 2002; Folli & Harley 2006), Doron & Dubnov propose **three distinct syntactic-semantic structures** that explain why only A/B verbs alternate:

### 3.1 Structural Distinction Between A/B, A, and B Verbs (§3.1, pp. 7–10)
1. **A/B Verbs (Alternating — Directed Action toward a Result State):**
   - Structure: `Agent  V_D-ACTION  [PP  Locatum/Location  [PP  P_SYMMETRIC  Location/Locatum]]`
   - The verb takes an obligatory **Agent** and a **small-clause PP complement** denoting the result state. **Neither** Locatum nor Location is directly selected by the verb; both are arguments of the preposition `P`.
   - Because BH is verb-framed, the verb itself lexicalizes the direction/path of change, leaving the preposition **stative** (`in/contact` rather than `into`).
   - Because `ב-` ("close connection / being together"; Gesenius §119h) and `מן` ("separation / being separate"; Gesenius §119v) are **symmetric stative relations**, their two arguments can freely reverse positions inside the PP without changing grammaticality — producing Frame A ↔ Frame B with the **same preposition**.
   - *(Note on indefinite Locatum, fn. 13 & fn. 21)*: In Frame B, `P` may be omitted when the Locatum is indefinite (e.g., `וּמִלֵּאתִי אֶת-הַבַּיִת הַזֶּה כָּבוֹד`, Haggai 2:7), a general property of BH small-clause predicates.

2. **A Verbs (Non-Alternating Frame A — Directed Motion of Locatum):**
   - Structure: `(Cause)  [VP  Locatum_i  [VP  V_D-MOVE  [PP  Ø_i  [PP  P  Location]]]]`
   - Describe the event in terms of the **motion of the Locatum** along a trajectory, without specifying a change of state of the Location.
   - The **Locatum is directly selected as an argument of the verb** (`V_D-MOVE`), while Location is inside `PP`. Because they are arguments of different heads (`V` vs. `P`), they **cannot alternate** — even when `P` is symmetric `ב-` or `מן`.
   - The external argument is optional and plays the role of **Cause** (not strictly Agent), since motion may be spontaneous; many A verbs are derived by causativizing unaccusative motion verbs.

3. **B Verbs (Non-Alternating Frame B — Acquiring/Losing a Mereological Part):**
   - Structure: `(Agent)  [VP  Location_i  [VP  V_ACQUIRE/LOSE_PART  [PP  Ø_i  [PP  P  Locatum]]]]`
   - Describe the event in terms of the **Location acquiring or losing an integral/possessed part** (a *mereological* part-whole relation — inclusion, covering, possession, consumption, or deprivation).
   - The **Location is directly selected as an argument of the verb**, while Locatum is inside `PP`. Because they belong to different heads (`V` vs. `P`), they **cannot alternate** even with symmetric `ב-` or `מן`.

### 3.2 Two Empirical Arguments Supporting the Analysis (§3.2, pp. 10–12)
1. **Path-Ambiguous Putting/Removal Verbs (§3.2.1, Table 1):**
   - Many BH verbs (e.g., `שִׁלַּח`, `הֶעֱלָה`, `הוֹרִיד`, `הֵבִיא`, `הוֹצִיא`, `הֵשִׁיב`, `קָבַץ`, `אָסַף`, `הִשְׁלִיךְ`, `הֵפִיץ`, `זָרַק`, `הִגְלָה`, `הֶעֱבִיר`) can occur as *both* putting verbs (with Goal PPs) and removal verbs (with Source PPs).
   - This shows (i) putting and removal verbs deserve a unified analysis, (ii) **path of motion is lexicalized in the verb**, while the preposition merely encodes presence at Goal or absence from Source, and (iii) crucially, **all such path-ambiguous verbs are either A or A/B verbs — never mereological B verbs**, because B verbs do not lexicalize a path of motion.
2. **Change-of-State Verbs Reinterpreted as Locative A Verbs (§3.2.2, Table 2):**
   - Non-locative change-of-state verbs (e.g., `קָרַע` tear, `שָׁבַר` break, `כִּלָּה` consume, `בָּעַר` burn, `שָׁחַט` slay, `הוֹבִישׁ` dry, `הֵעִיר` wake) have a single internal argument (the theme undergoing change).
   - When augmented with a non-subcategorized result PP denoting Location, they become locative verbs — and are **always non-alternating A verbs**, confirming that alternation is blocked whenever one argument is directly selected by `V`.

---

## 4. Morphological Correlates Across Classes (Sections 4–6, pp. 13–26)

A major empirical prediction directly testable by our morphological parser (§5) and supervised classifiers (§7) is the **strong correlation between Hebrew verbal templates (*binyanim*) and locative class**:

| Class | Causative (*Hif'il*) | Intensive (*Pi'el*) | Simple (*Pa'al*) | Total | Linguistic Motivation |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **A verbs** | **38 (40.0%)** | 12 (12.6%) | 45 (47.4%) | **95** | High *Hif'il* rate reflects adding a *Cause* argument to unaccusative motion verbs (Table 3: `עלה`→`העלה`, `ירד`→`הוריד`, `יצא`→`הוציא`). |
| **A/B verbs** | 7 (15.6%) | 7 (15.6%) | **31 (68.9%)** | **45** | Predominantly default *Pa'al*; obligatory Agent (middle *Nif'al* reads as passive, not unaccusative; fn. 33). |
| **B verbs** | 3 (8.1%) | **15 (40.5%)** | 19 (51.4%) | **37** | High *Pi'el* rate mirrors A's *Hif'il* rate; derived from transitive mereological relations (Table 4) or **Locatum incorporation** into the verbal root (§6.2: `כחל`, `כפר`, `גִּשֵּׁם`, `עִטֵּר`, `גדר`, `סִקֵּל`, `דִּשֵּׁן`, `שֵׁרֵשׁ`). |

*(Note: Locatum-incorporating B verbs such as `סִקֵּל`, `דִּשֵּׁן`, `שֵׁרֵשׁ` actually behave syntactically like path/alternating verbs—even permitting putting/removal ambiguity—but cannot surface in Frame A because the Locatum is already incorporated into the root.)*

---

## 5. Typology & Historical Evolution into Modern Hebrew (Sections 7–9, pp. 26–31)

- **BH as a Verb-Framed Language (§7):** Following Talmy (1985, 1991, 2000), BH encodes **direction/path in the verb** (`הביא`, `הוציא`, `העלה`, `הוריד`, `השיב`) and has very few (~20) **manner-of-motion** verbs (`רץ`, `הלך`, `רכב`, `עף`, `זחל`), which cannot combine directly with directional result phrases (instead using verb coordination or embedding, Table 5). Because direction lives in the verb, locative prepositions remain stative and symmetric, enabling Preposition Identity.
- **Modern Hebrew Shift Toward Satellite-Framed Properties (§8.1):** Unlike BH, MH has innovated many manner-of-motion verbs and freely combines them with directional prepositions (`רכב אל מתחת לגשר`, `זחל אל מחוץ לבור`), and has innovated many alternating surface-contact/removal verbs (`שפשף`, `ניער`, `ניגב`, `קרצף`, `צחצח`, `הבריש`, `טאטא`, `מירק`, `גירף`, `זיקק`, `עיסה`). Yet MH **retains Preposition Identity** — which neither a satellite-framed system nor its Slavic/Germanic contact languages could have produced independently, proving inheritance from BH.
- **Preservation of the Two-Cluster Boundary (§8.2):** The 3 classes cluster into **path verbs `A/(B)`** vs. **mereological `B` verbs**. Doron & Dubnov predict that historically, BH `A/(B)` verbs do not cross over into `B`-only verbs in MH: many alternating BH verbs continue to alternate in MH (`מילא`, `משח`, `זרע`, `שטף`, `רוקן/הריק`, `פרק`, `ניקה`, `ריפא`, `פינה`, `רחץ`, `בזז`, `מנע`, `הפשיט`), and **whenever alternation is lost, Frame A is always preserved** (`שם`, `הסיר`, `היזה`, `ירה`, `אסף`, `חשך`, `גזל`, `מחה`).

---

## 6. Direct Implications for Our Computational Study (§5–§8)

1. **§5 (Testing Central Claims):** We can empirically test (a) Frame A vs. Frame B distributions of all 177 verbs across BH and later corpora, (b) **Preposition Identity** (`ב-` and `מן/מ-` rates across frames), (c) binyan proportions (Hif'il in A, Pi'el in B, Pa'al in A/B), and (d) the §8.2 diachronic claim that lost alternations collapse to Frame A.
2. **§6 (Scope Expansion):** Searching all verbs in Modern Hebrew should rediscover both the paper's predicted MH manner-of-motion alternating innovations (§8.1) and additional alternating verbs outside the 177 BH list.
3. **§7 (Verb Classifiers):** Because morphology (binyan, voice/Nif'al passivity), syntax (preposition choice, subcategorization frames), and lexical argument types systematically differentiate A, A/B, and B verbs, comparing Lexical, Morphological, Syntactic, Combined, and Word2Vec features directly tests which linguistic cues carry the strongest signal.
