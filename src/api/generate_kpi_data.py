import requests
from datetime import datetime, timedelta
import random

BASE_URL = "https://musical-giggle-x5w45qppjpwghpg9p-3001.app.github.dev/api"  # Replace with your actual API URL

def get_dashboards():
    response = requests.get(f"{BASE_URL}/dashboards")
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch dashboards: {response.text}")
        return None

def create_kpi_metric(dashboard_id, kpi_type, metric_name, metric_value, metric_unit, date):
    data = {
        "dashboard_id": dashboard_id,
        "kpi_type": kpi_type,
        "metric_name": metric_name,
        "metric_value": metric_value,
        "metric_unit": metric_unit,
        "date": date.strftime('%Y-%m-%d')
    }
    response = requests.post(f"{BASE_URL}/create-kpi-metric", json=data)
    return response.status_code == 201

def populate_kpi_data():
    dashboards = get_dashboards()
    if not dashboards:
        print("No dashboards found. Exiting.")
        return

    start_date = datetime(2024, 1, 1)
    end_date = datetime(2025, 1, 1)
    current_date = start_date

    kpi_configs = [
        {"type": "kpi1", "name": "Total Revenue", "unit": "USD", "min": 100000, "max": 500000},
        {"type": "kpi2", "name": "Number of Orders", "unit": "Count", "min": 500, "max": 2000},
        {"type": "kpi3", "name": "Average Order Value", "unit": "USD", "min": 100, "max": 500}
    ]

    while current_date < end_date:
        for dashboard in dashboards:
            for kpi in kpi_configs:
                metric_value = round(random.uniform(kpi["min"], kpi["max"]), 2)
                success = create_kpi_metric(
                    dashboard['id'],
                    kpi['type'],
                    kpi['name'],
                    metric_value,
                    kpi['unit'],
                    current_date
                )
                if success:
                    print(f"Created {kpi['type']} for dashboard {dashboard['name']} on {current_date.date()}")
                else:
                    print(f"Failed to create {kpi['type']} for dashboard {dashboard['name']} on {current_date.date()}")
        
        current_date += timedelta(days=1)

    print("Data population complete!")

if __name__ == "__main__":
    populate_kpi_data()