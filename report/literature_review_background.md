# Literature Review — Part 2: Historical Hebrew Strata, Linguistic Foundations & Machine Learning (§1.2)

> This document covers all general background topics required by Section 1.2 of [project.docx.pdf](../project.docx.pdf): morphology & syntax, the five historical periods of Hebrew (Biblical, Rabbinic, Medieval, Haskalah, and Modern), supervised classifiers, and classification evaluation metrics, with full scholarly references.

---

## 1. Morphology and Syntax Foundations

### 1.1 Morphology (מורפולוגיה)
Hebrew is a **non-concatenative (root-and-pattern) Semitic language** with rich inflectional and clitic morphology (Coffin & Bolozky 2005; Berman 1978):
- **Root (*shoresh*) and Template (*binyan* / *mishkal*):** Most verbs are built by interleaving a consonantal root (typically 3, occasionally 4 consonants) into one of seven verbal templates (*binyanim*):
  - **Simple (Pa'al / Qal)** and its middle/passive counterpart **Nif'al**
  - **Intensive (Pi'el)**, passive **Pu'al**, and middle/reflexive **Hitpa'el** (and Rabbinic **Nitpa'el**)
  - **Causative (Hif'il)** and passive **Huf'al**
  - As Doron (2003, 2008) and Doron & Dubnov (2017) demonstrate, *binyan* is not merely morphological — it systematically modulates argument structure (agency, causativity, voice), which directly correlates with locative verb class (`A`, `A/B`, `B`).
- **Lemma (ערך מילוני):** The canonical citation form of a word (for Hebrew verbs, traditionally 3rd person masculine singular past tense, e.g., `מילא`, `הסיר`).
- **Parts of Speech (POS / קטגוריה לקסיקלית):** Lexical categories (`VERB`, `NOUN`, `ADJ`, `ADV`, `ADP`, `PRON`, `PROPN`, `NUM`, `CCONJ`, `SCONJ`, `DET`, `AUX`, `PART`).
- **Inflectional Features (מאפייני הטיה):** Verbs inflect for tense/aspect, person, gender, and number; nouns and adjectives inflect for gender, number, and **state** (*absolute* / נפרד vs. *construct* / נסמך, forming *smikhut* noun chains).
- **Clitic Prefixes and Suffixes:** Orthographic words in Hebrew frequently fuse multiple morphemes:
  - **Proclitic prefixes (`מ ש ה ו כ ל ב`):** Prepositions (`ב-`, `ל-`, `כ-`, `מ-`), definite article (`ה-`), conjunction (`ו-`), and subordinator (`ש-`), which can stack (e.g., `ובבית` = `ו` + `ב` + `ה` + `בית`).
  - **Enclitic suffixes:** Possessive pronouns on nouns (`ספרי`, `ספרך`), pronominal complements on prepositions (`בו`, `ממנו`), and accusative object suffixes on verbs (`מצאתיו`, `מצאתיך`) — synthetic forms that are prevalent in Biblical Hebrew and largely replaced by analytic constructions (`של`, `את`) in Modern Hebrew.

### 1.2 Syntax and Dependency Parsing (תחביר ועץ תלויות)
**Dependency grammar** represents sentence syntax as a directed, labeled tree whose nodes are words/morphemes and whose directed edges (`head -> dependent`) are annotated with grammatical relations (Kübler, McDonald & Nivre 2009; Universal Dependencies — de Marneffe et al. 2021):
- **Core clause arguments:** `root` (main predicate), `nsubj` / `nsubj:pass` (nominal subject / passive subject), `obj` (direct object, marked by `case:acc` `את` when definite), `iobj` (indirect object).
- **Oblique complements & prepositional phrases:** `obl` (oblique nominal dependent on a verb, such as a locative PP `במים` or `מן הבור`), linked to standalone prepositions via `case` or carrying a cliticized `ADP` prefix in `seg`/`prefixes` (as verified in our Phase 0 DictaBERT inspection).
- **Subordination & modification:** `ccomp` / `xcomp` (clausal complements), `advcl` (adverbial clauses), `acl` / `acl:relcl` (adnominal/relative clauses), `conj` (coordination), `compound:smixut` (construct-state noun compounds).
- **Tree depth** (longest directed path from `root` to a leaf) reflects syntactic embedding and structural complexity (e.g., paratactic coordination chains vs. deeply nested hypotactic/subordinate clauses), a key diachronic indicator explored in §4.

---

## 2. Historical Strata of the Hebrew Language

Hebrew spans over three millennia of documented textual history, conventionally divided into five major strata that correspond directly to our project corpora (Sáenz-Badillos 1993; Khan 2013):

### 2.1 Biblical Hebrew (לשון המקרא)
**Period & Corpus:** ~1200–200 BCE; represented by the Tanakh (Early/Classical BH in the Pentateuch and Former Prophets; Late BH in Ezra–Nehemiah, Chronicles, Esther, Daniel, Ecclesiastes).

- **Morphological characteristics:**
  - **Aspectual/converted verbal system:** Prominent use of the *waw*-consecutive (*wayyiqtol* for narrative past, e.g., `וַיֹּאמֶר`, and *weqatal* for sequential future/modal), alongside *qatal* (perfective), *yiqtol* (imperfective), and *cohortative* / *jussive* modal forms (Joüon & Muraoka 2006; Waltke & O'Connor 1990).
  - **Synthetic pronominal affixation:** Frequent direct-object clitic suffixes attached directly to verbs (e.g., `וַיִּפְרְקֵנוּ`, `מְשַׁחְתִּיו`) and possessive suffixes on nouns, alongside extensive construct chains (*smikhut*).
  - **Directive *-he* (`הָ-`):** Locative/directional suffix attached to nouns (e.g., `יִזְרְעֶאלָה`, `אַרְצָה`) encoding Goal without a preposition.
  - **Binyan system:** Active *Pa'al*, *Pi'el*, *Hif'il*; internal passives (*Pu'al*, *Huf'al*, and vestigial *Qal* passive); *Nif'al* and *Hitpa'el* for middle/reflexive/passive.
- **Syntactic characteristics:**
  - **Verb-initial default word order (VSO):** Especially dominant in narrative *wayyiqtol* clauses (Joüon & Muraoka 2006; Holmstedt 2013).
  - **Parataxis over hypotaxis:** Clauses are heavily chained via coordinating `ו-` (*waw*) rather than deep clausal subordination; relativization uses `אֲשֶׁר` (rarely `שֶׁ-` in Late BH/northern dialects).
  - **Verb-framed motion typology:** Path/direction is lexicalized inside the verb (`העלה`, `הוריד`, `הוציא`), with very few manner-of-motion verbs and stative symmetric locative prepositions `ב-` and `מן` (Doron & Dubnov 2017).
  - **Differential object marking:** Definite direct objects typically take `אֶת` (though poetic texts often omit it).

**Key Sources:** Gesenius, Kautzsch & Cowley (1910); Waltke & O'Connor (1990); Sáenz-Badillos (1993, ch. 3–4); Joüon & Muraoka (2006); Khan (2013, *EHLL* entries on Classical & Late Biblical Hebrew).

---

### 2.2 Rabbinic / Mishnaic Hebrew (לשון חכמים / חז"ל)
**Period & Corpus:** ~200 BCE–500 CE (Tannaitic: Mishnah, Tosefta, Halakhic Midrashim; Amoraic: Aggadic Midrashim, Talmudic Hebrew).

- **Morphological characteristics:**
  - **Restructured tripartite tense system:** Complete disappearance of *waw*-consecutive (*wayyiqtol* / *weqatal*); reorganization into a clear tense system: *qatal* = Past, active participle (*benoni*) = Present/habitual, *yiqtol* = Future/modal, plus the periphrastic past habitual `הָיָה + participle` (Pérez Fernández 1997; Segal 1927).
  - **Binyan innovations:** Emergence of **Nitpa'el** (`נִתְפַּעֵל`, blending *Nif'al* and *Hitpa'el*) for reflexive/passive; decline of internal *Pu'al* (except participles); productive verbal nouns (`קְטִילָה`, `קִטּוּל`, `הַקְטָלָה`) and *Nif'al*/*Pi'el* shifts.
  - **Pronominal & lexical shifts:** 1pl pronoun `אָנוּ` (replacing `אֲנַחְנוּ`), feminine demonstrative `זוֹ`, 3mp suffix `-ן` alongside `-ם`, and substantial **Aramaic** (and Greek/Latin) lexical & morphological influence (Bar-Asher 2013; Sáenz-Badillos 1993).
- **Syntactic characteristics:**
  - **Shift from VSO toward SVO:** Particularly in participial and legal/casuistic clauses (`הממלא מים מן הבור...`), reducing verb-initial dominance.
  - **Analytic genitive `שֶׁל`:** Replaces or supplements synthetic construct chains and possessive suffixes (`בֵּיתוֹ שֶׁל...`, `הַבַּיִת שֶׁל...`).
  - **Subordinator `שֶׁ-`:** Largely replaces Biblical `אֲשֶׁר` for relative and complement clauses, accompanied by richer hypotactic legal conditionals (`אִם`, `כֵּיוָן שֶׁ-`, `אַף עַל פִּי שֶׁ-`).
  - **Infinitive usage:** Replacement of BH infinitive absolute and bare infinitive construct with `לְ- + infinitive` (`לִקְטוֹל`) and `שֶׁ- + finite verb`.

**Key Sources:** Segal (1927); Sáenz-Badillos (1993, ch. 5); Pérez Fernández (1997); Bar-Asher (2013, *EHLL* "Rabbinic Hebrew"); Breuer (2013, *EHLL* "Rabbinic Hebrew: Syntax").

---

### 2.3 Medieval Hebrew (לשון ימי הביניים)
**Period & Corpus:** ~600–1750 CE — a non-vernacular, learned written language comprising multiple distinct stylistic registers, three of which appear directly in our corpus: (a) **Maimonides' *Mishneh Torah*** (clear, classicized Mishnaic legal prose), (b) **Philosophical works (*ספרי מחשבה*)** (largely shaped by the 12th–13th c. Tibbonide translations from Judeo-Arabic, e.g., Judah & Samuel ibn Tibbon), and (c) **Ethical literature (*ספרי מוסר*)**.

- **Morphological characteristics:**
  - **Arabic-inspired derivational productivity (Tibbonide Hebrew):** Massive expansion of abstract nouns with `-וּת` (`אֵיכוּת`, `כַּמּוּת`, `מַהוּת`, `אַחְדוּת`, `מְצִיאוּת`), denominal relational adjectives in `-י` (`טִבְעִי`, `רוּחָנִי`, `שִׂכְלִי`), and calqued technical terminology (Goshen-Gottstein 2006; Sáenz-Badillos 1993).
  - **Hybrid morphology:** Conscious synthesis of Rabbinic (*Mishneh Torah*) and Biblical morphology, with productive *Hitpa'el* / *Nitpa'el* and passive participles used as nominalized concepts.
  - **Frequent nominalization & infinitive/verbal-noun usage:** Preference for abstract verbal nouns (`הַשָּׂגָה`, `הַנָּחָה`, `הַעְתָּקָה`) in philosophical discourse.
- **Syntactic characteristics:**
  - **High syntactic complexity & hypotaxis:** Especially in Tibbonide philosophical prose, long multi-clause periodic sentences with heavy logical subordination (`מִפְּנֵי שֶׁ-`, `לְפִי שֶׁ-`, `כַּאֲשֶׁר`, `אִלּוּ`, `עַל כֵּן`), leading to substantially greater dependency tree depth and sentence length than BH.
  - **Arabic syntactic calques:** Copular/existential structures, conditional clause patterns, topicalized *casus pendens* constructions, and frequent use of resumptive pronouns and impersonal passives (Goshen-Gottstein 2006; Rabin 2000).
  - **Stylistic divergence across sub-corpora:** Rambam's *Mishneh Torah* preserves concise, lucid Mishnaic syntax (`SVO`/participial legal rules), whereas philosophical and ethical texts show heavier nominal density and abstract argument structures.

**Key Sources:** Sáenz-Badillos (1993, ch. 6–7); Rabin (2000); Goshen-Gottstein (2006); Goldenberg (2013) & Hary / Morag entries in Khan (2013, *EHLL* "Medieval Hebrew").

---

### 2.4 Haskalah / Enlightenment Hebrew (לשון ההשכלה)
**Period & Corpus:** Late 18th to late 19th century (~1780–1880s); Jewish Enlightenment literature (novels, essays, periodicals, satires) in Central and Eastern Europe.

- **Morphological characteristics:**
  - **Early Haskalah — Biblical purism (*melitzah*):** Deliberate rejection of Rabbinic and Medieval forms in favor of Biblical lexicon and morphology, including revival of *waw*-consecutive (*wayyiqtol*), Biblical pronouns (`אָנֹכִי`, `אֲנַחְנוּ`), and pronominal object suffixes on verbs (Sáenz-Badillos 1993; Kahn 2009).
  - **Late Haskalah — Synthetic transition:** Writers such as Mendele Mocher Sforim (S. Y. Abramowitz) broke with strict purism, blending Biblical, Rabbinic, and Medieval morphology (reintroducing Rabbinic `שֶׁ-`, `שֶׁל`, participial present tense, and abstract `-וּת` nouns) to achieve expressive narrative realism (Kahn 2009; Patterson 1988).
  - **Mixed verbal system:** Coexistence of *wayyiqtol* with Rabbinic *qatal* for narrative past, and active participles functioning as present tense (Kahn 2009).
- **Syntactic characteristics:**
  - **European (Yiddish, German, Russian) syntactic calques beneath Biblical veneer:** Despite Biblical vocabulary, sentence architecture often mirrors European literary prose — longer sentences, complex relative/subordinate clauses, indirect speech, and increased SVO word order alongside rhetorical VSO inversion (Kahn 2009, 2013).
  - **Analytic and periphrastic constructions:** Gradual expansion of compound prepositions, discourse connectors, and literary register devices bridging classical Hebrew and nascent Modern Hebrew.

**Key Sources:** Patterson (1988); Sáenz-Badillos (1993, ch. 8); Kahn (2009, *The Verbal System in Late Enlightenment Hebrew*); Kahn (2013, *EHLL* "Maskilic Hebrew").

---

### 2.5 Modern Hebrew (העברית המודרנית)
**Period & Corpus:** Late 19th century (revival as a spoken vernacular) to present; represented in our corpus across **six distinct genres** spanning formal institutional/technical prose (Knesset protocols, Medical texts, News), literary prose (Original & Translated Literature), and informal computer-mediated communication (Tapuz Forum, Blogs).

- **Morphological characteristics:**
  - **Productive root-and-pattern & linear derivation:** Fully active 7-binyan verbal system (with *Pu'al* and *Huf'al* largely restricted to formal/written registers, while *Nif'al* and *Hitpa'el* remain productive in speech), quadriliteral roots (`טִלְפֵּן`, `פִּרְסֵם`, `שִׁכְפֵּל`), acronyms, blends, and foreign loanwords (Coffin & Bolozky 2005; Berman 1978).
  - **Shift from synthetic to analytic inflection:** Verbal accusative suffixes (`מצאתיו`) and bound possessive suffixes (`ספרי`) are largely replaced in everyday usage by analytic `את + pronoun` (`מצאתי אותו`) and `של + pronoun` (`הספר שלי`), surviving mainly in high literary/formal registers (Glinert 1989).
  - **Tense system:** Strict Past (*qatal*) / Present (*benoni* participle) / Future (*yiqtol*) tripartite system; no *waw*-consecutive.
- **Syntactic characteristics:**
  - **SVO dominant word order** (with flexible discourse-driven fronting and VS in presentational/existential/formal journalistic clauses).
  - **Analytic prepositions & subordinating syntax:** Heavy use of `ש-` for complement/relative clauses, rich compound prepositions (`על ידי`, `מתחת ל-`, `מחוץ ל-`), and obligatory `את` before definite direct objects.
  - **Typological shift & locative alternation:** As Doron & Dubnov (2017, §8) show, MH retains BH **Preposition Identity** (`ב-`, `מן/מ-`) and the `A/(B)` vs. `B` class boundary, while acquiring **satellite-framed** characteristics — notably combining manner-of-motion verbs with directional PPs (`רכב אל מתחת לגשר`) and innovating many alternating surface-contact verbs (`שפשף`, `ניגב`, `קרצף`, `הבריש`, `טאטא`).
  - **Strong register/genre stratification:** Formal genres (Knesset, Medical, News) exhibit longer sentences, higher nominalization/construct-chain density, and more passive forms, whereas informal genres (Tapuz Forum, Blogs) exhibit shorter clauses, colloquial lexicon, ellipses, and innovative verbal usages.

**Key Sources:** Berman (1978, 1997); Glinert (1989); Sáenz-Badillos (1993, ch. 8); Coffin & Bolozky (2005); Khan (2013, *EHLL* "Modern Hebrew"); Doron & Dubnov (2017, §8).

---

## 3. Supervised Classifiers and Evaluation Metrics

### 3.1 Supervised Classification Algorithms (§7)
In Phase 7, we map each verb $v$ to a fixed-dimensional feature vector $\mathbf{x}_v \in \mathbb{R}^d$ (lexical, morphological, syntactic, combined, or word2vec embeddings) and predict its discrete linguistic category $y_v \in \{\text{A}, \text{A/B}, \text{B}\}$. Comparing diverse model families tests whether class boundaries are linear or nonlinear in feature space (Hastie, Tibshirani & Friedman 2009; Bishop 2006; Jurafsky & Martin 2024):

| Classifier Family | Core Principle | Strengths for Our Task | Key Considerations |
| :--- | :--- | :--- | :--- |
| **Logistic Regression** (multinomial, L2) | Linear decision boundaries modeling $P(y \mid \mathbf{x})$ via softmax + regularization | Strong baseline on high-dimensional sparse lexical/syntactic features; directly interpretable weights | Requires feature scaling; cannot capture feature interactions without explicit engineering |
| **Support Vector Machine (SVM)** | Maximizes margin between classes (Linear or RBF kernel) | Excels in small-$N$, high-$d$ regimes (e.g., 177 verbs with TF-IDF or 300-d word2vec vectors) | Sensitive to regularization $C$, kernel bandwidth $\gamma$, and feature scaling |
| **Random Forest** | Ensemble of bagged decision trees with random feature subsampling | Captures nonlinear feature interactions (e.g., *binyan* × preposition) without scaling; provides feature importances | Can underperform linear models on very high-dimensional sparse text vectors |
| **Gradient Boosted Trees** (e.g., `HistGradientBoosting` / XGBoost) | Sequential additive trees fitting residual errors | State-of-the-art on structured tabular features (morphological + syntactic profiles) | Needs careful regularization/depth limits on small datasets ($N \approx 177$) to avoid overfitting |
| **Multi-Layer Perceptron (MLP)** | Feedforward neural network with nonlinear hidden layers | Effective on dense continuous embeddings (word2vec / DictaBERT embeddings) | Prone to overfitting on small $N$; requires strong L2 weight decay / early stopping |

### 3.2 10-Fold Stratified Cross-Validation
Because the Doron & Dubnov dataset is compact ($N = 177$) and **class-imbalanced** (95 A = 53.7%, 45 A/B = 25.4%, 37 B = 20.9%), **10-fold stratified cross-validation** is essential (Kohavi 1995; Hastie et al. 2009):
- The dataset is partitioned into 10 folds preserving the exact class proportions in every fold.
- In each iteration $k \in \{1, \dots, 10\}$, the model trains on 9 folds and evaluates on the held-out fold $k$.
- **Leakage prevention:** All unsupervised preprocessing steps (TF-IDF fitting, SVD/PCA dimensionality reduction, `StandardScaler`, feature selection) must be wrapped in a `scikit-learn` `Pipeline` so they are fit *exclusively* on the 9 training folds of each split.

### 3.3 Classification Evaluation Metrics
For each class $c$, let $TP_c$, $FP_c$, $FN_c$, and $TN_c$ denote true positives, false positives, false negatives, and true negatives (Powers 2011; Sokolova & Lapalme 2009; Jurafsky & Martin 2024):

1. **Accuracy:** Overall proportion of correctly classified instances:
   $$\text{Accuracy} = \frac{\sum_c TP_c}{N}$$
   *Caveat:* Under class imbalance (53.7% Class A), a trivial majority-class classifier achieves 53.7% accuracy without learning anything — hence Accuracy alone is insufficient.

2. **Precision (per class $c$):** Fraction of instances predicted as class $c$ that truly belong to class $c$:
   $$\text{Precision}_c = \frac{TP_c}{TP_c + FP_c}$$

3. **Recall / Sensitivity (per class $c$):** Fraction of true class $c$ instances correctly recovered by the classifier:
   $$\text{Recall}_c = \frac{TP_c}{TP_c + FN_c}$$

4. **F-Measure ($F_1$ score, per class $c$):** Harmonic mean of Precision and Recall (penalizing extreme trade-offs between the two):
   $$F_{1,c} = \frac{2 \cdot \text{Precision}_c \cdot \text{Recall}_c}{\text{Precision}_c + \text{Recall}_c}$$

5. **Multi-Class Aggregation (Macro vs. Weighted vs. Micro):**
   - **Macro-averaged Precision / Recall / $F_1$:** Unweighted arithmetic mean across all classes $C$ — treats minority classes (`A/B`, `B`) equally to majority class `A`, making **Macro-$F_1$** our primary metric for imbalanced verb classification.
   - **Weighted-averaged Precision / Recall / $F_1$:** Class scores weighted by class support $N_c / N$.
   - **Micro-averaged $F_1$:** Aggregates global $TP, FP, FN$ across classes (in single-label multi-class classification, Micro-Precision = Micro-Recall = Micro-$F_1$ = Accuracy).

---

## 4. Bibliography

- Bar-Asher, Moshe. 2013. "Rabbinic Hebrew." In *Encyclopedia of Hebrew Language and Linguistics*, edited by Geoffrey Khan, Vol. 3, 315–323. Leiden: Brill.
- Berman, Ruth A. 1978. *Modern Hebrew Structure*. Tel Aviv: University Publishing Projects.
- Berman, Ruth A. 1997. "Modern Hebrew." In *The Semitic Languages*, edited by Robert Hetzron, 312–333. London: Routledge.
- Bishop, Christopher M. 2006. *Pattern Recognition and Machine Learning*. New York: Springer.
- Breuer, Yochanan. 2013. "Rabbinic Hebrew: Syntax." In *Encyclopedia of Hebrew Language and Linguistics*, edited by Geoffrey Khan, Vol. 3. Leiden: Brill.
- Clark, Eve V., and Herbert H. Clark. 1979. "When nouns surface as verbs." *Language* 55(4): 767–811.
- Coffin, Edna Amir, and Shmuel Bolozky. 2005. *A Reference Grammar of Modern Hebrew*. Cambridge: Cambridge University Press.
- de Marneffe, Marie-Catherine, Christopher D. Manning, Joakim Nivre, and Daniel Zeman. 2021. "Universal Dependencies." *Computational Linguistics* 47(2): 255–308.
- Doron, Edit. 2003. "Agency and Voice: The semantics of the Semitic templates." *Natural Language Semantics* 11(1): 1–67.
- Doron, Edit. 2008. "The contribution of the template to verb meaning" [Hebrew]. In *Modern Linguistics of Hebrew*, edited by Galia Hatav, 57–88. Jerusalem: Magnes Press.
- Doron, Edit, and Keren Dubnov. 2017. "The locative alternation in Biblical (and Modern) Hebrew." In *Advances in Biblical Hebrew Linguistics: Data, Methods and Analyses*, edited by Adina Moshavi and Tania Notarius, 321–360. Winona Lake, IN: Eisenbrauns.
- Gesenius, Wilhelm, Emil Kautzsch, and Arthur E. Cowley. 1910. *Gesenius' Hebrew Grammar*. 2nd English ed. Oxford: Clarendon Press.
- Glinert, Lewis. 1989. *The Grammar of Modern Hebrew*. Cambridge: Cambridge University Press.
- Goshen-Gottstein, Moshe H. 2006. *Syntax and Vocabulary of Mediaeval Hebrew as Influenced by Arabic* [Hebrew], revised by Shraga Assif and Uri Melammed. Jerusalem: Ben-Zvi Institute.
- Hastie, Trevor, Robert Tibshirani, and Jerome Friedman. 2009. *The Elements of Statistical Learning: Data Mining, Inference, and Prediction*. 2nd ed. New York: Springer.
- Holmstedt, Robert D. 2013. "Word Order: Biblical Hebrew." In *Encyclopedia of Hebrew Language and Linguistics*, edited by Geoffrey Khan, Vol. 3. Leiden: Brill.
- Joüon, Paul, and Takamitsu Muraoka. 2006. *A Grammar of Biblical Hebrew*. 2nd revised ed. (*Subsidia Biblica* 27). Rome: Editrice Pontificio Istituto Biblico.
- Jurafsky, Daniel, and James H. Martin. 2024. *Speech and Language Processing*. 3rd ed. draft. Stanford University.
- Kahn, Lily. 2009. *The Verbal System in Late Enlightenment Hebrew*. Leiden / Boston: Brill.
- Kahn, Lily. 2013. "Maskilic Hebrew." In *Encyclopedia of Hebrew Language and Linguistics*, edited by Geoffrey Khan, Vol. 2. Leiden: Brill.
- Khan, Geoffrey (Ed.-in-Chief). 2013. *Encyclopedia of Hebrew Language and Linguistics* (4 vols.). Leiden: Brill.
- Kohavi, Ron. 1995. "A study of cross-validation and bootstrap for accuracy estimation and model selection." *Proceedings of IJCAI-95*, 1137–1143.
- Kübler, Sandra, Ryan McDonald, and Joakim Nivre. 2009. *Dependency Parsing*. Synthesis Lectures on Human Language Technologies. San Rafael, CA: Morgan & Claypool.
- Patterson, David. 1988. *A Phoenix in Fetters: Studies in Nineteenth and Early Twentieth Century Hebrew Fiction*. Savage, MD: Rowman & Littlefield.
- Pérez Fernández, Miguel. 1997. *An Introductory Grammar of Rabbinic Hebrew* (trans. John F. Elwolde). Leiden: Brill.
- Powers, David M. W. 2011. "Evaluation: From Precision, Recall and F-Measure to ROC, Informedness, Markedness & Correlation." *Journal of Machine Learning Technologies* 2(1): 37–63.
- Rabin, Chaim. 2000. *The Development of the Syntax of Post-Biblical Hebrew*. Leiden: Brill.
- Rappaport, Malka, and Beth Levin. 1988. "What to do with theta-roles." In *Syntax and Semantics 21: Thematic Relations*, edited by Wendy Wilkins, 7–36. New York: Academic Press.
- Sáenz-Badillos, Ángel. 1993. *A History of the Hebrew Language* (trans. John Elwolde). Cambridge: Cambridge University Press.
- Segal, M. H. 1927. *A Grammar of Mishnaic Hebrew*. Oxford: Clarendon Press.
- Sokolova, Marina, and Guy Lapalme. 2009. "A systematic analysis of performance measures for classification tasks." *Information Processing & Management* 45(4): 427–437.
- Talmy, Leonard. 1985. "Lexicalization patterns: Semantic structure in lexical form." In *Language Typology and Syntactic Description*, Vol. 3, edited by Timothy Shopen, 57–149. Cambridge: Cambridge University Press.
- Talmy, Leonard. 2000. *Toward a Cognitive Semantics*. Cambridge, MA: MIT Press.
- Waltke, Bruce K., and M. O'Connor. 1990. *An Introduction to Biblical Hebrew Syntax*. Winona Lake, IN: Eisenbrauns.
