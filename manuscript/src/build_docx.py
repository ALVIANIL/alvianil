import re, subprocess, os
os.chdir('/home/user/alvianil/manuscript/src')

def inline(path):
    s = open(path).read()
    def rep(m):
        f = m.group(1)
        if not f.endswith('.tex'): f += '.tex'
        return inline(f) if os.path.exists(f) else ''
    return re.sub(r'\\input\{([^}]+)\}', rep, s)

s = inline('main.tex')

# 1. TikZ pictures -> pre-rendered PNG
tikz = [m for m in re.finditer(
    r'\\resizebox\{[^}]*\}\{!\}\{\s*\\begin\{tikzpicture\}.*?\\end\{tikzpicture\}\s*\}',
    s, flags=re.S)]
for m, png in zip(reversed(tikz), ['fig2_prisma', 'fig1_block']):
    s = s[:m.start()] + '\\includegraphics[width=\\textwidth]{../figures/%s.png}' % png + s[m.end():]

# 2. unwrap resizebox around tabulars
s = re.sub(r'\\resizebox\{\\textwidth\}\{!\}\{%?\s*(\\begin\{tabular\})', r'\1', s)
s = re.sub(r'(\\end\{tabular\})\s*\}', r'\1', s)

# 3. custom column types -> plain p{} that pandoc understands
s = re.sub(r'[LC]\{([0-9.]+cm)\}', r'p{\1}', s)

# 4. resolve cross-references from the compiled .aux
labels = dict(re.findall(r'\\newlabel\{([^}]+)\}\{\{([^}]*)\}', open('main.aux').read()))
s = re.sub(r'\\ref\{([^}]+)\}', lambda m: labels.get(m.group(1), '?'), s)

# 5. number the captions explicitly (pandoc does not)
cf = ct = 0
def cap(m):
    global cf, ct
    env = m.group(1)
    if env == 'figure':
        cf += 1; tag = 'Figure %d: ' % cf
    else:
        ct += 1; tag = 'Table %d: ' % ct
    return m.group(0).replace('\\caption{', '\\caption{\\textbf{%s}' % tag, 1)
s = re.sub(r'\\begin\{(figure|table)\}\[H\].*?\\end\{\1\}', cap, s, flags=re.S)

# 4b. resolve \cite keys to Vancouver bracket numbers using the compiled .aux
aux = open('main.aux').read()
bibnum = {k: int(v) for k, v in re.findall(r'\\bibcite\{([^}]+)\}\{(\d+)\}', aux)}
def rng(ns):
    ns = sorted(set(ns)); out = []; i = 0
    while i < len(ns):
        j = i
        while j + 1 < len(ns) and ns[j + 1] == ns[j] + 1: j += 1
        out.append(str(ns[i]) if j - i < 2 else '%d\u2013%d' % (ns[i], ns[j]))
        i = j + 1
    return ','.join(out)
def citerep(m):
    ns = [bibnum[k.strip()] for k in m.group(1).split(',') if k.strip() in bibnum]
    return '[%s]' % rng(ns) if ns else ''
s = re.sub(r'\\cite\{([^}]*)\}', citerep, s)

# 4c. replace thebibliography with an explicitly numbered list
def bibrep(m):
    items = re.findall(r'\\bibitem\{([^}]+)\}\s*(.*?)(?=\\bibitem\{|\Z)',
                       m.group(1), flags=re.S)
    lines = ['[%d] %s' % (bibnum.get(k, 0), ' '.join(t.split()))
             for k, t in sorted(items, key=lambda kv: bibnum.get(kv[0], 0))]
    return '\\section*{References}\n\n' + '\n\n'.join(lines)
s = re.sub(r'\\begin\{thebibliography\}\{[^}]*\}(.*?)\\end\{thebibliography\}',
           bibrep, s, flags=re.S)
s = s.replace('\\setlength{\\itemsep}{1.5pt}\\small', '')
s = s.replace('\\renewcommand{\\refname}{References}', '')

# 5b. render simple inline math as plain text (keep LaTeX escapes intact)
SIMPLE = re.compile(r'^[0-9A-Za-z.,;:+\-/=<>()\s]*(\\%)?$')
def demath(m):
    t = m.group(1)
    return t if SIMPLE.match(t) else m.group(0)
s = re.sub(r'\$([^$]{1,40})\$', demath, s)

# 6. drop preamble constructs pandoc cannot use
s = re.sub(r'\\usetikzlibrary\{[^}]*\}', '', s)
s = re.sub(r'\\tikzset\{.*?\n\}\n', '', s, flags=re.S)
s = s.replace('\\thispagestyle{empty}', '').replace('\\setcounter{page}{1}', '')
s = s.replace('\\newpage', '\\clearpage')

open('main_docx.tex', 'w').write(s)
r = subprocess.run(['pandoc', 'main_docx.tex', '-f', 'latex', '-o',
                    '/home/user/alvianil/manuscript/Manuscript_BSPC.docx',
                    '--resource-path=.:..:../figures', '--wrap=none'],
                   capture_output=True, text=True)
print('pandoc rc', r.returncode, (r.stderr or '')[:800])
print('figures numbered:', cf, ' tables numbered:', ct)
