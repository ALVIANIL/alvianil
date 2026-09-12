#!/usr/bin/env python3
"""Fill the 'Location where item is reported' column of the PRISMA 2020 checklist
for the BSPC manuscript, editing the supplied template in place so that its
wording, styling, header and licence statement are preserved exactly."""
import re, os, shutil, zipfile

TEMPLATE = "PRISMA_2020_checklist_template.docx"
OUTPUT   = "../PRISMA_2020_Checklist_Completed.docx"

# --- content: item number -> text for column 4 (**bold** supported) ----------
LOC = {
"1": "**Title page and p. 1.** The title reads “Evaluation Protocol Outweighs Multimodal "
     "Fusion in Wearable Stress and Attention Monitoring: Systematic Review and Meta-Analysis”, "
     "identifying the report as a systematic review with a quantitative synthesis.",

"2": "**Abstract, p. 1** (single paragraph, 173 words). Reports the objective, the eligibility "
     "window and outcome scope, the information sources, the number screened (116) and included "
     "(60), the synthesis approach (within-study contrasts only), the principal results with "
     "magnitudes (median fusion gain 4.67 pp, k = 4; median evaluation-induced gap 9.14 pp, "
     "k = 10; personalization 27.41 pp accuracy and 48.66 pp F1; laboratory-to-field 13.00 pp F1; "
     "WESAD saturation) and the conclusions. **Not covered in the abstract**, because of the word "
     "limit: registration status, funding and certainty of evidence (PRISMA 2020 for Abstracts "
     "items 3, 11 and 12).",

"3": "**Section 1.1, p. 2; Section 1.3, p. 3; Section 2.3, p. 5.** Section 1.3 states the specific "
     "gap: almost all quantitative support for multimodal fusion in this field is assembled from "
     "between-study comparisons in which fusion is confounded with cohort, stressor protocol, "
     "label source, class definition, preprocessing and validation scheme, so a between-study "
     "difference estimates the sum of these rather than the effect of fusion. Section 2.3 states "
     "that prior reviews treat the two sensing families in parallel and pool headline numbers, "
     "and that none places the fusion effect and the evaluation effect on a common scale.",

"4": "**Section 1.4, p. 4.** Three research questions (RQ1 to RQ3) and five objectives (O1 to O5) "
     "are stated explicitly. RQ1: magnitude of the fusion gain when estimated only from "
     "within-study, protocol-matched comparisons. RQ2: how that gain compares with the "
     "within-study difference attributable to evaluation choices. RQ3: whether the dominant "
     "benchmark has saturated and how completely the evidence base is reported and verifiable.",

"5": "**Section 3.2, p. 6**, with the full criteria and the number of records excluded under each "
     "in **Table 2, p. 7** (publication window 2022-01-01 to 2026-03-31; peer-reviewed journal "
     "articles only; outcome restricted to psychological stress, attention, inattention, "
     "drowsiness, cognitive load or mental workload; empirical study reporting a quantitative "
     "evaluation of a detection or monitoring model; wearable, camera-based or fused sensing with "
     "an ML or DL model; bibliographic record independently corroborated). Grouping for the "
     "syntheses is specified in **Section 3.5, p. 9**: studies enter the fusion-contrast group "
     "only if they report a single-modality and a multimodal result on the same cohort under the "
     "same protocol, and the evaluation-contrast group only if they report the same model under a "
     "more favorable and a more realistic evaluation condition.",

"6": "**Section 3.1, p. 5** and **Table 1, p. 6**, which gives the screened and included counts "
     "for every publisher of record (IEEE 27 included of 30 screened, MDPI 10 of 11, Elsevier 8 "
     "of 21, PLOS 6 of 22, Springer Nature 4 of 16, JMIR 2 of 7, Springer 2 of 3, BMC 1 of 2, and "
     "medRxiv, Research Square, ACM and RSC 0 of 1 each). Distribution of the included corpus is "
     "also shown in **Figure 4(b), p. 9**. Registers, websites, organisations and reference-list "
     "searching were **not** used. **Date last searched: 11 September 2026** (verification "
     "searches of publisher and indexed records). The corresponding limitation, that records came "
     "from a pre-specified corpus rather than fresh database queries executed for this review, is "
     "stated in **Section 6.2, p. 19**.",

"7": "**Section 3.1, p. 5**, with the per-publisher yield in **Table 1, p. 6**. **Deviation from "
     "the item, stated explicitly in Sections 3.1 (p. 5) and 6.2 (p. 19):** because the records "
     "were drawn from a pre-specified corpus of 117 and then screened and verified, the review "
     "does not present per-database Boolean strings, filters or limits, and corpus composition is "
     "reported by publisher of record rather than by database hit counts. The complete list of "
     "the 116 screened records with each screening decision is supplied as supplementary material "
     "(data/corpus.csv), so the selection is fully reproducible.",

"8": "**Section 3.3, p. 7**, with the flow in **Figure 2, p. 8** and the criteria in **Table 2, "
     "p. 7**: 117 records identified, 1 duplicate removed, 116 unique records screened, 56 "
     "excluded at eligibility appraisal, 60 included. Automation tools were **not** used. "
     "**Not reported in the manuscript:** how many reviewers screened each record, and whether "
     "they worked independently.",

"9": "**Section 3.3, p. 7** specifies the data-collection and verification procedure: for each of "
     "the 60 included studies the title, authors, journal, year, volume, pagination and DOI were "
     "checked against the publisher or indexed record, and the reported headline outcome was "
     "sought in the same source. A value entered the quantitative synthesis only if it could be "
     "recovered from the openly retrievable record; values that could not be recovered were coded "
     "as not recovered rather than imputed, and no value was taken on the authority of a "
     "secondary citation. Extracted values are archived in data/evidence.py. **Not reported in "
     "the manuscript:** how many reviewers collected data from each report and whether they "
     "worked independently; no study authors were contacted for missing or unclear information.",

"10a": "**Section 3.5, p. 9** defines the two estimands (the fusion gain and the "
       "evaluation-induced gap). The outcome domains sought were classification accuracy, "
       "F1 score and AUROC for the detection of stress, attention, drowsiness or cognitive load. "
       "All corroborated outcome records are listed in **Table 4, p. 10**, which reports every "
       "result compatible with each domain that could be recovered, including multiple results "
       "per study where a study reported more than one dataset, class count or protocol (34 "
       "outcome records from 28 studies). Where a study reported several results, all recoverable "
       "ones were entered rather than a single selected value.",

"10b": "**Section 3.5, p. 9** and **Table 4, p. 10**: sensing configuration, evaluation dataset, "
       "participant count, validation protocol, metric and number of classes were sought for "
       "every outcome record. Study-level variables (publication year, application area, "
       "publisher of record) are in **Figures 3 and 4, pp. 8 to 9**, and reporting-completeness "
       "variables in **Table 3, p. 9**. Assumptions about missing information are stated in "
       "**Section 3.3, p. 7**: unrecoverable fields were coded as not recovered and never imputed "
       "or inferred. Funding of the included studies was not extracted.",

"11": "**Section 3.4, p. 9**, with results in **Table 3, p. 9**. **Deviation from the item, "
      "stated in Sections 3.4 (p. 9) and 6.2 (p. 19):** a formal risk-of-bias instrument "
      "(for example QUADAS-2 or PROBAST) was **not** applied. In its place each included study "
      "was appraised on whether five items material to interpreting a reported result could be "
      "recovered from the openly retrievable record: the headline performance metric, the "
      "evaluation cohort size, the validation protocol, whether a public benchmark was used, and "
      "whether any variance or confidence interval accompanied the point estimate. The dominant "
      "bias of concern in this literature, subject-dependent evaluation reported without label, "
      "is addressed directly by the protocol-stratified analysis in **Section 4.2, p. 12**. "
      "**Not reported:** how many reviewers performed the appraisal or whether they worked "
      "independently.",

"12": "**Section 3.5, p. 9.** The effect measure for both estimands is the **within-study "
      "difference in the originally reported metric, expressed in percentage points (pp)**: the "
      "multimodal minus the best single-modality result for the fusion gain, and the favorable "
      "minus the realistic condition for the evaluation-induced gap. Accuracy, F1 and AUROC "
      "differences are reported separately by metric in **Tables 5 and 6, pp. 13 to 14** and are "
      "never pooled across metrics; the caveat that a percentage point of F1 and a percentage "
      "point of AUROC are not interchangeable is stated in **Section 6.2, p. 19**.",

"13a": "**Section 3.5, p. 9.** A study is eligible for the fusion synthesis only if a single "
       "research team reports a single-modality baseline and a multimodal result on the same "
       "cohort, with the same pipeline and under the same validation protocol (4 contrasts from "
       "4 studies, **Table 5, p. 13**). A study is eligible for the evaluation synthesis only if "
       "it reports the same model under a more favorable and a more realistic evaluation "
       "condition, with the varied factor being personalization, deployment setting, dataset or "
       "task granularity (10 contrasts from 6 studies, **Table 6, p. 14**). Studies whose "
       "headline outcome could not be corroborated contribute to the narrative synthesis only "
       "(**Section 4.1.1, pp. 11 to 12**).",

"13b": "**Section 3.3, p. 7** and **Section 3.5, p. 9.** No conversion or imputation of summary "
       "statistics was performed. Values were transcribed in the metric and precision reported by "
       "the source; differences were computed by subtraction within a study and expressed in "
       "percentage points, with AUROC values expressed on a 0 to 100 scale for display only. "
       "Missing summary statistics were coded as not recovered and the affected study was "
       "excluded from the quantitative synthesis rather than having values estimated.",

"13c": "**Tables 4 to 7 (pp. 10 to 17)** and **Figures 3 to 10 (pp. 8 to 16)**. Individual study "
       "results are tabulated in Table 4; paired within-study contrasts are shown as slope plots "
       "and gain bars in **Figure 7, p. 13**, and as range segments in **Figure 8(a), p. 14**; "
       "the two estimands are placed on a common axis in **Figure 8(b), p. 14**. All figures are "
       "generated directly from the archived evidence records by a single script "
       "(src/make_all_figures.py), so no displayed value is entered by hand.",

"13d": "**Section 3.5, p. 9.** **No pooled meta-analytic model was fitted.** Given the small "
       "number of eligible within-study contrasts (k = 4 and k = 10), effect sizes are summarized "
       "by the **median and the full range**, and the comparison of interest is the relative "
       "magnitude of two medians rather than a hypothesis test. The rationale, and the decision "
       "not to compute a pooled random-effects estimate or heterogeneity statistics such as I-squared, "
       "are stated in Section 3.5 and revisited in **Section 6.2, p. 19**. No significance testing "
       "was performed.",

"13e": "**Section 3.5, p. 9**, with results in **Section 4.2, p. 12** and **Section 4.4, p. 13**. "
       "Heterogeneity was explored by **stratification rather than by meta-regression**: WESAD "
       "results are stratified by validation protocol in **Figure 6(b), p. 12**; the evaluation "
       "contrasts are grouped into four mechanisms (personalization, deployment setting, task "
       "granularity, dataset transfer) in **Figure 8(b), p. 14** and **Table 6, p. 14**; and "
       "reported accuracy is plotted against evaluation cohort size in **Figure 9(b), p. 15**. "
       "Formal subgroup tests were not performed because k is too small to support them.",

"13f": "**Not conducted.** No sensitivity analysis (for example leave-one-study-out) was "
       "performed, because with k = 4 fusion contrasts and k = 10 evaluation contrasts the "
       "removal of a single contrast is not informative about robustness. In place of a "
       "sensitivity analysis the manuscript reports the **full range alongside every median** "
       "(Tables 5 and 6, pp. 13 to 14) and states in **Section 6.2, p. 19** that medians over "
       "k = 4 and k = 10 are unstable and that the personalization estimate rests on one study "
       "reporting two metrics.",

"14": "**Not performed, and acknowledged.** No assessment of risk of bias due to missing results "
      "(publication or selective-reporting bias) was undertaken: funnel-plot asymmetry and "
      "Egger-type tests are not interpretable at k = 4 and k = 10. The closely related problem of "
      "**selective protocol reporting** is instead measured directly and reported as a primary "
      "finding: the validation protocol was recoverable for only 8 of 60 studies (13.3%) and a "
      "variance or confidence interval for only 3 of 60 (5.0%), in **Section 3.4 (p. 9), Table 3 "
      "(p. 9), Section 4.5 (pp. 15 to 16)** and **Figure 10, p. 16**.",

"15": "**Not performed.** GRADE or any equivalent formal certainty assessment was not applied, and "
      "no certainty rating is attached to any outcome. The manuscript instead qualifies every "
      "synthesized estimate by the number of contributing contrasts and the full range "
      "(**Tables 5 and 6, pp. 13 to 14**) and devotes **Section 6.2, p. 19** to the four "
      "limitations that bound the conclusions. Readers should treat the absence of a formal "
      "certainty rating as a limitation of this review.",

"16a": "**Section 3.3, p. 7**, with the full flow diagram in **Figure 2, p. 8**: 117 records "
       "identified in the pre-specified corpus, 1 duplicate removed, 116 unique records screened, "
       "56 excluded at eligibility appraisal, 60 studies included in the narrative synthesis, "
       "verification attempted for all 60, and 28 studies carried into the quantitative synthesis "
       "contributing 34 outcome records, 4 fusion contrasts and 10 evaluation contrasts.",

"16b": "**Figure 4(a), p. 9** gives the number excluded under each criterion and **Table 2, p. 7** "
       "the criterion definitions: 41 excluded because the reported outcome fell outside the "
       "stress, attention and cognitive-load scope, 10 because no quantitative model evaluation "
       "was reported, 3 because the record was a preprint or conference paper, and 2 because it "
       "fell outside the 2022 to 2026 window. **Section 3.2, p. 6** names the categories of "
       "wearable study that are frequently cited in this area but were excluded here (cardiac "
       "arrhythmia, sleep staging, seizure detection, glucose, physical fatigue, human activity "
       "recognition, materials characterisation). A record-by-record list of all 56 exclusions "
       "with the reason for each is supplied as supplementary material (EVIDENCE_AUDIT.md, "
       "section 4, and data/corpus.csv).",

"17": "**Table 4, p. 10** cites each of the 28 studies contributing quantitative data and gives "
      "its sensing configuration, evaluation dataset, cohort size, validation protocol, metric "
      "and value. The remaining 32 included studies are cited and characterised in **Section "
      "4.1.1, pp. 11 to 12**, grouped by architectural elaboration, deployment constraints, "
      "measurement validity and generalization as an explicit target. Corpus-level "
      "characteristics are in **Figure 3, p. 8** (year and application area) and **Figure 4(b), "
      "p. 9** (publisher of record). All 60 included studies are cited in the reference list "
      "(pp. 20 to 22).",

"18": "**Table 3, p. 9** presents the reporting-recoverability appraisal across all 60 included "
      "studies (headline metric 28/60, evaluation cohort size 18/60, public benchmark 14/60, "
      "validation protocol 8/60, variance or confidence interval 3/60), and **Figure 10, p. 16** "
      "displays the same data. **Per-study risk-of-bias judgements are not presented**, because "
      "no formal risk-of-bias instrument was applied (see item 11); the per-study recoverability "
      "coding underlying Table 3 is supplied as supplementary material (data/evidence.py, "
      "RECOVER).",

"19": "**Table 4, p. 10** presents, for every one of the 34 corroborated outcome records, the "
      "summary statistic as reported by the source study together with its evaluation dataset, "
      "cohort size, protocol and metric. Paired within-study results are given in **Table 5, "
      "p. 13** (unimodal and multimodal value and the difference) and **Table 6, p. 14** "
      "(favorable and realistic value and the gap). **Precision is largely unavailable:** a "
      "variance or confidence interval was recoverable for only 3 of 60 studies, so effect "
      "estimates are presented as point values without intervals; this is reported as a finding "
      "in **Section 4.5, pp. 15 to 16** and as a limitation in **Section 6.2, p. 19**.",

"20a": "**Section 4.3, p. 12** for the fusion synthesis and **Section 4.4, pp. 13 to 15** for the "
       "evaluation synthesis, with the contributing studies and their characteristics listed "
       "row by row in **Table 5, p. 13** and **Table 6, p. 14**. Both sections state that every "
       "contributing contrast is internal to a single study, so cohort, pipeline and protocol are "
       "held fixed by construction. The reporting quality of the contributing studies is "
       "characterised in **Table 3, p. 9**.",

"20b": "**Section 4.3, p. 12** and **Section 4.4, pp. 13 to 15**, with **Tables 5 and 6 "
       "(pp. 13 to 14)** and **Figures 7 and 8 (pp. 13 to 14)**. Fusion synthesis: median "
       "+4.67 pp, range +1.00 to +14.30, k = 4. Evaluation synthesis: median 9.14 pp, range 1.26 "
       "to 48.66, k = 10, approximately twice the median fusion gain. By mechanism: "
       "personalization median 38.03 pp (k = 2), deployment setting 13.00 pp (k = 1), task "
       "granularity 5.42 pp (k = 4), dataset transfer 4.00 pp (k = 3). **Precision:** no "
       "confidence intervals are reported, since no pooled model was fitted (item 13d); the full "
       "range accompanies every median. **Heterogeneity statistics such as I-squared and "
       "prediction intervals are not reported** and would not be interpretable at these values "
       "of k.",

"20c": "**Section 4.2, p. 12** (WESAD results stratified by validation protocol; 9 of 10 "
       "corroborated records above 86% and 7 of 9 above 92% irrespective of architecture; "
       "leave-one-subject-out median 94.59% indistinguishable from the protocol-unreported median "
       "95.06%; the single subject-independent generalized evaluation at 67.65%), **Section 4.4, "
       "pp. 13 to 15** (the four mechanisms), and **Section 4.5, p. 15** (reported accuracy "
       "against cohort size: slope +3.1 pp per decade, Pearson r = +0.12, k = 16, that is, "
       "essentially flat). Displayed in **Figures 6(b) (p. 12), 8 (p. 14) and 9 (p. 15)**.",

"20d": "**Not conducted**, for the reason given under item 13f. No sensitivity analysis is "
       "presented. The robustness caveat is stated instead in **Section 6.2, p. 19**: medians "
       "over k = 4 and k = 10 are unstable, full ranges are reported throughout, and the "
       "personalization estimate would be materially strengthened or weakened by two or three "
       "further studies reporting both conditions.",

"21": "**Not assessed**, consistent with item 14; no funnel plot, Egger test or equivalent is "
      "presented for either synthesis. The related and directly measured finding on incomplete "
      "protocol and variance reporting is presented in **Section 4.5, pp. 15 to 16**, **Table 3, "
      "p. 9** and **Figure 10, p. 16**, and its consequence, that an unlabelled accuracy figure "
      "in this literature carries very little information, is stated at the end of "
      "**Section 4.5, p. 16**.",

"22": "**Not assessed.** No GRADE or equivalent certainty rating is presented for any outcome "
      "(see item 15). **Section 6.2, p. 19** sets out the four limitations that bound confidence "
      "in the findings: the small number of within-study contrasts, corroboration limited by "
      "access as well as by reporting, corpus construction from a pre-specified record set, and "
      "heterogeneity of metrics and tasks.",

"23a": "**Section 6.1, pp. 18 to 19**, supported by the trend synthesis in **Section 5, "
       "pp. 17 to 18**. The interpretation is that fusion helps but by less than is generally "
       "assumed once cohort, pipeline and protocol are held fixed, that evaluation choices move "
       "reported performance roughly twice as far, and that the binding constraint on deployable "
       "systems is the evaluation regime rather than the sensing configuration or the network "
       "architecture. **Section 2.3, p. 5** and **Section 5.6, p. 18** place this against the "
       "prior review that found most wearable stress models lack generalization.",

"23b": "**Section 6.2, p. 19**, limitations two and four: corroboration was limited by access as "
       "well as by reporting (a headline outcome was corroborable for 46.7% of included studies, "
       "so the recovery rates are a lower bound on the literature's transparency), and the "
       "contrasts span accuracy, F1 and AUROC and binary through four-class tasks, so the "
       "aggregate medians summarize a heterogeneous set rather than estimating a single "
       "underlying parameter. Incomplete reporting in the evidence base is quantified in "
       "**Table 3, p. 9** and **Figure 10, p. 16**.",

"23c": "**Section 6.2, p. 19**, limitations one and three: only 4 fusion contrasts and 10 "
       "evaluation contrasts met the matched-protocol requirement, so medians are unstable and "
       "the central claim is framed as a difference in order of magnitude rather than a precise "
       "ratio; and the corpus was assembled from a pre-specified set of 117 records rather than "
       "from fresh database queries, which is documented and reproducible but is not equivalent "
       "to an exhaustive search. The strict outcome criterion, which excluded 41 records, is also "
       "noted as narrowing comparability with reviews that admit any wearable-sensing "
       "application. Absent elements of the review process (no registration, no formal "
       "risk-of-bias instrument, no certainty assessment) are recorded against items 11, 14, 15 "
       "and 24a of this checklist.",

"23d": "**Section 6.1, p. 19** gives three concrete recommendations for practice: report "
       "subject-independent performance as the primary result; treat benchmark-to-benchmark "
       "transfer as insufficient evidence of generalization; and justify each additional sensor "
       "against the specific unimodal baseline it displaces, reporting the ablation under a "
       "matched protocol. It notes that for closed-loop and therapeutic systems these are safety "
       "prerequisites rather than methodological preferences. **Section 7, p. 19** identifies "
       "subject-independent generalization on existing benchmarks as the appropriate target for "
       "future work, and **Table 7, p. 17** maps each constraint to its implication for "
       "deployment.",

"24a": "**The review was not registered.** It was not entered in PROSPERO or any other "
       "prospective register, and no registration number exists. This is not currently stated in "
       "the manuscript; the authors should add a registration statement to the Methods "
       "(Section 3) before submission.",

"24b": "**No review protocol was prepared or published.** The review method is specified in full "
       "in **Sections 3.1 to 3.5, pp. 5 to 9**, and the screening decisions, evidence base and "
       "analysis scripts are supplied as supplementary material so the procedure is reproducible, "
       "but this is a post-hoc specification and not a pre-registered protocol.",

"24c": "**Not applicable**, since the review was neither registered nor governed by a "
       "pre-specified protocol (items 24a and 24b), so there is no registered information to "
       "amend. All methodological decisions are those reported in Sections 3.1 to 3.5, "
       "pp. 5 to 9.",

"25": "**Not reported in the manuscript.** No funding statement appears in the current version. "
      "The authors should add a statement naming any financial or non-financial support and the "
      "role of the funders, or stating that the review received no specific grant, before "
      "submission; the author contribution statement on the title page lists funding acquisition "
      "roles for four authors, so a corresponding funding statement is expected by the journal.",

"26": "**Not reported in the manuscript.** The Declaration of Competing Interest section was "
      "removed from the current version at the authors' request. Biomedical Signal Processing "
      "and Control requires this declaration, so it should be reinstated in the manuscript or "
      "supplied through the journal's submission system before submission.",

"27": "**No availability statement currently appears in the manuscript**, the Data and Code "
      "Availability section having been removed from the current version. The following are "
      "nevertheless prepared and available as supplementary material and should be cited in a "
      "reinstated statement: the screened corpus with every inclusion and exclusion decision and "
      "reason (data/corpus.csv, 116 records); the complete extracted evidence base, comprising "
      "the 34 corroborated outcome records, the 4 fusion contrasts, the 10 evaluation contrasts, "
      "the corroboration list and the reporting-recoverability coding (data/evidence.py); the "
      "analytic and display code that generates every figure and data table from those records "
      "(src/make_all_figures.py, src/make_tables.py); and the full evidence audit documenting the "
      "verification of each claim (EVIDENCE_AUDIT.md). No template data-collection form was used, "
      "the extraction schema being the field structure of data/evidence.py.",
}

