import sys, csv, json, statistics as st
sys.path.insert(0, '/home/user/alvianil/manuscript/data')
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import MaxNLocator
from evidence import OUTCOMES, FUSION, PROTOCOL, ATTEMPTED, CORROBORATED, RECOVER

OUT = '/home/user/alvianil/manuscript/figures/'
plt.rcParams.update({
    'font.size': 16, 'axes.titlesize': 17, 'axes.labelsize': 16,
    'xtick.labelsize': 14.5, 'ytick.labelsize': 14.5, 'legend.fontsize': 14,
    'figure.dpi': 200, 'savefig.dpi': 400, 'savefig.bbox': 'tight',
    'axes.grid': True, 'grid.alpha': 0.25, 'grid.linestyle': ':',
    'axes.axisbelow': True, 'font.family': 'DejaVu Sans',
})
C = dict(blue='#2B6CB0', orange='#DD6B20', green='#2F855A', red='#C53030',
         purple='#6B46C1', teal='#2C7A7B', grey='#4A5568', gold='#B7791F',
         pink='#B83280', slate='#718096')

def panel(ax, letter):
    ax.text(-0.055, 1.045, f'({letter})', transform=ax.transAxes,
            fontsize=18, fontweight='bold', va='bottom', ha='right')

corpus = list(csv.DictReader(open('/home/user/alvianil/manuscript/data/corpus.csv')))
inc = [r for r in corpus if r['decision'] == 'include']
exc = [r for r in corpus if r['decision'] == 'exclude']

# ---------------------------------------------------------------- Figure 3
years = ['2022', '2023', '2024', '2025', '2026']
areas = ['Laboratory', 'Benchmark', 'Daily life', 'Occupational', 'Clinical',
         'Education', 'Driving', 'Aviation']
acol = [C['blue'], C['teal'], C['green'], C['orange'], C['red'], C['purple'],
        C['gold'], C['slate']]
M = np.array([[sum(1 for r in inc if r['year'] == y and r['area'] == a)
               for y in years] for a in areas], float)

fig, ax = plt.subplots(1, 2, figsize=(17.5, 6.6))
bot = np.zeros(len(years))
for i, a in enumerate(areas):
    ax[0].bar(years, M[i], bottom=bot, label=a, color=acol[i],
              edgecolor='white', linewidth=1.0)
    bot += M[i]
for x, t in zip(range(len(years)), bot):
    ax[0].text(x, t + 0.35, f'{int(t)}', ha='center', fontweight='bold', fontsize=15)
ax[0].set_xlabel('Publication year'); ax[0].set_ylabel('Number of included studies')
ax[0].set_title('Included studies by year and application area')
ax[0].set_ylim(0, bot.max() + 3.4)
ax[0].yaxis.set_major_locator(MaxNLocator(integer=True))
ax[0].legend(ncol=2, frameon=False, loc='upper left', fontsize=13)
panel(ax[0], 'a')

tot = M.sum(1); order = np.argsort(tot)
ax[1].barh([areas[i] for i in order], tot[order],
           color=[acol[i] for i in order], edgecolor='white', linewidth=1.0)
for i, v in enumerate(tot[order]):
    ax[1].text(v + 0.2, i, f'{int(v)}  ({v/tot.sum()*100:.0f}%)',
               va='center', fontsize=14)
ax[1].set_xlabel('Number of included studies')
ax[1].set_title('Application area of the included corpus')
ax[1].set_xlim(0, tot.max() * 1.32); ax[1].grid(axis='y', alpha=0)
panel(ax[1], 'b')
fig.tight_layout(); fig.savefig(OUT + 'fig3_corpus.png'); plt.close(fig)

# ---------------------------------------------------------------- Figure 4
RL = {'E1': 'Outside 2022-2026\nwindow', 'E2': 'Not a peer-reviewed\njournal article',
      'E3': 'Outcome outside\nstress / attention scope',
      'E4': 'No quantitative model\nevaluation'}
from collections import Counter
rc = Counter(r['reason'] for r in exc)
pubs = Counter(r['publisher'] for r in inc)

