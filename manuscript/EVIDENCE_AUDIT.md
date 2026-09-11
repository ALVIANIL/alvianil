# Strict Evidence Audit of the Uploaded Manuscript

Audit performed before the manuscript was redesigned. Verification channel: publisher and
indexed records retrieved through web search. **The Crossref REST API (`api.crossref.org`) is
blocked by this environment's network egress policy**, as are `doi.org`, OpenAlex, Europe PMC,
Semantic Scholar, PubMed and all publisher domains, so DOI validation was performed against
publisher landing pages and indexed records surfaced through search rather than through a
Crossref API call. Every record reported below as verified was corroborated against at least
one of: the publisher's article page, PubMed/PMC, the journal's own listing, or an
institutional repository copy.

Verdict scale: **Supported** / **Partially supported** / **Unsupported** / **Contradicted** /
**Unverifiable**.

---

## 1. Fabricated or unsupported numerical claims

These claims were carried through the abstract, narrative, tables and figures of the uploaded
manuscript. None survived verification. All were removed.

### A1. "Combining EEG with GSR was 86.6% accurate versus 77.1% using EEG alone"
Cited as **[11]** in Section 1.3 and as **[37]** in Sections 2.3 and 4.3.1; also Table 6 row
"1D-CNN-LSTM, EEG+GSR, 86.60".

* **Verdict: Unsupported, plus a citation mismatch.**
* [11] = Dalmeida & Masala, *Sensors* 2021;21:2873, an HRV-feature study. It contains no
  EEG/GSR fusion experiment. It is also a 2021 paper, outside the 2022 to 2026 window.
* [37] = Kim H, Song S, Cho BH, Jang DP. *PLOS ONE* 2024;19:e0305864. **Verified actual
  results:** AUROC 0.954 ± 0.018 (multiple-column ResNet-50, EEG+GSR); 0.944 ± 0.027 (GSR,
  ResNet-152); 0.886 ± 0.069 (EEG, Vision Transformer); n = 30. The metric is AUROC, not
  accuracy, and the values 86.6 and 77.1 do not appear.
* **Action:** claim removed. The verified AUROC triple is used instead, and yields a
  within-study fusion gain of +1.00 pp over the best unimodal channel, not +9.5.

### A2. "Adding wearable physiological data to facial action units and gaze gave a 12% improvement over vision-only models"; "73% multimodal accuracy"
Cited as **[26]** in Sections 1.3, 2.3, 4.1.3, 4.1.4 and 4.3.2.

* **Verdict: Unsupported, and the direction of the authors' own conclusion is reversed.**
* [26] = Awada M, Becerik-Gerber B, Lucas GM, Roll SC. *PLOS ONE* 2024;19:e0296468.
  **Verified actual results:** XGBoost reached 82.78% combining physiological and behavioral
  features versus 79.55% using the physiological set alone, a difference of 3.23 pp. The
  authors state that this ~3% difference indicates physiological data alone may be adequate.
* There is no vision-only baseline, no 73% figure and no 12% gain in the source.
* **Action:** claim removed. The verified +3.23 pp contrast is used, together with the
  authors' own conclusion.

### A3. "38.6% better personalized than participant-exclusive generalized models (95.5% vs. 56.9%)"
Cited as **[33]**; drives the abstract's "3.11% to 38.6%" range, Table 5's personalized row
(mean 26.8, max 38.6) and Figures 6, 9 and 10 of the uploaded manuscript.

* **Verdict: Unsupported. Both endpoint values are wrong.**
* [33] = Li J, Washington P. *JMIR AI* 2024;3:e52171. **Verified actual results** for
  three-class classification: personalized 95.06% accuracy, F1 91.71; subject-inclusive
  generalized 66.95%, F1 42.50; subject-exclusive generalized 67.65%, F1 43.05.
* The true personalization gap is 27.41 pp of accuracy (not 38.6) and 48.66 pp of F1.
* **Action:** corrected values used. This is the single largest verified effect in the
  redesigned manuscript and is reported as 27.41 pp / 48.66 pp.

