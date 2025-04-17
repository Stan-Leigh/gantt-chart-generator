import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

st.set_page_config(page_title="Interactive Gantt Chart", layout="wide")
st.title("📊 Interactive Gantt Chart Generator")

st.markdown("""
Use the table below to edit tasks, start dates, and end dates.
Click the checkbox to preview the chart.
""")

# About
expander_bar = st.expander("Read more")
expander_bar.markdown("""
1. To add a new row, hover over the table and click on the '+' on the top right of the table.
2. To delete a row, hover to the leftmost column of the table (the blank column before the 'Task' column). Click on the check box to highlight the whole row then click on the bin sign on the top right of the table.                    
3. To edit any field, double-click on the field to be edited and change it.
4. Click on the check box beside 'Generate Gantt Chart' to display your Gantt chart.
                      Enjoy!
""")

st.header("Gantt Chart data")

# Sample default data
def get_default_data():
    return pd.DataFrame({
        "Task": [
            "Project Proposal & Approval",
            "Literature Review & Related Works",
            "Definition of Objectives, Scope & Methodology"
        ],
        "Start": [
            "2024-01-07", "2024-01-20", "2024-02-11"
        ],
        "End": [
            "2024-02-11", "2024-06-27", "2024-03-20"
        ]
    })

# Editable table
data = st.data_editor(
    get_default_data(),
    column_config={
        "Start": st.column_config.TextColumn("Start Date"),
        "End": st.column_config.TextColumn("End Date")
    },
    use_container_width=True,
    num_rows="dynamic"
)

st.header("Plot specifications")

bar_color = st.selectbox('What color should the bars be?', ('grey', 'blue', 'red', 'black', 'orange'))
figure_size = st.selectbox('Select a figure size', ((14, 8), (12, 8), (14, 10), (12, 10), (10, 8)))
font_name = st.selectbox('Select a font', ('Gill Sans MT', 'Arial', 'Cambria', 'Times New Roman', 'Tahoma', "Helvetica"))
font_size_labels = st.selectbox('Select a font size for the x and y labels', (10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20))
font_size_ticks = st.selectbox('Select a font size for the x and y ticks', (10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20), )
x_label = st.text_input("What should be the label for the x-axis? Edit the field below", "MONTHS")
y_label = st.text_input("What should be the label for the y-axis? Edit the field below", "TASKS")

st.markdown("*To save the image, Right-click on the image and select 'Save image as...'*")

# Plot if checkbox is ticked
if st.checkbox("Generate Gantt Chart"):
    df = data.copy()
    df["Start"] = pd.to_datetime(df["Start"])
    df["End"] = pd.to_datetime(df["End"])

    fig, ax = plt.subplots(figsize=figure_size)
    for _, row in df.iterrows():
        ax.barh(row["Task"], row["End"] - row["Start"], left=row["Start"], height=0.8, color=bar_color)

    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))

    plt.xlabel(x_label, fontsize=font_size_labels, fontname=font_name)
    plt.xticks(fontsize=font_size_ticks, fontname=font_name)
    plt.ylabel(y_label, fontsize=font_size_labels, fontname=font_name)
    plt.yticks(fontsize=font_size_ticks, fontname=font_name)
    plt.grid(axis='x', linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.gca().invert_yaxis()

    st.pyplot(fig)
