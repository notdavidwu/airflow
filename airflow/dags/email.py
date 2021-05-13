from airflow.models import DAG
from airflow.operators.email_operator import EmailOperator
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
from tempfile import NamedTemporaryFile


dag = DAG(
    "email_example",
    description="Sample Email Example with File attachments",
    schedule_interval="@daily",
    start_date=datetime(2021, 5, 12),
    catchup=False,
)


def build_email(**context):
    with NamedTemporaryFile(mode='w+', suffix=".txt") as file:
        file.write("Hello World")

        email_op = EmailOperator(
            task_id='send_email',
            to="davidwu5858@gmail.com",
            subject="Test Email Please Ignore",
            html_content=None,
            files=[file.name],
        )
        email_op.execute(context)


email_op_python = PythonOperator(
    task_id="python_send_email", python_callable=build_email, provide_context=True, dag=dag
)
