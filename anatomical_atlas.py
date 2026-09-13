
from pathlib import Path
import json, struct, numpy as np

def _simple_name(x):
    return str(x).strip().lower().replace("-","_").replace(" ","_")

def load_obj(path):
    V=[]; F=[]
    for line in Path(path).read_text(encoding="utf-8", errors="ignore").splitlines():
        if line.startswith("v "):
            p=line.split()
            if len(p)>=4: V.append([float(p[1]),float(p[2]),float(p[3])])
        elif line.startswith("f "):
            ids=[]
            for tok in line.split()[1:]:
                try: ids.append(int(tok.split("/")[0])-1)
                except: pass
            if len(ids)>=3:
                for i in range(1,len(ids)-1): F.append([ids[0],ids[i],ids[i+1]])
    return np.asarray(V,np.float32), np.asarray(F,np.int32)

def load_ascii_stl(path):
    V=[]; F=[]; lut={}
    def idx(p):
        k=tuple(round(float(x),7) for x in p)
        if k not in lut: lut[k]=len(V); V.append(list(k))
        return lut[k]
    tri=[]
    for line in Path(path).read_text(encoding="utf-8", errors="ignore").splitlines():
        s=line.strip().split()
        if len(s)==4 and s[0].lower()=="vertex":
            tri.append(idx([float(s[1]),float(s[2]),float(s[3])]))
            if len(tri)==3: F.append(tri); tri=[]
    return np.asarray(V,np.float32), np.asarray(F,np.int32)

def load_binary_stl(path):
    b=Path(path).read_bytes()
    if len(b)<84: return np.zeros((0,3),np.float32), np.zeros((0,3),np.int32)
    n=struct.unpack("<I",b[80:84])[0]; V=[]; F=[]; lut={}
    off=84
    def idx(p):
        k=tuple(round(float(x),7) for x in p)
        if k not in lut: lut[k]=len(V); V.append(list(k))
        return lut[k]
    for _ in range(n):
        if off+50>len(b): break
        vals=struct.unpack("<12fH",b[off:off+50]); off+=50
        tri=[idx(vals[3:6]),idx(vals[6:9]),idx(vals[9:12])]
        F.append(tri)
    return np.asarray(V,np.float32), np.asarray(F,np.int32)

def load_mesh(path):
    p=Path(path); ext=p.suffix.lower()
    if ext==".obj": return load_obj(p)
    if ext==".stl":
        head=p.read_bytes()[:80].lstrip().lower()
        return load_ascii_stl(p) if head.startswith(b"solid") else load_binary_stl(p)
    raise ValueError(f"Formato no soportado: {ext}. Use OBJ o STL.")

def _basis(a,b):
    d=np.asarray(b,float)-np.asarray(a,float); L=float(np.linalg.norm(d))
    if L<1e-8: return np.eye(3),1.0
    ez=d/L
    ref=np.array([0.,0.,1.]) if abs(ez[2])<.9 else np.array([0.,1.,0.])
    ex=np.cross(ez,ref); ex/=max(np.linalg.norm(ex),1e-9)
    ey=np.cross(ez,ex); ey/=max(np.linalg.norm(ey),1e-9)
    return np.stack([ex,ey,ez],axis=1),L

def register_mesh_to_segment(V, a, b):
    """Normaliza un atlas local y lo registra entre dos joints SKEL.
    Eje principal del atlas = eje de mayor varianza; se orienta proximal→distal.
    """
    V=np.asarray(V,float)
    if V.size==0: return V.astype(np.float32)
    c=V.mean(0); X=V-c
    _,_,vh=np.linalg.svd(X,full_matrices=False)
    ez=vh[0]/max(np.linalg.norm(vh[0]),1e-9)
    ref=vh[1] if len(vh)>1 else np.array([1.,0.,0.])
    ex=ref-np.dot(ref,ez)*ez; ex/=max(np.linalg.norm(ex),1e-9)
    ey=np.cross(ez,ex); ey/=max(np.linalg.norm(ey),1e-9)
    B0=np.stack([ex,ey,ez],axis=1)
    Q=X@B0
    zspan=float(np.ptp(Q[:,2])); zspan=max(zspan,1e-6)
    B,L=_basis(a,b)
    scale=L/zspan
    Q*=scale
    # proximal end to a
    Q[:,2]-=Q[:,2].min()
    return (np.asarray(a,float)+Q@B.T).astype(np.float32)

