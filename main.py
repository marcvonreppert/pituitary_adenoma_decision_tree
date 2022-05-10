import baum
from tree_gen import *              #import * holt einfach alles - ist wie einfach dahin kopieren!!
from walker import JohnnieWalker
import dataio
from sklearn.metrics import confusion_matrix



# #________________________________________
# pid = 735
#
# # Loop über alle Pat, predictedes Label und eigentliches Label speichern
# # dann confusion matrix
#
# # dataio getting patient parameters
# env = dataio.get_patient_data(pid)
#
# ground_truth = dataio.get_ground_truth()
# all_pids = dataio.get_all_pids()
# decision_results = []
#
# print(env)
# print(ground_truth)
# print(all_pids)
#
# # gen tree
# # exec(open('tree_gen.py').read())
#
# #(((start_node.return_next(env)).return_next(env)).return_next(env))
# # hiermit könnte man händisch durchtesten, alternativ dazu der Walker
#
#
# jw = JohnnieWalker()
# print("reached final node: " + jw.decide(start_node, env).get_name())
#
# jw.print_decision_tree(start_node, prefix="> ")
# #___________________________________________


decision_results = []
ground_truth = dataio.get_ground_truth()
all_pids = dataio.get_all_pids()
print(all_pids)
print(ground_truth)


#all_pids.sort(reverse = True)
#print(all_pids)

for i in all_pids:

    pid = i
    env = dataio.get_patient_data(pid)


    jw = JohnnieWalker()
    print(pid)
    print("reached final node: " + jw.decide(start_node, env).get_name())


    decision_results.append(jw.decide(start_node, env).get_name())


#print(decision_results)
#print(ground_truth)

#results_set = set(decision_results)
#ground_truth_set = set(ground_truth)
#print(results_set)
#print(ground_truth_set)


matrix_results_dictionary = {
    "operative behandlung": 1,
    "medikamentoese behandlung": 2,
    "wait and scan": 3
}

matrix_ground_truth_dict = {
    "operativ kausal": 1,
    "andere kausale OP": 1,
    "andere Behandlung": 1,
    "kausal medikamentös": 2,
    "wait and scan": 3,
    "postoperativ wait and scan": 3
}

renamed_results = []
for i in decision_results:
    renamed = matrix_results_dictionary[i]
    renamed_results.append(renamed)

print(renamed_results)

renamed_ground_truth = []
for i in ground_truth:
    renamed = matrix_ground_truth_dict[i]
    renamed_ground_truth.append(renamed)

print(renamed_ground_truth)

#y_actu = [2, 0, 2, 2, 0, 1, 1, 2, 2, 0, 1, 2]
#y_pred = [0, 0, 2, 1, 0, 2, 1, 0, 2, 0, 2, 2]
print(confusion_matrix(renamed_ground_truth, renamed_results))