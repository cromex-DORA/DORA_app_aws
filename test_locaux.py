
import pandas as pd
from app.DORApy.classes import Class_NDictGdf,Class_NGdfREF
from flask import Flask, send_from_directory, jsonify, request
from app.DORApy import gestion_admin,creation_tableau_vierge_DORA
from app.DORApy.decorators.token_admin import check_token_admin
from app.DORApy.classes import Class_Folder
from app.DORApy.classes.modules import connect_path,config_DORA
import os
import boto3
from tempfile import NamedTemporaryFile

bucket_files_common = os.getenv('S3_BUCKET_COMMON_FILES')
bucket_files_custom = os.getenv('S3_BUCKET_USERS_FILES')

s3_region = os.getenv('S3_UPLOADS_REGION')
s3_access_key = os.getenv('S3_UPLOADS_ACCESS_KEY')
s3_secret_key = os.getenv('S3_UPLOADS_SECRET_KEY')

###Fichiers config
import os

s3r = boto3.resource('s3',
    region_name=s3_region,
    aws_access_key_id=s3_access_key,
    aws_secret_access_key=s3_secret_key
)

def upload_workbook(workbook, bucket, key):
    with NamedTemporaryFile() as tmp:
        workbook.save(tmp.name)
        tmp.seek(0)
        s3r.meta.client.upload_file(tmp.name, bucket, key)

excel_modif = creation_tableau_vierge_DORA.create_tableau_vierge_DORA(["BORDEAUX METROPOLE"])

bucket_users_files = os.getenv('S3_BUCKET_USERS_FILES')
#excel_modif = config_DORA.recuperation_excel_MIA_MO_vierge_DORA()
path = os.path.join("MO_gemapi","MO_gemapi_10041","tableau_vierge_prout.xlsx")
upload_workbook(excel_modif, "doras3bdddorabucket", path)

#connect_path.upload_file_vers_s3("custom","doras3bdddorabucket",path)
#ajout_MO_ou_PPG.ajout_shp_MO_ou_PPG("PPG")

#couche_test = gpd.read_file("D:/projet_DORA/shp_files/ME/BV Me sup AG 2021.shp")
#couche_test.to_file("G:/travail/carto/projets basiques/PAOT global 5.0/test/test_ME.gpkg", driver='GPKG')
#gdf_ROE = gpd.read_file("D:/projet_DORA/shp_files/ROE/ROE_AG_2023.gpkg")
#gdf_SAGE = gpd.read_file("D:/projet_DORA/shp_files/SAGE/SAGE superficiels.shp")

#gdf_ME = gpd.read_file("D:/projet_DORA/shp_files/ME/BV Me sup AG 2021.shp")
#dict_gdf = Class_NDictGdf.chercher_gdf()
#user_folder = actualisation_dossier_MO()
