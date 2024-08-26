
import pandas as pd
from app.DORApy.classes import Class_NDictGdf,Class_NGdfREF
from flask import Flask, send_from_directory, jsonify, request
from app.DORApy import creation_carte
from app.DORApy.decorators.token_admin import check_token_admin
from app.DORApy.classes import Class_Folder
import geopandas as gpd

###Fichiers config
import os
bucket_users_files = os.getenv('S3_BUCKET_USERS_FILES')
folder_prefix = 'MO_gemapi/'
#folders = Class_Folder.lister_rep_et_fichiers(bucket_users_files, folder_prefix)
folders = Class_Folder.lister_rep_et_fichiers(bucket_users_files, folder_prefix)
print("coucou")
#ajout_MO_ou_PPG.ajout_shp_MO_ou_PPG("PPG")

#couche_test = gpd.read_file("D:/projet_DORA/shp_files/ME/BV Me sup AG 2021.shp")
#couche_test.to_file("G:/travail/carto/projets basiques/PAOT global 5.0/test/test_ME.gpkg", driver='GPKG')
#gdf_ROE = gpd.read_file("D:/projet_DORA/shp_files/ROE/ROE_AG_2023.gpkg")
#gdf_SAGE = gpd.read_file("D:/projet_DORA/shp_files/SAGE/SAGE superficiels.shp")

#gdf_ME = gpd.read_file("D:/projet_DORA/shp_files/ME/BV Me sup AG 2021.shp")
#dict_gdf = Class_NDictGdf.chercher_gdf()
#user_folder = actualisation_dossier_MO()
