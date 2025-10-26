# Ensembles de base
alpha = set('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz')  # lettres
beta = set('0123456789')  # chiffres
theta = set('- ')  # séparateurs (tiret ou espace)
epsilon = {''}  # chaîne vide
delta = set('.,!?;:@#$%^&*()[]{}/<>\\|`~"\'+=-_')  # ponctuation et caractères spéciaux

# Alphabet complet
sigma = alpha | beta | theta | epsilon | delta

# Table de transition
transition = {
    'q0': {
        'alpha': 'q1',  # Lecture de 2 lettres (XY)
        'epsilon': 'q0',  # Ignore chaîne vide
        'delta': 'q0',  # Ignore ponctuation
        'theta': 'q0'  # Ignore séparateurs
    },
    'q1': {
        'theta': 'q2'  # Séparateur après lettres
    },
    'q2': {
        'beta': 'q3'  # Lecture de 4 chiffres (abcd)
    },
    'q3': {
        'theta': 'q4'  # Séparateur après chiffres
    },
    'q4': {
        'alpha': 'q5'  # 1 ou 2 lettres finales (T ou ZT)
    },
    'q5': {
        'epsilon': 'q7',  # Fin format XY-abcd-T
        'delta': 'q7',  # Fin avec ponctuation
        'theta': 'q7'  # Fin avec séparateur
    },
    'q6': {
        'epsilon': 'q7',  # Fin format XY-abcd-ZT
        'delta': 'q7',  # Fin avec ponctuation
        'theta': 'q7'  # Fin avec séparateur
    },
    'q7': {
        'theta': 'rej',
        'epsilon': 'rej',
        'delta': 'rej'

    },  # État d'acceptation final
    'rej': {}  # État de rejet
}

# États finaux (acceptants)
final_states = {'q7'}
etat_inital = {'q0'}

    

def accept(word : str):
    etat = 'q0'
    #read_count = 0
    alpha_count = 0
    beta_count = 0

    # if len(word) > 10 or len(word) < 9:
    #     return False
    
    for char in word:
       # print('etat :', etat, 'char :', char)
        
        if etat == 'q0':
            if char in epsilon or char in delta or char in theta:
                # Reste en q0, ignore ces caractères
                continue
            elif char in alpha:
                alpha_count += 1
                if alpha_count == 2:
                    etat = 'q1'
                    alpha_count = 0
            else:
                return False
                
        elif etat == 'q1':
            if char in theta:
                etat = 'q2'
            else:
                return False
                
        elif etat == 'q2':
            if char in beta:
                beta_count += 1
                if beta_count == 4:
                    etat = 'q3'
                    beta_count = 0
            else:
                return False
                
        elif etat == 'q3':
            if char in theta:
                etat = 'q4'
            else:
                return False
                
        elif etat == 'q4':
            if char in alpha:
                alpha_count += 1
                if alpha_count == 1:
                    etat = 'q5'
                elif alpha_count == 2:
                    etat = 'q6'
                else:
                    return False
            else:
                return False
                
        elif etat == 'q5':
            if char in alpha:
                alpha_count += 1
                if alpha_count == 2:
                    etat = 'q6'
                else:
                    return False
            elif char in epsilon or char in delta or char in theta:
                return True
            else:
                return False
                
        elif etat == 'q6':
            if char in epsilon or char in delta or char in theta or char in alpha:
                return True
                 
            else:
                return False

        # elif etat == 'q7':
        #     if char in alpha :
        #         return True
        #     else:
        #         return True
    
    return etat in ['q5', 'q6', 'q7']
        

def plates_reader(text):

    plates = set()
    for i in range(0, len(text)):
        word1 = text[i:i+9:1]
        word2 = text[i:i+10:1]
        
        # print(repr(word1), " ",accept(word1), ' ' , len(word1))
        # print(repr(word2), " ",accept(word2) , ' ' , len(word2))

        if accept(word1) :
            plates.add(word1)

        if accept(word2) :
            plates.add(word2)

    return plates


def clean_plates(plates :set):
    cleaned_plates = set()
    
    for plate in plates:
        print("\nPlaque originale:", plate)
        
        # Supprimer les caractères non-alphabétiques au début
        while plate and plate[0] not in alpha:
            plate = plate[1:]
        
        # Supprimer les caractères non-alphabétiques à la fin
        while plate and plate[-1] not in alpha:
            plate = plate[:-1]
        
        if plate:
            cleaned_plates.add(plate)
        

    return cleaned_plates


def normalize(plates: set):
    """
    Normalise les plaques en convertissant toutes les lettres en majuscules
    et en remplaçant les espaces par des tirets
    """
    normalized_plates = set()
    
    for plate in plates:
        # Convertir en majuscules et remplacer les espaces par des tirets
        normalized_plate = plate.upper().replace(' ', '-')
        normalized_plates.add(normalized_plate)
        print(f"\nPlaque normalisée: {plate} -> {normalized_plate}")
    
    return normalized_plates


text =  """

as--1234-a as-1243-az
 """


plates = plates_reader(text)
print("\nPlaques Detecter:",plates)

# Nettoyer les plaques
cleaned_plates = clean_plates(plates)
print("\nPlaques nettoyées:", cleaned_plates)

# Normaliser les plaques (majuscules)
normalized_plates = normalize(cleaned_plates)
print("\n \nPlaques normalisées:", normalized_plates)
 

        