fig, ax = plt.subplots(1, 2, figsize=(17.5, 6.4))
k = ['E3', 'E4', 'E2', 'E1']
ax[0].bar([RL[x] for x in k], [rc[x] for x in k],
          color=[C['red'], C['orange'], C['gold'], C['slate']],
          edgecolor='white', linewidth=1.0)
for i, x in enumerate(k):
    ax[0].text(i, rc[x] + 0.7, f'{rc[x]}  ({rc[x]/len(exc)*100:.0f}%)',
               ha='center', fontweight='bold', fontsize=14.5)
ax[0].set_ylabel('Records excluded'); ax[0].set_ylim(0, max(rc.values()) + 6)
ax[0].yaxis.set_major_locator(MaxNLocator(integer=True))
ax[0].set_title(f'Reasons for exclusion at full-record appraisal (n = {len(exc)})')
ax[0].tick_params(axis='x', labelsize=13)
panel(ax[0], 'a')

pk = [p for p, _ in pubs.most_common()]
ax[1].bar(pk, [pubs[p] for p in pk], color=C['blue'], edgecolor='white', linewidth=1.0)
for i, p in enumerate(pk):
    ax[1].text(i, pubs[p] + 0.35, str(pubs[p]), ha='center',
               fontweight='bold', fontsize=14.5)
ax[1].set_ylabel('Included studies'); ax[1].set_ylim(0, max(pubs.values()) + 3.5)
ax[1].yaxis.set_major_locator(MaxNLocator(integer=True))
ax[1].set_title(f'Publisher of record for the included corpus (n = {len(inc)})')
ax[1].tick_params(axis='x', rotation=28, labelsize=13.5)
for lab in ax[1].get_xticklabels(): lab.set_ha('right')
panel(ax[1], 'b')
fig.tight_layout(); fig.savefig(OUT + 'fig4_screening.png'); plt.close(fig)
print('figures 3-4 done')

# ---------------------------------------------------------------- Figure 5
acc = [o for o in OUTCOMES if o['metric'] == 'Accuracy']
def fam(m):
    m = m.lower()
    if 'facial' in m: return 'Camera (rPPG /\nfacial video)'
    if 'eeg' in m and '+' in m: return 'EEG + peripheral'
    if 'eeg' in m: return 'EEG only'
    if m.count('+') >= 2: return 'Three or more\nchannels'
    if '+' in m: return 'Two channels'
    return 'Single PPG / BVP\nor ECG'
groups = {}
for o in acc: groups.setdefault(fam(o['mod']), []).append(o['value'])
keys = sorted(groups, key=lambda k: -st.median(groups[k]))
fig, ax = plt.subplots(figsize=(14.5, 7.4))
pos = np.arange(len(keys))
bp = ax.boxplot([groups[k] for k in keys], positions=pos, widths=0.55,
                patch_artist=True, medianprops=dict(color='black', lw=2.4),
                whiskerprops=dict(lw=1.5), capprops=dict(lw=1.5),
                flierprops=dict(marker=''))
for p, c in zip(bp['boxes'], [C['blue'], C['teal'], C['green'], C['orange'],
                              C['purple'], C['red']]):
    p.set_facecolor(c); p.set_alpha(0.32); p.set_edgecolor(c); p.set_linewidth(2)
rng = np.random.default_rng(7)
for i, k in enumerate(keys):
    v = groups[k]
    ax.scatter(np.full(len(v), i) + rng.uniform(-0.16, 0.16, len(v)), v,
               s=95, color=C['grey'], zorder=4, edgecolor='white', linewidth=1.2)
    ax.text(i, 101.6, f'k = {len(v)}', ha='center', fontsize=14, fontweight='bold')
    ax.text(i, 59.0, f'median\n{st.median(v):.1f}%', ha='center', fontsize=13.5,
            color=C['grey'])
