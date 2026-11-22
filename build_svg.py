import json
S=json.load(open('scenes.json'))
from PIL import Image
def svg(name,vb=None,cls='stage'):
    s=S[name]; ev=s['ev']; ta=s['title_at']
    W,H=2436,1125
    vb=vb or (0,0,W,H)
    defs=[];body=[];k=0
    groups={}
    def key(e): return e['src']+str(e['m'][4:])  # same tube placement
    gi={}
    for i,e in enumerate(ev):
        kk=key(e)
        if kk not in gi: gi[kk]=len(gi)
    for i,e in enumerate(ev):
        if ta is not None and i==ta and s['title']:
            x,y,w,h=s['title']
            body.append(f'<g class="ttl"><image href="assets/titles/{name}.webp" x="{x}" y="{y}" width="{w}" height="{h}"/></g>')
        m=' '.join(map(str,e['m']))
        big = abs(e['m'][0])+abs(e['m'][1])>600
        cp=''
        if e['clip']:
            k+=1
            if isinstance(e['clip'],str): defs.append(f'<clipPath id="{name}c{k}"><path d="{e["clip"]}"/></clipPath>')
            else:
                x,y,w,h=e['clip']; defs.append(f'<clipPath id="{name}c{k}"><rect x="{x}" y="{y}" width="{w}" height="{h}"/></clipPath>')
            cp=f' clip-path="url(#{name}c{k})"'
        g=gi[key(e)]
        kind='photo' if 'photos' in e['src'] else ('big '+('L' if e['m'][4]<1218 else 'R') if big else 'sm')
        body.append(f'<g class="tb {kind} f{g%4}" data-k="{g}"><g{cp}><image href="{e["src"]}" width="1" height="1" preserveAspectRatio="none" transform="matrix({m})"/></g></g>')
    if ta is not None and ta>=len(ev) and s['title']:
        x,y,w,h=s['title'];body.append(f'<g class="ttl"><image href="assets/titles/{name}.webp" x="{x}" y="{y}" width="{w}" height="{h}"/></g>')
    return f'<svg class="{cls}" viewBox="{" ".join(map(str,vb))}" preserveAspectRatio="xMidYMid slice" aria-hidden="true"><defs>{"".join(defs)}</defs>{"".join(body)}</svg>'
out={n:svg(n) for n in ['portfolio','logos','social','report','other','thanks']}
out['about']=svg('about',(0,0,1100,1125),'portrait-svg')
out['skills']=svg('skills',(1100,0,1336,1125),'portrait-svg')
json.dump(out,open('svgs.json','w'),ensure_ascii=False)
print({k:len(v) for k,v in out.items()})
