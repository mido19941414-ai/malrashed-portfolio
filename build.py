import json,re
s=open('index.src.html').read()
svgs=json.load(open('svgs.json'))
for k,v in svgs.items(): s=s.replace('{{'+k+'}}',v)
assert '{{' not in s
open('../portfolio-website/index.html','w').write(s)
print('built',len(s))