def load_atlas_registered(root, joints, joint_names):
    root=Path(root); man=json.loads((root/"manifest.json").read_text(encoding="utf-8"))
    J=np.asarray(joints,np.float32); names=[str(x) for x in joint_names]
    nm={_simple_name(n):i for i,n in enumerate(names)}
    out={"bones":[],"muscles":[],"missing":[],"version":man.get("atlas_version","")}
    for group,key in [("bones","bones"),("muscles","muscles")]:
        for s in man.get(key,[]):
            f=root/s["file"]; a=nm.get(_simple_name(s["proximal"])); b=nm.get(_simple_name(s["distal"]))
            if not f.exists():
                out["missing"].append(s["file"]); continue
            if a is None or b is None:
                out["missing"].append(s["id"]+" [joint mapping]"); continue
            V,F=load_mesh(f)
            seq=np.stack([register_mesh_to_segment(V,J[t,a],J[t,b]) for t in range(J.shape[0])])
            out[group].append({"id":s["id"],"V":seq,"F":F})
    return out


# === V110.3.20.15 · BodyParts3D real anatomical asset manager ===
# Geometry source: BodyParts3D / Anatomography, DBCLS.
# Mirror used at runtime: Kevin-Mattheus-Moerman/BodyParts3D.
# Geometry license: CC BY-SA 2.1 Japan.
# No procedural anatomy is generated as fallback.

import os as _os, tempfile as _tempfile, urllib.request as _urlreq, urllib.error as _urlerr, re as _re

_BP3D_REPO="Kevin-Mattheus-Moerman/BodyParts3D"
_BP3D_BRANCH="main"
_BP3D_API=f"https://api.github.com/repos/{_BP3D_REPO}/git/trees/{_BP3D_BRANCH}?recursive=1"
_BP3D_RAW=f"https://raw.githubusercontent.com/{_BP3D_REPO}/{_BP3D_BRANCH}"
_BP3D_CREDIT="BodyParts3D, © The Database Center for Life Science licensed under CC Attribution-Share Alike 2.1 Japan"

