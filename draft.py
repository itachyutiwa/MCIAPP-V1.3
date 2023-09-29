import locale
locale.setlocale(locale.LC_ALL, 'fr_FR.utf8')  # Remplacez 'fr_FR.utf8' par la locale appropriée
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from ttkbootstrap import Style  
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import Label
import datetime as dt
import pandas as pd
import os
import numpy as np

# Global variables to store the file paths
selected_beneficiaire_path = ""
selected_emission_path = ""
selected_consommation_path = ""

def upload_beneficiaire_file():
    global selected_beneficiaire_path
    file_path = filedialog.askopenfilename()
    if file_path:
        selected_beneficiaire_path = file_path
        beneficiaire_entry.delete(0, tk.END)
        beneficiaire_entry.insert(0, selected_beneficiaire_path)

def upload_emission_file():
    global selected_emission_path
    file_path = filedialog.askopenfilename()
    if file_path:
        selected_emission_path = file_path
        emission_entry.delete(0, tk.END)
        emission_entry.insert(0, selected_emission_path)

def upload_consommation_file():
    global selected_consommation_path
    file_path = filedialog.askopenfilename()
    if file_path:
        selected_consommation_path = file_path
        consommation_entry.delete(0, tk.END)
        consommation_entry.insert(0, selected_consommation_path)


def age(x):
    if isinstance(x, str):
        return -5555555
    else:
        today = dt.datetime.strptime(str(end_date_entry.get()),"%d/%m/%Y").date()
        return today.year - x.year - ((today.month, today.day) < (x.month, x.day))



def toggle_date_fields_benef():
    if benef_checkbox_var.get() == 1:
        anterieure_entry_benef_sortie.config(state="normal")
        posterieure_entry_benef_sortie.config(state="normal")
    else:
        anterieure_entry_benef_sortie.config(state="disabled")
        posterieure_entry_benef_sortie.config(state="disabled")


def toggle_date_fields_emission():
    if emission_checkbox_var.get() == 1:
        anterieure_date_emission_entry.config(state="normal")
        posterieure_date_emission_entry.config(state="normal")
    else:
        anterieure_date_emission_entry.config(state="disabled")
        posterieure_date_emission_entry.config(state="disabled")


    
def toggle_date_fields_conso():
    if conso_checkbox_var.get() == 1:
        anterieure_dt_soins_conso.config(state="normal")
        posterieure_dt_soins_conso.config(state="normal")
        anterieure_date_recept_conso.config(state="normal")
        posterieure_date_recept_conso.config(state="normal")

    else:
        anterieure_dt_soins_conso.config(state="disabled")
        posterieure_dt_soins_conso.config(state="disabled")
        anterieure_date_recept_conso.config(state="disabled")
        posterieure_date_recept_conso.config(state="disabled")




# Create the main window
window = tk.Tk()
window.title("********************** CONTROLE DELEGUE MCI-CARE COTE D'IVOIRE *************************")

# Create a ttkbootstrap style
style = Style(theme="superhero")

# Create Label, Entry field, and Upload button for BENEFICIAIRE
beneficiaire_label = ttk.Label(window, text="BENEFICIAIRE:")
beneficiaire_label.grid(row=0, column=0, padx=10, pady=5)

beneficiaire_entry = ttk.Entry(window, width=50)
beneficiaire_entry.grid(row=0, column=1, padx=10, pady=5)

beneficiaire_upload_button = ttk.Button(window, text="Chargez fichier BENEFICIAIRE", command=upload_beneficiaire_file)
beneficiaire_upload_button.grid(row=0, column=2, padx=10, pady=10)

# Create Label, Entry field, and Upload button for EMISSION
emission_label = ttk.Label(window, text="EMISSION:")
emission_label.grid(row=1, column=0, padx=10, pady=5)

emission_entry = ttk.Entry(window, width=50)
emission_entry.grid(row=1, column=1, padx=10, pady=5)

emission_upload_button = ttk.Button(window, text="Chargez fichier EMISSION", command=upload_emission_file)
emission_upload_button.grid(row=1, column=2, padx=10, pady=10)

# Create Label, Entry field, and Upload button for CONSOMMATION
consommation_label = ttk.Label(window, text="CONSOMMATION:")
consommation_label.grid(row=2, column=0, padx=10, pady=5)

consommation_entry = ttk.Entry(window, width=50)
consommation_entry.grid(row=2, column=1, padx=10, pady=5)

