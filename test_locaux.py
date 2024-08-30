
import pandas as pd
from app.DORApy.classes import Class_NDictGdf,Class_NGdfREF
from flask import Flask, send_from_directory, jsonify, request
from app.DORApy import gestion_admin,creation_tableau_vierge_DORA
from app.DORApy.decorators.token_admin import check_token_admin
from app.DORApy import creation_carte
import os
import boto3
from tempfile import NamedTemporaryFile

bucket_files_common = os.getenv('S3_BUCKET_COMMON_FILES')
bucket_files_custom = os.getenv('S3_BUCKET_USERS_FILES')

s3_region = os.getenv('S3_UPLOADS_REGION')
s3_access_key = os.getenv('S3_UPLOADS_ACCESS_KEY')
s3_secret_key = os.getenv('S3_UPLOADS_SECRET_KEY')

geojson_data=creation_carte.creation_carto_syndicats("33")

#connect_path.upload_file_vers_s3("custom","doras3bdddorabucket",path)
#ajout_MO_ou_PPG.ajout_shp_MO_ou_PPG("PPG")

#couche_test = gpd.read_file("D:/projet_DORA/shp_files/ME/BV Me sup AG 2021.shp")
#couche_test.to_file("G:/travail/carto/projets basiques/PAOT global 5.0/test/test_ME.gpkg", driver='GPKG')
#gdf_ROE = gpd.read_file("D:/projet_DORA/shp_files/ROE/ROE_AG_2023.gpkg")
#gdf_SAGE = gpd.read_file("D:/projet_DORA/shp_files/SAGE/SAGE superficiels.shp")

#gdf_ME = gpd.read_file("D:/projet_DORA/shp_files/ME/BV Me sup AG 2021.shp")
#dict_gdf = Class_NDictGdf.chercher_gdf()
#user_folder = actualisation_dossier_MO()