# Requested structures. Multiple aliases allow metadata wording differences.
_BP3D_TARGETS=[
    # Bones
    dict(group="bones", id="hip_bone_r", side="r", aliases=["right hip bone"], proximal="pelvis", distal="femur_r"),
    dict(group="bones", id="hip_bone_l", side="l", aliases=["left hip bone"], proximal="pelvis", distal="femur_l"),
    dict(group="bones", id="femur_r", aliases=["right femur"], proximal="femur_r", distal="tibia_r"),
    dict(group="bones", id="femur_l", aliases=["left femur"], proximal="femur_l", distal="tibia_l"),
    dict(group="bones", id="patella_r", aliases=["right patella"], proximal="femur_r", distal="tibia_r"),
    dict(group="bones", id="patella_l", aliases=["left patella"], proximal="femur_l", distal="tibia_l"),
    dict(group="bones", id="tibia_r", aliases=["right tibia"], proximal="tibia_r", distal="talus_r"),
    dict(group="bones", id="tibia_l", aliases=["left tibia"], proximal="tibia_l", distal="talus_l"),
    dict(group="bones", id="fibula_r", aliases=["right fibula"], proximal="tibia_r", distal="talus_r"),
    dict(group="bones", id="fibula_l", aliases=["left fibula"], proximal="tibia_l", distal="talus_l"),
    dict(group="bones", id="talus_r", aliases=["right talus"], proximal="talus_r", distal="calcn_r"),
    dict(group="bones", id="talus_l", aliases=["left talus"], proximal="talus_l", distal="calcn_l"),
    dict(group="bones", id="calcaneus_r", aliases=["right calcaneus"], proximal="calcn_r", distal="toes_r"),
    dict(group="bones", id="calcaneus_l", aliases=["left calcaneus"], proximal="calcn_l", distal="toes_l"),
    dict(group="bones", id="humerus_r", aliases=["right humerus"], proximal="humerus_r", distal="ulna_r"),
    dict(group="bones", id="humerus_l", aliases=["left humerus"], proximal="humerus_l", distal="ulna_l"),
    dict(group="bones", id="radius_r", aliases=["right radius"], proximal="radius_r", distal="hand_r"),
    dict(group="bones", id="radius_l", aliases=["left radius"], proximal="radius_l", distal="hand_l"),
    dict(group="bones", id="ulna_r", aliases=["right ulna"], proximal="ulna_r", distal="hand_r"),
    dict(group="bones", id="ulna_l", aliases=["left ulna"], proximal="ulna_l", distal="hand_l"),
    dict(group="bones", id="scapula_r", aliases=["right scapula"], proximal="thorax", distal="scapula_r"),
    dict(group="bones", id="scapula_l", aliases=["left scapula"], proximal="thorax", distal="scapula_l"),
    dict(group="bones", id="clavicle_r", aliases=["right clavicle"], proximal="thorax", distal="scapula_r"),
    dict(group="bones", id="clavicle_l", aliases=["left clavicle"], proximal="thorax", distal="scapula_l"),

    # Major muscles - real source meshes, not synthetic bundles
    dict(group="muscles", id="gluteus_maximus_r", aliases=["right gluteus maximus"], proximal="pelvis", distal="femur_r"),
    dict(group="muscles", id="gluteus_maximus_l", aliases=["left gluteus maximus"], proximal="pelvis", distal="femur_l"),
    dict(group="muscles", id="gluteus_medius_r", aliases=["right gluteus medius"], proximal="pelvis", distal="femur_r"),
    dict(group="muscles", id="gluteus_medius_l", aliases=["left gluteus medius"], proximal="pelvis", distal="femur_l"),
    dict(group="muscles", id="iliacus_r", aliases=["right iliacus"], proximal="pelvis", distal="femur_r"),
    dict(group="muscles", id="iliacus_l", aliases=["left iliacus"], proximal="pelvis", distal="femur_l"),
    dict(group="muscles", id="psoas_major_r", aliases=["right psoas major"], proximal="pelvis", distal="femur_r"),
    dict(group="muscles", id="psoas_major_l", aliases=["left psoas major"], proximal="pelvis", distal="femur_l"),
    dict(group="muscles", id="rectus_femoris_r", aliases=["right rectus femoris"], proximal="femur_r", distal="tibia_r"),
    dict(group="muscles", id="rectus_femoris_l", aliases=["left rectus femoris"], proximal="femur_l", distal="tibia_l"),
    dict(group="muscles", id="vastus_lateralis_r", aliases=["right vastus lateralis"], proximal="femur_r", distal="tibia_r"),
    dict(group="muscles", id="vastus_lateralis_l", aliases=["left vastus lateralis"], proximal="femur_l", distal="tibia_l"),
    dict(group="muscles", id="vastus_medialis_r", aliases=["right vastus medialis"], proximal="femur_r", distal="tibia_r"),
    dict(group="muscles", id="vastus_medialis_l", aliases=["left vastus medialis"], proximal="femur_l", distal="tibia_l"),
    dict(group="muscles", id="biceps_femoris_r", aliases=["right biceps femoris"], proximal="pelvis", distal="tibia_r"),
    dict(group="muscles", id="biceps_femoris_l", aliases=["left biceps femoris"], proximal="pelvis", distal="tibia_l"),
    dict(group="muscles", id="semitendinosus_r", aliases=["right semitendinosus"], proximal="pelvis", distal="tibia_r"),
    dict(group="muscles", id="semitendinosus_l", aliases=["left semitendinosus"], proximal="pelvis", distal="tibia_l"),
    dict(group="muscles", id="semimembranosus_r", aliases=["right semimembranosus"], proximal="pelvis", distal="tibia_r"),
    dict(group="muscles", id="semimembranosus_l", aliases=["left semimembranosus"], proximal="pelvis", distal="tibia_l"),
    dict(group="muscles", id="gastrocnemius_r", aliases=["right gastrocnemius"], proximal="tibia_r", distal="calcn_r"),
    dict(group="muscles", id="gastrocnemius_l", aliases=["left gastrocnemius"], proximal="tibia_l", distal="calcn_l"),
    dict(group="muscles", id="soleus_r", aliases=["right soleus"], proximal="tibia_r", distal="calcn_r"),
    dict(group="muscles", id="soleus_l", aliases=["left soleus"], proximal="tibia_l", distal="calcn_l"),
    dict(group="muscles", id="tibialis_anterior_r", aliases=["right tibialis anterior"], proximal="tibia_r", distal="toes_r"),
    dict(group="muscles", id="tibialis_anterior_l", aliases=["left tibialis anterior"], proximal="tibia_l", distal="toes_l"),
    dict(group="muscles", id="fibularis_longus_r", aliases=["right fibularis longus","right peroneus longus"], proximal="tibia_r", distal="toes_r"),
    dict(group="muscles", id="fibularis_longus_l", aliases=["left fibularis longus","left peroneus longus"], proximal="tibia_l", distal="toes_l"),
    dict(group="muscles", id="deltoid_r", aliases=["right deltoid"], proximal="scapula_r", distal="humerus_r"),
    dict(group="muscles", id="deltoid_l", aliases=["left deltoid"], proximal="scapula_l", distal="humerus_l"),
    dict(group="muscles", id="biceps_brachii_r", aliases=["right biceps brachii"], proximal="humerus_r", distal="radius_r"),
    dict(group="muscles", id="biceps_brachii_l", aliases=["left biceps brachii"], proximal="humerus_l", distal="radius_l"),
    dict(group="muscles", id="triceps_brachii_r", aliases=["right triceps brachii"], proximal="humerus_r", distal="ulna_r"),
    dict(group="muscles", id="triceps_brachii_l", aliases=["left triceps brachii"], proximal="humerus_l", distal="ulna_l"),
]

