"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """"""


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """"""

import sqlite3

conn = sqlite3.connect("interview.db")
c = conn.cursor()

# * List of tables to union
table_list = ["roster_1", "roster_2", "roster_3", "roster_4", "roster_5"]

# * Base query
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
        AND eligibility_end_date >= '2022-05-01'
"""

# * Create a union query for each table
union_query = " UNION ALL ".join(query.format(table) for table in table_list)

# * Create the new table
c.executescript(
    f"DROP TABLE IF EXISTS std_member_info; CREATE TABLE std_member_info AS {union_query};"
)

# * Commit changes to DB and close connection
conn.commit()
conn.close()


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """"""


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """"""


# Heading Printer
def print_header(text):
    print("\n")
    print("-" * len(text))
    print(text)
    print("-" * len(text))
    print("\n")


conn = sqlite3.connect("interview.db")
c = conn.cursor()


# ! How many distinct members are eligible in April 2022?


query_eligible_members = """
                            SELECT 
                                COUNT(DISTINCT member_id) as '# of Distinct Members'
                                FROM std_member_info
"""

# Execute the query and fetch the result
c.execute(query_eligible_members)
num_eligible_members = c.fetchone()[0]

print_header("Distinct Members Eligible in April 2022")
print(
    f"\tNumber of distinct members eligible in April 2022: \033[1;30;47m{num_eligible_members}\033[0m\n"
)


# ! How many members were included more than once?


query_duplicated_members = """
                            SELECT 
                                COUNT(member_id) - COUNT(DISTINCT member_id) as '# of Duplicated Members'
                                FROM std_member_info
"""


# Execute the query and fetch the result
c.execute(query_duplicated_members)
num_duplicated_members = c.fetchone()[0]

print_header("Members Included More Than Once")
print(
    f"\tNumber of members included more than once: \033[1;30;47m{num_duplicated_members}\033[0m\n"
)


# ! What is the breakdown of members by payer?


query_by_payer = """
                    SELECT
                        payer, COUNT(DISTINCT member_id)
                        FROM std_member_info
                        GROUP BY payer
"""


# Execute the query and fetch the result
c.execute(query_by_payer)
breakdown_by_payer = c.fetchall()

print_header("Breakdown of Members by Payer")
for payer, count in breakdown_by_payer:
    print(
        f"\tPayer: \033[1;30;47m{payer}\033[0m   |   Members: \033[1;30;47m{count}\033[0m\n"
    )


# ! How many members live in a zip code with a food_access_score lower than 2?


query_food_access = """
                    SELECT COUNT(DISTINCT smi.member_id) 
                        FROM std_member_info smi 
                        JOIN model_scores_by_zip msbz ON smi.zip_code = msbz.zcta 
                        WHERE msbz.food_access_score < 2
"""


# Execute the query and fetch the result
c.execute(query_food_access)
num_members_food_access = c.fetchone()[0]

print_header("Members with Food Access Score Lower Than 2")
print(
    f"\tNumber of members living in a zip code with a food access score lower than 2: \033[1;30;47m{num_members_food_access}\033[0m\n"
)


# ! What is the average social isolation score for the members?


# Query for the average social isolation score for the members
query_social_isolation = """
                        SELECT AVG(msbz.social_isolation_score) 
                            FROM std_member_info smi 
                            JOIN model_scores_by_zip msbz ON smi.zip_code = msbz.zcta
"""

# Execute the query and fetch the result
c.execute(query_social_isolation)
avg_social_isolation_score = c.fetchone()[0]

print_header("Average Social Isolation Score for Members")
print(
    f"\tAverage social isolation score for the members: \033[1;30;47m{avg_social_isolation_score}\033[0m\n"
)


# ! Which members live in the zip code with the highest algorex_sdoh_composite_score?


# Query for the members living in the zip code with the highest algorex_sdoh_composite_score
query_algorex_score = """
                        SELECT smi.member_id 
                            FROM std_member_info smi 
                            JOIN model_scores_by_zip msbz ON smi.zip_code = msbz.zcta 
                            WHERE msbz.algorex_sdoh_composite_score = 
                                (SELECT MAX(algorex_sdoh_composite_score) FROM model_scores_by_zip)
"""

# Execute the query and fetch the result
c.execute(query_algorex_score)
members_max_algorex_score = c.fetchall()

print_header("Members Living in Zip with Highest Algorex SDOH Composite Score")
for member in members_max_algorex_score:
    print(f"\tMember ID:  \033[1;30;47m{member[0]}\033[0m")
print("\n")


# Close the connection
conn.close()