### A4. "CapsNet 94.52% versus SVM 84.3% on WESAD, a 10.22% difference"
Cited as **[61]**; Table 6 rows "SVM (Baseline) 84.30" and the Figure 8 anchor.

* **Verdict: Unsupported.**
* [61] = Khayyat M, Munshi RM, Alabduallah B, et al. *PLOS ONE* 2024;19:e0310776.
  **Verified actual results:** CapsNet reached 96.76% on WESAD and 92.76% on SWELL multiclass;
  98.52% (SWELL) and 99.82% (WESAD) for binary classification.
* Neither 94.52 nor 84.30 appears. The SVM baseline anchoring the manuscript's central
  "progress" narrative does not exist in the cited source.
* **Action:** removed; verified values used, which instead support a dataset-transfer contrast
  (WESAD 96.76 vs SWELL-KW 92.76 = 4.00 pp) and a task-granularity contrast (99.82 vs
  96.76 = 3.06 pp).

### A5. "SADDNet with 98.11% on WESAD (5.86% over baseline CNN)"
Cited as **[47]**; Table 6.

* **Verdict: Unsupported.**
* [47] = Ali MS, Motin MA, Bipro SS, Kabir S, Syfullah MK, Kumar DK. *IEEE Sens J*
  2026;26:6293–301. **Verified actual results:** 92.25% accuracy, 94.91% F1, 0.895 AUC under
  **subject-independent leave-one-subject-out** validation on CATSA (50 participants) and
  WESAD (15 participants).
* **Action:** corrected to 92.25% LOSO. Notably the source is one of the few studies that
  states its protocol, which the redesigned manuscript uses as evidence.

### A6. "Fernandez et al. found LightGBM (91.5%) was 4.2% better than CNN on 19-channel student EEG"
Cited as **[30]**; Table 4 EEG row.

* **Verdict: Partially supported.** LightGBM is confirmed as the best model, but the verified
  reported figure is **86.24% in intersubject analysis** for three-class classification
  (relax/neutral/stress). The 91.5% and 4.2% figures were not corroborated.
* **Action:** corrected to 86.24% and used as a subject-independent data point.

### A7. "Abdul Kader et al. compared Naive Bayes and LDA on EEG and GSR, where NB achieved 81.3% on GSR and 80.5% on EEG"
Cited as **[75]**.

* **Verdict: Unsupported.**
* [75] = Abdul Kader L, Al-Shargie F, Tariq U, Al-Nashash H. *Sensors* 2024;24:5373.
  **Verified actual results:** maximum accuracy **70.3% using EEG alone** and **84.6% using
  fused EEG and GSR**, two stress levels, n = 20.
* **Action:** corrected. This became the largest verified within-study fusion gain in the
  redesigned manuscript (+14.30 pp).

### A8. Table 5, "Closed-Loop, mean gain 12.0 pp"
Cited as **[38]**.

* **Verdict: Unsupported / derived without basis.** The manuscript's own body text describes
  this study in terms of a PPG-to-ECG pulse-rate correlation of r = 0.871, not a 12 pp
  accuracy gain. A correlation coefficient cannot be converted into a percentage-point
  performance gain.
* **Action:** the row was removed. [38] (Rahman FN et al., *Biosens Bioelectron*
  2026;301:118461) is retained as a narrative citation for closed-loop architecture only.

### A9. Abstract, "performance increments ranging from 3.11% to 38.6%"
* **Verdict: Unsupported at both endpoints.** The upper bound derives from A3 (fabricated).
  The lower bound, 3.11% attributed to [45], could not be corroborated; the retrievable record
  for that research group describes a differently titled paper and no 94.67%/3.11% pair was
  recoverable.
* **Action:** replaced with the verified within-study range of +1.00 to +14.30 pp
  (median +4.67 pp, k = 4).

---

## 2. Claims that did verify

Reported for completeness; these were retained.

