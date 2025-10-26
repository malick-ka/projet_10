# plates.py
# -----------------------------
# Ce module contient les fonctions permettant
# d'extraire automatiquement les plaques d'immatriculation
# à partir d'un texte quelconque.
# -----------------------------

def pattern_recognition(string, seps=[' ', '-'], default_sep='-'):
    """
    Cette fonction essaie de repérer des motifs qui ressemblent
    à des plaques d'immatriculation dans une chaîne de caractères.
    Exemple : 'DK-3456-A' ou 'TH-1234-BC'
    """

    # On commence par normaliser la chaîne :
    # on enlève les séparateurs superflus et on remplace tout par '-'
    for sep in seps:
        string = string.strip(sep)
        string = string.replace(sep, default_sep)

    # Petite condition de base : on ne traite que si la chaîne est assez longue
    # et qu’il y a au moins deux tirets (souvent nécessaires dans une plaque)
    condition = (len(string) >= 9 and string.count(default_sep) >= 2)

    if not condition:
        # Rien de plausible ici, on sort tout de suite
        return set()

    # On met tout en majuscules, comme les plaques
    string = string.upper()

    patterns = []

    # Tant qu’il y a assez d’informations, on continue à chercher
    while condition:
        pattern = ''
        for i in range(len(string)):
            if string[i] == default_sep:
                try:
                    # Ici, on vérifie si la structure autour du tiret
                    # correspond à une plaque classique : 2 lettres, 4 chiffres, etc.
                    if (string[i-2:i].isalpha() and string[i+1:i+5].isdigit() and default_sep == string[i+5]):
                        has_embedded_patterns = False
                        try:
                            # Cas d’une plaque avec deux lettres à la fin, ex : DK-1234-BC
                            if string[i+6:i+8].isalpha():
                                pattern1 = string[i-2:i+8]
                            else:
                                raise Exception
                               
                            # Cas où il n’y a qu’une seule lettre après, ex : DK-1234-A
                            if string[i+6:i+7].isalpha():
                                pattern2 = string[i-2:i+7]
                                has_embedded_patterns = True
                           
                            # On gère les deux situations possibles
                            if has_embedded_patterns:
                                string = string[i-2:]
                                string = string.replace(pattern1, '')

                                # On garde les deux variantes possibles
                                patterns.extend([pattern1, pattern2])
                                pattern = pattern1
                                break
                        except Exception:
                            # Si on a qu’une seule lettre finale (comme DK-3456-A)
                            if string[i+6:i+7].isalpha():
                                pattern = string[i-2:i+7]
                                string = string[i-2:]
                                string = string.replace(pattern, '')
                                patterns.append(pattern)
                            else:
                                # Sinon on avance juste dans la chaîne
                                string = string[i+1:]
                            break
                except IndexError:
                    # Si on dépasse la longueur de la chaîne, on arrête cette boucle
                    string = string[i+1:]
                    break

        # Si aucun motif n’a été trouvé ici, on avance dans le texte
        if not pattern:
            string = string[i+1:]

        # On nettoie les tirets en trop
        string = string.strip(default_sep)

        # On vérifie s’il reste encore assez de matière pour continuer
        condition = (len(string) >= 9 and string.count(default_sep) >= 2)

    # On retourne les motifs trouvés, sans doublons
    return set(patterns)


def extract_plates_from_text(text):
    """
    Cette fonction est celle appelée directement par l’interface Tkinter.
    Elle prend un texte complet, le découpe, et cherche des plaques
    grâce à la fonction pattern_recognition().
    """

    # On découpe le texte en "mots" ou tokens simples
    tokens = text.replace('\n', ' ').replace(',', ' ').split()

    detected = set()

    # Pour chaque token, on regarde s’il contient un motif de plaque
    for token in tokens:
        detected.update(pattern_recognition(token))

    # On trie et nettoie la liste avant de la renvoyer
    result = sorted(list(detected))

    # Retourne une simple liste de plaques détectées
    return result
