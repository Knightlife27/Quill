from datetime import datetime, timedelta
import random
import uuid


start_date = datetime(2024, 1, 1)
end_date = datetime(2024, 12, 31)


with open('insert_statements.sql', 'w') as file:
    current_date = start_date
    while current_date <= end_date:
        
        transaction_id = uuid.uuid4()
        
       
        created_at = current_date.strftime("%Y-%m-%d %H:%M:%S.%f")
        
        
        amount = round(random.uniform(1, 1000), 2)

        
        sql = f"INSERT INTO transactions (id, amount, created_at) VALUES ('{transaction_id}', {amount}, '{created_at}');\n"
        file.write(sql)

       
        current_date += timedelta(days=1)

print("SQL INSERT statements with random values generated in 'insert_statements.sql'")
