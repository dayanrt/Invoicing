import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Sales CT Dashboard", page_icon=":bar_chart:", 
layout="wide")
df = pd.read_excel(io='CFO03.xlsx', 
engine='openpyxl', 
sheet_name='Sheet1',
skiprows=0,
usecols='A:J',
nrows=19,)
#df['Year'] = df['Invoice date'].dt.year
df['Month'] = df['Expectedpaymentdate'].dt.month_name()
st.sidebar.header("Please Filter Here")
#Contractcurrency = st.sidebar.multiselect("Select the Currency:", options=df["Contractcurrency"].unique(), default=df["Contractcurrency"].unique())
#Account = st.sidebar.multiselect("Select the Account:", options=df["Account"].unique(), default=df["Account"].unique())
#Status = st.sidebar.multiselect("Select the Status:", options=df["Status"].unique(), default=df["Status"].unique())
#Year = st.sidebar.multiselect("Select the Year:", options=df["Year"].unique(), default=df["Year"].unique())
Month = st.sidebar.multiselect("Select the Month:", options=df["Month"].unique(), default=df["Month"].unique())

df_selection = df.query("Month == @Month")

st.dataframe(df_selection)
st.title(":bar_chart CT MX Sales Dashboard")
st.markdown("##")

total_sales1 = int(df_selection["GBP"].sum())
#total_sales2 = int(df_selection["Net amount GBP"].sum())
left_column, right_column = st.columns(2)
with left_column: 
  st.subheader("Total sales:")
  st.subheader(f"GBP {total_sales1:,}")
#with right_column:
#  st.subheader("Net sales:")
#  st.subheader(f"GBP {total_sales2:,}")
st.markdown("---")

#Hasta aquí todo bien

desired = df.select_dtypes(['float64']).columns
cashflow = df_selection.groupby("Month")[desired].sum()[["GBP"]].sort_values(by="Month")

#sales_by_Workorder = (df_selection.groupby(by=["Workorder"]).sum()[["Total amount GBP"]].sort_values(by="Total amount GBP"))
fig_product_income = px.bar(cashflow,orientation="v", title="<b>MX Invoicing</b>", category_orders={"Month": ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]}, 
color=["blue", "blue", "blue"],template="plotly_white")
fig_product_income.add_hline(y=83100, line_width=3, line_dash="dash", line_color="red")
fig_product_income.update_layout(plot_bgcolor="rgba(0,0,0,0)", font=dict(color="black"), yaxis_title="GBP", yaxis=dict(showgrid=True, gridcolor='#cecdcd'), xaxis=dict(showgrid=True, gridcolor='#cecdcd'), height=900)  
fig_product_income.update_layout(showlegend=False)

#fig_account_income = px.pie(df_selection, values = "Total amount GBP", names = "Account", hole =0.5)
#fig_account_income.update_traces(text = df_selection["Account"], textposition= "outside")
#fig1 = go.Figure(go.Indicator(domain = {'x': [0, 1], 'y': [0, 1]}, value = int(df_selection["Total amount GBP"].sum()), mode = "gauge+number+delta", title = {'text': "Sales target; Breakeven: 2M"}, delta = {'reference': 2000000, "prefix": "2M;"}, gauge = {'axis': {'range': [None, 4000000]},'steps' : [{'range': [0, 1500000], 'color': "tomato"},{'range': [1500000, 2500000], 'color': "orange"}],'threshold' : {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 3500000}}))
left_column, right_column = st.columns(2)
left_column.plotly_chart(fig_product_income, use_container_width=True)
#with right_column:
#  right_column.plotly_chart(fig_account_income, use_container_width=True)
#  right_column.plotly_chart(fig1, use_container_width=True)
st.markdown("---")
