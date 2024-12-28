import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Load the dataset
merged_df = pd.read_csv("dashboard/main.csv")
day_df = pd.read_csv("dashboard/daycleaned.csv")

# Title and Logo
import streamlit as st
from PIL import Image

# Display logo
st.title("Bike Rental Analysis Dashboard")

# Add the logo to the sidebar
st.sidebar.image("dashboard/bike_rent_logo.png", width=180)

# Add your filter features below
st.sidebar.header("Filter Options")
# Year Filter
selected_year = st.sidebar.selectbox(
    "Select Year",
    options=["All Years"] + list(merged_df['year'].unique()),
    index=0  # Default to "All Years"
)

# Day Filter
selected_day = st.sidebar.selectbox(
    "Select Day",
    options=["All Days"] + list(merged_df['weekday'].unique()),
    index=0  # Default to "All Days"
)

# Time Filter
selected_time = st.sidebar.selectbox(
    "Select Time",
    options=["All Hours"] + list(merged_df['time'].unique()),
    index=0  # Default to "All Hours"
)

# Apply Filters
filtered_df = merged_df.copy()
if selected_year != "All Years":
    filtered_df = filtered_df[filtered_df['year'] == selected_year]

if selected_day != "All Days":
    filtered_df = filtered_df[filtered_df['weekday'] == selected_day]

if selected_time != "All Hours":
    filtered_df = filtered_df[filtered_df['time'] == selected_time]

# Define weather condition mapping
weather_condition_mapping = {1: 'Clear/Partly Cloudy', 2: 'Misty/Cloudy', 3: 'Light Rain/Snow'}

# Weather Condition Filter
selected_weather = st.sidebar.selectbox(
    "Select Weather Condition",
    options=["All Conditions"] + list(weather_condition_mapping.values()),
    index=0  # Default to "All Conditions"
)

if selected_weather != "All Conditions":
    filtered_df = filtered_df[filtered_df['weather_condition_hourly'] == selected_weather]


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

# Visualization 4: Bar and Pie Charts for Rentals 
st.header("Rentals by Weather Condition")
weather_stats = day_df.groupby('weather_condition').agg({'total_rentals': 'mean'}).reset_index()
weather_stats.columns = ['weather_condition', 'mean_rentals']
fig4a, ax4a = plt.subplots(figsize=(6, 4))
ax4a.bar(weather_stats['weather_condition'], weather_stats['mean_rentals'], color=['#1f77b4', '#ff7f0e', '#2ca02c'])
ax4a.set_title('Average Bike Rentals by Weather Condition Daily', fontsize=14)
ax4a.set_xlabel('Weather Condition', fontsize=12)
ax4a.set_ylabel('Average Rentals', fontsize=12)
ax4a.grid(axis='y', linestyle='--', alpha=0.7)
st.pyplot(fig4a)


# Dynamically generate the explode parameter based on the length of the data
explode_values = [0.05] * len(weather_stats['mean_rentals'])

fig4b, ax4b = plt.subplots()
ax4b.pie(
    weather_stats['mean_rentals'], 
    labels=weather_stats['weather_condition'], 
    autopct='%1.1f%%', 
    startangle=140, 
    colors=['#1f77b4', '#ff7f0e', '#2ca02c'], 
    explode=explode_values  # Use dynamically generated explode values
)
ax4b.set_title('Percentage of Rentals by Weather Condition', fontsize=14)
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

# Visualization 8: Clustered Bar Chart of Rentals by Time Status
st.header("Clustered Bar Chart of Rentals by Time Status")

# Filter the DataFrame for specific times
filtered_df = merged_df[merged_df['time'].isin(['08:00', '10:00', '14:00', '18:00'])].copy()

# Add a new column 'peak_status' based on the time slots
filtered_df['peak_status'] = filtered_df['time'].apply(
    lambda x: 'Peak' if x in ['08:00', '18:00'] else 'Off-Peak'
)

# Add a new column 'rental_category' using bins for total rentals
filtered_df['rental_category'] = pd.cut(
    filtered_df['total_rentals_hourly'],
    bins=[0, 50, 200, filtered_df['total_rentals_hourly'].max()],
    labels=['Low', 'Medium', 'High']
)

# Combine `time` and `peak_status` into a new column `time_status`
filtered_df['time_status'] = filtered_df['time'] + " (" + filtered_df['peak_status'] + ")"

# Group and pivot data by 'time_status' and 'rental_category'
pivot_table = filtered_df.pivot_table(
    values='total_rentals_hourly',
    index='rental_category',
    columns='time_status',
    aggfunc='size',
    fill_value=0
)

# Define bar width
bar_width = 0.2
positions = np.arange(len(pivot_table.index))

# Create the plot
fig8, ax8 = plt.subplots(figsize=(12, 6))

# Colors for Peak and Off-Peak times
colors = ['#1E90FF', '#FFB6C1', '#ADD8E6', '#FF4500']  # Pastel for Off-Peak, Dope for Peak

# Iterate over the columns to plot each time_status separately
for i, (time_status, data) in enumerate(pivot_table.items()):
    ax8.bar(
        positions + i * bar_width,  # Adjust bar positions for each time_status
        data.values,               # Heights of the bars
        bar_width,                 # Width of each bar
        label=time_status,         # Label for the legend
        color=colors[i]            # Assign colors
    )

# Customize the chart
ax8.set_xticks(positions + (len(pivot_table.columns) - 1) * bar_width / 2)
ax8.set_xticklabels(pivot_table.index, fontsize=10)
ax8.set_title("Clustered Bar Chart of Rentals by Time Status", fontsize=14)
ax8.set_xlabel("Rental Category", fontsize=12)
ax8.set_ylabel("Count of Rentals", fontsize=12)
ax8.legend(title="Time Status", fontsize=10)
ax8.grid(axis='y', linestyle='--', alpha=0.5)

# Tight layout to avoid overlap
plt.tight_layout()

# Show the plot in Streamlit
st.pyplot(fig8)