consommation_upload_button = ttk.Button(window, text="Chargez fichier CONSOMMATION", command=upload_consommation_file)
consommation_upload_button.grid(row=2, column=2, padx=10, pady=10)

# Label and Entry for Start Date
start_label = ttk.Label(window, text="Date début:")
start_label.grid(row=3, column=0, padx=10, pady=10, sticky="w")
start_date_entry = ttk.Entry(window)
start_date_entry.grid(row=3, column=1, padx=10, pady=10, sticky="w")

# Label and Entry for End Date
end_label = ttk.Label(window, text="Date de fin:")
end_label.grid(row=3, column=2, padx=10, pady=10, sticky="w")
end_date_entry = ttk.Entry(window)
end_date_entry.grid(row=3, column=3, padx=10, pady=10, sticky="w")

# Label and Entry for Seuil coûteux
seuil_label = ttk.Label(window, text="Seuil coûteux:")
seuil_label.grid(row=4, column=0, padx=10, pady=10, sticky="w")
seuil_entry = ttk.Entry(window)
seuil_entry.grid(row=4, column=1, padx=10, pady=10, sticky="w")

# Label and Entry for COUTIER
COUTIER_label = ttk.Label(window, text="COUTIER:")
COUTIER_label.grid(row=4, column=2, padx=10, pady=10, sticky="w")
COUTIER_entry = ttk.Entry(window)
COUTIER_entry.grid(row=4, column=3, padx=10, pady=10, sticky="w")



#Début

# Add a label for RESTRICTIONS
restrictions_label = ttk.Label(window, text="RESTRICTIONS", font=("Helvetica", 12, "bold"))
restrictions_label.grid(row=5, column=0, columnspan=3, padx=10, pady=10, sticky="w")

# Create IntVar variables for the checkboxes
benef_checkbox_var = tk.IntVar()
emission_checkbox_var = tk.IntVar()
conso_checkbox_var = tk.IntVar()



# Create checkboxes for BENEF, EMISSION, and CONSO
benef_checkbox = ttk.Checkbutton(window, text="BENEF.", variable=benef_checkbox_var, command=toggle_date_fields_benef)
benef_checkbox.grid(row=6, column=0, padx=10, pady=5, sticky="w")

emission_checkbox = ttk.Checkbutton(window, text="EMISSION.", variable=emission_checkbox_var, command=toggle_date_fields_emission)
emission_checkbox.grid(row=6, column=1, padx=10, pady=5, sticky="w")

conso_checkbox = ttk.Checkbutton(window, text="CONSO.", variable=conso_checkbox_var, command=toggle_date_fields_conso)
conso_checkbox.grid(row=6, column=2, padx=10, pady=5, sticky="w")


# Créez une étiquette pour afficher le texte "BENEFICIAIRE"
benef_label = Label(window, text="BENEFICIAIRE", font=("Arial", 10, "bold"))
benef_label.grid(row=7, column=2, columnspan=3, padx=10, pady=10, sticky="w")



date_sortie_label_benf = ttk.Label(window, text="Date sortie ")
anterieure_entry_benef_sortie = ttk.Entry(window, state="disabled")
posterieure_entry_benef_sortie = ttk.Entry(window, state="disabled")
anterieure_entry_benef_sortie.grid(row=8, column=2, padx=10, pady=5, sticky="w")
posterieure_entry_benef_sortie.grid(row=8, column=4, padx=10, pady=5, sticky="w")
antérieur_entry_date_sortie = ttk.Label(window, text="Antérieur à :") #Début
antérieur_entry_date_sortie.grid(row=8, column=1, padx=10, pady=5, sticky="e")
posterieur_entry_date_sortie = ttk.Label(window, text="Postérieur à :")
posterieur_entry_date_sortie.grid(row=8, column=3, padx=10, pady=5, sticky="e")#Fin
date_sortie_label_benf.grid(row=8, column=0, padx=10, pady=5, sticky="w")



# Créez une étiquette pour afficher le texte "BENEFICIAIRE"
emission_label = Label(window, text="EMISSION", font=("Arial", 10, "bold"))
emission_label.grid(row=11, column=2, columnspan=3, padx=10, pady=10, sticky="w")


