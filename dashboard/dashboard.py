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

# Visualization 3: Clustered Bar Chart by Weekday and Time Category
st.header("Total Rentals by Weekday and Time Category")
time_category_grouped = filtered_df.groupby(['weekday', 'time_category'], observed=False)['total_rentals_hourly'].sum().unstack()
fig3, ax3 = plt.subplots(figsize=(10, 6))
time_category_grouped.plot(kind='bar', ax=ax3, cmap='viridis', width=0.8)
ax3.set_title('Clustered Bar Chart of Total Rentals by Weekday and Time Category', fontsize=14)
ax3.set_xlabel('Weekday', fontsize=12)
ax3.set_ylabel('Total Rentals', fontsize=12)
plt.xticks(rotation=45, fontsize=10)
plt.legend(title='Time Category', bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=10)
plt.tight_layout()
st.pyplot(fig3)

# Visualization 4: Bar and Pie Charts for Rentals at 16:00
st.header("Rentals by Weather Condition at 16:00")
filtered_time_df = filtered_df[filtered_df['time'] == '16:00']
weather_stats = filtered_time_df.groupby('weather_condition_daily').agg({'total_rentals_daily': 'mean'}).reset_index()
weather_stats.columns = ['weather_condition', 'mean_rentals']
fig4a, ax4a = plt.subplots(figsize=(6, 4))
ax4a.bar(weather_stats['weather_condition'], weather_stats['mean_rentals'], color=['#1f77b4', '#ff7f0e', '#2ca02c'])
ax4a.set_title('Average Bike Rentals by Weather Condition (16:00)', fontsize=14)
ax4a.set_xlabel('Weather Condition', fontsize=12)
ax4a.set_ylabel('Average Rentals', fontsize=12)
ax4a.grid(axis='y', linestyle='--', alpha=0.7)
st.pyplot(fig4a)

fig4b, ax4b = plt.subplots()
ax4b.pie(weather_stats['mean_rentals'], labels=weather_stats['weather_condition'], autopct='%1.1f%%', startangle=140, colors=['#1f77b4', '#ff7f0e', '#2ca02c'], explode=(0.05, 0.05, 0.05))
ax4b.set_title('Percentage of Rentals by Weather Condition (16:00)', fontsize=14)
plt.tight_layout()
st.pyplot(fig4b)

# Visualization 5: Stacked Bar Chart of Rentals by Weather Condition and Temperature
st.header("Rentals by Weather Condition and Temperature")
grouped_data = filtered_df.groupby(['weather_condition_hourly', 'temperature_category']).agg({'total_rentals_hourly': ['mean', 'sum']}).reset_index()
grouped_data.columns = ['weather_condition', 'temperature_category', 'mean_rentals', 'total_rentals']
pivot_data = grouped_data.pivot(index='weather_condition', columns='temperature_category', values='mean_rentals')
pivot_data = pivot_data[['Cold', 'Moderate', 'Hot']]
fig5, ax5 = plt.subplots(figsize=(10, 6))
pivot_data.plot(kind='bar', stacked=True, ax=ax5, color=['#1f77b4', '#ff7f0e', '#d62728'])
ax5.set_title('Stacked Bar Chart of Rentals by Weather Condition and Temperature', fontsize=14)
ax5.set_xlabel('Weather Condition', fontsize=12)
ax5.set_ylabel('Average Rentals', fontsize=12)
plt.xticks(rotation=0)
plt.legend(title='Temperature Category', fontsize=10)
ax5.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
st.pyplot(fig5)

# Visualization 6: Heatmap of Hourly Rentals by Weather Condition
st.header("Hourly Rentals by Weather Condition")
hourly_weather_pivot = filtered_df.pivot_table(values='total_rentals_hourly', index='time', columns='weather_condition_hourly', aggfunc='mean')
fig6, ax6 = plt.subplots(figsize=(12, 6))
sns.heatmap(hourly_weather_pivot, annot=True, fmt='.1f', cmap='coolwarm', cbar_kws={'label': 'Average Rentals'})
plt.title('Heatmap of Hourly Rentals by Weather Condition', fontsize=14)
plt.xlabel('Weather Condition', fontsize=12)
plt.ylabel('Hour of the Day', fontsize=12)
plt.xticks(rotation=45)
plt.yticks(rotation=0)
plt.tight_layout()
st.pyplot(fig6)

# Visualization 7: Heatmap of Rentals by Peak/Off-Peak and Weather Condition
st.header("Rentals by Peak/Off-Peak and Weather Condition")
filtered_df['peak_category'] = filtered_df['time'].str[:2].astype(int).apply(lambda x: 'Peak' if 7 <= x <= 9 or 17 <= x <= 19 else 'Off-Peak')
peak_weather_pivot = filtered_df.pivot_table(values='total_rentals_hourly', index='peak_category', columns='weather_condition_hourly', aggfunc='mean')
fig7, ax7 = plt.subplots(figsize=(8, 5))
sns.heatmap(peak_weather_pivot, annot=True, fmt='.1f', cmap='YlGnBu', cbar_kws={'label': 'Average Rentals'})
plt.title('Heatmap of Rentals by Peak/Off-Peak and Weather Condition', fontsize=14)
plt.xlabel('Weather Condition', fontsize=12)
plt.ylabel('Time of Day (Peak/Off-Peak)', fontsize=12)
plt.xticks(rotation=45)
plt.yticks(rotation=0)
plt.tight_layout()
st.pyplot(fig7)

