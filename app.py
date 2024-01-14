import streamlit as st
import pandas as pd

# Load CSV data
data = pd.read_csv('result.csv')

# Sidebar with filters
st.sidebar.title("Filter Options")

# Add filter for title
filter_title = st.sidebar.selectbox("Select Title", data['motion'].unique())

# Display filtered data
filtered_data = data.loc[data['motion'] == filter_title]

# Remove 'file_path' column
filtered_data = filtered_data.drop(columns=['file_path'])

# Define the desired order and names of columns
column_mapping = {
    'gov_scr': 'Gov Side Score',
    'opp_scr': 'Opp Side Score',
    'pm_comments': 'PM comments',
    'lo_comments': 'LO comments',
    'mc_comments': 'MC comments',
    'mo_comments': 'MO comments'
    # Add more columns as needed  
}

# Rename columns
filtered_data = filtered_data.rename(columns=column_mapping)

# Define the desired order of columns (excluding 'motion' and 'debate')
custom_column_order = ['Gov Side Score', 'PM comments', 'MC comments', 'Opp Side Score',  'LO comments',  'MO comments']  # Replace with your desired column names

# Reorder columns
filtered_data = filtered_data[['motion', 'debate'] + custom_column_order]

# Display the title
st.title("Analysis")

# Display 'motion' and 'debate' columns at the top
motion_col_index = 0
debate_col_index = 1

# Display 'motion' horizontally
st.subheader("Motion")
st.write(filtered_data.iloc[0, motion_col_index])

# Display 'debate' horizontally
st.subheader("Debate")
st.write(filtered_data.iloc[0, debate_col_index])

# Display other columns' values in aligned round boxes
num_columns = len(filtered_data.columns)
num_boxes_per_row = 3  # You can adjust this based on your preference

# Exclude 'motion' and 'debate' columns from the list
other_columns = filtered_data.columns[2:]  # Start from the 3rd column, as the first two are 'motion' and 'debate'

# Calculate the number of rows required
num_rows = (len(other_columns) + num_boxes_per_row - 1) // num_boxes_per_row

# Create layout using st.columns()
box_layout = st.columns(num_boxes_per_row)

for i in range(num_rows):
    with box_layout[i % num_boxes_per_row]:
        for j in range(num_boxes_per_row):
            col_index = i * num_boxes_per_row + j
            if col_index < len(other_columns):
                st.subheader(other_columns[col_index])

                # Generate HTML for round box
                style = f"border-radius: 10px; padding: 10px; background-color: #f0f0f0;"
                st.markdown(f'<div style="{style}">{", ".join(map(str, filtered_data[other_columns[col_index]].tolist()))}</div>', unsafe_allow_html=True)