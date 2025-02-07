import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import os

# Set page configuration
st.set_page_config(
    page_title="TRİO Fan Seçimi🕊️🕊️🕊️🕊️🕊️",  # Title that appears in the browser tab
    page_icon="🕊️",  # Emoji as the tab logo (favicon)
    layout="wide"
)

# **Custom CSS for Layout Styling**
st.markdown("""
    <style>
        .block-container {
            max-width: 1200px !important;
            margin: auto !important;
        }
        .stPlotlyChart {
            width: 100% !important;
        }
    </style>
""", unsafe_allow_html=True)

# Load FontAwesome for Icons
st.markdown("""
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
        .title { text-align:center; font-size:32px; color: #2E86C1; font-weight:bold; }
        .sidebar-title { font-size:24px; font-weight:bold; color: #34495E; }
    </style>
""", unsafe_allow_html=True)

# **Streamlit App Title**
st.markdown('<h1 class="title"><i class="fa-solid fa-fan"></i> TRİO Fan Seçimi</h1>', unsafe_allow_html=True)

# **Sidebar - Fan Model Selection**
st.sidebar.markdown('<p class="sidebar-title"><i class="fa-solid fa-wind"></i> Fan Seçimi</p>', unsafe_allow_html=True)

# Define available CSV files (including the grouped TRİO B190-063)
csv_files = {
    "TRİO B190-063": ["TRİO B190-063-1.csv", "TRİO B190-063-2.csv"],
    "TRİO B225-089": ["TRİO B225-089.csv"],
    "TRİO B250-080": ["TRİO B250-080.csv"],
    "TRİO B280-081": ["TRİO B280-081.csv"],
    "TRİO B355-145": ["TRİO B355-145.csv"],
    "TRİO B355-164": ["TRİO B355-164-1.csv", "TRİO B355-164-2.csv"],
    
    # Grouped as a single selection
}

# Define image files for visualization
image_files_left = {
    "TRİO B190-063": "images/trio_b190_063_left.png",
    "TRİO B225-089": "images/trio_b225_089_left.png",
    "TRİO B250-080": "images/trio_b250_080_left.png",
    "TRİO B280-081": "images/trio_b280_081_left.png",
    "TRİO B355-145": "images/trio_b355_145_left.png",
    "TRİO B355-164": "images/trio_b355_164_left.png",
}

image_files_bottom = {
    "TRİO B190-063": "images/trio_b190_063_bottom.png",
    "TRİO B225-089": "images/trio_b225_089_bottom.png",
    "TRİO B250-080": "images/trio_b250_080_bottom.png",
    "TRİO B280-081": "images/trio_b280_081_bottom.png",
    "TRİO B355-145": "images/trio_b355_145_bottom.png",
    "TRİO B355-164": "images/trio_b355_164_bottom.png",
}

# **Dropdown for Fan Selection (Single Selection)**
selected_file = st.sidebar.selectbox(
    "📂 Lütfen bir fan modeli seçin:", 
    list(csv_files.keys()), 
    index=0
)

# Sidebar success message
st.sidebar.success(f"✅ Seçili Fan: {selected_file}")

# **Create Layout: Left Column (Image) | Right Column (Graph)**
col1, col2 = st.columns([1, 1.5], gap="large")  # Adjust width ratio

# **Initialize Plotly Figure**
fig = px.line(title=f"📊 {selected_file} - Interpolated Fan Curve")

# **Load Data and Plot**
for file in csv_files[selected_file]:  # If it's "TRİO B190-063", both files will be loaded automatically
    df = pd.read_csv(file, header=None, names=["Flow (m³/h)", "Pressure (Pa)"])
    df = df.sort_values("Flow (m³/h)")

    # **Interpolation**
    x_data = df["Flow (m³/h)"].values
    y_data = df["Pressure (Pa)"].values
    x_dense = np.linspace(x_data[0], x_data[-1], 200)
    y_dense = np.interp(x_dense, x_data, y_data)

    # **Add to Plot**
    fig.add_scatter(x=x_dense, y=y_dense, mode="lines", name=file.replace(".csv", ""),showlegend=True)

# **Fix Axis Scaling to Prevent Resizing Issues**
fig.update_layout(
    autosize=False,
    height=500,
    width=900,
    xaxis=dict(title="Flow (m³/h)"),
    yaxis=dict(title="Pressure (Pa)")
)

# **Interpolation User Input**
st.sidebar.markdown("🔢 **Flow değerini hesapla**")
x_input = st.sidebar.number_input(
    "Flow (m³/h) değerini girin:",
    min_value=float(df["Flow (m³/h)"].min()),
    max_value=float(df["Flow (m³/h)"].max()),
    value=float(df["Flow (m³/h)"].mean())
)

if st.sidebar.button("🔎 Hesapla"):
    for file in csv_files[selected_file]:  # Apply interpolation to all linked CSVs
        df = pd.read_csv(file, header=None, names=["Flow (m³/h)", "Pressure (Pa)"])
        df = df.sort_values("Flow (m³/h)")

        x_data = df["Flow (m³/h)"].values
        y_data = df["Pressure (Pa)"].values
        y_interp = np.interp(x_input, x_data, y_data)

        # **Update the Plot with Interpolation Point**
        fig.add_scatter(
            x=[x_input], y=[y_interp],
            mode="markers+text",
            text=[f"({x_input:.2f}, {y_interp:.2f})"],
            textposition="top center",
            marker=dict(size=10),
            name=f"Interpolated {file.replace('.csv', '')}",
            showlegend=False
        )

        # **Add Vertical and Horizontal Dashed Lines**
        fig.add_vline(x=x_input, line_width=1.5, line_dash="dash", line_color="blue")
        fig.add_hline(y=y_interp, line_width=1.5, line_dash="dot", line_color="gray")

    # **Show Interpolation Result in Sidebar**
    st.sidebar.success(f"🎯 Interpolated Pressure (Pa): **{y_interp:.2f}**")

# **Render the Updated Plot**
with col2:
    st.plotly_chart(fig, use_container_width=True)

# **Left Image Display**
# Display Left-Side Image
with col1:
    if selected_file in image_files_left:
        img_path = image_files_left[selected_file]  # Ensure it's a single string
        if isinstance(img_path, str) and os.path.exists(img_path):
            st.image(img_path, caption=f"📷 {selected_file} - Sol Görsel", use_container_width=True)
        else:
            st.warning(f"⚠️ Sol taraftaki resim bulunamadı: {img_path}")

# Display Bottom Image
if selected_file in image_files_bottom:
    img_path = image_files_bottom[selected_file]  # Ensure it's a single string
    if isinstance(img_path, str) and os.path.exists(img_path):
        st.image(img_path, caption=f"📷 {selected_file} - Alt Görsel", use_container_width=True)
    else:
        st.warning(f"⚠️ Alt taraftaki resim bulunamadı: {img_path}")
