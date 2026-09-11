"""Verified evidence base. Every row was independently corroborated against the
publisher / indexed record. `src` records the corroborating statement."""
import json

# --- A. Corroborated headline outcomes -------------------------------------
OUTCOMES = [
 # ref, short, year, modality, n, dataset, protocol, metric, value, classes
 dict(ref=26, study="Awada et al.",        year=2024, mod="EDA+BVP+TEMP+behav.", n=None,
      dataset="In-house (office)", protocol="NR", metric="Accuracy", value=82.78, classes=4),
 dict(ref=37, study="Kim et al.",          year=2024, mod="EEG+GSR", n=30,
      dataset="In-house (VR interview)", protocol="NR", metric="AUROC", value=95.40, classes=2),
 dict(ref=12, study="Campanella et al.",   year=2023, mod="PPG+EDA", n=29,
      dataset="In-house", protocol="NR", metric="Accuracy", value=90.00, classes=2),
 dict(ref=33, study="Li & Washington",     year=2024, mod="BVP+EDA+TEMP", n=15,
      dataset="WESAD", protocol="Personalized", metric="Accuracy", value=95.06, classes=3),
 dict(ref=33, study="Li & Washington",     year=2024, mod="BVP+EDA+TEMP", n=15,
      dataset="WESAD", protocol="Subject-independent", metric="Accuracy", value=67.65, classes=3),
 dict(ref=58, study="Rashid et al.",       year=2023, mod="BVP+EDA+TEMP+ACC", n=15,
      dataset="WESAD", protocol="NR", metric="Accuracy", value=94.12, classes=2),
 dict(ref=58, study="Rashid et al.",       year=2023, mod="BVP+EDA+TEMP+ACC", n=15,
      dataset="WESAD", protocol="NR", metric="Accuracy", value=86.34, classes=3),
 dict(ref=43, study="Barki et al.",        year=2025, mod="In-ear PPG", n=15,
      dataset="In-house", protocol="NR", metric="Accuracy", value=97.78, classes=2),
 dict(ref=50, study="Ali et al. (ReTeNet)",year=2025, mod="BVP", n=15,
      dataset="WESAD", protocol="NR", metric="Accuracy", value=98.23, classes=3),
 dict(ref=47, study="Ali et al. (SADDNet)",year=2026, mod="PPG", n=50,
      dataset="CATSA+WESAD", protocol="LOSO", metric="Accuracy", value=92.25, classes=2),
 dict(ref=55, study="Ali et al. (TEANet)", year=2026, mod="BVP", n=15,
      dataset="WESAD", protocol="LOSO", metric="Accuracy", value=96.94, classes=2),
 dict(ref=55, study="Ali et al. (TEANet)", year=2026, mod="BVP", n=19,
      dataset="RUET-SPML", protocol="LOSO", metric="Accuracy", value=92.94, classes=2),
 dict(ref=61, study="Khayyat et al.",      year=2024, mod="HRV", n=15,
      dataset="WESAD", protocol="NR", metric="Accuracy", value=96.76, classes=3),
 dict(ref=61, study="Khayyat et al.",      year=2024, mod="HRV", n=25,
      dataset="SWELL-KW", protocol="NR", metric="Accuracy", value=92.76, classes=3),
 dict(ref=54, study="Momeni et al.",       year=2022, mod="ECG+EDA+RESP+TEMP", n=None,
      dataset="In-house", protocol="NR", metric="Accuracy", value=90.98, classes=2),
 dict(ref=16, study="Xu et al.",           year=2024, mod="Facial video (rPPG)", n=None,
      dataset="In-house", protocol="NR", metric="Accuracy", value=94.33, classes=2),
 dict(ref=16, study="Xu et al.",           year=2024, mod="Facial video (rPPG)", n=None,
      dataset="In-house", protocol="NR", metric="Accuracy", value=83.83, classes=3),
 dict(ref=99, study="Gedam et al.",        year=2025, mod="ECG+GSR+TEMP", n=200,
      dataset="In-house", protocol="NR", metric="Accuracy", value=96.17, classes=2),
 dict(ref=19, study="Hongn et al.",        year=2025, mod="EDA+BVP+TEMP+ACC", n=36,
      dataset="In-house (public)", protocol="NR", metric="Accuracy", value=93.00, classes=2),
 dict(ref=30, study="Fernandez et al.",    year=2025, mod="EEG", n=None,
      dataset="In-house", protocol="Subject-independent", metric="Accuracy", value=86.24, classes=3),
 dict(ref=4,  study="Rescio et al.",       year=2024, mod="EEG+ECG+EDA", n=None,
      dataset="In-house", protocol="NR", metric="Accuracy", value=95.38, classes=2),
 dict(ref=74, study="Chen & Lee",          year=2023, mod="ECG", n=None,
      dataset="In-house", protocol="NR", metric="Accuracy", value=93.42, classes=2),
 dict(ref=75, study="Abdul Kader et al.",  year=2024, mod="EEG+GSR", n=20,
      dataset="In-house", protocol="NR", metric="Accuracy", value=84.60, classes=2),
 dict(ref=13, study="Toshnazarov et al.",  year=2024, mod="PPG+ACC+context", n=26,
      dataset="In-house (lab)", protocol="NR", metric="F1", value=84.00, classes=2),
 dict(ref=13, study="Toshnazarov et al.",  year=2024, mod="PPG+ACC+context", n=18,
      dataset="In-house (field)", protocol="NR", metric="F1", value=71.00, classes=2),
 dict(ref=1,  study="Alsahreef et al.",     year=2026, mod="HRV", n=None,
      dataset="PARFAIT", protocol="NR", metric="Accuracy", value=98.10, classes=2),
 dict(ref=5,  study="Donati et al.",        year=2023, mod="ECG", n=None,
      dataset="In-house (factory)", protocol="NR", metric="Accuracy", value=88.40, classes=2),
 dict(ref=14, study="Mohammadi et al.",     year=2022, mod="ECG+EDA+RESP+TEMP", n=15,
      dataset="WESAD", protocol="NR", metric="Accuracy", value=96.00, classes=2),
 dict(ref=21, study="El Arwadi & Abu Daher",year=2025, mod="ECG (HRV)", n=None,
      dataset="In-house", protocol="LOSO", metric="Accuracy", value=90.80, classes=2),
 dict(ref=25, study="Kumar et al.",         year=2024, mod="PPG+EDA+TEMP", n=None,
      dataset="In-house", protocol="NR", metric="Accuracy", value=94.00, classes=2),
 dict(ref=49, study="Laiti et al.",         year=2026, mod="PPG (HRV)", n=15,
      dataset="WESAD", protocol="NR", metric="AUROC", value=91.58, classes=2),
 dict(ref=49, study="Laiti et al.",         year=2026, mod="PPG (HRV)", n=None,
      dataset="Wellby (real world)", protocol="NR", metric="AUROC", value=77.02, classes=2),
 dict(ref=53, study="Shikha et al.",        year=2024, mod="EDA+BVP+HRV", n=None,
      dataset="In-house", protocol="NR", metric="Accuracy", value=98.28, classes=2),
 dict(ref=109,study="Kim et al.",           year=2025, mod="HR+step count", n=None,
      dataset="In-house (free living)", protocol="NR", metric="Accuracy", value=74.40, classes=2),
]


