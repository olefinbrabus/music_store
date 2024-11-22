import requests
import random
import time
import pandas as pd

BASE_URL = "http://127.0.0.1:5000"

HEADERS = {
    "Connection": "Close"
}


def populate_data(count):
    for i in range(count):
        data = {
            "name": f"Instrument_{i}",
            "price": round(random.uniform(100, 1000), 2),
            "category_id": 1
        }
        response = requests.post(f"{BASE_URL}/instruments", json=data, headers=HEADERS)
        if response.status_code != 200:
            print(f"Error inserting data: {response.json()}")


def measure_query_execution_time(function, *args):
    start_time = time.time()
    function(*args)
    end_time = time.time()
    return end_time - start_time


def test_select():
    response = requests.get(f"{BASE_URL}/instruments", headers=HEADERS)
    if response.status_code != 200:
        print(f"Error fetching data: {response.json()}")


def test_insert():
    data = {
        "name": "Test_Instrument",
        "price": round(random.uniform(100, 1000), 2),
        "category_id": 1
    }
    response = requests.post(f"{BASE_URL}/instruments", json=data, headers=HEADERS)
    if response.status_code != 200:
        print(f"Error inserting data: {response.json()}")


def test_update():
    data = {"name": "Updated_Instrument", "price": 500.0, "category_id": 1}
    response = requests.put(f"{BASE_URL}/instruments/1", json=data, headers=HEADERS)
    if response.status_code != 200:
        print(f"Error updating data: {response.json()}")


def test_delete():
    response = requests.delete(f"{BASE_URL}/instruments/1", headers=HEADERS)
    if response.status_code != 200:
        print(f"Error deleting data: {response.json()}")


test_sizes = [1000, 10000]
results = []

for size in test_sizes:
    print(f"Testing with {size} records...")

    populate_time = measure_query_execution_time(populate_data, size)

    select_time = measure_query_execution_time(test_select)
    insert_time = measure_query_execution_time(test_insert)
    update_time = measure_query_execution_time(test_update)
    delete_time = measure_query_execution_time(test_delete)

    results.append({
        "size": size,
        "populate_time": populate_time,
        "select_time": select_time,
        "insert_time": insert_time,
        "update_time": update_time,
        "delete_time": delete_time
    })

    print(f"Completed testing for {size} records.")

df_results = pd.DataFrame(results)
print(df_results)

df_results.to_csv("api_performance_results.csv", index=False)