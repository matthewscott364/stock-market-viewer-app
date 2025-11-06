import streamlit as st
import pandas as pd
import plotly.express as px

#Page configuration
st.set_page_config(page_title='Stock Market Data Viewer', layout='wide', initial_sidebar_state='expanded')

#Load dataset
df = pd.read_csv('random_stock_market_dataset.csv')
st.title('Stock Market Data Viewer')
st.write('This application allows you to view and filter stock market data.')

#Dropdown menu for column selection
available_columns = [col for col in df.columns if col != 'Date']
selected_column = st.selectbox("Select metric to filter by:", available_columns, format_func=lambda x: x.replace('_', ' ').title())

# Slider for filtering by volume with expander
with st.expander(f"Filter by {selected_column.replace('_', ' ').title()}"):
    min_value = int(df[selected_column].min())
    max_value = int(df[selected_column].max())
    selected_range = st.slider(f"Select range for {selected_column.replace('_', ' ').title()}:", min_value, max_value, (min_value, max_value))

    # Filter dataframe based on slider selection
    filtered_df = df[(df[selected_column] >= selected_range[0]) & (df[selected_column] <= selected_range[1])]

    st.write(f"Displaying records where {selected_column.replace('_', ' ').title()} is between {selected_range[0]} and {selected_range[1]}:")
    st.dataframe(filtered_df)

# Create two columns for layout
col_left, col_right = st.columns(2)

# Bar chart for visualizing selected metric aligned to the left
with col_left:
    st.subheader(f"{selected_column.replace('_', ' ').title() if selected_column else 'All Metrics'} Bar Chart")
    if selected_column:
        st.bar_chart(filtered_df.set_index('Date')[selected_column])
    else:
        st.bar_chart(df.set_index('Date'))

# Area chart for visualizing distribution of selected metric aligned to the right
with col_right:
    st.subheader(f"{selected_column.replace('_', ' ').title() if selected_column else 'All Metrics'} Area Chart")
    if selected_column:
        fig_area = px.area(filtered_df, x='Date', y=selected_column, title=f'{selected_column.replace("_", " ").title()} Over Time')
        st.plotly_chart(fig_area, use_container_width=True)
    else:
        fig_area = px.area(df, x='Date', y=available_columns, title='All Metrics Over Time')
        st.plotly_chart(fig_area, use_container_width=True)

# Line chart for visualizing selected metric over time
st.subheader(f"{selected_column.replace('_', ' ').title() if selected_column else 'All Metrics'} Line Chart Over Time")

if selected_column:
    st.line_chart(filtered_df.set_index('Date')[selected_column])
else:
    st.line_chart(df.set_index('Date'))

# Display summary statistics
st.subheader('Summary Statistics')
if selected_column:
    st.write(df[selected_column].describe())
else:
    st.write(df.describe())

