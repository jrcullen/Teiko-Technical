import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Set page config
st.set_page_config(page_title="Immune Cell Dashboard", layout="wide")

# Load data
summary_df = pd.read_csv("outputs/summary.csv")
stats_df = pd.read_csv("outputs/stats.csv")
subset_df = pd.read_csv("outputs/subset_data.csv")
boxplot_path = "outputs/boxplot.png"

st.title("Loblaw Bio Clinical Trial Dashboard")
st.markdown("Interactive dashboard for Bob's trial analysis")

# Overview Table (Part 2)
st.header("Data Overview: Immune Cell Frequencies")

with st.expander("Show filters"):
    sample_filter = st.multiselect(
        "Select Sample(s):",
        options=summary_df["sample"].unique()
    )
    population_filter = st.multiselect(
        "Select Population(s):",
        options=summary_df["population"].unique()
    )

filtered_summary = summary_df.copy()
if sample_filter:
    filtered_summary = filtered_summary[filtered_summary["sample"].isin(sample_filter)]
if population_filter:
    filtered_summary = filtered_summary[filtered_summary["population"].isin(population_filter)]

st.dataframe(filtered_summary.reset_index(drop=True))

# Responders vs Non-Responders (Part 3)
st.header("Statistical Analysis: Responders vs Non-Responders")

st.image(boxplot_path, caption="Boxplot: Percentage of Cell Populations by Response", use_container_width=True)

st.subheader("Significant Differences Between Responders and Non-Responders")
st.dataframe(stats_df.style.format({"p_value": "{:.4f}"}))

# Subset Analysis (Part 4)
st.header("Data Subset Analysis: Baseline Melanoma PBMC Samples")

# Filters for subset analysis
st.subheader("Filters")
condition_filter = st.selectbox("Condition", ["melanoma"], index=0, disabled=True)
sample_type_filter = st.selectbox("Sample Type", ["PBMC"], index=0, disabled=True)
treatment_filter = st.selectbox("Treatment", ["miraclib"], index=0, disabled=True)
time_filter = st.number_input("Time from treatment start", value=0, min_value=0)

filtered_subset = subset_df[
    (subset_df["condition"] == condition_filter) &
    (subset_df["sample_type"] == sample_type_filter) &
    (subset_df["treatment"] == treatment_filter) &
    (subset_df["time_from_treatment_start"] == time_filter)
]

# Compute metrics
samples_per_project = filtered_subset.groupby("project")["sample"].nunique()
responders_count = filtered_subset[filtered_subset["response"]=="yes"]["subject"].nunique()
non_responders_count = filtered_subset[filtered_subset["response"]=="no"]["subject"].nunique()
males_count = filtered_subset[filtered_subset["sex"]=="M"]["subject"].nunique()
females_count = filtered_subset[filtered_subset["sex"]=="F"]["subject"].nunique()

avg_b_cells_males_responders = filtered_subset[
    (filtered_subset["sex"]=="M") & (filtered_subset["response"]=="yes")
]["b_cell"].mean()
if pd.notna(avg_b_cells_males_responders):
    avg_b_cells_males_responders = round(avg_b_cells_males_responders, 2)

# Display metrics nicely
st.subheader("Metrics")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Responders", responders_count)
    st.metric("Non-Responders", non_responders_count)
with col2:
    for proj, count in samples_per_project.items():
        st.metric(f"Samples in {proj}", count)
with col3:
    st.metric("Males", males_count)
    st.metric("Females", females_count)

st.subheader("Average B Cells (Melanoma Males, Responders, Time=0)")
st.write(f"**{avg_b_cells_males_responders}**")

st.subheader("Filtered Subset Data")
st.dataframe(filtered_subset.reset_index(drop=True))