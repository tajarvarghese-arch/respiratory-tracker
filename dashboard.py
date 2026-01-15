import streamlit as st
import json
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt

st.set_page_config(page_title="Respiratory Virus Tracker - New York", layout="wide")

st.title("Respiratory Virus Tracker - New York County")
st.write("Real historical flu data (2011-2026) + recent COVID-19 and RSV data from NYC DOH")

try:
    with open('respiratory_data.json', 'r') as file:
        data = json.load(file)
    
    dates = sorted(data.keys())
    
    df_data = []
    for date in dates:
        ny_data = data[date]["New York"]
        df_data.append({
            "Date": pd.to_datetime(date),
            "Flu": ny_data["flu_cases"],
            "COVID": ny_data["covid_cases"],
            "RSV": ny_data["rsv_cases"]
        })
    
    df = pd.DataFrame(df_data)
    
    st.subheader("Latest Weekly Data (as of January 10, 2026)")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        latest_flu = df["Flu"].iloc[-1]
        st.metric("Flu Cases", f"{latest_flu:,}", delta="↓ Decreasing")
    
    with col2:
        latest_covid = df["COVID"].iloc[-1]
        st.metric("COVID-19 Cases", f"{latest_covid:,}", delta="↑ Increasing")
    
    with col3:
        latest_rsv = df["RSV"].iloc[-1]
        st.metric("RSV Cases", f"{latest_rsv:,}", delta="↓ Stable")
    
    st.divider()
    
    st.subheader("Respiratory Virus Trends Over Time")
    
    fig, ax = plt.subplots(figsize=(14, 7))
    
    ax.plot(df["Date"], df["Flu"], label="Flu", color="blue", linewidth=2.5, marker='o', markersize=4)
    ax.plot(df["Date"], df["COVID"], label="COVID-19", color="red", linewidth=2.5, marker='s', markersize=4)
    ax.plot(df["Date"], df["RSV"], label="RSV", color="green", linewidth=2.5, marker='^', markersize=4)
    
    ax.set_xlabel("Date", fontsize=12, fontweight='bold')
    ax.set_ylabel("Number of Cases", fontsize=12, fontweight='bold')
    ax.set_title("New York County Respiratory Virus Cases - Historical Trends")
    ax.legend(fontsize=11, loc='upper left')
    ax.grid(True, alpha=0.3)
    
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    st.pyplot(fig)
    
    st.divider()
    
    st.subheader("Filter by Date Range")
    
    min_date = df["Date"].min()
    max_date = df["Date"].max()
    
    date_range = st.date_input(
        "Select date range to analyze:",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )
    
    if len(date_range) == 2:
        start, end = date_range
        filtered_df = df[(df["Date"] >= pd.to_datetime(start)) & (df["Date"] <= pd.to_datetime(end))]
        
        st.subheader("Filtered View - " + str(len(filtered_df)) + " weeks of data")
        
        fig2, ax2 = plt.subplots(figsize=(14, 7))
        
        ax2.plot(filtered_df["Date"], filtered_df["Flu"], label="Flu", color="blue", linewidth=2.5, marker='o')
        ax2.plot(filtered_df["Date"], filtered_df["COVID"], label="COVID-19", color="red", linewidth=2.5, marker='s')
        ax2.plot(filtered_df["Date"], filtered_df["RSV"], label="RSV", color="green", linewidth=2.5, marker='^')
        
        ax2.set_xlabel("Date")
        ax2.set_ylabel("Number of Cases")
        ax2.set_title("Respiratory Viruses in Selected Date Range")
        ax2.legend(fontsize=11)
        ax2.grid(True, alpha=0.3)
        
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        st.pyplot(fig2)
        
        st.divider()
        
        st.subheader("Statistics for Selected Period")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.write("**Flu Statistics**")
            st.metric("Average", f"{filtered_df['Flu'].mean():.0f}")
            st.metric("Peak", f"{filtered_df['Flu'].max():.0f}")
            st.metric("Total", f"{filtered_df['Flu'].sum():.0f}")
        
        with col2:
            st.write("**COVID-19 Statistics**")
            st.metric("Average", f"{filtered_df['COVID'].mean():.0f}")
            st.metric("Peak", f"{filtered_df['COVID'].max():.0f}")
            st.metric("Total", f"{filtered_df['COVID'].sum():.0f}")
        
        with col3:
            st.write("**RSV Statistics**")
            st.metric("Average", f"{filtered_df['RSV'].mean():.0f}")
            st.metric("Peak", f"{filtered_df['RSV'].max():.0f}")
            st.metric("Total", f"{filtered_df['RSV'].sum():.0f}")

except FileNotFoundError:
    st.error("Error: respiratory_data.json not found")
except Exception as e:
    st.error("Error: " + str(e))
