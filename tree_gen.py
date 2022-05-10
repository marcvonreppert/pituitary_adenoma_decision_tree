import baum
import dataio
import numpy as np

# all nodes                             #hier kreiere ich alle nodes
start_node = baum.forkNode()
start_node.set_name("startpunkt")

hyperfunctioning_node = baum.forkNode()
hyperfunctioning_node.set_name("hyperfunctioning")
prolaktinom_node = baum.forkNode()
prolaktinom_node.set_name("prolaktinom")
other_node = baum.forkNode()
other_node.set_name("andere")

nonfunctioning_node = baum.forkNode()
nonfunctioning_node.set_name("nonfunctioning")
micro_node = baum.forkNode()
micro_node.set_name("mikroadenom")
macro_node = baum.forkNode()
macro_node.set_name("makroadenom")
mass_symptoms_node = baum.forkNode()
mass_symptoms_node.set_name("massesymptome")

medication_node = baum.therapyNode()
medication_node.set_name("medikamentoese behandlung")
op_node = baum.therapyNode()
op_node.set_name("operative behandlung")
wns_node = baum.therapyNode()
wns_node.set_name("wait and scan")

# link nodes                            #hier weise ich den Nodes ihre Verbindung untereinander zu
start_node.add_children([hyperfunctioning_node, nonfunctioning_node])

hyperfunctioning_node.add_parent([start_node])
hyperfunctioning_node.add_children([prolaktinom_node, other_node])
prolaktinom_node.add_parent([hyperfunctioning_node])
other_node.add_parent([hyperfunctioning_node])
prolaktinom_node.add_children([medication_node])
other_node.add_children([op_node])

nonfunctioning_node.add_parent([start_node])
nonfunctioning_node.add_children([micro_node, macro_node])  #hierauf bezieht sich die 0 oder 1 aus der d2c-map
micro_node.add_parent([nonfunctioning_node])
macro_node.add_parent([nonfunctioning_node])
micro_node.add_children([mass_symptoms_node, wns_node])
macro_node.add_children([mass_symptoms_node, wns_node])
mass_symptoms_node.add_parent([micro_node, macro_node])
mass_symptoms_node.add_children([op_node])

# hier werden die Einteilungsregeln eingebaut
# add decision functionality

def hormonaktivitaet(env):

    hyperfunctioning = "hyperfunctioning adenoma"
    nonfunctioning = "nonfunctioning adenoma"
    ishyperfunctioning = False
    isnonfunctioning = False

    if env['op_had_hormonactive'] == 0 or \
            'hormoninaktiv' in env['patient_comment']:
        isnonfunctioning = True

    if env['op_had_hormonactive'] == 1 or \
            'produzierend' in env['patient_comment'] or \
            'hormonaktiv' in env['patient_comment'] or \
            'Akrenwachstum' in env['clinic_abnormalities'] or \
            'Stammfettsucht' in env['clinic_abnormalities'] or \
            'Striae rubra' in env['clinic_abnormalities']:
        ishyperfunctioning = True

    else:
        print("Es konnte keine eindeutige Entscheidung getroffen werden. Annahme: Hormoninaktiv.")
        isnonfunctioning = True

    if ishyperfunctioning:
        print("classified as hyperfunctioning adenoma")
        return hyperfunctioning
    if isnonfunctioning:
        print("classified as nonfunctioning adenoma")
        return nonfunctioning

start_node.add_decisionfunc(hormonaktivitaet)
start_node.add_d_2_c_map({'hyperfunctioning adenoma': 0, 'nonfunctioning adenoma': 1})


def micro_macro(env):
    if env['imaging_size_kk'] >= 10 or env['imaging_size_ll'] >= 10 or env['imaging_size_ap'] >= 10 \
            or env['imaging_micro_or_macro'] == 1 \
            or 'Makroadenom' in env['patient_comment']:

        return 'makro'

    elif env['imaging_size_kk'] < 10 and env['imaging_size_ll'] < 10 and env['imaging_size_ap'] < 10 or \
            env['imaging_micro_or_macro'] == 2 or \
            'Mikroadenom' in env['patient_comment']:

        return 'mikro'

    else:
        print("Es fehlen Größenangaben. Annahme: Makroadenom.")
        return 'makro'


