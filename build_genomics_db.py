import sqlite3
import pandas as pd

print("💾 Initializing SQL Relational Database...")

# 1. Connect to SQLite database (creates file automatically if it doesn't exist)
db_name = "genomics_warehouse.db"
conn = sqlite3.connect(db_name)
cursor = conn.cursor()

# 2. Create table structure of relational database
print("🏗️ Creating 'mutations' table with strict relational data schema...")
cursor.execute("""
    CREATE TABLE IF NOT EXISTS mutations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        gene_id TEXT NOT NULL,
        chromosome TEXT NOT NULL,
        position INTEGER NOT NULL,
        reference_allele TEXT NOT NULL,
        mutant_allele TEXT NOT NULL,
        clinical_significance TEXT NOT NULL
    )
""")
conn.commit()

# 3. Read clean mutations/variants CSV file (Perl output) into Pandas
print("📊 Ingesting clean mutations/variants (Perl output matrix)...")
csv_file = "clean_mutations.csv"
df = pd.read_csv(csv_file)

# Lowercase column headers to ensure they perfectly match SQL table names
df.columns = [c.lower() for c in df.columns]

# 4. Insert pandas dataframe rows directly into relational SQL structure
print("🔀 Streaming data arrays into SQL table rows...")
df.to_sql("mutations", conn, if_exists="append", index=False)

# 5. Run quick verification query to check SQL database
print("\n🔍 Running SQL verification query...")
cursor.execute("""
    SELECT gene_id, COUNT(*), clinical_significance 
    FROM mutations 
    GROUP BY gene_id, clinical_significance
""")
rows = cursor.fetchall()

print("--- SQL VERIFICATION REPORT ---")
for row in rows:
    print(f"🧬 Gene: {row[0]} | Observations Count: {row[1]} | Classification: {row[2]}")

# Safely close database connection
conn.close()
print("\n🎉 Success! SQL Database generated and verified as: genomics_warehouse.db")
