import re, sys
PAIRS = [
 ('behavioural','behavioral'),('Behavioural','Behavioral'),
 ('personalised','personalized'),('Personalised','Personalized'),
 ('personalisation','personalization'),('Personalisation','Personalization'),
 ('generalised','generalized'),('Generalised','Generalized'),
 ('generalisation','generalization'),('Generalisation','Generalization'),
 ('generalise','generalize'),
 ('optimising','optimizing'),('Optimising','Optimizing'),
 ('optimised','optimized'),('optimisation','optimization'),
 ('synthesised','synthesized'),('synthesise','synthesize'),('synthesises','synthesizes'),
 ('characterises','characterizes'),('characterise','characterize'),
 ('summarised','summarized'),('summarises','summarizes'),
 ('organised','organized'),('mobilises','mobilizes'),
 ('favourable','favorable'),('Favourable','Favorable'),
 ('coloured','colored'),('colour','color'),('colours','colors'),
 ('labelled','labeled'),('labelling','labeling'),
 ('modelling','modeling'),('normalisation','normalization'),
 ('utilise','utilize'),('utilised','utilized'),
 ('recognised','recognized'),('minimise','minimize'),('emphasise','emphasize'),
 ('analysed','analyzed'),('analyse','analyze'),
 ('centre','center'),('whilst','while'),('per cent','percent'),
]
def convert(t):
    for a,b in PAIRS:
        t = re.sub(r'\b%s\b' % re.escape(a), b, t)
    return t
for f in sys.argv[1:]:
    s = open(f).read(); n = convert(s)
    if n != s:
        open(f,'w').write(n); print('converted', f)
