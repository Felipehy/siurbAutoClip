from utils.format.afastamento_format import AfastamentoFormat
from utils.format.concessao_format import ConcessaoFormat
from utils.format.exoneracao_format import ExoneracaoFormat
from utils.format.ferias_format import FeriasFormat
from utils.format.nomeacao_format import NomeacaoFormat
from utils.format.remocao_format import RemocaoFormat
from utils.format.substituicao_format import SubstituicaoFormat
from utils.extract_extern_factory import ExtractExternFactory
from utils.extract_extern.format.img_format import ImgFormat
from utils.validate import *
import json

def extractExoAndNome(cleanTextP,cleanTextSpan,textAllP):

    f = NomeacaoFormat()

    dict = {}
    list = []

    organ = cleanTextP[1].strip()
    unit = cleanTextP[2].strip()

    if not " da Secretaria Municipal de Infraestrutura Urbana e Obras" in cleanTextP: return None
    
    dict["orgao"] = organ
    dict["unidade_responsavel"] = unit

    dict["conteudo"] = f.format_allText(textAllP,unit)

    for i in range(0,len(cleanTextSpan),1):
        
        #Id do documento
        if "Documento:" in cleanTextSpan[i]:
            doc = cleanTextSpan[i].replace(" Documento:", "").strip()
            dict["id_doc"] = doc

        #Data da publicacao
        if "Publicação:" in cleanTextSpan[i]: 
            publication = cleanTextSpan[i].replace(" Publicação:", "").strip()
            dict["publicacao"] = publication

    for i in range(0,len(cleanTextP),1):

        #Data do documento(nao e a data da publicacao)
        if "Processo" in cleanTextP[i]:
            date = f.format_dateExtand(cleanTextP[i-1])
            dict["data"] = date

        #Processo
        if "Processo" in cleanTextP[i]:
            process = f.format_process(cleanTextP[i])
            dict["processo"] = process

        #Name da pessoa
        if "RF" in cleanTextP[i] or "RG" in cleanTextP[i]: 
            format_name = f.format_name(cleanTextP[i-1])
            if format_name.isupper():
                name = format_name
                dict["name"] = name
            
        if "RF" in cleanTextP[i] or "RG" in cleanTextP[i]:

            #Data que a pessoa saiu ou entrou    
            if "/" in cleanTextP[i+1]:
                _date = f.format_date(cleanTextP[i+1])
                dict["data"] = _date

        #Cargo da pessoa
        if "cargo" in cleanTextP[i]:
            position = f.format_position(cleanTextP[i])
            dict["cargo"] = position
    
        #Departamento
        if "Departamento" in cleanTextP[i] or "Gabinete" in cleanTextP[i]:
            depart = f.format_department(cleanTextP[i])
            dict["departamento"] = depart

            list.append(json.dumps(dict, ensure_ascii=False))

    return list

def extractSubstituicao(cleanTextP,cleanTextSpan,textAllP):

    f = SubstituicaoFormat()

    dict = {}
    list = []

    if not " SUBSTITUIÇÃO" in cleanTextP: return None

    organ = cleanTextP[1].strip()
    unit = cleanTextP[2].strip()

    dict["orgao"] = organ
    dict["unidade_responsavel"] = unit

    dict["conteudo"] = f.format_allText(textAllP,unit)

    for i in range(0,len(cleanTextSpan),1):
        
        #Id do documento
        if "Documento:" in cleanTextSpan[i]:
            doc = cleanTextSpan[i].replace(" Documento:", "").strip()
            dict["id_doc"] = doc

        #Data da publicacao
        if "Publicação:" in cleanTextSpan[i]: 
            publication = cleanTextSpan[i].replace(" Publicação:", "").strip()
            dict["publicacao"] = publication

    oneTime = False

    for i in range(0,len(cleanTextP),1):
        
        #Nome e o cargo antigo
        if "RF" in cleanTextP[i] and oneTime == False:
            name = f.format_name(cleanTextP[i+1])
            position = cleanTextP[i+2].replace("\xa0"," ").strip()
            dict["name"] = name
            dict["cargo"] = position
            oneTime = True

        #Cargo apoós a substituicao
        if "cargo" in cleanTextP[i]:
            newPosition = f.format_position(cleanTextP[i])
            dict["novo_cargo"] = newPosition

        #Departamento
        if "Departame" in cleanTextP[i] or "Gabinete" in cleanTextP[i] or "Assessoria" in cleanTextP[i]:
            depart = f.format_department(cleanTextP[i])
            dict["departamento"] = depart

        #Nome da pessoa que foi substituida e o cargo dela
        if "substituição" in cleanTextP[i]:
            sub = f.format_name(cleanTextP[i])
            positionSub = cleanTextP[i+2].replace("\xa0","").strip()
            dict["substituicao"] = sub
            dict["cargo_sub"] = positionSub
        
        #Periodo de ferias
        if "período" in cleanTextP[i]:
            period = f.format_date(cleanTextP[i])
            dict["ferias_inicio"] = period[0].strip()
            dict["ferias_fim"] = period[1].strip()

            list.append(json.dumps(dict, ensure_ascii=False))
    
    return list