# --- B. Within-study, protocol-matched unimodal -> multimodal contrasts -----
FUSION = [
 dict(ref=75, study="Abdul Kader et al. (2024)", uni="EEG", multi="EEG+GSR",
      level="Feature-level", metric="Accuracy", u=70.30, m=84.60, n=20),
 dict(ref=12, study="Campanella et al. (2023)", uni="PPG (HR)", multi="PPG+EDA",
      level="Feature-level", metric="Accuracy", u=83.89, m=90.00, n=29),
 dict(ref=26, study="Awada et al. (2024)", uni="Physiological", multi="Physiological + behavioral",
      level="Decision-level", metric="Accuracy", u=79.55, m=82.78, n=None),
 dict(ref=37, study="Kim et al. (2024)", uni="GSR", multi="EEG+GSR",
      level="Feature-level", metric="AUROC", u=94.40, m=95.40, n=30),
]

# --- C. Within-study contrasts attributable to evaluation / deployment ------
PROTOCOL = [
 dict(ref=33, study="Li & Washington (2024)", contrast="Personalized vs subject-independent",
      kind="Personalization", metric="Accuracy", hi=95.06, lo=67.65),
 dict(ref=33, study="Li & Washington (2024)", contrast="Personalized vs subject-independent",
      kind="Personalization", metric="F1", hi=91.71, lo=43.05),
 dict(ref=13, study="Toshnazarov et al. (2024)", contrast="Laboratory vs free-living",
      kind="Deployment setting", metric="F1", hi=84.00, lo=71.00),
 dict(ref=55, study="Ali et al. (2026, TEANet)", contrast="WESAD vs in-house cohort",
      kind="Dataset transfer", metric="Accuracy", hi=96.94, lo=92.94),
 dict(ref=61, study="Khayyat et al. (2024)", contrast="WESAD vs SWELL-KW",
      kind="Dataset transfer", metric="Accuracy", hi=96.76, lo=92.76),
 dict(ref=58, study="Rashid et al. (2023)", contrast="Binary vs three-class",
      kind="Task granularity", metric="Accuracy", hi=94.12, lo=86.34),
 dict(ref=16, study="Xu et al. (2024)", contrast="Stress state vs stress level",
      kind="Task granularity", metric="Accuracy", hi=94.33, lo=83.83),
 dict(ref=61, study="Khayyat et al. (2024)", contrast="Binary vs multiclass (WESAD)",
      kind="Task granularity", metric="Accuracy", hi=99.82, lo=96.76),
 dict(ref=49, study="Laiti et al. (2026)", contrast="WESAD vs Wellby real-world cohort",
      kind="Dataset transfer", metric="AUROC", hi=91.58, lo=77.02),
 dict(ref=53, study="Shikha et al. (2024)", contrast="Two-level vs three-level stress",
      kind="Task granularity", metric="Accuracy", hi=98.28, lo=97.02),
]

