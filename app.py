import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import calendar
# Setup for charts
sns.set(style="whitegrid")

@st.cache_data
def load_data():
    xls = pd.ExcelFile('Data-Analytics-Case-Study.xlsx')
    customer_df = pd.read_excel(xls, sheet_name='Customer Information')
    vendor_df = pd.read_excel(xls, sheet_name='Vendor Information')
    key_df = pd.read_excel(xls, sheet_name='Key')
    return customer_df, vendor_df, key_df

customer_df, vendor_df, key_df = load_data()

st.title("Shadiyana Data Analysis Dashboard")

# Sidebar for navigation
st.sidebar.header("Navigation")
section = st.sidebar.radio("Go to", ["Raw Data", "Customer Insights", "Vendor Insights", "Seasonal & Area Trends"])

if section == "Raw Data":
    st.subheader("Customer Data")
    st.write(customer_df.head())  # Show first 5 rows of customer data
    
    st.subheader("Vendor Data")
    st.write(vendor_df.head())  # Show first 5 rows of vendor data

    st.subheader("Key Data")
    st.write(key_df.head())  # Show first 5 rows of key data

if section == "Customer Insights":
    st.header("Customer Preferences and Behavior")

    # Convert date columns to datetime format
    customer_df['Event Date'] = pd.to_datetime(customer_df['Event Date'], errors='coerce').dt.tz_localize(None)
    customer_df['Date of Query'] = pd.to_datetime(customer_df['Date of Query'], errors='coerce').dt.tz_localize(None)
    customer_df = customer_df.dropna(subset=['Event Date', 'Date of Query'])

    # Extract months and calculate lead time
    customer_df['Event Month'] = customer_df['Event Date'].dt.month
    customer_df['Query Month'] = customer_df['Date of Query'].dt.month
    customer_df['Lead Time (Days)'] = (customer_df['Event Date'] - customer_df['Date of Query']).dt.days

    # Sidebar filters
    with st.sidebar:
        st.subheader(" Filters")
        min_guests, max_guests = int(customer_df['Number of Guests'].min()), int(customer_df['Number of Guests'].max())
        guest_range = st.slider("Number of Guests", min_value=min_guests, max_value=max_guests, value=(min_guests, max_guests))

        customer_filtered = customer_df[
            (customer_df['Number of Guests'] >= guest_range[0]) &
            (customer_df['Number of Guests'] <= guest_range[1])
        ]

    # Guest Count Distribution
    st.subheader("Guest Count Distribution")
    fig, ax = plt.subplots()
    sns.histplot(customer_filtered['Number of Guests'], kde=True, ax=ax, color='skyblue')
    ax.set_xlabel("Number of Guests")
    st.pyplot(fig)

    # Top Businesses by Query Count
    st.subheader("Top 10 Popular Businesses")
    top_venues = customer_filtered['Business Name'].value_counts().nlargest(10)
    st.bar_chart(top_venues)

    # Event Seasonality
    import calendar
    st.subheader("Event Demand by Month")
    ordered_months = list(calendar.month_name)[1:]
    event_month_counts = (
        customer_filtered['Event Month']
        .dropna()
        .apply(lambda x: calendar.month_name[int(x)])
        .value_counts()
        .reindex(ordered_months, fill_value=0)
    )
    st.line_chart(event_month_counts)

    #  Lead Time Analysis
    st.subheader("Lead Time: Days Between Query and Event")
    fig2, ax2 = plt.subplots()
    sns.histplot(customer_filtered['Lead Time (Days)'], bins=30, kde=True, color='mediumseagreen', ax=ax2)
    ax2.set_xlabel("Lead Time (Days)")
    st.pyplot(fig2)

    # Average Guest Count by Business
    st.subheader("Average Guest Count per Business (Top 10)")
    avg_guest_per_vendor = (
        customer_filtered.groupby('Business Name')['Number of Guests']
        .mean()
        .sort_values(ascending=False)
        .head(10)
    )
    fig3, ax3 = plt.subplots(figsize=(10, 5))
    sns.barplot(x=avg_guest_per_vendor.values, y=avg_guest_per_vendor.index, ax=ax3, palette='coolwarm')
    ax3.set_xlabel("Average Guests")
    ax3.set_ylabel("Business Name")
    st.pyplot(fig3)

    # Query Activity Heatmap
    st.subheader("Monthly Query Heatmap")
    customer_filtered['Query Year'] = customer_filtered['Date of Query'].dt.year
    query_heatmap = customer_filtered.pivot_table(
        index='Query Year',
        columns='Query Month',
        values='Buyer Name',
        aggfunc='count'
    ).fillna(0)
    query_heatmap.columns = [calendar.month_abbr[int(c)] for c in query_heatmap.columns]

    fig4, ax4 = plt.subplots(figsize=(12, 4))
    sns.heatmap(query_heatmap, cmap="YlGnBu", annot=True, fmt=".0f", linewidths=.5, ax=ax4)
    st.pyplot(fig4)