date_emission_label = ttk.Label(window, text="Date émission ")
anterieure_date_emission_entry = ttk.Entry(window, state="disabled")
posterieure_date_emission_entry = ttk.Entry(window, state="disabled")
date_emission_label.grid(row=12, column=0, padx=10, pady=5, sticky="w")
anterieure_date_emission_entry.grid(row=12, column=2, padx=10, pady=5, sticky="w")
posterieure_date_emission_entry.grid(row=12, column=4, padx=10, pady=5, sticky="w")
antérieur_date_emission = ttk.Label(window, text="Antérieur à :") #Début
antérieur_date_emission .grid(row=12, column=1, padx=10, pady=5, sticky="e")
posterieur_date_emission  = ttk.Label(window, text="Postérieur à :")
posterieur_date_emission .grid(row=12, column=3, padx=10, pady=5, sticky="e")#Fin label

#Début
# Créez une étiquette pour afficher le texte "BENEFICIAIRE"
conso_label = Label(window, text="CONSO", font=("Arial", 10, "bold"))
conso_label.grid(row=15, column=2, columnspan=3, padx=10, pady=10, sticky="w")

# Initially disable the date fields
date_soins_label_conso = ttk.Label(window, text="Date soins ")
anterieure_dt_soins_conso = ttk.Entry(window, state="disabled")
posterieure_dt_soins_conso = ttk.Entry(window, state="disabled")
date_soins_label_conso.grid(row=16, column=0, padx=10, pady=5, sticky="w")
anterieure_dt_soins_conso.grid(row=16, column=2, padx=10, pady=5, sticky="w")
posterieure_dt_soins_conso.grid(row=16, column=4, padx=10, pady=5, sticky="w")
antérieur_date_soins = ttk.Label(window, text="Antérieur à :") #Début
antérieur_date_soins.grid(row=16, column=1, padx=10, pady=5, sticky="e")
posterieur_date_soins  = ttk.Label(window, text="Postérieur à :")
posterieur_date_soins.grid(row=16, column=3, padx=10, pady=5, sticky="e")#Fin label


date_recept_conso = ttk.Label(window, text="Date réception ")
anterieure_date_recept_conso = ttk.Entry(window, state="disabled")
posterieure_date_recept_conso = ttk.Entry(window, state="disabled")
date_recept_conso.grid(row=17, column=0, padx=10, pady=5, sticky="w")
anterieure_date_recept_conso.grid(row=17, column=2, padx=10, pady=5, sticky="w")
posterieure_date_recept_conso.grid(row=17, column=4, padx=10, pady=5, sticky="w")
antérieur_date_rgl = ttk.Label(window, text="Antérieur à :") #Début
antérieur_date_rgl.grid(row=17, column=1, padx=10, pady=5, sticky="e")
posterieur_date_rgl  = ttk.Label(window, text="Postérieur à :")
posterieur_date_rgl.grid(row=17, column=3, padx=10, pady=5, sticky="e")#Fin label



