# 🚗 French Motor Insurance GLM Dashboard

Interactive Streamlit dashboard for analyzing French Motor Insurance data with GLM pure premium predictions.

## 📊 Features

- **Overview**: Dataset statistics and key metrics
- **GLM Predictions**: Model performance analysis
- **Claims Analysis**: Frequency and severity breakdown
- **Vehicle Features**: Brand, power, age, fuel type analysis
- **Driver Demographics**: Age groups and behavior patterns
- **Data Explorer**: Interactive filtering and search
- **Pivot Tables**: Custom aggregations and metrics

## 🚀 Live Demo

**Deployed on Streamlit Cloud**: [Your App URL Here]

## 📦 Dataset

- **Size**: 678,013 insurance policies
- **Features**: 63 columns (numeric & categorical)
- **Format**: Compressed NPZ (14.3 MB) - 92.5% smaller than CSV
- **Source**: French Motor Insurance dataset

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **Data Processing**: Pandas, NumPy
- **Visualization**: Plotly
- **Deployment**: GitHub + Streamlit Cloud

## 📁 Repository Structure

```
app2/
├── app.py                      # Main Streamlit application
├── requirements.txt            # Python dependencies
├── data_numeric.npz           # Numeric data (12.75 MB)
├── data_categorical.npz       # Categorical data (1.57 MB)
├── data_metadata.json         # Column metadata
├── category_mappings.json     # Category encodings
├── README.md                  # This file
└── .gitignore                 # Git exclusions
```

## 🚀 Quick Start

### Run Locally

```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/french-motor-insurance-dashboard.git
cd french-motor-insurance-dashboard

# Install dependencies
pip install -r requirements.txt

# Run app
streamlit run app.py
```

### Deploy to Streamlit Cloud

1. Fork this repository
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Click "New app"
4. Select your repository
5. Set main file: `app.py`
6. Deploy! 🎉

## 📊 Data Format

This app uses **compressed NPZ format** for optimal performance:

- **92.5% smaller** than original CSV (192 MB → 14.3 MB)
- **10x faster** loading time
- **GitHub compatible** (< 100 MB limit)
- **No external dependencies** required

## 🎯 Key Metrics

The dashboard analyzes:
- Claim frequency and severity
- Premium predictions vs actual
- Regional and demographic patterns
- Vehicle characteristics impact
- GLM model performance

## 📝 License

This project is for educational and analytical purposes.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Contact

For questions or feedback, please open an issue on GitHub.

---

**Built with ❤️ using Streamlit**
