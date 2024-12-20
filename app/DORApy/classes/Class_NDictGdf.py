import os
import geopandas as gpd
from app.DORApy.classes.Class_NGdfREF import NGdfREF
from app.DORApy.classes.Class_DgfDecoupREF import creation_decoupREF
from app.DORApy.classes.modules import connect_path
from shapely.geometry import MultiPolygon
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import sys
import itertools
_default = object()

environment = os.getenv('ENVIRONMENT')
chemin_fichiers_shp = os.getenv('chemin_fichiers_shp')


class NDictGdf(dict):
    def __init__(self,dict_custom_maitre=None,liste_echelle_REF=None):
        self.name = "dict_gdf_perso"


    def __repr__(self):
        return f"nom_gdf : {self.name}"
    
    def chercher_gdf(echelle_REF):
        if echelle_REF=="SAGE":
            chemin_fichiers_shp = "shp_files\\SAGE\\SAGE superficiels.shp"
            type_geom = "polygon"
        if echelle_REF=="BVG":
            chemin_fichiers_shp = "shp_files\\BVG\\data\\bv_gestion_sdage2022\\bv_gestion_sdage2022.shp"
            type_geom = "polygon"        
        if echelle_REF=="PPG":
            chemin_fichiers_shp = "shp_files\\ppg\\PPG_NA.shp"
            type_geom = "polygon"
        if echelle_REF=="DEP":
            chemin_fichiers_shp = "shp_files\\dep\\departement NAQ + AG.shp"
            type_geom = "polygon"
        if echelle_REF=="ME":
            chemin_fichiers_shp = "shp_files\\ME\\BV ME sup AG 2021.shp"
            type_geom = "polygon"
        if echelle_REF=="SME":
            chemin_fichiers_shp = "shp_files\\SOUS_ME\\SME_DORA_MO.shp"
            type_geom = "polygon"            
        if echelle_REF=="MO":
            chemin_fichiers_shp = "shp_files\\syndicats GEMAPI\\MO_gemapi_NA.shp"
            type_geom = "polygon"
        if echelle_REF=="ROE":
            chemin_fichiers_shp = "shp_files\\ROE\\ROE_AG_2023.gpkg"
            type_geom = "point"
        if echelle_REF=="ME_CE":
            chemin_fichiers_shp = "shp_files\\ME\\ME CE AG complet.shp"
            type_geom = "lignes"          
        chemin_fichiers_shp = connect_path.get_file_path_racine(chemin_fichiers_shp)
        gdf_REF = NGdfREF(echelle_REF,chemin_fichiers_shp,type_geom)
        gdf_REF.gdf = gdf_REF.gdf.set_geometry("geometry_"+echelle_REF)
        return gdf_REF


    def creer_image_MO_et_PPG(self,CODE_MO):
        self['gdf_MO'] = NGdfREF.suppression_EPTB_dans_gdf_MO(self['gdf_MO'])
        
        liste_PPG_MO = self['gdf_PPG'].df_info.loc[self['gdf_PPG'].df_info['CODE_MO_gemapi']==CODE_MO]['CODE_PPG'].to_list()
        print(CODE_MO,sys.stderr)
        
        gdf = self['gdf_MO'].gdf
        gdf_CE = self['gdf_ME_CE'].gdf
        gdf_zoom = gdf[gdf['CODE_MO'] == CODE_MO]
        print(len(gdf_zoom),sys.stderr)

        # Obtenir les limites de la bounding box de l'élément
        
        minx, miny, maxx, maxy = gdf_zoom.total_bounds

        # Définir une marge autour de l'élément pour le zoom
        margin = 0.1  # 10% de marge
        x_margin = (maxx - minx) * margin
        y_margin = (maxy - miny) * margin

        # Tracer la carte avec zoom
        fig, ax = plt.subplots(figsize=(10, 10))
        gdf.plot(ax=ax, color='none', edgecolor='black', legend=True)
        gdf_CE.plot(ax=ax, color='blue', edgecolor='black')
        gdf_zoom.plot(ax=ax, color='none', edgecolor='red',linewidth=2)
        if len(liste_PPG_MO)>0:
            gdf_PPG_zoom = self['gdf_PPG'].gdf.loc[self['gdf_PPG'].gdf['CODE_PPG'].isin(liste_PPG_MO)]
            gdf_PPG_zoom = gdf_PPG_zoom.buffer(-200)
            gdf_PPG_zoom.plot(ax=ax, color='none', edgecolor='green',linewidth=2)

        legend_elements = [Patch(facecolor='none', edgecolor='red', lw=2, label='MO'),
                        Patch(facecolor='none', edgecolor='green', lw=2, label='PPG')]
        ax.legend(handles=legend_elements)

        # Définir les limites des axes pour le zoom
        ax.set_xlim(minx - x_margin, maxx + x_margin)
        ax.set_ylim(miny - y_margin, maxy + y_margin)

        # Ajouter des éléments supplémentaires (titre, axes, etc.)
        ax.set_title(f'Carte du MO')
        ax.set_xlabel('Longitude')
        ax.set_ylabel('Latitude')

        # Sauvegarder l'image
        output_path = 'map_image.png'
        plt.savefig(output_path, dpi=300)
        plt.show()
        return plt
        
        
    