#---------------- LES FONCTIONS
def critere_benef(file,ante=pd.to_datetime(str(start_date_entry.get())), post=pd.to_datetime(str(end_date_entry.get()))):
    nom_dossier = str(COUTIER_entry.get())
    sous_dossier = "PRODUCTION"
    if not os.path.exists(nom_dossier):
        os.mkdir(nom_dossier)
    if not os.path.exists(os.path.join(nom_dossier, sous_dossier)):
        os.mkdir(os.path.join(nom_dossier, sous_dossier))

    benef = pd.read_excel(file)
    benef["Date Sortie"] = pd.to_datetime(benef["Date Sortie"], format='%d/%m/%Y', errors='coerce')
    benef["Date Sortie"] = benef["Date Sortie"].apply(lambda x: pd.NaT if x > post else x)
    benef = benef[(benef["Date Sortie"].lt(pd.to_datetime(str(post)))) & (benef["Date Sortie"].gt(pd.to_datetime(ante))) | (benef["Date Sortie"].isna())]
    benef_doublon = benef[benef.duplicated(keep=False)]
    benef_sans_doublon = benef.drop_duplicates()

    police_benef = benef_sans_doublon.groupby(["Num Police"])["Num Police"].agg({"count"}).reset_index()
    benef_sans_doublon["age"] = pd.to_datetime(benef_sans_doublon['Date Naissance']).apply(age)
    benef_sans_date_naiss = benef_sans_doublon[benef_sans_doublon['Date Naissance'].isna()]


    if benef_sans_doublon.shape[0] != 0:
        ENFANT_SUP_25 = benef_sans_doublon[benef_sans_doublon["Statut Ace"].isin(['E']) & (benef_sans_doublon['age'] > 25)]
        ADULTES_SUP_60 = benef_sans_doublon[benef_sans_doublon["Statut Ace"].ne('E') & (benef_sans_doublon['age'] > 60)]
    else:
        ENFANT_SUP_25 = benef_sans_doublon
        ADULTES_SUP_60 = benef_sans_doublon
    
    
    if len(benef_sans_doublon) !=0:  

            path_sans_doublon = os.path.join(nom_dossier, sous_dossier, "SANS_DOUBLONS BENEF.xlsx") 
            benef_sans_doublon.to_excel(path_sans_doublon)

    if len(benef_doublon) !=0:
        path_doublon = os.path.join(nom_dossier, sous_dossier, "DOUBLONS BENEF.xlsx")
        benef_doublon.to_excel(path_doublon)

    if len(police_benef) !=0:
            path_police_benef = os.path.join(nom_dossier, sous_dossier, "POLICE BENEF.xlsx")
            police_benef.to_excel(path_police_benef)

    if len(ENFANT_SUP_25) !=0:
            path_ENFANT_SUP_25 = os.path.join(nom_dossier, sous_dossier, "ENFANT_25.xlsx")
            ENFANT_SUP_25.to_excel(path_ENFANT_SUP_25)

    if len(ADULTES_SUP_60) !=0:
        path_ADULTES_SUP_60 = os.path.join(nom_dossier, sous_dossier, "ADULTE_60.xlsx")
        ADULTES_SUP_60.to_excel(path_ADULTES_SUP_60)
    
    if len(benef_sans_date_naiss) != 0:
        path_benef_sans_date_naiss = os.path.join(nom_dossier, sous_dossier, "BENEF SANS DATE DE NAISSANCE.xlsx")
        benef_sans_date_naiss.to_excel(path_benef_sans_date_naiss)
    return

def critere_emission(file, post=pd.to_datetime(str(end_date_entry.get()))):
    nom_dossier = str(COUTIER_entry.get())
    sous_dossier = "PRODUCTION"
    if not os.path.exists(nom_dossier):
        os.mkdir(nom_dossier)
    if not os.path.exists(os.path.join(nom_dossier, sous_dossier)):
        os.mkdir(os.path.join(nom_dossier, sous_dossier))

    emission = pd.read_excel(file)
    emission["Date Emission"] = pd.to_datetime(emission["Date Emission"], format='%d/%m/%Y', errors='coerce')
    emission = emission[(emission["Date Emission"] <= pd.to_datetime(str(anterieure_date_emission_entry.get())))]
    doublons_emission = emission[emission.duplicated(keep=False)]
    sans_doublons_emission =emission.drop_duplicates()
    police_emission = emission.groupby(["Gestionnaire"])["Mt Prime Net"].agg({"sum","count"}).sort_values(by=['sum'], ascending=False).reset_index()
    
    if len(doublons_emission) !=0:
        path_doublon = os.path.join(nom_dossier, sous_dossier, "SANS_DOUBLONS BENEF.xlsx") 
        doublons_emission.to_excel(path_doublon)
        
    if len(sans_doublons_emission) !=0:
        path_sans_doublon = os.path.join(nom_dossier, sous_dossier, "SANS_DOUBLONS EMISSION.xlsx") 
        sans_doublons_emission.to_excel(path_sans_doublon)
    
    if len(police_emission) !=0:
        path_police_emission = os.path.join(nom_dossier, sous_dossier, "POLICE EMMISSION.xlsx") 
        police_emission.to_excel(path_police_emission)
    return

def critere_conso(file):
        nom_dossier = str(COUTIER_entry.get())
        sous_dossier = "CONSOMMATION"
        if not os.path.exists(nom_dossier):
            os.mkdir(nom_dossier)
        if not os.path.exists(os.path.join(nom_dossier, sous_dossier)):
            os.mkdir(os.path.join(nom_dossier, sous_dossier))

        conso = pd.read_excel(file)
        doublons_conso = conso[conso.duplicated(keep=False)]
        sans_doublons_conso = conso.drop_duplicates()
        police_conso = conso.groupby(['Num Police'])['Montant Paye'].agg({"count","sum"}).sort_values(by=["count"], ascending=False).reset_index()
        
        if len(doublons_conso) != 0:
            path_doublon = os.path.join(nom_dossier, sous_dossier, "DOUBLONS CONSO.xlsx") 
            doublons_conso.to_excel(path_doublon)

        if len(sans_doublons_conso) != 0:
            path_sans_doublons_conso = os.path.join(nom_dossier, sous_dossier,"SANS_DOUBLONS CONSO.xlsx")
            sans_doublons_conso.to_excel(path_sans_doublons_conso)

        if len(police_conso) !=0:
            path_police_conso = os.path.join(nom_dossier, sous_dossier,"POLICE CONSO.xlsx")
            police_conso.to_excel(path_police_conso)
        return


