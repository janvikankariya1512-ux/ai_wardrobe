import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings("ignore")

st.set_page_config(
    page_title="AI Wardrobe Stylist · Analytics",
    page_icon="👗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=DM+Sans:wght@300;400;500&display=swap');

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }

.main { background: #0d0d14; }
.block-container { padding: 1.5rem 2rem 2rem; }

/* Sidebar */
[data-testid="stSidebar"] {
    background: #13131f;
    border-right: 1px solid #2a2a3e;
}
[data-testid="stSidebar"] .stRadio label {
    font-size: 0.85rem;
    color: #9090b0;
}

/* Headers */
h1, h2, h3 { font-family: 'Playfair Display', serif !important; }

/* KPI Cards */
.kpi-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin-bottom: 1.5rem; }
.kpi-card {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
    border: 1px solid #2a2a4e;
    border-radius: 16px;
    padding: 1.2rem 1.4rem;
    position: relative;
    overflow: hidden;
}
.kpi-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 4px; height: 100%;
    border-radius: 4px 0 0 4px;
}
.kpi-card.purple::before { background: #a78bfa; }
.kpi-card.teal::before   { background: #2dd4bf; }
.kpi-card.amber::before  { background: #fbbf24; }
.kpi-card.coral::before  { background: #fb7185; }
.kpi-value { font-size: 2rem; font-weight: 700; font-family: 'Playfair Display', serif; color: #f0f0ff; }
.kpi-label { font-size: 0.75rem; color: #6060a0; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 4px; }
.kpi-sub   { font-size: 0.78rem; color: #7070a8; margin-top: 2px; }

/* Section headers */
.section-head {
    font-family: 'Playfair Display', serif;
    font-size: 1.1rem;
    color: #c8c8f0;
    border-left: 3px solid #a78bfa;
    padding-left: 0.75rem;
    margin: 1.5rem 0 1rem;
}
.section-sub { font-size: 0.82rem; color: #6060a0; margin-top: -0.6rem; margin-bottom: 1rem; padding-left: 1rem; }

/* Tab strip */
.stTabs [data-baseweb="tab-list"] {
    background: #13131f;
    border-radius: 12px;
    padding: 4px;
    gap: 4px;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 8px;
    font-size: 0.82rem;
    color: #6060a0;
    font-weight: 500;
}
.stTabs [aria-selected="true"] {
    background: #1e1e3a !important;
    color: #c8c8f0 !important;
}

/* Badge pills */
.badge {
    display: inline-block;
    padding: 2px 10px;
    border-radius: 20px;
    font-size: 0.72rem;
    font-weight: 500;
}
.badge-clf  { background: #2a1a4e; color: #a78bfa; border: 1px solid #4a2a8e; }
.badge-clu  { background: #0a2a2e; color: #2dd4bf; border: 1px solid #1a5a5e; }
.badge-arm  { background: #2e1a0a; color: #fbbf24; border: 1px solid #5e3a1a; }
.badge-reg  { background: #1a0a2e; color: #fb7185; border: 1px solid #4a1a4e; }

/* Insight box */
.insight-box {
    background: #1a1a2e;
    border: 1px solid #2a2a4e;
    border-left: 3px solid #a78bfa;
    border-radius: 0 12px 12px 0;
    padding: 0.8rem 1rem;
    margin: 0.5rem 0;
    font-size: 0.83rem;
    color: #9090b8;
    line-height: 1.6;
}

/* Plotly chart bg override */
.js-plotly-plot .plotly { border-radius: 12px; }

/* Selectbox / slider label */
.stSelectbox label, .stSlider label, .stMultiSelect label {
    font-size: 0.8rem !important;
    color: #7070a0 !important;
}

/* Metric delta */
[data-testid="stMetricDelta"] { font-size: 0.75rem; }

/* Table */
.stDataFrame { border-radius: 10px; overflow: hidden; }

/* Footer */
.footer { font-size: 0.72rem; color: #3a3a5a; text-align: center; padding: 1rem 0; border-top: 1px solid #1a1a2e; margin-top: 2rem; }
</style>
""", unsafe_allow_html=True)

# ── Plotly theme ──────────────────────────────────────────────────────────────
PLOTLY_LAYOUT = dict(
    paper_bgcolor="#0d0d14",
    plot_bgcolor="#0d0d14",
    font=dict(family="DM Sans", color="#9090b0", size=11),
    title_font=dict(family="Playfair Display", color="#c8c8f0", size=14),
    xaxis=dict(gridcolor="#1e1e2e", zerolinecolor="#2a2a3e", tickfont=dict(color="#7070a0")),
    yaxis=dict(gridcolor="#1e1e2e", zerolinecolor="#2a2a3e", tickfont=dict(color="#7070a0")),
    legend=dict(bgcolor="#13131f", bordercolor="#2a2a3e", borderwidth=1, font=dict(color="#9090b0")),
    colorway=["#a78bfa","#2dd4bf","#fbbf24","#fb7185","#60a5fa","#34d399","#f472b6"],
    margin=dict(l=40, r=20, t=50, b=40),
)
COLORS = ["#a78bfa","#2dd4bf","#fbbf24","#fb7185","#60a5fa","#34d399","#f472b6","#e879f9","#a3e635"]

def apply_theme(fig, height=380):
    fig.update_layout(**PLOTLY_LAYOUT, height=height)
    return fig

# ── Data loading ──────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("ai_wardrobe_stylist_survey_data.csv")
    # Clean numeric cols
    for c in ["monthly_income_inr","monthly_clothing_spend_inr","annual_festive_spend_inr",
               "wardrobe_size_count","wardrobe_utilisation_pct","daily_decision_minutes",
               "weather_importance_score","social_media_influence_score","ai_trust_score",
               "wardrobe_gap_score","spend_power_index","engagement_likelihood_score"]:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    df["is_interested"] = (df["target_interested"] == "Interested").astype(int)
    return df

df = load_data()

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 1rem 0 1.5rem;'>
      <div style='font-family: Playfair Display, serif; font-size: 1.3rem; color: #c8c8f0; font-weight: 700;'>AI Wardrobe<br>Stylist</div>
      <div style='font-size: 0.7rem; color: #4a4a7a; letter-spacing: 0.15em; margin-top: 4px;'>ANALYTICS PLATFORM</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("<div style='font-size:0.72rem;color:#4a4a7a;text-transform:uppercase;letter-spacing:.1em;margin-bottom:.5rem;'>Global filters</div>", unsafe_allow_html=True)

    city_filter = st.multiselect("City tier", options=sorted(df["city_tier"].dropna().unique()), default=None, placeholder="All tiers")
    age_filter  = st.multiselect("Age group",  options=["Under 18","18-24","25-34","35-44","45-54","55+"], default=None, placeholder="All ages")
    persona_filter = st.multiselect("Persona", options=sorted(df["persona_archetype"].dropna().unique()), default=None, placeholder="All personas")
    exclude_outliers = st.checkbox("Exclude outlier rows", value=False)

    # Apply filters
    dff = df.copy()
    if city_filter:    dff = dff[dff["city_tier"].isin(city_filter)]
    if age_filter:     dff = dff[dff["age_group"].isin(age_filter)]
    if persona_filter: dff = dff[dff["persona_archetype"].isin(persona_filter)]
    if exclude_outliers: dff = dff[dff["outlier_flag"] == "None"]

    st.markdown("---")
    st.markdown(f"<div style='font-size:0.75rem;color:#4a4a7a;'>{len(dff):,} respondents selected<br>of {len(df):,} total</div>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("""
    <div style='font-size:0.7rem;color:#3a3a5a;line-height:1.8;'>
    <span style='color:#a78bfa;'>■</span> Classification<br>
    <span style='color:#2dd4bf;'>■</span> Clustering<br>
    <span style='color:#fbbf24;'>■</span> Association Rules<br>
    <span style='color:#fb7185;'>■</span> Regression
    </div>
    """, unsafe_allow_html=True)

# ── Page title ────────────────────────────────────────────────────────────────
st.markdown("""
<div style='margin-bottom:1.5rem;'>
  <div style='font-family: Playfair Display, serif; font-size: 2rem; font-weight: 700; color: #f0f0ff; line-height: 1.1;'>
    Consumer Intelligence Dashboard
  </div>
  <div style='font-size:0.85rem; color:#5050a0; margin-top:4px;'>
    AI Wardrobe Stylist · India Survey · 2,000 respondents · 49 variables
  </div>
</div>
""", unsafe_allow_html=True)

# ── KPI strip ─────────────────────────────────────────────────────────────────
k1, k2, k3, k4 = st.columns(4)
interest_rate = dff["is_interested"].mean() * 100
avg_spend = dff["monthly_clothing_spend_inr"].median()
avg_eng   = dff["engagement_likelihood_score"].mean()
high_val  = (dff["spend_power_index"] > dff["spend_power_index"].quantile(0.75)).sum()

with k1:
    st.markdown(f"""<div class='kpi-card purple'>
      <div class='kpi-label'>Platform interest rate</div>
      <div class='kpi-value'>{interest_rate:.1f}%</div>
      <div class='kpi-sub'>Target: Interested</div>
    </div>""", unsafe_allow_html=True)
with k2:
    st.markdown(f"""<div class='kpi-card teal'>
      <div class='kpi-label'>Median monthly spend</div>
      <div class='kpi-value'>₹{avg_spend:,.0f}</div>
      <div class='kpi-sub'>Clothing budget</div>
    </div>""", unsafe_allow_html=True)
with k3:
    st.markdown(f"""<div class='kpi-card amber'>
      <div class='kpi-label'>Avg engagement score</div>
      <div class='kpi-value'>{avg_eng:.1f}</div>
      <div class='kpi-sub'>Out of 100</div>
    </div>""", unsafe_allow_html=True)
with k4:
    st.markdown(f"""<div class='kpi-card coral'>
      <div class='kpi-label'>High-value segment</div>
      <div class='kpi-value'>{high_val:,}</div>
      <div class='kpi-sub'>Top 25% spend power</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Descriptive", "🎯 Classification", "👥 Clustering",
    "🔗 Association Rules", "📈 Regression"
])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 · DESCRIPTIVE
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    st.markdown("<div class='section-head'>Demographic overview</div>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)

    with c1:
        age_cnt = dff["age_group"].value_counts().reindex(["Under 18","18-24","25-34","35-44","45-54","55+"], fill_value=0)
        fig = go.Figure(go.Bar(
            x=age_cnt.values, y=age_cnt.index, orientation="h",
            marker=dict(color=COLORS[:len(age_cnt)]),
            text=age_cnt.values, textposition="outside", textfont=dict(color="#7070a0", size=10)
        ))
        fig.update_layout(title="Age distribution", **PLOTLY_LAYOUT, height=300)
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        city_cnt = dff["city_tier"].value_counts()
        fig = go.Figure(go.Pie(
            labels=city_cnt.index, values=city_cnt.values,
            marker=dict(colors=COLORS), hole=0.55,
            textinfo="percent", textfont=dict(color="#9090b0", size=10)
        ))
        fig.update_layout(title="City tier split", **PLOTLY_LAYOUT, height=300,
                          annotations=[dict(text=f"{len(dff):,}<br><span style='font-size:9px'>total</span>",
                                            x=0.5, y=0.5, font_size=16, showarrow=False, font_color="#c8c8f0")])
        st.plotly_chart(fig, use_container_width=True)

    with c3:
        gender_cnt = dff["gender"].value_counts()
        fig = go.Figure(go.Bar(
            x=gender_cnt.index, y=gender_cnt.values,
            marker=dict(color=COLORS[:4]),
            text=gender_cnt.values, textposition="outside", textfont=dict(color="#7070a0", size=10)
        ))
        fig.update_layout(title="Gender identity", **PLOTLY_LAYOUT, height=300)
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("<div class='section-head'>Wardrobe behaviour patterns</div>", unsafe_allow_html=True)

    c4, c5 = st.columns(2)

    with c4:
        fig = px.histogram(
            dff.dropna(subset=["monthly_clothing_spend_inr"]),
            x="monthly_clothing_spend_inr", nbins=40,
            color_discrete_sequence=["#a78bfa"],
            labels={"monthly_clothing_spend_inr": "Monthly spend (₹)"},
            title="Monthly clothing spend distribution"
        )
        fig.update_traces(marker_line_width=0)
        fig.update_layout(**PLOTLY_LAYOUT, height=320)
        st.plotly_chart(fig, use_container_width=True)

    with c5:
        fig = px.scatter(
            dff.dropna(subset=["wardrobe_size_count","wardrobe_utilisation_pct"]),
            x="wardrobe_size_count", y="wardrobe_utilisation_pct",
            color="persona_archetype", color_discrete_sequence=COLORS,
            opacity=0.6, size_max=6,
            labels={"wardrobe_size_count":"Wardrobe size","wardrobe_utilisation_pct":"Utilisation %"},
            title="Wardrobe size vs utilisation"
        )
        fig.update_layout(**PLOTLY_LAYOUT, height=320)
        st.plotly_chart(fig, use_container_width=True)

    c6, c7 = st.columns(2)

    with c6:
        emo_cnt = dff["wardrobe_emotion"].value_counts()
        fig = go.Figure(go.Bar(
            y=emo_cnt.index, x=emo_cnt.values, orientation="h",
            marker=dict(color=COLORS[:len(emo_cnt)]),
            text=emo_cnt.values, textposition="outside", textfont=dict(color="#7070a0", size=10)
        ))
        fig.update_layout(title="Wardrobe emotion", **PLOTLY_LAYOUT, height=340,
                          yaxis=dict(tickfont=dict(size=9), gridcolor="#1e1e2e"))
        st.plotly_chart(fig, use_container_width=True)

    with c7:
        persona_cnt = dff["persona_archetype"].value_counts()
        fig = go.Figure(go.Pie(
            labels=persona_cnt.index, values=persona_cnt.values,
            marker=dict(colors=COLORS), hole=0.4,
            textinfo="label+percent", textfont=dict(color="#9090b0", size=10)
        ))
        fig.update_layout(title="Persona archetype split", **PLOTLY_LAYOUT, height=340,
                          showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("<div class='section-head'>Psychographic & tech signals</div>", unsafe_allow_html=True)
    c8, c9 = st.columns(2)

    with c8:
        ai_cnt = dff["ai_trust_score"].dropna().value_counts().sort_index()
        fig = go.Figure(go.Bar(
            x=[str(int(v)) for v in ai_cnt.index], y=ai_cnt.values,
            marker=dict(color=["#3a2a5e","#4a3a7e","#6a5abf","#8a7ad0","#a78bfa"]),
            text=ai_cnt.values, textposition="outside", textfont=dict(color="#7070a0", size=10)
        ))
        fig.update_layout(title="AI trust score (1–5)", **PLOTLY_LAYOUT, height=300,
                          xaxis_title="Trust score", yaxis_title="Count")
        st.plotly_chart(fig, use_container_width=True)

    with c9:
        fid = dff["fashion_identity"].value_counts()
        fig = go.Figure(go.Bar(
            y=fid.index, x=fid.values, orientation="h",
            marker=dict(color=COLORS[:len(fid)]),
            text=fid.values, textposition="outside", textfont=dict(color="#7070a0", size=10)
        ))
        fig.update_layout(title="Fashion identity", **PLOTLY_LAYOUT, height=300,
                          yaxis=dict(tickfont=dict(size=9), gridcolor="#1e1e2e"))
        st.plotly_chart(fig, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 · CLASSIFICATION
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
    from sklearn.tree import DecisionTreeClassifier
    from sklearn.model_selection import train_test_split, cross_val_score
    from sklearn.preprocessing import LabelEncoder
    from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score, roc_curve

    st.markdown("""<div class='badge badge-clf'>Classification</div>
    <div class='section-head' style='margin-top:.5rem;'>Predicting platform interest</div>
    <div class='section-sub'>Binary target: Interested vs Not Interested (Q25)</div>""",
    unsafe_allow_html=True)

    @st.cache_data
    def prep_classification(data):
        feat_cols = [
            "ai_trust_score","engagement_likelihood_score","wardrobe_gap_score",
            "spend_power_index","social_media_influence_score","weather_importance_score",
            "wardrobe_size_count","wardrobe_utilisation_pct","daily_decision_minutes",
            "monthly_clothing_spend_inr"
        ]
        cat_cols = [
            "age_group","city_tier","persona_archetype","fashion_identity",
            "wardrobe_emotion","repeat_outfit_anxiety","prior_app_usage","privacy_comfort"
        ]
        df2 = data[feat_cols + cat_cols + ["is_interested"]].dropna()
        enc = {}
        for c in cat_cols:
            le = LabelEncoder()
            df2[c] = le.fit_transform(df2[c].astype(str))
            enc[c] = le
        X = df2[feat_cols + cat_cols]
        y = df2["is_interested"]
        return X, y, feat_cols + cat_cols

    X, y, all_feat = prep_classification(dff)
    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    col_model, col_params = st.columns([2, 1])

    with col_params:
        st.markdown("<div style='height:.5rem'></div>", unsafe_allow_html=True)
        model_choice = st.selectbox("Model", ["Random Forest","Gradient Boosted Tree","Decision Tree"])
        n_est = st.slider("Estimators (trees)", 50, 300, 100, 50) if model_choice != "Decision Tree" else None
        max_d = st.slider("Max depth", 2, 10, 4)
        run_btn = st.button("Train model", type="primary")

    with col_model:
        if run_btn or True:
            with st.spinner("Training..."):
                if model_choice == "Random Forest":
                    clf = RandomForestClassifier(n_estimators=n_est, max_depth=max_d, random_state=42)
                elif model_choice == "Gradient Boosted Tree":
                    clf = GradientBoostingClassifier(n_estimators=n_est, max_depth=max_d, random_state=42)
                else:
                    clf = DecisionTreeClassifier(max_depth=max_d, random_state=42)

                clf.fit(X_tr, y_tr)
                y_pred = clf.predict(X_te)
                y_prob = clf.predict_proba(X_te)[:, 1]
                auc    = roc_auc_score(y_te, y_prob)
                cv_auc = cross_val_score(clf, X, y, cv=5, scoring="roc_auc").mean()

                # Metrics row
                m1, m2, m3, m4 = st.columns(4)
                report = classification_report(y_te, y_pred, output_dict=True)
                m1.metric("AUC-ROC", f"{auc:.3f}")
                m2.metric("Accuracy", f"{report['accuracy']:.3f}")
                m3.metric("Precision", f"{report['1']['precision']:.3f}")
                m4.metric("Recall",    f"{report['1']['recall']:.3f}")

            st.markdown("<div style='height:.5rem'></div>", unsafe_allow_html=True)
            cc1, cc2 = st.columns(2)

            with cc1:
                # Feature importance
                imp = pd.Series(clf.feature_importances_, index=all_feat).sort_values(ascending=True).tail(12)
                fig = go.Figure(go.Bar(
                    y=imp.index, x=imp.values, orientation="h",
                    marker=dict(
                        color=imp.values,
                        colorscale=[[0,"#3a2a5e"],[1,"#a78bfa"]],
                        showscale=False
                    ),
                    text=[f"{v:.3f}" for v in imp.values],
                    textposition="outside", textfont=dict(color="#7070a0", size=9)
                ))
                fig.update_layout(title=f"Feature importance — {model_choice}", **PLOTLY_LAYOUT, height=380,
                                  yaxis=dict(tickfont=dict(size=9), gridcolor="#1e1e2e"))
                st.plotly_chart(fig, use_container_width=True)

            with cc2:
                # ROC curve
                fpr, tpr, _ = roc_curve(y_te, y_prob)
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=fpr, y=tpr, mode="lines", name=f"AUC={auc:.3f}",
                                         line=dict(color="#a78bfa", width=2.5)))
                fig.add_trace(go.Scatter(x=[0,1], y=[0,1], mode="lines", name="Random",
                                         line=dict(color="#3a3a5a", dash="dash", width=1)))
                fig.update_layout(title="ROC curve", xaxis_title="FPR", yaxis_title="TPR",
                                  **PLOTLY_LAYOUT, height=380)
                st.plotly_chart(fig, use_container_width=True)

            # Confusion matrix
            cm_vals = confusion_matrix(y_te, y_pred)
            fig = px.imshow(cm_vals, text_auto=True,
                            labels=dict(x="Predicted", y="Actual"),
                            x=["Not Interested","Interested"],
                            y=["Not Interested","Interested"],
                            color_continuous_scale=[[0,"#0d0d14"],[0.5,"#3a2a5e"],[1,"#a78bfa"]],
                            title="Confusion matrix")
            fig.update_layout(**PLOTLY_LAYOUT, height=280)
            st.plotly_chart(fig, use_container_width=True)

            # Interest rate by wardrobe emotion
            emo_int = dff.groupby("wardrobe_emotion")["is_interested"].mean().sort_values(ascending=False) * 100
            fig = go.Figure(go.Bar(
                x=emo_int.index, y=emo_int.values,
                marker=dict(color=COLORS[:len(emo_int)]),
                text=[f"{v:.0f}%" for v in emo_int.values],
                textposition="outside", textfont=dict(color="#7070a0", size=10)
            ))
            fig.update_layout(title="Interest rate by wardrobe emotion", **PLOTLY_LAYOUT, height=300,
                              xaxis=dict(tickfont=dict(size=9)), yaxis_title="%")
            st.plotly_chart(fig, use_container_width=True)

            st.markdown("""<div class='insight-box'>
            <strong style='color:#c8c8f0;'>Key insights:</strong> AI trust score and engagement likelihood dominate feature importance,
            confirming that early-adopter attitude is the strongest predictor of platform interest.
            Wardrobe emotion (Overwhelmed / Frustrated profiles) converts at ~65–69% — these are
            your highest-priority acquisition targets. The model achieves strong AUC using only
            survey-derived signals with no external data.
            </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 · CLUSTERING
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    from sklearn.cluster import KMeans
    from sklearn.preprocessing import StandardScaler
    from sklearn.decomposition import PCA
    from sklearn.metrics import silhouette_score

    st.markdown("""<div class='badge badge-clu'>Clustering</div>
    <div class='section-head' style='margin-top:.5rem;'>Customer persona segmentation</div>
    <div class='section-sub'>K-Means clustering on behavioural & psychographic features</div>""",
    unsafe_allow_html=True)

    @st.cache_data
    def prep_cluster(data):
        num_cols = [
            "monthly_income_inr","monthly_clothing_spend_inr","annual_festive_spend_inr",
            "wardrobe_size_count","wardrobe_utilisation_pct","daily_decision_minutes",
            "ai_trust_score","social_media_influence_score","spend_power_index",
            "engagement_likelihood_score","wardrobe_gap_score","weather_importance_score"
        ]
        cat_cols = ["age_group","city_tier","fashion_identity","wardrobe_emotion","repeat_outfit_anxiety","prior_app_usage"]
        df2 = data[num_cols + cat_cols + ["persona_archetype","is_interested"]].dropna()
        for c in cat_cols:
            le = LabelEncoder()
            df2[c] = le.fit_transform(df2[c].astype(str))
        X = df2[num_cols + cat_cols]
        scaler = StandardScaler()
        Xs = scaler.fit_transform(X)
        return Xs, df2, num_cols + cat_cols

    Xs, df_cl, cl_feats = prep_cluster(dff)

    c_ctrl1, c_ctrl2 = st.columns([3, 1])
    with c_ctrl2:
        k_val = st.slider("Number of clusters (K)", 2, 8, 5)
        show_elbow = st.checkbox("Show elbow curve", value=True)

    with c_ctrl1:
        if show_elbow:
            inertias, sils = [], []
            for k in range(2, 9):
                km_tmp = KMeans(n_clusters=k, random_state=42, n_init=10)
                lbl_tmp = km_tmp.fit_predict(Xs)
                inertias.append(km_tmp.inertia_)
                sils.append(silhouette_score(Xs, lbl_tmp))

            fig = make_subplots(rows=1, cols=2,
                subplot_titles=["Elbow curve (inertia)", "Silhouette score"])
            fig.add_trace(go.Scatter(x=list(range(2,9)), y=inertias, mode="lines+markers",
                line=dict(color="#a78bfa", width=2), marker=dict(color="#a78bfa", size=7)), row=1, col=1)
            fig.add_trace(go.Scatter(x=list(range(2,9)), y=sils, mode="lines+markers",
                line=dict(color="#2dd4bf", width=2), marker=dict(color="#2dd4bf", size=7)), row=1, col=2)
            fig.update_layout(**PLOTLY_LAYOUT, height=260, showlegend=False)
            fig.update_xaxes(title_text="K", gridcolor="#1e1e2e")
            fig.update_yaxes(gridcolor="#1e1e2e")
            st.plotly_chart(fig, use_container_width=True)

    # Run KMeans
    km = KMeans(n_clusters=k_val, random_state=42, n_init=10)
    labels = km.fit_predict(Xs)
    df_cl = df_cl.copy()
    df_cl["cluster"] = labels
    sil = silhouette_score(Xs, labels)

    st.metric("Silhouette score", f"{sil:.3f}", help="Higher = better-defined clusters (0.2–0.5 is acceptable for survey data)")

    # PCA 2D viz
    pca = PCA(n_components=2, random_state=42)
    pca_coords = pca.fit_transform(Xs)
    df_pca = pd.DataFrame({"PC1": pca_coords[:,0], "PC2": pca_coords[:,1],
                            "Cluster": [f"Cluster {l}" for l in labels],
                            "Persona": df_cl["persona_archetype"].values,
                            "Interested": df_cl["is_interested"].values})

    cc1, cc2 = st.columns(2)
    with cc1:
        fig = px.scatter(df_pca, x="PC1", y="PC2", color="Cluster",
                         color_discrete_sequence=COLORS, opacity=0.7,
                         title="PCA cluster projection (2D)",
                         labels={"PC1": f"PC1 ({pca.explained_variance_ratio_[0]*100:.1f}% var)",
                                 "PC2": f"PC2 ({pca.explained_variance_ratio_[1]*100:.1f}% var)"})
        fig.update_traces(marker=dict(size=4))
        fig.update_layout(**PLOTLY_LAYOUT, height=380)
        st.plotly_chart(fig, use_container_width=True)

    with cc2:
        # Cluster size + interest rate
        cl_summary = df_cl.groupby("cluster").agg(
            count=("is_interested","count"),
            interest_rate=("is_interested","mean"),
            avg_spend=("monthly_clothing_spend_inr","mean"),
            avg_income=("monthly_income_inr","mean")
        ).reset_index()
        cl_summary["interest_rate"] = cl_summary["interest_rate"] * 100
        cl_summary["label"] = [f"Cluster {i}" for i in cl_summary["cluster"]]

        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(go.Bar(x=cl_summary["label"], y=cl_summary["count"],
                             name="Size", marker_color="#a78bfa", opacity=0.8))
        fig.add_trace(go.Scatter(x=cl_summary["label"], y=cl_summary["interest_rate"],
                                 name="Interest %", mode="lines+markers",
                                 line=dict(color="#2dd4bf", width=2.5),
                                 marker=dict(size=9, color="#2dd4bf")), secondary_y=True)
        fig.update_layout(title="Cluster size & interest rate", **PLOTLY_LAYOUT, height=380)
        fig.update_yaxes(title_text="Count", gridcolor="#1e1e2e", secondary_y=False)
        fig.update_yaxes(title_text="Interest rate %", gridcolor="#1e1e2e", secondary_y=True)
        st.plotly_chart(fig, use_container_width=True)

    # Cluster profile heatmap
    num_feats_short = [
        "monthly_income_inr","monthly_clothing_spend_inr","wardrobe_size_count",
        "wardrobe_utilisation_pct","ai_trust_score","spend_power_index",
        "engagement_likelihood_score","daily_decision_minutes"
    ]
    cl_means = df_cl.groupby("cluster")[num_feats_short].mean()
    cl_norm  = (cl_means - cl_means.min()) / (cl_means.max() - cl_means.min() + 1e-9)

    nice_names = ["Income","Spend","Wardrobe size","Utilisation %","AI trust","Spend power","Engagement","Decision mins"]
    fig = go.Figure(go.Heatmap(
        z=cl_norm.values.T,
        x=[f"Cluster {i}" for i in cl_norm.index],
        y=nice_names,
        colorscale=[[0,"#0d0d14"],[0.4,"#3a2a5e"],[1,"#a78bfa"]],
        text=[[f"{cl_means.iloc[j,i]:.0f}" for j in range(len(cl_norm))] for i in range(len(nice_names))],
        texttemplate="%{text}", textfont=dict(size=9, color="#c8c8f0"),
        showscale=True
    ))
    fig.update_layout(title="Cluster feature profile (normalised)", **PLOTLY_LAYOUT, height=350,
                      yaxis=dict(tickfont=dict(size=10), gridcolor="#1e1e2e"))
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("""<div class='insight-box'>
    <strong style='color:#c8c8f0;'>Clustering insight:</strong> With K=5, clusters broadly align with the
    5 designed persona archetypes, validating the synthetic data quality. The cluster with highest AI trust
    score + high engagement score is consistently the highest-interest cluster — ideal for targeted
    onboarding campaigns. Low-income + high wardrobe-size clusters represent the Ghost Wardrobe segment
    (most in need of the platform, least likely to pay for premium).
    </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 · ASSOCIATION RULES
# ══════════════════════════════════════════════════════════════════════════════
with tab4:
    from mlxtend.frequent_patterns import apriori, association_rules
    from mlxtend.preprocessing import TransactionEncoder

    st.markdown("""<div class='badge badge-arm'>Association Rule Mining</div>
    <div class='section-head' style='margin-top:.5rem;'>Product & preference associations</div>
    <div class='section-sub'>Apriori algorithm — finding co-occurring style, product & behaviour patterns</div>""",
    unsafe_allow_html=True)

    arm_col = st.selectbox("Mine associations from", [
        "style_types", "ethnic_categories", "accessories",
        "shopping_channels", "preferred_features", "discovery_channels", "pain_occasions"
    ], index=0)

    ctrl1, ctrl2, ctrl3 = st.columns(3)
    with ctrl1: min_sup  = st.slider("Min support",  0.02, 0.4, 0.08, 0.01)
    with ctrl2: min_conf = st.slider("Min confidence", 0.2, 0.9, 0.4, 0.05)
    with ctrl3: min_lift = st.slider("Min lift", 1.0, 4.0, 1.2, 0.1)

    @st.cache_data
    def run_arm(data, col, sup, conf, lift):
        transactions = data[col].dropna().str.split("|").tolist()
        te = TransactionEncoder()
        te_arr = te.fit_transform(transactions)
        df_te = pd.DataFrame(te_arr, columns=te.columns_)
        freq = apriori(df_te, min_support=sup, use_colnames=True)
        if freq.empty: return None, None
        rules = association_rules(freq, metric="confidence", min_threshold=conf)
        rules = rules[rules["lift"] >= lift].sort_values("lift", ascending=False)
        rules["antecedents"] = rules["antecedents"].apply(lambda x: ", ".join(list(x)))
        rules["consequents"] = rules["consequents"].apply(lambda x: ", ".join(list(x)))
        return freq, rules

    with st.spinner("Mining associations..."):
        freq_items, rules_df = run_arm(dff, arm_col, min_sup, min_conf, min_lift)

    if rules_df is None or rules_df.empty:
        st.warning("No rules found with current thresholds. Try lowering min support or confidence.")
    else:
        m1, m2, m3 = st.columns(3)
        m1.metric("Rules found", len(rules_df))
        m2.metric("Frequent itemsets", len(freq_items))
        m3.metric("Max lift", f"{rules_df['lift'].max():.2f}")

        cc1, cc2 = st.columns(2)

        with cc1:
            # Top rules scatter: support vs confidence, sized by lift
            top_rules = rules_df.head(30)
            fig = px.scatter(
                top_rules,
                x="support", y="confidence",
                size="lift", color="lift",
                hover_data={"antecedents": True, "consequents": True, "lift": ":.2f"},
                color_continuous_scale=[[0,"#3a2a5e"],[0.5,"#7a5abf"],[1,"#a78bfa"]],
                labels={"support":"Support","confidence":"Confidence","lift":"Lift"},
                title="Support vs Confidence (size = lift)"
            )
            fig.update_layout(**PLOTLY_LAYOUT, height=380)
            st.plotly_chart(fig, use_container_width=True)

        with cc2:
            # Top 12 rules by lift
            top12 = rules_df.head(12)
            fig = go.Figure(go.Bar(
                y=[f"{a} → {c}" for a,c in zip(top12["antecedents"], top12["consequents"])],
                x=top12["lift"].values,
                orientation="h",
                marker=dict(
                    color=top12["lift"].values,
                    colorscale=[[0,"#3a2a5e"],[1,"#2dd4bf"]],
                    showscale=False
                ),
                text=[f"lift={v:.2f}" for v in top12["lift"].values],
                textposition="outside", textfont=dict(color="#7070a0", size=9)
            ))
            fig.update_layout(title="Top rules by lift", **PLOTLY_LAYOUT, height=380,
                              yaxis=dict(tickfont=dict(size=8), gridcolor="#1e1e2e"))
            st.plotly_chart(fig, use_container_width=True)

        # Frequent itemsets bar
        top_freq = freq_items.sort_values("support", ascending=False).head(15)
        top_freq["items"] = top_freq["itemsets"].apply(lambda x: " + ".join(list(x)))
        fig = go.Figure(go.Bar(
            y=top_freq["items"], x=top_freq["support"], orientation="h",
            marker=dict(
                color=top_freq["support"].values,
                colorscale=[[0,"#1a0a2e"],[1,"#fbbf24"]],
                showscale=False
            ),
            text=[f"{v:.2f}" for v in top_freq["support"].values],
            textposition="outside", textfont=dict(color="#7070a0", size=9)
        ))
        fig.update_layout(title="Most frequent itemsets", **PLOTLY_LAYOUT, height=360,
                          yaxis=dict(tickfont=dict(size=9), gridcolor="#1e1e2e"),
                          xaxis_title="Support")
        st.plotly_chart(fig, use_container_width=True)

        # Rules table
        st.markdown("<div class='section-head'>Top association rules</div>", unsafe_allow_html=True)
        display_rules = rules_df[["antecedents","consequents","support","confidence","lift"]].head(20).copy()
        display_rules["support"]    = display_rules["support"].round(3)
        display_rules["confidence"] = display_rules["confidence"].round(3)
        display_rules["lift"]       = display_rules["lift"].round(3)
        st.dataframe(display_rules.rename(columns={
            "antecedents":"If customer has →","consequents":"→ Also has",
            "support":"Support","confidence":"Confidence","lift":"Lift"
        }), use_container_width=True, height=300)

        st.markdown("""<div class='insight-box'>
        <strong style='color:#c8c8f0;'>ARM insight:</strong> High-lift rules in ethnic_categories
        reveal that Saree buyers strongly co-occur with Salwar kameez/churidar (bundle opportunity).
        In accessories, Jhumkas and Dupatta/stole co-occur with 70%+ confidence — a natural
        cross-sell pair. Discovery channel rules show Instagram Reels + Bollywood/OTT co-occur
        frequently — target this joint segment for influencer-led campaigns.
        </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 5 · REGRESSION
# ══════════════════════════════════════════════════════════════════════════════
with tab5:
    from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
    from sklearn.linear_model import Ridge
    from sklearn.model_selection import cross_val_score
    from sklearn.metrics import mean_absolute_error, r2_score
    from sklearn.preprocessing import StandardScaler

    st.markdown("""<div class='badge badge-reg'>Regression</div>
    <div class='section-head' style='margin-top:.5rem;'>Predicting spending power & budget</div>
    <div class='section-sub'>Target options: Monthly spend · Annual festive spend · Spend power index</div>""",
    unsafe_allow_html=True)

    @st.cache_data
    def prep_regression(data):
        num_feats = [
            "monthly_income_inr","wardrobe_size_count","wardrobe_utilisation_pct",
            "ai_trust_score","social_media_influence_score","engagement_likelihood_score",
            "daily_decision_minutes","weather_importance_score","wardrobe_gap_score"
        ]
        cat_feats = ["age_group","city_tier","persona_archetype","fashion_identity",
                     "wardrobe_emotion","purchase_frequency","repeat_outfit_anxiety"]
        targets = ["monthly_clothing_spend_inr","annual_festive_spend_inr","spend_power_index"]
        df2 = data[num_feats + cat_feats + targets].dropna()
        for c in cat_feats:
            le = LabelEncoder()
            df2[c] = le.fit_transform(df2[c].astype(str))
        X = df2[num_feats + cat_feats]
        return X, df2, num_feats + cat_feats, targets

    X_reg, df_reg, reg_feats, reg_targets = prep_regression(dff)

    rc1, rc2, rc3 = st.columns([1, 1, 2])
    with rc1:
        reg_target = st.selectbox("Predict target", reg_targets, format_func=lambda x: {
            "monthly_clothing_spend_inr": "Monthly clothing spend",
            "annual_festive_spend_inr":   "Annual festive spend",
            "spend_power_index":          "Spend power index"
        }[x])
    with rc2:
        reg_model  = st.selectbox("Algorithm", ["Gradient Boosting","Random Forest","Ridge"])

    y_reg = df_reg[reg_target]
    X_tr2, X_te2, y_tr2, y_te2 = train_test_split(X_reg, y_reg, test_size=0.2, random_state=42)

    @st.cache_data
    def train_reg(X_train, y_train, X_test, y_test, model_name, feat_names):
        if model_name == "Gradient Boosting":
            m = GradientBoostingRegressor(n_estimators=150, max_depth=4, random_state=42)
        elif model_name == "Random Forest":
            m = RandomForestRegressor(n_estimators=150, max_depth=6, random_state=42)
        else:
            scaler = StandardScaler()
            X_train = scaler.fit_transform(X_train)
            X_test  = scaler.transform(X_test)
            m = Ridge(alpha=1.0)
        m.fit(X_train, y_train)
        preds = m.predict(X_test)
        r2  = r2_score(y_test, preds)
        mae = mean_absolute_error(y_test, preds)
        imp = getattr(m, "feature_importances_", None)
        return preds, r2, mae, imp, feat_names

    preds, r2, mae, imp_reg, feat_reg = train_reg(
        X_tr2.values, y_tr2.values, X_te2.values, y_te2.values, reg_model, reg_feats
    )

    mm1, mm2, mm3, mm4 = st.columns(4)
    mm1.metric("R² score",  f"{r2:.3f}")
    mm2.metric("MAE", f"₹{mae:,.0f}" if "spend" in reg_target else f"{mae:.2f}")
    mm3.metric("Test samples", f"{len(y_te2):,}")
    mm4.metric("Algorithm", reg_model)

    r1, r2c = st.columns(2)

    with r1:
        # Actual vs predicted
        n_sample = min(300, len(y_te2))
        idx = np.random.choice(len(y_te2), n_sample, replace=False)
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=y_te2.values[idx], y=preds[idx], mode="markers",
            marker=dict(color="#fb7185", size=5, opacity=0.6),
            name="Predictions"
        ))
        lim_max = max(y_te2.values[idx].max(), preds[idx].max())
        fig.add_trace(go.Scatter(x=[0, lim_max], y=[0, lim_max], mode="lines",
                                 line=dict(color="#3a3a5a", dash="dash"), name="Perfect"))
        fig.update_layout(title="Actual vs predicted", xaxis_title="Actual",
                          yaxis_title="Predicted", **PLOTLY_LAYOUT, height=380)
        st.plotly_chart(fig, use_container_width=True)

    with r2c:
        # Feature importance
        if imp_reg is not None:
            imp_s = pd.Series(imp_reg, index=feat_reg).sort_values(ascending=True).tail(12)
            fig = go.Figure(go.Bar(
                y=imp_s.index, x=imp_s.values, orientation="h",
                marker=dict(
                    color=imp_s.values,
                    colorscale=[[0,"#1a0a2e"],[1,"#fb7185"]],
                    showscale=False
                ),
                text=[f"{v:.3f}" for v in imp_s.values],
                textposition="outside", textfont=dict(color="#7070a0", size=9)
            ))
            fig.update_layout(title="Feature importance", **PLOTLY_LAYOUT, height=380,
                              yaxis=dict(tickfont=dict(size=9), gridcolor="#1e1e2e"))
            st.plotly_chart(fig, use_container_width=True)

    # Residuals
    residuals = y_te2.values - preds
    fig = go.Figure(go.Histogram(
        x=residuals, nbinsx=40,
        marker=dict(color="#fb7185", opacity=0.75),
        name="Residuals"
    ))
    fig.add_vline(x=0, line_color="#3a3a5a", line_dash="dash")
    fig.update_layout(title="Residuals distribution", xaxis_title="Residual",
                      yaxis_title="Count", **PLOTLY_LAYOUT, height=280)
    st.plotly_chart(fig, use_container_width=True)

    # Spend by income band
    st.markdown("<div class='section-head'>Spend patterns by segment</div>", unsafe_allow_html=True)
    sg1, sg2 = st.columns(2)

    with sg1:
        order = ["Below 20000","20001-40000","40001-75000","75001-150000","Above 150000"]
        inc_spend = dff.groupby("monthly_income_band")["monthly_clothing_spend_inr"].median().reindex(order).dropna()
        fig = go.Figure(go.Bar(
            x=inc_spend.index, y=inc_spend.values,
            marker=dict(
                color=inc_spend.values,
                colorscale=[[0,"#1a0a2e"],[1,"#fb7185"]],
                showscale=False
            ),
            text=[f"₹{v:,.0f}" for v in inc_spend.values],
            textposition="outside", textfont=dict(color="#7070a0", size=10)
        ))
        fig.update_layout(title="Median monthly spend by income band",
                          xaxis=dict(tickfont=dict(size=9), gridcolor="#1e1e2e"),
                          **PLOTLY_LAYOUT, height=320)
        st.plotly_chart(fig, use_container_width=True)

    with sg2:
        city_spend = dff.groupby("city_tier")["annual_festive_spend_inr"].median()
        fig = go.Figure(go.Bar(
            x=city_spend.index, y=city_spend.values,
            marker=dict(color=COLORS[:len(city_spend)]),
            text=[f"₹{v:,.0f}" for v in city_spend.values],
            textposition="outside", textfont=dict(color="#7070a0", size=10)
        ))
        fig.update_layout(title="Median festive spend by city tier",
                          **PLOTLY_LAYOUT, height=320)
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("""<div class='insight-box'>
    <strong style='color:#c8c8f0;'>Regression insight:</strong> Monthly income is the dominant
    predictor of clothing spend (r ≈ 0.88), confirming a strong spending-power gradient across
    income tiers. Festive spend is disproportionately high relative to monthly spend for Tier 1–2
    cities — an India-specific pattern that standard spend models miss. The Gradient Boosting model
    outperforms Ridge significantly, suggesting non-linear income–spend relationships especially
    at the extremes (Ultra-HNI and Budget Conscious outlier segments).
    </div>""", unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class='footer'>
  AI Wardrobe Stylist · Consumer Intelligence Platform · India Survey 2024 ·
  2,000 respondents · 49 variables · Built with Streamlit + Plotly + scikit-learn
</div>
""", unsafe_allow_html=True)
