import random
import copy

antwort_moeglich = [
        "Mithilfe eines 2D-Lasers",
        "Mit einer Biegemaschine",
        "Mittels einer Stanzmaschine",
        "Mit dem 3D-Drucker",
        "Mit einer Drehmaschine",
        "Wurde geschweißt",
        "Wurde gegossen",
        "Mit einer Fräsmaschine"
        ]

tmp = copy.deepcopy(antwort_moeglich)
final = []
antwort_moeglich_index = [3, 2, 1, 0]
antwort_index =  [2,1,3,0]
correct_ans = 0

for i in range(len(tmp)):
    if i == antwort_moeglich_index[0]:
        correct_ans = tmp[i]
        del tmp[i]
        break

for i in range(3):
    element = random.choice(tmp)
    final.append(element)
    tmp.remove(element)

final.insert(antwort_index[0],correct_ans)

