import pandas as pd
from pathlib import Path

base = Path(".")
print(f"Running from: {base.resolve()}")

for lake in base.glob("*_data_lake"):
    print(f"\n--- {lake.name} ---")
    
    raw_folder = lake / "Raw" if (lake / "Raw").exists() else lake / "raw"
    if not raw_folder.exists():
        print(f"  No Raw folder found, skipping")
        continue

    files = list(raw_folder.glob("*.xlsx")) + list(raw_folder.glob("*.csv"))
    if not files:
        print(f"  No files in {raw_folder}")
        continue

    for raw_file in files:
        print(f"  Found: {raw_file.name}")
        df = pd.read_excel(raw_file) if raw_file.suffix == '.xlsx' else pd.read_csv(raw_file)
        print(f"  RAW shape: {df.shape}")
        df = df.drop_duplicates()
        df.columns = [str(c).strip().replace(' ', '_') for c in df.columns]
        clean_folder = lake / "Clean"
        clean_folder.mkdir(exist_ok=True)
        out = clean_folder / f"clean_{raw_file.stem}.csv"
        df.to_csv(out, index=False)
        print(f"  CLEAN shape: {df.shape}")
        print(f"  Saved to: {out}")

print("\n>>> ALL 5 DATA LAKES CLEANED IN ONE RUN! <<<")