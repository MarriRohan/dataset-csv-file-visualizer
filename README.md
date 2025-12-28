# CSV Dataset Visualizer and Insight Generator

A Python-based data analysis and visualization tool that processes CSV datasets and generates rankings, insights, and visual charts such as bar charts, pie charts, line charts, and heatmaps.  
The project produces an auto-generated HTML report for easy analysis and sharing.

---

## Project Overview

The CSV Dataset Visualizer helps users understand datasets by:
- Analyzing numeric and categorical columns
- Ranking entities based on meaningful criteria
- Visualizing distributions and trends
- Generating a structured HTML report

This project is suitable for academic projects, data analysis practice, hackathons, and portfolios.

---

## Features

- Upload and analyze any CSV file
- Displays the complete dataset without hiding rows
- Automatically detects numeric columns
- Classifies values into High, Medium, and Low impact
- Generates multiple visualizations:
  - Bar charts
  - Pie charts
  - Line (trend) charts
  - Heatmaps
- Produces ranking-based insights such as:
  - Industries that created the most rich individuals
  - Youngest individuals ranked by age
- Creates a downloadable HTML report

---

## Example Insights

- Industry-wise ranking by number of wealthy individuals
- Age-based rankings (youngest to oldest)
- Distribution of values across categories
- High vs Low impact analysis
- Summary statistics (mean, minimum, maximum)

---

## Tech Stack

| Category | Tools |
|--------|------|
| Language | Python |
| Data Processing | pandas, numpy |
| Visualization | matplotlib, seaborn |
| File Selection | tkinter |
| Output Format | HTML |

---

## How to Run

### Step 1: Clone the Repository
 ```sh
git clone <your-repository-url>
cd csv-dataset-visualizer
 ```
### Step 2: Install Dependencies
 ```sh
pip install pandas numpy matplotlib seaborn 
 ```
### Step 3: Run the Script
 ```sh
python csvv.py 
 ```
### Step 4: Select CSV File
A file selection dialog will open.
Choose any CSV file to begin analysis.
### Step 5: View the Report
Open report.html in a web browser to view the generated analysis and charts.

