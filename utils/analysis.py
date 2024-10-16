import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from utils.markdown import centered_subheader, centered_title

def show_info_of_a_column(df) -> pd.DataFrame:
	tmp = df.isnull().sum().to_frame().T
	list_nunique = []
	list_dtypes = []
	list_null_values = []
	# Get list dtypes
	for col in df.columns:
		list_dtypes.append(df[col].dtype)
		list_nunique.append(df[col].nunique())
		list_null_values.append(df.isnull().sum()[col])
	tmp_df = pd.DataFrame({"# Null values": list_null_values, "Data Type": list_dtypes, "# unique values": list_nunique}, index=df.columns)
	return tmp_df
	
def visualize_categorical(df):
	categorical_columns = df.select_dtypes(include=['object']).columns.tolist()
	column_name = st.selectbox("Select a column", categorical_columns)
    # Đếm tần suất các giá trị trong cột phân loại
	value_counts = df[column_name].value_counts().reset_index()
	value_counts.columns = [column_name, 'count']

    # Lựa chọn kiểu visualization
	chart_type = st.selectbox("Type of Chart", 
                              ["Bar Chart", "Horizontal Bar Chart", "Pie Chart", "Donut Chart", "Sunburst Chart"])

    # Biểu đồ thanh
	if chart_type == "Bar Chart":
		fig = px.bar(value_counts, x=column_name, y='count', title=f'Bar Chart of {column_name}',
                     labels={column_name: column_name, 'count': 'Count'}, color=column_name)
    
    # Biểu đồ thanh ngang
	elif chart_type == "Horizontal Bar Chart":
		fig = px.bar(value_counts, y=column_name, x='count', orientation='h', title=f'Horizontal Bar Chart of {column_name}',
                     labels={column_name: column_name, 'count': 'Count'}, color=column_name)
    
    # Biểu đồ tròn
	elif chart_type == "Pie Chart":
		fig = px.pie(value_counts, names=column_name, values='count', title=f'Pie Chart of {column_name}', color=column_name)
    
    # Biểu đồ donut
	elif chart_type == "Donut Chart":
		fig = px.pie(value_counts, names=column_name, values='count', hole=0.5, title=f'Donut Chart of {column_name}', color=column_name)
    
    # Biểu đồ sunburst
	elif chart_type == "Sunburst Chart":
		fig = px.sunburst(df, path=[column_name], values=None, title=f'Sunburst Chart of {column_name}', color=column_name)
    
    # Hiển thị biểu đồ
	st.plotly_chart(fig)

def visualize_numerical(df):
	numerical_columns = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
	column_name = st.selectbox("Select a column", numerical_columns)
	# Lựa chọn kiểu visualization
	chart_type = st.selectbox("Type of Chart", 
                              ["Histogram", "Box Plot", "Violin Plot", "Scatter Plot"])

    # Biểu đồ phân phối (histogram)
	if chart_type == "Histogram":
		fig = px.histogram(df, x=column_name, title=f'Histogram of {column_name}',
                           labels={column_name: column_name}, nbins=30)
    
    # Biểu đồ hộp (box plot)
	elif chart_type == "Box Plot":
		fig = px.box(df, y=column_name, title=f'Box Plot of {column_name}', 
                     labels={column_name: column_name}, points="all")
    
    # Biểu đồ violin
	elif chart_type == "Violin Plot":
		fig = px.violin(df, y=column_name, title=f'Violin Plot of {column_name}', 
                        labels={column_name: column_name}, box=True, points="all")
    
    # Biểu đồ scatter (scatter plot) - yêu cầu chọn thêm cột số khác để làm trục Y
	elif chart_type == "Scatter Plot":
		y_column = st.selectbox("Select Y-axis", numerical_columns, index=0)
		fig = px.scatter(df, x=column_name, y=y_column, title=f'Scatter Plot of {column_name} vs {y_column}',
                         labels={column_name: column_name, y_column: y_column})
    
    # Hiển thị biểu đồ
	st.plotly_chart(fig)
	
