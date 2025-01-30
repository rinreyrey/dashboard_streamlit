import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

def create_daily_orders_df(df):
    daily_orders_df = df.resample(rule='D', on='order_delivered_customer_date').agg({
        "order_id": "nunique"
    })
    daily_orders_df = daily_orders_df.reset_index()
    daily_orders_df.rename(columns={
        "order_id": "order_count"
    }, inplace=True)
    
    return daily_orders_df

def create_sum_order_items_df(df):
    sum_order_items_df = df.groupby("product_category_name_english").order_id.nunique().sort_values(ascending=False).reset_index()
    sum_order_items_df = sum_order_items_df.rename(columns={
    'product_category_name_english': 'product_name',
    'order_id': 'order_sum'
    })
    return sum_order_items_df

def create_bycity_df(df):
    sum_order_cities_df = df.groupby(by="customer_city").order_id.nunique().sort_values(ascending=False).reset_index()
    sum_order_cities_df = sum_order_cities_df.rename(columns={
    'order_id': 'order_sum'
    })
    
    return sum_order_cities_df

main_data_df = pd.read_csv("main_data.csv")

min_date = main_data_df["order_delivered_customer_date"].min()
max_date = main_data_df["order_delivered_customer_date"].max()

main_data_df['order_delivered_customer_date'] = pd.to_datetime(main_data_df['order_delivered_customer_date'])

st.header('Dashboard')
 
with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")
    
    # Mengambil start_date & end_date dari date_input
    date_range = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )
    
if len(date_range) == 2:
    start_date, end_date = date_range
    main_df = main_data_df[(main_data_df["order_delivered_customer_date"] >= str(start_date)) & 
                (main_data_df["order_delivered_customer_date"] <= str(end_date))]
        
    daily_orders_df = create_daily_orders_df(main_df)
    sum_order_items_df = create_sum_order_items_df(main_df)
    sum_order_cities_df = create_bycity_df(main_df)  

    st.subheader('Daily Orders')
 
    col1, col2 = st.columns(2)
 
    with col1:
        total_orders = daily_orders_df.order_count.sum()
        st.metric("Total orders", value=total_orders)

    st.subheader("Best & Worst Performing Product")
 
    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))
 
    colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
 
    sns.barplot(x="order_sum", y="product_name", hue="order_sum", hue_order=sum_order_items_df['order_sum'].head(5), data=sum_order_items_df.head(5), palette=colors, ax=ax[0], legend=False)
    ax[0].set_ylabel(None)
    ax[0].set_xlabel("Number of Sales", fontsize=30)
    ax[0].set_title("Best Performing Product", loc="center", fontsize=50)
    ax[0].tick_params(axis='y', labelsize=35)
    ax[0].tick_params(axis='x', labelsize=30)
 
    sns.barplot(x="order_sum", y="product_name", hue="order_sum", data=sum_order_items_df.sort_values(by="order_sum", ascending=True).head(5), palette=colors, ax=ax[1], legend=False)
    ax[1].set_ylabel(None)
    ax[1].set_xlabel("Number of Sales", fontsize=30)
    ax[1].invert_xaxis()
    ax[1].yaxis.set_label_position("right")
    ax[1].yaxis.tick_right()
    ax[1].set_title("Worst Performing Product", loc="center", fontsize=50)
    ax[1].tick_params(axis='y', labelsize=35)
    ax[1].tick_params(axis='x', labelsize=30)
 
    st.pyplot(fig)

    st.subheader("The City That Buys the Most")

    fig, ax = plt.subplots(figsize=(20, 10))
    colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
    sns.barplot(
        x="order_sum", y="customer_city", hue="order_sum", hue_order=sum_order_cities_df['order_sum'].head(5), data=sum_order_cities_df.head(5), palette=colors, legend=False
    )
    ax.set_title("Number of Customer by Cities", loc="center", fontsize=30)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='y', labelsize=20)
    ax.tick_params(axis='x', labelsize=15)
    st.pyplot(fig)


   