import pandas as pd
import numpy as np
import openpyxl
import random
import datetime as dt
class Production:
    def __init__(self):
        return 
######--------Conformez toutes les variables benef, coti et conso à celles de test.py
    def database(self, file_benef, file_cotisation, file_conso):
        self.file_benef = file_benef
        self.file_cotisation = file_cotisation
        self.file_conso = file_conso
        benef = pd.read_excel(file_benef)
        cotisation = pd.read_excel(file_cotisation)
        consommation = pd.read_excel(file_conso)
        #Nombre de police unique benef -- ok
        police_en_gestion = benef.groupby(["Num Police"])["Matricule"].agg({"count"}).reset_index().shape[0]

        #nombre de police unique cotisation -- ok
        police_facturee = len(cotisation.groupby(["Num Police"]))
                
        #nombre de ligne cotisation sans doublons -- ok
        piece_de_facturation = cotisation.drop_duplicates().shape[0] 

        #somme de beneficiaire par police unique -- ok
        beneficiaire = np.sum(benef.groupby(["Num Police"])["Matricule"].agg({"count"}).reset_index()["count"]) 
        
        #somme de MT PRIME NET sans doublons cotisation -- ok
        valeur_facturee = np.sum(cotisation.groupby(["Num Police"])["Mt Prime Net"].agg({"sum"}).reset_index()["sum"])
        return {
            "infos":
                       {
                        "police_en_gestion":police_en_gestion,
                        "police_facturee":police_facturee,
                        "piece_de_facturation":piece_de_facturation,
                        "beneficiaire":beneficiaire,
                        "valeur_facturee":valeur_facturee
                        },
       
            "db":
                {
                    "benef":benef,
                    "cotisation":cotisation,
                    "consommation":consommation,
                }
             }

        

    #Vérifiez si  nombre de police unique benef égale au nombre de police unique cotisation
    #sinon vérifiez si les police de différence consomment
    def production(self, file_benef, file_cotisation, file_conso):
        benef = self.database(file_benef,file_cotisation,file_conso)["db"]["benef"]
        cotisation = self.database(file_benef,file_cotisation,file_conso)["db"]["cotisation"]
        consommation = self.database(file_benef,file_cotisation,file_conso)["db"]["consommation"]

        df1 = benef["Num Police"].dropna().apply(lambda x: str(x).replace(" ","")).drop_duplicates().tolist()
        df2 = cotisation["Num Police"].dropna().apply(lambda x: str(x).replace(" ","")).drop_duplicates().tolist()
        df3 = consommation["Num Police"].dropna().apply(lambda x: str(x).replace(" ","")).drop_duplicates().tolist()
        result_1 = [id for id in df1 if id in df3 and id not in df2]
        
        return {
                "production":result_1
                }

    #Vérifiez si  nombre de police unique benef égale au nombre de police unique cotisation --ok
    def affiliation_avnants(self,file_benef,file_cotisation,file_conso):
        benef = self.database(file_benef,file_cotisation,file_conso)["db"]["benef"]
        cotisation = self.database(file_benef,file_cotisation,file_conso)["db"]["cotisation"]
        df1 = benef["Num Police"].dropna().apply(lambda x: str(x).replace(" ","")).drop_duplicates().tolist()
        df2 = cotisation["Num Police"].dropna().apply(lambda x: str(x).replace(" ","")).drop_duplicates().tolist()
        "Les NUM POLICE se trouvant dans beneficiaire  sans cotisation "
        result_1 = [id for id in df1 if id not in df2]
        
        return {
            "polices":result_1
            }
              

    #Choisir un nombre aléatoire parmi MT PRIME NET cotisation sans doublons --ok
    #Numéro de Quittance + Date émis policesion associé à soumettre  au courtier pour vérif
    def affiliation_pieces_justificatives(self, file_benef,file_cotisation,file_conso, n_alea=3):
        cotisation = self.database(file_benef,file_cotisation,file_conso)["db"]["cotisation"]
        val_alea = list(set(cotisation.drop_duplicates()["Num Police"].dropna().apply(lambda x: str(x))))
        random.shuffle(list(set(val_alea)))
        liste, n = [],0
        for i in val_alea:
            while len(liste) != n_alea:
                liste.append(i)
                n = n+1
        infos = {"Affiliation pièces justificatives":{}}
        for i in cotisation["Num Police"]:
            for j in liste:
                if i == j:
                    data = cotisation[cotisation["Num Police"]==i].drop_duplicates()
                    quittance = [i for i in data["Num Quittance"]]
                    date_emission = [i for i in data["Date Emission"]]
                    for i, j in zip(quittance,date_emission):
                        infos["Affiliation pièces justificatives"][f"[Quittance N°{i + 1}"] = f" {j}]"
                        
        return {
            "pieces_justif":list(infos['Affiliation pièces justificatives'].items())
        }

    #Choisir un nombre aléatoire de police  parmi cotisation sans doublons --ok
    def affiliation_facuration(self,file_benef,file_cotisation,file_conso, n_alea=3):
        
        cotisation = self.database(file_benef,file_cotisation,file_conso)["db"]["cotisation"]
        val_alea = list(set(cotisation.drop_duplicates()["Num Police"].dropna().apply(lambda x: str(x))))
        random.shuffle(val_alea)
        alea = val_alea[:n_alea]
        return {
            "aff_facuration": alea
        }
    #Vérifiez les numéros police benf sans cotisation avec consommation --ok
    def recouvrement(self,file_benef,file_cotisation,file_conso):
        benef = self.database(file_benef,file_cotisation,file_conso)["db"]["benef"]
        cotisation = self.database(file_benef,file_cotisation,file_conso)["db"]["cotisation"]
        consommation = self.database(file_benef,file_cotisation,file_conso)["db"]["consommation"]
        df1 = benef["Num Police"].dropna().apply(lambda x: str(x).replace(" ","")).drop_duplicates().tolist()
        df2 = cotisation["Num Police"].dropna().apply(lambda x: str(x).replace(" ","")).drop_duplicates().tolist()
        df3 = consommation["Num Police"].dropna().apply(lambda x: str(x).replace(" ","")).drop_duplicates().tolist()
        
       
        # 2. Les ID se trouvant dans BENEF et CONSO mais pas dans COTISA
        result_2 = [id for id in df1 if id in df3 and id not in df2]

        # 3. Les ID se trouvant dans CONSO mais pas dans BENEF et COTISA
        result_3 = [id for id in df3 if id not in df1 and id not in df2]
        
        return {
            "recouv":list(set(result_2 + result_3))
        }

    def facturation_frais_gestion(self,file_benef,file_cotisation,file_conso):
        return {
            "frais_gestion":"***"
        }
    
    def resultats(self, file_benef,file_cotisation,file_conso):
        production = self.production(file_benef,file_cotisation,file_conso)["production"]
        affiliation_avnants = self.affiliation_avnants(file_benef,file_cotisation,file_conso)["polices"]
        affiliation_pieces_justificatives = self.affiliation_pieces_justificatives(file_benef,file_cotisation,file_conso, n_alea=3)["pieces_justif"]
        affiliation_facuration = self.affiliation_facuration(file_benef,file_cotisation,file_conso, n_alea=3)["aff_facuration"]
        recouvrement = self.recouvrement(file_benef,file_cotisation,file_conso)["recouv"]
        facturation_frais_gestion = self.facturation_frais_gestion(file_benef,file_cotisation,file_conso)["frais_gestion"]  
        
        rs = {
            "result":[],
            "anorm":[]
        }
    
        
        if len(production) !=0:
            rs["result"].append("KO, anomalie constatée")
            rs["anorm"].append(production)
        else:
            rs["result"].append("OK")
            rs["anorm"].append("RAS")

        if len(affiliation_avnants) !=0:
            rs["result"].append("KO, anomalie constatée")
            rs["anorm"].append(affiliation_avnants)
        else:
            rs["result"].append("OK")
            rs["anorm"].append("RAS")


        if len(affiliation_pieces_justificatives) !=0:
            rs["result"].append("En cours, infos filiale / courtier attendus"),
            rs["anorm"].append("Attente des détails scannés des avenants spécifiés pour vérification des pièces constitutives.")



        if len(affiliation_facuration) !=0:
            rs["result"].append("En cours, infos filiale / courtier attendus"),
            rs["anorm"].append("Absence de détail de facturation relatif aux bénéficiaires des polices.")
    


        if len(recouvrement) !=0:
            rs["result"].append("En cours, infos filiale / courtier attendus"),
            rs["anorm"].append("Absence de l'état de recouvrement des factures de la période.")

        
        if len(facturation_frais_gestion) !=0:
            rs["result"].append("En cours, infos filiale / courtier attendus"),
            rs["anorm"].append("Absence des états de facturation des honoraires de gestion")

       

        return rs


