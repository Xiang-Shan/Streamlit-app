# Convert CSV to NPY Format - Solution for GitHub Size Limit

## Why NPY Format?

### Advantages:
- **Smaller Size**: 50-70% reduction (192MB → ~60-90MB)
- **Faster Loading**: Binary format loads 5-10x faster
- **Fits GitHub**: Under 100MB limit
- **Better Compression**: Especially for numeric data
- **No Kaggle Needed**: Self-contained in repository

### Disadvantages:
- Requires column names to be stored separately
- Less human-readable (binary format)

## Step 1: Convert Your CSV to NPY

Run this script on your Mac:

```python
# convert_to_npy.py
import pandas as pd
import numpy as np
import json

print("Loading CSV...")
df = pd.read_csv('GLM_example_with_GLMs_Predictions.csv')

print(f"Original CSV size: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
print(f"Shape: {df.shape}")
print(f"Columns: {list(df.columns)}")

# Save column names and dtypes
metadata = {
    'columns': list(df.columns),
    'dtypes': {col: str(dtype) for col, dtype in df.dtypes.items()}
}

with open('data_metadata.json', 'w') as f:
    json.dump(metadata, f, indent=2)

# Convert to numpy arrays
print("\nConverting to numpy arrays...")

# Separate numeric and non-numeric columns
numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
object_cols = df.select_dtypes(include=['object']).columns.tolist()

# Save numeric data as NPY
if numeric_cols:
    numeric_data = df[numeric_cols].values
    np.save('data_numeric.npy', numeric_data)
    print(f"Saved numeric data: {len(numeric_cols)} columns")

# Save categorical data as NPY (encoded)
if object_cols:
    # Create a dictionary to store category mappings
    category_mappings = {}
    categorical_data = np.zeros((len(df), len(object_cols)), dtype=np.int32)
    
    for i, col in enumerate(object_cols):
        categories = df[col].astype('category')
        category_mappings[col] = list(categories.cat.categories)
        categorical_data[:, i] = categories.cat.codes
    
    np.save('data_categorical.npy', categorical_data)
    
    with open('category_mappings.json', 'w') as f:
        json.dump(category_mappings, f, indent=2)
    
    print(f"Saved categorical data: {len(object_cols)} columns")

# Save column order
with open('column_order.json', 'w') as f:
    json.dump({
        'numeric': numeric_cols,
        'categorical': object_cols
    }, f, indent=2)

print("\n✅ Conversion complete!")
print("\nFiles created:")
print("  - data_numeric.npy (numeric columns)")
print("  - data_categorical.npy (categorical columns)")
print("  - data_metadata.json (column info)")
print("  - category_mappings.json (category encodings)")
print("  - column_order.json (column order)")
```

Save and run:
```bash
cd /Users/xiang/my_venv3.13.3/code/Streamlit/Test2_backup/app
python convert_to_npy.py
```

## Step 2: Check File Sizes

```bash
ls -lh *.npy *.json
```

Expected results:
- data_numeric.npy: ~50-80MB
- data_categorical.npy: ~10-20MB
- Total: ~60-100MB (fits GitHub!)

## Step 3: Update app.py to Load NPY Files

The load_data() function will be updated to load from NPY instead of CSV.

## Step 4: Add to Git

```bash
git add data_numeric.npy data_categorical.npy *.json
git commit -m "Add compressed dataset in NPY format"
git push
```

## Comparison

| Format | Size | Load Time | GitHub |
|--------|------|-----------|--------|
| CSV | 192 MB | ~3-5 sec | ❌ Too large |
| NPY | ~70 MB | ~0.5 sec | ✅ Fits! |
| Gzip CSV | ~40 MB | ~8-10 sec | ✅ Fits but slow |

NPY is the best balance of size and speed!
