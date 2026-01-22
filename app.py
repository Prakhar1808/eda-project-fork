# app.py
import streamlit as st
import sys
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# Add the path to your module
sys.path.append('Prakhar/converted_scripts/dataVisualization')

# Import your new modular functions
try:
    import eda_functions as eda
except ImportError as e:
    st.error(f"Could not import module: {e}")
    st.stop()

st.set_page_config(layout="wide")
st.title("Instagram Usage & Lifestyle Dashboard")

# --- Sidebar for Controls ---
with st.sidebar:
    st.header("Data Input")
    # Option A: File Uploader
    uploaded_file = st.file_uploader("Upload your CSV", type=['csv'])

    # Option B: Use the original file (you'll need to adjust the path for Linux)
    use_sample = st.checkbox("Use sample dataset path")

    if use_sample:
        # You MUST update this path to point to your actual CSV file on Arch Linux
        file_path = "/home/prakhar/Documents/GitHub/eda-project-fork/instagram_users_lifestyle.csv"
    else:
        file_path = None

# --- Load Data ---
df = None
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.sidebar.success(f"Uploaded: {uploaded_file.name}")
elif use_sample and os.path.exists(file_path):
    df = eda.load_data(file_path)  # Use our function
    st.sidebar.info("Using sample dataset.")
else:
    st.info("👈 Please upload a CSV file or select the sample dataset to begin.")
    st.stop()

# --- Main Dashboard Tabs ---
tab1, tab2, tab3 = st.tabs(["Data Overview", "Visualizations", "Correlations"])

with tab1:
    st.header("Dataset Overview")
    
    # Quick stats at the top
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Rows", df.shape[0])
    with col2:
        st.metric("Total Columns", df.shape[1])
    with col3:
        numeric_cols = df.select_dtypes(include=[np.number]).shape[1]
        st.metric("Numeric Columns", numeric_cols)
    with col4:
        missing_total = df.isna().sum().sum()
        st.metric("Missing Values", missing_total)
    
    # Interactive controls in an expander
    with st.expander("📊 Detailed Data Explorer", expanded=True):
        # Row/Column selection
        col_a, col_b = st.columns(2)
        with col_a:
            preview_rows = st.slider(
                "Rows to preview", 
                min_value=5, 
                max_value=min(100, len(df)),  # Don't exceed 100 rows
                value=10,
                help="Large datasets: keep this small for faster preview"
            )
        
        with col_b:
            # Let user select specific columns to show
            all_columns = df.columns.tolist()
            default_cols = all_columns[:min(10, len(all_columns))]  # First 10 columns
            selected_columns = st.multiselect(
                "Columns to display",
                all_columns,
                default=default_cols,
                help="Select specific columns to reduce memory usage"
            )
        
        # Show data preview
        st.subheader("Data Preview")
        if selected_columns:
            try:
                # Use Streamlit's dataframe with height limit
                st.dataframe(
                    df[selected_columns].head(preview_rows),
                    use_container_width=True,
                    height=400
                )
                
                # Show a sample warning for large datasets
                if len(df) > 10000:
                    st.info(f"Showing first {preview_rows} rows of {len(df):,} total rows. Data has been sampled for performance.")
            except Exception as e:
                st.error(f"Error displaying data: {e}")
                # Fallback: show just the first few rows without selection
                st.dataframe(df.head(5))
        else:
            st.warning("Please select at least one column to display")
    
    # Basic Information in an expander
    with st.expander("📋 Basic Dataset Information", expanded=False):
        if st.button("Generate Summary", key="summary_btn"):
            with st.spinner("Processing dataset info..."):
                try:
                    # Use caching for expensive operations
                    @st.cache_data
                    def get_summary_stats(_df):
                        return {
                            'dtypes': _df.dtypes,
                            'missing': _df.isna().sum(),
                            'numeric_summary': _df.describe() if not _df.select_dtypes(include=[np.number]).empty else None
                        }
                    
                    stats = get_summary_stats(df)
                    
                    # Display in columns
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write("**Data Types:**")
                        dtype_df = pd.DataFrame(stats['dtypes'].reset_index())
                        dtype_df.columns = ['Column', 'Data Type']
                        st.dataframe(dtype_df, height=300, use_container_width=True)
                    
                    with col2:
                        st.write("**Missing Values:**")
                        missing_df = pd.DataFrame(stats['missing'][stats['missing'] > 0].reset_index())
                        if not missing_df.empty:
                            missing_df.columns = ['Column', 'Missing Count']
                            st.dataframe(missing_df, height=300, use_container_width=True)
                            # Visualize missing values
                            st.bar_chart(missing_df.set_index('Column'))
                        else:
                            st.success("✅ No missing values!")
                    
                    # Show numeric summary if available
                    if stats['numeric_summary'] is not None:
                        st.write("**Numeric Columns Summary:**")
                        st.dataframe(stats['numeric_summary'], use_container_width=True)
                
                except Exception as e:
                    st.error(f"Error generating summary: {e}")
    
    # Column Explorer
    with st.expander("🔍 Column Explorer", expanded=False):
        selected_col = st.selectbox("Select a column to explore:", df.columns)
        
        if selected_col:
            col_data = df[selected_col]
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"**Statistics for `{selected_col}`**")
                st.write(f"Data type: `{col_data.dtype}`")
                st.write(f"Unique values: `{col_data.nunique()}`")
                st.write(f"Missing values: `{col_data.isna().sum()}`")
                
                if pd.api.types.is_numeric_dtype(col_data):
                    st.write(f"Min: `{col_data.min():.2f}`")
                    st.write(f"Max: `{col_data.max():.2f}`")
                    st.write(f"Mean: `{col_data.mean():.2f}`")
                    st.write(f"Std Dev: `{col_data.std():.2f}`")
            
            with col2:
                # Quick visualization based on data type
                if pd.api.types.is_numeric_dtype(col_data):
                    # For large datasets, sample the data
                    if len(col_data) > 10000:
                        sample_data = col_data.sample(10000, random_state=42)
                        st.write(f"*Showing 10,000 sample points of {len(col_data):,} total*")
                    else:
                        sample_data = col_data
                    
                    fig, ax = plt.subplots(figsize=(8, 4))
                    ax.hist(sample_data.dropna(), bins=30, edgecolor='black')
                    ax.set_title(f"Distribution of {selected_col}")
                    ax.set_xlabel(selected_col)
                    ax.set_ylabel("Frequency")
                    st.pyplot(fig)
                elif pd.api.types.is_categorical_dtype(col_data) or col_data.nunique() < 20:
                    # Show value counts for categorical
                    value_counts = col_data.value_counts().head(10)
                    st.bar_chart(value_counts)
    
    # Data Quality Check
    with st.expander("✅ Data Quality Check", expanded=False):
        quality_issues = []
        
        # Check for columns with high missing percentage
        missing_pct = (df.isna().sum() / len(df)) * 100
        high_missing = missing_pct[missing_pct > 50].index.tolist()
        if high_missing:
            quality_issues.append(f"⚠️ {len(high_missing)} columns have >50% missing values")
        
        # Check for constant columns
        constant_cols = [col for col in df.columns if df[col].nunique() == 1]
        if constant_cols:
            quality_issues.append(f"⚠️ {len(constant_cols)} constant columns (single value)")
        
        # Check for duplicate rows
        duplicates = df.duplicated().sum()
        if duplicates > 0:
            quality_issues.append(f"⚠️ {duplicates} duplicate rows found")
        
        if quality_issues:
            for issue in quality_issues:
                st.warning(issue)
        else:
            st.success("✅ No major data quality issues detected")

