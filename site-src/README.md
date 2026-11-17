# Demo site source

The site is plain HTML/CSS/JS (no build step). The files at the root of this branch are the site itself: `index.html`, `style.css`, `app.js`, `vendor/` (three.js r160, MIT), `data/`, `img/`.

This folder has the scripts that produced `data/`:

- `pipeline.py`: preprocessing without FSL + prediction with `vgg16_ad.h5`.
  N4 bias correction, affine registration to MNI152 (ICBM 2009a) with SimpleITK, resample to the Harvard-Oxford 1 mm grid, skull strip with the MNI brain mask, hippocampus z-range from the Harvard-Oxford atlas, then the same slice/crop/resize/average code as `backend/images/functions.py`.
- `export.py`: writes the viewer volumes (uint8, gzip), brain/hippocampus meshes (marching cubes), the model-input sprite and `cases.json`. Predictions from `pipeline.py` stay local and are not written to `data/`.
- `qc.py`: quick registration/mask check image.

Requirements: Python 3.9, tensorflow 2.15, nibabel, nilearn, SimpleITK, scikit-image, scipy, pillow, xlrd.

```bash
python pipeline.py IXI158-Guys-0783-T1.nii.gz out/IXI158 vgg16_ad.h5 nilearn_data
python export.py out data IXI.xls IXI002 IXI158 IXI251 IXI607 IXI464
```

Scans: IXI T1 (https://brain-development.org/ixi-dataset/), CC BY-SA 3.0. No ADNI data is used or published here.
