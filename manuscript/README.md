# Manuscript: BSPC submission package

**Title.** Evaluation Protocol Outweighs Multimodal Fusion in Wearable Stress and Attention
Monitoring: Systematic Review and Meta-Analysis

**Target journal.** Biomedical Signal Processing and Control (Elsevier).

## Deliverables

| File | Description |
|---|---|
| `Manuscript_BSPC.pdf` | Compiled manuscript, 0.7 in margins, 22 pages |
| `Manuscript_BSPC.tex` | Self-contained LaTeX source (all inputs inlined) |
| `Manuscript_BSPC_Overleaf.zip` | Ready for Overleaf: New Project > Upload Project |
| `Manuscript_BSPC.docx` | Word version with all 10 figures, 7 tables and a numbered reference list |
| `src/` | Full LaTeX source |
| `EVIDENCE_AUDIT.md` | Strict evidence audit of the uploaded manuscript |

## LaTeX source

```
src/main.tex            master file
src/preamble.tex      0.7 in margins, TikZ styles, table column types
src/titlepage.tex     title page with author details
src/body_1..4.tex     abstract, introduction, related work, methodology, results,
                      trends, discussion, conclusion
src/fig1_block.tex      Figure 1, block diagram, TikZ (generated, do not hand-edit)
src/fig2_prisma.tex     Figure 2, PRISMA flow, TikZ (generated, do not hand-edit)
src/tab1,3,4,5,6.tex    generated tables (do not hand-edit)
src/bibliography.tex    generated reference list in first-citation order
src/make_all_figures.py ALL figure code, self-contained
src/reference_justified.docx  pandoc style template giving justified body text
```

### One script for every figure

`src/make_all_figures.py` is standalone: it embeds the complete evidence base and
needs no other project file. It emits the TikZ source for Figures 1 and 2 and
renders Figures 3 to 10 as PNG.

```bash
python3 make_all_figures.py --stats          # regenerate everything, print the statistics
python3 make_all_figures.py --outdir OUT --texdir TEX
```

## Rebuilding

```bash
cd src
python3 make_all_figures.py # Figures 1-10 (TikZ sources + rendered PNG)
python3 make_tables.py      # Tables 1, 3, 4, 5, 6
python3 make_bib.py         # reference list in citation order
pdflatex main.tex && pdflatex main.tex
python3 build_docx.py       # DOCX with resolved citations and numbered captions
```

Requires `texlive-latex-extra`, `texlive-pictures`, `pandoc`, and Python with `matplotlib`.

## Evidence base

Every reported value is generated from machine-readable records, not typed into the
manuscript:

- `data/corpus.csv` — 116 screened records with include/exclude decision, exclusion reason
  and application area.
- `data/evidence.py` — 34 corroborated outcome records, 4 within-study fusion contrasts,
  10 within-study evaluation contrasts, the corroboration list and the reporting-recovery
  coding, each tagged with its source reference.

Headline results: median within-study fusion gain +4.67 pp (k = 4, range +1.00 to +14.30);
median within-study evaluation-induced gap 9.14 pp (k = 10, range 1.26 to 48.66);
personalization gap 27.41 pp accuracy and 48.66 pp F1 within a single study.

## Before submission

Run the reference list through a Crossref DOI check on an unrestricted network. Crossref,
doi.org, OpenAlex, Europe PMC and all publisher domains were blocked by the network policy
of the environment in which this package was produced, so DOI validation was performed
against publisher landing pages and indexed records instead. See section 7 of
`EVIDENCE_AUDIT.md`.
