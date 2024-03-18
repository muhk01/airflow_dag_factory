# airflow_dag_factory
DAG Factory implementation using YAML files

# Create 'yaml' Folder
First create YAML folder in same path with DAG Files.

# Config YAML files as Following example
Config YAML files, now without Python coding understanding, we can create a pipeline just using YAML files.

# YAML Configuration
```
tasks:
  - task_id: task1
    operator: BashOperator
    bash_command: "echo 'Task 1'"
    dependencies: []

  - task_group_id: this_task_group
    tasks:
      - task_id: task3
        operator: BashOperator
        bash_command: "echo 'Task 3'"
        dependencies: []

      - task_id: task22
        operator: BashOperator
        bash_command: "echo 'Task 3'"
        dependencies: [task3]

      - task_id: task4
        operator: BashOperator
        bash_command: "echo 'Task 4'"
        dependencies: [task22]

      - task_id: task5
        operator: BashOperator
        bash_command: "echo 'Task 4'"
        dependencies: [task22]
      
      - task_id: task70
        operator: BashOperator
        bash_command: "echo 'Task 4'"
        dependencies: [task5]

      - task_id: task80
        operator: BashOperator
        bash_command: "echo 'Task 4'"
        dependencies: [task5]
      
      - task_id: task90
        operator: BashOperator
        bash_command: "echo 'Task 4'"
        dependencies: [task5]
      
      - task_id: task100
        operator: BashOperator
        bash_command: "echo 'Task 4'"
        dependencies: [task22, task70, task4]

    dependencies: [task1]

  - task_id: task2
    operator: BashOperator
    bash_command: "echo 'Task 2'"
    dependencies: [this_task_group]
  
  - task_id: task10
    operator: BashOperator
    bash_command: "echo 'Task 2'"
    dependencies: [task2]
  
  - task_id: task11
    operator: BashOperator
    bash_command: "echo 'Task 2'"
    dependencies: [task2]
  
  - task_id: task110
    operator: BashOperator
    bash_command: "echo 'Task 2'"
    dependencies: [task10, task11]
```
# Result
![result](https://raw.githubusercontent.com/muhk01/airflow_dag_factory/main/img/DAGFactory.PNG)

# Additional workaround
Some bash script may require an argument, an additional placeholder and argument thrown from DAG script may required.