def extractFeriasDeferidas(cleanTextP,cleanTextSpan,textAllP):

    f = FeriasFormat()

    dict = {}
    list = []

    if not " FÉRIAS DEFERIDAS" in cleanTextP: return None

    organ = cleanTextP[1].strip()
    unit = cleanTextP[2].strip()

    dict["orgao"] = organ
    dict["unidade_responsavel"] = unit

    dict["conteudo"] = f.format_allText(textAllP,unit)

    for i in range(0,len(cleanTextSpan),1):
        
        #Id do documento
        if "Documento:" in cleanTextSpan[i]:
            doc = cleanTextSpan[i].replace(" Documento:", "").strip()
            dict["id_doc"] = doc

        #Data da publicacao
        if "Publicação:" in cleanTextSpan[i]: 
            publication = cleanTextSpan[i].replace(" Publicação:", "").strip()
            dict["publicacao"] = publication

    for i in range(0,len(cleanTextP),1):

        if "RF" in cleanTextP[i]:
            name = f.format_name(cleanTextP[i])
            position = cleanTextP[i+1].replace("\xa0", " ").strip()     
            ex = f.format_workout(cleanTextP[i+2])
            days = f.format_days(cleanTextP[i+3])
            date = f.format_date(cleanTextP[i+4])

            dict["name"] = name
            dict["cargo"] = position
            dict["exercicio"] = ex
            dict["qtt_dias"] = days
            dict["data"] = date

            list.append(json.dumps(dict, ensure_ascii=False))
    
    return list

def extractConcessao(cleanTextP,cleanTextSpan,textAllP):
    
    f = ConcessaoFormat()

    dict = {}
    list = []

    listTagInterest = [" INTERESSADO:"," Interessados:", " Interessada:", " INTERESSADA:", " INTERESSADAS:", " Interessadas:"]

    for i in range(0,len(cleanTextP),1):
        if "Concessão de Aposentadoria" in cleanTextP[i]: break
        if i == len(cleanTextP): return None

    organ = cleanTextP[1].strip()
    unit = cleanTextP[2].strip()

    dict["orgao"] = organ
    dict["unidade_responsavel"] = unit

    dict["conteudo"] = f.format_allText(textAllP,unit)

    for i in range(0,len(cleanTextSpan),1):
        
        #Id do documento
        if "Documento:" in cleanTextSpan[i]:
            doc = cleanTextSpan[i].replace(" Documento:", "").strip()
            dict["id_doc"] = doc

        #Data da publicacao
        if "Publicação:" in cleanTextSpan[i]: 
            publication = cleanTextSpan[i].replace(" Publicação:", "").strip()
            dict["data_doc"] = publication

        if " Registro Funcional:" in cleanTextSpan[i]:
            reg_func = f.format_regFunc(cleanTextSpan[i])
            dict["reg_func"] = reg_func

    for i in range(0,len(cleanTextP),1):

        if "Concessão de Aposentadoria" in cleanTextP[i]:
            num_proc = f.format_numProc(cleanTextP[i])
            dict["num_proc"] = num_proc

        if " Registro Funcional:" in cleanTextP[i]:
            reg_func = f.format_regFunc(cleanTextP[i])
            dict["reg_func"] = reg_func

        for tag in listTagInterest:
            if tag in cleanTextP[i]:
                name = f.format_name(cleanTextP[i])
                dict["name"] = name
                break

        if " Cargo:" in cleanTextP[i]:
            cargo = f.format_position(cleanTextP[i])
            dict["cargo"] = cargo

        if " Símbolo:" in cleanTextP[i]:
            simbolo = f.format_symbol(cleanTextP[i])
            dict["simbolo"] = simbolo
        
    list.append(json.dumps(dict, ensure_ascii=False))

    return list

