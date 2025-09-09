#!/usr/bin/env python3
import argparse
import json
import random
import shutil
import sys
import tarfile
import zipfile
from pathlib import Path
from typing import List, Tuple, Optional

import numpy as np
from PIL import Image

try:
    from pycocotools import mask as maskUtils
except ImportError:
    maskUtils = None

try:
    import matplotlib.pyplot as plt
except ImportError:
    plt = None


# ----------------- utils -----------------
IMG_EXT = {".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff"}


def list_images(path: Path):
    return sorted([p for p in path.rglob("*") if p.suffix.lower() in IMG_EXT])


def ensure_pairs(images_dir: Path, masks_dir: Path) -> List[Tuple[Path, Path]]:
    pairs = []
    for img in list_images(images_dir):
        m1 = masks_dir / (img.stem + ".png")
        m2 = masks_dir / img.name
        if m1.exists():
            pairs.append((img, m1))
        elif m2.exists():
            pairs.append((img, m2))
        else:
            raise FileNotFoundError(f"Mask missing for {img.name}")
    return pairs


def split_items(items: list, ratios=(0.7, 0.2, 0.1), seed=1337):
    random.Random(seed).shuffle(items)
    n = len(items)
    n_train = int(n * ratios[0])
    n_val = int(n * ratios[1])
    train = items[:n_train]
    val = items[n_train:n_train + n_val]
    test = items[n_train + n_val:]
    return train, val, test


def copy_split(pairs: List[Tuple[Path, Optional[Path]]], root: Path, split_name: str):
    img_out = root / split_name / "images"
    msk_out = root / split_name / "masks"
    img_out.mkdir(parents=True, exist_ok=True)
    msk_out.mkdir(parents=True, exist_ok=True)
    for img, m in pairs:
        shutil.copy2(img, img_out / img.name)
        if m:
            shutil.copy2(m, msk_out / (img.stem + ".png"))


# ----------------- coco export -----------------
def coco_encode_mask(binary_mask: np.ndarray, h: int, w: int):
    if maskUtils is None:
        raise RuntimeError("pycocotools not installed")
    rle = maskUtils.encode(np.asfortranarray(binary_mask.astype(np.uint8)))
    rle["counts"] = rle["counts"].decode("ascii")
    area = float(maskUtils.area(rle))
    bbox = [float(x) for x in maskUtils.toBbox(rle)]
    return rle, area, bbox


def export_coco(pairs, categories, out_json: Path):
    cat_map = {i + 1: n for i, n in enumerate(categories)}
    images, annotations, cats = [], [], []
    for i, n in cat_map.items():
        cats.append({"id": i, "name": n})

    img_id, ann_id = 1, 1
    for img, mask in pairs:
        with Image.open(img) as im:
            w, h = im.size
        images.append({"id": img_id, "file_name": img.name, "width": w, "height": h})

        mask_arr = np.array(Image.open(mask))
        if len(categories) == 1:
            bin_mask = (mask_arr > 0).astype(np.uint8)
            if bin_mask.sum() > 0:
                rle, area, bbox = coco_encode_mask(bin_mask, h, w)
                annotations.append({
                    "id": ann_id, "image_id": img_id, "category_id": 1,
                    "segmentation": rle, "area": area, "bbox": bbox, "iscrowd": 0
                })
                ann_id += 1
        else:
            for cid in range(1, len(categories) + 1):
                bin_mask = (mask_arr == cid).astype(np.uint8)
                if bin_mask.sum() == 0:
                    continue
                rle, area, bbox = coco_encode_mask(bin_mask, h, w)
                annotations.append({
                    "id": ann_id, "image_id": img_id, "category_id": cid,
                    "segmentation": rle, "area": area, "bbox": bbox, "iscrowd": 0
                })
                ann_id += 1
        img_id += 1

    out_json.parent.mkdir(parents=True, exist_ok=True)
    with out_json.open("w") as f:
        json.dump({"images": images, "annotations": annotations, "categories": cats}, f)
    print(f"[OK] saved COCO -> {out_json}")


# ----------------- visualize -----------------
def visualize(split_root: Path, split: str, n: int = 12):
    if plt is None:
        print("[warn] matplotlib not installed")
        return
    imgs = list_images(split_root / split / "images")
    if not imgs:
        return
    n = min(n, len(imgs))
    cols, rows = 4, int(np.ceil(n / 4))
    plt.figure(figsize=(cols * 3, rows * 3))
    for i, p in enumerate(imgs[:n]):
        plt.subplot(rows, cols, i + 1)
        im = Image.open(p)  
        plt.imshow(im)
        m = split_root / split / "masks" / (p.stem + ".png")
        if m.exists():
            mask = Image.open(m)
            plt.imshow(mask, alpha=0.35)
        plt.axis("off")
    out_png = split_root / f"preview_{split}.png"
    plt.tight_layout()
    plt.savefig(out_png, dpi=150)
    print(f"[OK] preview saved -> {out_png}")


# ----------------- main -----------------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dataset-root", type=Path, required=True)
    ap.add_argument("--images-subdir", default="images")
    ap.add_argument("--masks-subdir", default=None)
    ap.add_argument("--prepare", action="store_true")
    ap.add_argument("--split", nargs=3, type=float, default=[0.7, 0.2, 0.1])
    ap.add_argument("--to-coco", action="store_true")
    ap.add_argument("--category-names", nargs="+", default=["tooth"])
    ap.add_argument("--viz", type=int, default=0)
    args = ap.parse_args()

    images_dir = args.dataset_root / args.images_subdir
    masks_dir = args.dataset_root / args.masks_subdir if args.masks_subdir else None

    if masks_dir:
        pairs = ensure_pairs(images_dir, masks_dir)
    else:
        pairs = [(p, None) for p in list_images(images_dir)]

    train, val, test = split_items(pairs, tuple(args.split))
    split_root = args.dataset_root / "splits"
    for name, items in [("train", train), ("val", val), ("test", test)]:
        copy_split(items, split_root, name)
        if args.to_coco and masks_dir:
            export_coco(items, args.category_names, split_root / name / "annotations" / "instances.json")
        if args.viz > 0:
            visualize(split_root, name, n=args.viz)


if __name__ == "__main__":
    main()