def resume(file_benef, file_emission, file_conso, seuil_ctx,ante=pd.to_datetime(str(start_date_entry.get())), post=pd.to_datetime(str(end_date_entry.get()))):
    nom_dossier = str(COUTIER_entry.get())
    sous_dossier = "RESULTATS"
    if not os.path.exists(nom_dossier):
        os.mkdir(nom_dossier)
    if not os.path.exists(os.path.join(nom_dossier, sous_dossier)):
        os.mkdir(os.path.join(nom_dossier, sous_dossier))

    benef = pd.read_excel(file_benef)
    benef["Date Sortie"] = pd.to_datetime(benef["Date Sortie"], format='%d/%m/%Y', errors='coerce')
    benef["Date Sortie"] = benef["Date Sortie"].apply(lambda x: pd.NaT if x >= post else x)
    benef = benef[(benef["Date Sortie"] <= pd.to_datetime(str(post))) & (benef["Date Sortie"] >= pd.to_datetime(str(ante))) | (benef["Date Sortie"].isna())]

    emission = pd.read_excel(file_emission)
    emission = emission[(emission["Date Emission"] <= pd.to_datetime(str(anterieure_date_emission_entry.get())))]
    emission["Date Emission"] = pd.to_datetime(emission["Date Emission"], format='%d/%m/%Y', errors='coerce')

    conso = pd.read_excel(file_conso)

    benef_sans_doublon = benef.drop_duplicates()
    benef_sans_doublon["age"] = pd.to_datetime(benef_sans_doublon['Date Naissance']).apply(age)
    benef_sans_date_naiss = benef_sans_doublon[benef_sans_doublon['Date Naissance'].isna()]
    sans_doublons_emission =emission.drop_duplicates()
    sans_doublons_conso = conso.drop_duplicates()
    if benef_sans_doublon.shape[0] != 0:
        ENFANT_SUP_25 = benef_sans_doublon[benef_sans_doublon["Statut Ace"].isin(['E']) & (benef_sans_doublon['age'] > 25)]
        ADULTES_SUP_60 = benef_sans_doublon[benef_sans_doublon["Statut Ace"].ne('E') & (benef_sans_doublon['age'] > 60)]
    else:
        ENFANT_SUP_25 = benef_sans_doublon
        ADULTES_SUP_60 = benef_sans_doublon
    
    
    liste_police_anormale = set(sans_doublons_conso["Num Police"]).difference(set(sans_doublons_emission["Num Police"]))

    cond1 = sans_doublons_conso['Num Police'].isin(liste_police_anormale) & pd.to_datetime(sans_doublons_conso["Date Soins"]).gt(pd.to_datetime(str(start_date_entry.get())))
    police_anomale = sans_doublons_conso[cond1].astype({'Montant Paye': 'float'})

    police_anomale_resume = police_anomale.groupby(['Num Police'])['Montant Paye'].agg(['count', 'sum']).reset_index()


    if len(ADULTES_SUP_60) !=0:
        try:
            cond2 = sans_doublons_conso['Matricule Beneficiaire'].isin(ADULTES_SUP_60["Matricule"].unique())
            ADULTES_SUP_60_CONSO = sans_doublons_conso[cond2]
        except:
            print("ADULTES_SUP_60 vide")
    
    if len(ENFANT_SUP_25) !=0:
        try:
            cond3 = sans_doublons_conso['Matricule Beneficiaire'].isin(ENFANT_SUP_25["Matricule"].unique())
            ENFANT_SUP_25_CONSO = sans_doublons_conso[cond3]
        except:
            print("ENFANT_25_CONSO vide")
    
    if len(benef_sans_date_naiss) != 0:
        try:
            condition = sans_doublons_conso['Matricule Beneficiaire'].isin(benef_sans_date_naiss["Matricule"].unique())
            benef_sans_date_naiss = sans_doublons_conso[condition]
        except:
            print("benef_sans_date_naiss vide")

    cond4 = pd.to_datetime(sans_doublons_conso["Date Soins"]).lt(pd.to_datetime(str(anterieure_dt_soins_conso.get()))) & pd.to_datetime(sans_doublons_conso["Date Recepetion"]).gt(pd.to_datetime(str(posterieure_date_recept_conso.get())))
    PRESTATIONS_TARDIVES = sans_doublons_conso[cond4]
    
    cond5 = sans_doublons_conso['Montant Paye'].astype("float").gt(float(seuil_ctx))
    CONSO_COUTEUSES = sans_doublons_conso[cond5]

    if len(ENFANT_SUP_25_CONSO) !=0:
            path_ENFANT_SUP_25_CONSO = os.path.join(nom_dossier, sous_dossier, "ENFANT_SUP_25_CONSO.xlsx")
            ENFANT_SUP_25_CONSO.to_excel(path_ENFANT_SUP_25_CONSO)

    if len(ADULTES_SUP_60_CONSO) !=0:
        path_ADULTES_SUP_60_CONSO = os.path.join(nom_dossier, sous_dossier, "ADULTE_60.xlsx")
        ADULTES_SUP_60_CONSO.to_excel(path_ADULTES_SUP_60_CONSO)

    if len(police_anomale) != 0:
        path_police_anomale =  os.path.join(nom_dossier, sous_dossier, "POLICES ANORMALES.xlsx")
        police_anomale.to_excel(path_police_anomale)

    if len(police_anomale_resume) != 0:   
        path_police_anomale_resume =  os.path.join(nom_dossier, sous_dossier, "POLICE ANORMALES RESUME.xlsx")
        police_anomale_resume.to_excel(path_police_anomale_resume)

    if len(PRESTATIONS_TARDIVES) != 0:
        path_PRESTATIONS_TARDIVES =  os.path.join(nom_dossier, sous_dossier, "CONSO TARDIVES.xlsx")
        PRESTATIONS_TARDIVES.to_excel(path_PRESTATIONS_TARDIVES)

    if len(CONSO_COUTEUSES) != 0:
        path_CONSO_COUTEUSES =  os.path.join(nom_dossier, sous_dossier, "CONSO COUTEUSES.xlsx")
        CONSO_COUTEUSES.to_excel(path_CONSO_COUTEUSES)

    if len(benef_sans_date_naiss) != 0:
        path_benef_sans_date_naiss =  os.path.join(nom_dossier, sous_dossier, "BENEF SANS DATE DE NAISSANCE.xlsx")
        benef_sans_date_naiss.to_excel(path_benef_sans_date_naiss)
    return

