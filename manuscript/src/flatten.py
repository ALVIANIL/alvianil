import re, os
os.chdir('/home/user/alvianil/manuscript/src')

def inline(path):
    s = open(path).read()
    def rep(m):
        f = m.group(1)
        if not f.endswith('.tex'): f += '.tex'
        return inline(f) if os.path.exists(f) else m.group(0)
    return re.sub(r'\\input\{([^}]+)\}', rep, s)

s = inline('main.tex')
# figures live next to the .tex in the distributed package
s = s.replace('{../figures/', '{figures/')
hdr = ('%% Evaluation Protocol Outweighs Multimodal Fusion in Wearable and Camera-Based\n'
       '%% Stress and Attention Monitoring: A Systematic Review with Within-Study Meta-Analysis\n'
       '%%\n'
       '%% Self-contained LaTeX source. Compile with:\n'
       '%%     pdflatex Manuscript_BSPC.tex && pdflatex Manuscript_BSPC.tex\n'
       '%% Requires: texlive-latex-extra, texlive-pictures, texlive-fonts-recommended.\n'
       '%% Keep the figures/ directory alongside this file.\n\n')
open('/home/user/alvianil/manuscript/Manuscript_BSPC.tex', 'w').write(hdr + s)
print('flattened lines:', (hdr + s).count('\n'))
