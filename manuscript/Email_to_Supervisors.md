**Subject:** Revised manuscript for resubmission to *Biomedical Signal Processing and Control* — substantially restructured, with completed PRISMA 2020 checklist — requesting your feedback

Dear Sir/Madam, and dear all,

I hope this message finds you well.

As you know, our manuscript on multimodal wearable and camera-based stress and attention monitoring was not accepted by *Computers in Biology and Medicine*. The editor's decision carried no detailed technical comments, only the note that although the problems addressed were potentially of interest to the readership, the manuscript did not meet the journal's required quality standards. Because there was no specific list of faults to work through, I took the decision as a signal to re-examine the work from its foundations rather than to revise it superficially. I am writing to place before you the outcome of that work, and to ask for your guidance before we proceed.

I have prepared a substantially restructured manuscript aimed at ***Biomedical Signal Processing and Control*** (BSPC, Elsevier), together with a completed PRISMA 2020 checklist. Both are attached. I set out below what I examined, what I changed, and where I believe the contribution now lies. I do so with the full awareness that the judgement on all of this is yours.

---

### 1. I began with a verification audit rather than with writing

Before changing any text, I traced every substantive numerical claim in our previous version back to the paper it was attributed to. This was slower than I expected and, I must report honestly, it was necessary. Several figures we had carried through the abstract, the narrative and the summary tables could not be corroborated against the primary sources:

- The EEG and GSR fusion result we reported as 86.6% against 77.1% does not appear in the cited source; that study reports AUROC values of 0.954, 0.944 and 0.886, and the citation pointed to two different papers in two different sections.
- The 12% gain from adding physiological data to facial and gaze features is not in the cited paper. That study reports 82.78% against 79.55%, a difference of 3.23 pp, and its authors explicitly conclude that physiological data alone may be adequate — close to the opposite of the reading we gave it.
- The 38.6 pp personalization gain that anchored our abstract and our fusion table is not supported. The correct values are 95.06% against 67.65%, a gap of 27.41 pp.
- The CapsNet-versus-SVM comparison on WESAD (94.52% against 84.3%), which anchored one of our figures, does not appear in the cited study at all.
- Three further values, for SADDNet, for the EEG student study and for the one-channel EEG and GSR system, also differed from their sources.

I want to be clear that I raise this only so that the record is accurate and so that nothing of this kind can reach a reviewer. Every one of these has been removed or replaced with the verified value, and I have kept a full audit trail documenting each check. I am grateful that this surfaced now rather than after publication.

The audit also showed that 41 of our 117 references reported no stress, attention or cognitive-load outcome at all — they covered arrhythmia, sleep staging, seizure detection, glucose, materials characterisation and similar topics. Two preprints and one conference paper were included despite our own stated exclusion criteria, and two 2021 papers fell outside the window. These have been removed.

### 2. The scientific framing has been rebuilt, and this is where I believe the novelty now sits

Our earlier version surveyed the field and reported that multimodal fusion outperforms unimodal approaches. On reflection, and after the audit, I came to think the weakness was not presentational but structural: almost all evidence for fusion in this literature — ours included — was assembled by comparing an accuracy reported by one study against an accuracy reported by a different study. Those two numbers differ in cohort, stressor protocol, labelling, class definition, preprocessing and, critically, validation scheme. Such a comparison estimates the sum of all of those differences, not the effect of fusion.

The reframed manuscript is built on an observation that I have not found exploited systematically anywhere in this area: **within a single study, one team frequently reports both a unimodal baseline and a fused model under an identical protocol, and separately reports the same model under two different evaluation regimes.** Restricting the synthesis to these *within-study* contrasts removes the between-study confounds and lets the fusion effect and the evaluation effect be estimated on the same scale and compared directly.

The results are, I think, genuinely interesting, and they are not what we previously claimed:

| Quantity | Estimate |
|---|---|
| Median within-study fusion gain | **+4.67 pp** (range +1.00 to +14.30, k = 4) |
| Median within-study evaluation-induced gap | **9.14 pp** (range 1.26 to 48.66, k = 10) — about twice as large |
| Personalization alone | **27.41 pp** accuracy and **48.66 pp** F1, within one study on identical data |
| Laboratory to free-living | **13.00 pp** of F1 |
| WESAD to a real-world cohort | **14.56 pp** of AUROC, against only 4.00 pp between two curated benchmarks |

In short: fusion does help, and every matched contrast is positive, but it helps by less than the field assumes, and by considerably less than the performance swing produced by evaluation choices that are often left unreported. The defensible conclusion is that the binding constraint on deployable systems is the evaluation regime, not the sensing configuration or the network architecture.

### 3. Two supporting findings that I believe strengthen the case