ax.set_xticks(pos); ax.set_xticklabels(keys, fontsize=13.5)
ax.set_ylabel('Corroborated reported accuracy (%)')
ax.set_ylim(56, 105)
ax.set_title('Corroborated classification accuracy by sensing configuration')
ax.axhline(90, color=C['red'], ls='--', lw=1.8, alpha=0.8)
ax.text(len(keys) - 0.42, 90.6, '90% reference', color=C['red'], fontsize=13.5, ha='right')
fig.tight_layout(); fig.savefig(OUT + 'fig5_modality.png'); plt.close(fig)

# ---------------------------------------------------------------- Figure 6
w = [o for o in OUTCOMES if 'WESAD' in o['dataset']]
lab = [f"{o['study'].split(' et al')[0].split(' &')[0]}\n{o['year']} ({o['classes']}-cls)" for o in w]
val = [o['value'] for o in w]
prot = [o['protocol'] for o in w]
pc = {'LOSO': C['green'], 'Subject-independent': C['red'],
      'Personalized': C['purple'], 'NR': C['slate']}
idx = np.argsort(val)
fig, ax = plt.subplots(1, 2, figsize=(18, 7.0))
ax[0].barh(range(len(idx)), [val[i] for i in idx],
           color=[pc[prot[i]] for i in idx], edgecolor='white', linewidth=1.2)
ax[0].set_yticks(range(len(idx))); ax[0].set_yticklabels([lab[i] for i in idx], fontsize=13)
for j, i in enumerate(idx):
    ax[0].text(val[i] + 0.7, j, f'{val[i]:.2f}', va='center', fontsize=13.5,
               fontweight='bold')
ax[0].set_xlim(60, 106); ax[0].set_xlabel('Reported accuracy on WESAD (%)')
ax[0].set_title('WESAD results, ordered by reported accuracy')
ax[0].grid(axis='y', alpha=0)
hs = [plt.Rectangle((0, 0), 1, 1, color=pc[k]) for k in
      ['Personalized', 'NR', 'LOSO', 'Subject-independent']]
ax[0].legend(hs, ['Personalized (subject-dependent)', 'Protocol not reported',
                  'Leave-one-subject-out', 'Subject-independent generalized'],
             loc='upper center', bbox_to_anchor=(0.5, -0.16), ncol=2,
             frameon=False, fontsize=12.5)
panel(ax[0], 'a')

byp = {}
for v, p in zip(val, prot): byp.setdefault(p, []).append(v)
ordk = ['Personalized', 'NR', 'LOSO', 'Subject-independent']
ordk = [k for k in ordk if k in byp]
for i, k in enumerate(ordk):
    v = byp[k]
    ax[1].scatter(np.full(len(v), i) + rng.uniform(-0.1, 0.1, len(v)), v,
                  s=190, color=pc[k], edgecolor='white', linewidth=1.5, zorder=3)
    ax[1].hlines(st.median(v), i - 0.28, i + 0.28, color='black', lw=3, zorder=4)
    ax[1].text(i, 58.5, f'k = {len(v)}\nmed {st.median(v):.1f}%', ha='center', fontsize=13.5)
ax[1].set_xticks(range(len(ordk)))
ax[1].set_xticklabels(['Personalized', 'Not\nreported', 'LOSO', 'Subject-\nindependent'],
                      fontsize=14)
ax[1].set_ylabel('Reported accuracy on WESAD (%)'); ax[1].set_ylim(55, 104)
ax[1].set_title('The same benchmark, stratified by evaluation protocol')
ax[1].axhspan(92, 100, color=C['gold'], alpha=0.13)
ax[1].text(-0.42, 96.2, 'saturation\nband\n(92-100%)', fontsize=12.5,
           color=C['gold'], ha='left', va='center', fontweight='bold')
panel(ax[1], 'b')
fig.subplots_adjust(bottom=0.28, wspace=0.3); fig.savefig(OUT + 'fig6_wesad.png'); plt.close(fig)
print('figures 5-6 done')

