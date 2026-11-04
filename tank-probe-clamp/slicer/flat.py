import json,glob,os,sys
R=r"C:/Program Files/OrcaSlicer/resources/profiles"
idx={}
for f in glob.glob(R+"/**/*.json",recursive=True):
    try: j=json.load(open(f,encoding='utf-8'))
    except: continue
    if isinstance(j,dict) and 'name' in j: idx.setdefault((os.path.basename(os.path.dirname(f)),j['name']),j)
def flat(kind,name):
    j=idx[(kind,name)]; base=flat(kind,j['inherits']) if j.get('inherits') else {}
    base.update({k:v for k,v in j.items() if k!='inherits'}); return base
out=sys.argv[1]
for kind,name,fn in [('machine','Creality Ender-3 V3 SE 0.4 nozzle','m.json'),('process','0.20mm Standard @Creality Ender3V3SE 0.4','p.json'),('filament','Creality Generic PLA @Ender-3V3-all','f.json')]:
    d=flat(kind,name)
    if kind=='filament': d['compatible_printers']=[]
    if kind=='process': d['compatible_printers']=[]; d['wall_loops']='3'; d['sparse_infill_density']='20%'
    json.dump(d,open(os.path.join(out,fn),'w'),indent=1)
    print(kind,name,len(d),'keys')