def extractAfastamento(cleanTextP,cleanTextSpan,textAllP):
    
    f = AfastamentoFormat()

    dict = {}
    list = []

    listServer = ["servidor", "servidora", "SERVIDOR", "SERVIDORA"]
    listMonth = [
        "/01/", "janeiro",
        "/02/", "fevereiro",
        "/03/", "março",
        "/04/", "abril",
        "/05/", "maio",
        "/06/", "junho",
        "/07/", "julho",
        "/08/", "agosto",
        "/09/", "setembro",
        "/10/", "outubro",
        "/11/", "novembro",
        "/12/", "dezembro"
    ]

    oneTime = True

    organ = cleanTextP[1].strip()
    unit = cleanTextP[2].strip()

    dict["orgao"] = organ
    dict["unidade_responsavel"] = unit

    dict["conteudo"] = f.format_allText(textAllP,unit)

    for i in range(0,len(cleanTextP),1):
        if "Despacho" in cleanTextP[i]: break
        if i == len(cleanTextP)-1: return None

    for i in range(0,len(cleanTextSpan),1):
        
        #Id do documento
        if "Documento:" in cleanTextSpan[i]:
            doc = cleanTextSpan[i].replace(" Documento:", "").strip()
            dict["id_doc"] = doc

        #Data da publicacao
        if "Publicação:" in cleanTextSpan[i]: 
            publication = cleanTextSpan[i].replace(" Publicação:", "").strip()
            dict["data_doc"] = publication

    for i in range(0,len(cleanTextP),1):
        
        for j in listServer:
            if j in cleanTextP[i]:
                name = f.format_name(cleanTextP[i],j)
                dict["name"] = name
                
        
        if "Curso" in cleanTextP[i] or "curso" in cleanTextP[i]: 
            if cleanTextP[i].find('"') >= 1 and cleanTextP[i+1].find('"') >= 1:
                reason = cleanTextP[i] + cleanTextP[i+1] 
            else:
                reason = cleanTextP[i]
            reason = f.format_reason(reason)
            dict["motivo"] = reason
        elif "participar" in cleanTextP[i]:
            reason = f.format_reason(cleanTextP[i])
            dict["motivo"] = reason

        for j in listMonth:
            if j in cleanTextP[i] and oneTime == True and not "Rua Quinze de novembro" in cleanTextP[i]:
                date = f.format_date(cleanTextP[i])
                if (len(date) == 1):
                    dict["dia_inicial"] = date[0]
                    dict["dia_final"] = date[0]
                else:
                    dict["dia_inicial"] = date[0]
                    dict["dia_final"] = date[1]
                oneTime = False
        
    list.append(json.dumps(dict, ensure_ascii=False))

    return list

def extractRemocao(cleanTextP,cleanTextSpan,textAllP):

    f = RemocaoFormat()

    dict = {}
    list = []

    listServer = ["servidor", "servidora", "SERVIDOR", "SERVIDORA"]

    organ = cleanTextP[1].strip()
    unit = cleanTextP[2].strip()

    dict["organ"] = organ
    dict["responsible_unit"] = unit

    dict["content"] = f.format_allText(textAllP,unit)

    for i in range(0,len(cleanTextSpan),1):
        
        #Id do documento
        if "Documento:" in cleanTextSpan[i]:
            doc = cleanTextSpan[i].replace(" Documento:", "").strip()
            dict["id_doc"] = doc

        #Data da publicacao
        if "Publicação:" in cleanTextSpan[i]: 
            publication = cleanTextSpan[i].replace(" Publicação:", "").strip()
            dict["date_doc"] = publication

    for i in range(0,len(cleanTextP),1):

        for j in listServer:
            if j in cleanTextP[i]:
                name = f.format_name(cleanTextP[i],j)
                position = cleanTextP[i+2]
                dict["name"] = name
                dict["position"] = position

        if " Divisão" in cleanTextP[i] or "Divisão" in cleanTextP[i] or "Assessoria" in cleanTextP[i]:
            department = f.format_department(cleanTextP[i])
            dict["department"] = department 

        if "partir" in cleanTextP[i]:
            starting = f.format_date(cleanTextP[i])
            dict["starting"] = starting

    list.append(json.dumps(dict, ensure_ascii=False))

    return list

