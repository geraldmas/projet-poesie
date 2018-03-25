class Mot:
	def __init__(self, orthographe):
        self.orthographe = mot
        self.apparitions = 1
        self.suiviPar = []

    def estSuiviPar(self, autremot):
    	if autremot.lower() in self.suiviPar.keys():
    		self.suiviPar[autremot.lower()] += 1
    	else:
    		self.suiviPar[autremot.lower()] = 1
    	autremot.apparitions += 1

file = open("test.txt", "r")
to_add = []
for line in file.readlines():
	to_add += [x.lower() for x in line.split()]

liste_mots = []

for i, mot in enumerate(to_add):
	if mot in [x.orthographe for x in liste_mots]:
		if i < len(to_add):
			mot.estSuiviPar(to_add[i+1])
		else: 
			mot.apparitions += 1
	else:
		liste_mots.append(Mot(mot))

file.close()