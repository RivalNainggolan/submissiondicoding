import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
merged_df = pd.read_csv("dashboard/main.csv")

# Title and Logo
import streamlit as st
from PIL import Image

# Display logo
st.title("Bike Rental Analysis Dashboard")

# Add the logo to the sidebar
st.sidebar.image("bike_rent_logo.png", width=180)

# Add your filter features below
st.sidebar.header("Filter Options")
selected_years = st.sidebar.multiselect("Select Year(s)", options=merged_df['year'].unique(), default=merged_df['year'].unique())
selected_hour_filter = st.sidebar.radio("Filter by Time", ("All Hours", "Specific Hour"), index=0)

# Hour filter
if selected_hour_filter == "Specific Hour":
    selected_hour = st.sidebar.selectbox("Select Hour", options=merged_df['time'].unique())
    filtered_df = merged_df[merged_df['time'] == selected_hour]
else:
    filtered_df = merged_df.copy()

# Day filter
selected_day_filter = st.sidebar.radio("Filter by Day", ("All Days", "Specific Day"), index=0)
if selected_day_filter == "Specific Day":
    selected_day = st.sidebar.selectbox("Select Day", options=merged_df['weekday'].unique())
    filtered_df = filtered_df[filtered_df['weekday'] == selected_day]

# Apply Year Filter
filtered_df = filtered_df[filtered_df['year'].isin(selected_years)]

# Visualization 1: Bar Chart of Average Rentals by Weekday
st.header("Average Total Rentals by Weekday")
weekday_grouped = filtered_df.groupby('weekday').agg({'total_rentals_daily': ['mean']}).reset_index()
weekday_grouped.columns = ['weekday', 'average_rentals']
weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
weekday_grouped['weekday'] = pd.Categorical(weekday_grouped['weekday'], categories=weekday_order, ordered=True)
weekday_grouped = weekday_grouped.sort_values('weekday')
fig1, ax1 = plt.subplots(figsize=(10, 6))
sns.barplot(data=weekday_grouped, x='weekday', y='average_rentals', palette='viridis', hue='weekday', dodge=False)
plt.title('Average Total Rentals by Weekday', fontsize=16)
plt.xlabel('Weekday', fontsize=12)
plt.ylabel('Average Rentals', fontsize=12)
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', linewidth=0.5)
plt.legend([], [], frameon=False)
plt.tight_layout()
st.pyplot(fig1)

# Visualization 2: Line Chart of Hourly Bike Rentals
st.header("Hourly Bike Rentals Analysis")
hourly_grouped = filtered_df.groupby('time').agg({'total_rentals_hourly': ['mean']}).reset_index()
hourly_grouped.columns = ['time', 'mean_rentals']
fig2, ax2 = plt.subplots(figsize=(12, 6))
ax2.plot(hourly_grouped['time'], hourly_grouped['mean_rentals'], label='Mean Rentals', marker='o')
ax2.set_title('Hourly Bike Rentals Analysis', fontsize=16)
ax2.set_xlabel('Time (Hourly)', fontsize=12)
ax2.set_ylabel('Number of Rentals', fontsize=12)
ax2.grid(axis='y', linestyle='--', linewidth=0.5)
ax2.legend(title='Rental Statistics', fontsize=10, title_fontsize=12)
plt.tight_layout()
st.pyplot(fig2)

# Add more visualizations as needed...
