
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
# Function to load default data
@st.cache_data
def load_default_data():
    return pd.read_excel(
        r'C:\Users\Extreme\OneDrive\Desktop\streamlit  dashboards\labour productivity\Labor_Productivity_Analytics_Dataset.xlsx',
        sheet_name='Sheet1',
        engine='openpyxl'
    )

# Function to load uploaded files (supports Excel and CSV)
def load_uploaded_file(uploaded_file):
    try:
        if uploaded_file.name.endswith('.xlsx'):
            return pd.read_excel(uploaded_file, engine='openpyxl')
        elif uploaded_file.name.endswith('.csv'):
            return pd.read_csv(uploaded_file)
        else:
            st.sidebar.error("Unsupported file type! Please upload an Excel or CSV file.")
            st.stop()
    except Exception as e:
        st.sidebar.error(f"Error loading file: {e}")
        st.stop()

# Sidebar for file upload or default dataset
st.sidebar.title("Upload or Load Dataset")

data_source = st.sidebar.radio(
    "Choose Data Source:",
    ("Default Dataset", "Upload Your Own Dataset")
)

# Load dataset based on user input
if data_source == "Default Dataset":
    data = load_default_data()
    st.sidebar.success("Default dataset loaded successfully!")
else:
    uploaded_file = st.sidebar.file_uploader("Upload an Excel or CSV file", type=['xlsx', 'csv'])

    if uploaded_file is not None:
        data = load_uploaded_file(uploaded_file)
        st.sidebar.success("Dataset uploaded successfully!")
    else:
        st.sidebar.warning("Please upload a dataset to proceed.")
        st.stop()


# Refresh Button
if st.button("Refresh Dashboard"):
    st.experimental_set_query_params()

# Tooltip Message
tooltip_message = (
    "The dataset is a working process. You cannot open the Excel file directly, "
    "and no modifications can be made. You can only add data to existing columns, "
    "and you cannot change the column names."
)
st.markdown(
    f'<span style="color: grey; font-size: 12px; text-decoration: underline;">{tooltip_message}</span>',
    unsafe_allow_html=True
)
# Sidebar setup
st.sidebar.title("Labor Productivity Dashboard")
analysis_choice = st.sidebar.radio(
    "Select Analysis Category:",
    ["Labor Productivity Analytics", "Parameters for Analytics", "Visual Themes of Labor Productivity"]
)

# Sidebar options for selecting metrics
if analysis_choice == "Labor Productivity Analytics":
    metric = st.sidebar.radio(
        "Select Metric:",
        [
            "Labor Presence at Machine (within Zone)",
            "Labor Total Produced Output",
            "Productivity (90% target achieved with 90% presence)",
            "Labor Target Productivity",
            "Labor Efficiency Rate",
            "Productivity Zone - Green (90%+), Yellow (80%-90%), Red (<80%)",
            "Labor Anomaly Conduct"
        ]
    )
elif analysis_choice == "Parameters for Analytics":
    parameter = st.sidebar.radio(
        "Select Parameter:",
        [
            "Product",
            "Department",
            "Shift",
            "Time Intervals (Week, Month, Year)",
            "Manager",
            "Factory Units",
            "Machine Unit"
        ]
    )
elif analysis_choice == "Visual Themes of Labor Productivity":
    theme = st.sidebar.radio(
        "Select Theme:",
        [
            "Productivity Pulse",
            "Department Dynamics",
            "Productivity Panorama",
            "Target Tracker",
            "Shift Synergy",
            "Efficiency Compass",
            "Productivity Evolution"
        ]
    )




# Sidebar filter section
st.sidebar.header("Filters")

# Separate Date filters
start_date = st.sidebar.date_input("Start Date", data['Date'].min())
end_date = st.sidebar.date_input("End Date", data['Date'].max())

# Other filters
product_type = st.sidebar.multiselect("Select Product Type", options=data['Product_Type'].unique())
department = st.sidebar.multiselect("Select Department", options=data['Department'].unique())
shift = st.sidebar.multiselect("Select Shift", options=data['Shift'].unique())
manager = st.sidebar.multiselect("Select Manager", options=data['Manager'].unique())
factory_unit = st.sidebar.multiselect("Select Factory Unit", options=data['Factory_Unit'].unique())
machine_unit = st.sidebar.multiselect("Select Machine Unit", options=data['Machine_Unit'].unique())
productivity_zone = st.sidebar.multiselect("Select Productivity Zone", options=data['Productivity_Zone'].unique())
anomaly_conduct = st.sidebar.multiselect("Select Anomaly Conduct", options=data['Anomaly_Conduct'].unique())

# Efficiency rate slider
efficiency_rate = st.sidebar.slider(
    "Select Labor Efficiency Rate",
    min_value=float(data['Labor_Efficiency_Rate'].min()),
    max_value=float(data['Labor_Efficiency_Rate'].max()),
    value=(float(data['Labor_Efficiency_Rate'].min()), float(data['Labor_Efficiency_Rate'].max()))
)

# Apply filters
filtered_data = data[
    (data['Date'] >= pd.to_datetime(start_date)) &
    (data['Date'] <= pd.to_datetime(end_date)) &
    (data['Product_Type'].isin(product_type) if product_type else True) &
    (data['Department'].isin(department) if department else True) &
    (data['Shift'].isin(shift) if shift else True) &
    (data['Manager'].isin(manager) if manager else True) &
    (data['Factory_Unit'].isin(factory_unit) if factory_unit else True) &
    (data['Machine_Unit'].isin(machine_unit) if machine_unit else True) &
    (data['Productivity_Zone'].isin(productivity_zone) if productivity_zone else True) &
    (data['Anomaly_Conduct'].isin(anomaly_conduct) if anomaly_conduct else True) &
    (data['Labor_Efficiency_Rate'].between(efficiency_rate[0], efficiency_rate[1]))
]
color_palette = px.colors.qualitative.Set1
color_palette2 = px.colors.qualitative.Set1_r # Using a vibrant color palette