def extractContractConsorcio(cleanTextP,cleanTextSpan,textAllP,html_site,driver):

    dict = {}
    list = []

    try:
        f, formatExtract = ExtractExternFactory.create(html=html_site,driver=driver)
    except Exception as e:
        print(e)
        formatExtract = None

    organ = cleanTextP[1].strip()
    unit = cleanTextP[2].strip()

    dict["organ"] = organ
    dict["responsible_unit"] = unit

    dict["content"] = f.format_allText(textAllP,unit)
    
    for i in cleanTextP:
        if (i.find("TERMO DE CONTRATO") != -1):    
            dict["typeContract"] = "termo de contrato"  
            break

    if (dict.get("typeContract") == None): return None 

    for i in range(0,len(cleanTextSpan),1):
        
        #Id do documento
        if ("Documento:" in cleanTextSpan[i]):
            doc = cleanTextSpan[i].replace(" Documento:", "").strip()
            dict["id_doc"] = doc

        #Data da publicacao
        if ("Publicação:" in cleanTextSpan[i]): 
            publication = cleanTextSpan[i].replace(" Publicação:", "").strip()
            dict["date_doc"] = publication

    for i in range(0,len(cleanTextP),1):
        
        if (' Número do Contrato' in cleanTextP[i]): 
            dict["numContract"] = cleanTextP[i+1].strip()
            
        if (' Contratado(a)' in cleanTextP[i]):
            dict["hired"] = cleanTextP[i+1].strip()

        if (' Tipo de Pessoa' in cleanTextP[i]):
            dict["typePerson"] = cleanTextP[i+1].strip()
        
        if (' CPF /CNPJ/ RNE' in cleanTextP[i]):
            dict["cnpj"] = cleanTextP[i+1].strip()

        if (' Data da Assinatura' in cleanTextP[i]):
            dict["dateAss"] = cleanTextP[i+1].strip()
            dict["yearOfContract"] = f.format_year(dict["dateAss"])

        if (' Prazo do Contrato' in cleanTextP[i]):
            dict["contractTemp"] = cleanTextP[i+1].strip()
        
        if (' Tipo do Prazo' in cleanTextP[i]):
            dict["typeTerm"] = cleanTextP[i+1].strip()
            dict["startDate"] = dict["dateAss"]
            dict["endDate"] = f.format_endDate(dict["dateAss"],dict["contractTemp"],dict["typeTerm"])

        if (' Síntese' in cleanTextP[i]):

            text = ""

            for j in range(1,100,1):
                if cleanTextP[i+j] == ' Data de Publicação':break
                text += cleanTextP[i+j] + ","

            dict["synthesis"] = text
            
            object = f.format_object(text)
            dict["objects"] = object

            if (hasPriceInObject(text) or formatExtract == None):
                dict["price"] = f.format_ObjectPrice(text)
            else:
                dict["price"] = formatExtract.extractPriceOnContract()

            if (hasContractTerm(text) or formatExtract == None):
                dict["contractTerm"] = f.format_ContractTerm(text,dict["dateAss"])
            else:
                dict["contractTerm"] = formatExtract.extractContractTerm(dict["dateAss"])

            if (hasProcessSEI(text) or formatExtract == None):
                dict["processSEI"] = f.format_processSEI(text)
            else:
                dict["processSEI"] = formatExtract.extractProcessSEI()
            
            if (hasAllocation(text) or formatExtract == None):
                dict["Allocation"] = f.format_allocation(text)
            else:
                dict["Allocation"] = formatExtract.extractAllocation()

            if (hasContractor(text) or formatExtract == None):
                dict["contractor"] = f.format_contractor(text)
            else:
                dict["contractor"] = formatExtract.extractContractor()

            if (hasCommitment(text) or formatExtract == None):
                dict["commitmentNote"] = f.format_commitment(text)
            else:
                dict["commitmentNote"] = formatExtract.extractCommitment()

    if (dict.get("hired") == None or dict["hired"] == "" and formatExtract != None):
        dict["dateAss"] = formatExtract.extractHired()

    if (dict.get("contractTerm") == None or dict["contractTerm"] not in "SIURB"):
        if (dict.get("numContract")):
            dict["contractTerm"] = f.doContractTerm(dict["numContract"], dict["yearOfContract"][2:])
        else:    
            dict["contractTerm"] = None

    list.append(json.dumps(dict, ensure_ascii=False))

    return list

