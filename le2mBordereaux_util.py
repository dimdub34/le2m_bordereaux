

def get_prenom(prenom):
    def get_maj(p):
        return [i[0].upper() + i[1:].lower() for i in p]
    pcomp = prenom.split("-")
    plusp = prenom.split()
    if len(pcomp) > 1:
        return "-".join(get_maj(pcomp))
    elif len(plusp) > 1:
        return " ".join(get_maj(plusp))
    else:
        return prenom[0].upper() + prenom[1:].lower()
