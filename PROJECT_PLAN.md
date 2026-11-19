# NLP Mini-Project Plan & Progress Tracker: Locative Verbs in Hebrew

> **Course:** Mini-Project, Semester A 2027 — *On Motion / Locative Verbs in Hebrew* (*על פעלי התנועה בעברית*)
> **Primary Paper:** Edit Doron & Keren Dubnov (2017), *"The locative alternation in Biblical (and Modern) Hebrew"* ([DoronDubnov_revised.pdf](DoronDubnov_revised.pdf))
> **Project Spec:** [project.docx.pdf](project.docx.pdf)

---

## Progress Dashboard

| Phase | Spec Section(s) | Status | Key Deliverable(s) |
| :--- | :---: | :---: | :--- |
| **Phase 0:** Environment & Repo Setup | Setup | ✅ Completed | Clean repo structure, `.venv`, local offline `dictabert-tiny-joint`, smoke test + CPU benchmark |
| **Phase 1:** Literature Review & Theoretical Background | §1.1, §1.2 | ✅ Completed | [literature_review_doron_dubnov.md](report/literature_review_doron_dubnov.md), [literature_review_background.md](report/literature_review_background.md), [doron_dubnov_177_verbs.csv](data/curated/doron_dubnov_177_verbs.csv) |
| **Phase 2:** Corpora Acquisition & Preprocessing | §2 | ✅ Completed | 16 normalized Parquet shards (`data/processed/`, 323,977 sents / 6.65M words) + raw & processed audit tables |
| **Phase 3:** Automated Parsing with DictaBERT | §3 | ⬜ Not Started | Parsed corpora (morphology + dependency trees) saved to disk |
| **Phase 4:** Diachronic & Genre Corpus Statistics | §4 | ⬜ Not Started | Statistical tables, plots, tree-depth & linguistic analysis |
| **Phase 5:** Testing Doron & Dubnov's Central Claims | §5 | ⬜ Not Started | 177-verb extraction, Frame A/B & preposition identity results (BH + all corpora) |
| **Phase 6:** Expanding Scope to All Verbs | §6 | ⬜ Not Started | Full-corpus verb classification & characterization of new alternating verbs |
| **Phase 7:** Supervised Verb Classification | §7 | ⬜ Not Started | Multi-feature & word2vec classifiers, 10-fold CV benchmarks, ablation analysis |
| **Phase 8:** LLM & AI Tool Integration | §8 | ⬜ Not Started | DictaLM / LLM integration for semantic role disambiguation, discovery & baseline |
| **Phase 9:** Personal Initiative (Research Extensions) | §11 | ⬜ Not Started | 1–2 deep, data-driven extensions beyond the spec |
| **Phase 10:** Final Report & Submission Package | §9, §10 | ⬜ Not Started | Polished report, curated datasets, reproducible codebase |

*Status legend:* `⬜ Not Started` · `🟨 In Progress` · `✅ Completed` · `⛔ Blocked`

---

## Key External Resources (from `project.docx.pdf`)