def extractContractCompras(cleanTextP,cleanTextSpan,textAllP,html_site,driver):

    dict = {}
    list = []

    try:
        f, formatExtract = ExtractExternFactory.create(html=html_site,driver=driver)
    except Exception as e:
        print(e)
        formatExtract = None

    organ = cleanTextP[1].strip()
    unit = cleanTextP[2].strip()

    dict["organ"] = organ
    dict["responsible_unit"] = unit

    dict["content"] = f.format_allText(textAllP,unit)
    
    for i in cleanTextP:
        if (i.find("TERMO DE CONTRATO") != -1):    
            dict["typeContract"] = "termo de contrato"  
            break

    if (dict.get("typeContract") == None): return None 

    for i in range(0,len(cleanTextSpan),1):
        
        #Id do documento
        if ("Documento:" in cleanTextSpan[i]):
            doc = cleanTextSpan[i].replace(" Documento:", "").strip()
            dict["id_doc"] = doc

        #Data da publicacao
        if ("Publicação:" in cleanTextSpan[i]): 
            publication = cleanTextSpan[i].replace(" Publicação:", "").strip()
            dict["date_doc"] = publication

    for i in range(0,len(cleanTextP),1):
        
        if (' Número do Contrato' in cleanTextP[i]): 
            dict["numContract"] = cleanTextP[i+1].strip()
            
        if (' Contratado(a)' in cleanTextP[i]):
            dict["hired"] = cleanTextP[i+1].strip()

        if (' Tipo de Pessoa' in cleanTextP[i]):
            dict["typePerson"] = cleanTextP[i+1].strip()
        
        if (' CPF /CNPJ/ RNE' in cleanTextP[i]):
            dict["cnpj"] = cleanTextP[i+1].strip()

        if (' Data da Assinatura' in cleanTextP[i]):
            dict["dateAss"] = cleanTextP[i+1].strip()
            dict["yearOfContract"] = f.format_year(dict["dateAss"])

        if (' Prazo do Contrato' in cleanTextP[i]):
            dict["contractTemp"] = cleanTextP[i+1].strip()
        
        if (' Tipo do Prazo' in cleanTextP[i]):
            dict["typeTerm"] = cleanTextP[i+1].strip()
            dict["startDate"] = dict["dateAss"]
            dict["endDate"] = f.format_endDate(dict["dateAss"],dict["contractTemp"],dict["typeTerm"])

        if (' Síntese' in cleanTextP[i]):

            text = ""

            for j in range(1,100,1):
                if cleanTextP[i+j] == ' Data de Publicação':break
                text += cleanTextP[i+j] + ","

            dict["synthesis"] = text
            
            object = f.format_object(text)
            dict["objects"] = object

            if (hasPriceInObject(text) or formatExtract == None):
                dict["price"] = f.format_ObjectPrice(text)
            else:
                dict["price"] = formatExtract.extractPriceOnContract()

            if (hasContractTerm(text) or formatExtract == None):
                dict["contractTerm"] = f.format_ContractTerm(text,dict["dateAss"])
            else:
                dict["contractTerm"] = formatExtract.extractContractTerm(dict["dateAss"])

            if (hasProcessSEI(text) or formatExtract == None):
                dict["processSEI"] = f.format_processSEI(text)
            else:
                dict["processSEI"] = formatExtract.extractProcessSEI()
            
            if (hasAllocation(text) or formatExtract == None):
                dict["Allocation"] = f.format_allocation(text)
            else:
                dict["Allocation"] = formatExtract.extractAllocation()

            if (hasContractor(text) or formatExtract == None):
                dict["contractor"] = f.format_contractor(text)
            else:
                dict["contractor"] = formatExtract.extractContractor()

            if (hasCommitment(text) or formatExtract == None):
                dict["commitmentNote"] = f.format_commitment(text)
            else:
                dict["commitmentNote"] = formatExtract.extractCommitment()

    if (dict.get("hired") == None or dict["hired"] == "" and formatExtract != None):
        dict["dateAss"] = formatExtract.extractHired()

    if (dict.get("contractTerm") == None or dict["contractTerm"] not in "SIURB"):
        if (dict.get("numContract")):
            dict["contractTerm"] = f.doContractTerm(dict["numContract"], dict["yearOfContract"][2:])
        else:    
            dict["contractTerm"] = None

    list.append(json.dumps(dict, ensure_ascii=False))

    return list

