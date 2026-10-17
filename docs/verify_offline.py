from pathlib import Path
import json,hashlib,collections
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
root=Path(__file__).resolve().parents[1]
data=json.loads((root/'docs/saved-topology.json').read_text(encoding='utf8'))
assert hashlib.sha256((root/data['source']).read_bytes()).hexdigest()==data['sha256']
dev=data['devices'];links=data['links']; byid={d['id']:d for d in dev}
assert len(dev)==184 and len(links)==144
assert all(l['from'] in byid and l['to'] in byid for l in links)
print('Original PKT SHA-256 matches inspected snapshot:',data['sha256'])
print('Saved topology:',len(dev),'devices;',len(links),'cable links')
print('Device types:',json.dumps(dict(collections.Counter(d['type'] for d in dev)),sort_keys=True))
core={d['id']:d for d in dev if d['type'] in ['Router','Switch','MultiLayerSwitch','Server']}
fig,ax=plt.subplots(figsize=(13,10))
for l in links:
 if l['from'] in core and l['to'] in core:
  a,b=core[l['from']],core[l['to']];ax.plot([a['x'],b['x']],[-a['y'],-b['y']],color='#b1b9c4',lw=1,zorder=1)
colors={'Router':'#e76f51','Switch':'#457b9d','MultiLayerSwitch':'#8e44ad','Server':'#2a9d8f'}
for kind,color in colors.items():
 ds=[d for d in core.values() if d['type']==kind];ax.scatter([d['x'] for d in ds],[-d['y'] for d in ds],c=color,s=80,label=kind,zorder=2)
for d in core.values():ax.annotate(d['name'],(d['x'],-d['y']),xytext=(4,7),textcoords='offset points',fontsize=7)
ax.set_title('MapleTech saved topology — infrastructure devices and cable links',fontsize=14);ax.axis('off');ax.legend(loc='lower left')
fig.text(.5,.015,'Reconstruction from saved file metadata, not a Packet Tracer screenshot or live simulation. End devices omitted.',ha='center',fontsize=9)
assets=root/'docs/assets';assets.mkdir(exist_ok=True);fig.tight_layout(rect=(0,.03,1,1));fig.savefig(assets/'saved-topology.png',dpi=150);plt.close(fig)
print('PASS: source hash, saved metadata counts and link endpoints; infrastructure plot generated.')
print('NOT RUN: Packet Tracer simulation, DHCP lease acquisition, WAN ping/traceroute or service access.')