if section == "Vendor Insights":
    st.header("Vendor Distribution and Pricing Analysis")

    # Drop any rows with missing vendor names
    vendor_df = vendor_df.dropna(subset=["Business Name"])

    # 💰 Budget Category Distribution
    st.subheader("Budget Category Distribution")
    budget_counts = vendor_df['Budget Category'].value_counts()
    st.bar_chart(budget_counts)

    # 📍 Sub-Area Distribution
    st.subheader("Vendors by Sub-Area")
    sub_area_counts = vendor_df['Sub Area'].value_counts()
    fig1, ax1 = plt.subplots(figsize=(10, 4))
    sns.barplot(x=sub_area_counts.values, y=sub_area_counts.index, ax=ax1, palette="viridis")
    ax1.set_xlabel("Number of Vendors")
    ax1.set_ylabel("Sub Area")
    st.pyplot(fig1)

    # 🧭 Budget Category by Sub Area
    st.subheader("Budget Category by Sub-Area")
    category_by_area = vendor_df.groupby(['Sub Area', 'Budget Category']).size().unstack(fill_value=0)
    st.dataframe(category_by_area)

    fig2, ax2 = plt.subplots(figsize=(12, 6))
    category_by_area.plot(kind='bar', stacked=True, ax=ax2, colormap="Accent")
    ax2.set_title("Vendor Distribution by Budget and Sub-Area")
    ax2.set_ylabel("Number of Vendors")
    ax2.set_xlabel("Sub Area")
    st.pyplot(fig2)

    # 🏢 Top Sub Areas with Most Vendors
    st.subheader("Top 10 Sub Areas with Most Vendors")
    top_areas = sub_area_counts.head(10)
    st.bar_chart(top_areas)

    # 🎯 Ratio of Budget Tiers
    st.subheader("Proportion of Budget Tiers")
    fig3, ax3 = plt.subplots()
    budget_counts.plot.pie(autopct='%1.1f%%', ax=ax3, startangle=90, colors=sns.color_palette("pastel"))
    ax3.set_ylabel('')
    ax3.set_title("Overall Budget Distribution of Vendors")
    st.pyplot(fig3)

if section == "Seasonal & Area Trends":
    st.header("Seasonal Trends and Area Insights")
    
    # Merging customer and vendor data based on Business Name
    merged_df = pd.merge(customer_df, vendor_df, on='Business Name', how='inner')

    merged_df['Event Month'] = merged_df['Event Date'].dt.month
    # Seasonal trend of customer events by month
    event_month_counts = merged_df.groupby('Event Month').size() 

    # Seasonal trend by Sub Area (location)
    event_area_counts = merged_df.groupby('Event Month')['Sub Area'].value_counts().unstack(fill_value=0)

    # Visualizing the seasonal event distribution
    st.subheader("Customer Event Demand by Month and Area")
    fig, ax = plt.subplots(figsize=(12, 6))
    event_area_counts.plot(kind='line', ax=ax)
    ax.set_xlabel("Month")
    ax.set_ylabel("Number of Events")
    ax.set_title("Customer Event Demand by Month and Sub Area")
    st.pyplot(fig)

    # Vendor distribution by sub-area
    vendor_area_counts = vendor_df['Sub Area'].value_counts()

    # Visualizing vendor distribution by sub-area
    st.subheader("Vendor Distribution by Sub-Area")
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(x=vendor_area_counts.index, y=vendor_area_counts.values, ax=ax, palette="viridis")
    ax.set_xlabel("Sub Area")
    ax.set_ylabel("Number of Vendors")
    ax.set_title("Distribution of Vendors Across Sub Areas")
    st.pyplot(fig)

    # Vendor availability by event month (assuming vendors have monthly activity)
    vendor_month_counts = merged_df.groupby('Budget Category')['Event Month'].value_counts().unstack(fill_value=0)

    # Visualizing vendor distribution by month
    st.subheader("Vendor Distribution by Month")
    fig, ax = plt.subplots(figsize=(12, 6))
    vendor_month_counts.plot(kind='bar', stacked=True, ax=ax, colormap="Accent")
    ax.set_xlabel("Month")
    ax.set_ylabel("Number of Vendors")
    ax.set_title("Vendor Distribution by Month and Budget Category")
    st.pyplot(fig)

    # Merge customer and vendor data to analyze correlation between customer demand and vendor supply
    area_df = merged_df.groupby('Sub Area').agg({
        'Event Month': 'size',  # Number of customer events by Sub Area
        'Business Name': 'nunique'  # Number of unique vendors by Sub Area
    }).rename(columns={'Event Month': 'Event Count', 'Business Name': 'Vendor Count'})

    # Correlation between customer demand and vendor availability by sub-area
    st.subheader("Correlation Between Customer Demand and Vendor Availability by Sub-Area")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.scatterplot(data=area_df, x='Vendor Count', y='Event Count', ax=ax, color='purple')
    ax.set_xlabel("Number of Vendors")
    ax.set_ylabel("Number of Customer Events")
    ax.set_title("Correlation Between Vendor Availability and Customer Demand by Sub Area")
    st.pyplot(fig)

    # Display correlation coefficient
    correlation = area_df['Event Count'].corr(area_df['Vendor Count'])
    st.write(f"Correlation Coefficient: {correlation:.2f}")

    if correlation > 0:
        st.write("There is a positive correlation between vendor availability and customer demand.")
    elif correlation < 0:
        st.write("There is a negative correlation between vendor availability and customer demand.")
    else:
        st.write("There is no correlation between vendor availability and customer demand.")
    



