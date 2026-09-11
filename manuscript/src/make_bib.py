import json, re, sys
RAW = {x['n']: x['raw'] for x in json.load(
    open('/tmp/claude-0/-home-user-alvianil/a816ead8-e3f1-5885-8aef-97fe989523df/scratchpad/ms/refs.json'))}
# Verified additional reference not present in the source corpus
RAW[118] = ("Vos G, Trinh K, Sarnyai Z, Rahimi Azghadi M. Generalizable machine learning for "
            "stress monitoring from wearable devices: A systematic literature review. "
            "Int J Med Inform 2023;173:105026. https://doi.org/10.1016/j.ijmedinf.2023.105026.")
# Corrections applied after independent verification
FIX = {47: ("Under- Resourced", "Under-Resourced"),
       13: ("SOSW :", "SOSW:")}

body = ''
for f in ['body_1.tex','body_2.tex','body_3.tex','tab1.tex','tab3.tex','tab4.tex','tab5.tex','tab6.tex','body_4.tex']:
    body += open(f).read()
order, seen = [], set()
for m in re.finditer(r'\\cite\{([^}]*)\}', body):
    for k in m.group(1).split(','):
        k = k.strip()
        if k and k not in seen:
            seen.add(k); order.append(k)
missing = [k for k in order if int(k[1:]) not in RAW]
if missing: sys.exit('missing bibliographic records: %s' % missing)

def clean(s):
    s = s.strip()
    if s.endswith('.'): s = s[:-1]
    s = re.sub(r'\s+', ' ', s)
    s = s.replace('—', '--').replace('–', '--')
    s = s.replace('&', '\\&').replace('%', '\\%').replace('#', '\\#')
    s = re.sub(r'https://doi\.org/(\S+)', r'https://doi.org/\1', s)
    return s + '.'

out = ['\\begin{thebibliography}{99}',
       '\\setlength{\\itemsep}{1.5pt}\\small']
for k in order:
    n = int(k[1:]); s = RAW[n]
    if n in FIX: s = s.replace(*FIX[n])
    out.append('\\bibitem{%s} %s' % (k, clean(s)))
out.append('\\end{thebibliography}')
open('bibliography.tex','w').write('\n'.join(out))
print('references in citation order:', len(order))
inc = {int(l.split(',')[0]) for l in open('/home/user/alvianil/manuscript/data/corpus.csv').readlines()[1:]
       if l.split(',')[4] == 'include'}
cited = {int(k[1:]) for k in order}
print('included studies not cited:', sorted(inc - cited))
print('cited but not in included set:', sorted(cited - inc))