#Prod = Production().recouvrement("E:/MCI-CARE-CI/SANLAM BENIN/RESULTATS/ASCOMA/PRODUCTION/BJ  BENEF  SEM01 2021 ASCOMA.xlsx","E:/MCI-CARE-CI/SANLAM BENIN/RESULTATS/ASCOMA/PRODUCTION/BJ COTIS SEM01 2021 ASCOMA.xlsx","E:/MCI-CARE-CI/SANLAM BENIN/RESULTATS/ASCOMA/CONSOMMATION/BJ ECARTS CONSOS SEM_01_2021 ASCOMA.xlsx")


class Prestation:
    def __init__(self):
        return 

    def database(self, file_benef, file_cotisation, file_conso):
        self.file_benef = file_benef
        self.file_cotisation = file_cotisation
        self.file_conso = file_conso
        benef = pd.read_excel(file_benef)
        cotisation = pd.read_excel(file_cotisation)
        consommation = pd.read_excel(file_conso)

        benef = pd.read_excel(file_benef)
        cotisation = pd.read_excel(file_cotisation)
        consommation = pd.read_excel(file_conso)

        #Nombre de police unique de prestations --ok
        police_presta = consommation.groupby(["Num Police"])["Matricule Beneficiaire"].agg({"count"}).reset_index().shape[0]

        #Nombre de beneficiaire des prestations
        beneficiaire_presta = len(set(consommation["Matricule Beneficiaire"]))

        #Dépense totale de toutes les prestations --ok
        depense_presta = np.sum(consommation.groupby(["Num Police"])["Montant Paye"].agg({"sum"}).reset_index()["sum"])

        #Nombre de ligne de consommations --ok
        enregistrements = consommation.shape[0]

        return  {
                    "infos":
                            {
                                "police_presta":police_presta,
                                "beneficiaire_presta":beneficiaire_presta,
                                "depense_presta":depense_presta,
                                "enregistrements":enregistrements, 
                                },
                    "db":
                        {
                            "benef":benef,
                            "cotisation":cotisation,
                            "consommation":consommation,
                        }
                }

    #Vérifiez si toutes les polices conso ont été facturées dans cotisation
    def conso_autorisees(self,file_benef,file_cotisation,file_conso):
        benef = self.database(file_benef,file_cotisation,file_conso)["db"]["benef"]
        cotisation = self.database(file_benef,file_cotisation,file_conso)["db"]["cotisation"]
        consommation = self.database(file_benef,file_cotisation,file_conso)["db"]["consommation"]
        df1 = benef["Num Police"].dropna().apply(lambda x: str(x).replace(" ","")).drop_duplicates().tolist()
        df2 = cotisation["Num Police"].dropna().apply(lambda x: str(x).replace(" ","")).drop_duplicates().tolist()
        df3 = consommation["Num Police"].dropna().apply(lambda x: str(x).replace(" ","")).drop_duplicates().tolist()
        
        # 1. Les ID se trouvant dans df3 mais pas dans df2
        result_1 = [id for id in df3 if id not in df2]
      
        # 2. Les ID se trouvant dans df1 et df3 mais pas dans df2
        result_2 = [id for id in df1 if id in df3 and id not in df2]

        # 3. Les ID se trouvant dans df3 mais pas dans df1 et df2
        result_3 = [id for id in df3 if id not in df1 and id not in df2]
        return {
            "conso_auto":set(result_1+result_2+result_3)
        }

    #Verifier que la date émission cotisation <= date fin benef sinon relever les consommation associées
    def periode_couverture(self,file_benef,file_cotisation,file_conso,date_fin):
        cotisation = self.database(file_benef,file_cotisation,file_conso)["db"]["cotisation"].reset_index(drop=True)
        consommation = self.database(file_benef,file_cotisation,file_conso)["db"]["consommation"].reset_index(drop=True)
        cotisation_filtre = cotisation[cotisation['Date Emission'] >= pd.to_datetime(date_fin, format='%d/%m/%Y', dayfirst=True)]["Num Police"].tolist()
        filtrage = set(list(consommation[consommation['Num Police'].isin(cotisation_filtre)]['Num Police']))

        return {
            "periode_couv": filtrage
        }

    #Verifiez que les enfants age <= 25 et les adultes <= 60 dans benef sinon relevez les conso associées
    def condition_age(self,file_benef,file_cotisation,file_conso,date_fin="31/12/2022"):
        def age(x):
            if isinstance(x, str):
                return -5555555
            else:
                today = dt.datetime.strptime(str(date_fin), "%d/%m/%Y").date()
                return today.year - x.year - ((today.month, today.day) < (x.month, x.day))

        benef = self.database(file_benef,file_cotisation,file_conso)["db"]["benef"]
        consommation = self.database(file_benef,file_cotisation,file_conso)["db"]["consommation"]

        benef_sans_doublon = benef.drop_duplicates()
        benef_sans_doublon["Date Naissance"] = pd.to_datetime(benef_sans_doublon['Date Naissance'], format='infer', errors='coerce')
        benef_sans_doublon["age"] = benef_sans_doublon['Date Naissance'].apply(age)

        sans_doublons_conso = consommation.drop_duplicates()
        ENFANT_SUP_25 = benef_sans_doublon[benef_sans_doublon["Statut Ace"].isin(['E']) & (benef_sans_doublon['age'] > 25)]
        ADULTES_SUP_60 = benef_sans_doublon[benef_sans_doublon["Statut Ace"].ne('E') & (benef_sans_doublon['age'] > 60)]

        cond1 = sans_doublons_conso['Matricule Beneficiaire'].isin(ENFANT_SUP_25["Matricule"].unique())
        ENFANT_SUP_25_CONSO = sans_doublons_conso[cond1]["Num Police"].apply(lambda x: str(x)).tolist()

        cond2 = sans_doublons_conso['Matricule Beneficiaire'].isin(ADULTES_SUP_60["Matricule"].unique())
        ADULTES_SUP_60_CONSO = sans_doublons_conso[cond2]["Num Police"].apply(lambda x: str(x)).tolist()
        
        return {
            "cndt_age": set(ENFANT_SUP_25_CONSO + ADULTES_SUP_60_CONSO)
        }



      #Vérifiez que les lignes consommation sont unique sinon relevez les conso associées
    def double_conso(self,file_benef,file_cotisation,file_conso):
        consommation = self.database(file_benef,file_cotisation,file_conso)["db"]["consommation"]
        dble_conso = set(consommation[consommation.duplicated(keep=False)]["Num Police"].apply(lambda x: str(x)).tolist())
        return {
                "db_conso":dble_conso
        }


    #Verifiez que date soins consommation - date emission cotisation <= 3 mois sinon relevez les conso associées
    def delai_contractuel(self,file_benef,file_cotisation,file_conso):
        cotisation = self.database(file_benef,file_cotisation,file_conso)["db"]["cotisation"]
        consommation = self.database(file_benef,file_cotisation,file_conso)["db"]["consommation"]
        # Convertissez les colonnes de dates en objets datetime si elles ne le sont pas déjà
        cotisation['Date Emission'] = pd.to_datetime(cotisation['Date Emission'])
        consommation['Date Soins'] = pd.to_datetime(consommation['Date Soins'])

        # Calculez la différence en mois
        consommation['Difference en mois'] = (abs(cotisation['Date Emission'] - consommation['Date Soins']).dt.days / 30)

        # Filtrez les lignes où la différence est supérieure à 3 mois
        liste = set(list(consommation[consommation["Difference en mois"] > 3]["Num Police"]))

        return {
            "delai_cnt": liste
        }
  
    #Choisir quelques consommation élévées
    def depense_imortantes(self,file_benef,file_cotisation,file_conso):
        consommation = self.database(file_benef,file_cotisation,file_conso)["db"]["consommation"]
        # Trier par ordre décroissant de la colonne "MT" et sélectionner les n premiers éléments
        conso_sorted = consommation.sort_values(by='Montant Paye', ascending=False).drop_duplicates(subset=['Montant Paye','Num Police'], keep='first')

        # Obtenir les valeurs de la colonne "NUM_POLICE" des n premiers éléments
        n_premiers_NUM_POLICE = set(conso_sorted['Num Police'].tolist())
        return {
            "dp_mpt":n_premiers_NUM_POLICE
        }
    
    def resultats(self, file_benef,file_cotisation,file_conso,date_fin):
        conso_autorisees = self.conso_autorisees(file_benef,file_cotisation,file_conso)["conso_auto"]
        periode_couverture = self.periode_couverture(file_benef,file_cotisation,file_conso,date_fin)["periode_couv"]
        condition_age = self.condition_age(file_benef,file_cotisation,file_conso, date_fin)["cndt_age"]
        double_conso = self.double_conso(file_benef,file_cotisation,file_conso)["db_conso"]
        delai_contractuel = self.delai_contractuel(file_benef,file_cotisation,file_conso)["delai_cnt"]
        depense_imortantes = self.depense_imortantes(file_benef,file_cotisation,file_conso)["dp_mpt"]  
        
        rs = {"result":[], "anorm":[]}
        
        if len(conso_autorisees) !=0:
            rs["result"].append("KO, anomalie constatée")
            rs["anorm"].append(conso_autorisees)
        else:
            rs["result"].append("OK")
            rs["anorm"].append("NEANT")

        if len(periode_couverture) !=0:
            rs["result"].append("KO, anomalie constatée")
            rs["anorm"].append(periode_couverture)
        else:
            rs["result"].append("OK")
            rs["anorm"].append("NEANT")


        if len(condition_age) !=0:
            rs["result"].append("KO, anomalie constatée"),
            rs["anorm"].append(condition_age)
        else:
            rs["result"].append("OK")
            rs["anorm"].append("NEANT")




        if len(double_conso) !=0:
            rs["result"].append("KO, anomalie constatée"),
            rs["anorm"].append(double_conso)
        else:
            rs["result"].append("OK")
            rs["anorm"].append("NEANT")


        if len(delai_contractuel) !=0:
            rs["result"].append("KO, anomalie constatée"),
            rs["anorm"].append(delai_contractuel)
        else:
            rs["result"].append("OK")
            rs["anorm"].append("NEANT")

        
        if len(depense_imortantes) !=0:
            rs["result"].append("KO, anomalie constatée"),
            rs["anorm"].append(depense_imortantes)

        return rs

#     #Choisir un certains de consommation doit la fréquence est regulière au fil des mois consécutifs
#     def depense_frequente(self, seuil):
#         freq_conso = self.consommation.groupby(["NUM_POLICE"])["NUM_POLICE"].agg({"count"}).reset_index()
#         return {
#             "7.Dépenses fréquentes":""
#         }
        
# Presta = Prestation().periode_couverture("E:/MCI-CARE-CI/SANLAM BENIN/RESULTATS/ASCOMA/PRODUCTION/BJ  BENEF  SEM01 2021 ASCOMA.xlsx","E:/MCI-CARE-CI/SANLAM BENIN/RESULTATS/ASCOMA/PRODUCTION/BJ COTIS SEM01 2021 ASCOMA.xlsx","E:/MCI-CARE-CI/SANLAM BENIN/RESULTATS/ASCOMA/CONSOMMATION/BJ ECARTS CONSOS SEM_01_2021 ASCOMA.xlsx","31/12/2021")
# print(Presta)