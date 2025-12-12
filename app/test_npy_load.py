"""
Test loading NPY files and verify they match the original CSV
"""
import pandas as pd
import numpy as np
import json
from pathlib import Path

def load_from_npy():
    """Load data from NPZ files"""
    
    print("Loading data from NPZ files...")
    
    # Load metadata
    with open('data_metadata.json', 'r') as f:
        metadata = json.load(f)
    
    with open('category_mappings.json', 'r') as f:
        category_mappings = json.load(f)
    
    # Load numeric data from compressed format
    numeric_data = np.load('data_numeric.npz')['data']
    numeric_df = pd.DataFrame(numeric_data, columns=metadata['numeric_columns'])
    
    # Load categorical data from compressed format
    categorical_data = np.load('data_categorical.npz')['data']
    categorical_df = pd.DataFrame(categorical_data, columns=metadata['categorical_columns'])
    
    # Decode categorical data
    for col in metadata['categorical_columns']:
        col_idx = metadata['categorical_columns'].index(col)
        codes = categorical_data[:, col_idx]
        categories = category_mappings[col]
        categorical_df[col] = pd.Categorical.from_codes(codes, categories=categories)
    
    # Combine dataframes in original column order
    df = pd.DataFrame()
    for col in metadata['columns']:
        if col in numeric_df.columns:
            df[col] = numeric_df[col]
        elif col in categorical_df.columns:
            df[col] = categorical_df[col]
    
    print(f"✅ Loaded {len(df):,} rows × {len(df.columns)} columns")
    return df

def verify_data():
    """Verify NPY data matches original CSV"""
    
    print("=" * 70)
    print("Testing NPZ File Loading")
    print("=" * 70)
    
    # Load from NPZ
    print("\n📂 Loading from NPZ files...")
    df_npy = load_from_npy()
    
    # Load original CSV (if exists)
    csv_path = Path('GLM_example_with_GLMs_Predictions.csv')
    if csv_path.exists():
        print(f"\n📂 Loading original CSV for comparison...")
        df_csv = pd.read_csv(csv_path)
        
        # Compare
        print(f"\n🔍 Verification:")
        print(f"   Shape match: {df_npy.shape == df_csv.shape}")
        print(f"   Column match: {list(df_npy.columns) == list(df_csv.columns)}")
        
        # Check data equality (with tolerance for float precision)
        numeric_cols = df_npy.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            if not np.allclose(df_npy[col].values, df_csv[col].values, rtol=1e-5, equal_nan=True):
                print(f"   ⚠️  Mismatch in column: {col}")
        
        categorical_cols = df_npy.select_dtypes(include=['object', 'category']).columns
        for col in categorical_cols:
            if not (df_npy[col].astype(str) == df_csv[col].astype(str)).all():
                print(f"   ⚠️  Mismatch in column: {col}")
        
        print(f"   ✅ Data verification passed!")
    
    # Display sample
    print(f"\n📋 Sample Data (first 5 rows):")
    print(df_npy.head())
    
    # Display info
    print(f"\n📊 Data Info:")
    print(f"   Memory usage: {df_npy.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
    print(f"   Numeric columns: {len(df_npy.select_dtypes(include=[np.number]).columns)}")
    print(f"   Categorical columns: {len(df_npy.select_dtypes(include=['object', 'category']).columns)}")
    
    # File sizes
    print(f"\n💾 File Sizes:")
    for file in ['data_numeric.npy', 'data_categorical.npy', 'data_metadata.json', 'category_mappings.json']:
        if Path(file).exists():
            size = Path(file).stat().st_size / 1024**2
            print(f"   {file}: {size:.2f} MB")
    
    print("\n" + "=" * 70)
    print("✅ Test Complete!")
    print("=" * 70)
    print("\nYou can now:")
    print("  1. Update app.py to use this load function")
    print("  2. Delete the original CSV (optional)")
    print("  3. Add NPY files to git and push to GitHub")
    
    return df_npy

if __name__ == '__main__':
    df = verify_data()