| Resource | Purpose | Link |
| :--- | :--- | :--- |
| **Text Corpora Archive** | 5 historical layers + MH genres | [Google Drive Download](https://drive.google.com/file/d/1M3vAm4Aqm8uaFZyqwIwk0r6KNtFYb1_E/view?usp=sharing) |
| **Dicta Joint Parser Model** | Morphology + Dependency Parsing | [dicta-il/dictabert-tiny-joint](https://huggingface.co/dicta-il/dictabert-tiny-joint) |
| **Morphological Analysis Demo** | Interactive parser verification | [Dicta Joint Demo](https://huggingface.co/spaces/dicta-il/joint-demo) |
| **Syntactic Analysis Demo** | Dependency tree inspection | [Oracle Parser Live Parse](https://oracleparser.netlify.app/#/liveParse) |
| **DictaBERT / Dicta Models** | Pretrained Hebrew models / embeddings | [DictaBERT Collection](https://huggingface.co/collections/dicta-il/dictabert) |
| **DictaLM 2.0 Chat** | Hebrew LLM exploration (§8) | [DictaLM 2.0 Instruct Demo](https://huggingface.co/spaces/dicta-il/dictalm2.0-instruct-demo) |

---

## Proposed Repository Structure

```text
Mini Project/
├── PROJECT_PLAN.md              # This living plan & progress tracker
├── README.md                    # Final repository overview & reproduction guide
├── requirements.txt             # Pinned Python dependencies
├── project.docx.pdf             # Project instructions
├── DoronDubnov_revised.pdf      # Core reference paper
├── data/
│   ├── raw/                     # Downloaded corpora (gitignored)
│   ├── processed/               # Cleaned sentences & metadata (gitignored)
│   ├── parsed/                  # DictaBERT morphological & syntactic parses (Parquet/JSONL, gitignored)
│   └── curated/                 # Small curated artifacts (177 verb list, gold samples, feature tables)
├── src/
│   ├── corpora/                 # Loading, cleaning, sentence/verse normalization
│   ├── parsing/                 # Batched DictaBERT-tiny-joint inference & serialization
│   ├── stats/                   # §4 corpus statistics & visualizations
│   ├── locative/                # §5 & §6 frame extraction, preposition checks, verb discovery
│   ├── classifiers/             # §7 feature engineering, word2vec, 10-fold CV pipelines
│   └── llm/                     # §8 DictaLM / LLM prompting & evaluation scripts
├── notebooks/                   # Exploratory analysis & figure generation
├── results/
│   ├── tables/                  # CSV/Markdown summary tables
│   └── figures/                 # Publication-ready plots for the report
└── report/                      # Drafts, bibliography, and final report
```

---

## Phase-by-Phase Execution Plan

### Phase 0: Environment & Repository Setup
- [x] Create directory structure (`data/`, `src/`, `notebooks/`, `results/`, `report/`) and configure `.gitignore` (ignore large raw/parsed data and model caches).
- [x] Set up Python virtual environment (`.venv`, Python 3.11.5) and install core packages (`torch` CPU, `transformers`, `pandas`, `pyarrow`, `scikit-learn`, `gensim`, `matplotlib`, `seaborn`, `scipy`, `tqdm`, `jupyter`).
- [x] Decide compute strategy: **Local CPU** (6 threads, `dictabert-tiny-joint` achieves **~41 sent/s** at `batch_size=32`, fully offline from `models/dictabert-tiny-joint`).
- [x] Run smoke test (`src/parsing/smoke_test.py`) of `dicta-il/dictabert-tiny-joint` on 6 sample sentences (Modern, Biblical vocalized/unvocalized, Rabbinic) and inspect exact JSON schema (`results/tables/phase0_smoke_test_output.json`).

---

### Phase 1: Literature Review & Theoretical Background (§1)

#### 1.1 Doron & Dubnov (2017) — Core Paper (§1.1)
- [x] Read Sections 1–3 thoroughly (pp. 1–12) and Sections 4–9 (pp. 13–31) for the full verb lists and Modern Hebrew comparison.
- [x] Write a structured summary (`report/literature_review_doron_dubnov.md`) covering:
  - [x] **Arguments & Frames:** Agent/Cause (external), Locatum & Location (internal); **Frame A** (`V Locatum P+Location`) vs. **Frame B** (`V Location P+Locatum`).
  - [x] **Three Verb Classes (177 BH verbs total):** A (95), A/B (45), B (37) + binyan proportions (Causative 40% in A, Intensive 40% in B, Simple ~70% in A/B).
  - [x] **Locative Alternation Preposition Identity:** `ב-` (*b-*) for putting verbs and `מן / מ-` (*min / mi-*) for removal verbs in both frames.
  - [x] **Typological Explanation (Talmy):** Verb-framed BH + symmetric stative prepositions.
  - [x] **Diachronic Inheritance (§8 of paper):** Modern Hebrew preserves Preposition Identity and the `A/(B)` vs. `B` cluster boundary.
- [x] Digitize the paper's complete list of **177 BH locative verbs** (from Sections 4, 5, 6 and fn. 33) via `src/locative/build_doron_dubnov_lexicon.py` into `data/curated/doron_dubnov_177_verbs.csv` (178 rows incl. the documented `אסר` fn. 33 / Ex. 33 erratum, plus Modern Hebrew plene `mh_lemmas`).

#### 1.2 Linguistic & ML Background (§1.2)
*(Saved in `report/literature_review_background.md` with full scholarly bibliography.)*
- [x] **Morphology & Syntax:** Roots/templates, lemmas, POS, inflectional features, clitic prefixes/suffixes, UD dependency trees & tree depth.
- [x] **Biblical Hebrew (לשון המקרא):** Morphological & syntactic characteristics + scholarly references (Gesenius, Waltke & O'Connor, Joüon & Muraoka, Sáenz-Badillos, Khan *EHLL*).
- [x] **Rabbinic Hebrew (לשון חכמים / חז"ל):** Morphological & syntactic characteristics + scholarly references (Segal, Pérez Fernández, Bar-Asher, Breuer).
- [x] **Medieval Hebrew (לשון ימי הביניים):** Morphological & syntactic characteristics across Rambam, Tibbonide philosophy & Musar + scholarly references (Sáenz-Badillos, Rabin, Goshen-Gottstein, Khan *EHLL*).
- [x] **Haskalah Hebrew (לשון ההשכלה):** Early purism (*melitzah*) vs. late synthetic style + scholarly references (Patterson, Kahn 2009/2013, Sáenz-Badillos).
- [x] **Modern Hebrew (העברית המודרנית):** Morphological, syntactic, typological & genre stratification characteristics + scholarly references (Berman, Glinert, Coffin & Bolozky, Doron & Dubnov).
- [x] **Classifiers & Evaluation Metrics:** Logistic Regression, SVM, Random Forest, Gradient Boosting, MLP; 10-fold stratified CV & leakage prevention; Accuracy, Precision, Recall, F-Measure (Macro/Weighted/Micro) + scholarly references (Hastie et al., Bishop, Kohavi, Powers, Sokolova & Lapalme, Jurafsky & Martin).

---

### Phase 2: Corpora Acquisition & Preprocessing (§2)
- [x] Download and extract the corpora archive (`corpora.rar`, 478 MB compressed / 1.13 GB uncompressed, 404,294 files, ~186.5M words) into `data/raw/extracted/` via `src/corpora/download_corpora.py` + 7-Zip.
- [x] Audit folder structure, file formats, character encodings, and verify all 5 historical layers & sub-corpora (`src/corpora/audit_raw.py` -> `results/tables/phase2_raw_audit.json`):
  - [x] **Biblical (מקרא):** Tanakh (39 books, UTF-8, niqqud + te'amim)
  - [x] **Rabbinic (חז"ל):** Mishnah (63), Tosefta (61), Tannaitic Midrashim (`Midrash - Halakhah`, 5), Aggadic Midrashim (21 primary works; late Medieval commentaries separated out)
  - [x] **Medieval (ימי הביניים):** Rambam's Mishneh Torah (1,091), Musar (22), Thought (12 primary works)
  - [x] **Haskala (ספרות ההשכלה):** 320 works (UTF-8)
  - [x] **Modern Hebrew (עברית מודרנית — all `cp1255`):** News (378k `.txt` across 5 outlets; 99 `.log` excluded), Literature (`O.txt` original + `T.txt` translated), Tapuz Forum (255), Blogs (11,176), Medical (12,750), Knesset protocols (282)
- [x] Inspect text cleanliness and handle encoding (`utf-8-sig` vs. `cp1255`), niqqud/te'amim stripping, Mikra maqaf normalization, HTML/markup/`[IMG]` removal, Tapuz cross-doc boilerplate deduplication, and Hebrew sentence splitting (`<=120` words/sent).
- [x] Write and run `src/corpora/preprocess.py` producing 16 uniform Parquet shards in `data/processed/` (**323,977 sentences**, **6,646,770 words** — 100% of Tanakh, Mishnah, Tosefta, and Rambam + deterministic stratified samples with `seed=42` for the multi-million-word sub-corpora).
- [x] Log corpus counts and local CPU parse estimate (`~132 min` total at 41 sent/s) in `results/tables/phase2_processed_summary.csv`.

---

### Phase 3: Automated Morphological & Syntactic Parsing (§3)
- [ ] Implement `src/parsing/run_dicta_parser.py` using `dicta-il/dictabert-tiny-joint` with:
  - [ ] Batched inference & GPU acceleration (`torch.cuda` / mixed precision if supported).
  - [ ] Chunking / handling for sentences exceeding BERT's 512-token limit.
  - [ ] Per-subcorpus checkpointing so runs are resumable and crash-safe.
  - [ ] Structured output saving per token: `token_id`, `surface`, `lemma`, `pos`, `morph_feats` (gender, number, person, tense, state/construct, binyan if present), `prefixes` (`מ ש ה ו כ ל ב`), `suffixes` (possessive, object clitics), `head`, `deprel`.
- [ ] Validate parser outputs on a small sample from each period against the [Morphological Demo](https://huggingface.co/spaces/dicta-il/joint-demo) and [Syntactic Demo](https://oracleparser.netlify.app/#/liveParse).
- [ ] Run parser across all 5 periods and all sub-corpora:
  - [ ] Biblical Hebrew (Tanakh)
  - [ ] Rabbinic Hebrew (4 sub-corpora)
  - [ ] Medieval Hebrew (3 sub-corpora)
  - [ ] Haskalah Literature
  - [ ] Modern Hebrew (6 genres)
- [ ] Perform post-parse integrity checks (0 corrupted files, valid tree roots/no cycles, token alignment sanity checks).

---

### Phase 4: Corpus-Level Statistical Analysis (§4)
Build `src/stats/compute_stats.py` and generate comparative tables & visualizations across the 5 historical periods (and across the 6 Modern Hebrew genres):

- [ ] **Lexical statistics:**
  - [ ] Top words & top lemmas with frequencies; Zipf distribution comparison across periods.
  - [ ] Vocabulary size, Type-Token Ratio (TTR) / standardized TTR (fixed-window TTR so comparisons aren't biased by corpus size!).
  - [ ] Cross-period lexical overlap (Jaccard / shared core vocabulary).
- [ ] **Sentence length & lexical diversity:**
  - [ ] Sentence length distribution (mean, median, std, IQR, 95th percentile) in tokens & words.
  - [ ] Number of unique words / unique lemmas per sentence (and unique-to-total ratio).
- [ ] **Syntactic tree depth:**
  - [ ] Compute dependency tree depth (longest path from root to leaf) per sentence; also compute mean dependency distance (MDD) as a complementary complexity metric.
  - [ ] **Interpret the meaning of tree depth:** Relate depth to syntactic complexity, subordination/embedding (hypotaxis vs. parataxis), coordination conventions in UD trees, and sentence length (also report depth normalized by sentence length!).
- [ ] **Morphological feature distributions:**
  - [ ] POS tag proportions (NOUN, VERB, ADJ, ADV, ADP, PRON, etc.) and Noun-to-Verb ratio.
  - [ ] Inflectional features: gender, number, person, tense/aspect, construct vs. absolute state (`סמיכות`), prefix frequencies (`ב/ל/מ/כ/ה/ו/ש`), possessive & object suffix frequencies (tracking the historical shift from synthetic suffixes in BH to analytic `של`/`את` in MH!).
- [ ] **Syntactic structure distributions:**
  - [ ] Dependency relation (`deprel`) frequency distributions (`nsubj`, `obj`, `iobj`, `obl`, `case`, `advcl`, `acl`, `conj`, etc.).
  - [ ] Additional insightful statistics:
    - [ ] Word order (VS vs. SV ratios across periods).
    - [ ] Preposition distribution (`ב-`, `מן/מ-`, `על`, `אל`, `ל-`, `את`).
    - [ ] Passive/middle vs. active verb ratios and verbal valency distributions.
- [ ] Export clean CSV tables to `results/tables/` and high-resolution figures to `results/figures/`.

---

### Phase 5: Testing Doron & Dubnov's Central Claims (§5)

> **Key Technical Insight (Crucial Design Point):**
> In Hebrew, Frame A (`מילא מים במיכל` — *filled water in-the-tank*) and Frame B (`מילא את המיכל במים` — *filled ACC the-tank with-water*) share the **exact same surface dependency pattern**: `VERB -> obj (NP1)` + `VERB -> obl (NP2) -> case (P)`.
> Therefore, automated classification of an occurrence into **Frame A vs. Frame B** requires a layered strategy:
> 1. **Syntactic extraction:** Identify verb occurrences with direct object (`obj`, or passive/middle `nsubj` per Doron & Dubnov §2.1, or cliticized object suffix on the verb!) and/or locative PP complement (`obl` + `case` preposition, plus double-object / prepositionless indefinite Locatum cases per fn. 13/21).
> 2. **Frame A vs. Frame B disambiguation:** Combine (a) syntactic cues (e.g., directional prepositions `אל/ל-`, `מאת/מעל`, passive subject type, verb-specific alternation patterns), (b) semantic argument typing (container/place/human vs. substance/theme using lexical ontologies, embeddings, or clustering of `obj` vs. `obl` noun lemmas), and (c) LLM-assisted semantic role annotation (linking cleanly to §8), validated on a manually annotated gold subset!

#### Stage 1: Biblical Hebrew (Tanakh)
- [ ] Match all occurrences of the **177 Doron & Dubnov locative verbs** in parsed Tanakh (handle lemma normalization, orthographic/niqqud variants, binyan matching so e.g. Pa'al vs. Pi'el/Hif'il homographs aren't conflated, and passive/middle forms).
- [ ] Extract full argument frames for every occurrence: verb lemma, binyan/morph features, subject, direct object (including object clitic suffixes & passive subjects), and all `obl`/PP dependents with their `case` prepositions.
- [ ] Build & validate the automated Frame A vs. Frame B classifier on a manually annotated gold set of BH verses (e.g., 100–200 verses across A, B, and A/B verbs) to report precision/recall of the automatic pipeline itself.
- [ ] Automatically classify each locative verb in Tanakh into **A**, **B**, or **A/B** based on its observed frames.
- [ ] Extract the preposition in each frame for every alternating verb and measure **Preposition Identity** rate (`ב-` in both frames for putting; `מן/מ-` in both frames for removal; vs. exceptions like `על` or elided P).
- [ ] Compute statistics and compare directly against Doron & Dubnov (2017):
  - [ ] Agreement matrix (confusion matrix) between our automated classification and Doron & Dubnov's 95 A / 45 A-B / 37 B classification.
  - [ ] Binyan distribution check (Causative ~40% in A, Intensive ~40% in B, Simple ~70% in A/B).
  - [ ] Qualitative error analysis on disagreements (parser errors in BH vs. partial/elliptical frames vs. rare verbs).

#### Stage 2: All Remaining Corpora (Rabbinic, Medieval, Haskalah, Modern Hebrew)
- [ ] Run the exact same extraction, frame classification, and preposition identity pipeline on Rabbinic, Medieval, Haskalah, and Modern Hebrew (both overall and per genre).
- [ ] Track how the 177 BH verbs behave diachronically across all 5 periods:
  - [ ] Which verbs survive in each period?
  - [ ] Does **Preposition Identity** (`ב-` / `מן`) remain stable from BH through Modern Hebrew?
  - [ ] Test Doron & Dubnov §8.2: Do BH `A/(B)` verbs ever become `B`-only in later periods? When alternation is lost, is **Frame A** consistently preserved?
- [ ] Summarize comparative statistics across all periods in tables and diachronic trend charts.

---

### Phase 6: Expanding the Scope Beyond Locative Verbs (§6)
- [ ] Choose primary target corpus for full-verb expansion (recommended: **Modern Hebrew** — e.g., News + Literature, or both **Modern Hebrew** and **Tanakh** for contrast).
- [ ] Filter all verbs in the target corpus meeting a minimum frequency threshold (e.g., ≥20 ditransitive/PP-taking occurrences) to ensure reliable frame estimation.
- [ ] Automatically classify *all* eligible verbs into the paper's syntactic categories (`Frame A`, `Frame B`, `Alternating A/B`, and `Non-locative / Other`).
- [ ] Detect **newly discovered alternating verbs** (verbs outside Doron & Dubnov's 177 list that appear in both Frame A and Frame B, especially with identical prepositions `ב-` or `מן/מ-`).
- [ ] Check whether Modern Hebrew manner-of-motion/contact innovations predicted in Doron & Dubnov §8.1 (`שפשף`, `ניגב`, `קרצף`, `צחצח`, `הבריש`, `טאטא`, `מירק`, `גירף`, `זיקק`, `עיסה`, etc.) emerge automatically from the data!
- [ ] Linguistically characterize the newly discovered alternating verbs:
  - [ ] Semantic domains (manner-of-motion/surface contact, communication/information transfer, loading/covering, metaphorical locatives, etc.).
  - [ ] Morphological templates (binyan distribution).
  - [ ] Preposition identity behavior (`ב-`, `מן`, or other prepositions like `על`/`ל-`).

---

### Phase 7: Building & Evaluating Verb Classifiers (§7)
- [ ] Construct the labeled verb classification dataset(s):
  - [ ] **Dataset 1 (Gold BH Benchmark):** Doron & Dubnov's 177 verbs labeled `{A, B, A/B}` (also test binary `{A/(B) vs. B}` and `{Alternating vs. Non-alternating}` to analyze class separability).
  - [ ] **Dataset 2 (Expanded Corpus Dataset):** Larger verb set from §6 (e.g., Modern Hebrew corpus) labeled by category, enabling testing of corpus-dependence and sample-size effects.
- [ ] Engineer separate feature vector representations per verb (aggregated over corpus occurrences; avoid label leakage!):
  - [ ] **Feature Set 1 — Lexical:** Context words/lemmas around the verb (window ±3 and argument head lemmas) encoded with TF-IDF / SVD or top-K PMI features.
  - [ ] **Feature Set 2 — Morphological:** Verb's own morphological feature distribution (binyan, voice/passive, tense, person/number/gender, object clitic rate) + neighboring/argument morphological features (definiteness, construct state, POS, prefixes).
  - [ ] **Feature Set 3 — Syntactic:** Dependency tree paths centered on the verb as root (subcategorization frames, `deprel` + preposition combinations, valency, depth, child POS/deprel bigrams).
  - [ ] **Feature Set 4 — Combined Feature Sets:** `Lex + Morph`, `Lex + Synt`, `Morph + Synt`, and `All Combined`.
  - [ ] **Feature Set 5 — Word2Vec Embeddings:** Obtain Dicta's Hebrew word2vec embeddings for each verb (plus fallback/comparison with corpus-trained word2vec if needed for archaic BH lemmas missing from Modern word2vec).
- [ ] Train and compare multiple classifier families on every feature set:
  - [ ] Logistic Regression (L2 regularized, class-weighted)
  - [ ] Support Vector Machine (Linear & RBF kernels)
  - [ ] Random Forest
  - [ ] Gradient Boosting (XGBoost / LightGBM / HistGradientBoosting)
  - [ ] Multi-Layer Perceptron (MLP)
  - [ ] Majority-class / Stratified Dummy Baseline (for sanity reference)
- [ ] Run **10-fold Stratified Cross-Validation** for every `(Feature Set × Classifier)` pair (ensure scaling/TF-IDF/SVD fit *inside* each CV fold to prevent data leakage!).
- [ ] Record **Accuracy, Precision, Recall, and F-Measure (Macro-F1 & Weighted-F1)** + per-class scores and confusion matrices.
- [ ] Conduct thorough analysis of results:
  - [ ] Feature ablation: Which feature families are sufficient vs. redundant? Does combining features beat individual sets?
  - [ ] Compare engineered linguistic features vs. static word2vec embeddings.
  - [ ] Class-level analysis: Which class (`A`, `B`, `A/B`) is hardest to classify and why?
  - [ ] Corpus/period sensitivity: Does training/extracting features from Modern Hebrew vs. Biblical Hebrew change classifier performance?
  - [ ] Feature importance inspection (SHAP / linear weights / RF importances) — link top predictive features back to Doron & Dubnov's linguistic theory.

---

### Phase 8: Integrating Dicta LLMs & AI Tools (§8)
Design and execute concrete, empirically evaluated uses of Dicta's LLMs ([DictaBERT collection](https://huggingface.co/collections/dicta-il/dictabert), [DictaLM 2.0 Instruct](https://huggingface.co/spaces/dicta-il/dictalm2.0-instruct-demo)) and/or modern LLMs:

- [ ] **Use Case 1 — Semantic Role Disambiguation (Frame A vs. Frame B):**
  - [ ] Design a structured Hebrew/English few-shot prompt asking the LLM to identify whether a sentence's direct object is the *Locatum* (Frame A) or *Location* (Frame B) and extract the preposition.
  - [ ] Benchmark LLM accuracy on the manually annotated gold sample from Phase 5 (and compare against heuristic/embedding frame classification).
- [ ] **Use Case 2 — Zero-Shot / Few-Shot Verb Classifier Benchmark (§7 Comparison):**
  - [ ] Prompt DictaLM / LLM to classify verbs into `A`, `B`, or `A/B` (with and without example corpus sentences) and compare Accuracy/Precision/Recall/F1 against the Phase 7 supervised ML classifiers.
- [ ] **Use Case 3 — Candidate Verification & Minimal-Pair Probing (§6):**
  - [ ] For newly discovered alternating verb candidates in §6, use the LLM to generate/judge grammaticality of Frame A vs. Frame B minimal pairs and propose semantic class descriptions, followed by human linguistic verification.
- [ ] **Use Case 4 — Contextualized DictaBERT Embeddings (optional bridge to §7 & §11):**
  - [ ] Extract contextualized hidden-state representations of verbs from DictaBERT (averaged across corpus instances) and compare against static word2vec in §7.

---

### Phase 9: Personal Initiative / Research Extensions (§11)
*(Grading explicitly weights personal initiative beyond the core specification. Select 2–3 high-impact directions that naturally emerge from early results.)*

- [ ] **Initiative Idea A — Testing Talmy's Typological Shift Across 3,000 Years:** Empirically measure the evolution of Hebrew from *verb-framed* (BH) toward *satellite-framed* tendencies (MH) by tracking co-occurrence of manner-of-motion verbs with directional prepositions across all 5 historical corpora (directly testing Doron & Dubnov §7–8.1).
- [ ] **Initiative Idea B — Modern Hebrew Genre Stratification:** Compare locative alternation rates, preposition identity, and innovative alternating verbs across the 6 Modern Hebrew genres (formal: Knesset, Medical, News vs. literary vs. informal: Tapuz Forum, Blogs).
- [ ] **Initiative Idea C — Parser Domain-Shift Audit (BH vs. MH):** Manually evaluate a stratified sample of `dictabert-tiny-joint` parses across Biblical, Rabbinic, Medieval, and Modern Hebrew to quantify historical domain-shift error rates and assess their impact on downstream syntactic conclusions.
- [ ] **Initiative Idea D — Diachronic Semantic/Frame Trajectories of Key Verbs:** Case-study timeline of 10–15 iconic verbs (e.g., `מילא`, `שם`, `הסיר`, `נישל`, `זרק`, `שטף`, `כיסה`, `הריק/רוקן`) tracking their Frame A/B ratios and prepositions from Tanakh through Modern Hebrew.
- [ ] **Initiative Idea E — Contextualized DictaBERT vs. Static Word2Vec vs. LLM Classification:** Unified comparison of linguistic features, static embeddings, contextual transformer embeddings, and LLM prompting in Phase 7/8.

---

### Phase 10: Final Report & Submission Package (§9 & §10)

#### Final Summary Report (§9)
- [ ] **Section 1 — Introduction & Research Questions:** Motivation, problem statement, overview of methodology.
- [ ] **Section 2 — Literature Review:** Doron & Dubnov (2017) summary; 5 historical strata of Hebrew (with full scholarly citations); ML classification & evaluation metrics.
- [ ] **Section 3 — Corpora & Processing Pipeline:** Description of all 5 corpora + MH genres, preprocessing, DictaBERT parsing pipeline, and domain-shift notes.
- [ ] **Section 4 — Corpus Statistical Analysis (§4):** Comprehensive tables, figures, tree-depth interpretation, and diachronic/genre linguistic insights.
- [ ] **Section 5 — Empirical Evaluation of Doron & Dubnov (§5):** BH replication results, cross-period findings, Preposition Identity verification, and comparison to paper claims.
- [ ] **Section 6 — Scope Expansion (§6):** Classification of all corpus verbs and linguistic characterization of newly discovered alternating verbs.
- [ ] **Section 7 — Verb Classification Experiments (§7):** Feature engineering, 10-fold CV results across all feature sets & classifiers, word2vec comparison, error & feature-importance analysis.
- [ ] **Section 8 — LLM & AI Integration (§8):** Methodology, prompt designs, quantitative evaluation, and qualitative findings.
- [ ] **Section 9 — Personal Initiative (§11):** Additional research questions, findings, and insights.
- [ ] **Section 10 — Summary, Conclusions, Limitations & Future Work.**
- [ ] **References:** Complete, consistent academic bibliography.

#### Submission Package (§10)
- [ ] Final formatted report (PDF + source).
- [ ] Curated datasets & result tables (177-verb gold list, summary stats, frame extraction outputs, classifier datasets & metrics).
- [ ] Clean, commented, reproducible codebase (`src/`, `notebooks/`, `requirements.txt`, updated `README.md` with exact reproduction steps).
- [ ] Final sanity review against every item in `project.docx.pdf`.

---

## Key Technical Risks & Mitigations

| Risk / Challenge | Mitigation |
| :--- | :--- |
| **Frame A vs. Frame B surface syntactic identity** (`V + obj + obl[P]`) | Combine syntactic extraction with argument-type semantics (noun clustering / ontologies) + LLM semantic role disambiguation (§8), verified on a manually annotated gold set. |
| **DictaBERT parser domain shift on Biblical / Rabbinic / Medieval Hebrew** | Validate parses against Dicta's demos on sample verses; document systematic errors (e.g., waw-consecutive, object clitics, poetic word order) and handle clitic object suffixes explicitly. |
| **Large parsing runtime across 5 periods & 6 MH genres** | Use `dictabert-tiny-joint` (specifically designed for speed) with GPU batching, length sorting, and per-file checkpointing. |
| **Class imbalance & small sample size (177 verbs) in §7** | Use **10-fold Stratified CV**, report **Macro-F1** alongside Weighted-F1 & Accuracy, apply class weighting, and fit all feature transforms strictly inside CV folds. |
| **OOV / archaic verbs in Modern Hebrew word2vec** | Log OOV rate explicitly; compare Dicta word2vec against corpus-trained embeddings and/or contextual DictaBERT embeddings. |
| **Typo in spec §1.2 item 10** (*"לשון חכמים"* repeated under *"העברית המודרנית"*) | Cover **Modern Hebrew** morphology and syntax thoroughly (as intended by the heading). |

---

## Decision & Experiment Log

*Use this section to log key decisions, corpus sizes, experiment metrics, and unexpected findings as you work.*

| Date | Phase | Entry / Decision / Result |
| :--- | :---: | :--- |
| 2026-11-19 | Planning | Reviewed `project.docx.pdf` and `DoronDubnov_revised.pdf`; extracted all 6 resource URLs and created initial `PROJECT_PLAN.md`. |
| 2026-11-19 | Phase 0 | Completed repo scaffold, `.gitignore`, `requirements.txt`, `.venv` (Python 3.11.5, PyTorch 2.15.0+cpu, Transformers 4.57.6). Downloaded self-contained `dicta-il/dictabert-tiny-joint` + `BertForJointParsing` code to `models/dictabert-tiny-joint` (offline load: 0.45s). |
| 2026-11-19 | Phase 0 | Smoke test (`src/parsing/smoke_test.py`) benchmarked **~41.1 sent/s** on local CPU (6 threads, `batch_size=32`). Key schema & linguistic findings: (1) prepositions appear either as standalone `ADP`/`case` tokens (`מן הבור`) or as cliticized prefixes in `seg` + `morph.prefixes=['ADP']` (`במים` -> `seg=('ב','מים')`, `בו` -> `pos='PRON', pref=['ADP']`); (2) DictaBERT strips niqqud internally, which can cause BH domain-shift errors (e.g., `וּמִלֵּאתָ` misparsed as `ADJ` `מלאה`, and archaic `ויצף` getting `lex='[BLANK]'`); (3) keeping `do_ner=True` tags temporal adjuncts like `בשבת` as `TIMEX`, which will help filter non-locative `ב-` adjuncts in §5–§6. |
| 2026-11-19 | Phase 1 | Completed literature reviews (`report/literature_review_doron_dubnov.md`, `report/literature_review_background.md` with 34 verified scholarly references) and digitized Doron & Dubnov's full BH locative verb database via `src/locative/build_doron_dubnov_lexicon.py` -> `data/curated/doron_dubnov_177_verbs.csv` (178 rows: 96 A [38 Caus, 12 Int, 46 Simp], 45 A/B [7 Caus, 7 Int, 31 Simp], 37 B [3 Caus, 15 Int, 19 Simp], explicitly documenting the paper's fn. 33 erratum where `אסר` appears both in Ex. 33 as A/B and in fn. 33 under A-Simple, and adding Modern Hebrew plene lemma variants for Phase 5 matching). |
| 2026-11-19 | Phase 2 | Downloaded & extracted `corpora.rar` (478 MB / 404,294 files / 1.13 GB / ~186.5M words). Audit (`results/tables/phase2_raw_audit.json`) revealed critical encoding split (`utf-8-sig` for historical strata vs. `cp1255` for all 6 Modern Hebrew genres), 99 non-text `.log` files in `Modern/news`, repeated banner boilerplate in `tapuz`, and late commentaries bundled in `Hazal/Midrash` & `Medieval/Thought`. Built 16 clean Parquet shards in `data/processed/` via `src/corpora/preprocess.py` (323,977 sentences, 6.65M words: 100% of Tanakh [23,204 verses], Mishnah, Tosefta, and Rambam + deterministic `seed=42` stratified samples of larger sub-corpora; est. local CPU parse time ~2.2 hrs). |
