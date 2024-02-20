import pandas as pd
from radiateur import Radiateur

# ---------------------- PARAMETRES -------------------------
# Fichiers CSV des radiateurs à utiliser
FICHIERS = ["radiateur_bat_principal", "radiateurs_conciergerie"]
# Régime de fonctionnement respectifs à analyser (entrée, sortie)
REGIME = [(45, 30), (50, 30)]
# Régime de dimensionnement respectifs des radiateurs (entrée, sortie)
REGIME_DIM = [(60, 40), (60, 40)]


# ------------------- IMPORT DATA RADIATEUR ------------------------
def import_radiateur(fichier_rad, t_entree_dim, t_sortie_dim):
    df_radiateurs = pd.read_csv(f"data/{fichier_rad}.csv", delimiter=";")
    liste_de_radiateur = []
    for index, rows in df_radiateurs.iterrows():
        puissance_nom = int(rows["Puissance [W]"])
        consigne_temp_ambiante = int(rows["Consigne"])
        radiateur = Radiateur(puissance_nominale=puissance_nom, temperature_ambiante=consigne_temp_ambiante, t_entree_dim=t_entree_dim, t_sortie_dim=t_sortie_dim)
        liste_de_radiateur.append(radiateur)
    return liste_de_radiateur


# ------------------- CALCUL PUISSANCE TOTALE RADIATEUR ------------------------
def calcul_puissance_totale(liste_de_radiateur, t_entree, t_sortie):
    puissance_tot = 0
    for radiateur in liste_de_radiateur:
        puissance = float(radiateur.calcul_puissance(t_entree=t_entree, t_sortie=t_sortie))
        puissance_tot += puissance
    return puissance_tot


# --------------------- AFFICHAGE DES RESULTATS --------------------------
def affichage_resultats(puissance_tot, fichier_rad, t_entree, t_sortie):
    print(f"\nRégime de température :\nEntrée : {t_entree}\nSortie : {t_sortie}")
    print(f"\nLa puissance développée par les radiateurs de '{fichier_rad}' est de : {puissance_tot} W soit {puissance_tot / 1000} kW")


if __name__ == "__main__":
    for fichier, regime, dim in zip(FICHIERS, REGIME, REGIME_DIM):
        liste_radiateur = import_radiateur(fichier_rad=fichier, t_entree_dim=dim[0], t_sortie_dim=dim[1])
        puissance_totale = calcul_puissance_totale(liste_de_radiateur=liste_radiateur, t_entree=regime[0], t_sortie=regime[1])
        affichage_resultats(puissance_tot=puissance_totale, fichier_rad=fichier, t_entree=regime[0], t_sortie=regime[1])
