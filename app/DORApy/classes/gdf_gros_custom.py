# -*- coding: utf-8 -*-
import geopandas as gpd
import numpy as np
import pandas as pd

class gdf_gros_custom(gpd.GeoDataFrame):
    @property
    def _constructor(self):
        return gdf_gros_custom

    def presence_alias(self):
        # return the geographic center point of this DataFrame
        liste_nom_potentiellement_alias = ['ALIAS',"Alias","alias"]
        for x in liste_nom_potentiellement_alias:
            if x in list(self):
                self.presence_alias = True
                self.nom_colonne_alias = x
        return self

    def modifier_liste_colonnes_a_garder_couche_custom(self,liste_colonnes_a_garder_couche_custom):
        self.liste_colonnes_a_garder_couche_custom = liste_colonnes_a_garder_couche_custom
        return self
