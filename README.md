---
title: AI Wardrobe Stylist Analytics
emoji: 👗
colorFrom: purple
colorTo: indigo
sdk: streamlit
sdk_version: "1.35.0"
app_file: app.py
pinned: false
---

# AI Wardrobe Stylist — Analytics Dashboard

A production-grade Streamlit analytics platform for the AI Wardrobe Stylist India consumer survey (2,000 respondents, 49 variables).

## Features

| Tab | Analytics type | Algorithms |
|-----|---------------|-----------|
| Descriptive | EDA & profiling | Distribution plots, cross-tabs |
| Classification | Platform interest prediction | Random Forest, Gradient Boosting, Decision Tree |
| Clustering | Customer persona segmentation | K-Means + PCA + Elbow/Silhouette |
| Association Rules | Product & preference co-occurrence | Apriori (mlxtend) |
| Regression | Spending power prediction | Gradient Boosting, Random Forest, Ridge |

## Quick start

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy to Streamlit Cloud

1. Push this folder to a GitHub repository
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repo → select `app.py` → Deploy

## Project structure

```
wardrobe_dashboard/
├── app.py                              # Main dashboard
├── ai_wardrobe_stylist_survey_data.csv # Dataset (2,000 rows × 49 cols)
├── requirements.txt                    # Dependencies
├── .streamlit/
│   └── config.toml                     # Dark theme config
└── README.md
```

## Dataset columns (49)
Demographics · Wardrobe behaviour · Style preferences · Psychographics ·
Tech attitude · Derived features · Classification target (`target_interested`)