| Manuscript claim | Source | Verdict |
|---|---|---|
| SELF-CARE 94.12% (2-class) / 86.34% (3-class) on WESAD | Rashid N, Mortlock T, Al Faruque MA. *IEEE Internet Things J* 2023;10:14114–27 | **Supported** (energy efficiency 2.2× / 2.7× also confirmed) |
| ReTeNet 98.23%, AUC 0.9953 on WESAD | Ali MS, Motin MA, Kabir S. *IEEE Signal Process Lett* 2025;32:3635–9 | **Supported** (F1 97.58 also confirmed) |
| ViT on in-ear PPG, 97.78% accuracy, F1 0.9779 | Barki H, Nkenyereye L, Chung W-Y. *IEEE Sens J* 2025;25:4015–27 | **Supported** (n = 15) |
| rPPG facial video, ~94% stress state / ~84% stress level | Xu J, Song C, Yue Z, Ding S. *IEEE J Biomed Health Inform* 2024;28:5335–46 | **Supported** (94.33% / 83.83%) |
| CAFS 90.98% accuracy, 94.37% energy reduction | Momeni N, Arza Valdes A, Rodrigues J, Sandi C, Atienza D. *IEEE Trans Biomed Eng* 2022;69:1072–84 | **Supported** |
| F1 falls 0.84 (lab) to 0.71 (real life) | Toshnazarov K et al. *IEEE Internet Things J* 2024;11:21527–45 | **Supported** (n = 26 lab, 18 field) |
| XGBoost 96.17% on 200-student ECG/GSR/temperature data | Gedam S, Dutta S, Jha R. *Sci Rep* 2025;15:20610 | **Supported** |
| XGBoost 93% stress vs rest, 91% exercise type | Hongn A et al. *Sci Data* 2025;12:520 | **Supported** (n = 36/30/31) |
| Vos et al. show better cross-dataset generalization | Vos G, Trinh K, Sarnyai Z, Rahimi Azghadi M. *J Biomed Inform* 2023;148:104556 | **Supported** (ensemble +25% over singular models; data and code public) |

---

## 3. Internal contradictions with the manuscript's own protocol

1. **Preprints and conference papers were included despite being excluded by Table 2.**
   [62] medRxiv preprint (10.1101/2022.03.03.22271859); [81] Research Square preprint
   (10.21203/rs.3.rs-5469584/v1); [98] ACM DAC conference paper (10.1145/3649329.3663513).
2. **Window violation.** The abstract claimed 2021 to 2026 while citing [11] and [57] from
   2021; the new window is 2022 to 2026 and both are now excluded.
3. **Corpus arithmetic never reconciled.** The abstract claimed 75 included studies while the
   reference list contained 117 entries, with no separation between included studies and
   background citations.
4. **Duplicate record.** Entry [23] (IEEE-style) and entry [89] (Vancouver-style) are the same
   study, Xiong Q, Gui L, Shu C, *Sci Rep* 2026;16:9317. That study is real and was verified;
   the duplication was a formatting artifact.
5. **Search yields not reproducible.** Table 1 reported per-database counts labelled
   "Estimated Initial Results" summing to 5,214, and Section 3.3 reported a precise PRISMA
   cascade (2,263 duplicates, 1,823 title/abstract exclusions, 237 inaccessible full texts,
   252 full-text exclusions) derived from those estimates. Estimated counts cannot support an
   exact PRISMA flow. **Action:** the redesigned manuscript reports only counts that can be
   reproduced from the actual record set, and its Table 1 reports real publisher-level
   screening yield instead.

---

## 4. Topical relevance failures

Forty-one of 116 records report no stress, attention, drowsiness or cognitive-load outcome and
were excluded. They are real papers, correctly cited, but they do not bear on the review's
question and their presence inflated apparent coverage. Examples: face-touch monitoring [15];
garment ECG for atrial fibrillation [20]; SVM sports rehabilitation [23]/[89]; geometry of
raised islands on flexible substrates [44]; exertional heat stroke [46]; loss-of-pulse
detection [60]; MIMO skin-implantable antenna [63]; sports health monitoring [66], [97];
cardiac rhythm disorders [69]; Alzheimer's detection [71]; hydrogel e-skin [77]; liquid-metal
boxing training [78]; thermoelectric foam [80]; atrial fibrillation wristband [83];
implantable ECG [88]; human activity recognition [90]; pressure sensors [93]; speech
recognition [94]; sleep staging [95]; nocturnal seizures [96]; blood glucose [100];
fetal movement [106]; end-of-life care [111]; tissue hardness [112]; cortisol aptananosensor
in artificial cerebrospinal fluid [113]; **oxidative** stress in exhaled breath [114], which
is chemical rather than psychological stress; device prognostics [116].

