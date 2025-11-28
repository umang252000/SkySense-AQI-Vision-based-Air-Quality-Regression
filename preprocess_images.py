import os
import shutil
from PIL import Image
import pandas as pd
import numpy as np
from datetime import datetime

IMAGE_DIR = "images"
LABELS_CSV = "labels.csv"
OUTPUT_DIR = "labelled"
SIZE = (128, 128)   
VAL_PERCENT = 0.15  


df = pd.read_csv(LABELS_CSV)

def parse_timestamp(ts):
    if pd.isna(ts):
        return None
    try:
        return datetime.strptime(ts, "%Y:%m:%d %H:%M:%S")
    except:
        return None

print("Parsing timestamps...")
df["parsed_time"] = df["timestamp_exif"].apply(parse_timestamp)

min_time = datetime(2000, 1, 1)
df["parsed_time"] = df["parsed_time"].apply(lambda x: x if x is not None else min_time)

df_sorted = df.sort_values(by="parsed_time")

total = len(df_sorted)
val_count = int(total * VAL_PERCENT)

val_df = df_sorted.tail(val_count)
train_df = df_sorted.head(total - val_count)

print(f"Total images: {total}")
print(f"Train images: {len(train_df)}")
print(f"Val images:   {len(val_df)}")

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(os.path.join(OUTPUT_DIR, "train"), exist_ok=True)
os.makedirs(os.path.join(OUTPUT_DIR, "val"), exist_ok=True)

def save_resized_images(subset_df, folder_name):
    for _, row in subset_df.iterrows():
        fn = row["filename"]
        src = os.path.join(IMAGE_DIR, fn)
        if not os.path.exists(src):
            print("Missing:", src)
            continue

        try:
            img = Image.open(src).convert("RGB")
            img = img.resize(SIZE, Image.LANCZOS)
            dst_path = os.path.join(OUTPUT_DIR, folder_name, fn)
            img.save(dst_path, quality=90)
        except Exception as e:
            print("Error processing", fn, e)

print("Saving TRAIN images...")
save_resized_images(train_df, "train")

print("Saving VAL images...")
save_resized_images(val_df, "val")

train_df["set"] = "train"
val_df["set"] = "val"

final_df = pd.concat([train_df, val_df])
final_df.to_csv(os.path.join(OUTPUT_DIR, "labels_split.csv"), index=False)

print("=================================================")
print("✔ Time-based split completed!")
print("✔ Resized images saved to labelled/")
print("✔ labels_split.csv created")
print("=================================================")