# Generate charts based on selected options
if analysis_choice == "Labor Productivity Analytics":
    st.title("Labor Productivity Analytics Dashboard")
    if metric == "Labor Presence at Machine (within Zone)":
        # 1. Labor Presence at Machine (within Zone)
        st.subheader("Labor Presence at Machine (within Zone)")

        # 1. Bar Chart - Labor Presence by Productivity Zone and Shift
        presence_chart = px.bar(
            filtered_data,
            x='Productivity_Zone',
            y='Labor_Presence',
            color='Shift',
            barmode='group',
            title="Labor Presence by Productivity Zone and Shift",

        )
        presence_chart.update_layout(
            font=dict(color="white"),  # White font for visibility
            xaxis_title="Productivity Zone",
            yaxis_title="Labor Presence (hrs)"
        )
        # Adding a white outline to bars for emphasis
        presence_chart.update_traces()
        st.plotly_chart(presence_chart)

        # 2. Stacked Bar Chart - Labor Presence by Shift and Machine Unit
        presence_data = filtered_data.groupby(['Shift', 'Machine_Unit'])['Labor_Presence'].sum().reset_index()

        fig1 = px.bar(
            presence_data,
            x='Shift',
            y='Labor_Presence',
            color='Machine_Unit',
            title="Labor Presence by Shift and Machine Unit",
            labels={"Labor_Presence": "Presence Time", "Shift": "Shift"},
            color_discrete_sequence=color_palette
        )
        fig1.update_layout(
            font=dict(color="white"),
            xaxis_title="Shift",
            yaxis_title="Total Presence Time (hrs)"
        )
        # White outline for stacked bars
        fig1.update_traces()
        st.plotly_chart(fig1)

        # 3. Line Chart - Average Labor Presence by Day and Shift
        filtered_data['Day_of_Week'] = filtered_data['Date'].dt.day_name()
        average_presence_data = filtered_data.groupby(['Day_of_Week', 'Shift'])['Labor_Presence'].mean().reset_index()

        fig2 = px.line(
            average_presence_data,
            x='Day_of_Week',
            y='Labor_Presence',
            color='Shift',
            title="Average Labor Presence by Day and Shift",
            color_discrete_sequence=color_palette
        )
        fig2.update_layout(
            font=dict(color="white"),
            xaxis_title="Day of Week",
            yaxis_title="Avg Presence Time (hrs)"
        )
        # White outline for line chart markers
        fig2.update_traces(marker=dict(line=dict(color="white", width=1.5)))
        st.plotly_chart(fig2)



    elif metric == "Labor Total Produced Output":
        st.subheader("Labor Total Produced Output Over Time")

        # Chart 2: Department Comparison (Grouped Bar Chart)
        fig1= px.bar(filtered_data, x='Department', y='Labor_Total_Output', color='Shift',
                      title='Labor Total Output by Department and Shift', barmode='group')
        st.plotly_chart(fig1)



        # Chart 4: Monthly Aggregated Output by Department (Bar Chart)
        filtered_data['Month'] = filtered_data['Date'].dt.to_period("M").dt.to_timestamp()
        monthly_data = filtered_data.groupby(['Month', 'Department'])['Labor_Total_Output'].sum().reset_index()

        fig4 = px.bar(monthly_data, x='Month', y='Labor_Total_Output', color='Department',
                      title='Monthly Total Produced Output by Department',
                      labels={"Labor_Total_Output": "Total Output"})
        st.plotly_chart(fig4)
        # Chart 1: Box Plot by Department and Shift
        fig1 = px.box(filtered_data, x='Department', y='Labor_Total_Output', color='Shift',
                      title='Output Distribution by Department and Shift')
        st.plotly_chart(fig1)

        # Chart 2: Grouped Bar Chart by Factory Unit and Department
        fig2 = px.bar(filtered_data, x='Factory_Unit', y='Labor_Total_Output', color='Department',
                      title='Labor Total Output by Factory Unit and Department', barmode='group',
                      labels={"Labor_Total_Output": "Total Output"})
        st.plotly_chart(fig2)


        # Chart 1: Bar Chart by Factory Unit and Productivity Zone with Zone Colors
        zone_colors = {'Low': 'red', "Yellow": "#FFFF8F", 'High': 'green'}

        # Chart 2: Box Plot by Factory Unit and Productivity Zone
        fig2 = px.box(
            filtered_data,
            x='Factory_Unit',
            y='Labor_Total_Output',
            color='Productivity_Zone',
            title='Output Distribution by Factory Unit and Productivity Zone',
            color_discrete_map=zone_colors,
            labels={"Labor_Total_Output": "Total Output"}
        )
        st.plotly_chart(fig2)


    elif metric == "Productivity (90% target achieved with 90% presence)":



        # Visualization 2: Average Labor Presence by Product Type (Bar Chart)
        st.subheader("Average Labor Presence by Product Type")
        average_presence = filtered_data.groupby('Product_Type')['Labor_Presence'].mean().reset_index()
        fig_presence_product = px.bar(
            average_presence,
            x='Product_Type',
            y='Labor_Presence',
            color='Product_Type',
            title="Average Labor Presence by Product Type",
            labels={'Labor_Presence': 'Average Labor Presence (%)'},
            color_discrete_sequence=px.colors.qualitative.Safe
        )
        st.plotly_chart(fig_presence_product, use_container_width=True)


        # Visualization 3: Productivity by Shift
        st.subheader("Productivity by Shift")
        fig_productivity_shift = px.bar(
            filtered_data,
            x='Shift',
            y='Productivity',
            title="Productivity by Shift",
            color='Shift',
            labels={'Productivity': 'Productivity (%)'},
            color_discrete_sequence = px.colors.qualitative.Set3
        )
        st.plotly_chart(fig_productivity_shift, use_container_width=True)




    elif metric == "Labor Target Productivity":
        # Calculate Labor Target Productivity
        filtered_data['Labor_Target_Productivity'] = (filtered_data['Labor_Total_Output'] / filtered_data[
            'Labor_Target_Output']) * 100
        # 4. Labor Target Productivity Comparison
        st.subheader("Labor Output vs Target Output")
        target_chart = px.bar(
            filtered_data,
            x='Department',
            y=['Labor_Total_Output', 'Labor_Target_Output'],
            barmode='group',
            title="Comparison of Actual Output vs Target Output"
        )
        st.plotly_chart(target_chart)

        # Additional Plot: Productivity by Shift and Department
        fig2 = px.bar(filtered_data, x='Shift', y=['Labor_Total_Output', 'Labor_Target_Output'] ,
                      title='Labor Target Productivity by Shift',
                      labels={'Labor_Target_Productivity': 'Labor Target Productivity (%)', 'Shift': 'Shift'},
                      barmode='group')
        fig2.update_layout(xaxis_title='Shift', yaxis_title='Labor Target Productivity (%)')
        st.plotly_chart(fig2)
        # Additional Plot: Productivity by Shift and Department
        fig2 = px.bar(filtered_data, x='Productivity_Zone', y=['Labor_Total_Output', 'Labor_Target_Output'] ,
                      title='Labor Target Productivity by Productivity Zone ',
                      labels={'Labor_Target_Productivity': 'Labor Target Productivity (%)', 'Shift': 'Shift'},
                      barmode='group')
        fig2.update_layout(xaxis_title='Shift', yaxis_title='Labor Target Productivity (%)')
        st.plotly_chart(fig2)# Additional Plot: Productivity by Shift and Department
        fig2 = px.bar(filtered_data, x='Labor_Efficiency_Rate', y=['Labor_Total_Output', 'Labor_Target_Output'] ,
                      title='Labor Target Productivity by Shift and Department',
                      labels={'Labor_Target_Productivity': 'Labor Target Productivity (%)', 'Shift': 'Shift'},
                      barmode='group')
        fig2.update_layout(xaxis_title='Shift', yaxis_title='Labor Target Productivity (%)')
        st.plotly_chart(fig2)

    elif metric == "Labor Efficiency Rate":


        # Create a separate DataFrame for resampled weekly data
        weekly_data = filtered_data[['Date', 'Labor_Efficiency_Rate']].copy()
        weekly_data['Date'] = pd.to_datetime(weekly_data['Date'])
        weekly_data = weekly_data.set_index('Date').resample('W').mean().reset_index()

        # Plotting the resampled time series chart
        st.subheader("Labor Efficiency Rate Over Time (Weekly Average)")
        fig = px.line(
            weekly_data,
            x='Date',
            y='Labor_Efficiency_Rate',

            title="Labor Efficiency Rate Over Time (Weekly Average)",
            labels={'Labor_Efficiency_Rate': 'Efficiency Rate', 'Date': 'Date'}
        )
        st.plotly_chart(fig)



        # 2. Bar Chart for Labor Efficiency Rate by Product Type
        st.subheader("Labor Efficiency Rate by Product Type")
        fig = px.bar(
            filtered_data,
            x='Product_Type',
            y='Labor_Efficiency_Rate',
            title="Labor Efficiency Rate by Product Type",
            labels={'Labor_Efficiency_Rate': 'Efficiency Rate', 'Product_Type': 'Product Type'},
            color='Product_Type'
        )
        st.plotly_chart(fig)

        # 4. Box Plot for Labor Efficiency Rate across Departments
        st.subheader("Labor Efficiency Rate Across Departments")
        fig = px.box(
            filtered_data,
            x='Department',
            y='Labor_Efficiency_Rate',
            title="Efficiency Rate Distribution by Department",
            labels={'Labor_Efficiency_Rate': 'Efficiency Rate', 'Department': 'Department'},
            color='Department'
        )
        st.plotly_chart(fig)

    elif metric == "Productivity Zone - Green (90%+), Yellow (80%-90%), Red (<80%)":

        # 1. Stacked Bar Chart for Productivity Zones by Department
        st.subheader("Productivity Zone Distribution by Department")
        fig = px.histogram(
            filtered_data,
            x='Department',
            color='Productivity_Zone',
            title="Productivity Zone Distribution by Department",
            labels={'Productivity_Zone': 'Zone', 'Department': 'Department'},
            barmode='stack',
            color_discrete_map={'Green': 'green', 'Yellow': 'yellow', 'Red': 'red'}
        )
        st.plotly_chart(fig)

        # 2. Pie Chart for Overall Productivity Zone Distribution
        st.subheader("Overall Productivity Zone Distribution")
        zone_colors = {'Low': 'red', 'Yellow': '#FFFF8F', 'High': 'green'}
        fig3 = px.pie(
            filtered_data,
            names='Productivity_Zone',
            title='Productivity Zone Distribution',
            color='Productivity_Zone',
            color_discrete_map=zone_colors,
            hole=0.3
        )
        st.plotly_chart(fig3)

        # 3. Time Series Area Chart for Productivity Zones Over Time
        # Aggregate the count of each productivity zone by week
        time_zone_data = filtered_data.groupby(
            [filtered_data['Date'].dt.to_period('W'), 'Productivity_Zone']).size().unstack(fill_value=0).reset_index()
        time_zone_data['Date'] = time_zone_data['Date'].dt.start_time  # Convert to timestamp for plotting

        st.subheader("Productivity Zone Trends Over Time (Weekly)")
        fig = px.area(
            time_zone_data,
            x='Date',
            y=['Green', 'Yellow', 'Red'],
            title="Weekly Productivity Zone Trends",
            labels={'value': 'Count', 'Date': 'Date'},
            color_discrete_map={'Green': 'green', 'Yellow': 'yellow', 'Red': 'red'}
        )
        st.plotly_chart(fig)



    elif metric == "Labor Anomaly Conduct":
        st.subheader("Labor Anomaly Conduct")
        anomaly_chart = px.bar(
            filtered_data,
            x='Anomaly_Conduct',
            title="Instances of Labor Anomaly Conduct",
            color='Shift'
        )
        st.plotly_chart(anomaly_chart)
        fig = px.bar(
            filtered_data,
            x="Date",
            color="Anomaly_Conduct",
            title="Labor Anomalies by Date and Shift",

            labels={"Anomaly_Conduct": "Type of Anomaly", "count": "Frequency"}
        )

        st.plotly_chart(fig)
        

        st.subheader("Anomaly Distribution by Department")
        fig_dept = px.bar(
            filtered_data,
            x="Anomaly_Conduct",
            color="Department",
            title="Anomalies by Department",
            labels={"Anomaly_Conduct": "Type of Anomaly"},

        )

        st.plotly_chart(fig_dept)

        # Visualization: Anomaly Distribution by Factory Unit
        st.subheader("Anomaly Distribution by Factory Unit")
        fig_factory = px.bar(
            filtered_data,
            x="Anomaly_Conduct",
            color="Factory_Unit",
            title="Anomalies by Factory Unit",
            labels={"Anomaly_Conduct": "Type of Anomaly"},

        )

        st.plotly_chart(fig_factory)


        fig = px.scatter(
            filtered_data,
            x="Labor_Presence",
            y="Anomaly_Conduct",
            color="Anomaly_Conduct",
            title="Labor Presence vs. Anomalies",
            labels={"Labor_Presence": "Labor Presence (%)", "Anomaly_Conduct": "Type of Anomaly"}
        )

        st.plotly_chart(fig)