def visualization():
	# Đọc dữ liệu
	df = pd.read_csv('./data/MentalHealthSurvey.csv')

	# Tạo tiêu đề cho Dashboard
	centered_title("Mental Health Analysis Dashboard")
	# Hiển thị bảng dữ liệu ban đầu
	
	centered_subheader("Data Frame")
	num_rows = st.slider(label="Number of rows", min_value=0, max_value=len(df))
	st.write(df.head(num_rows))
	
	col1v1, col2v1 = st.columns(spec=[0.3, 0.46], gap='medium')
	with col1v1:
		centered_subheader("Information of each column")
		st.table(show_info_of_a_column(df))
	
	with col2v1:
		centered_subheader("Data Frame Describe")
		is_include_all = st.checkbox("Including categorical columns")
		st.table(df.describe(include=('all' if is_include_all == True else None)).T)
	
	col1, col2 = st.columns(spec=[0.9, 0.9], gap="large")
	with col1:
		centered_subheader("Visualization of Categorical Column")
		visualize_categorical(df)
	with col2:
		centered_subheader("Visualization of Numerical Column")
		visualize_numerical(df)
	

	centered_subheader("Bivariate Analysis")
	cols = st.columns(2)
	# Danh sách các biến về sức khỏe tâm lý
	mental_health_vars = ['depression', 'anxiety', 'isolation', 'future_insecurity']
    # Vòng lặp qua các biến và tạo biểu đồ
	for i, var in enumerate(mental_health_vars):
        # Chọn cột hiển thị
		with cols[i % 2]:
			fig = px.histogram(df, x='university', color=var, 
                               barmode='group', title=f'University vs {var.replace("_", " ").title()}',
                               labels={'university': 'University', 'count': 'Count'}, 
                               color_discrete_sequence=px.colors.qualitative.Set1)
			st.plotly_chart(fig)
	
	col1v2, col2v2 = st.columns(2)
	
	with col1v2:
		# Biểu đồ bar về mức độ trầm cảm theo giới tính
		centered_subheader("Mức độ trầm cảm theo giới tính")
		fig_bar = px.bar(df, x='gender', y='depression', title="Mức độ trầm cảm theo giới tính", 
                 labels={'gender': 'Giới tính', 'depression': 'Mức độ trầm cảm'},
                 color='gender', barmode='group', height=400)
		st.plotly_chart(fig_bar)
		
	with col2v2:
		centered_subheader('Mức độ lo âu theo năm học')
		fig_box = px.box(df, x='academic_year', y='anxiety', title='Mức độ lo âu theo năm học',
                 labels={'academic_year': 'Năm học', 'anxiety': 'Mức độ lo âu'}, 
                 color='academic_year', height=400)
		st.plotly_chart(fig_box)
		

	# # Bộ lọc tương tác theo giới tính
	# st.subheader("Lọc dữ liệu theo giới tính")
	# gender_filter = st.selectbox("Chọn giới tính", df['gender'].unique())
	# filtered_df = df[df['gender'] == gender_filter]
	# st.write(f"Dữ liệu cho {gender_filter}:")
	# st.write(filtered_df)

	# 	# Tạo thêm biểu đồ cho dữ liệu đã lọc
	# st.subheader(f"Biểu đồ cho {gender_filter}")
	# fig, ax = plt.subplots()
	# sns.barplot(x='academic_year', y='depression', data=filtered_df, ax=ax)
	# st.pyplot(fig)
	corr_matrix = df.corr(numeric_only=True)

	centered_subheader("Correlation Matrix of Numerical Columns")
	# Tạo heatmap với Plotly
	fig = go.Figure(
    data=go.Heatmap(
        z=corr_matrix.values,  # Ma trận tương quan
        x=corr_matrix.columns,  # Tên cột
        y=corr_matrix.columns,  # Tên hàng
        colorscale='RdBu',  # Bảng màu
        zmin=-1, zmax=1,  # Giá trị min/max cho màu sắc
        colorbar=dict(title="Correlation")  # Thanh màu chú thích
    	)
	)

	# Thêm tiêu đề và tùy chỉnh layout
	fig.update_layout(
		title="Correlation Matrix",
		xaxis_nticks=len(corr_matrix.columns),  # Số lượng ticks theo số cột
		yaxis_nticks=len(corr_matrix.columns),
		width=800, height=700,
	)

	# Hiển thị với Streamlit
	st.plotly_chart(fig)
		

