import pandas as pd
import os
import glob

# Find raw file
raw_files = glob.glob('Raw/*.csv')
print(f"Found RAW: {raw_files[0]}")
df = pd.read_csv(raw_files[0])
print(f"RAW shape: {df.shape}")
print(f"Columns: {df.columns.tolist()}")

#cleaning

# 1. Fix column names - remove spaces
df.columns = df.columns.str.strip()

# 2. Remove duplicates
df = df.drop_duplicates()

# 3. Strip whitespace from all string columns
for col in df.select_dtypes(include=['object']).columns:
    df[col] = df[col].astype(str).str.strip()

# 4. Clean Category - standardize
if 'Category' in df.columns:
    df['Category'] = df['Category'].str.lower().str.title()
    df['Category'] = df['Category'].replace({
        'Electronic': 'Electronics',
        'Nan': None,
        'None': None
    })

# 5. Clean Price - text like 'abd', 'four hundred' -> NaN
df['Price'] = pd.to_numeric(df['Price'], errors='coerce')

# 6. Clean Quantity - -2, 0, text -> NaN then filter
df['Quantity'] = pd.to_numeric(df['Quantity'], errors='coerce')
df = df[df['Quantity'] > 0] # Remove -ve and 0

# 7. Remove rows where Price is NaN (abd, four hundred)
df = df.dropna(subset=['Price', 'Quantity'])

# 8. Recalculate Total correctly
df['Total'] = (df['Quantity'] * df['Price']).round(2)

# 9. Clean Date
df['Order_Date'] = pd.to_datetime(df['Order_Date'], errors='coerce')

# 10. Optional: Remove Price > 5000 (outlier like 10000)
df = df[df['Price'] < 5000]

print(f"CLEAN shape: {df.shape}")

# Save
os.makedirs('Clean', exist_ok=True)
clean_path = f"Clean/clean_{os.path.basename(raw_files[0])}"
df.to_csv(clean_path, index=False)
print(f"Saved to: {clean_path} -> DB Created!")

import sqlite3

# --- L - LOAD ---
conn = sqlite3.connect('ecommerce.db')
df.to_sql('sales', conn, if_exists='replace', index=False)
conn.close()

print("✅ LOAD done! Data loaded to ecommerce.db -> table 'sales'")