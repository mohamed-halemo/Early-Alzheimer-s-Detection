import sys, numpy as np, glob, os
from PIL import Image
d=sys.argv[1]
v=np.load(os.path.join(d,'volumes.npz')); h=v['head']; m=v['mask']; hp=v['hippo']
h=np.clip(h/np.percentile(h,99.5)*255,0,255).astype(np.uint8)
def edge(a):
    e=np.zeros_like(a,bool); e[1:]|=a[1:]!=a[:-1]; e[:,1:]|=a[:,1:]!=a[:,:-1]; return e
def ov(img,mk,hpk):
    rgb=np.stack([img]*3,-1)
    rgb[edge(mk>0)]=[0,255,0]; rgb[hpk>0]=[255,60,60]; return rgb
ax=ov(h[:,:,60].T[::-1],m[:,:,60].T[::-1],hp[:,:,60].T[::-1])
co=ov(h[:,110,:].T[::-1],m[:,110,:].T[::-1],hp[:,110,:].T[::-1])
sa=ov(h[60,:,:].T[::-1],m[60,:,:].T[::-1],hp[60,:,:].T[::-1])
def pad(a,H=220,W=220):
    o=np.zeros((H,W,3),np.uint8); o[:a.shape[0],:a.shape[1]]=a; return o
row=np.concatenate([pad(ax),pad(co),pad(sa)],1)
sl=sorted(glob.glob(os.path.join(d,'slices','*.png')))
tiles=[np.array(Image.open(f)) for f in sl[::max(1,len(sl)//12)][:12]]
t=np.concatenate(tiles,1); t=np.stack([t]*3,-1)
W=max(row.shape[1],t.shape[1]); 
def padw(a): o=np.zeros((a.shape[0],W,3),np.uint8); o[:,:a.shape[1]]=a; return o
Image.fromarray(np.concatenate([padw(row),padw(t)],0)).save(sys.argv[2])