def remplissage_dictgdf(self,dict_custom_maitre=None,dict_dict_info_REF=None,liste_echelle_REF=_default):
    if liste_echelle_REF is _default:
        liste_echelle_REF = ['MO','PPG','ME','SME','BVG','SAGE']
    if liste_echelle_REF is not _default:     
        liste_gdf_deja_presents = [v.echelle_REF_shp for k,v in self.items()]
    
    if dict_custom_maitre!=None:
        liste_echelle_REF = []
        if hasattr(dict_custom_maitre,"liste_echelle_shp_custom_a_check"):
            liste_echelle_REF.extend(dict_custom_maitre.liste_echelle_shp_custom_a_check)
        if hasattr(dict_custom_maitre,"liste_echelle_REF_projet"):
            liste_echelle_REF.extend(dict_custom_maitre.liste_echelle_REF_projet)                
        liste_echelle_REF = list(set(liste_echelle_REF))

    for REF in liste_echelle_REF:
        if REF not in liste_gdf_deja_presents:
            self['gdf_'+REF] = NDictGdf.chercher_gdf(REF)
            if dict_dict_info_REF!=None:
                if 'df_info_'+REF in dict_dict_info_REF:
                    self['gdf_'+REF].df_info = dict_dict_info_REF['df_info_'+REF]
    return self


