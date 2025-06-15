import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# --- Load Data ---
df = pd.read_csv('notebook/student_dataset_cleaned.csv')

st.set_page_config(page_title="Student Performance Dashboard", layout="wide")

st.title("📚 Student Performance Analytics Dashboard")

# --- Top KPIs (Metric Boxes) ---
avg_marks = round(df['Average_Marks'].mean(), 2)
avg_attendance = round(df['Attendance (%)'].mean(), 2)
total_students = df.shape[0]
at_risk_count = df[df['At_Risk'] == True].shape[0]

col1, col2, col3, col4 = st.columns(4)
col1.metric("🎯 Total Students", total_students)
col2.metric("📈 Avg. Marks", avg_marks)
col3.metric("📊 Avg. Attendance (%)", avg_attendance)
col4.metric("🚨 At-Risk Students", at_risk_count)

st.markdown("---")

# --- Subject-wise Average Marks ---
st.subheader("📘 Subject-wise Average Marks")
subject_cols = ['Math', 'Physics', 'Chemistry']
subject_means = df[subject_cols].mean()
st.bar_chart(subject_means)

# --- Grade Distribution ---
st.subheader("📚 Grade Distribution")
grade_counts = df['Grade'].value_counts()
st.bar_chart(grade_counts)

# --- Correlation Matrix ---
st.subheader("📈 Correlation Between Scores & Attendance")
numeric_cols = ['Math', 'Physics', 'Chemistry', 'Average_Marks', 'Attendance (%)']
corr = df[numeric_cols].corr()
fig_corr, ax_corr = plt.subplots(figsize=(6, 4))
sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f", ax=ax_corr)
st.pyplot(fig_corr)

# --- Top 5 Students ---
st.subheader("🏅 Top 5 Students by Average Marks")
top_students = df.sort_values(by='Average_Marks', ascending=False).head(5)
st.dataframe(top_students[['Student_Names', 'Average_Marks', 'Attendance (%)', 'Grade']])

# Recognition message box for top students
st.markdown("""
<div style='background-color:#d1e7dd;padding:10px;border-left:5px solid #badbcc;border-radius:5px;margin-top:10px;color:#000'>
🎉 <strong>Recognition:</strong> These top-performing students should be praised and encouraged. Consider awarding them small gifts or certificates to motivate them and inspire others to strive for excellence.
</div>
""", unsafe_allow_html=True)

# --- At-Risk Students Section ---
st.subheader("🚨 At-Risk Students Overview")

# Filter by grade
grades = df['Grade'].dropna().unique()
selected_grade = st.selectbox("Filter At-Risk by Grade", sorted(grades))
at_risk_filtered = df[(df['At_Risk'] == True) & (df['Grade'] == selected_grade)]
st.write(f"Students at Risk in Grade {selected_grade}: {at_risk_filtered.shape[0]}")
st.dataframe(at_risk_filtered[['Student_Names', 'Average_Marks', 'Attendance (%)', 'Grade']])

# Download button
csv = at_risk_filtered.to_csv(index=False).encode('utf-8')
st.download_button("📥 Download At-Risk Students", data=csv, file_name='at_risk_students.csv', mime='text/csv')

# Warning message box for at-risk students
st.markdown("""
<div style='background-color:#fff3cd;padding:10px;border-left:5px solid #ffecb5;border-radius:5px;margin-top:10px;color:#000'>
⚠️ <strong>Note:</strong> These students are at risk of underperformance or dropout. It is highly recommended that the management provides timely academic support and personal guidance. A formal warning may help push them toward improvement.
</div>
""", unsafe_allow_html=True)

# --- At-Risk vs Non-Risk Pie ---
st.subheader("⚖️ Risk Category Proportion")
risk_counts = df['At_Risk'].value_counts()
risk_labels = ['Not At Risk', 'At Risk'] if True in risk_counts.index else ['At Risk', 'Not At Risk']
fig_pie, ax_pie = plt.subplots()
ax_pie.pie(risk_counts, labels=risk_labels, autopct='%1.1f%%', startangle=90, colors=['#66bb6a', '#ef5350'])
ax_pie.axis('equal')
st.pyplot(fig_pie)

# --- Search Student ---
st.subheader("🔍 Search Student by Name")
search_name = st.text_input("Enter full or partial name:")
if search_name:
    result = df[df['Student_Names'].str.contains(search_name, case=False)]
    if not result.empty:
        st.success(f"Found {result.shape[0]} result(s):")
        st.dataframe(result[['Student_Names', 'Average_Marks', 'Attendance (%)', 'Grade', 'At_Risk']])
    else:
        st.warning("No matching student found.")

# --- Footer ---
st.markdown("---")
st.markdown("Made with ❤️ by Karthik Thotakuri | for Tamizhan Skills")