def _http_bytes(url, timeout=25):
    req=_urlreq.Request(url,headers={"User-Agent":"PhysioSentinel-Gait/110.3.20.15"})
    with _urlreq.urlopen(req,timeout=timeout) as r:
        return r.read()

def _bp3d_cache_root():
    p=Path(_tempfile.gettempdir())/"physiosentinel_bodyparts3d_atlas_v2015"
    (p/"bones").mkdir(parents=True,exist_ok=True)
    (p/"muscles").mkdir(parents=True,exist_ok=True)
    return p

def _parse_fma_metadata(text):
    # Accept common tab/comma/whitespace separated BodyParts3D metadata layouts.
    out={}
    for line in text.splitlines():
        s=line.strip()
        if not s or s.startswith("#"): continue
        # Find FMA id anywhere near beginning and retain remaining text as name.
        m=_re.search(r'\b(?:FMA)?(\d{3,7})\b',s,re.I)
        if not m: continue
        fid=m.group(1)
        tail=s[m.end():].strip(" \t,;|\"'")
        # strip additional codes/columns before readable English name
        parts=[x.strip(" \"'") for x in _re.split(r'[\t|,;]+',tail) if x.strip(" \"'")]
        candidates=parts[::-1] if parts else [tail]
        name=max(candidates,key=lambda x: sum(ch.isalpha() for ch in x),default=tail).strip()
        if name:
            out[name.lower()]=fid
    return out

def _resolve_bodyparts3d_index():
    """Discover metadata and STL paths from repository tree. No fixed asset filename assumptions."""
    tree=json.loads(_http_bytes(_BP3D_API).decode("utf-8"))
    paths=[x.get("path","") for x in tree.get("tree",[]) if x.get("type")=="blob"]
    stls={Path(p).name.lower():p for p in paths if p.lower().endswith(".stl")}
    txts=[p for p in paths if p.lower().startswith("assets/") and p.lower().endswith((".txt",".csv",".tsv"))]
    names={}
    for p in txts:
        try:
            t=_http_bytes(f"{_BP3D_RAW}/{p}").decode("utf-8",errors="ignore")
            names.update(_parse_fma_metadata(t))
        except Exception:
            continue
    return names,stls