def start_progress():
    progress_bar['value'] = 0
    critere_benef(selected_beneficiaire_path,pd.to_datetime(str(start_date_entry.get())),pd.to_datetime(str(end_date_entry.get())))
    critere_emission(selected_emission_path,pd.to_datetime(str(end_date_entry.get())))
    critere_conso(selected_consommation_path)
    resume(selected_beneficiaire_path, selected_emission_path, selected_consommation_path,seuil_entry.get(),ante=pd.to_datetime(str(start_date_entry.get())),post=pd.to_datetime(str(end_date_entry.get())))
    update_progress()
    return

def update_progress():
    current_value = progress_bar['value']
    if current_value < 100:
        progress_bar['value'] += 5
        percentage = current_value + 5
        progress_label.config(text=f"{percentage}%")
        window.after(2000, update_progress)
    else:
        progress_label.config(text="Terminé")
    return
###################----------------------------------------------------------------------
# Add a button to start the control process
start_button = ttk.Button(window, text="COMMENCER LE CONTROLE", style="danger.Outline.TButton", command=start_progress)
start_button.grid(row=18, column=1, columnspan=3, pady=10, ipadx=2, sticky="we")

# Create a progress bar
progress_bar = ttk.Progressbar(window, orient="horizontal", length=200, mode="determinate", takefocus=True, maximum=100)
progress_bar.grid(row=19, column=1, columnspan=3, pady=10, padx=10, sticky="we")

# Add a label to display the percentage
progress_label = ttk.Label(window, text="0%")
progress_label.grid(row=20, column=2, columnspan=3, pady=10, padx=10, sticky="we")
# Start the Tkinter main loop
window.mainloop()


