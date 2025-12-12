# 🚀 APP2 - Minimal Deployment Package

## 📁 Required Files for GitHub

Your `app2` folder needs these **6 files only**:

```
app2/
├── app.py                      ✅ Main application
├── requirements.txt            ✅ Dependencies
├── data_numeric.npz           ❌ NEED TO COPY
├── data_categorical.npz       ❌ NEED TO COPY
├── data_metadata.json         ❌ NEED TO COPY  
├── category_mappings.json     ❌ NEED TO COPY
├── README.md                  ✅ Documentation
└── .gitignore                 ✅ Git configuration
```

## 📝 COPY FILES NOW

Run these commands to copy the data files to app2:

```bash
cd /Users/xiang/my_venv3.13.3/code/Streamlit/Test2_backup

# Copy NPZ files
cp app/data_numeric.npz app2/
cp app/data_categorical.npz app2/

# Copy JSON files  
cp app/data_metadata.json app2/
cp app/category_mappings.json app2/

# Verify files
ls -lh app2/
```

Expected output:
```
-rw-r--r--  app.py                    (25 KB)
-rw-r--r--  requirements.txt          (100 B)
-rw-r--r--  data_numeric.npz          (13 MB)
-rw-r--r--  data_categorical.npz      (1.6 MB)
-rw-r--r--  data_metadata.json        (4.3 KB)
-rw-r--r--  category_mappings.json    (582 B)
-rw-r--r--  README.md                 (3 KB)
-rw-r--r--  .gitignore                (200 B)
```

## 🚀 Deploy to GitHub

After copying files:

```bash
cd app2

# Initialize git
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: French Motor Insurance Dashboard"

# Create GitHub repo at: https://github.com/new
# Repository name: french-motor-insurance-dashboard

# Push to GitHub (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/french-motor-insurance-dashboard.git
git branch -M main
git push -u origin main
```

## ☁️ Deploy to Streamlit Cloud

1. Go to: https://share.streamlit.io
2. Click "New app"
3. Repository: YOUR_USERNAME/french-motor-insurance-dashboard
4. Branch: main
5. Main file: app.py
6. Click "Deploy!"

## ✅ Verification Checklist

- [ ] All 6 files copied to app2 folder
- [ ] Files verified with `ls -lh app2/`
- [ ] Git initialized in app2
- [ ] Files committed to git
- [ ] GitHub repository created
- [ ] Code pushed to GitHub
- [ ] App deployed on Streamlit Cloud
- [ ] Dashboard loads successfully

## 📊 File Sizes

- app.py: ~25 KB
- requirements.txt: ~100 B
- data_numeric.npz: ~13 MB ✅
- data_categorical.npz: ~1.6 MB ✅
- data_metadata.json: ~4.3 KB
- category_mappings.json: ~582 B
- **Total: ~14.3 MB** (fits GitHub perfectly!)

## 🎯 What's Different in app2?

**MINIMIZED** - Only essential files:
- ❌ No CSV files (use NPZ instead)
- ❌ No conversion scripts  
- ❌ No test scripts
- ❌ No deployment guides (except this one)
- ❌ No backup files
- ✅ Only production-ready files

**CLEAN** - Ready for deployment:
- ✅ Clean directory structure
- ✅ Minimal .gitignore
- ✅ Professional README
- ✅ GitHub optimized (< 15 MB)

## 🔧 Troubleshooting

### Files not copying?
Try this alternative method:
```bash
cd /Users/xiang/my_venv3.13.3/code/Streamlit/Test2_backup

# Use rsync instead
rsync -av app/data_*.* app2/
rsync -av app/category_mappings.json app2/
```

### Still not working?
Manual copy in Finder:
1. Open Finder
2. Navigate to: `/Users/xiang/my_venv3.13.3/code/Streamlit/Test2_backup/app`
3. Select these 4 files:
   - data_numeric.npz
   - data_categorical.npz
   - data_metadata.json
   - category_mappings.json
4. Copy (Cmd+C)
5. Navigate to: app2 folder
6. Paste (Cmd+V)

---

**Once files are copied, you're ready to deploy!** 🎉