# ---------------------------------------------------------------- Figure 7
fig, ax = plt.subplots(1, 2, figsize=(17.5, 7.0))
fs = sorted(FUSION, key=lambda r: r['m'] - r['u'])
lc = {'Feature-level': C['blue'], 'Decision-level': C['orange']}
for i, r in enumerate(fs):
    c = lc[r['level']]
    ax[0].plot([0, 1], [r['u'], r['m']], '-o', color=c, lw=3, ms=13,
               markeredgecolor='white', markeredgewidth=1.6, zorder=3)
    _dy = {2: 1.1, 1: -1.1}.get(i, 0.0)
    ax[0].annotate(f"{r['study'].split(' (')[0]}\n+{r['m']-r['u']:.2f} pp",
                   (1.035, r['m'] + _dy), fontsize=13.5, va='center', color=c,
                   fontweight='bold')
ax[0].set_xlim(-0.18, 1.75); ax[0].set_xticks([0, 1])
ax[0].set_xticklabels(['Best single\nmodality', 'Multimodal\nfusion'], fontsize=15)
ax[0].set_ylabel('Reported performance (%)')
ax[0].set_title('Within-study, protocol-matched fusion contrasts')
hs = [plt.Line2D([], [], color=lc[k], lw=3, marker='o', ms=10) for k in lc]
ax[0].legend(hs, list(lc), frameon=False, loc='lower left', fontsize=13.5)
panel(ax[0], 'a')

g = [r['m'] - r['u'] for r in fs]
nm = [r['study'].split(' (')[0] for r in fs]
ax[1].barh(range(len(g)), g, color=[lc[r['level']] for r in fs],
           edgecolor='white', linewidth=1.2)
for i, v in enumerate(g):
    ax[1].text(v + 0.28, i, f'+{v:.2f} pp', va='center', fontweight='bold', fontsize=14)
ax[1].set_yticks(range(len(g))); ax[1].set_yticklabels(nm, fontsize=13.5)
ax[1].axvline(st.median(g), color=C['red'], ls='--', lw=2.2)
ax[1].text(st.median(g) + 0.28, -0.62, f'median\n+{st.median(g):.2f} pp',
           color=C['red'], fontsize=13.5, fontweight='bold')
ax[1].set_xlabel('Gain over the best single modality (percentage points)')
ax[1].set_xlim(0, max(g) * 1.34); ax[1].set_ylim(-0.95, len(g) - 0.35)
ax[1].set_title('Magnitude of the corroborated fusion gain')
ax[1].grid(axis='y', alpha=0)
panel(ax[1], 'b')
fig.tight_layout(); fig.savefig(OUT + 'fig7_fusion.png'); plt.close(fig)

# ---------------------------------------------------------------- Figure 8
kinds = ['Personalization', 'Deployment setting', 'Task granularity', 'Dataset transfer']
kc = {'Personalization': C['purple'], 'Deployment setting': C['red'],
      'Task granularity': C['orange'], 'Dataset transfer': C['teal']}
fig, ax = plt.subplots(1, 2, figsize=(18, 7.2))
rows = sorted(PROTOCOL, key=lambda r: r['hi'] - r['lo'])
for i, r in enumerate(rows):
    d = r['hi'] - r['lo']
    ax[0].plot([r['lo'], r['hi']], [i, i], color=kc[r['kind']], lw=4, zorder=2)
    ax[0].scatter([r['lo'], r['hi']], [i, i], s=150, color=kc[r['kind']],
                  edgecolor='white', linewidth=1.5, zorder=3)
    ax[0].text(r['hi'] + 1.1, i, f'{d:.2f} pp', va='center', fontsize=13.5,
               fontweight='bold', color=kc[r['kind']])
ax[0].set_yticks(range(len(rows)))
ax[0].set_yticklabels([f"{r['study'].split(' (')[0]}\n{r['contrast']} [{r['metric']}]"
                       for r in rows], fontsize=12)
ax[0].set_xlabel('Reported performance (%)'); ax[0].set_xlim(38, 118)
ax[0].set_ylim(-1.5, len(rows) - 0.4)
ax[0].set_title('Within-study contrasts attributable to evaluation choices')
ax[0].grid(axis='y', alpha=0)
hs = [plt.Line2D([], [], color=kc[k], lw=4) for k in kinds]
ax[0].legend(hs, kinds, frameon=False, loc='upper center',
             bbox_to_anchor=(0.5, -0.13), ncol=4, fontsize=13)