# --- XML helpers -------------------------------------------------------------
RPR = ('<w:rPr><w:rFonts w:ascii="Arial" w:hAnsi="Arial" w:cs="Arial"/>'
       '<w:color w:val="auto"/><w:sz w:val="16"/><w:szCs w:val="16"/>{b}</w:rPr>')

def esc(t):
    return (t.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'))

def runs(text):
    """Build w:r runs, honouring **bold** spans."""
    out = []
    for i, part in enumerate(text.split('**')):
        if not part:
            continue
        rpr = RPR.format(b='<w:b/><w:bCs/>' if i % 2 else '')
        out.append(f'<w:r>{rpr}<w:t xml:space="preserve">{esc(part)}</w:t></w:r>')
    return ''.join(out)

def split_cells(row):
    cells, depth, start = [], 0, None
    for m in re.finditer(r'<w:tc[ >]|</w:tc>', row):
        if m.group(0).startswith('<w:tc'):
            if depth == 0:
                start = m.start()
            depth += 1
        else:
            depth -= 1
            if depth == 0:
                cells.append((start, m.end()))
    return cells

def cell_text(chunk):
    t = ''.join(re.findall(r'<w:t(?: [^>]*)?>(.*?)</w:t>', chunk, re.S))
    for a, b in [('&amp;', '&'), ('&lt;', '<'), ('&gt;', '>')]:
        t = t.replace(a, b)
    return ' '.join(t.split())

# --- main --------------------------------------------------------------------
def main():
    work = '_build'
    shutil.rmtree(work, ignore_errors=True)
    os.makedirs(work)
    with zipfile.ZipFile(TEMPLATE) as z:
        names = z.namelist()
        z.extractall(work)

    path = os.path.join(work, 'word', 'document.xml')
    doc = open(path, encoding='utf-8').read()
    tbl = re.search(r'<w:tbl>.*?</w:tbl>', doc, re.S).group(0)
    new_tbl, filled, missing = tbl, [], []

    # widen the location column so the detailed entries are legible,
    # keeping the overall table width unchanged (15200 dxa)
    new_tbl = new_tbl.replace('<w:gridCol w:w="11745"/>', '<w:gridCol w:w="7300"/>')
    new_tbl = new_tbl.replace('<w:gridCol w:w="1200"/>', '<w:gridCol w:w="5645"/>')
    new_tbl = new_tbl.replace('<w:tcW w:w="11745" w:type="dxa"/>', '<w:tcW w:w="7300" w:type="dxa"/>')
    new_tbl = new_tbl.replace('<w:tcW w:w="1200" w:type="dxa"/>', '<w:tcW w:w="5645" w:type="dxa"/>')

    for row in re.findall(r'<w:tr\b.*?</w:tr>', new_tbl, re.S):
        cs = split_cells(row)
        if len(cs) != 4:
            continue
        item = cell_text(row[cs[1][0]:cs[1][1]])
        if item not in LOC:
            if item and item != 'Item #':
                missing.append(item)
            continue
        cell = row[cs[3][0]:cs[3][1]]
        m = re.search(r'(<w:p\b[^>]*>.*?)(</w:p>)', cell, re.S)
        para = m.group(0)
        # insert the runs just before </w:p>, after any existing pPr
        newpara = para[:-len('</w:p>')] + runs(LOC[item]) + '</w:p>'
        newrow = row[:cs[3][0]] + cell.replace(para, newpara) + row[cs[3][1]:]
        new_tbl = new_tbl.replace(row, newrow)
        filled.append(item)

    doc = doc.replace(tbl, new_tbl)
    open(path, 'w', encoding='utf-8').write(doc)

    out = os.path.abspath(OUTPUT)
    if os.path.exists(out):
        os.remove(out)
    with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as z:
        for n in names:                       # preserve original entry order
            z.write(os.path.join(work, n), n)
    shutil.rmtree(work, ignore_errors=True)

    print('filled %d items' % len(filled))
    print('order :', ' '.join(filled))
    if missing:
        print('UNFILLED rows:', missing)
    assert len(filled) == 42, 'expected 42 checklist rows, filled %d' % len(filled)

if __name__ == '__main__':
    main()
