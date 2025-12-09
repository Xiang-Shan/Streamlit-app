# French Motor Insurance GLM Analysis Dashboard 🚗📊

A comprehensive Streamlit dashboard for analyzing French motor insurance claims data with GLM (Generalized Linear Model) predictions.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://your-app-url.streamlit.app)

## 🎯 Features

- **7 Interactive Analysis Tabs**:
  - 📊 Overview - Dataset summary and key metrics
  - 🎯 GLM Predictions - Model performance analysis
  - 📈 Claims Analysis - Detailed claim patterns
  - 🚗 Vehicle Features - Vehicle characteristics impact
  - 👥 Driver Demographics - Driver profile analysis
  - 📋 Data Explorer - Interactive data browsing
  - 🔄 Pivot Table - Custom aggregations and metrics

- **30+ Interactive Visualizations** using Plotly
- **Advanced Filtering** by Region, Area, and Density
- **Automatic Data Download** from Kaggle using kagglehub
- **Pivot Table Builder** with 7 calculated metrics
- **Responsive Design** optimized for all screen sizes

## 📊 Dataset

**Source**: [French Motor Insurance Dataset on Kaggle](https://www.kaggle.com/datasets/xiangshan1989/french-motor-insurance)

**Size**: 678,014 insurance policies with GLM predictions

**Features**:
- Policy details (ID, Exposure, Claims)
- Geographic data (Region, Area, Density)
- Vehicle characteristics (Brand, Power, Age, Gas type)
- Driver demographics (Age, Bonus-Malus score)
- GLM predictions (Frequency, Severity)
- Claim amounts

## 🚀 Quick Start

### Option 1: Deploy to Streamlit Cloud (Recommended)

1. **Fork or clone this repository**

2. **Push to your GitHub account**

3. **Deploy on Streamlit Cloud**:
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Click "New app"
   - Select your repository
   - Set main file path: `app.py`
   - Click "Deploy"

**That's it!** The app will automatically download the dataset from Kaggle on first run. No API keys or secrets required!

### Option 2: Run Locally

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/french-insurance-dashboard.git
   cd french-insurance-dashboard
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the app**:
   ```bash
   streamlit run app.py
   ```

4. **Open in browser**: The app will open automatically at `http://localhost:8501`

## 📦 Dependencies

```
streamlit>=1.28.0      # Web application framework
pandas>=2.0.0          # Data manipulation
numpy>=1.24.0          # Numerical operations
plotly>=5.17.0         # Interactive visualizations
kagglehub>=0.2.0       # Kaggle dataset downloads
```

## 🎨 Dashboard Tabs

### 📊 Overview
- Total policies, claims, and key metrics
- Regional and area distribution charts
- Density analysis with claim frequency

### 🎯 GLM Predictions
- Model performance comparison
- Predicted vs Actual frequency analysis
- Severity predictions evaluation

### 📈 Claims Analysis
- Claim frequency and severity statistics
- Claims by vehicle brand and age
- Claim amount distribution

### 🚗 Vehicle Features
- Vehicle power and fuel type distribution
- Brand-level analysis with claim rates
- Vehicle age impact on claims

### 👥 Driver Demographics
- Driver age distribution
- Bonus-Malus score analysis
- Age group impact on claim frequency

### 📋 Data Explorer
- Interactive data browsing
- Column selection and filtering
- Statistical summaries
- CSV export functionality

### 🔄 Pivot Table
- Custom row/column dimensions
- 7 calculated metrics:
  - Number of Policies
  - Total Claims
  - Total Exposure
  - Total Claim Amount
  - Avg Claim Frequency %
  - Avg Claim Severity
  - Loss Ratio %
- Heatmap visualizations

## 🔧 Customization

### Modify Dataset Source
Update the dataset in the `load_data()` function in `app.py`:
```python
path = kagglehub.dataset_download("yourusername/your-dataset")
```

### Add New Filters
Edit the sidebar filters section:
```python
selected_brand = st.sidebar.selectbox("Vehicle Brand", brands)
```

### Create Custom Visualizations
Add new charts in any tab:
```python
fig = px.bar(data, x='column1', y='column2')
st.plotly_chart(fig, use_container_width=True)
```

## 📁 Project Structure

```
.
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── .gitignore            # Git ignore rules
└── DEPLOYMENT_GUIDE.md   # Detailed deployment instructions
```

## 🐛 Troubleshooting

### Dataset Download Issues
- **Problem**: First load takes 30-60 seconds
  - **Solution**: This is normal - kagglehub downloads and caches the dataset

- **Problem**: "Dataset not found" error
  - **Solution**: Verify the dataset URL is correct and public

- **Problem**: Connection timeout
  - **Solution**: Check internet connection and retry

### Performance Tips
- First run downloads ~192MB - subsequent runs use cache
- Local cache location: `~/.cache/kagglehub/`
- Streamlit Cloud provides automatic caching

### Memory Issues
- Streamlit Cloud offers 1GB RAM (sufficient for this dataset)
- Use filters to reduce memory usage if needed
- Clear cache if experiencing issues

## 💡 Usage Tips

1. **Apply Filters First**: Use sidebar filters to focus analysis on specific segments
2. **Explore All Tabs**: Each tab provides unique analytical perspectives
3. **Build Pivot Tables**: Combine dimensions to discover patterns
4. **Download Filtered Data**: Export data subsets for further analysis
5. **Hover for Details**: All charts show detailed info on hover

## 🤝 Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/NewFeature`)
3. Make your changes
4. Commit (`git commit -m 'Add NewFeature'`)
5. Push (`git push origin feature/NewFeature`)
6. Open a Pull Request

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- **Dataset**: [French Motor Insurance](https://www.kaggle.com/datasets/xiangshan1989/french-motor-insurance) by Xiang Shan
- **Framework**: [Streamlit](https://streamlit.io) for the web interface
- **Visualizations**: [Plotly](https://plotly.com) for interactive charts
- **Data Access**: [Kagglehub](https://github.com/Kaggle/kagglehub) for dataset downloads

## 📧 Contact

**Project Maintainer**: Xiang Shan

**Dataset on Kaggle**: [xiangshan1989/french-motor-insurance](https://www.kaggle.com/datasets/xiangshan1989/french-motor-insurance)

**Issues**: Please report issues on the GitHub repository

---

<div align="center">
  
  **Built with ❤️ using Streamlit**
  
  ⭐ Star this repo if you find it useful!
  
</div>
