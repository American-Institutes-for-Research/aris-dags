from datetime import timedelta, datetime
from pickle import TRUE
import airflow
import code_executer
from airflow import DAG
from airflow.operators.python import PythonOperator, PythonVirtualenvOperator
from airflow.operators.python_operator import BranchPythonOperator
from airflow.contrib.operators.ssh_operator import SSHOperator
from airflow.contrib.hooks.ssh_hook import SSHHook
SERVICE_GIT_DIR = 'C:\\ARIS\\autoDigest\\ipeds' # File housing ARIS repos on SAS server's C drive

# default args
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email': ['mtrihn@air.org', 'gchickering@air.org'],
    'email_on_failure': TRUE,
    'email_on_retry': False,
    'start_date': datetime.now() - timedelta(minutes=20),
    'retries': 0,
    'retry_delay': timedelta(minutes=5),
}

# Define Main DAG for CCD pipeline 
dag = DAG(dag_id='aris_ccd_etl',
          default_args=default_args,
        #   schedule_interval='0,10,20,30,40,50 * * * *',
          dagrun_timeout=timedelta(seconds=600))


# def links():
#     '''
#     Purpose: execute ccd_data_list_downloader.py  on command line to generate list of CCD links
#     '''
#     ssh = SSHHook(ssh_conn_id="svc_202205_sasdev")
#     ssh_client = None
#     print(ssh)
#     try:
#         ssh_client = ssh.get_conn()
#         ssh_client.load_system_host_keys()
#         command = 'cd ' +  SERVICE_GIT_DIR + ' && python ' + '\\IO\\ccd_data_list_downloader.py' 
#         stdin, stdout, stderr = ssh_client.exec_command(command)
#         out = stdout.read().decode().strip()
#         error = stderr.read().decode().strip()
#         print(out)
#         print(error)
#     finally:
#         if ssh_client:
#             ssh_client.close()


# def dat():
#     '''
#     Purpose: execute ccd_data_downloader.py on command line to download CCD data 
#     '''
#     ssh = SSHHook(ssh_conn_id="svc_202205_sasdev")
#     ssh_client = None
#     print(ssh)
#     try:
        
#         ssh_client = ssh.get_conn()
#         ssh_client.load_system_host_keys()
#         command = 'cd ' +  SERVICE_GIT_DIR + ' && python ' +  'IO\\ccd_data_downloader.py'
#         stdin, stdout, stderr = ssh_client.exec_command(command)
#         out = stdout.read().decode().strip()
#         error = stderr.read().decode().strip()
#         print(out)
#         print(error)
#     finally:
#         if ssh_client:
#             ssh_client.close()

def Completion_Survey():
    '''
    Purpose: execute ccd_nonfiscal_state_RE2.sas on command line to generate nonfiscal long data from ccd data 
    '''
    ssh = SSHHook(ssh_conn_id="svc_202205_sasdev")
    ssh_client = None
    print(ssh)
    try:
        ssh_client = ssh.get_conn()
        ssh_client.load_system_host_keys()
        command = 'cd ' +  SERVICE_GIT_DIR + '\\SAS' + '\\d21' +'\\Completion Survey SAS code'  +' && sas ccd_nonfiscal_state_RE2'
        stdin, stdout, stderr = ssh_client.exec_command(command)
        out = stdout.read().decode().strip()
        error = stderr.read().decode().strip()
        print(out)
        print(error)
    finally:
        if ssh_client:
            ssh_client.close()