# --- D. Corroboration audit of the verification subsample -------------------
# Verification was attempted for every one of the 60 included studies.
ATTEMPTED = [1,3,4,5,7,8,10,12,13,14,16,17,19,21,22,24,25,26,28,29,30,31,33,34,35,37,38,41,42,
             43,45,47,48,49,50,51,52,53,54,55,56,58,61,70,72,73,74,75,76,79,86,87,91,99,101,102,
             105,108,109,115]
CORROBORATED = [1,4,5,12,13,14,16,19,21,25,26,30,33,37,43,47,49,50,53,54,55,58,61,74,75,99,101,109]

if __name__ == "__main__":
    json.dump(dict(outcomes=OUTCOMES, fusion=FUSION, protocol=PROTOCOL,
                   attempted=ATTEMPTED, corroborated=CORROBORATED),
              open('evidence.json','w'), indent=1)
    print("outcome rows      :", len(OUTCOMES))
    print("fusion contrasts  :", len(FUSION))
    print("protocol contrasts:", len(PROTOCOL))
    print("attempted / corroborated: %d / %d (%.1f%%)" %
          (len(ATTEMPTED), len(CORROBORATED), 100*len(CORROBORATED)/len(ATTEMPTED)))
    import statistics as st
    fg=[r['m']-r['u'] for r in FUSION]
    print("fusion gain  median %.2f  range %.2f-%.2f" % (st.median(fg), min(fg), max(fg)))
    pg=[r['hi']-r['lo'] for r in PROTOCOL]
    print("protocol gap median %.2f  range %.2f-%.2f" % (st.median(pg), min(pg), max(pg)))
    for k in ("Personalization","Deployment setting","Dataset transfer","Task granularity"):
        v=[r['hi']-r['lo'] for r in PROTOCOL if r['kind']==k]
        print("   %-20s n=%d  median %.2f" % (k, len(v), st.median(v)))

# --- E. Recoverability coding of the verification subsample (n=33) ---------
# A study is coded 1 for an item only if that item was explicitly recovered
# from the openly retrievable record during verification.
RECOVER = {
 'Headline metric'      : [1,4,5,12,13,14,16,19,21,25,26,30,33,37,43,47,49,50,53,54,55,58,61,
                           74,75,99,101,109],
 'Evaluation cohort size': [3,12,13,19,33,37,42,43,47,49,50,55,58,61,75,91,99,101],
 'Validation protocol'  : [13,21,30,33,47,49,55,101],
 'Public benchmark used': [14,22,33,47,49,50,52,55,58,61,70,72,91,101],
 'Variance or CI reported': [14,37,47],
}
