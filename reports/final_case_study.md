# Case Study: E-commerce Customer Behavior Deep Dive

## 1. Problem Statement
The e-commerce platform seeks to understand user behavior patterns to improve conversion rates and customer lifetime value. This report analyzes event-level data to pinpoint where users drop off and which customer segments are most valuable.

## 2. Dataset Description
- **Source**: eCommerce Events History (October 2019)
- **Size**: 3.9 Million cleaned events
- **Features**: Event Time, Event Type (View, Cart, Purchase), Product IDs, Category, Brand, Price, User IDs, and Session IDs.
- **Engineered Features**: Session Duration, Customer Type (New vs Returning), RFM Scores, and Activity Timeframes.

## 3. Methodology
1. **Data Cleaning**: Handled missing category labels, removed duplicates, and synchronized timestamps.
2. **Funnel Analysis**: Calculated transition rates between View -> Cart -> Purchase.
3. **Behavior Modeling**: Analyzed the correlation between session length and purchase likelihood.
4. **Segmentation**: Performed RFM (Recency, Frequency, Monetary) analysis to group users based on value.
5. **Visualization**: Used Python (Matplotlib/Seaborn) to create business-friendly charts.

## 4. Key Findings & Business Recommendations

| Finding | Impact | Action |
| :--- | :--- | :--- |
| **Top-Funnel Drop-off** | 95% of viewers never add to cart | Optimize Product Pages & UI/UX |
| **VIP Contribution** | 40%+ Revenue from <10% Users | Launch VIP Loyalty Program |
| **Golden Hours (10AM-2PM)** | Highest conversion & traffic volume | Sync Ad Spend & Email Campaigns |
| **Duration Correlation** | Conversions peak after 5-10 mins | Implement Live Chat for long sessions |

## 5. Conclusion
By shifting focus from broad traffic acquisition to **top-funnel engagement** and **high-value retention**, the platform can significantly increase its ROI without increasing total ad spend.

---
*Analysis performed by Senior Data Analyst Antigravity*