def creation_dict_decoupREF(self,dict_custom_maitre=None):
    def ajout_custom_liste_echelle_REF(self,dict_custom_maitre):
        liste_echelle_REF_projet = dict_custom_maitre.liste_echelle_REF_projet + ['custom']
        return liste_echelle_REF_projet
    
    def ajout_custom_dict_geom_REF(self,dict_custom_maitre):
        self['gdf_custom'] = dict_custom_maitre.gdf_custom
        return self

    def hierarchisation_liste_echelle(liste_combinaison_REF):
        list_hierarchie_shp_hydro = ['custom','DEP','CT','EPTB','SAGE','MO','PPG','BVG','ME','SME','ROE']
        dict_hierarchie_hydro = {}
        for numero_hierarchie,echelle_shp in enumerate(list_hierarchie_shp_hydro):
            dict_hierarchie_hydro[echelle_shp] = numero_hierarchie
        dict_tempo_shp = {x:dict_hierarchie_hydro[x] for x in liste_combinaison_REF}
        dict_tempo_shp = dict(sorted(dict_tempo_shp.items(), key=lambda x: x[1], reverse=False))
        liste_combinaison_REF = list(dict_tempo_shp)
        return liste_combinaison_REF    

    def decoupage_entite_par_entite(self,liste_combinaison_REF,dict_custom_maitre=None):
        dict_geomREF_decoupREF = {}
        for [REF1,REF2] in liste_combinaison_REF:
            gdf_REF1 = self['gdf_' + REF1]
            gdf_REF2 = self['gdf_' + REF2]
            dict_geomREF_decoupREF['gdf_decoup' + REF2 +'_' + REF1] = creation_decoupREF(gdf_REF1,gdf_REF2,REF1,REF2,dict_custom_maitre)
            '''
            if len(dict_geomREF_decoupREF['gdf_decoup' + REF2 +'_' + REF1])>0:
                dict_tempo_pour_copie['gdf_decoup' + REF2 +'_' + REF1] = copy.deepcopy(dict_geomREF_decoupREF['gdf_decoup' + REF2 +'_' + REF1])
                dict_tempo_pour_copie['gdf_decoup' + REF2 +'_' + REF1] = dict_tempo_pour_copie['gdf_decoup' + REF2 +'_' + REF1].set_geometry("geometry")
                dict_tempo_pour_copie['gdf_decoup' + REF2 +'_' + REF1].to_file("D:/projet_DORA/shp_files/decoup_files/decoup" + REF2 + REF1 + ".gpkg", driver='GPKG')'''
        return dict_geomREF_decoupREF

    def regle_tri_dict_decoupREF(self,projet=None):
        def extraire_plus_gros_polygon(multipolygon):
            areas = [i.area for i in multipolygon.geoms]
            max_area = areas.index(max(areas))    
            return multipolygon.geoms[max_area]

        for echelle_shp_par_decoupage,shp_decoupREF in self.items():
            #Regles generales
            if shp_decoupREF.type_de_geom=="polygon":
                REF_entite = echelle_shp_par_decoupage[10:].split("_")[0]
                REF_index = echelle_shp_par_decoupage[10:].split("_")[1]
                #Pour tous projets, Chaque ME ne doit appartenir qu'à un seul BVG
                if REF_entite=='ME' and REF_index=='BVG':
                    shp_decoupREF.gdf = shp_decoupREF.gdf.loc[(shp_decoupREF.gdf['ratio_surf']>0.3)]
                #Pour tous projets, on considère que presque chaque PPG ne doit appartenir qu'à une seule MO
                if REF_entite=='PPG' and REF_index=='MO':
                    shp_decoupREF.gdf = shp_decoupREF.gdf.loc[(shp_decoupREF.gdf['ratio_surf']>0.8)]                   
                if REF_entite=='SME' and REF_index!='MO':
                    if len(shp_decoupREF.gdf)>0:
                    #Highlander ! Il ne doit rester qu'un seul SME par entité
                        shp_decoupREF.gdf.loc[shp_decoupREF.gdf.geom_type=='MultiPolygon','geometry'] = shp_decoupREF.gdf.loc[shp_decoupREF.gdf.geom_type=='MultiPolygon']['geometry'].map(lambda x : extraire_plus_gros_polygon(x))   
                        shp_decoupREF.gdf['CODE_MO_tempo'] = shp_decoupREF.gdf['CODE_SME'].apply(lambda x:x.split("_SME")[0])
                        shp_decoupREF.gdf = shp_decoupREF.gdf.sort_values('ratio_surf',ascending=False).groupby(['CODE_MO_tempo','CODE_'+REF_entite]).first()
                        shp_decoupREF.gdf = shp_decoupREF.gdf.reset_index()
                        shp_decoupREF.gdf = shp_decoupREF.gdf[[x for x in list (shp_decoupREF.gdf) if x!='CODE_MO_tempo']]
            #Regles liées aux projets
            if projet!=None:
                ###Regles de tri uniques pour chaque projets
                if (projet.type_rendu=='tableau' or projet.type_rendu=='carte' or projet.type_rendu=='tableau_DORA_vers_BDD') and (projet.type_donnees=='action' or projet.type_donnees=='toutes_pressions'):
                    #Pour tous projets carto, on ne garde pas les entités qui ont au moins de 5% de la surface dans le final
                    if shp_decoupREF.type_de_geom=="polygon":
                        shp_decoupREF.gdf = shp_decoupREF.gdf.loc[(shp_decoupREF.gdf['ratio_surf']>0.05)]                     
                    
                    for echelle_carto_REF in projet.liste_echelle_REF_projet:
                        REF_entite = echelle_shp_par_decoupage[10:].split("_")[0]
                        REF_index = echelle_shp_par_decoupage[10:].split("_")[1]
                        if REF_entite=='ME' and REF_index=='custom':
                            shp_decoupREF.gdf = shp_decoupREF.gdf.loc[(shp_decoupREF.gdf['ratio_surf']>0.05)|(shp_decoupREF.gdf['surface_decoup'+REF_entite]>500000)]
                            shp_decoupREF.gdf.loc[shp_decoupREF.gdf.geom_type=='MultiPolygon','geometry'] = shp_decoupREF.gdf.loc[shp_decoupREF.gdf.geom_type=='MultiPolygon']['geometry'].map(lambda x : extraire_plus_gros_polygon(x))

                    for echelle_carto_REF in projet.liste_echelle_REF_projet:
                        REF_entite = echelle_shp_par_decoupage[10:].split("_")[0]
                        REF_index = echelle_shp_par_decoupage[10:].split("_")[1]
                        if (REF_entite=='ME' or REF_entite=='SME') and REF_index=='custom':
                            #Pour les PPG par MO, la ration de surface doit étre de 0.1 (Sauf si une action est bien présente sur le CODE_REF !) et on garde que les plus gros polygon
                            shp_decoupREF.gdf = shp_decoupREF.gdf.loc[(shp_decoupREF.gdf['ratio_surf']>0.1)|(shp_decoupREF.gdf['surface_decoup'+REF_entite]>5000000)]
                            shp_decoupREF.gdf.loc[shp_decoupREF.gdf.geom_type=='MultiPolygon','geometry'] = shp_decoupREF.gdf.loc[shp_decoupREF.gdf.geom_type=='MultiPolygon']['geometry'].map(lambda x : extraire_plus_gros_polygon(x))
                        if REF_entite=='PPG' and REF_index=='custom':
                            #Pour les PPG par MO, la ration de surface doit étre de 0.5 (Sauf si une action est bien présente sur le CODE_REF !) et on garde que les plus gros polygon
                            shp_decoupREF.gdf = shp_decoupREF.gdf.loc[(shp_decoupREF.gdf['ratio_surf']>0.5)|(shp_decoupREF.gdf['surface_decoup'+REF_entite]>20000000)]
                            shp_decoupREF.gdf.loc[shp_decoupREF.gdf.geom_type=='MultiPolygon','geometry'] = shp_decoupREF.gdf.loc[shp_decoupREF.gdf.geom_type=='MultiPolygon']['geometry'].map(lambda x : extraire_plus_gros_polygon(x))

                if (projet.type_rendu=='tableau_vierge') and (projet.type_donnees=='action'):
                    if shp_decoupREF.type_de_geom=="polygon":
                        if len(shp_decoupREF.gdf)>0:
                            shp_decoupREF.gdf = shp_decoupREF.gdf.loc[(shp_decoupREF.gdf['ratio_surf']>0.05)]                     

            if projet==None:
                REF_entite = echelle_shp_par_decoupage[10:].split("_")[0]
                REF_index = echelle_shp_par_decoupage[10:].split("_")[1]
                #Pour les PPG par MO, la ration de surface doit étre de 0.3 et on garde que les plus gros polygon
                if REF_entite=='SAGE' and REF_index=='MO':
                    shp_decoupREF.gdf = shp_decoupREF.gdf.loc[shp_decoupREF.gdf['ratio_surf']>0.9]
                #Pour les PPG par MO, la ration de surface doit étre de 0.3 et on garde que les plus gros polygon
                if REF_entite=='PPG' and REF_index=='custom':
                    if len(shp_decoupREF.gdf)>0:
                        shp_decoupREF.gdf = shp_decoupREF.gdf.loc[shp_decoupREF.gdf['ratio_surf']>0.3]
                        def extraire_plus_gros_polygon(multipolygon):
                            liste_filtre = [True if(a.area)>5000000 else False for a in multipolygon]
                            multipolygon = list(itertools.compress(multipolygon.geoms, liste_filtre))
                            multipolygon =  MultiPolygon(list(multipolygon))
                            return multipolygon
                        shp_decoupREF.gdf.loc[shp_decoupREF.gdf.geom_type=='MultiPolygon','geometry'] = shp_decoupREF.gdf.loc[shp_decoupREF.gdf.geom_type=='MultiPolygon']['geometry'].map(lambda x : extraire_plus_gros_polygon(x))
                if REF_entite=='ME' and (REF_index=='custom' or REF_index=='BVG' or REF_index=='PPG'):
                    shp_decoupREF.gdf = shp_decoupREF.gdf.loc[(shp_decoupREF.gdf['ratio_surf']>0.3)|(shp_decoupREF.gdf['surface_decoup'+REF_entite]>50000000)]
        return self

    def suppression_CODE_REF_vide(self):
        for echelle_shp_par_decoupage,shp_decoupREF in self.items():
            if len(shp_decoupREF.gdf)>0:
                REF_entite = echelle_shp_par_decoupage[10:].split("_")[0]
                REF_index = echelle_shp_par_decoupage[10:].split("_")[1]
                shp_decoupREF.gdf = shp_decoupREF.gdf.loc[~shp_decoupREF.gdf["CODE_"+REF_entite].isnull()]
                shp_decoupREF.gdf = shp_decoupREF.gdf.loc[~shp_decoupREF.gdf["CODE_"+REF_index].isnull()]
        return self
    
    liste_echelle_REF_projet = ajout_custom_liste_echelle_REF(self,dict_custom_maitre)
    self = ajout_custom_dict_geom_REF(self,dict_custom_maitre)
    liste_combinaison_REF = hierarchisation_liste_echelle(liste_echelle_REF_projet)
    liste_combinaison_REF = list(itertools.combinations(liste_combinaison_REF, 2))
    liste_combinaison_REF = [list(x) for x in liste_combinaison_REF]
    dict_geomREF_decoupREF = decoupage_entite_par_entite(self,liste_combinaison_REF,dict_custom_maitre)
    dict_geomREF_decoupREF = regle_tri_dict_decoupREF(dict_geomREF_decoupREF,dict_custom_maitre)
    #dict_geomREF_decoupREF = dictGdfCompletREF.suppression_entite_hors_des_custom(dict_geomREF_decoupREF,dict_custom_maitre)
    dict_geomREF_decoupREF = suppression_CODE_REF_vide(dict_geomREF_decoupREF)
    return dict_geomREF_decoupREF