panel(ax[0], 'a')

fg = [r['m'] - r['u'] for r in FUSION]
cats, vals, cols = ['Fusion'], [fg], [C['blue']]
for k in kinds:
    v = [r['hi'] - r['lo'] for r in PROTOCOL if r['kind'] == k]
    cats.append({'Personalization':'Personal-\nisation','Deployment setting':'Lab to\nfield','Task granularity':'Task\ngranularity','Dataset transfer':'Dataset\ntransfer'}[k]); vals.append(v); cols.append(kc[k])
for i, (v, c) in enumerate(zip(vals, cols)):
    ax[1].scatter(np.full(len(v), i) + rng.uniform(-0.09, 0.09, len(v)), v,
                  s=200, color=c, edgecolor='white', linewidth=1.6, zorder=3)
    ax[1].hlines(st.median(v), i - 0.3, i + 0.3, color='black', lw=3.2, zorder=4)
    ax[1].text(i, -4.2, f'k = {len(v)}\nmed {st.median(v):.1f}', ha='center', fontsize=13)
ax[1].axhline(st.median(fg), color=C['blue'], ls='--', lw=2.2, alpha=0.85)
ax[1].text(len(cats) - 0.45, st.median(fg) + 1.1,
           f'median fusion gain = {st.median(fg):.2f} pp', color=C['blue'],
           fontsize=13.5, fontweight='bold', ha='right')
ax[1].set_xticks(range(len(cats))); ax[1].set_xticklabels(cats, fontsize=13)
ax[1].set_xlim(-0.6, len(cats) - 0.4)
ax[1].set_ylabel('Within-study performance difference (pp)')
ax[1].set_ylim(-9, 56)
ax[1].set_title('Fusion gain against evaluation-induced differences')
panel(ax[1], 'b')
fig.subplots_adjust(bottom=0.24, wspace=0.42); fig.savefig(OUT + 'fig8_protocol_vs_fusion.png'); plt.close(fig)
print('figures 7-8 done')

# ---------------------------------------------------------------- Figure 9
fig, ax = plt.subplots(1, 2, figsize=(18.5, 6.8))
tr = [r for r in PROTOCOL if r['kind'] in ('Deployment setting', 'Dataset transfer')]
_short = {'Laboratory vs free-living': 'Lab vs free-living',
          'WESAD vs in-house cohort': 'WESAD vs in-house',
          'WESAD vs SWELL-KW': 'WESAD vs SWELL-KW',
          'WESAD vs Wellby real-world cohort': 'WESAD vs real world'}
nm = [f"{r['study'].split(' (')[0]}\n{_short[r['contrast']]}" for r in tr]
x = np.arange(len(tr)); wd = 0.36
ax[0].bar(x - wd/2, [r['hi'] for r in tr], wd, label='Development condition',
          color=C['blue'], edgecolor='white', linewidth=1.2)
ax[0].bar(x + wd/2, [r['lo'] for r in tr], wd, label='Transfer condition',
          color=C['red'], edgecolor='white', linewidth=1.2)
for i, r in enumerate(tr):
    ax[0].text(i - wd/2, r['hi'] + 0.7, f"{r['hi']:.1f}", ha='center', fontsize=13.5)
    ax[0].text(i + wd/2, r['lo'] + 0.7, f"{r['lo']:.1f}", ha='center', fontsize=13.5)
    ax[0].annotate(f"-{r['hi']-r['lo']:.1f} pp", (i, max(r['hi'], r['lo']) + 3.6),
                   ha='center', fontsize=14.5, fontweight='bold', color=C['red'])
ax[0].set_xticks(x); ax[0].set_xticklabels(nm, fontsize=13)
ax[0].set_xlim(-0.62, len(tr) - 0.38)
ax[0].set_ylabel('Reported performance (%)'); ax[0].set_ylim(55, 105)
ax[0].set_title('Loss on leaving the development condition')
ax[0].legend(frameon=False, loc='upper center', bbox_to_anchor=(0.5, -0.17),
             ncol=2, fontsize=13)