with tab2:
    st.header("Visualizations")
    # Use selectbox to choose which plot to show
    plot_choice = st.selectbox(
        "Choose a visualization:",
        [
            "Daily Activity Distribution",
            "Activity by Gender",
            "Reels Watched by Activity",
            "Instagram Activity by Age",
            "DMs sent by Relationship Status",
            # ... add all other plot names here
        ]
    )

    if plot_choice == "Daily Activity Distribution":
        fig = eda.plot_activity_distribution(df)
        if fig:
            st.pyplot(fig)
        else:
            st.warning("Required columns not found in data.")
    elif plot_choice == "Activity by Gender":
        fig = eda.plot_activity_by_gender(df)
        if fig:
            st.pyplot(fig)
        else:
            st.warning("Required columns not found in data.")
    elif plot_choice == "Reels Watched by Activity":
        fig = eda.plot_reels_by_activity(df)
        if fig:
            st.pyplot(fig)
        else:
            st.warning("Required columns not found in data.")
    elif plot_choice == "Instagram Activity by Age":
        fig = eda.plot_activity_by_age(df)
        if fig:
            st.pyplot(fig)
        else:
            st.warning("Required columns not found in data.")
    elif plot_choice == "DMs sent by Relationship Status":
        fig = eda.plot_dms_by_relationship_status(df)
        if fig:
            st.pyplot(fig)
        else:
            st.warning("Required columns not found in data.")
    # ... add more elif blocks for each plot

with tab3:
    st.header("Feature Correlations")
    if st.button("Generate Correlation Heatmap"):
        fig = eda.plot_correlation_matrix(df)
        if fig:
            st.pyplot(fig)
        else:
            st.warning("Not enough numeric columns for correlation.")

# --- Bonus: Download Processed Data ---
st.sidebar.divider()
st.sidebar.header("Export")
if st.sidebar.button("Prepare Data for Download"):
    # Example: Save the dataframe with the new 'activity_bin' column
    csv = df.to_csv(index=False).encode('utf-8')
    st.sidebar.download_button(
        label="Download CSV",
        data=csv,
        file_name="processed_instagram_data.csv",
        mime="text/csv",
    )
