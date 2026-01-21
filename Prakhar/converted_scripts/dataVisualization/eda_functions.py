# eda_functions.py
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set a consistent style for all plots
sns.set_style("whitegrid")

# 1. DATA LOADING FUNCTION
def load_data(file_path):
    """
    Loads the dataset from a given file path.
    Adjusts for the fact the original path was Windows-specific.
    """
    df = pd.read_csv(file_path)
    
    # Create the 'activity_bin' column if the original column exists
    if 'daily_active_minutes_instagram' in df.columns:
        df["activity_bin"] = pd.cut(
            df["daily_active_minutes_instagram"],
            bins=[0, 100, 200, 300, 400, 500],
            labels=["0–100", "100–200", "200–300", "300–400", "400–500"]
        )
    
    # Note: 'df_filtered' from the original script is undefined.
    # We'll handle age filtering inside a specific function later.
    return df

# 2. BASIC DATA INFO FUNCTION
def get_basic_info(df):
    """Returns basic dataframe info as strings for display."""
    buffer = []
    buffer.append(f"Dataset Shape: {df.shape[0]} rows, {df.shape[1]} columns")
    buffer.append("\n--- First 5 Rows ---")
    buffer.append(df.head().to_string())
    buffer.append("\n--- Column Names ---")
    buffer.append(", ".join(df.columns))
    buffer.append("\n--- Summary Statistics ---")
    buffer.append(df.describe().to_string())
    buffer.append(f"\n--- Missing Values ---\n{df.isna().sum().to_string()}")
    return "\n".join(buffer)

# 3. VISUALIZATION FUNCTIONS (One per plot from the original script)
def plot_activity_distribution(df):
    """Histogram of daily active minutes."""
    if 'daily_active_minutes_instagram' not in df.columns:
        return None
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.histplot(df['daily_active_minutes_instagram'], bins=20, kde=True, ax=ax)
    ax.set_title("Distribution of Daily Active Minutes on Instagram", fontsize=14)
    ax.set_xlabel("Daily Active Minutes", fontsize=12)
    ax.set_ylabel("User Count", fontsize=12)
    return fig

def plot_activity_by_gender(df):
    """Count plot of activity bins by gender."""
    if 'activity_bin' not in df.columns or 'gender' not in df.columns:
        return None
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.countplot(data=df, x="gender", hue="activity_bin", ax=ax)
    ax.set_title("Instagram Activity by Gender")
    ax.set_xlabel("Gender")
    ax.set_ylabel("User Count")
    ax.legend(title="Daily Active Minutes")
    return fig

def plot_reels_by_activity(df):
    """Bar plot: average reels watched per activity bin."""
    # ... (Implement similar to above for the 'reels_watched_per_day' plot)
    # Use the original plotting code but ensure it returns 'fig'
    pass

# 4. CORRELATION MATRIX FUNCTION
def plot_correlation_matrix(df):
    """Plots a heatmap of the correlation matrix."""
    numeric_df = df.select_dtypes(include=[np.number])
    if numeric_df.shape[1] < 2:
        return None
    corr = numeric_df.corr()
    fig, ax = plt.subplots(figsize=(12, 8))
    sns.heatmap(corr, annot=True, fmt=".2f", cmap='coolwarm', center=0, ax=ax)
    ax.set_title("Feature Correlation Matrix")
    return fig

# Add more functions for each visualization in your original script...