nonfunctioning_node.add_decisionfunc(micro_macro)
nonfunctioning_node.add_d_2_c_map({'mikro': 0, 'makro': 1})


def hormon_type(env):
    prolaktinoma = "prolactinoma"
    isProlaktinoma = False
    if ('Prolaktinom' in env['patient_comment']) or ('prolaktin' in env['patient_comment']):
        print("found prolaktin in patient comment")
        isProlaktinoma = True
    if env['op_adenom_classification'] == "Adenom ja - Prolaktinom":
        print("op adenom is classified as prolactinom")
        isProlaktinoma = True
    if env['labor_prolactine_mug_l'] >= 94:
        print("prolaktin über laborgrenzwert")
        isProlaktinoma = True



    if isProlaktinoma:
        print("classified as prolactinoma")
        return prolaktinoma
    else:
        print("classified as other hormone-producing adenoma")
        return "other hyperfunctioning adenoma"


hyperfunctioning_node.add_decisionfunc(hormon_type)
hyperfunctioning_node.add_d_2_c_map({'prolactinoma': 0, 'other hyperfunctioning adenoma': 1})


def mass_symptoms(env):

    mass_effects = "symptomatic mass effects"
    no_symptoms = "not symptomatic"

    has_mass_effects = False
    has_no_symptoms = False

    if (
            'Oligo/Amenorrhoe/Libidoverlust' in env['clinic_abnormalities'] or \
            'Galaktorrhoe' in env['clinic_abnormalities'] or \
            'Augenmuskelparesen' in env['clinic_abnormalities'] or \
            'Diabetes insipidus' in env['clinic_abnormalities'] or \
            'Neuropathie' in env['clinic_abnormalities'] or \
            'Osteoporose' in env['clinic_abnormalities'] or \
            'Potenzverlust' in env['clinic_abnormalities'] or \
            'Rhinoliquorrhoe' in env['clinic_abnormalities'] or \
            'Sehstörungen' in env['clinic_abnormalities'] or \

            'Verschiebung Chiasma optikum' in env['imaging_local'] or\
            'Ummantelung ACI' in env['imaging_local'] or\
            'suprasellär' in env['imaging_local'] or\
            'parasellär' in env['imaging_local'] or\
            'Infiltration S. cavernosus' in env['imaging_local'] or\

             env['ophthalmology_has_chiasma_syndrome'] == 1):

        has_mass_effects = True
        print("Patient has mass symptoms caused by adenoma")
        return mass_effects

    else:
        has_no_symptoms = True
        print("Patient doesn't have mass symptoms caused by adenoma")
        return no_symptoms

macro_node.add_decisionfunc(mass_symptoms)
macro_node.add_d_2_c_map({'symptomatic mass effects': 0, 'not symptomatic': 1})

micro_node.add_decisionfunc(mass_symptoms)
micro_node.add_d_2_c_map({'symptomatic mass effects': 0, 'not symptomatic': 1})

#sowohl Mikroadenome als auch Makroadenome werden nach Massesymptomen gecheckt


def therapy_prolaktinom(env):
    return "medication"


prolaktinom_node.add_decisionfunc(therapy_prolaktinom)
prolaktinom_node.add_d_2_c_map({'medication': 0})


def therapy_other_hyperfunctioning_adenoma(env):
    return "op"


other_node.add_decisionfunc(therapy_other_hyperfunctioning_adenoma)
other_node.add_d_2_c_map({'op': 0})


#def therapy_micro_adenoma(env):
#    return "wns"
#micro_node.add_decisionfunc(therapy_micro_adenoma)
#micro_node.add_d_2_c_map({'wns': 0})


def therapy_mass_symptoms(env):
    return "op"


mass_symptoms_node.add_decisionfunc(therapy_mass_symptoms)
mass_symptoms_node.add_d_2_c_map({'op': 0})