def extraction_dict_relation_shp_liste_a_partir_decoupREF(dict_custom_maitre,dict_decoupREF):
    class DictListeREFparREF(dict):
        def __getitem__(self, key):
            if key not in self:
                self[key] = self.create_key(key)
            return super().__getitem__(key)
        
        def create_key(self,key):
            REF1 = key.split("_")[2]
            REF2 = key.split("_")[4]
            dict_temporaire_inverse = DictListeREFparREF({})
            for k,v in self['dict_liste_' + REF2 +'_par_' + REF1].items():
                for x in v:
                    dict_temporaire_inverse.setdefault(x,[]).append(k)
            dict_temporaire_inverse.REF_maitre = REF1
            dict_temporaire_inverse.REF_noob = REF2
            return dict_temporaire_inverse

    dict_relation_shp_liste = DictListeREFparREF({})
    
    for echelle_shp_par_decoupage,shp_decoupREF in dict_decoupREF.items():
        REF1 = shp_decoupREF.echelle_maitre
        REF2 = shp_decoupREF.echelle_noob
        df_decoupREF_REF = shp_decoupREF.gdf.groupby('CODE_'+REF2).agg({'CODE_'+REF1:lambda x: list(x)})
        df_decoupREF_REF.columns = ['liste_' + REF1 +'_par_' + REF2]
        dict_relation_shp_liste['dict_liste_' + REF1 +'_par_' + REF2] = DictListeREFparREF(df_decoupREF_REF.to_dict()['liste_' + REF1 +'_par_' + REF2])
        dict_relation_shp_liste['dict_liste_' + REF1 +'_par_' + REF2].REF_maitre = REF2
        dict_relation_shp_liste['dict_liste_' + REF1 +'_par_' + REF2].REF_noob = REF1


    list_CODE_custom = [v.CODE_custom for k,v in dict_custom_maitre.items()]
    for nom_dict_relation,dict_relation_REF1_REF2 in dict_relation_shp_liste.items():
        if nom_dict_relation.endswith("custom"):
            for CODE_custom in list_CODE_custom:
                if CODE_custom not in dict_relation_REF1_REF2:
                    dict_relation_REF1_REF2[CODE_custom] = []
    return dict_relation_shp_liste

 