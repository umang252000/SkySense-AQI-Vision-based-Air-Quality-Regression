import os
import time
import piexif
import requests
import pandas as pd
from PIL import Image
from tqdm import tqdm

IMAGE_DIR = "images"
CITY_CSV = "city_gps.csv"
OUTPUT_CSV = "labels.csv"

OWM_API_KEY = "OpenWeatherMap Token"  

DEFAULT_LAT = 23.0225
DEFAULT_LON = 72.5714

RATE_LIMIT_SECONDS = 1.1   

if not os.path.exists(CITY_CSV):
    raise FileNotFoundError(f"{CITY_CSV} not found. Create the file in SkySense folder.")

city_df = pd.read_csv(CITY_CSV)

def get_gps_from_city(filename):
    """
    
    """
    name = filename.lower()
    for _, row in city_df.iterrows():
        key = str(row['keyword']).lower().strip()
        if key in name:
            return (row['lat'], row['lon'])
    return None



def get_gps_from_exif(path):
    try:
        exif_dict = piexif.load(path)
        gps_ifd = exif_dict.get("GPS")
        if not gps_ifd:
            return None

        def convert(coord, ref):
            d = coord[0][0] / coord[0][1]
            m = coord[1][0] / coord[1][1]
            s = coord[2][0] / coord[2][1]
            val = d + (m / 60) + (s / 3600)
            if ref in [b"S", b"W", "S", "W"]:
                val = -val
            return val

        lat = convert(gps_ifd[2], gps_ifd.get(1))
        lon = convert(gps_ifd[4], gps_ifd.get(3))
        return (lat, lon)

    except:
        return None


def parse_latlon_from_filename(fname):
    try:
        parts = fname.rsplit(".", 1)[0].split("_")
        if len(parts) >= 4:
            lat = float(parts[-2])
            lon = float(parts[-1])
            return (lat, lon)
        return None
    except:
        return None


def query_pm25(lat, lon):
    url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={OWM_API_KEY}"
    try:
        r = requests.get(url, timeout=10)
        if r.status_code != 200:
            return None
        data = r.json()
        pm25 = data['list'][0]['components']['pm2_5']
        pm10 = data['list'][0]['components']['pm10']
        return pm25, pm10
    except:
        return None


def main():
    files = sorted([f for f in os.listdir(IMAGE_DIR)
                    if f.lower().endswith(('.jpg', '.jpeg', '.png'))])

    print("Found", len(files), "images")

    rows = []

    for fn in tqdm(files):
        path = os.path.join(IMAGE_DIR, fn)

        
        gps = get_gps_from_exif(path)

        if not gps:
            gps = parse_latlon_from_filename(fn)

        if not gps:
            gps = get_gps_from_city(fn)

        if not gps:
            gps = (DEFAULT_LAT, DEFAULT_LON)

        lat, lon = gps

        
        res = query_pm25(lat, lon)

        if not res:
            print("⚠️ API error for:", fn)
            continue

        pm25, pm10 = res

        
        try:
            img = Image.open(path)
            info = img._getexif()
            timestamp = info.get(36867) if info else None
        except:
            timestamp = None

        rows.append({
            "filename": fn,
            "lat": lat,
            "lon": lon,
            "pm2_5": pm25,
            "pm10": pm10,
            "timestamp_exif": timestamp
        })

        time.sleep(RATE_LIMIT_SECONDS)

    
    df = pd.DataFrame(rows)
    df.to_csv(OUTPUT_CSV, index=False)
    print("\n✔ DONE — Saved labels to:", OUTPUT_CSV)
    print(df.head())


if __name__ == "__main__":
    main()
