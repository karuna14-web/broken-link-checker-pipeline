import pandas as pd
import os
from datetime import datetime

from checker import check_link
from db import create_connection, create_tables


# CHECK FILE
file_name = "urls.csv"

if not os.path.exists(file_name):
    print("File not found!")
    exit()

print("File found... starting project")


# READ CSV
data = pd.read_csv(file_name)

if 'url' not in data.columns:
    print("CSV must contain 'url' column")
    exit()

urls = data['url'].tolist()


# CHECK LINKS
valid_results = []
failed_results = []

print("\nChecking links...\n")

for u in urls:
    result = check_link(u)

    # add timestamp
    result.append(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    if result[4] == "Valid":
        valid_results.append(result)
    else:
        failed_results.append(result)

    print("Checked:", u)


# CONNECT DATABASE
conn = create_connection()
cursor = conn.cursor()

create_tables(cursor)


# INSERT VALID
for row in valid_results:
    cursor.execute("""
    INSERT INTO valid_links (url, status, time, final_url, domain, checked_on)
    VALUES (%s, %s, %s, %s, %s, %s)
    """, (row[0], row[1], row[2], row[3], row[5], row[6]))


# INSERT FAILED
for row in failed_results:
    cursor.execute("""
    INSERT INTO failed_links (url, status, time, final_url, domain, checked_on)
    VALUES (%s, %s, %s, %s, %s, %s)
    """, (row[0], row[1], row[2], row[3], row[5], row[6]))


conn.commit()
conn.close()


# FINAL REPORT
print("\n FINAL REPORT")
print("Total URLs:", len(urls))
print("Valid Links:", len(valid_results))
print("Failed Links:", len(failed_results))


# SAVE RESULTS TO FILE (VERY IMPORTANT PART)

valid_df = pd.DataFrame(valid_results, columns=[
    "url", "status", "time", "final_url", "category", "domain", "checked_on"
])

failed_df = pd.DataFrame(failed_results, columns=[
    "url", "status", "time", "final_url", "category", "domain", "checked_on"
])

valid_df.to_csv("valid_links_output.csv", index=False)
failed_df.to_csv("failed_links_output.csv", index=False)

print("\nResults also saved in CSV files!")