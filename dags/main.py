from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

# Define default arguments
default_args = {
    "owner": "nflavier",
    "start_date": datetime(2023, 1, 25),  # Set to a past date to allow immediate execution
    # Removed 'catchup' from default_args
}

# Define the DAG
dag = DAG(
    dag_id='hello_nitin',
    default_args=default_args,
    schedule_interval=timedelta(days=1),  # Correct parameter name
    catchup=False,  # Moved catchup out of default_args
)

# Define tasks using the DAG
t1 = BashOperator(
    task_id="hello_text_msg_1",
    bash_command='echo "Hello Nitin"',
    dag=dag,
)

t2 = BashOperator(
    task_id="hello_text_msg_2",
    bash_command='echo "Hello data"',
    dag=dag,
)

# Set task dependencies
t1 >> t2
