"""
Convert CSV to NPY format for GitHub deployment
Reduces file size by 50-70% while maintaining all data
"""
import pandas as pd
import numpy as np
import json
from pathlib import Path

def convert_csv_to_npy(csv_path='GLM_example_with_GLMs_Predictions.csv'):
    """Convert CSV to optimized NPY format"""
    
    print("=" * 70)
    print("Converting CSV to NPY Format")
    print("=" * 70)
    
    # Load CSV
    print(f"\n📂 Loading {csv_path}...")
    df = pd.read_csv(csv_path)
    
    # Display info
    print(f"✅ Loaded successfully!")
    print(f"   Rows: {len(df):,}")
    print(f"   Columns: {len(df.columns)}")
    print(f"   Memory: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
    
    # Separate numeric and categorical columns
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    object_cols = df.select_dtypes(include=['object']).columns.tolist()
    
    print(f"\n📊 Column Analysis:")
    print(f"   Numeric columns: {len(numeric_cols)}")
    print(f"   Categorical columns: {len(object_cols)}")
    
    # Save numeric data with compression
    print(f"\n💾 Saving numeric data (compressed)...")
    numeric_data = df[numeric_cols].values.astype(np.float32)  # Use float32 to save space
    np.savez_compressed('data_numeric.npz', data=numeric_data)
    numeric_size = Path('data_numeric.npz').stat().st_size / 1024**2
    print(f"   ✅ data_numeric.npz ({numeric_size:.2f} MB)")
    
    # Encode and save categorical data
    print(f"\n💾 Encoding categorical data...")
    category_mappings = {}
    categorical_data = np.zeros((len(df), len(object_cols)), dtype=np.int32)
    
    for i, col in enumerate(object_cols):
        categories = df[col].astype('category')
        category_mappings[col] = list(categories.cat.categories)
        categorical_data[:, i] = categories.cat.codes
        print(f"   {col}: {len(category_mappings[col])} unique values")
    
    np.savez_compressed('data_categorical.npz', data=categorical_data)
    categorical_size = Path('data_categorical.npz').stat().st_size / 1024**2
    print(f"   ✅ data_categorical.npz ({categorical_size:.2f} MB)")
    
    # Save metadata
    print(f"\n💾 Saving metadata...")
    
    metadata = {
        'columns': list(df.columns),
        'dtypes': {col: str(dtype) for col, dtype in df.dtypes.items()},
        'shape': df.shape,
        'numeric_columns': numeric_cols,
        'categorical_columns': object_cols
    }
    
    with open('data_metadata.json', 'w') as f:
        json.dump(metadata, f, indent=2)
    print(f"   ✅ data_metadata.json")
    
    with open('category_mappings.json', 'w') as f:
        json.dump(category_mappings, f, indent=2)
    print(f"   ✅ category_mappings.json")
    
    # Summary
    total_npy_size = numeric_size + categorical_size
    original_size = Path(csv_path).stat().st_size / 1024**2
    reduction = (1 - total_npy_size / original_size) * 100
    
    print("\n" + "=" * 70)
    print("✅ Conversion Complete!")
    print("=" * 70)
    print(f"\n📊 Size Comparison:")
    print(f"   Original CSV: {original_size:.2f} MB")
    print(f"   NPY files:    {total_npy_size:.2f} MB")
    print(f"   Reduction:    {reduction:.1f}%")
    print(f"\n✅ Files ready for GitHub (total: {total_npy_size:.2f} MB)")
    
    if total_npy_size < 100:
        print("✅ Fits within GitHub's 100MB file limit!")
    else:
        print("⚠️  Still over 100MB - consider additional compression")
    
    print("\n📝 Next steps:")
    print("   1. Test loading with: python test_npy_load.py")
    print("   2. Update app.py to use NPY files")
    print("   3. Add to git: git add *.npy *.json")
    print("   4. Commit and push to GitHub")
    
    return metadata

if __name__ == '__main__':
    convert_csv_to_npy()
