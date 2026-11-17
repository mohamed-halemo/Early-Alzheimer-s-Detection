"""Approximate BrainAware preprocessing without FSL, then run vgg16_ad.h5.

Steps (per scan):
  1. N4 bias correction (ADNI inputs were N3-corrected).
  2. Affine registration to MNI152 (ICBM 2009a with skull) with SimpleITK
     (the original notebook used elastix affine).
  3. Resample into the Harvard-Oxford 1mm grid (182x218x182).
  4. Skull strip with the MNI brain mask (stand-in for FSL BET).
  5. Hippocampus mask = Harvard-Oxford Left/Right Hippocampus (stand-in for FSL FIRST).
  6. Axial slices across the hippocampus z-range, crop non-zero, scale 0-255,
     resize 150x150, predict, average (same code as backend/images/functions.py).

usage: python -I pipeline.py <in.nii.gz> <out_dir> <weights.h5> <nilearn_dir>
"""
import json
import os
import sys

import numpy as np
import nibabel as nib
import SimpleITK as sitk
from PIL import Image

src, out_dir, weights, nl_dir = sys.argv[1:5]
os.makedirs(out_dir, exist_ok=True)

icbm_dir = os.path.join(nl_dir, "icbm152_2009", "mni_icbm152_nlin_sym_09a")
ICBM_T1 = os.path.join(icbm_dir, "mni_icbm152_t1_tal_nlin_sym_09a.nii.gz")
ICBM_MASK = os.path.join(icbm_dir, "mni_icbm152_t1_tal_nlin_sym_09a_mask.nii.gz")

from nilearn import datasets  # noqa: E402

ho = datasets.fetch_atlas_harvard_oxford("sub-maxprob-thr25-1mm", data_dir=nl_dir, verbose=0)
ho_img = ho.maps if hasattr(ho.maps, "affine") else nib.load(ho.maps)
ho_data = np.asarray(ho_img.dataobj).astype(np.int16)
labels = list(ho.labels)
hippo_ids = [labels.index("Left Hippocampus"), labels.index("Right Hippocampus")]
hippo = np.isin(ho_data, hippo_ids).astype(np.uint8)

# Reference grid as a SimpleITK image (HO grid, RAS affine in nibabel terms)
ho_ref_path = os.path.join(out_dir, "_ho_ref.nii.gz")
nib.save(nib.Nifti1Image(ho_data.astype(np.float32), ho_img.affine), ho_ref_path)
ref = sitk.ReadImage(ho_ref_path, sitk.sitkFloat32)
os.remove(ho_ref_path)

# 1. N4
moving = sitk.ReadImage(src, sitk.sitkFloat32)
shrink = 4
small = sitk.Shrink(moving, [shrink] * 3)
head = sitk.OtsuThreshold(small, 0, 1, 200)
n4 = sitk.N4BiasFieldCorrectionImageFilter()
n4.SetMaximumNumberOfIterations([50, 50, 30])
n4.Execute(small, head)
log_bias = n4.GetLogBiasFieldAsImage(moving)
moving = sitk.Cast(moving / sitk.Cast(sitk.Exp(log_bias), sitk.sitkFloat32), sitk.sitkFloat32)

# 2. Affine registration to MNI152 head template
fixed = sitk.ReadImage(ICBM_T1, sitk.sitkFloat32)


def run_reg(transform, iters):
    R = sitk.ImageRegistrationMethod()
    R.SetMetricAsMattesMutualInformation(32)
    R.SetMetricSamplingStrategy(R.RANDOM)
    R.SetMetricSamplingPercentage(0.15, seed=42)
    R.SetInterpolator(sitk.sitkLinear)
    R.SetOptimizerAsRegularStepGradientDescent(1.0, 1e-4, iters, relaxationFactor=0.6)
    R.SetOptimizerScalesFromPhysicalShift()
    R.SetShrinkFactorsPerLevel([4, 2, 1])
    R.SetSmoothingSigmasPerLevel([2, 1, 0])
    R.SetInitialTransform(transform, inPlace=False)
    t = R.Execute(fixed, moving)
    return t, R.GetMetricValue()


