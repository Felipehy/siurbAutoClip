
def text_size_is_bigger(text, max) -> bool:
    if len(text) > max:
        return True
    if len(text) < max:
        return False

def hasPriceInObject(text) -> bool:
        
        if ("R$" in text):  return True

        return False

def hasContractTerm(text) -> bool:
    
    if ("TERMO DE CONTRATO" in text): return True
    if ("TERMO DE ADITAMENTO" in text): return True

    return False

def hasProcessSEI(text) -> bool:
    
    if ("PROCESSO Nº" in text) : return True
    if ("PROCESSO SEI" in text) : return True
    if ("PROCESSO DO CONTRATO" in text): return True
    if ("PROCESSO ADMINISTRATIVO" in text): return True
    if ("Processo nº" in text): return True
    if ("PROCESSO" in text): return True
    if ("PROCESSO ADMINISTRATIVO Nº" in text): return True

    return False

def hasAllocation(text) -> bool:

    if ("DOTAÇÃO A SER ONERADA" in text): return True
    if ("DOTAÇÃO SER ONERADA" in text): return True

    return False

def hasContractor(text) -> bool:
    
    if ("CONTRATANTE" in text): return True
    if ("COTRATANTE" in text): return True
    
    return False

def hasCommitment(text) -> bool:

    if ("NOTA DE EMPENHO" in text): return True
    if ("NOTA EMPENHO" in text): return True
    if ("NOTAS DE EMPENHO" in text): return True   
    if ("NOTAS EMPENHO" in text): return True   
    if ("Nota(s) de empenho" in text): return True

    return False

def hasObjectAditamento(text):

    if ("OBJETO DO ADITAMENTO" in text): return True

    return False
