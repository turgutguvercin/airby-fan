import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import os

# Set page configuration
st.set_page_config(
    page_title="TRİO Fan Seçimi 🕊️",
    page_icon="🕊️",
    layout="wide"
)

# --- Data and Image File Definitions ---
csv_files = {
    "TRİO B190-063": ["TRİO B190-063-1.csv", "TRİO B190-063-2.csv"],
    "TRİO B225-089": ["TRİO B225-089.csv"],
    "TRİO B250-080": ["TRİO B250-080.csv"],
    "TRİO B280-081": ["TRİO B280-081.csv"],
    "TRİO B355-145": ["TRİO B355-145.csv"],
    "TRİO B355-164": ["TRİO B355-164-1.csv", "TRİO B355-164-2.csv"],
    "TRİO B400-147": [
        "TRİO B400-147-1.csv",
        "TRİO B400-147-2.csv",
        "TRİO B400-147-3.csv",
        "TRİO B400-147-4.csv"
    ],
    "TRİO B400-185": ["TRİO B400-185.csv"],
    "TRİO B400-188": ["TRİO B400-188.csv"],
    "TRİO B450-209-3F": ["TRİO B450-209-3F.csv"],
    "TRİO B450-218-1F": ["TRİO B450-218-1F.csv"],
    "TRİO B500-234-3F": ["TRİO B500-234-3F.csv"],
    "TRİO B560-243-3F": ["TRİO B560-243-3F-1.csv", "TRİO B560-243-3F-2.csv"],
}

image_files_left = {
    "TRİO B190-063": "images/trio_b190_063_left.png",
    "TRİO B225-089": "images/trio_b225_089_left.png",
    "TRİO B250-080": "images/trio_b250_080_left.png",
    "TRİO B280-081": "images/trio_b280_081_left.png",
    "TRİO B355-145": "images/trio_b355_145_left.png",
    "TRİO B355-164": "images/trio_b355_164_left.png",
    "TRİO B400-147": "images/trio_b400_147_left.png",
    "TRİO B400-185": "images/trio_b400_185_left.png",
    "TRİO B400-188": "images/trio_b400_188_left.png",
    "TRİO B450-209-3F": "images/trio_b450_209_3f_left.png",
    "TRİO B450-218-1F": "images/trio_b450_218_1f_left.png",
    "TRİO B500-234-3F": "images/trio_b500_234_3f_left.png",
    "TRİO B560-243-3F": "images/trio_b560_243_3f_left.png",
}

image_files_bottom = {
    "TRİO B190-063": "images/trio_b190_063_bottom.png",
    "TRİO B225-089": "images/trio_b225_089_bottom.png",
    "TRİO B250-080": "images/trio_b250_080_bottom.png",
    "TRİO B280-081": "images/trio_b280_081_bottom.png",
    "TRİO B355-145": "images/trio_b355_145_bottom.png",
    "TRİO B355-164": "images/trio_b355_164_bottom.png",
    "TRİO B400-147": "images/trio_b400_147_bottom.png",
    "TRİO B400-185": "images/trio_b400_185_bottom.png",
    "TRİO B400-188": "images/trio_b400_188_bottom.png",
    "TRİO B450-209-3F": "images/trio_b450_209_3f_bottom.png",
    "TRİO B450-218-1F": "images/trio_b450_218_1f_bottom.png",
    "TRİO B500-234-3F": "images/trio_b500_234_3f_bottom.png",
    "TRİO B560-243-3F": "images/trio_b560_243_3f_bottom.png",
}

# --- Initialize Session State Keys ---
if "selected_fan" not in st.session_state:
    st.session_state.selected_fan = None
if "nav_page" not in st.session_state:
    st.session_state.nav_page = "Ürün Ara"  # default page
if "results" not in st.session_state:
    st.session_state.results = None

# --- Navigation Callback using st.rerun() ---
def go_to_product_page(fan_name):
    st.session_state.selected_fan = fan_name
    st.session_state.nav_page = "Fan Seçimi"
    st.session_state.results = None  # Clear stored results
    st.rerun()  # Use st.rerun to force a re-run

# --- Sidebar Navigation ---
# Always show the main navigation selectbox.
nav_choice = st.sidebar.selectbox(
    "📂 Sayfa Seçimi",
    ["Fan Seçimi", "Ürün Ara"],
    index=0 if st.session_state.nav_page == "Fan Seçimi" else 1
)
st.session_state.nav_page = nav_choice

# If on Fan Seçimi, show the fan model selectbox.
if st.session_state.nav_page == "Fan Seçimi":
    all_fans = list(csv_files.keys())
    if st.session_state.selected_fan is None:
        st.session_state.selected_fan = all_fans[0]
    default_index = all_fans.index(st.session_state.selected_fan)
    selected_file = st.sidebar.selectbox("📂 Lütfen bir fan modeli seçin:", all_fans, index=default_index)
    st.session_state.selected_fan = selected_file
    st.sidebar.success(f"✅ Seçili Fan: {selected_file}")

# --- Custom Styling ---
st.markdown("""
    <style>
        .block-container {
            max-width: 1200px !important;
            margin: auto !important;
        }
        .stPlotlyChart {
            width: 100% !important;
        }
        .dataframe {
            font-size: 16px !important;
            border: 1px solid #d4d4d4;
            border-radius: 4px;
            overflow: hidden;
        }
    </style>
""", unsafe_allow_html=True)

