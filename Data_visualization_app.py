import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="Sales Data Visualization Dashboard",
                   page_icon= ":bar_chart:",
                   layout= "wide"
                   )

@st.cache_data
def get_data_from_excel():
  data_frame = pd.read_excel(
    io = 'supermarkt_sales.xlsx',
    engine = 'openpyxl',
    sheet_name= 'Sales',
    skiprows= 3,
    usecols= 'B:R',
    nrows= 1000,
  )
  # Add 'hour column to the data frame'
  data_frame["hour"] = pd.to_datetime(data_frame["Time"], format = "%H:%M:%S").dt.hour

  return data_frame

data_frame = get_data_from_excel()

# To run the python script in terminal to create the streamlit web app say "streamlit run script_name"
#st.dataframe(data_frame)

# Side bar
st.sidebar.header("Apply Filters:")

city = st.sidebar.multiselect(
  "Sort the city:",
  options = data_frame["City"].unique(),
  default = data_frame["City"].unique()
)

customer_type = st.sidebar.multiselect(
  "Sort Customer types:",
  options = data_frame["Customer_type"].unique(),
  default = data_frame["Customer_type"].unique()
)

gender = st.sidebar.multiselect(
  "Sort Gender:",
  options = data_frame["Gender"].unique(),
  default = data_frame["Gender"].unique()
)

# Adding functionalities to the side bar to filter using the loaded data through pandas
df_selection = data_frame.query(
  "City == @city & Customer_type == @customer_type & Gender == @gender"
)

# Sends filtered data frame to the web app instead of the original data frame
#st.dataframe(df_selection)

# Main Page Key Performance Indicators
st.title(":bar_chart: Sales Data Visualization Dashboard")
st.markdown("##")

# The top KPIs
total_sales = int(df_selection["Total"].sum())
average_rating = round(df_selection["Rating"].mean(),1)
star_rating = ":star:" * int(round(average_rating, 0))
average_sale_by_transaction = round(df_selection["Total"].mean(), 2)

left_column, middle_column, right_column = st.columns(3)
with left_column:
  st.subheader("Total Sales")
  st.subheader(f"US $ {total_sales}")
with middle_column:
  st.subheader("Average rating")
  st.subheader(f"{average_rating} {star_rating}")
with right_column:
  st.subheader("Average sale on transactions")
  st.subheader(f"{average_sale_by_transaction}")

st.markdown("---")

# Building the visualizations 
# Sales by products [Bar Chart]
sales_by_product_line = (
  df_selection.groupby(by=["Product line"])[["Total"]].sum().sort_values(by = "Total")
)

fig_product_sales = px.bar(
  sales_by_product_line,
  x = "Total",
  y = sales_by_product_line.index,
  orientation = "h",
  title = "<b> Sales by Product Line</b>",
  color_discrete_sequence = ["#0083B8"] * len(sales_by_product_line),
  template = "plotly_white",
)

fig_product_sales.update_layout(
  plot_bgcolor = "rgba(0,0,0,0)",
  xaxis = (dict(showgrid = False))
)

# Sales by Hours [Line Chart]
sales_by_hours = df_selection.groupby(by = ["hour"])[["Total"]].sum()
fig_hourly_sales = px.bar(
  sales_by_hours,
  x = sales_by_hours.index,
  y = "Total",
  title = "<b>Sales by hours</b>",
  color_discrete_sequence=["#0083B8"] * len(sales_by_hours),
  template = "plotly_white",
)

fig_hourly_sales.update_layout(
  plot_bgcolor = "rgba(0,0,0,0)",
  xaxis = dict(tickmode = "linear"),
  yaxis = (dict(showgrid = False)),
)

# Charts beside each other
left_column, right_column = st.columns(2)
left_column.plotly_chart(fig_product_sales, use_container_width = True)
right_column.plotly_chart(fig_hourly_sales, use_container_width = True)

# Custom styling 
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """

st.markdown(hide_st_style, unsafe_allow_html = True)