elif analysis_choice == "Parameters for Analytics":
    st.title("Labor Productivity Analytics by Parameters")
    if parameter == "Product":

        # Top 5 Products by Sales and Profit
        top_products = filtered_data.groupby('Product_Type').agg({
            'Labor_Total_Output': 'sum',
            'Labor_Target_Output': 'sum',
            'Productivity': 'mean',
            'Labor_Efficiency_Rate': 'mean'
        }).sort_values(by='Labor_Total_Output', ascending=False).head(5).reset_index()

        st.header("Top 5 Products by Sales and Profit")
        fig1 = px.bar(top_products, x='Product_Type', y=['Labor_Total_Output', 'Labor_Target_Output'],
                      title="Top 5 Products by Sales and Profit",
                      labels={'value': 'Output (Units)', 'Product_Type': 'Product Type'},
                      barmode='group')
        st.plotly_chart(fig1)

        # Bottom 5 Products by Sales and Profit
        bottom_products = filtered_data.groupby('Product_Type').agg({
            'Labor_Total_Output': 'sum',
            'Labor_Target_Output': 'sum',
            'Productivity': 'mean',
            'Labor_Efficiency_Rate': 'mean'
        }).sort_values(by='Labor_Total_Output', ascending=True).head(5).reset_index()

        st.header("Bottom 5 Products by Sales and Profit")
        fig2 = px.bar(bottom_products, x='Product_Type', y=['Labor_Total_Output', 'Labor_Target_Output'],
                      title="Bottom 5 Products by Sales and Profit",
                      labels={'value': 'Output (Units)', 'Product_Type': 'Product Type'},
                      barmode='group')
        st.plotly_chart(fig2)

        # Profit by Department
        st.header("Profit by Department")
        profit_department =filtered_data.groupby('Department').agg({
            'Labor_Total_Output': 'sum',
            'Labor_Target_Output': 'sum',
            'Labor_Efficiency_Rate': 'mean',
            'Productivity': 'mean'
        }).reset_index()

        fig3 = px.bar(profit_department, x='Department', y=['Labor_Total_Output', 'Labor_Target_Output'],
                      title="Profit by Department",
                      labels={'value': 'Output (Units)', 'Department': 'Department'},
                      barmode='group')
        st.plotly_chart(fig3)
        st.subheader("Productivity by Product Type")
        product_chart = px.bar(
            filtered_data,
            x='Product_Type',
            y='Labor_Total_Output',
            color='Product_Type',
            title="Labor Total Output by Product Type"
        )
        st.plotly_chart(product_chart)

        # Visualization 1: Sales by Product Over Time
        st.subheader("Sales by Product Over Time")
        fig_sales_product_time = px.bar(
            filtered_data,
            x='Date',
            y='Labor_Total_Output',
            color='Product_Type',
            title="Sales by Product Over Time",
            labels={'Labor_Total_Output': 'Total Output'},
            color_discrete_sequence=px.colors.qualitative.Vivid
        )
        st.plotly_chart(fig_sales_product_time, use_container_width=True)

        # Visualization 2: Productivity by Product and Zone
        st.subheader("Productivity by Product Type and Zone")
        fig_productivity_zone = px.bar(
            filtered_data,
            x='Product_Type',
            y='Productivity',
            color='Productivity_Zone',
            title="Productivity by Product Type and Zone",
            labels={'Productivity': 'Productivity (%)'},
            color_discrete_map={'Green': 'green', 'Yellow': 'yellow', 'Red': 'red'}
        )
        st.plotly_chart(fig_productivity_zone, use_container_width=True)

        # Visualization 3: Average Labor Presence by Department for Each Product
        st.subheader("Average Labor Presence by Department for Each Product Type")
        avg_presence_department = filtered_data.groupby(['Product_Type', 'Department'])[
            'Labor_Presence'].mean().reset_index()
        fig_presence_department = px.bar(
            avg_presence_department,
            x='Product_Type',
            y='Labor_Presence',
            color='Department',
            title="Average Labor Presence by Department for Each Product Type",
            labels={'Labor_Presence': 'Average Labor Presence (%)'},
            color_discrete_sequence=px.colors.qualitative.Bold
        )
        st.plotly_chart(fig_presence_department, use_container_width=True)

        # Visualization 4: Productivity by Product Type in Different Factory Units
        st.subheader("Productivity by Product Type in Different Factory Units")
        fig_productivity_factory = px.bar(
            filtered_data,
            x='Factory_Unit',
            y='Productivity',
            color='Product_Type',
            title="Productivity by Product Type in Different Factory Units",
            labels={'Productivity': 'Productivity (%)'},
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        st.plotly_chart(fig_productivity_factory, use_container_width=True)

        # Visualization 5: Productivity Distribution by Shift and Product Type
        st.subheader("Productivity Distribution by Shift and Product Type")
        fig_productivity_shift = px.box(
            filtered_data,
            x='Shift',
            y='Productivity',
            color='Product_Type',
            title="Productivity Distribution by Shift and Product Type",
            labels={'Productivity': 'Productivity (%)'},
            color_discrete_sequence=px.colors.qualitative.Safe
        )
        st.plotly_chart(fig_productivity_shift, use_container_width=True)

    elif parameter == "Department":
        # 2. Department - Productivity by Department
        st.subheader("Productivity by Department")
        department_chart = px.bar(
            filtered_data,
            x='Department',
            y=['Labor_Total_Output', 'Labor_Target_Output'],
            barmode='group',
            title="Labor Output vs Target Output by Department"
        )
        st.plotly_chart(department_chart)

        # 1. Overall Productivity by Department
        st.header("Overall Productivity by Department")
        fig1 = px.bar(filtered_data, x='Department', y='Productivity', color='Department',
                      title="Productivity by Department")
        st.plotly_chart(fig1)

        # 3. Total Output by Department and Product Type
        st.header("Total Output by Department and Product Type")
        fig3 = px.bar(filtered_data, x='Department', y='Labor_Total_Output', color='Product_Type', barmode='group',
                      title="Total Output by Department and Product Type")
        st.plotly_chart(fig3)

        # 4. Productivity Zone Distribution by Department
        st.header("Productivity Zone Distribution by Department")
        fig4 = px.histogram(filtered_data, x='Department', color='Productivity_Zone',
                            title="Productivity Zone Distribution by Department",
                            color_discrete_map={'Green': 'green', 'Yellow': 'yellow', 'Red': 'red'})
        st.plotly_chart(fig4)

        # 5. Efficiency Rate by Department
        st.header("Efficiency Rate by Department")
        fig5 = px.box(filtered_data, x='Department', y='Labor_Efficiency_Rate', color='Department',
                      title="Efficiency Rate by Department")
        st.plotly_chart(fig5)
    elif parameter == "Shift":

        # 1. Productivity by Shift
        st.header("Productivity by Shift")
        fig1 = px.bar(filtered_data, x='Shift', y='Productivity', color='Shift', title="Overall Productivity by Shift")
        st.plotly_chart(fig1)


        # 3. Output by Shift and Product Type
        st.header("Output by Shift and Product Type")
        fig3 = px.bar(filtered_data, x='Shift', y='Labor_Total_Output', color='Product_Type', barmode='group',
                      title="Total Output by Shift and Product Type")
        st.plotly_chart(fig3)

        # 4. Productivity Zone Distribution by Shift
        st.header("Productivity Zone Distribution by Shift")
        fig4 = px.histogram(filtered_data, x='Shift', color='Productivity_Zone',
                            title="Productivity Zone Distribution by Shift")
        st.plotly_chart(fig4)
        st.subheader("Productivity by Shift")
        shift_chart = px.bar(
            filtered_data,
            x='Shift',
            y='Productivity',
            color='Productivity_Zone',
            title="Average Productivity by Shift",
            color_discrete_map={'Green': 'green', 'Yellow': 'yellow', 'Red': 'red'}
        )
        st.plotly_chart(shift_chart)
    elif parameter == "Time Intervals (Week, Month, Year)":

        # Assuming 'data' is already loaded with necessary columns
        data['Date'] = pd.to_datetime(data['Date'])
        data['Week'] = data['Date'].dt.isocalendar().week
        data['Month'] = data['Date'].dt.month
        data['Year'] = data['Date'].dt.year

        # Sidebar filter for time interval selection
                # Filtered data setup for the chosen time interval
        time_interval = st.selectbox("Choose Interval", ["Weekly", "Monthly", "Yearly"])

        # Group the filtered data based on the selected time interval
        if time_interval == "Weekly":
            filtered_data['Week'] = filtered_data['Date'].dt.isocalendar().week
            interval_data = filtered_data.groupby('Week').mean(numeric_only=True).reset_index()
            x_column = 'Week'
        elif time_interval == "Monthly":
            filtered_data['Month'] = filtered_data['Date'].dt.month
            interval_data = filtered_data.groupby('Month').mean(numeric_only=True).reset_index()
            x_column = 'Month'
        else:  # Yearly
            filtered_data['Year'] = filtered_data['Date'].dt.year
            interval_data = filtered_data.groupby('Year').mean(numeric_only=True).reset_index()
            x_column = 'Year'



        # 1. Productivity Trends over Selected Interval
        st.header(f"Productivity Trends ({time_interval})")
        fig1 = px.line(
            interval_data,
            x=x_column,
            y='Productivity',
            title=f"Productivity Trends ({time_interval})",
            markers=True
        )
        st.plotly_chart(fig1)

        # 2. Total Output by Time Interval with a single color
        st.header(f"Total Output by {time_interval}")
        fig2 = px.bar(
            interval_data,
            x=x_column,
            y='Labor_Total_Output',
            title=f"Total Output by {time_interval}",
            color='Labor_Total_Output',
            color_discrete_sequence=['#2ca02c']  # Use a single color without specifying continuous scale
        )
        st.plotly_chart(fig2)

        # 3. Productivity Zone Distribution by Month (only for Monthly analysis)
        if time_interval == "Monthly":
            st.header("Productivity Zone Distribution by Month")
            fig3 = px.histogram(
                data,
                x='Month',
                color='Productivity_Zone',
                title="Productivity Zone Distribution by Month"
            )
            st.plotly_chart(fig3)

        # 4. Efficiency Rate by Time Interval
        st.header(f"Efficiency Rate ({time_interval})")
        fig4 = px.box(
            data,
            x=x_column,
            y='Labor_Efficiency_Rate',
            title=f"{time_interval} Efficiency Rate",
            color_discrete_sequence=['#1f77b4']
        )
        st.plotly_chart(fig4)

        # 5. Productivity Chart with Anomaly Overlays
        st.header(f"Productivity Trends with Anomaly Overlays ({time_interval})")
        fig5 = px.line(
            interval_data,
            x=x_column,
            y='Productivity',
            title=f"{time_interval} Productivity with Anomaly Indicators",
            markers=True,
            labels={x_column: x_column, "Productivity": "Productivity (%)"}
        )

        # Overlay anomaly markers on the line chart
        fig5.add_scatter(
            x=data[data['Anomaly_Conduct'].notna()][x_column],
            y=data[data['Anomaly_Conduct'].notna()]['Productivity'],
            mode='markers',
            marker=dict(color='red', size=10, symbol='x'),
            name='Anomalies'
        )

        # Update layout for a clean look
        fig5.update_layout(
            xaxis_title=x_column,
            yaxis_title="Productivity (%)",
            plot_bgcolor="rgba(0,0,0,0)",  # Transparent background
            paper_bgcolor="rgba(0,0,0,0)"
        )

        # Display the chart with anomaly overlays
        st.plotly_chart(fig5)


        # 3. Productivity Zone Distribution by Month (only for Monthly analysis)
        if time_interval == "Monthly":
            st.header("Productivity Zone Distribution by Month")
            fig3 = px.scatter(data, x='Month', color='Productivity_Zone',
                                title="Productivity Zone Distribution by Month",color_discrete_map={'Green': 'green', 'Yellow': 'yellow', 'Red': 'red'})
            st.plotly_chart(fig3)

        # 4. Monthly Efficiency Rate (only for Monthly analysis)
        if time_interval == "Monthly":
            st.header("Monthly Efficiency Rate")
            fig4 = px.box(data, x='Month', y='Labor_Efficiency_Rate', title="Monthly Efficiency Rate",
                          color_discrete_sequence=['#1f77b4'])
            st.plotly_chart(fig4)



    elif parameter == "Manager":

        # 1. Overall Productivity by Manager
        st.header("Overall Productivity by Manager")
        fig1 = px.bar(filtered_data, x='Manager', y='Productivity', color='Manager', title="Productivity by Manager")
        st.plotly_chart(fig1)



        # 3. Total Output by Manager and Product Type
        st.header("Total Output by Manager and Product Type")
        fig3 = px.bar(filtered_data, x='Manager', y='Labor_Total_Output', color='Product_Type', barmode='group',
                      title="Total Output by Manager and Product Type")
        st.plotly_chart(fig3)

        # 4. Productivity Zone Distribution by Manager
        st.header("Productivity Zone Distribution by Manager")
        fig4 = px.histogram(filtered_data, x='Manager', color='Productivity_Zone',
                            title="Productivity Zone Distribution by Manager")
        st.plotly_chart(fig4)

        # 5. Efficiency Rate by Manager
        st.header("Efficiency Rate by Manager")
        fig5 = px.box(filtered_data, x='Manager', y='Labor_Efficiency_Rate', color='Manager',
                      title="Efficiency Rate by Manager")
        st.plotly_chart(fig5)

    elif parameter == "Factory Units":

        # 1. Overall Productivity by Factory Unit
        st.header("Overall Productivity by Factory Unit")
        fig1 = px.bar(filtered_data, x='Factory_Unit', y='Productivity', color='Factory_Unit',
                      title="Productivity by Factory Unit")
        st.plotly_chart(fig1)



        # 3. Total Output by Factory Unit and Product Type
        st.header("Total Output by Factory Unit and Product Type")
        fig3 = px.bar(filtered_data, x='Factory_Unit', y='Labor_Total_Output', color='Product_Type', barmode='group',
                      title="Total Output by Factory Unit and Product Type")
        st.plotly_chart(fig3)

        # 4. Productivity Zone Distribution by Factory Unit
        st.header("Productivity Zone Distribution by Factory Unit")
        fig4 = px.histogram(filtered_data, x='Factory_Unit', color='Productivity_Zone',
                            title="Productivity Zone Distribution by Factory Unit"
                            ,color_discrete_map={'Green': 'green', 'Yellow': 'yellow', 'Red': 'red'})
        st.plotly_chart(fig4)

        # 5. Efficiency Rate by Factory Unit
        st.header("Efficiency Rate by Factory Unit")
        fig5 = px.box(filtered_data, x='Factory_Unit', y='Labor_Efficiency_Rate', color='Factory_Unit',
                      title="Efficiency Rate by Factory Unit")
        st.plotly_chart(fig5)

    elif parameter == "Machine Unit":

        # 1. Overall Productivity by Machine Unit
        st.header("Overall Productivity by Machine Unit")
        fig1 = px.bar(filtered_data, x='Machine_Unit', y='Productivity', color='Machine_Unit',
                      title="Productivity by Machine Unit")
        st.plotly_chart(fig1)


        # 3. Total Output by Machine Unit and Product Type
        st.header("Total Output by Machine Unit and Product Type")
        fig3 = px.bar(filtered_data, x='Machine_Unit', y='Labor_Total_Output', color='Product_Type', barmode='group',
                      title="Total Output by Machine Unit and Product Type")
        st.plotly_chart(fig3)

        # 4. Productivity Zone Distribution by Machine Unit
        st.header("Productivity Zone Distribution by Machine Unit")
        fig4 = px.histogram(filtered_data, x='Machine_Unit', color='Productivity_Zone',
                            title="Productivity Zone Distribution by Machine Unit",
                            color_discrete_map={'Green': 'green', 'Yellow': 'yellow', 'Red': 'red'})
        st.plotly_chart(fig4)

        # 5. Efficiency Rate by Machine Unit
        st.header("Efficiency Rate by Machine Unit")
        fig5 = px.box(filtered_data, x='Machine_Unit', y='Labor_Efficiency_Rate', color='Machine_Unit',
                      title="Efficiency Rate by Machine Unit")
        st.plotly_chart(fig5)

elif analysis_choice == "Visual Themes of Labor Productivity":
    if theme == "Productivity Pulse":
        st.title("Productivity Pulse")


        time_interval = st.selectbox("Choose Interval", ["Weekly", "Monthly", "Yearly"])




        # Group the filtered data based on the selected time interval
        if time_interval == "Weekly":
            filtered_data['Week'] = filtered_data['Date'].dt.isocalendar().week
            interval_data = filtered_data.groupby(['Week', 'Shift']).mean(numeric_only=True).reset_index()
            time_col = 'Week'
        elif time_interval == "Monthly":
            filtered_data['Month'] = filtered_data['Date'].dt.month
            interval_data = filtered_data.groupby(['Month', 'Shift']).mean(numeric_only=True).reset_index()
            time_col = 'Month'
        else:  # Yearly
            filtered_data['Year'] = filtered_data['Date'].dt.year
            interval_data = filtered_data.groupby(['Year', 'Shift']).mean(numeric_only=True).reset_index()
            time_col = 'Year'

        # 1. Time-Series Productivity by Shift
        st.header("Productivity Trends by Shift")
        fig1 = px.line(interval_data, x=time_col, y='Productivity', color='Shift', markers=True,
                       title=f"Productivity Trends Over {time_interval}",
                       labels={time_col: time_interval, 'Productivity': 'Productivity (%)'})
        st.plotly_chart(fig1)

        # 2. Shift-wise Productivity Peaks and Troughs
        st.header("Productivity Comparison Across Shifts")
        fig2 = px.bar(filtered_data, x='Shift', y='Productivity', color='Shift',
                      title="Shift-wise Productivity Peaks and Troughs",
                      labels={'Productivity': 'Productivity (%)'})
        st.plotly_chart(fig2)

        # 3. Anomaly Detection in Productivity (Time-Series Analysis)
        st.header("Anomaly Detection in Productivity")
        fig3 = px.line(interval_data, x=time_col, y='Productivity', color='Shift',
                       title="Productivity with Anomaly Detection")

        # Identify anomalies based on a simple threshold (e.g., 1.5 standard deviations)
        for shift in interval_data['Shift'].unique():
            shift_data = interval_data[interval_data['Shift'] == shift]
            mean_prod = shift_data['Productivity'].mean()
            std_prod = shift_data['Productivity'].std()
            anomalies = shift_data[(shift_data['Productivity'] > mean_prod + 1.5 * std_prod) |
                                   (shift_data['Productivity'] < mean_prod - 1.5 * std_prod)]
            fig3.add_scatter(x=anomalies[time_col], y=anomalies['Productivity'], mode='markers',
                             marker=dict(color='red', size=10), name=f"{shift} Anomalies")

        st.plotly_chart(fig3)

        # 4. Productivity Distribution Across Time Intervals
        st.header("Productivity Distribution by Time Interval")
        if time_interval == "Weekly":
            fig4 = px.box(filtered_data, x='Week', y='Productivity', color='Shift',
                          title="Weekly Productivity Distribution")
        elif time_interval == "Monthly":
            fig4 = px.box(filtered_data, x='Month', y='Productivity', color='Shift',
                          title="Monthly Productivity Distribution")
        else:
            fig4 = px.box(filtered_data, x='Year', y='Productivity', color='Shift',
                          title="Yearly Productivity Distribution")

        st.plotly_chart(fig4)



    elif theme == "Department Dynamics":
        # Assuming data is already filtered based on user inputs

        # Departmental Productivity Comparison over Selected Time Interval
        st.header("Departmental Productivity Comparison")
        fig1 = px.bar(
            filtered_data,
            x='Department',
            y='Productivity',
            color='Department',
            title="Departmental Productivity Comparison",
            barmode='group',
            labels={'Productivity': 'Productivity (%)'}
        )
        st.plotly_chart(fig1)
        # Managerial Influence on Departmental Productivity
        st.header("Manager's Influence on Departmental Productivity")
        fig2 = px.scatter(
            filtered_data,
            x='Manager',
            y='Productivity',
            color='Department',
            title="Manager's Influence on Departmental Productivity",
            labels={'Productivity': 'Productivity (%)'}
        )
        st.plotly_chart(fig2)
        # Bar chart showing average productivity by Manager
        st.header("Average Productivity by Manager")
        fig3 = px.bar(
            filtered_data,
            x='Manager',
            y='Productivity',
            color='Manager',
            title="Average Productivity by Manager",
            labels={'Productivity': 'Average Productivity (%)'},
            category_orders={'Manager': filtered_data['Manager'].unique().tolist()}
        )
        st.plotly_chart(fig3)
        # Departmental Efficiency by Manager
        st.header("Departmental Efficiency by Manager")
        fig4 = px.box(
            filtered_data,
            x='Department',
            y='Labor_Efficiency_Rate',
            color='Manager',
            title="Departmental Efficiency by Manager",
            labels={'Labor_Efficiency_Rate': 'Efficiency Rate (%)'}
        )
        st.plotly_chart(fig4)
        # Departmental Output vs. Managerial Influence
        st.header("Departmental Output vs. Managerial Influence")
        fig5 = px.scatter(
            filtered_data,
            x='Manager',
            y='Labor_Total_Output',
            color='Department',
            title="Departmental Output vs. Managerial Influence",
            labels={'Labor_Total_Output': 'Total Output'}
        )
        st.plotly_chart(fig5)

    elif theme == "Productivity Panorama":
        st.header("Productivity Panorama ")

        # 1. Stacked Bar Chart: Productivity by Factory and Machine Unit
        st.header("Productivity by Factory and Machine Unit (Stacked)")
        stacked_data = filtered_data.groupby(['Factory_Unit', 'Machine_Unit'])['Productivity'].mean().reset_index()
        fig1 = px.bar(stacked_data, x='Factory_Unit', y='Productivity', color='Machine_Unit', barmode='stack',
                      title="Stacked Productivity by Factory and Machine Unit",
                      labels={'Productivity': 'Average Productivity (%)'})
        st.plotly_chart(fig1)

        # 2. Bar Chart: Productivity by Machine Unit
        st.header("Productivity by Machine Unit")
        bar_data = filtered_data.groupby('Machine_Unit')['Productivity'].mean().reset_index()
        fig2 = px.bar(bar_data, x='Machine_Unit', y='Productivity', color='Productivity',
                      title="Productivity by Machine Unit",
                      labels={'Productivity': 'Average Productivity (%)'},
                      color_continuous_scale="Cividis")
        st.plotly_chart(fig2)

        # 3. Scatter Plot: Productivity by Factory and Machine Units
        st.header("Scatter Plot of Productivity by Factory and Machine Units")
        scatter_data = filtered_data[['Factory_Unit', 'Machine_Unit', 'Productivity']]
        fig3 = px.scatter(scatter_data, x='Factory_Unit', y='Machine_Unit', size='Productivity', color='Productivity',
                          title="Scatter Plot of Productivity by Factory and Machine Units",
                          labels={'Productivity': 'Productivity (%)'},
                          color_continuous_scale="Plasma", size_max=10)
        st.plotly_chart(fig3)

        # 4. Box Plot: Productivity Variation by Factory and Machine Units
        st.header("Productivity Variation by Factory and Machine Units")
        fig4 = px.box(filtered_data, x='Factory_Unit', y='Productivity', color='Machine_Unit',
                      title="Productivity Variation by Factory and Machine Units",
                      labels={'Productivity': 'Productivity (%)'})
        st.plotly_chart(fig4)




        # 4. Violin Plot: Productivity Distribution by Factory Unit
        st.header("Productivity Distribution by Factory Unit")
        fig4 = px.violin(filtered_data, x='Factory_Unit', y='Productivity', color='Factory_Unit', box=True,
                         points="all",
                         title="Violin Plot of Productivity Distribution by Factory Unit",
                         labels={'Productivity': 'Productivity (%)'})
        st.plotly_chart(fig4)

    elif theme == "Target Tracker":

        # 1. Grouped Bar Chart: Factory and Machine Unit Productivity Comparison
        st.header("Factory and Machine Unit Productivity Comparison (Grouped)")
        grouped_data = filtered_data.groupby(['Factory_Unit', 'Machine_Unit'])['Productivity'].mean().reset_index()
        fig1 = px.bar(grouped_data, x='Factory_Unit', y='Productivity', color='Machine_Unit', barmode='group',
                      title="Grouped Productivity by Factory and Machine Unit",
                      labels={'Productivity': 'Average Productivity (%)'})
        st.plotly_chart(fig1)

        # 2. Treemap Chart: Hierarchical View of Productivity by Factory and Machine Units
        st.header("Productivity Hierarchy (Treemap)")
        fig2 = px.treemap(filtered_data, path=['Factory_Unit', 'Machine_Unit'], values='Productivity',
                          color='Productivity', color_continuous_scale="Cividis",
                          title="Treemap Chart of Productivity by Factory and Machine Unit",
                          labels={'Productivity': 'Average Productivity (%)'})
        st.plotly_chart(fig2)



        # 4. Box Plot: Productivity Variation by Machine Unit within Factory Units
        st.header("Productivity Variation by Machine Unit within Factory Units")
        fig4 = px.box(filtered_data, x='Factory_Unit', y='Productivity', color='Machine_Unit',
                      title="Box Plot of Productivity Variation by Factory Unit and Machine Unit",
                      labels={'Productivity': 'Productivity (%)'})
        st.plotly_chart(fig4)

    elif theme == "Shift Synergy":
        st.header("Productivity Zones by Shift and Department (Stacked)")

        # 1. Grouped Bar Chart: Productivity Rates by Shift and Department
        st.header("Productivity Rates by Shift and Department")
        grouped_data = filtered_data.groupby(['Shift', 'Department', 'Productivity_Zone'])[
            'Productivity'].mean().reset_index()
        fig1 = px.bar(grouped_data, x='Shift', y='Productivity', color='Productivity_Zone', barmode='group',
                      facet_col='Department', title="Productivity Rates by Shift and Department",
                      labels={'Productivity': 'Average Productivity (%)'},color_discrete_map={'Green': 'green', 'Yellow': 'yellow', 'Red': 'red'})
        st.plotly_chart(fig1)



        # Calculate average productivity and standard deviation for real-time anomaly detection
        mean_productivity = filtered_data['Productivity'].mean()
        std_dev_productivity = filtered_data['Productivity'].std()
        anomaly_threshold = mean_productivity - 1.5 * std_dev_productivity

        # 1. Line Chart with Real-Time Anomaly Detection
        st.header("Real-Time Productivity Trends with Anomaly Detection")
        fig1 = px.scatter(filtered_data, x='Date', y='Productivity', color='Shift',
                       title="Real-Time Productivity Trends by Shift",
                       labels={'Productivity': 'Productivity (%)'})

        # Highlight anomalies in red for each shift
        for shift in filtered_data['Shift'].unique():
            shift_data = filtered_data[filtered_data['Shift'] == shift]
            anomalies = shift_data[shift_data['Productivity'] < anomaly_threshold]
            fig1.add_scatter(x=anomalies['Date'], y=anomalies['Productivity'], mode='markers',
                             marker=dict(color='red', size=8, symbol='x'),
                             name=f"{shift} Anomalies")

        st.plotly_chart(fig1)

        # 2. Scatter Plot for Productivity Zones with Anomaly Markers
        st.header("Productivity Zones with Anomaly Markers")
        fig2 = px.scatter(filtered_data, x='Shift', y='Productivity', color='Productivity_Zone',
                          title="Scatter Plot of Productivity Zones by Shift",
                          labels={'Productivity'})

        # Add red markers for anomalies
        fig2.add_scatter(x=anomalies['Shift'], y=anomalies['Productivity'], mode='markers',
                         marker=dict(color='red', size=10, symbol='diamond'),
                         name="Anomalies")

        st.plotly_chart(fig2)

        # 3. Distribution of Productivity Zones with Real-Time Anomaly Detection
        st.header("Productivity Distribution with Anomaly Detection")
        fig3 = px.box(filtered_data, x='Shift', y='Productivity', color='Productivity_Zone',
                      title="Productivity Distribution by Shift with Anomaly Detection",
                      labels={'Productivity': 'Productivity (%)'})

        # Add threshold line for anomaly detection
        fig3.add_hline(y=anomaly_threshold, line_dash="dot", line_color="red",
                       annotation_text="Anomaly Threshold", annotation_position="top left")

        st.plotly_chart(fig3)



        # 3. Comparative Violin Plot for Productivity Distribution by Zone
        st.header("Productivity Distribution by Zone Across Shifts")
        fig3 = px.violin(filtered_data, x='Productivity_Zone', y='Productivity', color='Shift', box=True, points="all",
                         title="Violin Plot of Productivity by Zone and Shift",
                         labels={'Productivity': 'Productivity (%)', 'Productivity_Zone': 'Zone'})
        st.plotly_chart(fig3)

    elif theme == "Efficiency Compass":
        # 1. Scatter Plot: Efficiency vs. Productivity by Department
        st.header("Labor Efficiency Rate vs. Productivity by Department")
        fig1 = px.scatter(filtered_data, x='Labor_Efficiency_Rate', y='Productivity', color='Department',
                          title="Labor Efficiency Rate vs. Productivity (Department-wise)",
                          labels={'Labor_Efficiency_Rate': 'Labor Efficiency Rate (%)',
                                  'Productivity': 'Productivity (%)'},
                          hover_data=['Machine_Unit'])
        fig1.update_traces(marker=dict(size=10))
        st.plotly_chart(fig1)

        # 2. Box Plot: Distribution of Labor Efficiency by Machine Unit
        st.header("Distribution of Labor Efficiency by Machine Unit")
        fig2 = px.box(filtered_data, x='Machine_Unit', y='Labor_Efficiency_Rate', color='Machine_Unit',
                      title="Labor Efficiency Distribution by Machine Unit",
                      labels={'Labor_Efficiency_Rate': 'Labor Efficiency Rate (%)'})
        st.plotly_chart(fig2)

        # 3. Stacked Bar Chart: Average Efficiency and Productivity by Department
        st.header("Average Efficiency and Productivity by Department")
        dept_data = filtered_data.groupby('Department').agg(
            {'Labor_Efficiency_Rate': 'mean', 'Productivity': 'mean'}).reset_index()
        fig3 = go.Figure()
        fig3.add_trace(go.Bar(x=dept_data['Department'], y=dept_data['Labor_Efficiency_Rate'], name='Efficiency Rate',
                              marker_color='blue'))
        fig3.add_trace(
            go.Bar(x=dept_data['Department'], y=dept_data['Productivity'], name='Productivity', marker_color='orange'))
        fig3.update_layout(barmode='stack', title="Average Efficiency and Productivity by Department",
                           yaxis_title="Percentage (%)")
        st.plotly_chart(fig3)

        # 4. Bubble Chart: Efficiency and Productivity by Department and Machine Unit
        st.header("Efficiency and Productivity by Department and Machine Unit")
        fig4 = px.scatter(filtered_data, x='Labor_Efficiency_Rate', y='Productivity', size='Productivity',
                          color='Department', hover_name='Machine_Unit',
                          title="Efficiency vs. Productivity by Department and Machine Unit",
                          labels={'Labor_Efficiency_Rate': 'Labor Efficiency Rate (%)',
                                  'Productivity': 'Productivity (%)'})
        fig4.update_traces(marker=dict(sizemode='diameter', opacity=0.7))
        st.plotly_chart(fig4)
    elif theme == "Productivity Evolution":

        # Ensure 'Year' and 'Month' columns exist and aggregate by month-year for heatmap
        filtered_data['Month'] = filtered_data['Date'].dt.month
        filtered_data['Year'] = filtered_data['Date'].dt.year
        pivot_data = filtered_data.pivot_table(index='Year', columns='Month', values='Productivity', aggfunc='mean')

        st.header("Monthly Productivity Patterns by Year")
        fig3 = px.imshow(
            pivot_data,
            title="Monthly Productivity Patterns by Year",
            labels={'x': 'Month', 'y': 'Year', 'color': 'Productivity (%)'},

        )
        st.plotly_chart(fig3)


        # Sidebar selection for time interval
        time_interval = st.selectbox("Select Time Interval", ["Weekly", "Monthly", "Yearly"])

        # Group the filtered data based on the selected time interval
        if time_interval == "Weekly":
            filtered_data['Week'] = filtered_data['Date'].dt.isocalendar().week
            interval_data = filtered_data.groupby(['Week', 'Shift']).mean(numeric_only=True).reset_index()
            time_col = 'Week'
        elif time_interval == "Monthly":
            filtered_data['Month'] = filtered_data['Date'].dt.month
            interval_data = filtered_data.groupby(['Month', 'Shift']).mean(numeric_only=True).reset_index()
            time_col = 'Month'
        else:  # Yearly
            filtered_data['Year'] = filtered_data['Date'].dt.year
            interval_data = filtered_data.groupby(['Year', 'Shift']).mean(numeric_only=True).reset_index()
            time_col = 'Year'

        # Generate productivity trend line charts for each shift
        shifts = interval_data['Shift'].unique()
        for shift in shifts:
            shift_data = interval_data[interval_data['Shift'] == shift]

            # Create a line chart for each shift
            fig = px.line(
                shift_data,
                x=time_col,
                y='Productivity',
                title=f"{shift} Shift Productivity Trend ({time_interval})",
                labels={'Productivity': 'Average Productivity (%)', time_col: time_interval},
                markers=True
            )

            # Customize the chart layout
            fig.update_layout(
                xaxis_title=time_interval,
                yaxis_title="Average Productivity (%)",
                template="plotly_white",
                showlegend=False
            )

            # Display each chart
            st.plotly_chart(fig, use_container_width=True)

        # Additional Insights: Overall Productivity Trend by Time Interval
        overall_productivity_trend = interval_data.groupby(time_col).mean(numeric_only=True).reset_index()

        fig_overall = px.line(
            overall_productivity_trend,
            x=time_col,
            y='Productivity',
            title=f"Overall Productivity Trend ({time_interval})",
            labels={'Productivity': 'Average Productivity (%)', time_col: time_interval},
            markers=True
        )

        fig_overall.update_layout(
            xaxis_title=time_interval,
            yaxis_title="Average Productivity (%)",
            template="plotly_white",
            showlegend=False
        )

        # Display the overall trend chart
        st.plotly_chart(fig_overall, use_container_width=True)
        st.header("Anomaly Detection in Productivity")
        fig3 = px.line(interval_data, x=time_col, y='Productivity', color='Shift',
                       title="Productivity with Anomaly Detection")

        # Identify anomalies based on a simple threshold (e.g., 1.5 standard deviations)
        for shift in interval_data['Shift'].unique():
            shift_data = interval_data[interval_data['Shift'] == shift]
            mean_prod = shift_data['Productivity'].mean()
            std_prod = shift_data['Productivity'].std()
            anomalies = shift_data[(shift_data['Productivity'] > mean_prod + 1.5 * std_prod) |
                                   (shift_data['Productivity'] < mean_prod - 1.5 * std_prod)]
            fig3.add_scatter(x=anomalies[time_col], y=anomalies['Productivity'], mode='markers',
                             marker=dict(color='red', size=10), name=f"{shift} Anomalies")

        st.plotly_chart(fig3)
