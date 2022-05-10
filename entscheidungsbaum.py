
#meine Notizen für die Funktionen siehe Zeile 3
#clinically_nonfunctioning():
    #had_hormonactive (in OP) = 0 OR
    #had_hormonactive (in hist) = 0 OR      
    #'hormoninaktiv' in comment
    #Frage an Dr. Lindner: welche Grenzwerte im Labor gelten zur Unterscheidung hormonaktiv / hormoninaktiv?
    #Prolaktin: Frau vor Menopause: ca. 400mU/L
    #           Frau nach Menopause und Mann: ca. 600mU/L
    #Cortisol: max. ca 620nmol/L
    #TSH: zwischen 0,40 und 4,0 mU/l
    #freies T4: zwischen 7 und 14,8 ng/l
    #IGF-1: 70-290ng/ml
    #GH: 0-8 ng/ml
    #Testosteron: Männer: 3,5–11,5 ng/ml (12–40 nmol/l)
    #             Frauen: 0,15–0,6 ng/ml (0,5–2,0 nmol/l)
    #LH: Männer: 1,7 - 8,6 U/l
    #    Frauen: zyklisch schwankend
    #FSH: Männer: 2 bis 10 IU/ml
    #     Frauen: zyklisch schwankend
    
        #MAKROADENOM:
        #imaging_size_kk  >= 10 OR
        #imaging_size_ll  >= 10 OR
        #imaging_size_ap  >= 10 OR
        # imaging_micro_or_macro  = 1 OR
        #'Makroadenom' in comment
        
                #KLINISCHE AUFFÄLLIGKEITEN: 
                #'Oligo/Amenorrhoe/Libidoverlust', 'Galaktorrhoe',
                #'Augenmuskelparesen', 'Diabetes insipidus', 'Neuropathie', 'Osteoporose',
                #'Potenzverlust', 'Rhinoliquorrhoe', 'Sehstörungen' in clinic_abnormalities    OR
                
                #BILDGEBENDE AUFFÄLLIGKEITEN:
                #'Verschiebung Chiasma optikum', 'Ummantelung ACI', 'suprasellär', 
                #'parasellär', 'Infiltration S. cavernosus' in imaging_local                    OR
    
                #OPHTHALMOLOGIE:
                #has_chiasmasyndrom == 1
                
                    #--> OP
                
                #KLINISCH UNAUFFÄLLIG:
                
                    #--> wait and scan
        
        #MIKROADENOM:
        # imaging_micro_or_macro  = 2
        #imaging_size_kk  <= 10 OR
        #imaging_size_ll  <= 10 OR
        #imaging_size_ap  <= 10 OR
        #'Mikroadenom' in comment
        
            #--> wait and scan
        


#clinically_functioning():
    #had_hormonactive (in OP) = 1 OR
    #had_hormonacive (in hist) = 1 OR
    #'produzierend' in comment
    #'Akrenwachstum','Stammfettsucht', 'Striae rubra' in clinic_abnormalities 
    
        #PROLAKTINOM
        #'Prolaktinom','prolaktin',  in comment
        #adenom_classification == "Adenom ja - Prolaktinom"
        #labor_prolactine_mug_l >= 94 (alternativ 35, 50, ...?)
        
            #--> kausal medikamentös
        
        #ANDERER HORMONPRODUZIERENDER TUMOR
        #Else:
            
            #--> OP  m


def hormonaktivität(op_had_hormonactive, patient_comment, clinic_abnormalities):
    
    if( 
        op_had_hormonactive==0 or
        'hormoninaktiv' in patient_comment):
        
            return "nonfunctioning adenoma"
    
    elif( 
        op_had_hormonactive==1 or
        'produzierend' in patient_comment or
        'Akrenwachstum','Stammfettsucht', 'Striae rubra' in clinic_abnormalities):
        
            return 'functioning adenoma'
    
    else:
        return 'keine Vorhersage möglich'
       
       
def mikro_makro(imaging_size_kk, imaging_size_ll, imaging_size_ap, imaging_micro_or_macro, patient_comment):
    
    if( 
        imaging_size_kk  >= 10 or
        imaging_size_ll  >= 10 or
        imaging_size_ap  >= 10 or
        imaging_micro_or_macro == 1 or
        'Makroadenom' in patient_comment):
        
           return "macroadenoma"
    
    elif (imaging_size_kk  <= 10 and
        imaging_size_ll  <= 10 and
        imaging_size_ap  <= 10 or
        'Mikroadenom' in patient_comment or
        imaging_micro_or_macro == 2):
        
           return "microadenoma"
       
    else:
        return 'keine Vorhersage möglich'
    
    
def hormon_type(labor_prolactine_mug_l, adenom_classification, patient_comment):

    if(
        'Prolaktinom' or 'prolaktin' in patient_comment or
        adenom_classification == "Adenom ja - Prolaktinom" or
        labor_prolactine_mug_l >= 94):
        
           return "prolactinoma"
       
    else:      
           return "other hyperfunctioning adenoma"
       
       
def mass_symptoms(clinic_abnormalities, imaging_local, ophthalmology_has_chiasma_syndrome):

    if(
        'Oligo/Amenorrhoe/Libidoverlust' or 'Galaktorrhoe' or
        'Augenmuskelparesen' or 'Diabetes insipidus' or 'Neuropathie' or 'Osteoporose' or
        'Potenzverlust' or 'Rhinoliquorrhoe' or 'Sehstörungen' in clinic_abnormalities or
        
        'Verschiebung Chiasma optikum' or 'Ummantelung ACI' or 'suprasellär' or 
        'parasellär' or 'Infiltration S. cavernosus' in imaging_local or

        ophthalmology_has_chiasma_syndrome == 1):
        
           return "symptomatic mass effects"
       
    else:      
           return "not symptomatic"

# =============================================================================
# # Vorschlag von Daniel        
# # diese Funktion spiegelt den eigentlichen Entscheidungsbaum wider.
# 
# def apply_guideline(patient_data: pd.Series):
#     hormonactive = hormonaktivität(
#         op_had_hormonactive=patient_data[''], 
#         had_hormonactive_hist=..., 
#         patient_comment=..., 
#         clinic_abnormalities=...
#     )
#     if hormonactive == '':
#         micro_macro = mikro_makro(
#             imaging_size_kk=..., 
#             imaging_size_ll=..., 
#             imaging_size_ap=...,
#             imaging_micro_or_macro=..., 
#             patient_comment=...
#         )
#     else:
#         ...
#         
#     return therapy
# =============================================================================

def main():                     # das ist die Hauptfunktion, die nur auf alles andere zurückgreift
    
    # load dataframe
    # aggregate data
    for patient in data.iterrows():
        therapy = apply_guideline(patient)
        print(patient.name, therapy)
    
    
if __name__ == '__main__':      # per Definition wird so bei Start des Programms zuerst dieser Teil ausgeführt
    main()



        

        
