# E-Commerce Messy to Clean ETL

Real-world ETL cleaning project

**Pipeline:** Raw Data Lake -> cleaner.py -> Clean Lake -> SQLite

**Raw Issues Found:**
- Column names with spaces: ' Customer_Name'
- Price: 'abd', 'four hundred', 10000 outlier
- Quantity: -2, 0
- Duplicates, nulls
- Total = -20000 (wrong calculation)

**Cleaning Steps:**
1. Stripped column names
2. Dropped duplicates
3. to_numeric with coerce for Price & Quantity
4. Filtered Quantity > 0
5. Removed Price > 5000 outliers
6. Recalculated Total = Quantity * Price
7. Standardized Category

**Result:** 103 -> 86 rows (16.5% bad data removed)

**Tech:** Python, Pandas
