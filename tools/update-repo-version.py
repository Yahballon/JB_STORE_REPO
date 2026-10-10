#!/usr/bin/env python3
"""Generate JB STORE metadata version and file index (AI-assisted)."""
from pathlib import Path
import hashlib,json,subprocess
root=Path.cwd();files=[]
for folder in ('apps','games','media','tools','emu'):
 for path in sorted((root/'repo'/folder).rglob('*.json')):
  data=path.read_bytes();json.loads(data)
  files.append({'path':path.relative_to(root).as_posix(),'sha':hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()})
files.sort(key=lambda item:item['path'])
version=hashlib.sha256(json.dumps(files,sort_keys=True,separators=(',',':')).encode()).hexdigest()
target=root/'repo/version.json'
if target.exists() and json.loads(target.read_text()).get('version')==version:
 print('Repository metadata unchanged (AI-assisted)');raise SystemExit(0)
commit=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()
target.write_text(json.dumps({'schema':1,'version':version,'commit':commit,'files':files},indent=2)+'\n')
print(f'Repository manifest: {len(files)} entries, version={version} (AI-assisted)')
