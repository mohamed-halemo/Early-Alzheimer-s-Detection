"""Export pipeline outputs to static site assets.

usage: python -I export.py <out_dir> <site_data_dir> <ixi_xls> CASE [CASE ...]
"""
import gzip
import json
import os
import sys

import numpy as np
import xlrd
from PIL import Image
from scipy import ndimage
from skimage import measure

out_dir, data_dir, xls = sys.argv[1:4]
cases = sys.argv[4:]
os.makedirs(data_dir, exist_ok=True)

sheet = xlrd.open_workbook(xls).sheet_by_index(0)
meta = {}
for i in range(1, sheet.nrows):
    r = sheet.row_values(i)
    if r[11] != "":
        meta[int(r[0])] = {"sex": {1: "M", 2: "F"}.get(int(r[1]), "?"), "age": round(float(r[11]))}

SITES = {"Guys": "Guy's Hospital, Philips 1.5T", "HH": "Hammersmith Hospital, Philips 3T",
         "IOP": "Institute of Psychiatry, GE 1.5T"}


def write_gz(path, arr):
    with gzip.open(path, "wb", compresslevel=9) as f:
        f.write(np.ascontiguousarray(arr).tobytes())
    return os.path.getsize(path)


def mesh(vol, level, step, sigma):
    v = ndimage.gaussian_filter(vol.astype(np.float32), sigma)
    verts, faces, normals, _ = measure.marching_cubes(v, level, step_size=step)
    return verts, faces


def write_mesh(path, verts, faces, colorize):
    # header: nv, nf (uint32); positions uint16 (x10); colors uint8 rgb; faces uint32
    nv, nf = len(verts), len(faces)
    pos = np.round(verts * 10).astype(np.uint16)
    parts = [np.array([nv, nf], np.uint32).tobytes(), pos.tobytes()]
    if colorize:
        c = verts.mean(0)
        d = np.linalg.norm(verts - c, axis=1)
        # local depth: distance relative to smoothed radius -> gyri warm, sulci cool
        t = (d - np.percentile(d, 5)) / (np.percentile(d, 99) - np.percentile(d, 5))
        t = np.clip(t, 0, 1)
        cool = np.array([59, 76, 192]) / 255
        warm = np.array([220, 160, 140]) / 255
        col = (cool[None] * (1 - t[:, None]) + warm[None] * t[:, None]) * 255
        parts.append(col.astype(np.uint8).tobytes())
    parts.append(faces.astype(np.uint32).tobytes())
    with gzip.open(path, "wb", compresslevel=9) as f:
        f.write(b"".join(parts))
    return os.path.getsize(path)


index = []
shared_done = False
for case in cases:
    cdir = os.path.join(out_dir, case)
    res = json.load(open(os.path.join(cdir, "result.json")))
    v = np.load(os.path.join(cdir, "volumes.npz"))
    head, mask, hippo = v["head"], v["mask"], v["hippo"]
    shape = head.shape
    hi = np.percentile(head[mask > 0], 99.5)
    vol8 = np.clip(head / hi * 255, 0, 255).astype(np.uint8)
    vol8[vol8 < 6] = 0
    od = os.path.join(data_dir, case)
    os.makedirs(od, exist_ok=True)
    # volume stored with x fastest (Fortran order of (x,y,z)) -> C order of (z,y,x)
    sz = write_gz(os.path.join(od, "t1.u8.gz"), np.transpose(vol8, (2, 1, 0)))

    if not shared_done:
        write_gz(os.path.join(data_dir, "brainmask.u8.gz"), np.transpose(mask.astype(np.uint8), (2, 1, 0)))
        write_gz(os.path.join(data_dir, "hippo.u8.gz"), np.transpose(hippo.astype(np.uint8), (2, 1, 0)))
        hv, hf = mesh(hippo, 0.5, 1, 1.0)
        write_mesh(os.path.join(data_dir, "hippo.mesh.gz"), hv, hf, False)
        shared_done = True

    # brain surface
    brain = head * mask
    gm_level = np.percentile(brain[mask > 0], 25)
    seg = ndimage.binary_closing(brain > gm_level * 0.8, iterations=1)
    seg = ndimage.binary_fill_holes(seg)
    lab, n = ndimage.label(seg)
    sizes = ndimage.sum(seg, lab, range(1, n + 1))
    seg = lab == (1 + int(np.argmax(sizes)))
    bv, bf = mesh(seg, 0.5, 2, 0.8)
    msz = write_mesh(os.path.join(od, "brain.mesh.gz"), bv, bf, True)

    # model input sprite: N slices of 150x150 in a grid, 10 per row
    import glob
    files = sorted(glob.glob(os.path.join(cdir, "slices", "z*.png")))
    tiles = [np.array(Image.open(f)) for f in files]
    cols = 10
    rows = (len(tiles) + cols - 1) // cols
    sprite = np.zeros((rows * 150, cols * 150), np.uint8)
    for k, t in enumerate(tiles):
        r, c = divmod(k, cols)
        sprite[r * 150:(r + 1) * 150, c * 150:(c + 1) * 150] = t
    Image.fromarray(sprite).save(os.path.join(od, "inputs.jpg"), quality=85)

    sid = int(case[3:6])
    site = res["source"].split("-")[1]
    entry = {
        "id": case,
        "file": res["source"],
        "age": meta[sid]["age"],
        "sex": meta[sid]["sex"],
        "site": SITES.get(site, site),
        # predictions are not published; only the slice indices used as model input
        "slices": [s["z"] for s in res["slices"]],
    }
    index.append(entry)
    print(case, "t1 %.1fMB mesh %.1fMB faces %d" % (sz / 1e6, msz / 1e6, len(bf)))

json.dump({"shape": list(shape), "cases": index}, open(os.path.join(data_dir, "cases.json"), "w"),
          separators=(",", ":"))
