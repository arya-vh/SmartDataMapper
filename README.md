# 🚀 Data Quality Guardian

A powerful AI-powered data quality analysis and matching tool that ensures data integrity through intelligent fuzzy matching, comprehensive reporting, and stunning interactive dashboards.

## ✨ Features

- **🔍 Smart Data Matching**: Combines exact matching with AI-powered fuzzy matching using Levenshtein distance
- **📊 Quality Metrics**: Comprehensive analysis of match rates, data cleanliness, and quality scores
- **🎨 Interactive Dashboard**: Beautiful Plotly-based visualizations with real-time insights
- **📈 Performance Tracking**: Detailed reports on matching success rates and confidence levels
- **⚡ Automated Pipeline**: End-to-end data quality assessment with one-click execution

## 🛠️ Installation

1. **Clone or download** the project files
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

   Additional dependencies (automatically installed):
   - `pandas` - Data manipulation
   - `plotly` - Interactive visualizations
   - `rapidfuzz` - Fuzzy string matching
   - `openpyxl` - Excel file support

## 📁 Project Structure

```
├── datamapper.py              # Main DataQualityGuardian class
├── run.py                     # Simple execution script
├── requirements.txt           # Python dependencies
├── raw_data.csv              # Input: Raw data to analyze
├── reference_data.xlsx       # Input: Reference data for matching
├── data_quality_dashboard.html # Output: Interactive dashboard
├── mapped_output_enhanced.csv # Output: Matched results
├── quality_report.csv        # Output: Quality metrics
├── unmatched_analysis.csv    # Output: Unmatched items analysis
└── unmatched_report.py       # Additional analysis script
```

## 🚀 Quick Start

1. **Prepare your data**:
   - Place your raw data in `raw_data.csv` with a `lookup_key` column
   - Place reference data in `reference_data.xlsx` with a `lookup_key` column

2. **Run the analysis**:
   ```bash
   python datamapper.py
   ```
   Or use the simple runner:
   ```bash
   python run.py
   ```

3. **View results**:
   - **Dashboard**: Open `data_quality_dashboard.html` in your browser
   - **Matched Data**: Check `mapped_output_enhanced.csv`
   - **Quality Report**: Review `quality_report.csv`

## 📊 Dashboard Features

The interactive dashboard includes:

- **🎯 Match Success Rate**: Pie chart showing exact vs fuzzy matches
- **📊 Match Types**: Bar chart comparing match categories
- **⭐ Confidence Distribution**: Histogram of matching confidence scores
- **⚡ Performance Timeline**: Gauge indicator with success metrics

## 🔧 Configuration

### Matching Parameters

- **Fuzzy Threshold**: Default 0.85 (85% similarity required)
- **Column Names**: Default `lookup_key` for both raw and reference data
- **Output Format**: CSV with enhanced matching metadata

### Customization

Modify the `DataQualityGuardian` class in `datamapper.py`:

```python
# Change fuzzy matching threshold
fuzzy_matches = self.fuzzy_matching(raw_clean, ref_clean, ref_df, threshold=0.90)

# Customize column names
final_matches = self.analyze_data_quality(raw_df, ref_df, 'your_raw_col', 'your_ref_col')
```

## 📈 Analysis Workflow

1. **Data Loading**: Reads CSV and Excel files
2. **Cleaning**: Removes whitespace, normalizes case, strips special characters
3. **Exact Matching**: Direct string comparisons
4. **Fuzzy Matching**: AI-powered similarity matching using Levenshtein distance
5. **Quality Scoring**: Calculates confidence levels and match types
6. **Report Generation**: Creates comprehensive quality metrics
7. **Dashboard Creation**: Builds interactive visualizations
8. **Auto-Opening**: Launches dashboard in default browser

## 🎯 Use Cases

- **Data Migration**: Ensure data integrity during system migrations
- **Master Data Management**: Identify duplicates and inconsistencies
- **Data Integration**: Match records across different systems
- **Quality Assurance**: Monitor data quality over time
- **Compliance**: Generate audit trails for data matching processes

## 📋 Requirements

- **Python**: 3.7+
- **Memory**: Depends on dataset size (recommended 4GB+ for large datasets)
- **Storage**: Sufficient space for input files and generated reports

## 🐛 Troubleshooting

### Common Issues

1. **Import Errors**: Ensure all dependencies are installed
   ```bash
   pip install pandas plotly rapidfuzz openpyxl
   ```

2. **File Not Found**: Verify input files exist in the correct location
   - `raw_data.csv`
   - `reference_data.xlsx`

3. **Browser Not Opening**: Dashboard saves to `data_quality_dashboard.html`
   - Open manually in your preferred browser

4. **Low Match Rates**: Adjust fuzzy threshold or check data quality
   ```python
   # Lower threshold for more matches
   threshold=0.75
   ```

## 🤝 Contributing

Feel free to enhance the tool with:
- Additional matching algorithms
- More visualization types
- Batch processing capabilities
- API integrations

## 📄 License

This project is open-source. Use at your own risk.

## 🆘 Support

For issues or questions:
1. Check the troubleshooting section
2. Review the code comments in `datamapper.py`
3. Examine the generated `quality_report.csv` for insights

---
