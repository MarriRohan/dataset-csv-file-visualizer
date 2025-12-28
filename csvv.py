import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from tkinter import Tk, filedialog

# ---------- FILE PICKER ----------
Tk().withdraw()  # hide tkinter window
CSV_FILE = filedialog.askopenfilename(
    title="Select CSV file",
    filetypes=[("CSV Files", "*.csv")]
)

if not CSV_FILE:
    raise FileNotFoundError("No CSV file selected")

# ---------- LOAD CSV ----------
df = pd.read_csv(CSV_FILE)

print("Loaded file:", CSV_FILE)

# ---------- CHECK DATA ----------
if df.empty:
    raise ValueError("CSV file is empty")

# ---------- SELECT NUMERIC COLUMNS ----------
numeric_cols = df.select_dtypes(include=np.number).columns

if len(numeric_cols) == 0:
    raise ValueError("No numeric columns found in CSV")

names_col = df.columns[0]   # assuming first column is Name

os.makedirs("charts", exist_ok=True)

report_sections = []

# ---------- ANALYSIS ----------
for col in numeric_cols:
    values = df[col]

    q1 = values.quantile(0.25)
    q3 = values.quantile(0.75)

    impact = []
    for v in values:
        if v >= q3:
            impact.append("HIGH")
        elif v <= q1:
            impact.append("LOW")
        else:
            impact.append("MEDIUM")

    df[f"{col}_Impact"] = impact

    # ---------- BAR CHART ----------
    plt.figure(figsize=(9,4))
    colors = ["red" if i=="HIGH" else "blue" if i=="LOW" else "gold" for i in impact]
    plt.bar(df[names_col], values, color=colors)
    plt.title(f"{col} – Bar Chart (Impact View)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f"charts/{col}_bar.png")
    plt.close()

    # ---------- PIE CHART ----------
    high = impact.count("HIGH")
    medium = impact.count("MEDIUM")
    low = impact.count("LOW")

    plt.figure(figsize=(5,5))
    plt.pie(
        [high, medium, low],
        labels=["High", "Medium", "Low"],
        colors=["red", "gold", "blue"],
        autopct="%1.1f%%",
        startangle=140
    )
    plt.title(f"{col} – Impact Distribution (Pie)")
    plt.savefig(f"charts/{col}_pie.png")
    plt.close()

    # ---------- SEPARATE LINE CHART ----------
    plt.figure(figsize=(9,4))
    plt.plot(df[names_col], values, marker="o")
    plt.title(f"{col} – Separate Trend Chart")
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f"charts/{col}_line.png")
    plt.close()

    report_sections.append(f"""
    <h3>{col} Analysis</h3>
    <ul>
      <li><b>Mean:</b> {values.mean():.2f}</li>
      <li><b>Max:</b> {values.max()}</li>
      <li><b>Min:</b> {values.min()}</li>
      <li><b>High:</b> {high}</li>
      <li><b>Medium:</b> {medium}</li>
      <li><b>Low:</b> {low}</li>
    </ul>

    <h4>Bar Chart</h4>
    <img src="charts/{col}_bar.png" width="700">

    <h4>Pie Chart</h4>
    <img src="charts/{col}_pie.png" width="400">

    <h4>Separate Trend Chart</h4>
    <img src="charts/{col}_line.png" width="700">
    """)

  # --- Find industry column ---
industry_col = None
for col in df.columns:
    if "industry" in col.lower():
        industry_col = col
        break

if not industry_col:
    raise ValueError("Industry column not found in CSV")

# --- Find net worth column ---
worth_col = None
for col in df.columns:
    if "worth" in col.lower():
        worth_col = col
        break

if not worth_col:
    raise ValueError("Net worth column not found in CSV")
    # ---------- BAR CHART ----------
    plt.figure(figsize=(8,4))
    colors = ["red" if i=="HIGH" else "blue" if i=="LOW" else "gold" for i in impact]
    plt.bar(df[names_col], values, color=colors)
    plt.title(f"{col} Impact Analysis")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f"charts/{col}_bar.png")
    plt.close()

    report_sections.append(f"""
    <h3>{col} Analysis</h3>
    <ul>
      <li>Mean: {values.mean():.2f}</li>
      <li>Max: {values.max()}</li>
      <li>Min: {values.min()}</li>
      <li>High Impact Count: {impact.count("HIGH")}</li>
      <li>Low Impact Count: {impact.count("LOW")}</li>
    </ul>
    """)

# ---------- HEATMAP ----------
plt.figure(figsize=(6,4))
sns.heatmap(df[numeric_cols], annot=True, cmap="coolwarm")
plt.title("Numeric Data Heatmap")
plt.tight_layout()
plt.savefig("charts/heatmap.png")
plt.close()

# ---------- HTML REPORT ----------
html = f"""
<html>
<head>
<title>CSV Impact Report</title>
<style>
body {{ font-family: Arial; padding:20px; background:#f8fafc }}
table {{ border-collapse: collapse; width:100% }}
td, th {{ border:1px solid #ccc; padding:6px }}
</style>
</head>

<body>
<h1>📊 CSV Impact Analysis Report</h1>

<h2>Complete Dataset</h2>
{df.to_html(index=False)}

<h2>Insights</h2>
{''.join(report_sections)}

<h2>Charts</h2>
"""

for col in numeric_cols:
    html += f'<img src="charts/{col}_bar.png" width="600"><br>'

html += '<img src="charts/heatmap.png" width="600">'

html += """
</body>
</html>
"""

with open("report.html", "w") as f:
    f.write(html)

print("✅ SUCCESS: report.html generated")
