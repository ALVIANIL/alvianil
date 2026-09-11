import sys, csv, statistics as st
sys.path.insert(0,'/home/user/alvianil/manuscript/data')
from evidence import OUTCOMES, FUSION, PROTOCOL, ATTEMPTED, CORROBORATED, RECOVER
from collections import Counter
OUT='/home/user/alvianil/manuscript/src/'
corpus=list(csv.DictReader(open('/home/user/alvianil/manuscript/data/corpus.csv')))
inc=[r for r in corpus if r['decision']=='include']
exc=[r for r in corpus if r['decision']=='exclude']

# map original ref id -> new citation key (assigned later by order of first use);
# here we just emit the original id, replaced downstream.
def cite(n): return '\\cite{r%d}' % n
def esc(x):
    return str(x).replace('&', '\\&').replace('%', '\\%').replace('_', '\\_')

# ---------------- Table 1: source corpus and screening yield by publisher
pub_all=Counter(r['publisher'] for r in corpus)
pub_inc=Counter(r['publisher'] for r in inc)
rows=[]
for p,_ in pub_all.most_common():
    n=pub_all[p]; k=pub_inc.get(p,0)
    rows.append((p,n,k,n-k,100*k/n))
t1=['\\begin{tabular}{L{3.7cm} C{2.3cm} C{2.3cm} C{2.3cm} C{2.4cm}}','\\toprule',
 '\\textbf{Publisher of record} & \\textbf{Records screened} & \\textbf{Studies included} & '
 '\\textbf{Records excluded} & \\textbf{Inclusion yield (\\%)} \\\\','\\midrule']
for p,n,k,e,y in rows: t1.append(f'{esc(p)} & {n} & {k} & {e} & {y:.1f} \\\\')
t1+=['\\midrule',
 f'\\textbf{{Total}} & \\textbf{{{len(corpus)}}} & \\textbf{{{len(inc)}}} & '
 f'\\textbf{{{len(exc)}}} & \\textbf{{{100*len(inc)/len(corpus):.1f}}} \\\\','\\bottomrule','\\end{tabular}']
open(OUT+'tab1.tex','w').write('\n'.join(t1))

# ---------------- Table 4: corroborated evidence base
lab={'NR':'Not reported','LOSO':'LOSO','Personalized':'Personalized',
     'Subject-independent':'Subject indep.'}
t4=['\\begin{tabular}{L{2.8cm} C{0.7cm} L{3.2cm} L{2.45cm} C{0.7cm} L{1.8cm} C{0.9cm} C{1.1cm}}',
 '\\toprule',
 '\\textbf{Study} & \\textbf{Year} & \\textbf{Sensing configuration} & \\textbf{Evaluation data} & '
 '\\textbf{$n$} & \\textbf{Protocol} & \\textbf{Metric} & \\textbf{Value (\\%)} \\\\','\\midrule']
for o in sorted(OUTCOMES,key=lambda a:(a['study'],a['year'],-a['value'])):
    t4.append('%s & %d & %s & %s & %s & %s & %s & %.2f \\\\' % (
        esc(o['study'])+' '+cite(o['ref']), o['year'], esc(o['mod']), esc(o['dataset']),
        o['n'] if o['n'] else 'NR', lab[o['protocol']], o['metric'], o['value']))
acc=[o['value'] for o in OUTCOMES if o['metric']=='Accuracy']
t4+=['\\midrule',
 '\\multicolumn{7}{l}{\\textbf{Median corroborated accuracy across %d accuracy records}} & '
 '\\textbf{%.2f} \\\\' % (len(acc), st.median(acc)),
 '\\multicolumn{7}{l}{Interquartile range} & %.2f--%.2f \\\\' % (
    st.quantiles(acc,n=4)[0], st.quantiles(acc,n=4)[2]),
 '\\bottomrule','\\end{tabular}']
open(OUT+'tab4.tex','w').write('\n'.join(t4))

