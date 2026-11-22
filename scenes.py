import numpy as np, json
from PIL import Image
from pypdf import PdfReader
from pypdf.generic import ContentStream
Image.MAX_IMAGE_PIXELS=None
F='/mnt/user-data/uploads/5210b2a3-portfolio_062026_.pdf'
r=PdfReader(F); H=1125.0; W=2436.0
TUBE={305:'t01',308:'t02',309:'t03',310:'t04',324:'t05',22:'t06',30:'t07',261:'t08',38:'t09',40:'t10',42:'t11',44:'t12',58:'t13',87:'t14',95:'t15',280:'t16',282:'t17',228:'t18',242:'t19'}
PHOTO={24:'photos/me-cap',32:'photos/me-glasses'}
def mul(m,n):
    a,b,c,d,e,f=m; A,B,C,D,E,F_=n
    return [a*A+b*C, a*B+b*D, c*A+d*C, c*B+d*D, e*A+f*C+E, e*B+f*D+F_]
def scene(pn):
    pg=r.pages[pn-1]; xo=pg['/Resources']['/XObject']
    cs=ContentStream(pg.get_contents(),r)
    ctm=[1,0,0,1,0,0]; clip=None; path=[]; cur=(0,0); stack=[]; lastre=None; pending_re=False
    ev=[]; title_at=None; nimg=0
    for o,op in cs.operations:
        if op==b'q': stack.append((ctm[:],clip))
        elif op==b'Q': ctm,clip=stack.pop()
        elif op==b'cm': ctm=mul([float(x) for x in o],ctm)
        elif op==b're': lastre=[float(x) for x in o]; pending_re=True; path=[]
        elif op in (b'm',b'l',b'c',b'v',b'y',b'h'):
            pending_re=False
            if op==b'm': path=[]
            v=[float(x) for x in o]
            T=lambda x,y:(round(ctm[0]*x+ctm[2]*y+ctm[4],1),round(H-(ctm[1]*x+ctm[3]*y+ctm[5]),1))
            if op==b'm': cur=T(*v); path.append('M%s %s'%cur)
            elif op==b'l': cur=T(*v); path.append('L%s %s'%cur)
            elif op==b'c': a=T(v[0],v[1]);b=T(v[2],v[3]);cur2=T(v[4],v[5]); path.append('C%s %s %s %s %s %s'%(a+b+cur2)); cur=cur2
            elif op==b'v': b=T(v[0],v[1]);cur2=T(v[2],v[3]); path.append('C%s %s %s %s %s %s'%(cur+b+cur2)); cur=cur2
            elif op==b'y': a=T(v[0],v[1]);cur2=T(v[2],v[3]); path.append('C%s %s %s %s %s %s'%(a+cur2+cur2)); cur=cur2
            elif op==b'h': path.append('Z')
        elif op in (b'W',b'W*'):
            if pending_re and lastre:
                x,y,w,h=lastre
                if w<0: x+=w; w=-w
                if h<0: y+=h; h=-h
                # transform by ctm (assume no rotation for clip rects)
                a,b,c,d,e,f=ctm; X=a*x+e; Y=d*y+f
                if not (abs(w-W)<1 and abs(h-H)<1): clip=[X,H-(Y+d*h),a*w,d*h]
            elif path:
                clip=' '.join(path)
        elif op in (b'f',b'f*',b'BT') and title_at is None and nimg>1: title_at=len(ev)
        elif op==b'Do':
            ob=xo[o[0]].get_object(); 
            if ob.get('/Subtype')!='/Image': continue
            oid=xo.raw_get(o[0]).idnum; nimg+=1
            if oid==307: continue
            src=TUBE.get(oid) and 'assets/tubes/%s.webp'%TUBE[oid] or (oid in PHOTO and 'assets/%s.webp'%PHOTO[oid])
            if not src: continue
            a,b,c,d,e,f=ctm
            M=[a,-b,-c,d,c+e,H-d-f]
            ev.append(dict(src=src,m=[round(v,2) for v in M],clip=(clip if isinstance(clip,str) else [round(v,1) for v in clip]) if clip else None,tube=oid in TUBE))
    return ev,title_at
def title_layer(pn,name):
    im=np.asarray(Image.open(f'vec/T-{pn:02d}.png').convert('RGB')).astype(float)
    bg=np.array([17,21,255.]); dist=np.sqrt(((im-bg)**2).sum(-1)); al=np.clip(dist/90,0,1)
    rgb=np.where(al[...,None]>.02,(im-(1-al[...,None])*bg)/np.maximum(al[...,None],.02),0)
    o=Image.fromarray(np.dstack([np.clip(rgb,0,255),al*255]).astype('uint8'),'RGBA')
    # drop header/footer bands (small text at top/bottom 12%)
    h=o.height; arr=np.array(o); arr[:int(h*.12)]=0; arr[int(h*.88):]=0; o=Image.fromarray(arr)
    bb=o.getbbox(); o=o.crop(bb); o.save(f'site/assets/titles/{name}.webp',quality=92,lossless=False)
    s=o.width and 0.5
    return [bb[0]/2,bb[1]/2,(bb[2]-bb[0])/2,(bb[3]-bb[1])/2]
import os; os.makedirs('site/assets/titles',exist_ok=True)
out={}
for pn,name in [(1,'portfolio'),(5,'logos'),(9,'social'),(16,'report'),(20,'other'),(22,'thanks'),(3,'about'),(4,'skills')]:
    ev,ta=scene(pn); t=None
    if pn not in (3,4): t=title_layer(pn,name)
    out[name]=dict(ev=ev,title_at=ta,title=t)
    print(name,ta,t,[(e['src'][-8:],e['clip'] is not None) for e in ev])
json.dump(out,open('scenes.json','w'))
