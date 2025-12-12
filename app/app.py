"""
French Motor Insurance GLM Analysis Dashboard
A Streamlit app to visualize French Motor Insurance data with GLM pure premium predictions

Features:
- Interactive data exploration with 7 analysis tabs
- Excel-like pivot table functionality
- 30+ interactive visualizations
- Advanced filtering system
- Cross-platform compatible
"""

import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

# Set page configuration
st.set_page_config(
    page_title='French Motor Insurance GLM Dashboard',
    layout='wide',
    page_icon='🚗',
    initial_sidebar_state='expanded'
)

# Custom CSS for better styling
st.markdown('''
<style>
    div.block-container{padding-top:2rem;}
    .stDataFrame{background-color:#f8f9fa;}
    h1 {color: #1f77b4;}
    h2 {color: #2ca02c;}
    h3 {color: #ff7f0e;}
</style>
''', unsafe_allow_html=True)

# Data loading function
@st.cache_data
def load_data():
    """Load the French Motor Insurance dataset from NPZ files in GitHub repository"""
    
    import json

    data_dir_candidates = [
        Path(__file__).resolve().parent,
        Path.cwd(),
    ]

    try:
        with st.spinner("📂 Loading dataset from repository..."):
            st.sidebar.info('📦 Loading from NPZ files...')

            data_dir = next((candidate for candidate in data_dir_candidates if (candidate / 'data_metadata.json').exists()), None)
            if data_dir is None:
                raise FileNotFoundError('data_metadata.json')

            metadata_path = data_dir / 'data_metadata.json'
            mappings_path = data_dir / 'category_mappings.json'
            numeric_path = data_dir / 'data_numeric.npz'
            categorical_path = data_dir / 'data_categorical.npz'

            with open(metadata_path, 'r') as f:
                metadata = json.load(f)

            with open(mappings_path, 'r') as f:
                category_mappings = json.load(f)

            numeric_data = np.load(numeric_path)['data']
            numeric_df = pd.DataFrame(numeric_data, columns=metadata['numeric_columns'])

            categorical_data = np.load(categorical_path)['data']
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
            
            st.sidebar.success(f"✅ Loaded {len(df):,} policies from repository!")
            return df
            
    except FileNotFoundError as e:
        st.error(f"""
        ⚠️ **Dataset files not found!**
        
        Missing file: {e.filename}
        
        **Required files in repository:**
        - data_numeric.npz (12.75 MB)
        - data_categorical.npz (1.57 MB)
        - data_metadata.json
        - category_mappings.json
        
        **Setup Instructions:**
        1. Ensure all NPZ files are committed to your GitHub repository
        2. Verify files are in the root directory with app.py
        3. Redeploy on Streamlit Cloud
        """)
        st.stop()
        
    except Exception as e:
        st.error(f"⚠️ Error loading data: {e}")
        st.info("""
        **Troubleshooting:**
        1. Ensure data files are in the same directory as app.py
        2. Check that all 4 required files exist in the repository
        3. Verify file names match exactly (case-sensitive)
        4. Try redeploying on Streamlit Cloud
        """)
        st.stop()
# Calculate metrics
@st.cache_data
def calculate_metrics(df):
    """Calculate key metrics for the dashboard"""
    metrics = {
        'total_policies': len(df),
        'total_claims': df['ClaimNb'].sum(),
        'total_exposure': df['Exposure'].sum(),
        'total_claim_amount': df['ClaimAmount'].sum(),
        'avg_pure_premium': df['PurePremium'].mean(),
        'avg_predicted_premium': df['Pred_GLMs'].mean(),
        'claim_frequency': df['ClaimNb'].sum() / df['Exposure'].sum(),
        'avg_claim_severity': df[df['ClaimAmount'] > 0]['ClaimAmount'].mean() if (df['ClaimAmount'] > 0).any() else 0
    }
    return metrics

# Pivot table helper functions
def calculate_pivot_metric(group_df, metric_name):
    """Calculate a metric for a grouped dataframe"""
    try:
        if metric_name == 'Frequency':
            result = group_df['ClaimNb'].sum() / group_df['Exposure'].sum() if group_df['Exposure'].sum() > 0 else 0
        elif metric_name == 'AvgClaimAmount':
            result = group_df['ClaimAmount'].sum() / group_df['ClaimNb'].sum() if group_df['ClaimNb'].sum() > 0 else 0
        elif metric_name == 'AvgPremium':
            result = group_df['Pred_GLMs'].mean()
        elif metric_name == 'TotalExposure':
            result = group_df['Exposure'].sum()
        elif metric_name == 'TotalClaims':
            result = group_df['ClaimNb'].sum()
        elif metric_name == 'TotalClaimAmount':
            result = group_df['ClaimAmount'].sum()
        elif metric_name == 'PolicyCount':
            result = len(group_df)
        elif metric_name == 'ClaimRate':
            result = (group_df['ClaimNb'] > 0).sum() / len(group_df) if len(group_df) > 0 else 0
        else:
            result = 0
        return result
    except:
        return 0

