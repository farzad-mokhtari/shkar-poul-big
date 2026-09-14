import json, urllib.request
from pathlib import Path
from datetime import datetime, timezone
URL='https://cdn.tsetmc.com/api/ClosingPrice/GetMarketWatch?market=0&paperTypes[0]=1&paperTypes[1]=2&paperTypes[2]=3&paperTypes[3]=4&paperTypes[4]=5&paperTypes[5]=6&paperTypes[6]=7&paperTypes[7]=8&paperTypes[8]=9&withBestLimits=false&hEven=0&RefID=0'
r=urllib.request.Request(URL,headers={'User-Agent':'Mozilla/5.0','Accept':'application/json'})
with urllib.request.urlopen(r,timeout=25) as x: raw=json.loads(x.read().decode('utf-8-sig'))
rows=raw.get('marketwatch', raw if isinstance(raw,list) else [])
out=[]
def n(v):
    try:return float(v or 0)
    except:return 0
for x in rows:
    if not isinstance(x,dict): continue
    out.append({'insCode':x.get('insCode',''),'symbol':x.get('lVal18AFC',''),'name':x.get('lVal30',''),'last':n(x.get('pDrCotVal')),'close':n(x.get('pClosing')),'volume':n(x.get('qTotTran5J')),'value':n(x.get('qTotCap')),'trades':n(x.get('zTotTran')),'flow':x.get('flow')})
Path('data/market.json').write_text(json.dumps({'ok':True,'source':'TSETMC public CDN','updatedAt':datetime.now(timezone.utc).isoformat(),'count':len(out),'items':out},ensure_ascii=False),encoding='utf8')
print(len(out))
