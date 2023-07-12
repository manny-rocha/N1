import sqlite3

conn = sqlite3.connect('interview.db')

c = conn.cursor()

# Select all members from roster_(#) who are eligible during April 2022
# res = c.execute("SELECT * FROM roster_1 WHERE eligibility_start_date <= '2022-04-01' AND eligibility_end_date >= '2022-04-30'")

# List of tables to union
table_list = ['roster_1', 'roster_2', 'roster_3', 'roster_4', 'roster_5']

# Base query
query = """
    SELECT 
        Person_Id as member_id,
        First_Name as member_first_name,
        Last_Name as member_last_name,
        Dob as date_of_birth,
        Street_Address as main_address,
        City as city,
        State as state,
        Zip as zip_code,
        payer as payer
    FROM {} 
        WHERE eligibility_start_date <= '2022-04-01' 
        AND eligibility_end_date >= '2022-04-30';
"""

# Create a union query for each table
union_query = " UNION ALL ".join(query.format(table) for table in table_list)

# Create the new table
c.execute(f"CREATE TABLE std_member_info IF NOT EXISTS AS {union_query}")

# Commit changes to DB and close connection
conn.commit()
conn.close()