from random import random
import glob

nb_couplet = 9
taille_refrain = 8
taille_couplet = 4
nb_couplet_avant_ref = 3
nb_phrase_total = nb_couplet*taille_couplet

# Lecture des fichiers

to_add = []

for infile in glob.glob('input/*.txt'):
	file = open(infile, "r")
	for line in file.readlines():
		to_add += [x.lower() for x in line.replace('.', ' .').replace(',', ' ,').replace('"', ' " ').split()]
	file.close()

# Création des listes de mots

dict_mots = {}

for i, mot in enumerate(to_add):
	if mot in dict_mots.keys():
		dict_mots[mot][0] += 1
	else:
		dict_mots[mot] = [1, {}, 0]
	if i+1 < len(to_add):
		if to_add[i+1] in dict_mots[mot][1].keys():
			dict_mots[mot][1][to_add[i+1]][0] += 1
		else:
			dict_mots[mot][1][to_add[i+1]] = [1, 0]

# Passage aux probas

total_mot = 0
for mot in dict_mots.keys():
	total_mot += dict_mots[mot][0]
	tot_mot_loc = 0
	for mot_suivant in dict_mots[mot][1].keys():
		tot_mot_loc += dict_mots[mot][1][mot_suivant][0]
	for mot_suivant in dict_mots[mot][1].keys():
		dict_mots[mot][1][mot_suivant][0] /= tot_mot_loc
for mot in dict_mots.keys():
	dict_mots[mot][0] /= total_mot

prob_cumm = 0
for mot in dict_mots.keys():
	prob_cumm += dict_mots[mot][0]
	dict_mots[mot][2] = prob_cumm
	prob_cumm_loc = 0
	for mot_suivant in dict_mots[mot][1].keys():
		prob_cumm_loc += dict_mots[mot][1][mot_suivant][0]
		dict_mots[mot][1][mot_suivant][1] = prob_cumm_loc

# Tirage au sort et écriture

output = open("output.txt", "w")

sorted_dict = sorted(dict_mots.items(), key = lambda t: t[1][2])

refrain = ""

cumm_courant = 0
i = 0
j = 0
while random() > sorted_dict[min(i+1, len(sorted_dict)-1)][1][2] and i+1 < len(sorted_dict):
	cumm_courant = sorted_dict[i][1][2]
	i+=1

mot_courant = sorted_dict[max(i-1, 0)][0]
while taille_refrain > 0:
	refrain += mot_courant + " "
	if mot_courant == ".":
		refrain = refrain[:-2]+"\n"
		taille_refrain -= 1
	sorted_dict = sorted(dict_mots[mot_courant][1].items(), key = lambda t: t[1][1])
	cumm_courant = 0
	i = 0
	while random() > sorted_dict[min(i+1, len(sorted_dict)-1)][1][1] and i+1 < len(sorted_dict):
		cumm_courant = sorted_dict[i][1][1]
		i+=1
	mot_courant = sorted_dict[max(i-1, 0)][0]


sorted_dict = sorted(dict_mots.items(), key = lambda t: t[1][2])
texte_genere = ""

cumm_courant = 0
i = 0
j = 0
k = 0
while random() > sorted_dict[min(i+1, len(sorted_dict)-1)][1][2] and i+1 < len(sorted_dict):
	cumm_courant = sorted_dict[i][1][2]
	i+=1

mot_courant = sorted_dict[max(i-1, 0)][0]
while nb_phrase_total > 0:
	texte_genere += mot_courant + " "
	if mot_courant == ".":
		texte_genere = texte_genere[:-2]+"\n"
		if j%taille_couplet == taille_couplet-1:
			if k%nb_couplet_avant_ref == nb_couplet_avant_ref-1:
				texte_genere += "\n"+refrain+"\n"
			else:
				texte_genere += "\n\n"
			k+=1
		j+=1
		nb_phrase_total -= 1
	sorted_dict = sorted(dict_mots[mot_courant][1].items(), key = lambda t: t[1][1])
	cumm_courant = 0
	i = 0
	while random() > sorted_dict[min(i+1, len(sorted_dict)-1)][1][1] and i+1 < len(sorted_dict):
		cumm_courant = sorted_dict[i][1][1]
		i+=1
	mot_courant = sorted_dict[max(i-1, 0)][0]
texte_genere += "\n"+refrain+"\n"
output.write(texte_genere)
output.close()