panel(ax[0], 'a')

sz = [(o['n'], o['value'], o['protocol']) for o in OUTCOMES
      if o['n'] and o['metric'] == 'Accuracy']
for n, v, p in sz:
    ax[1].scatter(n, v, s=200, color=pc.get(p, C['slate']), edgecolor='white',
                  linewidth=1.5, zorder=3)
xs = np.array([s[0] for s in sz], float); ys = np.array([s[1] for s in sz])
b, a = np.polyfit(np.log10(xs), ys, 1)
gx = np.logspace(np.log10(xs.min()), np.log10(xs.max()), 60)
ax[1].plot(gx, a + b * np.log10(gx), '--', color=C['grey'], lw=2.4)
r = np.corrcoef(np.log10(xs), ys)[0, 1]
ax[1].text(0.04, 0.06, f'slope = {b:+.1f} pp per decade\nPearson r = {r:+.2f}  (k = {len(sz)})',
           transform=ax[1].transAxes, fontsize=14, bbox=dict(fc='white', ec=C['grey'], alpha=0.9))
ax[1].set_xscale('log')
from matplotlib.ticker import FixedLocator, FixedFormatter
_t = [15, 20, 30, 50, 100, 200]
ax[1].xaxis.set_major_locator(FixedLocator(_t))
ax[1].xaxis.set_major_formatter(FixedFormatter([str(t) for t in _t]))
ax[1].xaxis.set_minor_formatter(plt.NullFormatter())
ax[1].set_xlabel('Participants in the evaluation cohort (log scale)')
ax[1].set_ylabel('Corroborated accuracy (%)'); ax[1].set_ylim(58, 104)
ax[1].set_title('Reported accuracy against evaluation cohort size')
panel(ax[1], 'b')
fig.subplots_adjust(bottom=0.3, wspace=0.28); fig.savefig(OUT + 'fig9_transfer.png'); plt.close(fig)

# ---------------------------------------------------------------- Figure 10
fig, ax = plt.subplots(1, 2, figsize=(17.5, 6.6))
nc = len(CORROBORATED); na = len(ATTEMPTED)
ax[0].bar(['Headline outcome\ncorroborated', 'Full text not openly\nretrievable'],
          [nc, na - nc], color=[C['green'], C['slate']],
          edgecolor='white', linewidth=1.2, width=0.55)
for i, v in enumerate([nc, na - nc]):
    ax[0].text(i, v + 0.45, f'{v}  ({v/na*100:.1f}%)', ha='center',
               fontweight='bold', fontsize=15)
ax[0].set_ylabel('Studies in the verification subsample')
ax[0].set_ylim(0, na * 0.82)
ax[0].yaxis.set_major_locator(MaxNLocator(integer=True))
ax[0].set_title(f'Independent corroboration of reported outcomes (n = {na})')
panel(ax[0], 'a')

fields = [k.replace(' size', '\nsize').replace('benchmark ', 'benchmark\n')
          .replace(' CI ', ' CI\n') for k in RECOVER]
ok = [len(v) for v in RECOVER.values()]
ax[1].barh(fields, [v / na * 100 for v in ok], color=C['blue'],
           edgecolor='white', linewidth=1.2)
for i, v in enumerate(ok):
    ax[1].text(v / na * 100 + 1.4, i, f'{v}/{na}  ({v/na*100:.0f}%)',
               va='center', fontsize=13.5, fontweight='bold')
ax[1].set_xlabel('Studies for which the item was recoverable (%)')
ax[1].set_xlim(0, 92); ax[1].grid(axis='y', alpha=0)
ax[1].set_title('Recoverability of reporting items from the public record')
ax[1].tick_params(axis='y', labelsize=13.5)
panel(ax[1], 'b')
fig.tight_layout(); fig.savefig(OUT + 'fig10_verifiability.png'); plt.close(fig)
print('figures 9-10 done')