def _lookup_fma(names, aliases):
    # exact normalized first, then conservative contains match
    def norm(s):
        return " ".join(_re.sub(r"[^a-z0-9]+"," ",str(s).lower()).split())
    norm_names={norm(k):v for k,v in names.items()}
    for alias in aliases:
        n=norm(alias)
        if n in norm_names: return norm_names[n]
    for alias in aliases:
        n=norm(alias)
        matches=[(k,v) for k,v in norm_names.items() if k==n or k.endswith(" "+n) or n in k]
        if len(matches)==1: return matches[0][1]
    return None

def ensure_bodyparts3d_atlas(force=False):
    """Download/cache a clinically focused real atlas subset. Returns status dict.
    Cache is runtime /tmp only; nothing is sent to Supabase.
    """
    root=_bp3d_cache_root()
    man_path=root/"manifest.json"
    if man_path.exists() and not force:
        try:
            man=json.loads(man_path.read_text(encoding="utf-8"))
            n=sum(1 for g in ("bones","muscles") for s in man.get(g,[]) if (root/s["file"]).exists())
            if n>=8:
                return {"ok":True,"root":str(root),"downloaded":0,"available":n,"missing":man.get("missing_sources",[]),"cached":True}
        except Exception:
            pass
    names,stls=_resolve_bodyparts3d_index()
    groups={"bones":[],"muscles":[]}; missing=[]; downloaded=0
    for spec in _BP3D_TARGETS:
        fid=_lookup_fma(names,spec["aliases"])
        if not fid:
            missing.append(spec["id"]+" [name not resolved]"); continue
        key=f"fma{fid}.stl".lower()
        remote_path=stls.get(key)
        if not remote_path:
            # tolerate leading zeros or case/path variations
            cand=[p for nm,p in stls.items() if nm==key or nm.endswith(f"{fid}.stl")]
            remote_path=cand[0] if cand else None
        if not remote_path:
            missing.append(spec["id"]+f" [FMA{fid} STL not found]"); continue
        local_rel=f'{spec["group"]}/{spec["id"]}.stl'
        local=root/local_rel
        if force or not local.exists() or local.stat().st_size<84:
            try:
                raw=_http_bytes(f"{_BP3D_RAW}/{remote_path}",timeout=40)
                if len(raw)<84: raise ValueError("STL vacío/corrupto")
                local.write_bytes(raw); downloaded+=1
            except Exception as exc:
                missing.append(spec["id"]+f" [download: {type(exc).__name__}]"); continue
        item={k:v for k,v in spec.items() if k not in ("group","aliases","side")}
        item["file"]=local_rel
        item["source_fma"]="FMA"+str(fid)
        item["source_name"]=spec["aliases"][0]
        groups[spec["group"]].append(item)
    man={
        "atlas_version":"BodyParts3D_runtime_v2015",
        "mode":"STRICT_REAL_MESH",
        "source":"BodyParts3D / Anatomography",
        "source_mirror":f"https://github.com/{_BP3D_REPO}",
        "license":"CC BY-SA 2.1 Japan",
        "credit":_BP3D_CREDIT,
        "bones":groups["bones"],"muscles":groups["muscles"],
        "missing_sources":missing,
    }
    man_path.write_text(json.dumps(man,indent=2,ensure_ascii=False),encoding="utf-8")
    available=len(groups["bones"])+len(groups["muscles"])
    return {"ok":available>0,"root":str(root),"downloaded":downloaded,"available":available,"missing":missing,"cached":False}

def bodyparts3d_atlas_status():
    root=_bp3d_cache_root(); mp=root/"manifest.json"
    if not mp.exists(): return {"ready":False,"root":str(root),"bones":0,"muscles":0,"missing":[]}
    try:
        man=json.loads(mp.read_text(encoding="utf-8"))
        b=sum(1 for s in man.get("bones",[]) if (root/s["file"]).exists())
        m=sum(1 for s in man.get("muscles",[]) if (root/s["file"]).exists())
        return {"ready":(b+m)>0,"root":str(root),"bones":b,"muscles":m,"missing":man.get("missing_sources",[])}
    except Exception as exc:
        return {"ready":False,"root":str(root),"bones":0,"muscles":0,"missing":[str(exc)]}
