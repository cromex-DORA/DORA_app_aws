from dotenv import load_dotenv
import boto3
import os
import io
from tempfile import NamedTemporaryFile
from pyexcel_ods3 import get_data
load_dotenv()

environment = os.getenv('ENVIRONMENT')

################################################
#aws
################################################
bucket_files_common = os.getenv('S3_BUCKET_COMMON_FILES')
bucket_files_custom = os.getenv('S3_BUCKET_USERS_FILES')

s3_region = os.getenv('S3_UPLOADS_REGION')
s3_access_key = os.getenv('S3_UPLOADS_ACCESS_KEY')
s3_secret_key = os.getenv('S3_UPLOADS_SECRET_KEY')


s3 = boto3.client(
    's3',
    region_name=s3_region,
    aws_access_key_id=s3_access_key,
    aws_secret_access_key=s3_secret_key
)

s3r = boto3.resource('s3',
    region_name=s3_region,
    aws_access_key_id=s3_access_key,
    aws_secret_access_key=s3_secret_key
)


################################################
#Dossier Docker
################################################
def definir_PATH_DOSSIER_MAITRE_racine():
    if environment =="developpement":
        PATH_DOSSIER_BDD_DORA = "/mnt/d/projet_DORA"
    if environment =="production":  
        PATH_DOSSIER_BDD_DORA = "./projet_DORA"  
    return PATH_DOSSIER_BDD_DORA

def conv_s3_obj_vers_python_obj(type_bucket,file_name):
    file_name = file_name.replace("\\","/")
    if type_bucket == "config":
        nom_bucket = bucket_files_common
    if type_bucket == "custom":
        nom_bucket = bucket_files_custom
    csv_obj = s3.get_object(Bucket=nom_bucket,Key=file_name)
    if file_name.split(".")[-1]=="csv":
        csv_content = csv_obj['Body'].read().decode('utf-8')
        obj_python = io.StringIO(csv_content)
    if file_name.split(".")[-1] in ["ods","xlsx","xlsm"]:
        obj_python = csv_obj['Body'].read()
    return obj_python

def get_file_path_racine(file_name):
    if environment == 'production':
        file_name = file_name.replace("\\","/")
        # Chemin pour accéder aux fichiers S3
        s3_file_path = f's3://{bucket_files_common}/{file_name}'
        return s3_file_path
    if environment == 'developpement':
        file_name = file_name.replace("\\","/")
        local_file_path = os.path.join(definir_PATH_DOSSIER_MAITRE_racine(),file_name)
        return local_file_path
    
def upload_file_vers_s3(type_bucket,file,path):
    
    def upload_workbook(workbook, bucket, key):
        with NamedTemporaryFile() as tmp:
            workbook.save(tmp.name)
            tmp.seek(0)
            s3r.meta.client.upload_file(tmp.name, bucket, key)  

    if type_bucket == "config":
        nom_bucket = bucket_files_common
    if type_bucket == "custom":
        nom_bucket = bucket_files_custom
    extension = os.path.splitext(path)[1][1:]
    if extension == "xlsx":
        upload_workbook(file, nom_bucket, path)
    
def download_file_from_s3(type_bucket,file_key):
    if type_bucket == "config":
        nom_bucket = bucket_files_common
    if type_bucket == "custom":
        nom_bucket = bucket_files_custom   
    complet_path = os.path.join("MO_gemapi",file_key)
    url = s3.generate_presigned_url(
        'get_object',
        Params={
            'Bucket': nom_bucket,
            'Key': complet_path
        },
        ExpiresIn=100
    )
    return url
    