# --- Page Rendering ---
if st.session_state.nav_page == "Fan Seçimi":
    st.markdown('<h1 style="text-align:center; color:#2E86C1;">Fan Seçimi</h1>', unsafe_allow_html=True)
    
    selected_file = st.session_state.selected_fan

    col1, col2 = st.columns([1, 1.5], gap="large")
    fig = px.line(title=f"📊 {selected_file} - Interpolated Fan Curve")
    for file in csv_files[selected_file]:
        if os.path.exists(file):
            df = pd.read_csv(file, header=None, names=["Flow (m³/h)", "Pressure (Pa)"])
            if not df.empty:
                df = df.sort_values("Flow (m³/h)")
                x_data = df["Flow (m³/h)"].values
                y_data = df["Pressure (Pa)"].values
                x_dense = np.linspace(x_data[0], x_data[-1], 200)
                y_dense = np.interp(x_dense, x_data, y_data)
                fig.add_scatter(x=x_dense, y=y_dense, mode="lines", name=file.replace(".csv", ""))
        else:
            st.warning(f"⚠️ Dosya bulunamadı: {file}")
    fig.update_layout(
        autosize=False,
        height=500,
        width=900,
        xaxis=dict(title="Flow (m³/h)"),
        yaxis=dict(title="Pressure (Pa)")
    )
    with col2:
        st.plotly_chart(fig, use_container_width=True)
    with col1:
        img_path = image_files_left.get(selected_file, "")
        if os.path.exists(img_path):
            st.image(img_path, caption=f"📷 {selected_file} - Sol Görsel", use_container_width=True)
        else:
            st.warning(f"⚠️ Sol taraftaki resim bulunamadı: {img_path}")
    img_path = image_files_bottom.get(selected_file, "")
    if os.path.exists(img_path):
        st.image(img_path, caption=f"📷 {selected_file} - Alt Görsel", use_container_width=True)
    else:
        st.warning(f"⚠️ Alt taraftaki resim bulunamadı: {img_path}")

elif st.session_state.nav_page == "Ürün Ara":
    st.markdown('<h1 style="text-align:center; color:#2E86C1;">Ürün Ara</h1>', unsafe_allow_html=True)
    flow_input = st.number_input("Flow (m³/h) değeri:", min_value=0.0, step=50.0, value=500.0)
    pressure_input = st.number_input("Pressure (Pa) değeri:", min_value=0.0, step=10.0, value=100.0)
    if st.button("Uygun Ürünleri Bul"):
        results = []
        fig = px.line(title="🔍 Uygun Ürünler Grafiği")
        flow_margin = flow_input * 0.2
        pressure_margin = pressure_input * 0.3
        flow_min_allowed, flow_max_allowed = flow_input - flow_margin, flow_input + flow_margin
        pressure_min_allowed, pressure_max_allowed = pressure_input - pressure_margin, pressure_input + pressure_margin
        for fan, files in csv_files.items():
            for file in files:
                if os.path.exists(file):
                    df = pd.read_csv(file, header=None, names=["Flow (m³/h)", "Pressure (Pa)"])
                    df = df.sort_values("Flow (m³/h)")
                    x_data = df["Flow (m³/h)"].values
                    y_data = df["Pressure (Pa)"].values
                    x_dense = np.linspace(x_data[0], x_data[-1], 200)
                    y_dense = np.interp(x_dense, x_data, y_data)
                    intersects = np.any(
                        (x_dense >= flow_min_allowed) & (x_dense <= flow_max_allowed) &
                        (y_dense >= pressure_min_allowed) & (y_dense <= pressure_max_allowed)
                    )
                    if intersects:
                        results.append({
                            "Fan Modeli": fan,
                            "Dosya": file,
                            "Min Flow": round(x_data.min(), 2),
                            "Max Flow": round(x_data.max(), 2),
                            "Min Pressure": round(y_data.min(), 2),
                            "Max Pressure": round(y_data.max(), 2)
                        })
                        fig.add_scatter(x=np.round(x_dense, 2), y=np.round(y_dense, 2), mode="lines", name=file.replace(".csv", ""), showlegend=True,hoverlabel_namelength=-1)
        fig.add_scatter(
            x=[flow_input], y=[pressure_input], mode="markers+text",
            marker=dict(size=10, color="red", symbol="x"),
            name="Seçilen Nokta"
        )
        fig.add_shape(
            type="rect",
            x0=flow_min_allowed, x1=flow_max_allowed,
            y0=pressure_min_allowed, y1=pressure_max_allowed,
            line=dict(color="blue", width=2, dash="dot"),
            fillcolor="rgba(0,0,255,0.03)"
        )
        st.plotly_chart(fig, use_container_width=True)
        st.session_state.results = results

    if st.session_state.results:
        st.success("🔍 **Bu ürünlerin eğrileri, belirtilen aralığa giriyor:**")
        for i, row in pd.DataFrame(st.session_state.results).iterrows():
            cols = st.columns([3, 1])
            cols[0].write(
                f"**{row['Fan Modeli']}** | Min Flow: {row['Min Flow']} | "
                f"Max Flow: {row['Max Flow']} | Min Pressure: {row['Min Pressure']} | "
                f"Max Pressure: {row['Max Pressure']}"
            )
            if cols[1].button("Seç", key=f"select_{row['Fan Modeli']}_{i}"):
                go_to_product_page(row["Fan Modeli"])
