import json
import requests
import pandas as pd

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator


def get_data(**kwargs):
    url = 'https://raw.githubusercontent.com/airscholar/ApacheFlink-SalesAnalytics/main/output/new-output.csv'
    response = requests.get(url)

    if response.status_code == 200:
        df = pd.read_csv(url,header=None,names=['Category','Price','Quantity'])

        # convert dataframe to json 
        json_data = df.to_json(orient='records')
        kwargs['ti'].xcom_push(key='data',value=json_data)

    else:
        raise Exception(f'Failed to get data, response: {response.status_code}')

def preview_data(**kwargs):

    output_data = kwargs['ti'].xcom_pull(key='data',task_ids='get_data')
    print(output_data)

    if output_data:
        output_data = json.loads(output_data)
    else:
        raise ValueError("No data received from Xcom")
    
    df = pd.DataFrame(output_data)

    #Compute total sales
    df['Total'] = df['Price'] * df['Quantity']

    df = df.groupby('Category', as_index=False).agg({'Quantity': 'sum', 'Total': 'sum'})

    #sort by total sales
    df = df.sort_values(by='Total', ascending=False)

    print(df[['Category', 'Total']].head(20))


default_args = {
    "owner": 'nflavier',
    "start_date": datetime(2024, 8, 25),
}

# Define the DAG
dag = DAG(
    dag_id='fetch_preview_data',
    default_args=default_args,
    schedule_interval=timedelta(days=1),  # Correct parameter name
    catchup=False,  # Moved catchup out of default_args
)

get_data_from_url = PythonOperator(
    task_id="get_data",
    python_callable=get_data,
    dag = dag
)

preview_data_from_url = PythonOperator(
    task_id = 'preview_data',
    python_callable=preview_data,
    dag = dag
)

get_data_from_url >> preview_data_from_url