**The reference benchmark has saturated.** On WESAD, 7 of 9 corroborated records exceed 92% irrespective of architecture, and a k-nearest-neighbour classifier at 96.00% is not meaningfully separated from a transformer at 98.23%. More tellingly, leave-one-subject-out results (median 94.59%) are statistically indistinguishable from results whose protocol was never stated (median 95.06%), while the single properly subject-independent generalized evaluation falls to 67.65%. WESAD is therefore saturated for the protocols commonly used on it and remains unsolved for the one that deployment actually requires.

**Reporting completeness is the rate-limiting step.** Across the 60 included studies, the validation protocol was recoverable for only 8 (13.3%) and a variance or confidence interval for only 3 (5.0%). Given that the protocol distinction is worth up to 27.41 pp of accuracy within a single study, an unlabelled accuracy figure in this literature carries very little information. Reported accuracy also showed no relationship with cohort size (r = +0.12, k = 16), which is difficult to explain except as evaluation design rather than task difficulty setting the reported numbers.

### 4. What is new in the manuscript itself

- **New title, research questions and objectives.** Three questions (RQ1 to RQ3) and five objectives (O1 to O5), all framed around the confound-controlled estimate.
- **A tightened, fully verified corpus.** 117 records identified, 116 unique screened, 60 included (2022 to 2026 only); every bibliographic record independently corroborated, with corroboration made an explicit inclusion criterion.
- **Independent corroboration reported as a result.** A headline outcome could be corroborated for 28 of 60 studies (46.7%); only corroborated values enter the synthesis, and unrecoverable values are coded as not recovered rather than imputed.
- **Ten data-driven figures and seven data-driven tables**, every value generated programmatically from machine-readable evidence records rather than typed in, so the analysis is reproducible end to end.
- **Figure 1 (the system block diagram) and Figure 2 (the PRISMA flow) drawn natively in LaTeX/TikZ**, with the evaluation protocol shown as a processing stage in its own right — which is the visual statement of the paper's argument.
- **Alignment with BSPC's scope**, which I checked line by line: signal acquisition and conditioning, artefact handling and signal-quality gating, robustness and non-stationarity, multimodal fusion, real-time and embedded operation, interpretability, and closed-loop and feedback-controlled systems, all now treated explicitly and with translational framing.

### 5. The PRISMA 2020 checklist

I have completed the official PRISMA 2020 checklist in full and attached it. For each of the 42 items it gives the section number, the page, and the specific table or figure, together with a note on what is reported there. Your template's wording, structure and licence line are preserved exactly; only the location column has been completed.

I should draw your attention to one deliberate choice. **Eleven items are recorded as not done, with the reason stated, rather than being claimed.** These are: no sensitivity analysis (items 13f and 20d, as leave-one-out is uninformative at k = 4 and k = 10); no reporting-bias assessment (14 and 21, as funnel and Egger tests are not interpretable at that k); no GRADE certainty rating (15 and 22); and no registration or protocol (24a to 24c). Item 11 states plainly that no formal risk-of-bias instrument was applied and that a five-item reporting-recoverability appraisal was used in its place. My reasoning is that reviewers check these against the manuscript, and an honest gap is far easier to defend than an overstated tick. I would of course welcome your view if you would prefer a different approach.

### 6. Matters on which I would be grateful for your decision

The checklist has surfaced several items that I do not think I should settle alone:

1. **Reviewer procedure (items 8, 9, 11).** The manuscript does not currently state how many of us screened records and extracted data, or whether we worked independently. Could you advise what accurately reflects how we worked, so I can state it correctly?
2. **Funding statement (item 25).** No funding statement currently appears. Please let me know what should be acknowledged.
3. **Competing interests (item 26)** and **data availability (item 27).** Both sections were removed during revision and should be reinstated before submission, as BSPC requires them.
4. **Registration (item 24a).** PRISMA expects an explicit statement that the review was not registered; I propose adding one sentence to Section 3.
5. **DOI verification.** Every reference was checked against publisher and indexed records, but the environment I worked in blocked Crossref, so I would like to run a final Crossref DOI pass on an unrestricted connection before submission.

---

The attached files are the manuscript (PDF and Word), the LaTeX source, the completed PRISMA 2020 checklist, and the evidence audit documenting every verification.

I am very conscious that this version departs considerably from the one you last saw, and that the decision on whether this framing is the right one rests with you. **I would be most grateful if you would share your comments, corrections and suggestions on this thread**, so that we can keep all feedback together and I can work through it systematically. Any disagreement with the direction, the framing or the conclusions is genuinely welcome — it is far better raised now than by a reviewer.

Thank you very much for your time, your patience and your continued guidance. I am sincerely grateful for the support you have given this work, and I look forward to hearing your thoughts.

With warm regards and deep respect,

**Alvi Ibn Amzad Anil**
Department of Electrical and Electronic Engineering
BSRM School of Engineering, BRAC University
alviamzad02@gmail.com

*Attachments: Manuscript_BSPC.pdf · Manuscript_BSPC.docx · Manuscript_BSPC.tex · PRISMA_2020_Checklist_Completed.docx · EVIDENCE_AUDIT.md*
