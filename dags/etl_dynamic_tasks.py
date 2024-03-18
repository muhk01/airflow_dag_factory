from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.utils.dates import days_ago
from airflow.utils.task_group import TaskGroup
from datetime import datetime, timedelta
import yaml

# Create tasks from YAML file

def create_task(task_config, dag):
    task_id = task_config['task_id']
    operator = eval(task_config['operator'])
    bash_command = task_config['bash_command']

    return operator(task_id=task_id, bash_command=bash_command, dag=dag, depends_on_past=False)

def create_task_group(task_group_config, dag):
    with TaskGroup(group_id=task_group_config['task_group_id']) as tg:
        tasks = {}
        for task_config in task_group_config['tasks']:
            task = create_task(task_config, dag)
            task_id = task_config['task_id']
            tasks[task_id] = task

        for task_config in task_group_config['tasks']:
            task_id = task_config['task_id']
            task = tasks[task_id]
            dependencies = task_config.get('dependencies', [])
            for dep_task_id in dependencies:
                if dep_task_id in tasks:
                    tasks[dep_task_id] >> task

    return tg, tasks

with DAG(
    "etl_dynamic_tasks",
    default_args={
        'owner': 'airflow',
        'email': 'muhamadkoirul@gmail.com',
        'email_on_failure': True,
        'email_on_retry': False,
        'retries': 5,
        'retry_delay': timedelta(minutes=5)       
    },

    start_date=datetime(2022, 7, 13),
    schedule_interval=None,
    catchup=False,
    tags=['daily'],
) as dag:

    with open('..../yaml/etl_dynamic_tasks.yaml', 'r') as file:
        config = yaml.safe_load(file)

    tasks = {}

    for task_config in config['tasks']:
        if 'task_group_id' in task_config:
            task_group, task_group_tasks = create_task_group(task_config, dag)
            tasks[task_group.group_id] = task_group
            tasks.update(task_group_tasks)
            
            for dep_task_id in task_config.get('dependencies', []):
                if dep_task_id in tasks:
                    tasks[dep_task_id] >> task_group
        
        else:
            task = create_task(task_config, dag)
            tasks[task_config['task_id']] = task

            for dep_task_id in task_config.get('dependencies', []):
                tasks[dep_task_id] >> task
