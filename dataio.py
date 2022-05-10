# zuerst lade ich das dataframe aus dem parquet file
# dann erstelle ich aus dem df mit iterrow ein dictionary (env) mit allen relevanten Werten

import pandas as pd
import numpy as np

df_aggregated = pd.read_excel(r"C:\Users\marcv\Desktop\ICCAS\aggregated_dataframe.xlsx")

columns_string = [
    "patient_comment", "therapy_therapy_plan", "clinic_abnormalities", "imaging_local", "op_adenom_classification"
]
for col in columns_string:
    df_aggregated[col][df_aggregated[col].isnull()] = ''
        #alle leeren Felder in diesen Spalten werden jetzt mit einem leeren String versehen

all_pids = []
ground_truth = []
env = {}

def find_index(patient_id):
    #print(df_aggregated.index)
    return (df_aggregated.index[df_aggregated['pid'] == patient_id])[0] #holt alle indizes die die bedingung erfüllen, und davon das erste



def get_patient_data(pid):

    index = find_index(pid)


    #for index, row in df_aggregated.iterrows():
    #  print(f'Index: {index}, row: {row.values}')

    env = {
        "op_had_hormonactive": df_aggregated.loc[index,'op_had_hormonactive'],
        "patient_comment": df_aggregated.loc[index,'patient_comment'],
        "therapy_therapy_plan": df_aggregated.loc[index, 'therapy_therapy_plan'],
        "clinic_abnormalities": df_aggregated.loc[index, 'clinic_abnormalities'],
        "imaging_size_kk": df_aggregated.loc[index, 'imaging_size_kk'],
        "imaging_size_ll": df_aggregated.loc[index, 'imaging_size_ll'],
        "imaging_size_ap": df_aggregated.loc[index, 'imaging_size_ap'],
        "imaging_micro_or_macro": df_aggregated.loc[index, 'imaging_micro_or_macro'],
        "imaging_local": df_aggregated.loc[index, 'imaging_local'],
        "labor_prolactine_mug_l": df_aggregated.loc[index, 'labor_prolactine_mug_l'],
        "op_adenom_classification": df_aggregated.loc[index, 'op_adenom_classification'],
        "ophthalmology_has_chiasma_syndrome": df_aggregated.loc[index, 'opthalmology_has_chiasma_syndrome'] #Achtung Schreibfehler!
    }
    return env

def get_ground_truth():

    ground_truth = df_aggregated['therapy_therapy_plan'].tolist()
    return ground_truth

def get_all_pids():

    all_pids = df_aggregated['pid'].tolist()
    return all_pids
