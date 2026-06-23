import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import google.generativeai as genai

# ─────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────
st.set_page_config(page_title="Plant OT Report", layout="wide", page_icon="🕐")

GEMINI_API_KEY = ""  #ENTER API KEY HERE
genai.configure(api_key=GEMINI_API_KEY)
# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────
st.title("🕐 Plant Overtime Report Analyzer")
st.markdown("Upload the monthly OT CSV file to generate charts and an AI analysis report.")

# ─────────────────────────────────────────────
# FILE UPLOAD
# ─────────────────────────────────────────────
uploaded_file = st.file_uploader("Upload CSV File", type=["csv"])

if uploaded_file:
    # ── Read CSV ──────────────────────────────
    df = pd.read_csv(uploaded_file)

    # ── Clean column names (strip extra spaces) ──
    df.columns = df.columns.str.strip()

    # ── Rename key columns for easy use ──────
    df = df.rename(columns={
        "NAME OF THE STAFF": "Employee",
        "Total working hrs ": "OT_Hours",   # trailing space in original
        "Total working hrs": "OT_Hours",    # fallback without space
        "Total": "OT_Amount",
        "Per      hours ": "Per_Hour_Rate",
        "Per hours": "Per_Hour_Rate",
        "Employee Code": "Emp_Code",
        "Gross Salary": "Gross_Salary",
    })

    # ── Fix OT_Hours column name if still missing ──
    # Find the column that contains total hours (second-to-last before Total)
    cols = list(df.columns)
    if "OT_Hours" not in cols:
        # Try to find it by position: it's the column just before "Total"
        for i, c in enumerate(cols):
            if str(c).strip().lower() in ["total working hrs", "total working hrs "]:
                df = df.rename(columns={c: "OT_Hours"})
                break

    # ── Drop completely empty rows ────────────
    df = df.dropna(subset=["Employee"])
    df["Employee"] = df["Employee"].astype(str).str.strip()
    df = df[df["Employee"] != "nan"]

    # ── Ensure numeric ────────────────────────
    df["OT_Hours"] = pd.to_numeric(df["OT_Hours"], errors="coerce").fillna(0)
    df["OT_Amount"] = pd.to_numeric(df["OT_Amount"], errors="coerce").fillna(0)
    df["Gross_Salary"] = pd.to_numeric(df["Gross_Salary"], errors="coerce").fillna(0)

    # ── Day columns (1 to 30) ─────────────────
    day_cols = [str(i) for i in range(1, 31) if str(i) in df.columns]

    # ── Summary cards ─────────────────────────
    st.markdown("---")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("👷 Total Employees", len(df))
    c2.metric("⏱️ Total OT Hours", f"{df['OT_Hours'].sum():,.1f}")
    c3.metric("💰 Total OT Amount (₹)", f"₹{df['OT_Amount'].sum():,.0f}")
    c4.metric("🏢 Departments", df["Department"].nunique())

    st.markdown("---")

    # ─────────────────────────────────────────────
    # RAW DATA PREVIEW
    # ─────────────────────────────────────────────
    with st.expander("📋 View Raw Data"):
        st.dataframe(df[["Emp_Code", "Employee", "Department", "Gross_Salary", "OT_Hours", "OT_Amount"]].reset_index(drop=True))

    # ─────────────────────────────────────────────
    # CHARTS
    # ─────────────────────────────────────────────
    st.subheader("📊 Charts & Analysis")

    # ── Chart 1: Top 15 employees by OT Hours ──
    top_emp = df.nlargest(15, "OT_Hours")[["Employee", "Department", "OT_Hours", "OT_Amount"]].reset_index(drop=True)
    fig1 = px.bar(
        top_emp,
        x="OT_Hours",
        y="Employee",
        orientation="h",
        color="Department",
        title="Top 15 Employees by Overtime Hours",
        labels={"OT_Hours": "OT Hours", "Employee": ""},
        text="OT_Hours"
    )
    fig1.update_traces(texttemplate="%{text:.1f}h", textposition="outside")
    fig1.update_layout(height=500, yaxis=dict(autorange="reversed"))
    st.plotly_chart(fig1, use_container_width=True)

    col1, col2 = st.columns(2)

    # ── Chart 2: OT Hours by Department (Bar) ──
    with col1:
        dept_hours = df.groupby("Department")["OT_Hours"].sum().reset_index().sort_values("OT_Hours", ascending=False)
        fig2 = px.bar(
            dept_hours,
            x="Department",
            y="OT_Hours",
            title="Total OT Hours by Department",
            color="OT_Hours",
            color_continuous_scale="Oranges",
            text="OT_Hours"
        )
        fig2.update_traces(texttemplate="%{text:.1f}h", textposition="outside")
        fig2.update_layout(xaxis_tickangle=-30, coloraxis_showscale=False)
        st.plotly_chart(fig2, use_container_width=True)

    # ── Chart 3: OT Amount by Department (Pie) ──
    with col2:
        dept_amt = df.groupby("Department")["OT_Amount"].sum().reset_index()
        fig3 = px.pie(
            dept_amt,
            names="Department",
            values="OT_Amount",
            title="OT Amount Distribution by Department (₹)",
            hole=0.4
        )
        fig3.update_traces(textinfo="label+percent", textposition="outside")
        st.plotly_chart(fig3, use_container_width=True)

    # ── Chart 4: Daily OT pattern across the month ──
    if day_cols:
        daily_totals = df[day_cols].apply(pd.to_numeric, errors="coerce").sum()
        daily_df = pd.DataFrame({"Day": [int(d) for d in day_cols], "Total_OT_Hours": daily_totals.values})
        fig4 = px.line(
            daily_df,
            x="Day",
            y="Total_OT_Hours",
            title="Daily OT Hours Trend (All Employees Combined)",
            markers=True,
            labels={"Total_OT_Hours": "Total OT Hours", "Day": "Day of Month"}
        )
        fig4.update_traces(line_color="#FF6B35", marker=dict(size=6))
        fig4.update_layout(xaxis=dict(tickmode="linear", dtick=1))
        st.plotly_chart(fig4, use_container_width=True)

    col3, col4 = st.columns(2)

    # ── Chart 5: OT Hours vs Gross Salary scatter ──
    with col3:
        fig5 = px.scatter(
            df,
            x="Gross_Salary",
            y="OT_Hours",
            color="Department",
            hover_data=["Employee"],
            title="OT Hours vs Gross Salary by Employee",
            labels={"Gross_Salary": "Gross Salary (₹)", "OT_Hours": "OT Hours"}
        )
        st.plotly_chart(fig5, use_container_width=True)

    # ── Chart 6: Employee count per department ──
    with col4:
        emp_count = df.groupby("Department").size().reset_index(name="Employee Count").sort_values("Employee Count", ascending=False)
        fig6 = px.bar(
            emp_count,
            x="Department",
            y="Employee Count",
            title="Employee Count by Department",
            color="Employee Count",
            color_continuous_scale="Blues",
            text="Employee Count"
        )
        fig6.update_traces(textposition="outside")
        fig6.update_layout(xaxis_tickangle=-30, coloraxis_showscale=False)
        st.plotly_chart(fig6, use_container_width=True)

    # ── Chart 7: Full OT heatmap (Employee x Day) ──
    if day_cols:
        st.subheader("🗓️ Day-wise OT Heatmap")
        heat_df = df.set_index("Employee")[day_cols].apply(pd.to_numeric, errors="coerce").fillna(0)
        # Limit to top 30 by OT hours for readability
        top30 = df.nlargest(30, "OT_Hours")["Employee"].tolist()
        heat_df = heat_df.loc[heat_df.index.isin(top30)]

        fig7 = go.Figure(data=go.Heatmap(
            z=heat_df.values,
            x=[f"Day {d}" for d in day_cols],
            y=heat_df.index.tolist(),
            colorscale="YlOrRd",
            hoverongaps=False,
            colorbar=dict(title="OT Hrs")
        ))
        fig7.update_layout(
            title="Day-wise OT Hours Heatmap (Top 30 Employees by Total OT)",
            height=700,
            xaxis_tickangle=-45
        )
        st.plotly_chart(fig7, use_container_width=True)

    st.markdown("---")

    # ─────────────────────────────────────────────
    # AI ANALYSIS
    # ─────────────────────────────────────────────
    st.subheader("🤖 AI Analysis Report")

    if st.button("Generate AI Report", type="primary"):
        with st.spinner("Gemini 2.0 Flash is analyzing your overtime data..."):

            dept_summary = df.groupby("Department").agg(
                Employees=("Employee", "count"),
                Total_OT_Hours=("OT_Hours", "sum"),
                Total_OT_Amount=("OT_Amount", "sum"),
                Avg_OT_Hours=("OT_Hours", "mean")
            ).round(2).to_string()

            top10 = df.nlargest(10, "OT_Hours")[["Employee", "Department", "OT_Hours", "OT_Amount", "Gross_Salary"]].to_string(index=False)

            zero_ot = df[df["OT_Hours"] == 0]["Employee"].tolist()

            prompt = f"""
You are a senior HR analyst. Analyze the April 2026 overtime data for a pharmaceutical plant and write a professional report.

DEPARTMENT-WISE SUMMARY:
{dept_summary}

TOP 10 EMPLOYEES BY OT HOURS:
{top10}

EMPLOYEES WITH ZERO OT: {len(zero_ot)} employees

OVERALL STATS:
- Total Employees: {len(df)}
- Total OT Hours: {df['OT_Hours'].sum():,.1f}
- Total OT Amount: ₹{df['OT_Amount'].sum():,.0f}
- Average OT per Employee: {df['OT_Hours'].mean():.1f} hours

Write a structured report with the following sections:

## Executive Summary
(2-3 sentences giving the big picture)

## Department-wise Analysis
(Highlight which departments have highest and lowest OT, and why this might be significant)

## High Overtime Risk Employees
(Flag employees with unusually high OT hours — over-reliance risk, burnout risk)

## Cost Analysis
(Total OT cost implications, which departments are costing the most)

## Recommendations for HR
(At least 4 specific, actionable recommendations)

## Conclusion
(Brief closing with next steps)

Use ₹ for currency. Keep the tone professional and data-driven.
"""

            model = genai.GenerativeModel("gemini-2.5-flash")
            response = model.generate_content(prompt)
            report_text = response.text

            st.markdown(report_text)

            st.download_button(
                label="📥 Download Report as Text",
                data=report_text,
                file_name="OT_Report_April_2026.txt",
                mime="text/plain"
            )
