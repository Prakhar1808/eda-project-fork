# app.py
import streamlit as st
import sys
import os
# Add the path to your module
sys.path.append('Prakhar/converted_scripts/dataVisualization')

# Import your new modular functions
try:
    import eda_functions as eda
except ImportError as e:
    st.error(f"Could not import module: {e}")
    st.stop()

st.set_page_config(layout="wide")
st.title("📊 Instagram Usage & Lifestyle Dashboard")

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
    if st.button("Show Basic Information"):
        # Use our function
        info_text = eda.get_basic_info(df)
        st.text_area("Data Info", info_text, height=400)
    
    st.subheader("Interactive Data Preview")
    num_rows = st.slider("Rows to show", 5, 50, 10)
    st.dataframe(df.head(num_rows), use_container_width=True)

with tab2:
    st.header("Visualizations")
    # Use selectbox to choose which plot to show
    plot_choice = st.selectbox(
        "Choose a visualization:",
        [
            "Daily Activity Distribution",
            "Activity by Gender",
            "Reels Watched by Activity",
            "Activity by Employment",
            # ... add all other plot names
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
