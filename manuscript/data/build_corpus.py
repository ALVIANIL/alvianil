import json, csv, re
refs = {r['n']: r for r in json.load(open('/tmp/claude-0/-home-user-alvianil/a816ead8-e3f1-5885-8aef-97fe989523df/scratchpad/ms/refs.json'))}

# Decision map: id -> (decision, reason_code, subject_area)
# reason codes: E1 pre-2022, E2 not peer-reviewed journal article,
# E3 outcome outside stress/attention/cognitive-load scope,
# E4 no quantitative evaluation of a detection/monitoring model (protocol, review, acceptance, intervention)
INC = {
 1:'Occupational', 3:'Clinical', 4:'Occupational', 5:'Occupational', 7:'Driving',
 8:'Driving', 10:'Daily life', 12:'Laboratory', 13:'Daily life', 14:'Laboratory',
 16:'Laboratory', 17:'Occupational', 19:'Laboratory', 21:'Laboratory', 22:'Benchmark',
 24:'Laboratory', 25:'Daily life', 26:'Occupational', 28:'Clinical', 29:'Laboratory',
 30:'Education', 31:'Laboratory', 33:'Benchmark', 34:'Daily life', 35:'Daily life',
 37:'Laboratory', 38:'Laboratory', 41:'Laboratory', 42:'Aviation', 43:'Laboratory',
 45:'Driving', 47:'Benchmark', 48:'Daily life', 49:'Education', 50:'Benchmark',
 51:'Clinical', 52:'Benchmark', 53:'Benchmark', 54:'Laboratory', 55:'Benchmark',
 56:'Laboratory', 58:'Benchmark', 61:'Occupational', 70:'Benchmark', 72:'Benchmark',
 73:'Clinical', 74:'Education', 75:'Laboratory', 76:'Laboratory', 79:'Daily life',
 86:'Laboratory', 87:'Laboratory', 91:'Benchmark', 99:'Education', 101:'Benchmark',
 102:'Education', 105:'Daily life', 108:'Laboratory', 109:'Daily life',
 115:'Clinical',
}
EXC = {
 2:'E3', 6:'E3', 9:'E4', 11:'E1', 15:'E3', 18:'E3', 20:'E3', 23:'E3', 27:'E4',
 32:'E3', 36:'E3', 39:'E3', 40:'E4', 44:'E3', 46:'E3', 57:'E1', 59:'E4', 60:'E3',
 62:'E2', 63:'E3', 64:'E4', 65:'E4', 66:'E3', 67:'E3', 68:'E4', 69:'E3', 71:'E3',
 77:'E3', 78:'E3', 80:'E3', 81:'E2', 82:'E3', 83:'E3', 84:'E3', 85:'E3', 88:'E3',
 89:'E3', 90:'E3', 92:'E3', 93:'E3', 94:'E3', 95:'E3', 96:'E3', 97:'E3', 98:'E2',
 100:'E3', 103:'E3', 104:'E3', 106:'E3', 107:'E4', 110:'E4', 111:'E3', 112:'E3', 113:'E3',
 114:'E3', 116:'E3', 117:'E4',
}

PUB = [('10.1109/','IEEE'),('10.3390/','MDPI'),('10.1371/','PLOS'),('10.1016/','Elsevier'),
       ('10.1038/','Springer Nature'),('10.1007/','Springer'),('10.2196/','JMIR'),
       ('10.1186/','BMC'),('10.1039/','RSC'),('10.1145/','ACM'),('10.1101/','medRxiv'),
       ('10.21203/','Research Square')]
def pub(doi):
    for p,n in PUB:
        if doi.startswith(p): return n
    return 'Other'

rows=[]
for n in sorted(refs):
    r=refs[n]; raw=r['raw']
    # split "Authors. Title. Journal Year;vol:pages. https://doi..."
    parts=[p.strip() for p in raw.split('. ')]
    rows.append(dict(id=n, year=r['year'], doi=r['doi'], publisher=pub(r['doi']),
                     decision='include' if n in INC else 'exclude',
                     reason=EXC.get(n,''), area=INC.get(n,''), raw=raw))
with open('corpus.csv','w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)

inc=[r for r in rows if r['decision']=='include']
exc=[r for r in rows if r['decision']=='exclude']
print('seed records:',len(rows),' include:',len(inc),' exclude:',len(exc))
from collections import Counter
print('exclusion reasons:',dict(Counter(r['reason'] for r in exc)))
print('included by year:',dict(sorted(Counter(r['year'] for r in inc).items())))
print('included by area:',dict(Counter(r['area'] for r in inc)))
print('included by publisher:',dict(Counter(r['publisher'] for r in inc)))
print('all by publisher:',dict(Counter(r['publisher'] for r in rows)))
assert all(r['year']>=2022 for r in inc), 'pre-2022 leaked in'
