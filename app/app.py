# ===============================================================
# Ultra Premium Streamlit App - Zomato Restaurant Analysis
# Author: Aishwarya Patil (Enhanced Design)
# ===============================================================

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import plotly.express as px
import plotly.graph_objects as go

# ---------------------------------------------------------------
# 1️⃣ Page configuration
# ---------------------------------------------------------------
st.set_page_config(
    page_title="Zomato Restaurant Analysis",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Ultra Premium CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700;800&display=swap');
    
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    /* Remove default padding */
    .block-container {
        padding-top: 3rem !important;
        padding-bottom: 3rem !important;
        max-width: 95% !important;
    }
    
    /* Hide hamburger and footer */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Main app background */
    .stApp {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 50%, #7e22ce 100%);
    }
    
    /* Title Section */
    h1 {
        font-size: 4rem !important;
        font-weight: 800 !important;
        text-align: center;
        background: linear-gradient(135deg, #ffd700 0%, #ffed4e 50%, #fff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 0 40px rgba(255, 215, 0, 0.3);
        margin-bottom: 0.5rem !important;
        letter-spacing: -1px;
    }
    
    /* Subtitle */
    .subtitle {
        text-align: center;
        color: rgba(255, 255, 255, 0.9);
        font-size: 1.4rem;
        font-weight: 300;
        margin-bottom: 3rem;
        letter-spacing: 0.5px;
    }
    
    /* Metric Cards - Ultra Modern */
    div[data-testid="metric-container"] {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 20px;
        padding: 2rem 1.5rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    div[data-testid="metric-container"]:hover {
        transform: translateY(-8px);
        box-shadow: 0 16px 48px rgba(255, 215, 0, 0.3);
        border-color: rgba(255, 215, 0, 0.5);
    }
    
    div[data-testid="metric-container"] label {
        color: rgba(255, 255, 255, 0.8) !important;
        font-size: 0.95rem !important;
        font-weight: 500 !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    div[data-testid="metric-container"] [data-testid="stMetricValue"] {
        color: #ffd700 !important;
        font-size: 2.5rem !important;
        font-weight: 800 !important;
    }
    
    /* Sidebar - Glassmorphism */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(30, 60, 114, 0.95) 0%, rgba(126, 34, 206, 0.95) 100%);
        backdrop-filter: blur(20px);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    section[data-testid="stSidebar"] > div {
        padding: 2.5rem 1.5rem;
    }
    
    section[data-testid="stSidebar"] h2 {
        color: #ffd700 !important;
        font-weight: 700 !important;
        font-size: 1.8rem !important;
        margin-bottom: 2rem !important;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    
    section[data-testid="stSidebar"] label {
        color: rgba(255, 255, 255, 0.95) !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
    }
    
    section[data-testid="stSidebar"] .stSelectbox,
    section[data-testid="stSidebar"] .stSlider {
        margin-bottom: 2rem;
    }
    
    /* Subheaders */
    h2, h3 {
        color: white !important;
        font-weight: 700 !important;
        font-size: 2rem !important;
        margin-top: 3rem !important;
        margin-bottom: 1.5rem !important;
        text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
    }
    
    /* Chart containers */
    .js-plotly-plot, .plotly {
        border-radius: 20px !important;
        overflow: hidden;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3) !important;
    }
    
    /* Plotly charts background */
    .plotly .bg {
        fill: rgba(255, 255, 255, 0.05) !important;
    }
    
    /* Insight Cards */
    .insight-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        padding: 1.8rem;
        border-radius: 20px;
        margin: 1rem 0;
        color: white;
        font-size: 1.05rem;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
    }
    
    .insight-card:hover {
        transform: translateY(-5px) scale(1.02);
        box-shadow: 0 16px 48px rgba(255, 215, 0, 0.3);
        border-color: rgba(255, 215, 0, 0.5);
    }
    
    /* Info box in sidebar */
    .stAlert {
        background: rgba(255, 215, 0, 0.15) !important;
        border: 1px solid rgba(255, 215, 0, 0.3) !important;
        border-radius: 15px !important;
        color: white !important;
    }
    
    /* Divider */
    hr {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
        margin: 3rem 0;
    }
    
    /* Input widgets */
    .stSelectbox > div > div,
    .stSlider > div > div {
        background: rgba(255, 255, 255, 0.1) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 12px !important;
        color: white !important;
    }
    
    /* Slider */
    .stSlider > div > div > div > div {
        background: #ffd700 !important;
    }
    
    /* Remove extra spacing */
    .element-container {
        margin-bottom: 0 !important;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------
# 2️⃣ Load Dataset
# ---------------------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("../data/zomato.csv", encoding='latin-1')
    df.rename(columns={
        'Aggregate rating': 'rate',
        'Average Cost for two': 'cost_for_two',
        'Cuisines': 'cuisines',
        'City': 'city'
    }, inplace=True)
    df.drop_duplicates(inplace=True)
    drop_cols = ['url', 'address', 'phone', 'dish_liked', 'reviews_list', 'menu_item']
    df = df.drop([col for col in drop_cols if col in df.columns], axis=1, errors='ignore')
    df = df.dropna(subset=['rate', 'cost_for_two', 'cuisines'])
    df['rate'] = df['rate'].apply(lambda x: str(x).split('/')[0])
    df['rate'] = pd.to_numeric(df['rate'], errors='coerce')
    df['cost_for_two'] = df['cost_for_two'].astype(str).str.replace(',', '').astype(float)
    return df

df = load_data()

# ---------------------------------------------------------------
# 3️⃣ Sidebar
# ---------------------------------------------------------------
st.sidebar.header("🎛️ Dashboard Controls")
st.sidebar.markdown("---")

cities = df['city'].unique()
selected_city = st.sidebar.selectbox("🏙️ Select City", options=np.append("All", cities))

min_cost = int(df['cost_for_two'].min())
max_cost = int(df['cost_for_two'].max())
cost_range = st.sidebar.slider("💰 Cost for Two Range", min_value=min_cost, max_value=max_cost,
                               value=(min_cost, max_cost))

st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 About")
st.sidebar.info("Comprehensive insights into restaurant trends, ratings, and cuisines across major Indian cities.")

# ---------------------------------------------------------------
# 4️⃣ Header
# ---------------------------------------------------------------
st.title("🍽️ ZOMATO RESTAURANT ANALYSIS")
st.markdown('<p class="subtitle">Discover culinary insights across India\'s vibrant food landscape</p>', 
            unsafe_allow_html=True)

# ---------------------------------------------------------------
# 5️⃣ Filter Data
# ---------------------------------------------------------------
filtered_df = df.copy()

if selected_city != "All":
    filtered_df = filtered_df[filtered_df['city'] == selected_city]

filtered_df = filtered_df[(filtered_df['cost_for_two'] >= cost_range[0]) & 
                          (filtered_df['cost_for_two'] <= cost_range[1])]

# ---------------------------------------------------------------
# 6️⃣ Metrics
# ---------------------------------------------------------------
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("🏪 Total Restaurants", f"{filtered_df.shape[0]:,}")

with col2:
    st.metric("⭐ Avg Rating", f"{filtered_df['rate'].mean():.2f}")

with col3:
    st.metric("💵 Avg Cost", f"₹{filtered_df['cost_for_two'].mean():.0f}")

with col4:
    st.metric("🍜 Unique Cuisines", f"{filtered_df['cuisines'].nunique():,}")

st.markdown("---")

# ---------------------------------------------------------------
# 7️⃣ Visualizations
# ---------------------------------------------------------------

col1, col2 = st.columns(2)

with col1:
    st.subheader("🍴 Top 10 Cuisines")
    top_cuisines = filtered_df['cuisines'].value_counts().head(10)
    
    fig = go.Figure(go.Bar(
        y=top_cuisines.index,
        x=top_cuisines.values,
        orientation='h',
        marker=dict(
            color=top_cuisines.values,
            colorscale=[[0, '#7e22ce'], [0.5, '#ffd700'], [1, '#ff6b6b']],
            line=dict(color='rgba(255, 255, 255, 0.3)', width=1)
        ),
        text=top_cuisines.values,
        textposition='outside',
        textfont=dict(color='white', size=12, family='Poppins')
    ))
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(255, 255, 255, 0.05)',
        font=dict(size=12, color='white', family='Poppins'),
        height=450,
        margin=dict(l=20, r=40, t=10, b=10),
        xaxis=dict(
            showgrid=True,
            gridcolor='rgba(255, 255, 255, 0.1)',
            title="",
            color='white'
        ),
        yaxis=dict(
            showgrid=False,
            title="",
            color='white'
        ),
        showlegend=False
    )
    
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("🏙️ Top 10 Cities")
    city_counts = df['city'].value_counts().head(10)
    
    fig = go.Figure(go.Bar(
        y=city_counts.index,
        x=city_counts.values,
        orientation='h',
        marker=dict(
            color=city_counts.values,
            colorscale=[[0, '#1e3c72'], [0.5, '#00d4ff'], [1, '#7e22ce']],
            line=dict(color='rgba(255, 255, 255, 0.3)', width=1)
        ),
        text=city_counts.values,
        textposition='outside',
        textfont=dict(color='white', size=12, family='Poppins')
    ))
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(255, 255, 255, 0.05)',
        font=dict(size=12, color='white', family='Poppins'),
        height=450,
        margin=dict(l=20, r=40, t=10, b=10),
        xaxis=dict(
            showgrid=True,
            gridcolor='rgba(255, 255, 255, 0.1)',
            title="",
            color='white'
        ),
        yaxis=dict(
            showgrid=False,
            title="",
            color='white'
        ),
        showlegend=False
    )
    
    st.plotly_chart(fig, use_container_width=True)

# Average Rating
st.subheader("⭐ Average Rating by City")
avg_rating = df.groupby('city')['rate'].mean().sort_values(ascending=False).head(10)

fig = go.Figure(go.Bar(
    y=avg_rating.index,
    x=avg_rating.values,
    orientation='h',
    marker=dict(
        color=avg_rating.values,
        colorscale=[[0, '#ff6b6b'], [0.5, '#ffd700'], [1, '#4ade80']],
        line=dict(color='rgba(255, 255, 255, 0.3)', width=1)
    ),
    text=[f"{val:.2f}" for val in avg_rating.values],
    textposition='outside',
    textfont=dict(color='white', size=12, family='Poppins')
))

fig.update_layout(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(255, 255, 255, 0.05)',
    font=dict(size=12, color='white', family='Poppins'),
    height=450,
    margin=dict(l=20, r=60, t=10, b=10),
    xaxis=dict(
        showgrid=True,
        gridcolor='rgba(255, 255, 255, 0.1)',
        title="",
        color='white',
        range=[0, 5]
    ),
    yaxis=dict(
        showgrid=False,
        title="",
        color='white'
    ),
    showlegend=False
)

st.plotly_chart(fig, use_container_width=True)

# Scatter Plot
st.subheader("💰 Cost vs Rating Analysis")
fig = px.scatter(
    filtered_df, 
    x='cost_for_two', 
    y='rate',
    color='city' if selected_city == "All" else None,
    size='rate',
    hover_data=['cuisines'],
    labels={'cost_for_two': 'Cost for Two (₹)', 'rate': 'Rating'},
    color_discrete_sequence=['#ffd700', '#7e22ce', '#ff6b6b', '#4ade80', '#00d4ff', '#ff8c00']
)

fig.update_layout(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(255, 255, 255, 0.05)',
    font=dict(size=12, color='white', family='Poppins'),
    height=500,
    xaxis=dict(
        showgrid=True,
        gridcolor='rgba(255, 255, 255, 0.1)',
        color='white'
    ),
    yaxis=dict(
        showgrid=True,
        gridcolor='rgba(255, 255, 255, 0.1)',
        color='white'
    ),
    legend=dict(
        bgcolor='rgba(0,0,0,0.3)',
        bordercolor='rgba(255, 255, 255, 0.2)',
        font=dict(color='white')
    )
)

st.plotly_chart(fig, use_container_width=True)

# WordCloud
st.subheader("☁️ Cuisine Popularity Cloud")
text = " ".join(str(cuisine) for cuisine in filtered_df['cuisines'])
wc = WordCloud(
    width=1400, 
    height=600, 
    background_color=None,
    mode='RGBA',
    colormap='plasma',
    relative_scaling=0.5,
    min_font_size=12
).generate(text)

fig, ax = plt.subplots(figsize=(16, 7))
fig.patch.set_alpha(0)
ax.patch.set_alpha(0)
ax.imshow(wc, interpolation='bilinear')
ax.axis("off")
plt.tight_layout(pad=0)
st.pyplot(fig, transparent=True)

# ---------------------------------------------------------------
# 8️⃣ Insights
# ---------------------------------------------------------------
st.markdown("---")
st.subheader("📌 Key Insights")

insights = [
    "🏙️ **Metro Dominance**: Delhi NCR and Bangalore lead with the highest restaurant density",
    "🍜 **Cuisine Trends**: North Indian and Chinese cuisines dominate the food landscape",
    "💰 **Price-Quality Paradox**: Higher costs don't guarantee better ratings",
    "🍽️ **Dining Preferences**: Casual Dining and Quick Bites are consumer favorites",
    "⭐ **Quality Leaders**: Pune and Hyderabad maintain consistently high ratings"
]

cols = st.columns(2)
for idx, insight in enumerate(insights):
    with cols[idx % 2]:
        st.markdown(f'<div class="insight-card">{insight}</div>', unsafe_allow_html=True)

st.markdown("---")
st.markdown(
    '<p style="text-align: center; color: rgba(255, 255, 255, 0.6); padding: 2rem 0; font-size: 0.95rem;">Made with ❤️ by Aishwarya Patil | Powered by Streamlit</p>',
    unsafe_allow_html=True
)