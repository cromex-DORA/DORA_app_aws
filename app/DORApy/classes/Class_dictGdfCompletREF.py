# -*- coding: utf-8 -*-
from pickle import NONE
import pandas as pd
import geopandas as gpd

from app.DORApy.classes.modules import PPG,MO_gemapi,ME,BVG,SAGE,dep,ROE
from app.DORApy.classes.Class_GdfCompletREF import GdfCompletREF
from app.DORApy.classes.Class_DictDfInfoShp import DictDfInfoShp
from shapely.geometry import MultiPolygon, Polygon, Point
import shapely.geometry as geom
import os.path
from os import path
import numpy as np
import copy
import itertools
import geopandas as gpd

from app.DORApy.classes.modules import connect_path
PATH_DOSSIER_MAITRE = os.getenv('PATH_DOSSIER_MAITRE')

##########################################################################################
#List de couche gdf de différentes échelles
##########################################################################################
class dictGdfCompletREF(dict):
    @property
    def _constructor(self):
        return dictGdfCompletREF

    ##########################################################################################
    #dict_gdf_REF : Partie fonctions
    ##########################################################################################
    def ajout_echelle_dict_couche_complet_REF(self,dict_custom_maitre=None,liste_echelle_a_aller_chercher=None):
        if dict_custom_maitre!=None:
            liste_type_gdf = []
            if hasattr(dict_custom_maitre,"liste_echelle_shp_custom_a_check"):
                liste_type_gdf.extend(dict_custom_maitre.liste_echelle_shp_custom_a_check)
            if hasattr(dict_custom_maitre,"liste_echelle_REF_projet"):
                liste_type_gdf.extend(dict_custom_maitre.liste_echelle_REF_projet)                
            liste_type_gdf = list(set(liste_type_gdf))
            
        if dict_custom_maitre==None:
            liste_type_gdf = ['MO','PPG','ME','SME','BVG','SAGE']
            
        if liste_echelle_a_aller_chercher!=None:
            liste_type_gdf = liste_echelle_a_aller_chercher
        for echelle_carto_REF in liste_type_gdf:
            if "gdf_"+echelle_carto_REF not in self:
                if echelle_carto_REF == 'MO':
                    gdf_MO = MO_gemapi.import_shp_MO_gemapi(self)
                    gdf_MO = GdfCompletREF(gdf_MO)
                    gdf_MO.attribution_GdfCompletREF('MO')
                    gdf_MO['surface_MO'] = gdf_MO.area
                    self['gdf_MO'] = gdf_MO
                if echelle_carto_REF == 'PPG':
                    gdf_PPG = PPG.import_shp_PPG(self)
                    gdf_PPG = GdfCompletREF(gdf_PPG)
                    gdf_PPG.attribution_GdfCompletREF('PPG')
                    gdf_PPG['surface_PPG'] = gdf_PPG.area
                    self['gdf_PPG'] = gdf_PPG
                if echelle_carto_REF == 'ME':
                    liste_gdf_ME = []
                    if dict_custom_maitre!=None:
                        for grand_bassin in dict_custom_maitre.liste_grand_bassin:
                            if grand_bassin == "AG":
                                liste_gdf_ME.append(ME.import_shp_ME_AG(self))
                            if grand_bassin == "LB":
                                liste_gdf_ME.append(ME.import_shp_ME_LB(self))
                    if dict_custom_maitre==None:
                        liste_gdf_ME.append(ME.import_shp_ME_AG(self))
                    gdf_ME = pd.concat(liste_gdf_ME)
                    gdf_ME = GdfCompletREF(gdf_ME)
                    gdf_ME.attribution_GdfCompletREF('ME')
                    gdf_ME['surface_ME'] = gdf_ME.area
                    self['gdf_ME'] = gdf_ME
                if echelle_carto_REF == 'SME':
                    gdf_SME = ME.import_shp_SOUS_ME(self)
                    gdf_SME = GdfCompletREF(gdf_SME)
                    gdf_SME.attribution_GdfCompletREF('SME')
                    gdf_SME['surface_SME'] = gdf_SME.area
                    self['gdf_SME'] = gdf_SME
                if echelle_carto_REF == 'BVG':
                    gdf_BVG = BVG.import_shp_BVG(self)
                    gdf_BVG = GdfCompletREF(gdf_BVG)
                    gdf_BVG.attribution_GdfCompletREF('BVG')
                    gdf_BVG['surface_BVG'] = gdf_BVG.area
                    self['gdf_BVG'] = gdf_BVG
                if echelle_carto_REF == 'SAGE':
                    gdf_SAGE = SAGE.import_shp_SAGE(self)
                    gdf_SAGE = GdfCompletREF(gdf_SAGE)
                    gdf_SAGE.attribution_GdfCompletREF('SAGE')
                    gdf_SAGE['surface_SAGE'] = gdf_SAGE.area
                    self['gdf_SAGE'] = gdf_SAGE
                if echelle_carto_REF == 'DEP':
                    gdf_dep = dep.import_shp_dep(self)
                    gdf_dep = GdfCompletREF(gdf_dep)
                    gdf_dep.attribution_GdfCompletREF('DEP')
                    gdf_dep['surface_DEP'] = gdf_dep.area
                    self['gdf_DEP'] = gdf_dep
                if echelle_carto_REF == 'ROE':
                    gdf_ROE = ROE.import_shp_ROE()
                    gdf_ROE = GdfCompletREF(gdf_ROE)
                    gdf_ROE.attribution_GdfCompletREF('ROE')
                    self['gdf_ROE'] = gdf_ROE
                     
        return self 

    def tri_selection_dict_geom_REF(self,dict_custom_maitre,dict_dict_info_REF):
        if dict_custom_maitre.type_rendu=='carte' and dict_custom_maitre.type_donnees=='action' and dict_custom_maitre.thematique=='MIA' and dict_custom_maitre.liste_echelle_shp_custom_a_check==['DEP']:
            self['gdf_MO'] = pd.merge(self['gdf_MO'],dict_dict_info_REF['df_info_MO'][['CODE_MO',"TYPE_MO"]],on="CODE_MO",how='left')
            self['gdf_MO'] = self['gdf_MO'].loc[self['gdf_MO']['TYPE_MO']=="Syndicat"]
            self['gdf_MO'] = self['gdf_MO'][[x for x in list(self['gdf_MO']) if x!="TYPE_MO"]]
            self['gdf_MO'] = GdfCompletREF(self['gdf_MO'])
            self['gdf_MO'].attribution_GdfCompletREF('MO')
            self['gdf_MO']['surface_MO'] = self['gdf_MO'].area
        return self

    def actualisation_dict_geom_REF(self):
        try:
            filename = ("shp_files\\syndicats GEMAPI\\MO_gemapi_NA.shp")
            filename = os.path.join(PATH_DOSSIER_MAITRE,filename)
            self['gdf_MO'].to_file(filename)
            print("Fichier MO_gemapi_NA.shp mis à jour")
        except:
            pass
        try:
            self['gdf_PPG'].to_file('G:/travail/carto/couches de bases/PPG/PPG_NA.shp')
            print("Fichier PPG_NA.shp mis à jour")
        except:
            pass        

        return self

    def decoup_point_REF_custom(self,projet_representation_action):
        gros_custom = projet_representation_action.gdf_shp_custom.geometry.unary_union
        for gdf_point_REF in self:
            self[gdf_point_REF] = self[gdf_point_REF][self[gdf_point_REF].geometry.within(gros_custom)]
        return self

    def ajout_REF_special_SOUS_ME(self,projet):
        if (projet.type_rendu=='carte' or projet.type_rendu=='tableau_vierge' or projet.type_rendu=='tableau_DORA_vers_BDD') and projet.type_donnees=='action' and projet.thematique=='MIA' and projet.public_cible=='MO':
            gdf_ME = ME.import_shp_ME_AG(self)
            gdf_SME = ME.import_shp_SOUS_ME(gdf_ME)
            self['gdf_ME'] = ME.remplacement_ME_par_SME(gdf_SME,gdf_ME)
            tempo_gdf_ME =  self['gdf_ME'][self['gdf_ME']['CODE_ME'].str.contains("%")]
            tempo_gdf_ME["CODE_SME"] = tempo_gdf_ME["CODE_ME"]
            tempo_gdf_ME["CODE_ME"] = [x.split("%")[0] for x in tempo_gdf_ME["CODE_ME"].to_list()]
            dict_conversion_CODE_NOM_SME = dict(zip(tempo_gdf_ME['CODE_SME'].to_list(),tempo_gdf_ME['NOM_ME'].to_list()))
            list_tempo_a_supprimer_apres_essai = tempo_gdf_ME["CODE_SME"].to_list()
            tempo_gdf_ME = tempo_gdf_ME.groupby("CODE_ME").agg({"CODE_SME":lambda x: list(x)})
            dict_conversion_CODE_CODE_SME = dict(zip(tempo_gdf_ME.index,tempo_gdf_ME['CODE_SME'].to_list()))
            #LIGNE A ENLEVER, JUSTE POUR LESSAI
            #self['gdf_ME'] = self['gdf_ME'][self['gdf_ME']["CODE_ME"].isin(list_tempo_a_supprimer_apres_essai)]
            self['gdf_ME'].dict_conversion_CODE_CODE_SME = dict_conversion_CODE_CODE_SME
            self['gdf_ME'].dict_conversion_CODE_NOM_SME = dict_conversion_CODE_NOM_SME
            self['gdf_ME'].echelle_REF_shp = "ME"
            self['gdf_ME'].nom_entite_REF = "NOM_ME"
            self['gdf_ME'].colonne_geometry = "geometry_ME"
        return self

    def definition_gauche_droite_haut_bas_decoupREF_par_rapport_au_custom(self,dict_df_buffer_custom,CODE_custom):
        gdf_tempo = self.df
        gdf_tempo['geometry_point1_ligne_horizon'] = gpd.points_from_xy(0,gdf_tempo["centre_decoupREF"].y)
        gdf_tempo['geometry_point2_ligne_horizon'] = gpd.points_from_xy(1200000,gdf_tempo["centre_decoupREF"].y)
        gdf_tempo['ligne_horizon'] = gdf_tempo.apply(lambda x:geom.LineString([x['geometry_point1_ligne_horizon'], x['geometry_point2_ligne_horizon']]), axis=1)
        gdf_tempo['multi_point_horizon'] = gdf_tempo.apply(lambda x:x['ligne_horizon'].intersection(dict_df_buffer_custom[CODE_custom]['geometry_custom_buffer']),axis=1)
        gdf_tempo = gdf_tempo[["CODE_REF",'centre_decoupREF','multi_point_horizon']]
        gdf_tempo = gdf_tempo.set_geometry('multi_point_horizon')
        gdf_tempo = gdf_tempo.explode(index_parts=False)
        gdf_tempo["coord_x"] = gdf_tempo['multi_point_horizon'].x
        gdf_tempo = gdf_tempo.sort_values(["CODE_REF",'coord_x'],ascending=True).groupby('CODE_REF').head(2)
        gdf_tempo = gdf_tempo.reset_index(drop=True)
        gdf_tempo["orient_GD"] = "D"
        gdf_tempo.loc[gdf_tempo.index % 2 == 0,"orient_GD"] = "G"
        gdf_tempo['distance'] = gdf_tempo.apply(lambda x:abs(x["centre_decoupREF"].x - x["multi_point_horizon"].x) ,axis=1)
        gdf_tempo_final = gdf_tempo.loc[gdf_tempo.groupby('CODE_REF')['distance'].idxmin()]
        dict_orient_GD = dict(zip(gdf_tempo_final['CODE_REF'].to_list(),gdf_tempo_final['orient_GD'].to_list()))

        gdf_tempo = self.df
        gdf_tempo['geometry_point1_ligne_verti'] = gpd.points_from_xy(gdf_tempo["centre_decoupREF"].x,6000000)
        gdf_tempo['geometry_point2_ligne_verti'] = gpd.points_from_xy(gdf_tempo["centre_decoupREF"].x,7200000)
        gdf_tempo['ligne_verti'] = gdf_tempo.apply(lambda x:geom.LineString([x['geometry_point1_ligne_verti'], x['geometry_point2_ligne_verti']]), axis=1)
        gdf_tempo['multi_point_verti'] = gdf_tempo.apply(lambda x:x['ligne_verti'].intersection(dict_df_buffer_custom[CODE_custom]['geometry_custom_buffer']),axis=1)
        gdf_tempo = gdf_tempo[["CODE_REF",'centre_decoupREF','multi_point_verti']]
        gdf_tempo = gdf_tempo.set_geometry('multi_point_verti')
        gdf_tempo = gdf_tempo.explode(index_parts=False)
        gdf_tempo["coord_y"] = gdf_tempo['multi_point_verti'].y
        gdf_tempo = gdf_tempo.sort_values(["CODE_REF",'coord_y'],ascending=True).groupby('CODE_REF').head(2)
        gdf_tempo = gdf_tempo.reset_index(drop=True)
        gdf_tempo["orient_BH"] = "H"
        gdf_tempo.loc[gdf_tempo.index % 2 == 0,"orient_BH"] = "B"
        gdf_tempo['distance'] = gdf_tempo.apply(lambda x:abs(x["centre_decoupREF"].y - x["multi_point_verti"].y) ,axis=1)
        gdf_tempo_final = gdf_tempo.loc[gdf_tempo.groupby('CODE_REF')['distance'].idxmin()]
        dict_orient_BH = dict(zip(gdf_tempo_final['CODE_REF'].to_list(),gdf_tempo_final['orient_BH'].to_list()))



        self.df['orient_GD'] = self.df['CODE_REF'].map(dict_orient_GD)
        self.df['orient_BH'] = self.df['CODE_REF'].map(dict_orient_BH)
        return self


    def creation_dict_decoupREF_special(self,dict_custom_maitre):
        if dict_custom_maitre.type_rendu == "special_MO_gestion_SAGE":
            liste_combinaison_REF = [['MO','SAGE']]
        dict_geomREF_decoupREF = dictGdfCompletREF.decoupage_entite_par_entite(self,liste_combinaison_REF)
        dict_geomREF_decoupREF = dictGdfCompletREF.regle_tri_dict_decoupREF(dict_geomREF_decoupREF)
        return dict_geomREF_decoupREF


    def copie_custom_a_reduire(self):
        dict_geom_REF_reduire = dictGdfCompletREF(self)
        return dict_geom_REF_reduire

    def isolation_gros_custom_a_reduire(self,dict_special_custom_a_reduire,projet):
        liste_custom_a_reduire = list({k:v for k,v in dict_special_custom_a_reduire.items() if v["custom_a_reduire"]==True})
        echelle_REF_shp = projet.gdf_shp_MO.echelle_REF_shp
        colonne_geometry_custom = projet.gdf_shp_MO.colonne_geometry
        self['gdf_custom'] = self['gdf_custom'].loc[self['gdf_custom']['CODE_custom'].isin(liste_custom_a_reduire)]
        self['gdf_custom'] = GdfCompletREF(self['gdf_custom'])
        self['gdf_custom'].attribution_GdfCompletREF('custom')
        for nom_gdf_REF in list(dict_special_custom_a_reduire.keys()):
            if nom_gdf_REF not in liste_custom_a_reduire:
                del dict_special_custom_a_reduire[nom_gdf_REF]
        return self

    def creation_dict_decoupREF_par_custom(self,dict_custom_maitre=None):
        liste_echelle_REF_projet = [x.split("_")[1] for x in list(self)]
        def hierarchisation_liste_echelle(liste_combinaison_REF):
            list_hierarchie_shp_hydro = ['custom','DEP','CT','EPTB','SAGE','MO','PPG','BVG','ME','SME']
            dict_hierarchie_hydro = {}
            for numero_hierarchie,echelle_shp in enumerate(list_hierarchie_shp_hydro):
                dict_hierarchie_hydro[echelle_shp] = numero_hierarchie
            dict_tempo_shp = {x:dict_hierarchie_hydro[x] for x in liste_combinaison_REF}
            dict_tempo_shp = dict(sorted(dict_tempo_shp.items(), key=lambda x: x[1], reverse=False))
            liste_combinaison_REF = list(dict_tempo_shp)
            return liste_combinaison_REF
        liste_combinaison_REF = hierarchisation_liste_echelle(liste_echelle_REF_projet)
        echelle_projet = liste_combinaison_REF[0]
        liste_combinaison_REF = list(itertools.combinations(liste_combinaison_REF, 2))
        liste_combinaison_REF = [list(x) for x in liste_combinaison_REF]
        liste_combinaison_REF_sans_echelle_projet = [x for x in liste_echelle_REF_projet if x!=echelle_projet]

        dict_geomREF_decoupREF = dictGdfCompletREF({})
        #Permet d'optimiser le CODE, mais non indispensable
        for REF in ['ME']:
            combinaison_REF = [echelle_projet,REF]
            self['gdf_' + REF] = gpd.overlay(self['gdf_' + REF], self['gdf_' + echelle_projet][['CODE_'+echelle_projet,self['gdf_' + echelle_projet].nom_entite_REF,self['gdf_' + echelle_projet].colonne_geometry,'surface_'+echelle_projet]], how='intersection')
            #Traitement des P.... de multipolygons
            self['gdf_' + REF] = self['gdf_' + REF].explode(ignore_index=True)
            self['gdf_' + REF]['surface_'+REF] = self['gdf_' + REF].area
            self['gdf_' + REF] = self['gdf_' + REF].loc[self['gdf_' + REF]['surface_'+REF]>1000000]
            self['gdf_' + REF]['compte'] = self['gdf_' + REF].groupby('CODE_'+REF).cumcount()+1
            self['gdf_' + REF]['compte'] = self['gdf_' + REF]['compte'].astype(str)
            self['gdf_' + REF]['CODE_'+REF] = self['gdf_' + REF]['CODE_'+REF] + '$' + self['gdf_' + REF]['compte']
            self['gdf_' + REF]['geometry_'+ REF] = self['gdf_' + REF]['geometry']
            self['gdf_' + REF] = self['gdf_' + REF].drop(['geometry'],axis=1)
            self['gdf_' + REF] = self['gdf_' + REF].set_geometry('geometry_'+REF)
            self['gdf_' + REF] = GdfCompletREF(self['gdf_' + REF])
            self['gdf_' + REF].attribution_GdfCompletREF(REF)

        liste_CODE_custom = self['gdf_'+echelle_projet]['CODE_'+echelle_projet].to_list()
        for CODE_custom in liste_CODE_custom:
            dict_geomREF_decoupREF[CODE_custom] = {}

        for CODE_custom in liste_CODE_custom:
            for [REF1,REF2] in liste_combinaison_REF:
                dict_mapping_CODE_REF1_surface_REF1 = dict(zip(self['gdf_' + REF1]['CODE_'+REF1].to_list(),self['gdf_' + REF1].area.to_list()))
                gdf_decoup_REF1_REF2 = gpd.overlay(self['gdf_' + REF1].loc[self['gdf_' + REF1]['CODE_'+echelle_projet]==CODE_custom][['CODE_'+REF1,self['gdf_' + REF1].nom_entite_REF,self['gdf_' + REF1].colonne_geometry]], self['gdf_' + REF2].loc[self['gdf_' + REF2]['CODE_'+echelle_projet]==CODE_custom][['CODE_'+REF2,self['gdf_' + REF2].nom_entite_REF,self['gdf_' + REF2].colonne_geometry,'surface_'+REF2]], how='intersection')
                dict_geomREF_decoupREF[CODE_custom]['gdf_decoup' + REF2 +'_' + REF1]=gdf_decoup_REF1_REF2
                dict_geomREF_decoupREF[CODE_custom]['gdf_decoup' + REF2 +'_' + REF1] = GdfCompletREF(dict_geomREF_decoupREF[CODE_custom]['gdf_decoup' + REF2 +'_' + REF1])
                dict_geomREF_decoupREF[CODE_custom]['gdf_decoup' + REF2 +'_' + REF1].attribution_GdfCompletREF(REF2)
                dict_geomREF_decoupREF[CODE_custom]['gdf_decoup' + REF2 +'_' + REF1]['surface_' + REF1] = self['gdf_' + REF1]['CODE_'+REF1].map(dict_mapping_CODE_REF1_surface_REF1)
                dict_geomREF_decoupREF[CODE_custom]['gdf_decoup' + REF2 +'_' + REF1]['surface_decoup' + REF2] = dict_geomREF_decoupREF[CODE_custom]['gdf_decoup' + REF2 +'_' + REF1]['geometry'].area
                dict_geomREF_decoupREF[CODE_custom]['gdf_decoup' + REF2 +'_' + REF1]['ratio_surf'] = dict_geomREF_decoupREF[CODE_custom]['gdf_decoup' + REF2 +'_' + REF1]['surface_decoup' + REF2]/dict_geomREF_decoupREF[CODE_custom]['gdf_decoup' + REF2 +'_' + REF1]['surface_' + REF2]
                dict_geomREF_decoupREF[CODE_custom]['gdf_decoup' + REF2 +'_' + REF1] = dict_geomREF_decoupREF[CODE_custom]['gdf_decoup' + REF2 +'_' + REF1].loc[dict_geomREF_decoupREF[CODE_custom]['gdf_decoup' + REF2 +'_' + REF1]['ratio_surf']>0.05]
        #dict_geomREF_decoupREF.regle_tri_dict_decoupREF_par_custom(projet={})
        return dict_geomREF_decoupREF

    def ajout_liste_CODE_REF_voisin(self,):
        for CODE_custom in self:
            self[CODE_custom]['gdf_decoupME_custom']['CODE_ME_voisin'] = None
            for index, gdf_decoupME in self[CODE_custom]['gdf_decoupME_custom'].iterrows():   
                # get 'not disjoint' countries
                liste_CODE_ME_voisin = self[CODE_custom]['gdf_decoupME_custom'][~self[CODE_custom]['gdf_decoupME_custom'].geometry.disjoint(gdf_decoupME.geometry)].CODE_ME.tolist()
                # remove own name of the country from the list
                liste_CODE_ME_voisin = [CODE_ME for CODE_ME in liste_CODE_ME_voisin if gdf_decoupME.CODE_ME != CODE_ME]
                # add names of neighbors as NEIGHBORS value
                self[CODE_custom]['gdf_decoupME_custom'].at[index, "liste_CODE_ME_voisin"] = ", ".join(liste_CODE_ME_voisin)

        for CODE_custom in self:
            self[CODE_custom]['gdf_decoupME_custom']['liste_CODE_ME_voisin'] = [x.split(", ") for x in self[CODE_custom]['gdf_decoupME_custom']['liste_CODE_ME_voisin'].to_list()]
        return self

    def comparaison_si_entite_deja_existante(dict_geom_REF,couche_REF,REF):
        dict_geom_REF['gdf_REF_a_comparer'] = couche_REF
        liste_combinaison_REF = [[REF,"REF_a_comparer"]]
        dict_geom_REF = dictGdfCompletREF.decoupage_entite_par_entite(dict_geom_REF,liste_combinaison_REF)
        if len(dict_geom_REF)>0:
            gdf_comparaison = dict_geom_REF['gdf_decoupREF_a_comparer_'+REF]
            gdf_comparaison = gdf_comparaison.loc[gdf_comparaison['ratio_surf']>0.9]
            if len(gdf_comparaison)>0:
                dict_pb_potentiel = dict(zip(gdf_comparaison["NOM_"+REF].to_list(),gdf_comparaison["NOM_REF_a_comparer"].to_list()))
                for nom_REF,NOM_REF_a_comparer in dict_pb_potentiel.items():
                    print("Attention ! Potentiel " + REF + " déjà existant dans la BBD : " + nom_REF + " et " + NOM_REF_a_comparer)
                    print("Je supprime de la couche à ajouter l'entité " + NOM_REF_a_comparer)
                couche_REF = couche_REF.loc[~couche_REF['NOM_REF_a_comparer'].isin(dict_pb_potentiel.values())]
        if len(dict_geom_REF)==0:
            print("Aucune correspondance avec la BDD de syndicat")
        return couche_REF

    def ajout_CODE_REF_unique(couche_REF,REF,dict_dict_info_REF):
        def Generation_CODE_perso_PPG(couche_REF,df_info_PPG):
            NOM_REF_a_attribuer = couche_REF['NOM_init'].to_list()
            dict_NOM_PPG_CODE_PPG_df_info_PPG = dict(zip(df_info_PPG['NOM_PPG'].to_list(),[int(x.split("_")[1]) for x in df_info_PPG['CODE_PPG'].to_list()]))
            dict_tempo_NOM_CODE = {}
            for NOM_PPG in NOM_REF_a_attribuer:
                for i in range(200,99999):
                    if i not in list(dict_NOM_PPG_CODE_PPG_df_info_PPG.values()):
                        dict_tempo_NOM_CODE[NOM_PPG] = "PPG_" + str(i)
                        dict_NOM_PPG_CODE_PPG_df_info_PPG[NOM_PPG] = i
                        break
            couche_REF['CODE_PPG'] = couche_REF.apply(lambda x: dict_tempo_NOM_CODE[x['NOM_init']] if x['NOM_init'] in dict_tempo_NOM_CODE else x['CODE_PPG'],axis=1)
            return couche_REF        


        def Generation_CODE_perso_MO(couche_REF,df_info_MO):
            NOM_REF_a_attribuer = couche_REF['NOM_init'].to_list()
            dict_NOM_MO_CODE_MO_df_info_MO = dict(zip(df_info_MO['NOM_init'].to_list(),[int(x.split("_")[2]) for x in df_info_MO['CODE_MO'].to_list()]))
            dict_tempo_NOM_CODE = {}
            for NOM_MO in NOM_REF_a_attribuer:
                for i in range(10000,99999):
                    if i not in list(dict_NOM_MO_CODE_MO_df_info_MO.values()):
                        dict_tempo_NOM_CODE[NOM_MO] = "MO_gemapi_" + str(i)
                        dict_NOM_MO_CODE_MO_df_info_MO[NOM_MO] = i
                        break
            couche_REF['CODE_MO'] = couche_REF.apply(lambda x: dict_tempo_NOM_CODE[x['NOM_init']] if x['NOM_init'] in dict_tempo_NOM_CODE else x['CODE_MO'],axis=1)
            return couche_REF

        couche_REF = couche_REF[["NOM_REF_a_comparer",'geometry_REF_a_comparer']]
        couche_REF = couche_REF.rename({"NOM_REF_a_comparer":"NOM_init","geometry_REF_a_comparer":"geometry_"+REF},axis=1)
        couche_REF = couche_REF.set_geometry("geometry_"+REF)
        if REF == 'MO':
            couche_REF = Generation_CODE_perso_MO(couche_REF,dict_dict_info_REF['df_info_'+REF])
        if REF == 'PPG':  
            couche_REF = Generation_CODE_perso_PPG(couche_REF,dict_dict_info_REF['df_info_'+REF])  
        return couche_REF

    def ajout_CODE_DEP(couche_REF,REF,dict_geom_REF):
        decoup_par_DEP = gpd.overlay(couche_REF, dict_geom_REF['gdf_DEP'], how='intersection',keep_geom_type=False)
        decoup_par_DEP['nouvelle_surface'] = decoup_par_DEP.area
        decoup_par_DEP = decoup_par_DEP.loc[decoup_par_DEP.groupby("CODE_MO")['nouvelle_surface'].transform(max) == decoup_par_DEP['nouvelle_surface']]
        dict_CODE_MO_CODE_DEP = dict(zip(decoup_par_DEP['CODE_MO'].to_list(),decoup_par_DEP['CODE_DEP'].to_list()))
        couche_REF['CODE_DEP'] = couche_REF['CODE_MO'].map(dict_CODE_MO_CODE_DEP)
        return couche_REF
    
    def ajout_SP_GEMAPI(couche_REF,REF,dict_geom_REF):
        decoup_par_MO = gpd.overlay(couche_REF, dict_geom_REF['gdf_MO'], how='intersection',keep_geom_type=False)
        decoup_par_MO['nouvelle_surface'] = decoup_par_MO.area
        decoup_par_MO = decoup_par_MO.loc[decoup_par_MO.groupby("CODE_MO")['nouvelle_surface'].transform(max) == decoup_par_MO['nouvelle_surface']]
        dict_CODE_PPG_CODE_MO = dict(zip(decoup_par_MO['CODE_PPG'].to_list(),decoup_par_MO['CODE_MO'].to_list()))
        dict_CODE_PPG_NOM_MO = dict(zip(decoup_par_MO['CODE_PPG'].to_list(),decoup_par_MO['NOM_MO'].to_list()))
        couche_REF['CODE_MO'] = couche_REF['CODE_PPG'].map(dict_CODE_PPG_CODE_MO)
        couche_REF['NOM_MO'] = couche_REF['CODE_PPG'].map(dict_CODE_PPG_NOM_MO)
        return couche_REF        

    def envoi_des_infos_dans_dict_geom_REF(dict_geom_REF,couche_REF,REF,dict_dict_info_REF):
        if REF == 'MO':
            liste_CODE_MO_a_ajouter = couche_REF['CODE_MO'].to_list()
            dict_dict_info_REF['df_info_MO'].loc[dict_dict_info_REF['df_info_MO']['CODE_MO'].isin(liste_CODE_MO_a_ajouter),"shp"] = 1
            couche_REF['surface_MO'] = couche_REF.area
            list_col_gdf_MO = [x for x in list(dict_geom_REF['gdf_MO']) if x not in ['geometry_MO','surface_MO']]
            couche_REF = pd.merge(couche_REF[['CODE_MO',"geometry_MO",'surface_MO']],dict_dict_info_REF['df_info_MO'][list_col_gdf_MO],on="CODE_MO")
            dict_geom_REF['gdf_MO'] = pd.concat([dict_geom_REF['gdf_MO'],couche_REF])
        return dict_geom_REF


    
    def suppression_entite_hors_des_custom(self,projet=None):
        for echelle_shp_par_decoupage,shp_decoupREF in self.items():
            if projet!=None:
                if projet.type_donnees=='action':
                    REF_entite = echelle_shp_par_decoupage[10:].split("_")[0]
                    REF_index = echelle_shp_par_decoupage[10:].split("_")[1]
                    if REF_index!='custom':
                        if 'gdf_decoup' + REF_entite + '_custom' in self:
                            self[echelle_shp_par_decoupage] = self[echelle_shp_par_decoupage].loc[self[echelle_shp_par_decoupage]['CODE_'+REF_entite].isin(self['gdf_decoup' + REF_entite + '_custom']['CODE_'+REF_entite].to_list())]
                            self[echelle_shp_par_decoupage] = self[echelle_shp_par_decoupage].loc[self[echelle_shp_par_decoupage]['CODE_'+REF_index].isin(self['gdf_decoup' + REF_index + '_custom']['CODE_'+REF_index].to_list())]
        return self                


    def ajout_dit_liste_ME_par_SME(self,dict_dict_info_REF):
        df_info_SME = dict_dict_info_REF['df_info_SME']
        dict_liste_ME_par_SME = dict(zip(df_info_SME['CODE_SME'].to_list(),df_info_SME['ME_maitre'].to_list()))
        dict_liste_ME_par_SME = {k:v for k,v in dict_liste_ME_par_SME.items()}
        self["dict_liste_ME_par_SME"] = dict_liste_ME_par_SME
        return self
    
    def ajout_inversion_dict_relation_1_pour_1(self,nom_dict_a_inverser):
        REF1 = nom_dict_a_inverser[11:].split("_")[0]
        REF2 = nom_dict_a_inverser[11:].split("_")[2]        
        nouveau_dict = {}
        for k,v in self[nom_dict_a_inverser].items():
            for x in v:
                nouveau_dict.setdefault(x, []).append(k)
        nouveau_dict = {k:v[0] for k,v in nouveau_dict.items()}        
        self['dict_' + REF2 +'_par_' + REF1] = nouveau_dict
        return self

    def extraction_dict_relation_shp_liste_a_partir_decoupREF_par_custom(self):
        class DictListeREFparREF(dict):
            @property
            def _constructor(self):
                return DictListeREFparREF
        dict_relation_shp_liste = DictListeREFparREF({})
        for CODE_custom,dict_decoupREF in self.items():
            dict_relation_shp_liste[CODE_custom] = {}
            for echelle_shp_par_decoupage,shp_decoupREF in dict_decoupREF.items():
                REF1 = echelle_shp_par_decoupage[10:].split("_")[0]
                REF2 = echelle_shp_par_decoupage[10:].split("_")[1]
                df_decoupREF_REF = shp_decoupREF.groupby('CODE_'+REF2).agg({'CODE_'+REF1:lambda x: list(x)})
                df_decoupREF_REF.columns = ['liste_' + REF1 +'_par_' + REF2]
                dict_relation_shp_liste[CODE_custom]['dict_liste_' + REF1 +'_par_' + REF2] = df_decoupREF_REF['liste_' + REF1 +'_par_' + REF2].to_list()[0]

        return dict_relation_shp_liste

    def extraction_dict_relation_shp_liste_a_partir_decoupREF_par_custom(self):
        class DictListeREFparREF(dict):
            @property
            def _constructor(self):
                return DictListeREFparREF
        dict_relation_shp_liste = DictListeREFparREF({})
        for CODE_custom,dict_decoupREF in self.items():
            dict_relation_shp_liste[CODE_custom] = {}
            for echelle_shp_par_decoupage,shp_decoupREF in dict_decoupREF.items():
                REF1 = echelle_shp_par_decoupage[10:].split("_")[0]
                REF2 = echelle_shp_par_decoupage[10:].split("_")[1]
                df_decoupREF_REF = shp_decoupREF.groupby('CODE_'+REF2).agg({'CODE_'+REF1:lambda x: list(x)})
                df_decoupREF_REF.columns = ['liste_' + REF1 +'_par_' + REF2]
                dict_relation_shp_liste[CODE_custom]['dict_liste_' + REF1 +'_par_' + REF2] = df_decoupREF_REF['liste_' + REF1 +'_par_' + REF2].to_list()[0]

        return dict_relation_shp_liste


    def extraction_dict_nb_REF_a_partir_decoupREF(self):
        dict_nb_REF = {}
        for echelle_shp_par_decoupage,shp_decoupREF in self.items():
            REF1 = echelle_shp_par_decoupage[10:].split("_")[0]
            REF2 = echelle_shp_par_decoupage[10:].split("_")[1]
            df_decoupREF_REF = shp_decoupREF.groupby('CODE_'+REF2).agg({'CODE_'+REF1:lambda x: list(x)})
            df_decoupREF_REF.columns = ['liste_' + REF1 +'_par_' + REF2]
            dict_nb_REF['dict_nb_' + REF1 +'_par_' + REF2] = df_decoupREF_REF.to_dict()['liste_' + REF1 +'_par_' + REF2]
            for nom_dict_liste_REF1_par_REF2,liste_REF1_par_REF2 in dict_nb_REF['dict_nb_' + REF1 +'_par_' + REF2].items():
                dict_nb_REF['dict_nb_' + REF1 +'_par_' + REF2][nom_dict_liste_REF1_par_REF2] = len(liste_REF1_par_REF2)
        return dict_nb_REF
    
    def actualisation_dict_relation_shp_liste(dict_custom_maitre,dict_relation_shp_liste,dict_df_donnees):
        #Gérer les CODE_REF à rajouter dans les dict relations en fonction du type de projet
        if 'BDD_DORA' in dict_df_donnees:
            df_BDD_DORA = dict_df_donnees['BDD_DORA'].df
            
        if dict_custom_maitre.type_rendu=='carte' and dict_custom_maitre.type_donnees == 'action':
            if dict_custom_maitre.echelle_REF == 'MO' and (dict_custom_maitre.echelle_base_REF == 'ME' or dict_custom_maitre.echelle_base_REF == 'SME'):
                for nom_custom,entite_custom in dict_custom_maitre.items():
                    CODE_custom =  entite_custom.CODE_custom
                    echelle_REF_custom = entite_custom.echelle_REF
                    echelle_base_REF = entite_custom.echelle_base_REF
                    df_actions_custom = df_BDD_DORA.loc[df_BDD_DORA["CODE_"+echelle_REF_custom]==CODE_custom]
                    liste_CODE_echelle_base_REF = df_actions_custom.loc[~(df_actions_custom["CODE_" + echelle_REF_custom].isnull())]["CODE_" + echelle_base_REF].to_list()
                    liste_CODE_echelle_base_REF = list(set(liste_CODE_echelle_base_REF))
                    dict_relation_shp_liste['dict_liste_' + echelle_base_REF + '_par_custom'][CODE_custom] = dict_relation_shp_liste['dict_liste_' + echelle_base_REF + '_par_custom'][CODE_custom] + liste_CODE_echelle_base_REF
                    dict_relation_shp_liste['dict_liste_' + echelle_base_REF + '_par_custom'][CODE_custom] = list(set(dict_relation_shp_liste['dict_liste_' + echelle_base_REF + '_par_custom'][CODE_custom]))
                    dict_relation_shp_liste['dict_liste_' + echelle_base_REF + '_par_custom'][CODE_custom] = [x for x in dict_relation_shp_liste['dict_liste_' + echelle_base_REF + '_par_custom'][CODE_custom] if x!='nan']
        return dict_relation_shp_liste    
    
    def mise_a_jour_fichier_info_relation_shp(self,dict_relation_shp_liste):
        dict_df_info_shp = DictDfInfoShp({})
        dict_df_info_shp.creation_DictDfInfoShp()

        dict_relation_shp_liste_NOM = copy.deepcopy(dict_relation_shp_liste)
        #Conversion en NOM et pas en CODE
        for type_relation,dict_liste in dict_relation_shp_liste_NOM.items():
            REF_index = type_relation.split('_')[4]
            REF_entite = type_relation.split('_')[2]
            dict_mapping_CODE_entite_NOM_entite = dict(zip(dict_df_info_shp['df_info_' + REF_entite]['CODE_'+REF_entite].to_list(),dict_df_info_shp['df_info_' + REF_entite]['NOM_'+REF_entite].to_list()))
            for CODE_index,liste_CODE_entite in dict_liste.items():
                dict_liste[CODE_index] = [dict_mapping_CODE_entite_NOM_entite[x] for x in liste_CODE_entite]

        for type_entite,df_info_shp in dict_df_info_shp.items():
            REF_index = type_entite.split('_')[2]
            for type_relation_entite,dict_liste_entite_par_REF_index in dict_relation_shp_liste.items():
                if type_relation_entite.split('_')[4]==REF_index:
                    REF_entite = type_relation_entite.split('_')[2]
                    df_info_shp['liste_CODE_' + REF_entite] = df_info_shp['CODE_' + REF_index].map(dict_liste_entite_par_REF_index)

        for type_entite,df_info_shp in dict_df_info_shp.items():
            REF_index = type_entite.split('_')[2]
            for type_relation_entite,dict_liste_entite_par_REF_index in dict_relation_shp_liste_NOM.items():
                if type_relation_entite.split('_')[4]==REF_index:
                    REF_entite = type_relation_entite.split('_')[2]
                    df_info_shp['liste_NOM_' + REF_entite] = df_info_shp['CODE_' + REF_index].map(dict_liste_entite_par_REF_index)

        dict_df_info_shp.maj_fichier_DictDfInfoShp()
        return self

    def mise_a_jour_fichier_info_nb_entite(self,dict_nb_REF):
        dict_df_info_shp = DictDfInfoShp({})
        dict_df_info_shp.creation_DictDfInfoShp()
        for type_entite,df_info_shp in dict_df_info_shp.items():
            REF_index = type_entite.split('_')[2]
            for type_relation_entite,dict_nb_entite_par_REF_index in dict_nb_REF.items():
                if type_relation_entite.split('_')[4]==REF_index:
                    REF_entite = type_relation_entite.split('_')[2]
                    df_info_shp['nb_' + REF_entite] = df_info_shp['CODE_' + REF_index].map(dict_nb_entite_par_REF_index)
        dict_df_info_shp.maj_fichier_DictDfInfoShp()
        return self

    def garder_dep_entite(self,initial_entite):
        if initial_entite=="NAQ":
            list_CODE_REF = ["16","17","19","23","24","33","40","47","64","79","86","87"]
        if "gdf_DEP" in self:
            self['gdf_DEP'] = self['gdf_DEP'].loc[self['gdf_DEP']["CODE_DEP"].isin(list_CODE_REF)]
        return self