def extractContractAditamento(cleanTextP,cleanTextSpan,textAllP,html_site,driver):
     
    
    dict = {}
    list = []

    try:
        f, formatExtract = ExtractExternFactory.create(html=html_site,driver=driver)
    except Exception as e:
        print(e)
        formatExtract = None

    organ = cleanTextP[1].strip()
    unit = cleanTextP[2].strip()

    dict["organ"] = organ
    dict["responsible_unit"] = unit

    dict["content"] = f.format_allText(textAllP,unit)
    
    for i in cleanTextP:
        if (i.find("TERMO DE ADITAMENTO") != -1):    
            dict["typeContract"] = "TERMO DE ADITAMENTO"  
            break

    if (dict.get("typeContract") == None): return None 

    for i in range(0,len(cleanTextSpan),1):
        
        #Id do documento
        if ("Documento:" in cleanTextSpan[i]):
            doc = cleanTextSpan[i].replace(" Documento:", "").strip()
            dict["id_doc"] = doc

        #Data da publicacao
        if ("Publicação:" in cleanTextSpan[i]): 
            publication = cleanTextSpan[i].replace(" Publicação:", "").strip()
            dict["date_doc"] = publication

    for i in range(0,len(cleanTextP),1):
        
        if (' Número do Contrato' in cleanTextP[i]): 
            dict["numContract"] = cleanTextP[i+1].strip()
            
        if (' Contratado(a)' in cleanTextP[i]):
            dict["hired"] = cleanTextP[i+1].strip()

        if (' Tipo de Pessoa' in cleanTextP[i]):
            dict["typePerson"] = cleanTextP[i+1].strip()
        
        if (' CPF /CNPJ/ RNE' in cleanTextP[i]):
            dict["cnpj"] = cleanTextP[i+1].strip()

        if (' Data da Assinatura' in cleanTextP[i]):
            dict["dateAss"] = cleanTextP[i+1].strip()
            dict["yearOfContract"] = f.format_year(dict["dateAss"])

        if (' Prazo do Contrato' in cleanTextP[i]):
            dict["contractTemp"] = cleanTextP[i+1].strip()
        
        if (' Tipo do Prazo' in cleanTextP[i]):
            dict["typeTerm"] = cleanTextP[i+1].strip()
            dict["startDate"] = dict["dateAss"]
            dict["endDate"] = f.format_endDate(dict["dateAss"],dict["contractTemp"],dict["typeTerm"])

        if (' Síntese' in cleanTextP[i]):

            text = ""

            for j in range(1,100,1):
                if cleanTextP[i+j] == ' Data de Publicação':break
                text += cleanTextP[i+j] + ","

            dict["synthesis"] = text.strip()
            
            object = f.format_object(text)
            dict["objects"] = object

            if (hasPriceInObject(text) or formatExtract == None):
                dict["price"] = f.format_ObjectPrice(text)
            else:
                dict["price"] = formatExtract.extractPriceOnContract()

            if (hasContractTerm(text) or formatExtract == None):
                dict["contractTerm"] = f.format_ContractTerm(text,dict["dateAss"])
            else:
                dict["contractTerm"] = formatExtract.extractContractTerm(dict["dateAss"])

            if (hasProcessSEI(text) or formatExtract == None):
                dict["processSEI"] = f.format_processSEI(text)
            else:
                dict["processSEI"] = formatExtract.extractProcessSEI()
            
            if (hasAllocation(text) or formatExtract == None):
                dict["Allocation"] = f.format_allocation(text)
            else:
                dict["Allocation"] = formatExtract.extractAllocation()

            if (hasContractor(text) or formatExtract == None):
                dict["contractor"] = f.format_contractor(text)
            else:
                dict["contractor"] = formatExtract.extractContractor()

            if (hasCommitment(text) or formatExtract == None):
                dict["commitmentNote"] = f.format_commitment(text)
            else:
                dict["commitmentNote"] = formatExtract.extractCommitment()

            if (hasObjectAditamento(text) or formatExtract == None):
                dict["objects_aditamento"] = f.format_objects_aditamento(text)
            else:
                dict["objects_aditamento"] = formatExtract.extractObjectAditamento()

    if (dict.get("hired") == None or dict["hired"] == "" and formatExtract != None):
        dict["dateAss"] = formatExtract.extractHired()

    if (dict.get("contractTerm") == None or dict["contractTerm"] not in "SIURB"):
        if (dict.get("numContract")):
            dict["contractTerm"] = f.doContractTerm(dict["numContract"], dict["yearOfContract"][2:])
        else:    
            dict["contractTerm"] = None

    if (dict.get("price") != None and len(dict["price"]) > 50):
        dict["price"] = None

    list.append(json.dumps(dict, ensure_ascii=False))

    return list