rigid0 = sitk.CenteredTransformInitializer(
    fixed, moving, sitk.Euler3DTransform(), sitk.CenteredTransformInitializerFilter.MOMENTS)
rigid, m1 = run_reg(rigid0, 200)
rigid = sitk.CompositeTransform(rigid).GetNthTransform(0) if isinstance(rigid, sitk.CompositeTransform) else rigid
aff0 = sitk.AffineTransform(3)
eul = sitk.Euler3DTransform(rigid)
aff0.SetMatrix(eul.GetMatrix())
aff0.SetTranslation(eul.GetTranslation())
aff0.SetCenter(eul.GetCenter())
affine_t, m2 = run_reg(aff0, 300)
print("metric rigid %.4f affine %.4f" % (m1, m2))

# 3. Resample into HO grid
reg = sitk.Resample(moving, ref, affine_t, sitk.sitkLinear, 0.0, sitk.sitkFloat32)
mask_icbm = sitk.ReadImage(ICBM_MASK, sitk.sitkFloat32)
brain_mask = sitk.Resample(mask_icbm, ref, sitk.Transform(), sitk.sitkLinear, 0.0)
# back to numpy in HO voxel order (x, y, z); sitk arrays are (z, y, x)
reg_np = np.transpose(sitk.GetArrayFromImage(reg), (2, 1, 0)).astype(np.float32)
mask_np = (np.transpose(sitk.GetArrayFromImage(brain_mask), (2, 1, 0)) > 0.5).astype(np.float32)
# sitk reads the nibabel RAS affine as LPS physical space; voxel order is preserved.

# 4. Skull strip (image * brain mask), as in skull_stripping()
skull_stripped = reg_np * mask_np


# 6. Same slice code as backend Hippo_slices / preprocess_images
def cropping(img):
    if np.count_nonzero(img) == 0:
        return img
    xs, ys = np.where(img != 0)
    return img[min(xs):max(xs) + 1, min(ys):max(ys) + 1]


_, _, zs = np.where(hippo != 0)
slices, zlist = [], []
for i in range(zs.min(), zs.max() + 1):
    im = np.asarray(skull_stripped[:, :, i])
    im = cropping(im)
    im = np.abs(((im - im.min()) / (im.max() - im.min())) * 255)
    slices.append(Image.fromarray(im).convert("L"))
    zlist.append(int(i))

target = (150, 150)
batch = np.empty((len(slices),) + target, dtype=np.float32)
for k, s in enumerate(slices):
    batch[k] = np.array(s.resize(target), dtype=np.float32)
batch /= 255.0
batch = np.repeat(batch[..., None], 3, axis=-1)

from tensorflow import keras  # noqa: E402

model = keras.models.load_model(weights, compile=False)
pred = model.predict(batch, verbose=0)
pct = pred.sum(axis=0) / pred.shape[0] * 100
classes = ["AD", "CN", "MCI"]
result = {c: float(p) for c, p in zip(classes, pct)}
print(os.path.basename(src), {k: round(v, 2) for k, v in result.items()})

# Save outputs
sdir = os.path.join(out_dir, "slices")
os.makedirs(sdir, exist_ok=True)
for k, z in enumerate(zlist):
    Image.fromarray((batch[k, :, :, 0] * 255).astype(np.uint8)).save(os.path.join(sdir, "z%03d.png" % z))
np.savez_compressed(
    os.path.join(out_dir, "volumes.npz"),
    head=reg_np.astype(np.float32), mask=mask_np.astype(np.uint8), hippo=hippo)
json.dump({
    "source": os.path.basename(src),
    "percent": result,
    "slices": [{"z": z, "AD": float(p[0]), "CN": float(p[1]), "MCI": float(p[2])} for z, p in zip(zlist, pred)],
    "affine": ho_img.affine.tolist(),
    "metric": {"rigid": m1, "affine": m2},
}, open(os.path.join(out_dir, "result.json"), "w"), indent=1)