A further 10 records report no quantitative model evaluation (study protocols [59], [117],
narrative reviews [27], [40], technology-acceptance studies [9], [107], [110], intervention
trials [64], [65], and a perspective piece [68]).

---

## 5. Figures and tables of the uploaded manuscript

| Element | Status |
|---|---|
| Table 1 (search yields) | Unverifiable; counts self-described as estimates. Replaced. |
| Table 3 (MMAT quality scores for 75 studies) | Unverifiable; per-item Yes/No judgements for 75 studies cannot be reconstructed from the retrievable record. Replaced by a reporting-recovery table whose every cell is traceable. |
| Table 4 (best/median/lowest accuracy by modality) | Unsupported. Cells drew on off-topic sources: the PPG row's "99.86 (Deep CNN)" cites [69], a cardiac-rhythm study; the accelerometer row cites [66], [89], [90], none of which report a stress or attention outcome. Replaced. |
| Table 5 (fusion strategy effectiveness) | Unsupported. Mean/min/max gains rest on A1, A2, A3, A8. Replaced by within-study contrasts only. |
| Table 6 (deep learning benchmarks) | Partially supported. Rows for [58], [50], [43] verified; rows for [61], [37], [47], [11] contradicted. Replaced. |
| Table 7 (challenges) | Partially supported; retained only where a verified magnitude exists. |
| Figures 5 to 11 | All derived from Tables 4 to 6 and therefore inherit the above defects. All regenerated from the verified evidence base. |

---

## 6. Evidence trail for the redesigned manuscript

Every number in the redesigned manuscript traces to a machine-readable record:

* `data/corpus.csv` — all 116 screened records with the include/exclude decision, exclusion
  reason code and application area.
* `data/evidence.py` — the 34 corroborated outcome records, 4 within-study fusion contrasts,
  10 within-study evaluation contrasts, the corroboration list and the reporting-recovery
  coding. Each entry carries its source reference number.
* `src/make_tables.py` — generates Tables 1, 3, 4, 5 and 6 directly from those records; no
  table value is typed by hand.
* `src/make_figures.py` — generates Figures 3 to 10 from the same records.
* `src/make_bib.py` — emits the reference list in first-citation order from the verified
  bibliographic strings.

Corroboration outcome across the 60 included studies: **28 (46.7%)** yielded an independently
corroborable headline outcome. Reporting items recovered: headline metric 28/60 (46.7%),
evaluation cohort size 18/60 (30.0%), public benchmark 14/60 (23.3%), validation protocol
8/60 (13.3%), variance or confidence interval 3/60 (5.0%).

## 7. Residual limitations of this audit

1. Crossref, doi.org, OpenAlex, Europe PMC and all publisher domains are blocked by the
   network policy of this environment. DOI and metadata validation therefore relied on
   publisher landing pages and indexed records surfaced through search. Before submission,
   the reference list should be passed through a Crossref DOI check on an unrestricted
   network; no discrepancy is expected, but the check should be run.
2. Full texts could not be retrieved. Where a headline outcome was not recoverable from the
   openly retrievable record, the study contributes no number to the synthesis. Some of those
   32 studies almost certainly report their protocol and variance in the full text.
3. Two reference records have residual uncertainty in volume or article number that could not
   be cross-checked against a second independent source: [34] Bello-Orgaz et al. (*Biomed
   Signal Process Control* 2026;117:109683) and [45] Pavan et al. (*IEEE Sens Lett* 2025).
   Both are cited in narrative text only and neither contributes a number.
