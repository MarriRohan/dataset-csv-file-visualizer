import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import re
from tkinter import Tk, filedialog

# ---------- HELPER: SAFE FILE NAMES ----------
def safe_filename(name):
    """
    Convert any string into a safe filename.
    Removes invalid characters and replaces spaces.
    """
    name = re.sub(r'[\\/*?:"<>|]', "", name)
    name = name.replace(" ", "_")
    return name

# ---------- FILE PICKER ----------
Tk().withdraw()
csv_path = filedialog.askopenfilename(
    title="Select any CSV file",
    filetypes=[("CSV Files", "*.csv")]
)

if not csv_path:
    raise FileNotFoundError("No CSV file selected")

# ---------- LOAD CSV ----------
df = pd.read_csv(csv_path)
print("Loaded file:", csv_path)

if df.empty:
    raise ValueError("CSV file is empty")

# ---------- SETUP ----------
os.makedirs("charts", exist_ok=True)
report_sections = []

numeric_cols = df.select_dtypes(include="number").columns
categorical_cols = df.select_dtypes(exclude="number").columns

# ---------- NUMERIC COLUMNS VISUALIZATION ----------
for col in numeric_cols:
    values = df[col].dropna()
    safe_col = safe_filename(col)

    if values.empty:
        continue

    # BAR CHART
    plt.figure(figsize=(8,4))
    plt.bar(range(len(values)), values)
    plt.title(f"{col} - Bar Chart")
    plt.tight_layout()
    plt.savefig(f"charts/{safe_col}_bar.png")
    plt.close()

    # PIE CHART (BINNED)
    plt.figure(figsize=(5,5))
    values.value_counts(bins=3).plot.pie(autopct="%1.1f%%")
    plt.title(f"{col} - Distribution")
    plt.ylabel("")
    plt.tight_layout()
    plt.savefig(f"charts/{safe_col}_pie.png")
    plt.close()

    # LINE CHART
    plt.figure(figsize=(8,4))
    plt.plot(values.reset_index(drop=True))
    plt.title(f"{col} - Trend")
    plt.tight_layout()
    plt.savefig(f"charts/{safe_col}_line.png")
    plt.close()

    report_sections.append(f"""
    <h3>Numeric Column: {col}</h3>
    <img src="charts/{safe_col}_bar.png" width="600"><br>
    <img src="charts/{safe_col}_pie.png" width="400"><br>
    <img src="charts/{safe_col}_line.png" width="600"><br>
    """)

# ---------- CATEGORICAL COLUMNS VISUALIZATION ----------
for col in categorical_cols:
    counts = df[col].value_counts().head(10)
    safe_col = safe_filename(col)

    if counts.empty:
        continue

    plt.figure(figsize=(8,4))
    counts.plot(kind="bar")
    plt.title(f"{col} - Category Distribution (Top 10)")
    plt.tight_layout()
    plt.savefig(f"charts/{safe_col}_category.png")
    plt.close()

    report_sections.append(f"""
    <h3>Categorical Column: {col}</h3>
    <img src="charts/{safe_col}_category.png" width="600"><br>
    """)

# ---------- HEATMAP ----------
if len(numeric_cols) >= 2:
    plt.figure(figsize=(7,5))
    sns.heatmap(df[numeric_cols].corr(), annot=True, cmap="coolwarm")
    plt.title("Correlation Heatmap")
    plt.tight_layout()
    plt.savefig("charts/heatmap.png")
    plt.close()

    report_sections.append("""
    <h3>Correlation Heatmap</h3>
    <img src="charts/heatmap.png" width="600"><br>
    """)

# ---------- HTML REPORT ----------
html = f"""
<html>
<head>
<title>CSV Visualization Report</title>
<style>
body {{
    font-family: Arial;
    padding: 20px;
}}
img {{
    margin-bottom: 20px;
}}
</style>
</head>

<body>
<h1>CSV Dataset Visualization Report</h1>

<h2>Dataset Preview (First 50 Rows)</h2>
{df.head(50).to_html(index=False)}

<h2>Visual Analysis</h2>
{''.join(report_sections)}

</body>
</html>
"""

with open("report.html", "w") as f:
    f.write(html)

print("SUCCESS: report.html generated")
