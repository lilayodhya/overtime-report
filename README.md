# 🕐 Plant Overtime Report Analyzer

A Streamlit-based web application for analyzing and reporting on employee overtime data in manufacturing and industrial facilities. This tool transforms raw overtime CSV data into interactive visualizations and generates AI-powered HR insights using Google's Gemini API.

## 🎯 Features

### 📊 Interactive Visualizations
- **Top Employees by OT Hours** – Bar chart showing the 15 employees with the highest overtime hours
- **Department-wise Analysis** – Compare overtime hours and costs across departments
- **OT Amount Distribution** – Pie chart showing financial impact by department
- **Daily Trend Analysis** – Line chart tracking daily overtime patterns throughout the month
- **Scatter Plot** – Analyze the relationship between OT hours and gross salary
- **Department Staffing** – Employee count distribution by department
- **Heatmap** – Day-wise overtime hours for the top 30 employees

### 🤖 AI-Powered Report Generation
- Automated report generation using Google Gemini 2.5 Flash
- Structured analysis including:
  - Executive Summary
  - Department-wise insights
  - High overtime risk identification
  - Cost analysis
  - HR recommendations
  - Action items

### 📋 Data Management
- CSV file upload with automatic column name normalization
- Flexible column mapping for various CSV formats
- Real-time data cleaning and validation
- Summary metrics dashboard

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- A Google Gemini API key ([Get one here](https://ai.google.dev/))

### Installation

1. Clone the repository:
```bash
git clone https://github.com/lilayodhya/overtime-report.git
cd overtime-report
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your Gemini API key:
   - Create a `.streamlit/secrets.toml` file in your project directory:
   ```toml
   GEMINI_API_KEY = "your-api-key-here"
   ```

4. Run the application:
```bash
streamlit run app.py
```

5. Open your browser to `http://localhost:8501`

## 📥 Data Format

The application expects a CSV file with the following columns:

- **NAME OF THE STAFF** – Employee name
- **Employee Code** – Unique employee identifier
- **Department** – Department name
- **Gross Salary** – Base salary in ₹
- **Total working hrs** – Total overtime hours
- **Per hours** – Hourly overtime rate
- **Total** – Total overtime amount in ₹
- **1-30** – Daily overtime hours (columns for each day of the month)

**Note:** The application includes flexible column name mapping to handle variations in formatting.

### Example CSV Format:
```
NAME OF THE STAFF,Employee Code,Department,Gross Salary,Total working hrs,Per hours,Total,1,2,3,...,30
John Doe,E001,Production,50000,10.5,250,2625,0.5,0.5,0.5,...,0
Jane Smith,E002,Quality,55000,8.0,250,2000,0,0.5,0,...,0
```

## 🛠️ Technology Stack

| Technology | Purpose |
|-----------|---------|
| **Streamlit** | Web application framework |
| **Pandas** | Data manipulation and analysis |
| **Plotly** | Interactive visualizations |
| **Google Generative AI** | AI-powered report generation |
| **Python** | Core language |

## 📊 Key Metrics Displayed

- **Total Employees** – Count of employees in the dataset
- **Total OT Hours** – Sum of all overtime hours
- **Total OT Amount** – Total overtime cost in ₹
- **Departments** – Number of unique departments

## 💡 Use Cases

- **HR Planning** – Identify departments with excessive overtime needs
- **Cost Analysis** – Track overtime spending by department and employee
- **Resource Management** – Identify overworked employees for workload rebalancing
- **Compliance** – Monitor labor hours for regulatory compliance
- **Trend Analysis** – Understand monthly overtime patterns

## 🔐 Security Notes

- API keys should never be committed to version control
- Use Streamlit Secrets management for production deployments
- Keep `.streamlit/secrets.toml` in `.gitignore`

## 📝 License

This project is open source. Feel free to use and modify as needed.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## 📧 Support

For issues, questions, or suggestions, please open an issue on GitHub.

---

**Built with ❤️ for better HR analytics**
