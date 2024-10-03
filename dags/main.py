from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    "owner": "nflavier",
    "start_date": datetime(2024,1,25),
    'catchup': False
}

dag = DAG(
    dag_id='hello_nitin',
    default_args = default_args,
    schedule = timedelta(days=1)
)

t1 = BashOperator(
    task_id = "hello_text_msg_1",
    bash_command = 'echo "Hello Nitin"',
    dag = dag
)

t2 = BashOperator(
    task_id = "hello_text_msg_2",
    bash_command = 'echo "Hello data"',
    dag = dag
)

t1 >> t2