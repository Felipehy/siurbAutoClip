import pymysql
import json
from config.settings import HOST_DB,USER_DB,PASSWD_DB

class DiaryRepository():

    _tables = {
        1: ("tbl_nomeacao", "tn"),
        2: ("tbl_exoneracao", "te"), 
        3: ("tbl_substituicao", "ts"),
        4: ("tbl_ferias_def", "tfd"),
        5: ("tbl_conc_aposen", "tca"),
        6: ("tbl_afastamento", "ta"),
        7: ("tbl_remocao", "tr"),
        8: ("tbl_contrato_consorcio", "tcc"),
        9: ("tbl_contrato_compras","tcc"),
        10: ("tbl_contrato_aditamento","tca")
    }

    def __init__(self):
        self.connection = pymysql.connect(
            host=HOST_DB,
            user=USER_DB,
            passwd=PASSWD_DB,
        )

    def has_doc(self, id_doc:str ,doc_type: int) -> bool:
        
        table_info = self._tables.get(doc_type)
        
        if not table_info:
            raise ValueError(f"Tipo {doc_type} não mapeada")

        table, alias = table_info
        cursor = self.connection.cursor()
        cursor.execute(f"""
            SELECT DISTINCT {alias}.id_doc
            FROM db_diario.{table} {alias}
            WHERE {alias}.id_doc = %s
        """,[id_doc])

        result = cursor.fetchall()
        return bool(result)
    
    def save(self, data: list, db_method: str):

        method = getattr(self, db_method, None)
        
        if method is None:
            raise ValueError(f"Repository não tem metodo {db_method}")
        
        method(data)

    def _execute_many(self, query: str, records: list):

        cursor = self.connection.cursor()

        for record in records:
            try:    
                if record is None: continue
                cursor.execute(query,record)
            except Exception as e:
                print(f"{e} id document: {record['id_doc']}")
                continue

        self.connection.commit()

    def send_nomeacao(self,data: list):

        records = []
        for item in data:
            if (item is None): continue
            for row in item:
                d = json.loads(row)
                records.append([
                    d["name"], d["data"], d["cargo"], d["departamento"],
                    d["processo"], d["publicacao"], d["orgao"],
                    d["id_doc"], d["conteudo"]
                ])

        self._execute_many("""
            INSERT INTO db_diario.tbl_nomeacao
                (nome,data,cargo,departamento,num_proc,data_doc,orgao,id_doc,conteudo)
            VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, records)
    
    def send_exoneracao(self,data: list):

        records = []
        for item in data:
            if (item is None): continue
            for row in item:
                d = json.loads(row)
                records.append([
                    d["name"], d["data"], d["cargo"], d["departamento"],
                    d["processo"], d["publicacao"], d["orgao"],
                    d["id_doc"], d["conteudo"]
                ])

        self._execute_many("""
            INSERT INTO db_diario.tbl_exoneracao
                (nome,data,cargo,departamento,num_proc,data_doc,orgao,id_doc,conteudo)
            VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, records)
    
    def send_substituicao(self, data: list):
        records = []
        for item in data:
            if item is None: continue
            for row in item:
                d = json.loads(row)
                records.append([
                    d["name"], d["substituicao"], d["cargo"], d["novo_cargo"],
                    d["cargo_sub"], d["departamento"], d["ferias_inicio"],
                    d["ferias_fim"], d["publicacao"], d["orgao"],
                    d["id_doc"], d["conteudo"]
                ])

        self._execute_many("""
            INSERT INTO db_diario.tbl_substituicao
                (nome, substituido, cargo_ant, novo_cargo, cargo_sub, departamento,
                 ferias_inicio, ferias_fim, data_doc, orgao, id_doc, conteudo)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, records)

    def send_ferias_deferidas(self, data: list):
        records = []
        for item in data:
            if item is None: continue
            for row in item:
                d = json.loads(row)
                records.append([
                    d["name"], d["data"], d["cargo"], d["exercicio"],
                    d["qtt_dias"], d["publicacao"], d["orgao"],
                    d["id_doc"], d["conteudo"]
                ])

        self._execute_many("""
            INSERT INTO db_diario.tbl_ferias_def
                (nome, data, cargo, exercicio, qtt_dias, data_doc, orgao, id_doc, conteudo)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, records)

    def send_aposentadoria(self, data: list):
        records = []
        for item in data:
            if item is None: continue
            for row in item:
                d = json.loads(row)
                records.append([
                    d["name"], d["reg_func"], d["cargo"], d["simbolo"],
                    d["num_proc"], d["data_doc"], d["orgao"],
                    d["id_doc"], d["conteudo"]
                ])

        self._execute_many("""
            INSERT INTO db_diario.tbl_conc_aposen
                (nome, reg_func, cargo, simbolo, num_proc, data_doc, orgao, id_doc, conteudo)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, records)

    def send_afastamento(self, data: list):
        records = []
        for item in data:
            if item is None: continue
            for row in item:
                d = json.loads(row)
                records.append([
                    d["name"], d["motivo"], d["dia_inicial"], d["dia_final"],
                    d["data_doc"], d["orgao"], d["id_doc"], d["conteudo"]
                ])

        self._execute_many("""
            INSERT INTO db_diario.tbl_afastamento
                (nome, motivo, dia_inicial, dia_final, data_doc, orgao, id_doc, conteudo)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, records)

    def send_remocao(self, data: list):
        records = []
        for item in data:
            if item is None: continue
            for row in item:
                d = json.loads(row)
                records.append([
                    d["name"], d["department"], d["position"], d["starting"],
                    d["date_doc"], d["organ"], d["id_doc"], d["content"]
                ])

        self._execute_many("""
            INSERT INTO db_diario.tbl_remocao
                (nome, departamento, cargo, dia_inicial, data_doc, orgao, id_doc, conteudo)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, records)
    
    def send_contractConsorcio(self, data: list):
        records = []
        for item in data:
            if item is None: continue
            for row in item:
                d = json.loads(row)
                records.append([
                    d["organ"], d["content"],
                    d["id_doc"], d["date_doc"], d["numContract"], d["hired"], d["typePerson"], 
                    d["cnpj"], d["dateAss"], d["yearOfContract"], d["contractTemp"], d["typeTerm"],
                    d["startDate"], d["endDate"], d["synthesis"], d["objects"], d["price"],
                    d["contractTerm"], d["processSEI"], d["Allocation"], d["contractor"], d["commitmentNote"],
                ])
        self._execute_many("""
            INSERT INTO db_diario.tbl_contrato_consorcio
                (orgao,conteudo,id_doc,data_doc,numero_contratacao,nome_credor,tipo_pessoa,cnpj_empresarial,data_assinatura,ano_contrato,prazo_contratual
                ,tipo_prazo,dia_inicial_contrato,dia_final_contrato,sintese,descricao_objeto,valor_contrato,numero_contrato_siurb,numero_processo_sei,dotacao,prefeitura,nota_empenho)
                VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, records)

    def send_contractCompras(self, data: list):
        records = []
        for item in data:
            if item is None: continue
            for row in item:
                d = json.loads(row)
                records.append([
                    d["organ"], d["content"],
                    d["id_doc"], d["date_doc"], d["numContract"], d["hired"], d["typePerson"], 
                    d["cnpj"], d["dateAss"], d["yearOfContract"], d["contractTemp"], d["typeTerm"],
                    d["startDate"], d["endDate"], d["synthesis"], d["objects"], d["price"],
                    d["contractTerm"], d["processSEI"], d["Allocation"], d["contractor"], d["commitmentNote"],
                ])
        self._execute_many("""
            INSERT INTO db_diario.tbl_contrato_compras
                (orgao,conteudo,id_doc,data_doc,numero_contratacao,nome_credor,tipo_pessoa,cnpj_empresarial,data_assinatura,ano_contrato,prazo_contratual
                ,tipo_prazo,dia_inicial_contrato,dia_final_contrato,sintese,descricao_objeto,valor_contrato,numero_contrato_siurb,numero_processo_sei,dotacao,prefeitura,nota_empenho)
                VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, records)

    def send_contractAditamento(self, data: list):
        records = []
        for item in data:
            if item is None: continue
            for row in item:
                d = json.loads(row)
                records.append([
                    d["organ"], d["content"],
                    d["id_doc"], d["date_doc"], d["numContract"], d["hired"], d["typePerson"], 
                    d["cnpj"], d["dateAss"], d["yearOfContract"], d["contractTemp"], d["typeTerm"],
                    d["startDate"], d["endDate"], d["synthesis"], d["objects"],d["objects_aditamento"], d["price"],
                    d["contractTerm"], d["processSEI"], d["Allocation"], d["contractor"], d["commitmentNote"],
                ])
        self._execute_many("""
            INSERT INTO db_diario.tbl_contrato_aditamento
                (orgao,conteudo,id_doc,data_doc,numero_contratacao,nome_credor,tipo_pessoa,cnpj_empresarial,data_assinatura,ano_contrato,prazo_contratual
                ,tipo_prazo,dia_inicial_contrato,dia_final_contrato,sintese,descricao_objeto,objeto_do_aditamento,valor_contrato,numero_contrato_siurb,numero_processo_sei,dotacao,prefeitura,nota_empenho)
                VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, records)