# ---------------- Table 5: within-study fusion contrasts
t5=['\\begin{tabular}{L{3.2cm} L{2.25cm} L{2.8cm} L{1.9cm} C{0.7cm} C{1.4cm} C{1.4cm} C{1.3cm}}',
 '\\toprule',
 '\\textbf{Study} & \\textbf{Single modality} & \\textbf{Multimodal configuration} & '
 '\\textbf{Fusion level} & \\textbf{$n$} & \\textbf{Unimodal} & \\textbf{Multimodal} & '
 '\\textbf{Gain (pp)} \\\\','\\midrule']
for r in sorted(FUSION,key=lambda a:-(a['m']-a['u'])):
    t5.append('%s & %s & %s & %s & %s & %.2f & %.2f & $+$%.2f \\\\' % (
        esc(r['study'].split(' (')[0])+' '+cite(r['ref']), esc(r['uni']), esc(r['multi']),
        esc(r['level']), r['n'] if r['n'] else 'NR', r['u'], r['m'], r['m']-r['u']))
g=[r['m']-r['u'] for r in FUSION]
t5+=['\\midrule',
 '\\multicolumn{7}{l}{\\textbf{Median gain} (range %.2f to %.2f, $k=%d$)} & \\textbf{$+$%.2f} \\\\'
 % (min(g),max(g),len(g),st.median(g)),'\\bottomrule','\\end{tabular}']
open(OUT+'tab5.tex','w').write('\n'.join(t5))

# ---------------- Table 6: within-study evaluation contrasts
t6=['\\begin{tabular}{L{3.1cm} L{4.35cm} L{2.35cm} C{1.2cm} C{1.4cm} C{1.4cm} C{1.3cm}}','\\toprule',
 '\\textbf{Study} & \\textbf{Contrast} & \\textbf{Source of the difference} & \\textbf{Metric} & '
 '\\textbf{Favourable} & \\textbf{Realistic} & \\textbf{Gap (pp)} \\\\','\\midrule']
for r in sorted(PROTOCOL,key=lambda a:-(a['hi']-a['lo'])):
    t6.append('%s & %s & %s & %s & %.2f & %.2f & %.2f \\\\' % (
        esc(r['study'].split(' (')[0])+' '+cite(r['ref']), esc(r['contrast']), esc(r['kind']),
        r['metric'], r['hi'], r['lo'], r['hi']-r['lo']))
d=[r['hi']-r['lo'] for r in PROTOCOL]
t6+=['\\midrule',
 '\\multicolumn{6}{l}{\\textbf{Median evaluation-induced gap} (range %.2f to %.2f, $k=%d$)} & '
 '\\textbf{%.2f} \\\\' % (min(d),max(d),len(d),st.median(d)),
 '\\multicolumn{6}{l}{Median within-study fusion gain for comparison ($k=%d$)} & %.2f \\\\'
 % (len(g),st.median(g)),'\\bottomrule','\\end{tabular}']
open(OUT+'tab6.tex','w').write('\n'.join(t6))

# ---------------- Table 3: reporting recoverability
items=list(RECOVER)
t3=['\\begin{tabular}{L{5.4cm} C{2.6cm} C{2.6cm} C{3.1cm}}','\\toprule',
 '\\textbf{Reporting item} & \\textbf{Recovered ($k$)} & \\textbf{Not recovered} & '
 '\\textbf{Recovery rate (\\%)} \\\\','\\midrule']
N=len(ATTEMPTED)
for k in items:
    v=len(RECOVER[k]); t3.append('%s & %d & %d & %.1f \\\\' % (esc(k),v,N-v,100*v/N))
t3+=['\\bottomrule','\\end{tabular}']
open(OUT+'tab3.tex','w').write('\n'.join(t3))
print('tables written; median acc %.2f; IQR %.2f-%.2f' % (
    st.median(acc), st.quantiles(acc,n=4)[0], st.quantiles(acc,n=4)[2]))
print('fusion median %.2f ; eval median %.2f ; ratio %.2f' % (
    st.median(g), st.median(d), st.median(d)/st.median(g)))