def format_pivot_value(value, metric_name):
    """Format a pivot table value"""
    formats = {
        'Frequency': '{:.4f}',
        'AvgClaimAmount': '€{:,.2f}',
        'AvgPremium': '€{:,.2f}',
        'TotalExposure': '{:,.2f}',
        'TotalClaims': '{:,.0f}',
        'TotalClaimAmount': '€{:,.2f}',
        'PolicyCount': '{:,.0f}',
        'ClaimRate': '{:.2%}',
    }
    try:
        return formats.get(metric_name, '{:.2f}').format(value)
    except:
        return str(value)

# Main app
def main():
    st.title('🚗 French Motor Insurance GLM Analysis Dashboard')
    st.markdown('**Analyze GLM pure premium predictions for French motor insurance policies**')
    
    # Load data
    with st.spinner('Loading data...'):
        df = load_data()
        metrics = calculate_metrics(df)
    
    # Sidebar filters
    st.sidebar.header('📊 Data Filters')
    
    # Data split filter
    data_splits = ['All'] + sorted(df['DataMajor'].unique().tolist())
    selected_split = st.sidebar.selectbox('Data Split', data_splits)
    
    # Region filter
    regions = ['All'] + sorted(df['Region'].unique().tolist())
    selected_region = st.sidebar.multiselect('Region', regions, default=['All'])
    
    # Area filter
    areas = ['All'] + sorted(df['Area'].unique().tolist())
    selected_area = st.sidebar.multiselect('Area', areas, default=['All'])
    
    # Vehicle Brand filter
    brands = ['All'] + sorted(df['VehBrand'].unique().tolist())
    selected_brand = st.sidebar.multiselect('Vehicle Brand', brands, default=['All'])
    
    # Age range filter
    min_age, max_age = int(df['DrivAge'].min()), int(df['DrivAge'].max())
    age_range = st.sidebar.slider('Driver Age Range', min_age, max_age, (min_age, max_age))
    
    # Vehicle Power filter
    min_power, max_power = int(df['VehPower'].min()), int(df['VehPower'].max())
    power_range = st.sidebar.slider('Vehicle Power Range', min_power, max_power, (min_power, max_power))
    
    # Apply filters
    filtered_df = df.copy()
    
    if selected_split != 'All':
        filtered_df = filtered_df[filtered_df['DataMajor'] == selected_split]
    
    if 'All' not in selected_region:
        filtered_df = filtered_df[filtered_df['Region'].isin(selected_region)]
    
    if 'All' not in selected_area:
        filtered_df = filtered_df[filtered_df['Area'].isin(selected_area)]
    
    if 'All' not in selected_brand:
        filtered_df = filtered_df[filtered_df['VehBrand'].isin(selected_brand)]
    
    filtered_df = filtered_df[
        (filtered_df['DrivAge'] >= age_range[0]) &
        (filtered_df['DrivAge'] <= age_range[1]) &
        (filtered_df['VehPower'] >= power_range[0]) &
        (filtered_df['VehPower'] <= power_range[1])
    ]
    
    st.sidebar.markdown(f'**Filtered Records:** {len(filtered_df):,} / {len(df):,}')
    
    # Create tabs
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        '📊 Overview',
        '🎯 GLM Predictions',
        '📈 Claims Analysis',
        '🚗 Vehicle Features',
        '👥 Driver Demographics',
        '📋 Data Explorer',
        '🔄 Pivot Table'
    ])
    
    # Tab 1: Overview
    with tab1:
        st.header('📊 Dataset Overview')
        
        # Key metrics
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.metric('Total Policies', f"{len(filtered_df):,}")
        
        with col2:
            st.metric('Total Claims', f"{int(filtered_df['ClaimNb'].sum()):,}")
        
        with col3:
            total_exposure = filtered_df['Exposure'].sum()
            st.metric('Total Exposure', f"{total_exposure:,.2f}")
        
        with col4:
            claim_freq = filtered_df['ClaimNb'].sum() / total_exposure if total_exposure > 0 else 0
            st.metric('Claim Frequency', f"{claim_freq:.4f}")
        
        with col5:
            avg_premium = filtered_df['Pred_GLMs'].mean()
            st.metric('Avg Predicted Premium', f"€{avg_premium:,.2f}")
        
        st.markdown('---')
        
        # Charts
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader('Data Split Distribution')
            split_counts = filtered_df['DataMajor'].value_counts()
            fig = px.pie(values=split_counts.values, names=split_counts.index, 
                        title='Train/Valid/Test Split')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader('Claims Distribution')
            claim_dist = filtered_df['ClaimNb'].value_counts().sort_index()
            fig = px.bar(x=claim_dist.index, y=claim_dist.values,
                        labels={'x': 'Number of Claims', 'y': 'Count'})
            st.plotly_chart(fig, use_container_width=True)
        
        # Regional analysis
        st.subheader('Top 10 Regions by Policy Count')
        region_stats = filtered_df.groupby('Region').agg({
            'IDpol': 'count',
            'Pred_GLMs': 'mean'
        }).reset_index()
        region_stats.columns = ['Region', 'Policies', 'Avg Premium']
        region_stats = region_stats.sort_values('Policies', ascending=False).head(10)
        
        fig = px.bar(region_stats, x='Region', y='Policies', color='Avg Premium',
                    color_continuous_scale='Blues')
        st.plotly_chart(fig, use_container_width=True)
    
    # Tab 2: GLM Predictions
    with tab2:
        st.header('🎯 GLM Model Predictions Analysis')
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric('Mean Premium', f"€{filtered_df['Pred_GLMs'].mean():,.2f}")
        with col2:
            st.metric('Median Premium', f"€{filtered_df['Pred_GLMs'].median():,.2f}")
        with col3:
            st.metric('Std Premium', f"€{filtered_df['Pred_GLMs'].std():,.2f}")
        with col4:
            st.metric('Max Premium', f"€{filtered_df['Pred_GLMs'].max():,.2f}")
        
        st.markdown('---')
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader('Distribution of Predicted Premiums')
            fig = px.histogram(filtered_df, x='Pred_GLMs', nbins=50,
                             labels={'Pred_GLMs': 'Predicted Premium (€)'})
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader('Premium by Data Split')
            fig = px.box(filtered_df, x='DataMajor', y='Pred_GLMs', color='DataMajor',
                        labels={'Pred_GLMs': 'Predicted Premium (€)'})
            st.plotly_chart(fig, use_container_width=True)
        
        # Actual vs Predicted
        st.subheader('Actual vs Predicted Pure Premium')
        comparison_df = filtered_df[filtered_df['PurePremium'] > 0].copy()
        
        if len(comparison_df) > 0:
            col1, col2 = st.columns(2)
            
            with col1:
                sample_size = min(10000, len(comparison_df))
                sample_df = comparison_df.sample(n=sample_size, random_state=42)
                
                fig = px.scatter(sample_df, x='PurePremium', y='Pred_GLMs',
                               title=f'Actual vs Predicted (Sample of {sample_size:,})',
                               opacity=0.5)
                max_val = max(sample_df['PurePremium'].max(), sample_df['Pred_GLMs'].max())
                fig.add_trace(go.Scatter(x=[0, max_val], y=[0, max_val],
                                       mode='lines', name='Perfect Prediction',
                                       line=dict(color='red', dash='dash')))
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                comparison_df['Residual_Pct'] = ((comparison_df['PurePremium'] - comparison_df['Pred_GLMs']) 
                                                / comparison_df['PurePremium']) * 100
                fig = px.histogram(comparison_df, x='Residual_Pct', nbins=50,
                                 title='Prediction Errors (%)')
                st.plotly_chart(fig, use_container_width=True)
    
    # Tab 3: Claims Analysis
    with tab3:
        st.header('📈 Claims Analysis')
        
        col1, col2, col3, col4 = st.columns(4)
        total_claims = filtered_df['ClaimNb'].sum()
        policies_with_claims = (filtered_df['ClaimNb'] > 0).sum()
        total_claim_amount = filtered_df['ClaimAmount'].sum()
        avg_claim_amount = filtered_df[filtered_df['ClaimAmount'] > 0]['ClaimAmount'].mean() if (filtered_df['ClaimAmount'] > 0).any() else 0
        
        with col1:
            st.metric('Total Claims', f"{int(total_claims):,}")
        with col2:
            st.metric('Policies with Claims', f"{policies_with_claims:,}")
        with col3:
            st.metric('Total Claim Amount', f"€{total_claim_amount:,.2f}")
        with col4:
            st.metric('Avg Claim Severity', f"€{avg_claim_amount:,.2f}")
        
        st.markdown('---')
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader('Claim Frequency by Region')
            freq_by_region = filtered_df.groupby('Region').agg({
                'ClaimNb': 'sum', 'Exposure': 'sum'
            }).reset_index()
            freq_by_region['Frequency'] = freq_by_region['ClaimNb'] / freq_by_region['Exposure']
            freq_by_region = freq_by_region.sort_values('Frequency', ascending=False).head(10)
            
            fig = px.bar(freq_by_region, x='Region', y='Frequency', color='Frequency',
                        color_continuous_scale='Reds')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader('Claim Frequency by Area')
            freq_by_area = filtered_df.groupby('Area').agg({
                'ClaimNb': 'sum', 'Exposure': 'sum'
            }).reset_index()
            freq_by_area['Frequency'] = freq_by_area['ClaimNb'] / freq_by_area['Exposure']
            
            fig = px.bar(freq_by_area, x='Area', y='Frequency', color='Frequency',
                        color_continuous_scale='Oranges')
            st.plotly_chart(fig, use_container_width=True)
    
    # Tab 4: Vehicle Features
    with tab4:
        st.header('🚗 Vehicle Features Analysis')
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric('Vehicle Brands', filtered_df['VehBrand'].nunique())
        with col2:
            diesel_pct = (filtered_df['VehGas'] == 'Diesel').sum() / len(filtered_df) * 100
            st.metric('Diesel Vehicles', f"{diesel_pct:.1f}%")
        with col3:
            st.metric('Avg Vehicle Age', f"{filtered_df['VehAge'].mean():.1f} years")
        
        st.markdown('---')
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader('Top 10 Vehicle Brands')
            brand_counts = filtered_df['VehBrand'].value_counts().head(10)
            fig = px.bar(x=brand_counts.values, y=brand_counts.index, orientation='h')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader('Fuel Type Distribution')
            fuel_counts = filtered_df['VehGas'].value_counts()
            fig = px.pie(values=fuel_counts.values, names=fuel_counts.index)
            st.plotly_chart(fig, use_container_width=True)
    
    # Tab 5: Driver Demographics
    with tab5:
        st.header('👥 Driver Demographics Analysis')
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric('Avg Driver Age', f"{filtered_df['DrivAge'].mean():.1f} years")
        with col2:
            st.metric('Min Driver Age', f"{filtered_df['DrivAge'].min()} years")
        with col3:
            st.metric('Max Driver Age', f"{filtered_df['DrivAge'].max()} years")
        with col4:
            st.metric('Avg Bonus-Malus', f"{filtered_df['BonusMalus'].mean():.1f}")
        
        st.markdown('---')
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.histogram(filtered_df, x='DrivAge', nbins=50,
                             title='Distribution of Driver Age')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            age_groups = pd.cut(filtered_df['DrivAge'], 
                              bins=[0, 25, 35, 45, 55, 65, 100],
                              labels=['<25', '25-35', '35-45', '45-55', '55-65', '65+'])
            age_group_stats = filtered_df.copy()
            age_group_stats['AgeGroup'] = age_groups
            
            group_summary = age_group_stats.groupby('AgeGroup')['Pred_GLMs'].mean().reset_index()
            fig = px.bar(group_summary, x='AgeGroup', y='Pred_GLMs', 
                        title='Average Premium by Age Group',
                        color='Pred_GLMs', color_continuous_scale='Viridis')
            st.plotly_chart(fig, use_container_width=True)
    
    # Tab 6: Data Explorer
    with tab6:
        st.header('📋 Data Explorer')
        
        col1, col2 = st.columns(2)
        with col1:
            st.write(f'**Rows:** {len(filtered_df):,}')
            st.write(f'**Columns:** {len(filtered_df.columns)}')
        with col2:
            for split, count in filtered_df['DataMajor'].value_counts().items():
                pct = count / len(filtered_df) * 100
                st.write(f'**{split}:** {count:,} ({pct:.1f}%)')
        
        st.markdown('---')
        
        # Display sample data
        st.subheader('Data Sample')
        st.dataframe(filtered_df.head(100), use_container_width=True)
        
        # Download button
        csv = filtered_df.to_csv(index=False)
        st.download_button('📥 Download Filtered Data', csv, 'insurance_data.csv', 'text/csv')
        
        # Correlation matrix
        st.subheader('Correlation Matrix')
        corr_cols = ['VehPower', 'VehAge', 'DrivAge', 'BonusMalus', 'Density', 'ClaimNb', 'Pred_GLMs']
        corr_cols = [col for col in corr_cols if col in filtered_df.columns]
        corr_matrix = filtered_df[corr_cols].corr()
        
        fig = px.imshow(corr_matrix, text_auto='.2f', aspect='auto',
                       title='Correlation Matrix', color_continuous_scale='RdBu_r')
        st.plotly_chart(fig, use_container_width=True)
    
    # Tab 7: Pivot Table Explorer
    with tab7:
        st.header('🔄 Pivot Table Explorer')
        st.markdown('**Create custom pivot tables with calculated metrics**')
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.subheader('📊 Rows')
            row_dim = st.selectbox('Row Dimension', 
                                  ['Area', 'Region', 'VehBrand', 'VehGas', 'DataMajor'])
        
        with col2:
            st.subheader('📊 Columns (Optional)')
            col_dim = st.selectbox('Column Dimension', 
                                  ['None', 'Area', 'VehGas', 'DataMajor'])
        
        with col3:
            st.subheader('📈 Metrics')
            metrics_list = ['Frequency', 'AvgPremium', 'PolicyCount', 'TotalClaims', 'ClaimRate']
            selected_metrics = st.multiselect('Select Metrics', metrics_list, 
                                            default=['Frequency', 'AvgPremium'])
        
        st.markdown('---')
        
        if row_dim and selected_metrics:
            with st.spinner('Creating pivot table...'):
                # Create pivot table
                if col_dim == 'None':
                    # Simple aggregation
                    pivot_result = filtered_df.groupby(row_dim).apply(
                        lambda x: pd.Series({
                            metric: calculate_pivot_metric(x, metric) 
                            for metric in selected_metrics
                        })
                    ).reset_index()
                    
                    # Format values
                    for metric in selected_metrics:
                        pivot_result[f'{metric}_fmt'] = pivot_result[metric].apply(
                            lambda x: format_pivot_value(x, metric)
                        )
                    
                    st.subheader('📊 Pivot Table Results')
                    display_cols = [row_dim] + [f'{m}_fmt' for m in selected_metrics]
                    display_df = pivot_result[display_cols].copy()
                    display_df.columns = [row_dim] + selected_metrics
                    st.dataframe(display_df, use_container_width=True, height=400)
                    
                    # Download
                    csv = pivot_result[[row_dim] + selected_metrics].to_csv(index=False)
                    st.download_button('📥 Download Pivot Table', csv, 'pivot_table.csv', 'text/csv')
                    
                    # Visualization
                    if selected_metrics:
                        viz_metric = st.selectbox('Visualize Metric:', selected_metrics)
                        
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            top_20 = pivot_result.sort_values(viz_metric, ascending=False).head(20)
                            fig = px.bar(top_20, x=row_dim, y=viz_metric,
                                       title=f'{viz_metric} by {row_dim}',
                                       color=viz_metric)
                            st.plotly_chart(fig, use_container_width=True)
                        
                        with col2:
                            top_10 = pivot_result.sort_values(viz_metric, ascending=False).head(10)
                            fig = px.pie(top_10, values=viz_metric, names=row_dim,
                                       title=f'Top 10: {viz_metric} Distribution')
                            st.plotly_chart(fig, use_container_width=True)
                else:
                    # 2D pivot
                    pivot_result = filtered_df.groupby([row_dim, col_dim]).apply(
                        lambda x: pd.Series({
                            metric: calculate_pivot_metric(x, metric)
                            for metric in selected_metrics
                        })
                    ).reset_index()
                    
                    for metric in selected_metrics:
                        st.subheader(f'📊 {metric}')
                        pivot_table = pivot_result.pivot(index=row_dim, columns=col_dim, 
                                                        values=metric).fillna(0)
                        st.dataframe(pivot_table, use_container_width=True)
                        
                        fig = px.imshow(pivot_table, 
                                      title=f'{metric}: {row_dim} × {col_dim}',
                                      color_continuous_scale='RdYlGn', aspect='auto')
                        st.plotly_chart(fig, use_container_width=True)
        else:
            st.info('👆 Select row dimension and at least one metric to create a pivot table.')

if __name__ == '__main__':
    main()
