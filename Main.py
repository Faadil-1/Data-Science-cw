import streamlit as st
import plotly.express as px
import pandas as pd
import os
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="Minger Dashboard", page_icon=":rocket:",layout="wide")

st.title(" :bulb: DASHBOARD FOR MINGER STORE")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>',unsafe_allow_html=True)

os.chdir(r"C:\Users\Faadil\Data Science Individual cw")
df = pd.read_csv("Global_Superstore_Lite.csv", encoding = "ISO-8859-1")
mba = pd.read_csv("MBA_Results.csv", encoding = "ISO-8859-1")

col1, col2 = st.columns((2))
df["Order Date"] = pd.to_datetime(df["Order Date"])

# Getting the min and max date 
startDate = pd.to_datetime(df["Order Date"]).min()
endDate = pd.to_datetime(df["Order Date"]).max()

with col1:
    date1 = pd.to_datetime(st.date_input("Start Date", startDate))

with col2:
    date2 = pd.to_datetime(st.date_input("End Date", endDate))

df = df[(df["Order Date"] >= date1) & (df["Order Date"] <= date2)].copy()


st.sidebar.header("Choose your filter: ")
# Create for Region
region = st.sidebar.multiselect("Pick your Region", df["Region"].unique())
if not region:
    df2 = df.copy()
else:
    df2 = df[df["Region"].isin(region)]

# Create for Country
country = st.sidebar.multiselect("Pick the Country", df2["Country"].unique())
if not country:
    df3 = df2.copy()
else:
    df3 = df2[df2["Country"].isin(country)]

# Create for Ship Mode
ship_mode = st.sidebar.multiselect("Pick the Mode of Shipping",df3["Ship Mode"].unique())
if not ship_mode:
    df4 = df3.copy()
else:
    df4 = df3[df3["Ship Mode"].isin(ship_mode)]

# Create for Order Priority
order_priority = st.sidebar.multiselect("Pick the Priority of Order", df4["Order Priority"].unique())
if not order_priority:
    filtered_df = df4.copy()
else:
    filtered_df = df4[df4["Order Priority"].isin(order_priority)]

    
category_df = filtered_df.groupby(by = ["Category"], as_index = False)["Sales"].sum()


with col1:
    st.subheader("Category wise Sales")
    fig = px.bar(category_df, x = "Category", y = "Sales", text = ['${:,.2f}'.format(x) for x in category_df["Sales"]],
                 template = "presentation")
    st.plotly_chart(fig,use_container_width=True, height = 200)

with col2:
    st.subheader('Segment wise Sales')
    fig = px.pie(filtered_df, values = "Sales", names = "Segment", template = "plotly_dark")
    fig.update_traces(text = filtered_df["Segment"], textposition = "inside")
    st.plotly_chart(fig,use_container_width=True)

        
filtered_df["month_year"] = filtered_df["Order Date"].dt.to_period("M")
st.subheader('Average Profit over Time')

linechart = pd.DataFrame(filtered_df.groupby(filtered_df["month_year"].dt.strftime("%Y : %b"))["Profit"].mean()).reset_index()
fig2 = px.line(linechart, x = "month_year", y="Profit", labels = {"Profit": "Profit"}, height=500, width=1000, template="gridon")
st.plotly_chart(fig2,use_container_width=True)


st.subheader('Region wise Sales by Category')
bar_chart = px.bar(filtered_df, x='Region', y='Sales', labels={'Region': 'Region', 'Sales': 'Sales'}, height=500, width=1000, color='Category')
st.plotly_chart(bar_chart)


# Create a scatter plot
st.subheader('Profit vs Sales by Category')
data1 = px.scatter(filtered_df, x = "Sales", y = "Profit", size = "Quantity", color = "Category")
data1['layout'].update(xaxis = dict(title="Sales",titlefont=dict(size=19)),
                       yaxis = dict(title = "Profit", titlefont = dict(size=19)))
data1.add_hline(y=0, line=dict(color="black", dash="solid"))
st.plotly_chart(data1,use_container_width=True)


#Create a heatmap for Market Basket Analysis Results
st.set_option('deprecation.showPyplotGlobalUse', False)
st.subheader('Market Basket Analysis Heatmap')
pivot_table = pd.pivot_table(mba, index='antecedents', columns='consequents', values='lift')  
sns.heatmap(pivot_table, annot=True, cmap='coolwarm', fmt='g')
st.pyplot()
    
