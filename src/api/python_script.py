# from datetime import datetime, timedelta
# import random

# # Define the start and end dates for 2024
# start_date = datetime(2024, 1, 1)
# end_date = datetime(2024, 12, 31)

# # Open a file to write the SQL statements
# with open('insert_statements.sql', 'w') as file:
#     current_date = start_date
#     while current_date <= end_date:
#         # Generate a unique ID (e.g., based on date)
#         id = current_date.strftime("%Y%m%d")
#         date = current_date.strftime("%Y-%m-%d")
#         value = random.randint(1, 1000)  # Generate a random value between 1 and 1000

#         # Write the SQL INSERT statement
#         sql = f"INSERT INTO sample_table (id, date, value) VALUES ({id}, '{date}', {value});\n"
#         file.write(sql)

#         # Move to the next day
#         current_date += timedelta(days=1)

# print("SQL INSERT statements with random values generated in 'insert_statements.sql'")

from datetime import datetime, timedelta
import random
import uuid

# Define the start and end dates for 2024
start_date = datetime(2024, 1, 1)
end_date = datetime(2024, 12, 31)

# Open a file to write the SQL statements
with open('insert_statements.sql', 'w') as file:
    current_date = start_date
    while current_date <= end_date:
        # Generate a unique UUID for each entry
        transaction_id = uuid.uuid4()
        
        # Format the current date as a timestamp
        created_at = current_date.strftime("%Y-%m-%d %H:%M:%S.%f")
        
        # Generate a random amount between 1 and 1000
        amount = round(random.uniform(1, 1000), 2)

        # Write the SQL INSERT statement
        sql = f"INSERT INTO transactions (id, amount, created_at) VALUES ('{transaction_id}', {amount}, '{created_at}');\n"
        file.write(sql)

        # Move to the next day
        current_date += timedelta(days=1)

print("SQL INSERT statements with random values generated in 'insert_statements.sql'")
