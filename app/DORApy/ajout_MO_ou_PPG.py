# -*- coding: utf-8 -*-
import pandas as pd
import sys
import geopandas as gpd
import json

pd.set_option("display.max_rows", None, "display.max_columns", None,'display.max_colwidth',None)
from app.DORApy.classes.Class_DictCustomMaitre import DictCustomMaitre
from app.DORApy.classes.Class_dictGdfCompletREF import dictGdfCompletREF,GdfCompletREF
from app.DORApy.classes.Class_DictDfInfoShp import DictDfInfoShp


def conv_shp_en_geojson(files,temp_dir):
    
    # Use geopandas to read the shapefile
    gdf = gpd.read_file(temp_dir)
    gdf = gdf.to_crs("EPSG:4326")
    
    # Convert the GeoDataFrame to GeoJSON
    geojson = gdf.to_json()
    geojson = json.loads(geojson)
    return geojson


def ajout_shp_MO_ou_PPG(REF):
    dict_custom_maitre = DictCustomMaitre({})
    dict_custom_maitre.set_config_type_projet(type_rendu='special_MAJ_MO_PPG')

    dict_geom_REF = dictGdfCompletREF({})
    dict_geom_REF = dictGdfCompletREF.ajout_echelle_dict_couche_complet_REF(dict_geom_REF,dict_custom_maitre=None,liste_echelle_a_aller_chercher=["DEP","MO","PPG"])

    dict_dict_info_REF = DictDfInfoShp({})
    dict_dict_info_REF = dict_dict_info_REF.creation_DictDfInfoShp()

    #Récupération fichiers individuelles

    couche_REF = GdfCompletREF.recherche_shp_MO_ou_PPG_a_ajouter(REF)

    couche_REF = dictGdfCompletREF.comparaison_si_entite_deja_existante(dict_geom_REF,couche_REF,REF)

    couche_REF = dictGdfCompletREF.ajout_CODE_REF_unique(couche_REF,REF,dict_dict_info_REF)
    if REF == "MO":
        couche_REF = dictGdfCompletREF.ajout_CODE_DEP(couche_REF,REF,dict_geom_REF)
    if REF == "PPG":
        couche_REF = dictGdfCompletREF.ajout_SP_GEMAPI(couche_REF,REF,dict_geom_REF)        

    dict_dict_info_REF = DictDfInfoShp.actualisation_dict_dict_info_REF(couche_REF,REF,dict_dict_info_REF)
    dict_dict_info_REF = DictDfInfoShp.actualisation_par_utilisateur(REF,dict_dict_info_REF)

    dict_geom_REF = dictGdfCompletREF.envoi_des_infos_dans_dict_geom_REF(dict_geom_REF,couche_REF,REF,dict_dict_info_REF)
    dict_geom_REF = dictGdfCompletREF.actualisation_dict_geom_REF(dict_geom_REF)
    print("coucou")


