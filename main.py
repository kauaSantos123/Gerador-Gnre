import os
import shutil
import sys
import time as time
import xml.etree.ElementTree as ET
from datetime import date
from time import sleep

from PySide6 import QtCore
from PySide6.QtGui import QIcon
from PySide6.QtSql import QSqlDatabase, QSqlTableModel
from PySide6.QtWidgets import *
#selenium
from selenium import webdriver
from selenium.common.exceptions import (NoAlertPresentException,
                                        NoSuchElementException)
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait

from ui_main import Ui_Form


class Main(QWidget, Ui_Form):
    def __init__(self) -> None:
        super(Main,self).__init__()
        self.setupUi(self)
        appIcon = QIcon('./img/robo.png')
        self.setWindowIcon(appIcon)
        self.setWindowTitle("GNRE DIFAL")
        # _________________AÇOES_DE_BOTOES______________________#
        self.btn_comecar.clicked.connect(self.validar_data)

    def validar_data(self):
        global datavencimento
        datavencimento = self.Data_vencimento.text()
        self.pasta_ler()

    def pasta_ler(self):
      caminho_pasta = QFileDialog.getExistingDirectory(None, "Selecionar pasta")
      global pasta
      pasta = caminho_pasta
      self.lerxml()

    def lerxml(self):


        # PASTA QUE VAI LER OS XMLS
        pasta_xml = pasta
        # listar todos
        for root, subFolder, filename in os.walk(pasta_xml):
            for arq in filename:
                print(arq)
                # se for .xml o final vai passar pro for
                if arq.endswith(".xml"):
                    # ler xml
                    global xml_arq
                    xml_arq = f"{pasta}/%s" % (arq)

                    xml_file = arq
                    tree = ET.parse(xml_arq)
                    root = tree.getroot()
                    ns = {'nfe': 'http://www.portalfiscal.inf.br/nfe'}
                    try:
                        valor_difal = root.find(
                            './/nfe:NFe/nfe:infNFe/nfe:total/nfe:ICMSTot/nfe:vICMSUFDest', ns).text
                    except:
                        pass
                    try:
                        valor_st = root.find(
                            './/nfe:NFe/nfe:infNFe/nfe:total/nfe:ICMSTot/nfe:vST', ns).text
                    except:
                        pass
                    global CPF_CNPJ_DESTINATARIO
                    global RECEITA
                    global CONVENIO
                    global VALOR_TOTAL
                    global IDENTIFICAO
                    global INSCRITO
                    global IE
                    if valor_difal > str(0) :
                        # ICMS DIFAL
                        
                        try:
                            CPF_CNPJ_DESTINATARIO = root.find(
                                './/nfe:NFe/nfe:infNFe/nfe:dest/nfe:CPF', ns).text
                        except:
                            CPF_CNPJ_DESTINATARIO = root.find(
                                './/nfe:NFe/nfe:infNFe/nfe:dest/nfe:CNPJ', ns).text
                        print(CPF_CNPJ_DESTINATARIO)
                        CONVENIO = "87/15"
                        RECEITA = "100102"
                        VALOR_TOTAL = root.find(
                            './/nfe:NFe/nfe:infNFe/nfe:total/nfe:ICMSTot/nfe:vICMSUFDest', ns).text
                        if len(CPF_CNPJ_DESTINATARIO) > 11:
                            print('CNPJ')
                            IDENTIFICAO = 'tipoCNPJDest'
                        else:
                            print('CPF')
                            IDENTIFICAO = 'tipoCPFDest'
                        INSCRITO = 'optNaoInscritoDest'
                    elif valor_st > str(0):
                        # ICMS ST
                        try:
                            CPF_CNPJ_DESTINATARIO = root.find(
                                './/nfe:NFe/nfe:infNFe/nfe:dest/nfe:CNPJ', ns).text
                        except:
                            CPF_CNPJ_DESTINATARIO = root.find(
                                './/nfe:NFe/nfe:infNFe/nfe:dest/nfe:CPF', ns).text
                        CONVENIO = "85/93"
                        RECEITA = "100099"
                        VALOR_TOTAL = root.find(
                            './/nfe:NFe/nfe:infNFe/nfe:total/nfe:ICMSTot/nfe:vST', ns).text

                        if CPF_CNPJ_DESTINATARIO > '11':
                            print('CNPJ')
                            
                            IDENTIFICAO = 'tipoCNPJDest'
                        else:
                            print('CPF')
                            IDENTIFICAO = 'tipoCPFDest'
                        INSCRITO = "optInscritoDest"
                        IE = root.find(
                            './/nfe:NFe/nfe:infNFe/nfe:dest/nfe:IE', ns).text
                        

                        print(valor_st)
                    else:
                        self.sem_imposto()






                    global uf_f
                    uf_f = root.find(
                        './/nfe:NFe/nfe:infNFe/nfe:dest/nfe:enderDest/nfe:UF', ns).text
                    print(uf_f)
                    if uf_f == 'MG':
                        self.estado_MG()
                    elif uf_f == 'AC':
                        self.estado_AC()
                    elif uf_f == 'AL':
                        self.estado_AL()
                    elif uf_f == 'AM':
                        self.estado_AM()
                    elif uf_f == 'AP':
                        self.estado_AP()
                    elif uf_f == 'BA':
                        self.estado_BA()
                    elif uf_f == 'CE':
                        self.estado_CE()
                    elif uf_f == 'DF':
                        self.estado_DF()
                    elif uf_f == 'GO':
                        self.estado_GO()
                    elif uf_f == 'PE':
                        self.estado_PE()
                    elif uf_f == 'MT':
                        self.estado_MT()
                    elif uf_f == 'PI':
                        self.estado_PI()
                    elif uf_f == 'MS':
                        self.estado_MS()
                    elif uf_f == 'RN':
                        self.estado_RN()
                    elif uf_f == 'TO':
                        self.estado_TO()
                    elif uf_f == 'PA':
                        self.estado_PA()
                    elif uf_f == 'RO':
                        self.estado_RO()
                    elif uf_f == 'SC':
                        self.estado_SC()
                    elif uf_f == 'SE':
                        self.estado_SE()
                    elif uf_f == 'RS':
                        self.estado_RS()
                    elif uf_f == 'RJ':
                        self.estado_RJ()
                    elif uf_f == 'MA':
                        self.estado_MA()
                    elif uf_f == 'PR':
                        self.estado_PR()
                    elif uf_f == 'PB':
                        self.estado_PB()
                    elif uf_f == 'RR':
                        self.estado_RR()
                    elif uf_f == 'ES':
                        self.estado_ES()
                    elif uf_f == 'SP':
                        self.estado_SP()
    
    def sem_imposto(self):
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowTitle("Atenção")
            msg.setText("Nota sem imposto")
            msg.exec_() 
    #PRONTO DIFAL E ST
    def estado_AC(self):
        # Ler arquivo xml
        xml_arq
        tree = ET.parse(xml_arq)
        root = tree.getroot()
        ns = {'nfe': 'http://www.portalfiscal.inf.br/nfe'}
        # salvar informaçoes em variaveis
        Cnpj = root.find('.//nfe:NFe/nfe:infNFe/nfe:emit/nfe:CNPJ', ns).text
        Razao_Social = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:xNome', ns).text
        endereco = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:enderEmit/nfe:xLgr', ns).text
        Uf = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:enderEmit/nfe:UF', ns).text
        Cep = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:enderEmit/nfe:CEP', ns).text
        Codigo_Municipio = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:enderEmit/nfe:cMun', ns).text
        Codigo_Municipio = Codigo_Municipio[2:]
        Numero_Telefone = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:enderEmit/nfe:fone', ns).text
        Numero_Telefone = Numero_Telefone[2:]
        
        # dados para emitir gnre por estado
        Numero_NFE = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:ide/nfe:nNF', ns).text
        Periodo_Ref = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:ide/nfe:dhEmi', ns).text
        valor_difal = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:total/nfe:ICMSTot/nfe:vICMSUFDest', ns).text
        Ano_Ref = Periodo_Ref[:4]
        #dados destinatario

        razao_dest = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:dest/nfe:xNome', ns).text
        codigo_munc_dest = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:dest/nfe:enderDest/nfe:cMun', ns).text
        chave = root.find(
            './/nfe:protNFe/nfe:infProt/nfe:chNFe', ns).text
        
        codigo_munc_dest = codigo_munc_dest[2:]
        Periodo_Ref = Periodo_Ref[5:7]

        chrome_options = Options()
        chrome_options.add_argument("--incognito")
        web = webdriver.Chrome(chrome_options=chrome_options)
        web.maximize_window()
        web.get("https://www.gnre.pe.gov.br:444/gnre/v/guia/index")

        Select(web.find_element(By.ID, "ufFavorecida")).select_by_value(uf_f)

        sleep(2)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "optGnreSimples"))
        )
        web.find_element(By.ID, ("optGnreSimples")).click()
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "optNaoInscrito"))
        )
        web.find_element(By.ID, ("optNaoInscrito")).click()
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "tipoCNPJ"))
        )
        web.find_element(By.ID, ("tipoCNPJ")).click()
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "documentoEmitente"))
        )
        web.find_element(By.ID, ("documentoEmitente")).send_keys(Cnpj)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "razaoSocialEmitente"))
        )
        web.find_element(By.ID, ("razaoSocialEmitente")).send_keys(Razao_Social)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "razaoSocialEmitente"))
        )
        web.find_element(By.ID, ("enderecoEmitente")).send_keys(endereco)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "ufEmitente"))
        )
        Select(web.find_element(By.ID, "ufEmitente")).select_by_value(Uf)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "municipioEmitente"))
        )
        Select(web.find_element(By.ID, "municipioEmitente")
            ).select_by_value(Codigo_Municipio)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "cepEmitente"))
        )
        web.find_element(By.ID, ("cepEmitente")).send_keys(Cep)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "telefoneEmitente"))
        )
        web.find_element(By.ID, ("telefoneEmitente")).send_keys(Numero_Telefone)

        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "receita"))
        )
        Select(web.find_element(By.ID, "receita")
            ).select_by_value(RECEITA)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "tipoDocOrigem"))
        )
        Select(web.find_element(By.ID, "tipoDocOrigem")
            ).select_by_value('10')
        
        web.find_element(By.ID, ("numeroDocumentoOrigem")
                        ).send_keys(Numero_NFE)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "mesReferencia"))
        )
        Select(web.find_element(By.ID, "mesReferencia")
            ).select_by_value(Periodo_Ref)

        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "anoReferencia"))
        )
        Select(web.find_element(By.ID, "anoReferencia")
            ).select_by_value(Ano_Ref)

        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "dataVencimento"))
        )
        sleep(0.2)
        web.find_element(By.ID, ("dataVencimento")
                        ).send_keys(datavencimento)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "valor"))
        )
        web.find_element(By.ID, ("valor")
                        ).send_keys(VALOR_TOTAL)
        
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, INSCRITO))
        )
        web.find_element(By.ID, (INSCRITO)
                        ).click()
        
        #SE FOR INSCRITO NA UF
  
        if INSCRITO == "optInscritoDest":
            WebDriverWait(web, 10).until(
                EC.presence_of_element_located((By.ID, "inscricaoEstadualDestinatario"))
            )
            web.find_element(By.ID, ("inscricaoEstadualDestinatario")
                            ).send_keys(IE)
            WebDriverWait(web, 10).until(
                EC.presence_of_element_located((By.ID, "produto"))
            )
            sleep(0.6)
            Select(web.find_element(By.ID, "produto")
                ).select_by_value("22")
            WebDriverWait(web, 10).until(
                EC.presence_of_element_located((By.ID, "detalheReceita"))
            )
            Select(web.find_element(By.ID, "detalheReceita")
                ).select_by_value("000017")
            WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "campoAdicional02"))
            )
            sleep(0.2)
            web.find_element(By.ID, ("campoAdicional02")
                            ).send_keys(chave)
            web.find_element(By.ID, ("convenio")
                        ).send_keys(CONVENIO)
        else:
            print(IDENTIFICAO)
            WebDriverWait(web, 10).until(
                EC.presence_of_element_located((By.ID, IDENTIFICAO))
            )
            web.find_element(By.ID, (IDENTIFICAO)
                            ).click()
            WebDriverWait(web, 10).until(
                EC.presence_of_element_located((By.ID, "documentoDestinatario"))
            )
            sleep(0.2)
            web.find_element(By.ID, ("documentoDestinatario")
                            ).send_keys(CPF_CNPJ_DESTINATARIO)
            WebDriverWait(web, 10).until(
                EC.presence_of_element_located((By.ID, "razaoSocialDestinatario"))
            )
            web.find_element(By.ID, ("razaoSocialDestinatario")
                            ).send_keys(razao_dest)
            WebDriverWait(web, 10).until(
                EC.presence_of_element_located((By.ID, "municipioDestinatario"))
            )
            Select(web.find_element(By.ID, "municipioDestinatario")
                ).select_by_value(codigo_munc_dest)
            WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "campoAdicional01"))
            )
            sleep(0.2)
            web.find_element(By.ID, ("campoAdicional01")
                            ).send_keys(chave)
        

        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "dataPagamento"))
        )
        web.find_element(By.ID, ("dataPagamento")
                        ).clear()
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "dataPagamento"))
        )
        
        web.find_element(By.ID, ("dataPagamento")
                        ).send_keys(datavencimento)
        


        try:
            while True:
                if not web.execute_script("return window.top.closed"):
                    time.sleep(1)
                else:
                    print("navegador fechado")
                    break
        except:
            print("OK")
    #PRONTO DIFAL E ST
    def estado_AL(self):
        # Ler arquivo xml
        xml_arq
        tree = ET.parse(xml_arq)
        root = tree.getroot()
        ns = {'nfe': 'http://www.portalfiscal.inf.br/nfe'}
        # salvar informaçoes em variaveis
        Cnpj = root.find('.//nfe:NFe/nfe:infNFe/nfe:emit/nfe:CNPJ', ns).text
        Razao_Social = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:xNome', ns).text
        endereco = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:enderEmit/nfe:xLgr', ns).text
        Uf = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:enderEmit/nfe:UF', ns).text
        Cep = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:enderEmit/nfe:CEP', ns).text
        Codigo_Municipio = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:enderEmit/nfe:cMun', ns).text
        Codigo_Municipio = Codigo_Municipio[2:]
        Numero_Telefone = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:enderEmit/nfe:fone', ns).text
        Numero_Telefone = Numero_Telefone[2:]
        
        # dados para emitir gnre por estado
        Numero_NFE = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:ide/nfe:nNF', ns).text
        Periodo_Ref = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:ide/nfe:dhEmi', ns).text
        valor_difal = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:total/nfe:ICMSTot/nfe:vICMSUFDest', ns).text
        Ano_Ref = Periodo_Ref[:4]
        #dados destinatario

        razao_dest = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:dest/nfe:xNome', ns).text
        codigo_munc_dest = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:dest/nfe:enderDest/nfe:cMun', ns).text
        chave = root.find(
            './/nfe:protNFe/nfe:infProt/nfe:chNFe', ns).text
        
        codigo_munc_dest = codigo_munc_dest[2:]
        Periodo_Ref = Periodo_Ref[5:7]


        chrome_options = Options()
        chrome_options.add_argument("--incognito")
        web = webdriver.Chrome(chrome_options=chrome_options)
        web.maximize_window()
        web.get("https://www.gnre.pe.gov.br:444/gnre/v/guia/index")


        Select(web.find_element(By.ID, "ufFavorecida")).select_by_value(uf_f)

        sleep(2)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "optGnreSimples"))
        )
        web.find_element(By.ID, ("optGnreSimples")).click()
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "optNaoInscrito"))
        )
        web.find_element(By.ID, ("optNaoInscrito")).click()
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "tipoCNPJ"))
        )
        web.find_element(By.ID, ("tipoCNPJ")).click()
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "documentoEmitente"))
        )
        web.find_element(By.ID, ("documentoEmitente")).send_keys(Cnpj)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "razaoSocialEmitente"))
        )
        web.find_element(By.ID, ("razaoSocialEmitente")).send_keys(Razao_Social)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "razaoSocialEmitente"))
        )
        web.find_element(By.ID, ("enderecoEmitente")).send_keys(endereco)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "ufEmitente"))
        )
        Select(web.find_element(By.ID, "ufEmitente")).select_by_value(Uf)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "municipioEmitente"))
        )
        Select(web.find_element(By.ID, "municipioEmitente")
            ).select_by_value(Codigo_Municipio)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "cepEmitente"))
        )
        web.find_element(By.ID, ("cepEmitente")).send_keys(Cep)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "telefoneEmitente"))
        )
        web.find_element(By.ID, ("telefoneEmitente")).send_keys(Numero_Telefone)

        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "receita"))
        )
        Select(web.find_element(By.ID, "receita")
            ).select_by_value(RECEITA)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "tipoDocOrigem"))
        )
        Select(web.find_element(By.ID, "tipoDocOrigem")
            ).select_by_value('10')
        web.find_element(By.ID, ("numeroDocumentoOrigem")
                        ).send_keys(Numero_NFE)

        web.find_element(By.ID, ("convenio")
                        ).send_keys(CONVENIO)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "dataVencimento"))
        )
        sleep(0.2)
        web.find_element(By.ID, ("dataVencimento")
                        ).send_keys(datavencimento)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "valor"))
        )
        web.find_element(By.ID, ("valor")
                        ).send_keys(VALOR_TOTAL)
        
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, INSCRITO))
        )
        web.find_element(By.ID, (INSCRITO)
                        ).click()
        
        #SE FOR INSCRITO NA UF
  
        if INSCRITO == "optInscritoDest":
            WebDriverWait(web, 10).until(
                EC.presence_of_element_located((By.ID, "inscricaoEstadualDestinatario"))
            )
            web.find_element(By.ID, ("inscricaoEstadualDestinatario")
                            ).send_keys(IE)
            WebDriverWait(web, 10).until(
                EC.presence_of_element_located((By.ID, "produto"))
            )
            Select(web.find_element(By.ID, "produto")
                ).select_by_value("22")
        
        else:
            print(IDENTIFICAO)
            WebDriverWait(web, 10).until(
                EC.presence_of_element_located((By.ID, IDENTIFICAO))
            )
            web.find_element(By.ID, (IDENTIFICAO)
                            ).click()
            WebDriverWait(web, 10).until(
                EC.presence_of_element_located((By.ID, "documentoDestinatario"))
            )
            sleep(0.2)
            web.find_element(By.ID, ("documentoDestinatario")
                            ).send_keys(CPF_CNPJ_DESTINATARIO)
            WebDriverWait(web, 10).until(
                EC.presence_of_element_located((By.ID, "razaoSocialDestinatario"))
            )
            web.find_element(By.ID, ("razaoSocialDestinatario")
                            ).send_keys(razao_dest)
            WebDriverWait(web, 10).until(
                EC.presence_of_element_located((By.ID, "municipioDestinatario"))
            )
            Select(web.find_element(By.ID, "municipioDestinatario")
                ).select_by_value(codigo_munc_dest)
            WebDriverWait(web, 10).until(
                EC.presence_of_element_located((By.ID, "mesReferencia"))
            )
            Select(web.find_element(By.ID, "mesReferencia")
                ).select_by_value(Periodo_Ref)

            WebDriverWait(web, 10).until(
                EC.presence_of_element_located((By.ID, "anoReferencia"))
            )
            Select(web.find_element(By.ID, "anoReferencia")
                ).select_by_value(Ano_Ref)
        
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "campoAdicional00"))
        )
        sleep(0.2)
        web.find_element(By.ID, ("campoAdicional00")
                        ).send_keys(chave)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "dataPagamento"))
        )
        web.find_element(By.ID, ("dataPagamento")
                        ).clear()
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "dataPagamento"))
        )
        
        web.find_element(By.ID, ("dataPagamento")
                        ).send_keys(datavencimento)
        


        try:
            while True:
                if not web.execute_script("return window.top.closed"):
                    time.sleep(1)
                else:
                    print("navegador fechado")
                    break
        except:
            print("OK")
    #PRONTO DIFAL E ST
    def estado_AM(self):
         # Ler arquivo xml
        xml_arq
        tree = ET.parse(xml_arq)
        root = tree.getroot()
        ns = {'nfe': 'http://www.portalfiscal.inf.br/nfe'}
        # salvar informaçoes em variaveis
        Cnpj = root.find('.//nfe:NFe/nfe:infNFe/nfe:emit/nfe:CNPJ', ns).text
        Razao_Social = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:xNome', ns).text
        endereco = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:enderEmit/nfe:xLgr', ns).text
        Uf = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:enderEmit/nfe:UF', ns).text
        Cep = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:enderEmit/nfe:CEP', ns).text
        Codigo_Municipio = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:enderEmit/nfe:cMun', ns).text
        Codigo_Municipio = Codigo_Municipio[2:]
        Numero_Telefone = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:enderEmit/nfe:fone', ns).text
        Numero_Telefone = Numero_Telefone[2:]
        # dados para emitir gnre por estado
        Numero_NFE = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:ide/nfe:nNF', ns).text
        Periodo_Ref = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:ide/nfe:dhEmi', ns).text
        valor_difal = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:total/nfe:ICMSTot/nfe:vICMSUFDest', ns).text
        print(Periodo_Ref)
        Mes_Ref = Periodo_Ref[5:7]
        Ano_Ref = Periodo_Ref[:4]
        Emissao_nota = Periodo_Ref[8:10] +'/' + Periodo_Ref[5:7] + '/' + Periodo_Ref[:4]
        print(Emissao_nota)

        #dados destinatario

        razao_dest = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:dest/nfe:xNome', ns).text
        codigo_munc_dest = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:dest/nfe:enderDest/nfe:cMun', ns).text
        chave = root.find(
            './/nfe:protNFe/nfe:infProt/nfe:chNFe', ns).text
        
        codigo_munc_dest = codigo_munc_dest[2:]
        Periodo_Ref = Periodo_Ref[5:7]
        chrome_options = Options()
        chrome_options.add_argument("--incognito")
        web = webdriver.Chrome(chrome_options=chrome_options)
        web.maximize_window()
        web.get("https://www.gnre.pe.gov.br:444/gnre/v/guia/index")


        Select(web.find_element(By.ID, "ufFavorecida")).select_by_value(uf_f)

        sleep(2)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "optGnreSimples"))
        )
        web.find_element(By.ID, ("optGnreSimples")).click()
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "optNaoInscrito"))
        )
        web.find_element(By.ID, ("optNaoInscrito")).click()
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "tipoCNPJ"))
        )
        web.find_element(By.ID, ("tipoCNPJ")).click()
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "documentoEmitente"))
        )
        web.find_element(By.ID, ("documentoEmitente")).send_keys(Cnpj)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "razaoSocialEmitente"))
        )
        web.find_element(By.ID, ("razaoSocialEmitente")).send_keys(Razao_Social)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "razaoSocialEmitente"))
        )
        web.find_element(By.ID, ("enderecoEmitente")).send_keys(endereco)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "ufEmitente"))
        )
        Select(web.find_element(By.ID, "ufEmitente")).select_by_value(Uf)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "municipioEmitente"))
        )
        Select(web.find_element(By.ID, "municipioEmitente")
            ).select_by_value(Codigo_Municipio)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "cepEmitente"))
        )
        web.find_element(By.ID, ("cepEmitente")).send_keys(Cep)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "telefoneEmitente"))
        )
        web.find_element(By.ID, ("telefoneEmitente")).send_keys(Numero_Telefone)

        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "receita"))
        )
        Select(web.find_element(By.ID, "receita")
            ).select_by_value(RECEITA)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "produto"))
        )
        Select(web.find_element(By.ID, "produto")
            ).select_by_value('90')
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "tipoDocOrigem"))
        )
        Select(web.find_element(By.ID, "tipoDocOrigem")
            ).select_by_value('22')
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "numeroDocumentoOrigem"))
        )
        web.find_element(By.ID, ("numeroDocumentoOrigem")).send_keys(chave)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "periodo"))
        )
        Select(web.find_element(By.ID, "periodo")
            ).select_by_value('0')
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "mesReferencia"))
        )
        Select(web.find_element(By.ID, "mesReferencia")
            ).select_by_value(Mes_Ref)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "anoReferencia"))
        )
        Select(web.find_element(By.ID, "anoReferencia")
            ).select_by_value(Ano_Ref)
        sleep(0.6)
        web.find_element(By.ID, ("convenio")
                        ).send_keys(CONVENIO)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "dataVencimento"))
        )
        web.find_element(By.ID, ("dataVencimento")).send_keys(datavencimento)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "valor"))
        )
        web.find_element(By.ID, ("valor")).send_keys(VALOR_TOTAL)
        WebDriverWait(web, 10).until(

            EC.presence_of_element_located((By.ID, INSCRITO))
        )
        web.find_element(By.ID, (INSCRITO)
                        ).click()
        #SE FOR INSCRITO NA UF
  
        if INSCRITO == "optInscritoDest":
            WebDriverWait(web, 10).until(
                EC.presence_of_element_located((By.ID, "inscricaoEstadualDestinatario"))
            )
            web.find_element(By.ID, ("inscricaoEstadualDestinatario")
                            ).send_keys(IE)
        else:
            WebDriverWait(web, 10).until(
                EC.presence_of_element_located((By.ID, IDENTIFICAO))
            )
            web.find_element(By.ID, (IDENTIFICAO)
                            ).click()
            
            WebDriverWait(web, 10).until(
                EC.presence_of_element_located((By.ID, "documentoDestinatario"))
            )
            web.find_element(By.ID, ("documentoDestinatario")
                            ).send_keys(CPF_CNPJ_DESTINATARIO)
            WebDriverWait(web, 10).until(
                EC.presence_of_element_located((By.ID, "razaoSocialDestinatario"))
            )
            web.find_element(By.ID, ("razaoSocialDestinatario")
                            ).send_keys(razao_dest)
            WebDriverWait(web, 10).until(
                EC.presence_of_element_located((By.ID, "municipioDestinatario"))
            )
            Select(web.find_element(By.ID, "municipioDestinatario")
                ).select_by_value(codigo_munc_dest)

        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "dataPagamento"))
        )
        web.find_element(By.ID, ("dataPagamento")
                        ).clear()
        sleep(0.2)
        web.find_element(By.ID, ("dataPagamento")
                        ).send_keys(datavencimento)



        try:
            while True:
                if not web.execute_script("return window.top.closed"):
                    time.sleep(1)
                else:
                    print("navegador fechado")
                    break
        except:
            print("OK")
    #PRONTO DIFAL E ST
    def estado_AP(self):
         # Ler arquivo xml
        xml_arq
        tree = ET.parse(xml_arq)
        root = tree.getroot()
        ns = {'nfe': 'http://www.portalfiscal.inf.br/nfe'}
        # salvar informaçoes em variaveis
        Cnpj = root.find('.//nfe:NFe/nfe:infNFe/nfe:emit/nfe:CNPJ', ns).text
        Razao_Social = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:xNome', ns).text
        endereco = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:enderEmit/nfe:xLgr', ns).text
        Uf = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:enderEmit/nfe:UF', ns).text
        Cep = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:enderEmit/nfe:CEP', ns).text
        Codigo_Municipio = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:enderEmit/nfe:cMun', ns).text
        Codigo_Municipio = Codigo_Municipio[2:]
        Numero_Telefone = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:enderEmit/nfe:fone', ns).text
        Numero_Telefone = Numero_Telefone[2:]
        # dados para emitir gnre por estado
        Numero_NFE = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:ide/nfe:nNF', ns).text
        Periodo_Ref = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:ide/nfe:dhEmi', ns).text
        valor_difal = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:total/nfe:ICMSTot/nfe:vICMSUFDest', ns).text
        print(Periodo_Ref)
        Mes_Ref = Periodo_Ref[5:7]
        Ano_Ref = Periodo_Ref[:4]
        Emissao_nota = Periodo_Ref[8:10] +'/' + Periodo_Ref[5:7] + '/' + Periodo_Ref[:4]
        print(Emissao_nota)

        #dados destinatario

        razao_dest = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:dest/nfe:xNome', ns).text
        codigo_munc_dest = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:dest/nfe:enderDest/nfe:cMun', ns).text
        chave = root.find(
            './/nfe:protNFe/nfe:infProt/nfe:chNFe', ns).text
        
        codigo_munc_dest = codigo_munc_dest[2:]
        Periodo_Ref = Periodo_Ref[5:7]
        chrome_options = Options()
        chrome_options.add_argument("--incognito")
        web = webdriver.Chrome(chrome_options=chrome_options)
        web.maximize_window()
        web.get("https://www.gnre.pe.gov.br:444/gnre/v/guia/index")


        Select(web.find_element(By.ID, "ufFavorecida")).select_by_value(uf_f)

        sleep(2)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "optGnreSimples"))
        )
        web.find_element(By.ID, ("optGnreSimples")).click()
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "optNaoInscrito"))
        )
        web.find_element(By.ID, ("optNaoInscrito")).click()
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "tipoCNPJ"))
        )
        web.find_element(By.ID, ("tipoCNPJ")).click()
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "documentoEmitente"))
        )
        web.find_element(By.ID, ("documentoEmitente")).send_keys(Cnpj)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "razaoSocialEmitente"))
        )
        web.find_element(By.ID, ("razaoSocialEmitente")).send_keys(Razao_Social)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "razaoSocialEmitente"))
        )
        web.find_element(By.ID, ("enderecoEmitente")).send_keys(endereco)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "ufEmitente"))
        )
        Select(web.find_element(By.ID, "ufEmitente")).select_by_value(Uf)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "municipioEmitente"))
        )
        Select(web.find_element(By.ID, "municipioEmitente")
            ).select_by_value(Codigo_Municipio)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "cepEmitente"))
        )
        web.find_element(By.ID, ("cepEmitente")).send_keys(Cep)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "telefoneEmitente"))
        )
        web.find_element(By.ID, ("telefoneEmitente")).send_keys(Numero_Telefone)

        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "receita"))
        )
        Select(web.find_element(By.ID, "receita")
            ).select_by_value(RECEITA)

        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "tipoDocOrigem"))
        )
        Select(web.find_element(By.ID, "tipoDocOrigem")
            ).select_by_value('10')
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "numeroDocumentoOrigem"))
        )
        web.find_element(By.ID, ("numeroDocumentoOrigem")).send_keys(Numero_NFE)

        if INSCRITO == "optInscritoDest":
            pass
        else:
            WebDriverWait(web, 10).until(
                EC.presence_of_element_located((By.ID, "periodo"))
            )
            Select(web.find_element(By.ID, "periodo")
                ).select_by_value('0')
            WebDriverWait(web, 10).until(
                EC.presence_of_element_located((By.ID, "mesReferencia"))
            )
            Select(web.find_element(By.ID, "mesReferencia")
                ).select_by_value(Mes_Ref)
            WebDriverWait(web, 10).until(
                EC.presence_of_element_located((By.ID, "anoReferencia"))
            )
            Select(web.find_element(By.ID, "anoReferencia")
                ).select_by_value(Ano_Ref)
            sleep(0.6)
        web.find_element(By.ID, ("convenio")
                        ).send_keys(CONVENIO)
            
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "dataVencimento"))
        )
        sleep(0.9)
        web.find_element(By.ID, ("dataVencimento")).send_keys(datavencimento)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "valor"))
        )
        web.find_element(By.ID, ("valor")).send_keys(VALOR_TOTAL)
        WebDriverWait(web, 10).until(

            EC.presence_of_element_located((By.ID, INSCRITO))
        )
        web.find_element(By.ID, (INSCRITO)
                        ).click()
        #SE FOR INSCRITO NA UF
  
        if INSCRITO == "optInscritoDest":
            WebDriverWait(web, 10).until(
                EC.presence_of_element_located((By.ID, "inscricaoEstadualDestinatario"))
            )
            web.find_element(By.ID, ("inscricaoEstadualDestinatario")
                            ).send_keys(IE)
        else:
            WebDriverWait(web, 10).until(
                EC.presence_of_element_located((By.ID, IDENTIFICAO))
            )
            web.find_element(By.ID, (IDENTIFICAO)
                            ).click()
            
            WebDriverWait(web, 10).until(
                EC.presence_of_element_located((By.ID, "documentoDestinatario"))
            )
            web.find_element(By.ID, ("documentoDestinatario")
                            ).send_keys(CPF_CNPJ_DESTINATARIO)
            WebDriverWait(web, 10).until(
                EC.presence_of_element_located((By.ID, "razaoSocialDestinatario"))
            )
            web.find_element(By.ID, ("razaoSocialDestinatario")
                            ).send_keys(razao_dest)
            WebDriverWait(web, 10).until(
                EC.presence_of_element_located((By.ID, "municipioDestinatario"))
            )
            Select(web.find_element(By.ID, "municipioDestinatario")
                ).select_by_value(codigo_munc_dest)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "campoAdicional00"))
        )
        sleep(0.5)
        web.find_element(By.ID, ("campoAdicional00")
                        ).send_keys(chave)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "dataPagamento"))
        )
        web.find_element(By.ID, ("dataPagamento")
                        ).clear()
        sleep(0.9)
        web.find_element(By.ID, ("dataPagamento")
                        ).send_keys(datavencimento)
        try:
            while True:
                if not web.execute_script("return window.top.closed"):
                    time.sleep(1)
                else:
                    print("navegador fechado")
                    break
        except:
            print("OK")
    #PRONTO DIFAL E ST
    def estado_BA(self):
        # Ler arquivo xml
        xml_arq
        tree = ET.parse(xml_arq)
        root = tree.getroot()
        ns = {'nfe': 'http://www.portalfiscal.inf.br/nfe'}
        # salvar informaçoes em variaveis
        Cnpj = root.find('.//nfe:NFe/nfe:infNFe/nfe:emit/nfe:CNPJ', ns).text
        Numero_NFE = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:ide/nfe:nNF', ns).text
        Razao_Social = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:xNome', ns).text
        endereco = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:enderEmit/nfe:xLgr', ns).text
        Uf = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:enderEmit/nfe:UF', ns).text
        Cep = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:enderEmit/nfe:CEP', ns).text
        Codigo_Municipio = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:enderEmit/nfe:cMun', ns).text
        Codigo_Municipio = Codigo_Municipio[2:]
        Numero_Telefone = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:enderEmit/nfe:fone', ns).text
        valor_difal = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:total/nfe:ICMSTot/nfe:vICMSUFDest', ns).text
        Numero_Telefone = Numero_Telefone[2:]

        Periodo_Ref = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:ide/nfe:dhEmi', ns).text
        Ano_Ref = Periodo_Ref[:4]
        print(Periodo_Ref)
        Mes_Ref = Periodo_Ref[5:7]

        chrome_options = Options()
        chrome_options.add_argument("--incognito")
        web = webdriver.Chrome(chrome_options=chrome_options)
        web.maximize_window()
        web.get("https://www.gnre.pe.gov.br:444/gnre/v/guia/index")


        Select(web.find_element(By.ID, "ufFavorecida")).select_by_value(uf_f)

        sleep(2)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "optGnreSimples"))
        )
        web.find_element(By.ID, ("optGnreSimples")).click()
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "optNaoInscrito"))
        )
        web.find_element(By.ID, ("optNaoInscrito")).click()
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "tipoCNPJ"))
        )
        web.find_element(By.ID, ("tipoCNPJ")).click()
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "documentoEmitente"))
        )
        web.find_element(By.ID, ("documentoEmitente")).send_keys(Cnpj)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "razaoSocialEmitente"))
        )
        web.find_element(By.ID, ("razaoSocialEmitente")).send_keys(Razao_Social)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "razaoSocialEmitente"))
        )
        web.find_element(By.ID, ("enderecoEmitente")).send_keys(endereco)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "ufEmitente"))
        )
        Select(web.find_element(By.ID, "ufEmitente")).select_by_value(Uf)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "municipioEmitente"))
        )
        Select(web.find_element(By.ID, "municipioEmitente")
            ).select_by_value(Codigo_Municipio)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "cepEmitente"))
        )
        web.find_element(By.ID, ("cepEmitente")).send_keys(Cep)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "telefoneEmitente"))
        )
        web.find_element(By.ID, ("telefoneEmitente")).send_keys(Numero_Telefone)

        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "receita"))
        )
        Select(web.find_element(By.ID, "receita")
            ).select_by_value(RECEITA)
        if INSCRITO == "optInscritoDest":

            web.find_element(By.ID, ("convenio")
                        ).send_keys(CONVENIO)
            WebDriverWait(web, 10).until(
                EC.presence_of_element_located((By.ID, "produto"))
            )
            Select(web.find_element(By.ID, "produto")
                ).select_by_value("22")
            WebDriverWait(web, 10).until(
                EC.presence_of_element_located((By.ID, "tipoDocOrigem"))
            )
            Select(web.find_element(By.ID, "tipoDocOrigem")
                ).select_by_value('10')
            web.find_element(By.ID, ("numeroDocumentoOrigem")
                            ).send_keys(Numero_NFE)
        else:
            print(IDENTIFICAO)

        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "periodo"))
        )
        Select(web.find_element(By.ID, "periodo")
            ).select_by_value('0')
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "mesReferencia"))
        )
        Select(web.find_element(By.ID, "mesReferencia")
            ).select_by_value(Mes_Ref)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "anoReferencia"))
        )
        Select(web.find_element(By.ID, "anoReferencia")
            ).select_by_value(Ano_Ref)
        
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "dataVencimento"))
        )
        sleep(0.2)
        web.find_element(By.ID, ("dataVencimento")).send_keys(datavencimento)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "valor"))
        )
        web.find_element(By.ID, ("valor")).send_keys(VALOR_TOTAL)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "dataPagamento"))
        )
        web.find_element(By.ID, ("dataPagamento")).clear()
        sleep(0.2)
        web.find_element(By.ID, ("dataPagamento")).send_keys(datavencimento)    
        try:
            while True:
                if not web.execute_script("return window.top.closed"):
                    time.sleep(1)
                else:
                    print("navegador fechado")
                    break
        except:
            print("OK")
    #PRONTO DIFAL E ST
    def estado_CE(self):
        # Ler arquivo xml
        xml_arq
        tree = ET.parse(xml_arq)
        root = tree.getroot()
        ns = {'nfe': 'http://www.portalfiscal.inf.br/nfe'}
        # salvar informaçoes em variaveis
        Cnpj = root.find('.//nfe:NFe/nfe:infNFe/nfe:emit/nfe:CNPJ', ns).text
        Razao_Social = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:xNome', ns).text
        endereco = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:enderEmit/nfe:xLgr', ns).text
        Uf = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:enderEmit/nfe:UF', ns).text
        Cep = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:enderEmit/nfe:CEP', ns).text
        Codigo_Municipio = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:enderEmit/nfe:cMun', ns).text
        Codigo_Municipio = Codigo_Municipio[2:]
        Numero_Telefone = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:enderEmit/nfe:fone', ns).text
        Numero_Telefone = Numero_Telefone[2:]
        
        # dados para emitir gnre por estado
        Numero_NFE = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:ide/nfe:nNF', ns).text
        Periodo_Ref = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:ide/nfe:dhEmi', ns).text
        valor_difal = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:total/nfe:ICMSTot/nfe:vICMSUFDest', ns).text
        Ano_Ref = Periodo_Ref[:4]
        #dados destinatario

        razao_dest = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:dest/nfe:xNome', ns).text
        codigo_munc_dest = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:dest/nfe:enderDest/nfe:cMun', ns).text
        chave = root.find(
            './/nfe:protNFe/nfe:infProt/nfe:chNFe', ns).text
        
        codigo_munc_dest = codigo_munc_dest[2:]
        Periodo_Ref = Periodo_Ref[5:7]


        chrome_options = Options()
        chrome_options.add_argument("--incognito")
        web = webdriver.Chrome(chrome_options=chrome_options)
        web.maximize_window()
        web.get("https://www.gnre.pe.gov.br:444/gnre/v/guia/index")


        Select(web.find_element(By.ID, "ufFavorecida")).select_by_value(uf_f)

        sleep(2)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "optGnreSimples"))
        )
        web.find_element(By.ID, ("optGnreSimples")).click()
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "optNaoInscrito"))
        )
        web.find_element(By.ID, ("optNaoInscrito")).click()
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "tipoCNPJ"))
        )
        web.find_element(By.ID, ("tipoCNPJ")).click()
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "documentoEmitente"))
        )
        web.find_element(By.ID, ("documentoEmitente")).send_keys(Cnpj)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "razaoSocialEmitente"))
        )
        web.find_element(By.ID, ("razaoSocialEmitente")).send_keys(Razao_Social)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "razaoSocialEmitente"))
        )
        web.find_element(By.ID, ("enderecoEmitente")).send_keys(endereco)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "ufEmitente"))
        )
        Select(web.find_element(By.ID, "ufEmitente")).select_by_value(Uf)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "municipioEmitente"))
        )
        Select(web.find_element(By.ID, "municipioEmitente")
            ).select_by_value(Codigo_Municipio)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "cepEmitente"))
        )
        web.find_element(By.ID, ("cepEmitente")).send_keys(Cep)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "telefoneEmitente"))
        )
        web.find_element(By.ID, ("telefoneEmitente")).send_keys(Numero_Telefone)

        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "receita"))
        )
        Select(web.find_element(By.ID, "receita")
            ).select_by_value(RECEITA)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "tipoDocOrigem"))
        )
        Select(web.find_element(By.ID, "tipoDocOrigem")
            ).select_by_value('10')
        web.find_element(By.ID, ("numeroDocumentoOrigem")
                        ).send_keys(Numero_NFE)

        web.find_element(By.ID, ("convenio")
                        ).send_keys(CONVENIO)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "dataVencimento"))
        )
        sleep(0.2)
        web.find_element(By.ID, ("dataVencimento")
                        ).send_keys(datavencimento)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "valor"))
        )
        web.find_element(By.ID, ("valor")
                        ).send_keys(VALOR_TOTAL)
        
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, INSCRITO))
        )
        web.find_element(By.ID, (INSCRITO)
                        ).click()
        
        #SE FOR INSCRITO NA UF
  
        if INSCRITO == "optInscritoDest":
            WebDriverWait(web, 10).until(
                EC.presence_of_element_located((By.ID, "inscricaoEstadualDestinatario"))
            )
            web.find_element(By.ID, ("inscricaoEstadualDestinatario")
                            ).send_keys(IE)
            WebDriverWait(web, 10).until(
                EC.presence_of_element_located((By.ID, "produto"))
            )
            Select(web.find_element(By.ID, "produto")
                ).select_by_value("22")
        
        else:
            print(IDENTIFICAO)
            WebDriverWait(web, 10).until(
                EC.presence_of_element_located((By.ID, IDENTIFICAO))
            )
            web.find_element(By.ID, (IDENTIFICAO)
                            ).click()
            WebDriverWait(web, 10).until(
                EC.presence_of_element_located((By.ID, "documentoDestinatario"))
            )
            sleep(0.2)
            web.find_element(By.ID, ("documentoDestinatario")
                            ).send_keys(CPF_CNPJ_DESTINATARIO)
            WebDriverWait(web, 10).until(
                EC.presence_of_element_located((By.ID, "razaoSocialDestinatario"))
            )
            web.find_element(By.ID, ("razaoSocialDestinatario")
                            ).send_keys(razao_dest)
            WebDriverWait(web, 10).until(
                EC.presence_of_element_located((By.ID, "municipioDestinatario"))
            )
            Select(web.find_element(By.ID, "municipioDestinatario")
                ).select_by_value(codigo_munc_dest)
        

        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "dataPagamento"))
        )
        web.find_element(By.ID, ("dataPagamento")
                        ).clear()
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "dataPagamento"))
        )
        
        web.find_element(By.ID, ("dataPagamento")
                        ).send_keys(datavencimento)
        

        try:
            while True:
                if not web.execute_script("return window.top.closed"):
                    time.sleep(1)
                else:
                    print("navegador fechado")
                    break
        except:
            print("OK")
    #PRONTO DIFAL E ST
    def estado_DF(self):
        # Ler arquivo xml
        xml_arq
        tree = ET.parse(xml_arq)
        root = tree.getroot()
        ns = {'nfe': 'http://www.portalfiscal.inf.br/nfe'}
        # salvar informaçoes em variaveis
        Cnpj = root.find('.//nfe:NFe/nfe:infNFe/nfe:emit/nfe:CNPJ', ns).text
        Razao_Social = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:xNome', ns).text
        endereco = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:enderEmit/nfe:xLgr', ns).text
        Uf = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:enderEmit/nfe:UF', ns).text
        Cep = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:enderEmit/nfe:CEP', ns).text
        Codigo_Municipio = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:enderEmit/nfe:cMun', ns).text
        Codigo_Municipio = Codigo_Municipio[2:]
        Numero_Telefone = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:enderEmit/nfe:fone', ns).text
        Numero_Telefone = Numero_Telefone[2:]
        
        # dados para emitir gnre por estado
        Numero_NFE = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:ide/nfe:nNF', ns).text
        Periodo_Ref = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:ide/nfe:dhEmi', ns).text
        valor_difal = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:total/nfe:ICMSTot/nfe:vICMSUFDest', ns).text
        Ano_Ref = Periodo_Ref[:4]
        #dados destinatario

        razao_dest = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:dest/nfe:xNome', ns).text
        codigo_munc_dest = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:dest/nfe:enderDest/nfe:cMun', ns).text
        chave = root.find(
            './/nfe:protNFe/nfe:infProt/nfe:chNFe', ns).text
        
        codigo_munc_dest = codigo_munc_dest[2:]
        Periodo_Ref = Periodo_Ref[5:7]


        chrome_options = Options()
        chrome_options.add_argument("--incognito")
        web = webdriver.Chrome(chrome_options=chrome_options)
        web.maximize_window()
        web.get("https://www.gnre.pe.gov.br:444/gnre/v/guia/index")


        Select(web.find_element(By.ID, "ufFavorecida")).select_by_value(uf_f)

        sleep(2)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "optGnreSimples"))
        )
        web.find_element(By.ID, ("optGnreSimples")).click()
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "optNaoInscrito"))
        )
        web.find_element(By.ID, ("optNaoInscrito")).click()
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "tipoCNPJ"))
        )
        web.find_element(By.ID, ("tipoCNPJ")).click()
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "documentoEmitente"))
        )
        web.find_element(By.ID, ("documentoEmitente")).send_keys(Cnpj)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "razaoSocialEmitente"))
        )
        web.find_element(By.ID, ("razaoSocialEmitente")).send_keys(Razao_Social)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "razaoSocialEmitente"))
        )
        web.find_element(By.ID, ("enderecoEmitente")).send_keys(endereco)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "ufEmitente"))
        )
        Select(web.find_element(By.ID, "ufEmitente")).select_by_value(Uf)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "municipioEmitente"))
        )
        Select(web.find_element(By.ID, "municipioEmitente")
            ).select_by_value(Codigo_Municipio)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "cepEmitente"))
        )
        web.find_element(By.ID, ("cepEmitente")).send_keys(Cep)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "telefoneEmitente"))
        )
        sleep(0.2)
        web.find_element(By.ID, ("telefoneEmitente")).send_keys(Numero_Telefone)

        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "receita"))
        )
        Select(web.find_element(By.ID, "receita")
            ).select_by_value(RECEITA)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "tipoDocOrigem"))
        )
        Select(web.find_element(By.ID, "tipoDocOrigem")
            ).select_by_value('10')
        web.find_element(By.ID, ("numeroDocumentoOrigem")
                        ).send_keys(Numero_NFE)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "mesReferencia"))
        )
        Select(web.find_element(By.ID, "mesReferencia")
            ).select_by_value(Periodo_Ref)

        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "anoReferencia"))
        )
        Select(web.find_element(By.ID, "anoReferencia")
            ).select_by_value(Ano_Ref)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "dataVencimento"))
        )
        sleep(0.2)
        
        web.find_element(By.ID, ("dataVencimento")
                        ).send_keys(datavencimento)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "valor"))
        )
        web.find_element(By.ID, ("valor")
                        ).send_keys(VALOR_TOTAL)
        #SE FOR INSCRITO NA UF
        if INSCRITO == "optInscritoDest":

            web.find_element(By.ID, ("convenio")
                        ).send_keys(CONVENIO)
            WebDriverWait(web, 10).until(
                EC.presence_of_element_located((By.ID, "produto"))
            )
            Select(web.find_element(By.ID, "produto")
                ).select_by_value("22")
        else:
            print(IDENTIFICAO)
            
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "dataPagamento"))
        )
        web.find_element(By.ID, ("dataPagamento")
                        ).clear()
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "dataPagamento"))
        )
        
        web.find_element(By.ID, ("dataPagamento")
                        ).send_keys(datavencimento)
        


        try:
            while True:
                if not web.execute_script("return window.top.closed"):
                    time.sleep(1)
                else:
                    print("navegador fechado")
                    break
        except:
            print("OK")
    #PRONTO DIFAL E ST
    def estado_GO(self):
        # Ler arquivo xml
        xml_arq
        tree = ET.parse(xml_arq)
        root = tree.getroot()
        ns = {'nfe': 'http://www.portalfiscal.inf.br/nfe'}
        # salvar informaçoes em variaveis
        Cnpj = root.find('.//nfe:NFe/nfe:infNFe/nfe:emit/nfe:CNPJ', ns).text
        Razao_Social = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:xNome', ns).text
        endereco = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:enderEmit/nfe:xLgr', ns).text
        Uf = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:enderEmit/nfe:UF', ns).text
        Cep = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:enderEmit/nfe:CEP', ns).text
        Codigo_Municipio = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:enderEmit/nfe:cMun', ns).text
        Codigo_Municipio = Codigo_Municipio[2:]
        Numero_Telefone = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:enderEmit/nfe:fone', ns).text
        Numero_Telefone = Numero_Telefone[2:]
        
        # dados para emitir gnre por estado
        Numero_NFE = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:ide/nfe:nNF', ns).text
        Periodo_Ref = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:ide/nfe:dhEmi', ns).text
        valor_difal = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:total/nfe:ICMSTot/nfe:vICMSUFDest', ns).text
        Ano_Ref = Periodo_Ref[:4]
        #dados destinatario

        razao_dest = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:dest/nfe:xNome', ns).text
        codigo_munc_dest = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:dest/nfe:enderDest/nfe:cMun', ns).text
        chave = root.find(
            './/nfe:protNFe/nfe:infProt/nfe:chNFe', ns).text
        
        codigo_munc_dest = codigo_munc_dest[2:]
        Periodo_Ref = Periodo_Ref[5:7]


        chrome_options = Options()
        chrome_options.add_argument("--incognito")
        web = webdriver.Chrome(chrome_options=chrome_options)
        web.maximize_window()
        web.get("https://www.gnre.pe.gov.br:444/gnre/v/guia/index")


        Select(web.find_element(By.ID, "ufFavorecida")).select_by_value(uf_f)

        sleep(2)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "optGnreSimples"))
        )
        web.find_element(By.ID, ("optGnreSimples")).click()
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "optNaoInscrito"))
        )
        web.find_element(By.ID, ("optNaoInscrito")).click()
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "tipoCNPJ"))
        )
        web.find_element(By.ID, ("tipoCNPJ")).click()
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "documentoEmitente"))
        )
        web.find_element(By.ID, ("documentoEmitente")).send_keys(Cnpj)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "razaoSocialEmitente"))
        )
        web.find_element(By.ID, ("razaoSocialEmitente")).send_keys(Razao_Social)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "razaoSocialEmitente"))
        )
        web.find_element(By.ID, ("enderecoEmitente")).send_keys(endereco)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "ufEmitente"))
        )
        Select(web.find_element(By.ID, "ufEmitente")).select_by_value(Uf)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "municipioEmitente"))
        )
        Select(web.find_element(By.ID, "municipioEmitente")
            ).select_by_value(Codigo_Municipio)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "cepEmitente"))
        )
        sleep(0.5)
        web.find_element(By.ID, ("cepEmitente")).send_keys(Cep)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "telefoneEmitente"))
        )
        sleep(0.5)
        web.find_element(By.ID, ("telefoneEmitente")).send_keys(Numero_Telefone)
        sleep(0.5)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "receita"))
        )
        Select(web.find_element(By.ID, "receita")
            ).select_by_value(RECEITA)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "tipoDocOrigem"))
        )
        Select(web.find_element(By.ID, "tipoDocOrigem")
            ).select_by_value('10')
        web.find_element(By.ID, ("numeroDocumentoOrigem")
                        ).send_keys(Numero_NFE)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "mesReferencia"))
        )
        sleep(0.5)
        Select(web.find_element(By.ID, "mesReferencia")
            ).select_by_value(Periodo_Ref)

        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "anoReferencia"))
        )
        Select(web.find_element(By.ID, "anoReferencia")
            ).select_by_value(Ano_Ref)
        web.find_element(By.ID, ("convenio")
                        ).send_keys(CONVENIO)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "dataVencimento"))
        )
        sleep(0.5)
        web.find_element(By.ID, ("dataVencimento")
                        ).send_keys(datavencimento)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "valor"))
        )
        web.find_element(By.ID, ("valor")
                        ).send_keys(VALOR_TOTAL)
        
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, INSCRITO))
        )
        web.find_element(By.ID, (INSCRITO)
                        ).click()
        
        #SE FOR INSCRITO NA UF
        sleep(0.5)
        if INSCRITO == "optInscritoDest":
            WebDriverWait(web, 10).until(
                EC.presence_of_element_located((By.ID, "inscricaoEstadualDestinatario"))
            )
            web.find_element(By.ID, ("inscricaoEstadualDestinatario")
                            ).send_keys(IE)
            WebDriverWait(web, 10).until(
                EC.presence_of_element_located((By.ID, "produto"))
            )
            Select(web.find_element(By.ID, "produto")
                ).select_by_value("22")
            sleep(0.5)
        else:
            print(IDENTIFICAO)
            WebDriverWait(web, 10).until(
                EC.presence_of_element_located((By.ID, IDENTIFICAO))
            )
            web.find_element(By.ID, (IDENTIFICAO)
                            ).click()
            WebDriverWait(web, 10).until(
                EC.presence_of_element_located((By.ID, "documentoDestinatario"))
            )
            sleep(0.2)
            web.find_element(By.ID, ("documentoDestinatario")
                            ).send_keys(CPF_CNPJ_DESTINATARIO)
            WebDriverWait(web, 10).until(
                EC.presence_of_element_located((By.ID, "razaoSocialDestinatario"))
            )
            web.find_element(By.ID, ("razaoSocialDestinatario")
                            ).send_keys(razao_dest)
            WebDriverWait(web, 10).until(
                EC.presence_of_element_located((By.ID, "municipioDestinatario"))
            )
            Select(web.find_element(By.ID, "municipioDestinatario")
                ).select_by_value(codigo_munc_dest)
        
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "campoAdicional00"))
        )
        sleep(0.5)
        web.find_element(By.ID, ("campoAdicional00")
                        ).send_keys(chave)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "dataPagamento"))
        )
        sleep(0.5)
        web.find_element(By.ID, ("dataPagamento")
                        ).clear()
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "dataPagamento"))
        )
        sleep(0.5)
        web.find_element(By.ID, ("dataPagamento")
                        ).send_keys(datavencimento)
        


        try:
            while True:
                if not web.execute_script("return window.top.closed"):
                    time.sleep(1)
                else:
                    print("navegador fechado")
                    break
        except:
            print("OK")
    #PRONTO DIFAL E ST
    def estado_MA(self):
        # Ler arquivo xml
        xml_arq
        tree = ET.parse(xml_arq)
        root = tree.getroot()
        ns = {'nfe': 'http://www.portalfiscal.inf.br/nfe'}
        # salvar informaçoes em variaveis
        Cnpj = root.find('.//nfe:NFe/nfe:infNFe/nfe:emit/nfe:CNPJ', ns).text
        Razao_Social = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:xNome', ns).text
        endereco = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:enderEmit/nfe:xLgr', ns).text
        Uf = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:enderEmit/nfe:UF', ns).text
        Cep = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:enderEmit/nfe:CEP', ns).text
        Codigo_Municipio = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:enderEmit/nfe:cMun', ns).text
        Codigo_Municipio = Codigo_Municipio[2:]
        Numero_Telefone = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:enderEmit/nfe:fone', ns).text
        Numero_Telefone = Numero_Telefone[2:]
        # dados para emitir gnre por estado
        Numero_NFE = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:ide/nfe:nNF', ns).text
        Periodo_Ref = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:ide/nfe:dhEmi', ns).text
        valor_difal = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:total/nfe:ICMSTot/nfe:vICMSUFDest', ns).text
        Ano_Ref = Periodo_Ref[:4]
        #dados destinatario

        razao_dest = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:dest/nfe:xNome', ns).text
        codigo_munc_dest = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:dest/nfe:enderDest/nfe:cMun', ns).text
        chave = root.find(
            './/nfe:protNFe/nfe:infProt/nfe:chNFe', ns).text
        
        codigo_munc_dest = codigo_munc_dest[2:]
        Periodo_Ref = Periodo_Ref[5:7]

        print(Periodo_Ref)

        chrome_options = Options()
        chrome_options.add_argument("--incognito")
        web = webdriver.Chrome(chrome_options=chrome_options)
        web.maximize_window()
        web.get("https://www.gnre.pe.gov.br:444/gnre/v/guia/index")


        Select(web.find_element(By.ID, "ufFavorecida")).select_by_value(uf_f)

        sleep(2)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "optGnreSimples"))
        )
        web.find_element(By.ID, ("optGnreSimples")).click()
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "optNaoInscrito"))
        )
        web.find_element(By.ID, ("optNaoInscrito")).click()
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "tipoCNPJ"))
        )
        web.find_element(By.ID, ("tipoCNPJ")).click()
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "documentoEmitente"))
        )
        web.find_element(By.ID, ("documentoEmitente")).send_keys(Cnpj)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "razaoSocialEmitente"))
        )
        web.find_element(By.ID, ("razaoSocialEmitente")).send_keys(Razao_Social)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "razaoSocialEmitente"))
        )
        web.find_element(By.ID, ("enderecoEmitente")).send_keys(endereco)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "ufEmitente"))
        )
        Select(web.find_element(By.ID, "ufEmitente")).select_by_value(Uf)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "municipioEmitente"))
        )
        Select(web.find_element(By.ID, "municipioEmitente")
            ).select_by_value(Codigo_Municipio)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "cepEmitente"))
        )
        web.find_element(By.ID, ("cepEmitente")).send_keys(Cep)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "telefoneEmitente"))
        )
        web.find_element(By.ID, ("telefoneEmitente")).send_keys(Numero_Telefone)

        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "receita"))
        )
        Select(web.find_element(By.ID, "receita")
            ).select_by_value(RECEITA)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "produto"))
        )
        Select(web.find_element(By.ID, "produto")
            ).select_by_value('90')
        
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "tipoDocOrigem"))
        )
        Select(web.find_element(By.ID, "tipoDocOrigem")
            ).select_by_value('10')
        web.find_element(By.ID, ("numeroDocumentoOrigem")
                        ).send_keys(Numero_NFE)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "mesReferencia"))
        )
        Select(web.find_element(By.ID, "mesReferencia")
            ).select_by_value(Periodo_Ref)

        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "anoReferencia"))
        )
        Select(web.find_element(By.ID, "anoReferencia")
            ).select_by_value(Ano_Ref)
        web.find_element(By.ID, ("convenio")
                        ).send_keys(CONVENIO)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "dataVencimento"))
        )
        web.find_element(By.ID, ("dataVencimento")
                        ).send_keys(datavencimento)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "tipoValorPrincipal"))
        )
        web.find_element(By.ID, ("tipoValorPrincipal")
                        ).click()
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "valor"))
        )
        web.find_element(By.ID, ("valor")
                        ).send_keys(VALOR_TOTAL)
        
        WebDriverWait(web, 10).until(

            EC.presence_of_element_located((By.ID, INSCRITO))
        )
        web.find_element(By.ID, (INSCRITO)
                        ).click()
        if INSCRITO == "optInscritoDest":
            WebDriverWait(web, 10).until(
                EC.presence_of_element_located((By.ID, "inscricaoEstadualDestinatario"))
            )
            web.find_element(By.ID, ("inscricaoEstadualDestinatario")
                            ).send_keys(IE)

        else:
            WebDriverWait(web, 10).until(
                EC.presence_of_element_located((By.ID, IDENTIFICAO))
            )
            web.find_element(By.ID, (IDENTIFICAO)
                            ).click()
            
            WebDriverWait(web, 10).until(
                EC.presence_of_element_located((By.ID, "documentoDestinatario"))
            )
            web.find_element(By.ID, ("documentoDestinatario")
                            ).send_keys(CPF_CNPJ_DESTINATARIO)
            WebDriverWait(web, 10).until(
                EC.presence_of_element_located((By.ID, "razaoSocialDestinatario"))
            )
            web.find_element(By.ID, ("razaoSocialDestinatario")
                            ).send_keys(razao_dest)
            WebDriverWait(web, 10).until(
                EC.presence_of_element_located((By.ID, "municipioDestinatario"))
            )
            Select(web.find_element(By.ID, "municipioDestinatario")
                ).select_by_value(codigo_munc_dest)
    
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "dataPagamento"))
        )
        web.find_element(By.ID, ("dataPagamento")
                        ).clear()
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "dataPagamento"))
        )
        web.find_element(By.ID, ("dataPagamento")
                        ).send_keys(datavencimento)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "campoAdicional00"))
        )
        web.find_element(By.ID, ("campoAdicional00")
                        ).send_keys(chave)
        
        try:
            while True:
                if not web.execute_script("return window.top.closed"):
                    time.sleep(1)
                else:
                    print("navegador fechado")
                    break
        except:
            print("OK")
    #PRONTO DIFAL E ST
    def estado_MG(self):
      # Ler arquivo xml
        xml_arq
        tree = ET.parse(xml_arq)
        root = tree.getroot()
        ns = {'nfe': 'http://www.portalfiscal.inf.br/nfe'}
        # salvar informaçoes em variaveis
        Cnpj = root.find('.//nfe:NFe/nfe:infNFe/nfe:emit/nfe:CNPJ', ns).text
        Razao_Social = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:xNome', ns).text
        endereco = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:enderEmit/nfe:xLgr', ns).text
        Uf = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:enderEmit/nfe:UF', ns).text
        Cep = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:enderEmit/nfe:CEP', ns).text
        Codigo_Municipio = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:enderEmit/nfe:cMun', ns).text
        Codigo_Municipio = Codigo_Municipio[2:]
        Numero_Telefone = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:enderEmit/nfe:fone', ns).text
        Numero_Telefone = Numero_Telefone[2:]
        # dados para emitir gnre por estado
        Numero_NFE = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:ide/nfe:nNF', ns).text
        Periodo_Ref = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:ide/nfe:dhEmi', ns).text
        valor_difal = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:total/nfe:ICMSTot/nfe:vICMSUFDest', ns).text
        Ano_Ref = Periodo_Ref[:4]
        #dados destinatario

        razao_dest = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:dest/nfe:xNome', ns).text
        codigo_munc_dest = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:dest/nfe:enderDest/nfe:cMun', ns).text
        chave = root.find(
            './/nfe:protNFe/nfe:infProt/nfe:chNFe', ns).text
        
        codigo_munc_dest = codigo_munc_dest[2:]
        Periodo_Ref = Periodo_Ref[5:7]

        print(Periodo_Ref)

        chrome_options = Options()
        chrome_options.add_argument("--incognito")
        web = webdriver.Chrome(chrome_options=chrome_options)
        web.maximize_window()
        web.get("https://www.gnre.pe.gov.br:444/gnre/v/guia/index")


        Select(web.find_element(By.ID, "ufFavorecida")).select_by_value(uf_f)

        sleep(2)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "optGnreSimples"))
        )
        web.find_element(By.ID, ("optGnreSimples")).click()
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "optNaoInscrito"))
        )
        web.find_element(By.ID, ("optNaoInscrito")).click()
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "tipoCNPJ"))
        )
        web.find_element(By.ID, ("tipoCNPJ")).click()
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "documentoEmitente"))
        )
        web.find_element(By.ID, ("documentoEmitente")).send_keys(Cnpj)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "razaoSocialEmitente"))
        )
        web.find_element(By.ID, ("razaoSocialEmitente")).send_keys(Razao_Social)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "razaoSocialEmitente"))
        )
        web.find_element(By.ID, ("enderecoEmitente")).send_keys(endereco)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "ufEmitente"))
        )
        Select(web.find_element(By.ID, "ufEmitente")).select_by_value(Uf)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "municipioEmitente"))
        )
        Select(web.find_element(By.ID, "municipioEmitente")
            ).select_by_value(Codigo_Municipio)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "cepEmitente"))
        )
        web.find_element(By.ID, ("cepEmitente")).send_keys(Cep)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "telefoneEmitente"))
        )
        web.find_element(By.ID, ("telefoneEmitente")).send_keys(Numero_Telefone)

        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "receita"))
        )
        Select(web.find_element(By.ID, "receita")
            ).select_by_value(RECEITA)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "tipoDocOrigem"))
        )
        Select(web.find_element(By.ID, "tipoDocOrigem")
            ).select_by_value('10')
        web.find_element(By.ID, ("numeroDocumentoOrigem")
                        ).send_keys(Numero_NFE)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "convenio"))
        )
        web.find_element(By.ID, ("convenio")
                        ).send_keys(CONVENIO)
        if INSCRITO == "optInscritoDest":
            WebDriverWait(web, 10).until(
                EC.presence_of_element_located((By.ID, "mesReferencia"))
            )
            Select(web.find_element(By.ID, "mesReferencia")
                ).select_by_value(Periodo_Ref)
            WebDriverWait(web, 10).until(
                EC.presence_of_element_located((By.ID, "anoReferencia"))
            )
            Select(web.find_element(By.ID, "anoReferencia")
                ).select_by_value(Ano_Ref)
            WebDriverWait(web, 10).until(
                EC.presence_of_element_located((By.ID, "dataVencimento"))
            )
            web.find_element(By.ID, ("dataVencimento")
                            ).send_keys(datavencimento)
            WebDriverWait(web, 10).until(
                EC.presence_of_element_located((By.ID, "valor"))
            )
            web.find_element(By.ID, ("valor")
                            ).send_keys(VALOR_TOTAL)

            WebDriverWait(web, 10).until(
                EC.presence_of_element_located((By.ID, "dataPagamento"))
            )
            web.find_element(By.ID, ("dataPagamento")
                            ).clear()
            WebDriverWait(web, 10).until(
                EC.presence_of_element_located((By.ID, "dataPagamento"))
            )
            sleep(0.2)
            web.find_element(By.ID, ("dataPagamento")
                            ).send_keys(datavencimento)
            WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, INSCRITO))
            )
            web.find_element(By.ID, (INSCRITO)
                            ).click()

            WebDriverWait(web, 10).until(
                    EC.presence_of_element_located((By.ID, "inscricaoEstadualDestinatario"))
                )
            web.find_element(By.ID, ("inscricaoEstadualDestinatario")
                                ).send_keys(IE)
        else:
            WebDriverWait(web, 10).until(
                EC.presence_of_element_located((By.ID, "dataVencimento"))
            )
            web.find_element(By.ID, ("dataVencimento")
                            ).send_keys(datavencimento)
            WebDriverWait(web, 10).until(
                EC.presence_of_element_located((By.ID, "valor"))
            )
            web.find_element(By.ID, ("valor")
                            ).send_keys(VALOR_TOTAL)

            WebDriverWait(web, 10).until(
                EC.presence_of_element_located((By.ID, "dataPagamento"))
            )
            web.find_element(By.ID, ("dataPagamento")
                            ).clear()
            WebDriverWait(web, 10).until(
                EC.presence_of_element_located((By.ID, "dataPagamento"))
            )
            web.find_element(By.ID, ("dataPagamento")
                            ).send_keys(datavencimento)
        


        try:
            while True:
                if not web.execute_script("return window.top.closed"):
                    time.sleep(1)
                else:
                    print("navegador fechado")
                    break
        except:
            print("OK")
    #PRONTO DIFAL E ST
    def estado_MS(self):
        # Ler arquivo xml
        xml_arq
        tree = ET.parse(xml_arq)
        root = tree.getroot()
        ns = {'nfe': 'http://www.portalfiscal.inf.br/nfe'}
        # salvar informaçoes em variaveis
        Cnpj = root.find('.//nfe:NFe/nfe:infNFe/nfe:emit/nfe:CNPJ', ns).text
        Razao_Social = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:xNome', ns).text
        endereco = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:enderEmit/nfe:xLgr', ns).text
        Uf = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:enderEmit/nfe:UF', ns).text
        Cep = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:enderEmit/nfe:CEP', ns).text
        Codigo_Municipio = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:enderEmit/nfe:cMun', ns).text
        Codigo_Municipio = Codigo_Municipio[2:]
        Numero_Telefone = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:enderEmit/nfe:fone', ns).text
        Numero_Telefone = Numero_Telefone[2:]
        
        # dados para emitir gnre por estado
        Numero_NFE = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:ide/nfe:nNF', ns).text
        Periodo_Ref = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:ide/nfe:dhEmi', ns).text
        valor_difal = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:total/nfe:ICMSTot/nfe:vICMSUFDest', ns).text
        Ano_Ref = Periodo_Ref[:4]
        #dados destinatario

        razao_dest = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:dest/nfe:xNome', ns).text
        codigo_munc_dest = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:dest/nfe:enderDest/nfe:cMun', ns).text
        chave = root.find(
            './/nfe:protNFe/nfe:infProt/nfe:chNFe', ns).text
        
        codigo_munc_dest = codigo_munc_dest[2:]
        Periodo_Ref = Periodo_Ref[5:7]


        chrome_options = Options()
        chrome_options.add_argument("--incognito")
        web = webdriver.Chrome(chrome_options=chrome_options)
        web.maximize_window()
        web.get("https://www.gnre.pe.gov.br:444/gnre/v/guia/index")


        Select(web.find_element(By.ID, "ufFavorecida")).select_by_value(uf_f)

        sleep(2)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "optGnreSimples"))
        )
        web.find_element(By.ID, ("optGnreSimples")).click()
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "optNaoInscrito"))
        )
        web.find_element(By.ID, ("optNaoInscrito")).click()
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "tipoCNPJ"))
        )
        web.find_element(By.ID, ("tipoCNPJ")).click()
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "documentoEmitente"))
        )
        web.find_element(By.ID, ("documentoEmitente")).send_keys(Cnpj)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "razaoSocialEmitente"))
        )
        web.find_element(By.ID, ("razaoSocialEmitente")).send_keys(Razao_Social)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "razaoSocialEmitente"))
        )
        web.find_element(By.ID, ("enderecoEmitente")).send_keys(endereco)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "ufEmitente"))
        )
        Select(web.find_element(By.ID, "ufEmitente")).select_by_value(Uf)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "municipioEmitente"))
        )
        Select(web.find_element(By.ID, "municipioEmitente")
            ).select_by_value(Codigo_Municipio)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "cepEmitente"))
        )
        web.find_element(By.ID, ("cepEmitente")).send_keys(Cep)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "telefoneEmitente"))
        )
        web.find_element(By.ID, ("telefoneEmitente")).send_keys(Numero_Telefone)

        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "receita"))
        )
        Select(web.find_element(By.ID, "receita")
            ).select_by_value(RECEITA)
        web.find_element(By.ID, ("convenio")
                        ).send_keys(CONVENIO)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "dataVencimento"))
        )
        sleep(0.2)
        web.find_element(By.ID, ("dataVencimento")
                        ).send_keys(datavencimento)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "valor"))
        )
        web.find_element(By.ID, ("valor")
                        ).send_keys(VALOR_TOTAL)
        
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, INSCRITO))
        )
        web.find_element(By.ID, (INSCRITO)
                        ).click()
        
        #SE FOR INSCRITO NA UF
  
        if INSCRITO == "optInscritoDest":
            WebDriverWait(web, 10).until(
                EC.presence_of_element_located((By.ID, "tipoDocOrigem"))
            )
            Select(web.find_element(By.ID, "tipoDocOrigem")
                ).select_by_value('10')
            web.find_element(By.ID, ("numeroDocumentoOrigem")
                            ).send_keys(Numero_NFE)
            WebDriverWait(web, 10).until(
                EC.presence_of_element_located((By.ID, "inscricaoEstadualDestinatario"))
            )
            web.find_element(By.ID, ("inscricaoEstadualDestinatario")
                            ).send_keys(IE)
            WebDriverWait(web, 10).until(
                EC.presence_of_element_located((By.ID, "produto"))
            )
            Select(web.find_element(By.ID, "produto")
                ).select_by_value("22")
        
        else:
            print(IDENTIFICAO)
            WebDriverWait(web, 10).until(
                EC.presence_of_element_located((By.ID, IDENTIFICAO))
            )
            web.find_element(By.ID, (IDENTIFICAO)
                            ).click()
            WebDriverWait(web, 10).until(
                EC.presence_of_element_located((By.ID, "documentoDestinatario"))
            )
            sleep(0.2)
            web.find_element(By.ID, ("documentoDestinatario")
                            ).send_keys(CPF_CNPJ_DESTINATARIO)
            WebDriverWait(web, 10).until(
                EC.presence_of_element_located((By.ID, "razaoSocialDestinatario"))
            )
            web.find_element(By.ID, ("razaoSocialDestinatario")
                            ).send_keys(razao_dest)
            WebDriverWait(web, 10).until(
                EC.presence_of_element_located((By.ID, "municipioDestinatario"))
            )
            Select(web.find_element(By.ID, "municipioDestinatario")
                ).select_by_value(codigo_munc_dest)
        
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "campoAdicional00"))
        )
        sleep(0.2)
        web.find_element(By.ID, ("campoAdicional00")
                        ).send_keys(chave)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "dataPagamento"))
        )
        web.find_element(By.ID, ("dataPagamento")
                        ).clear()
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "dataPagamento"))
        )
        
        web.find_element(By.ID, ("dataPagamento")
                        ).send_keys(datavencimento)
        


        try:
            while True:
                if not web.execute_script("return window.top.closed"):
                    time.sleep(1)
                else:
                    print("navegador fechado")
                    break
        except:
            print("OK")
    #PRONTO DIFAL E ST
    def estado_MT(self):
        # Ler arquivo xml
        xml_arq
        tree = ET.parse(xml_arq)
        root = tree.getroot()
        ns = {'nfe': 'http://www.portalfiscal.inf.br/nfe'}
        # salvar informaçoes em variaveis
        Cnpj = root.find('.//nfe:NFe/nfe:infNFe/nfe:emit/nfe:CNPJ', ns).text
        Razao_Social = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:xNome', ns).text
        endereco = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:enderEmit/nfe:xLgr', ns).text
        Uf = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:enderEmit/nfe:UF', ns).text
        Cep = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:enderEmit/nfe:CEP', ns).text
        Codigo_Municipio = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:enderEmit/nfe:cMun', ns).text
        Codigo_Municipio = Codigo_Municipio[2:]
        Numero_Telefone = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:enderEmit/nfe:fone', ns).text
        Numero_Telefone = Numero_Telefone[2:]
        # dados para emitir gnre por estado
        Numero_NFE = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:ide/nfe:nNF', ns).text
        Periodo_Ref = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:ide/nfe:dhEmi', ns).text
        valor_difal = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:total/nfe:ICMSTot/nfe:vICMSUFDest', ns).text
        Ano_Ref = Periodo_Ref[:4]
        #dados destinatario

        razao_dest = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:dest/nfe:xNome', ns).text
        codigo_munc_dest = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:dest/nfe:enderDest/nfe:cMun', ns).text
        chave = root.find(
            './/nfe:protNFe/nfe:infProt/nfe:chNFe', ns).text
        
        codigo_munc_dest = codigo_munc_dest[2:]
        Periodo_Ref = Periodo_Ref[5:7]

        print(Periodo_Ref)

        chrome_options = Options()
        chrome_options.add_argument("--incognito")
        web = webdriver.Chrome(chrome_options=chrome_options)
        web.maximize_window()
        web.get("https://www.gnre.pe.gov.br:444/gnre/v/guia/index")


        Select(web.find_element(By.ID, "ufFavorecida")).select_by_value(uf_f)

        sleep(2)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "optGnreSimples"))
        )
        web.find_element(By.ID, ("optGnreSimples")).click()
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "optNaoInscrito"))
        )
        web.find_element(By.ID, ("optNaoInscrito")).click()
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "tipoCNPJ"))
        )
        web.find_element(By.ID, ("tipoCNPJ")).click()
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "documentoEmitente"))
        )
        web.find_element(By.ID, ("documentoEmitente")).send_keys(Cnpj)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "razaoSocialEmitente"))
        )
        web.find_element(By.ID, ("razaoSocialEmitente")).send_keys(Razao_Social)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "razaoSocialEmitente"))
        )
        web.find_element(By.ID, ("enderecoEmitente")).send_keys(endereco)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "ufEmitente"))
        )
        Select(web.find_element(By.ID, "ufEmitente")).select_by_value(Uf)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "municipioEmitente"))
        )
        Select(web.find_element(By.ID, "municipioEmitente")
            ).select_by_value(Codigo_Municipio)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "cepEmitente"))
        )
        web.find_element(By.ID, ("cepEmitente")).send_keys(Cep)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "telefoneEmitente"))
        )
        web.find_element(By.ID, ("telefoneEmitente")).send_keys(Numero_Telefone)

        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "receita"))
        )
        Select(web.find_element(By.ID, "receita")
            ).select_by_value(RECEITA)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "tipoDocOrigem"))
        )
        Select(web.find_element(By.ID, "tipoDocOrigem")
            ).select_by_value('22')
        web.find_element(By.ID, ("numeroDocumentoOrigem")
                        ).send_keys(chave)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "mesReferencia"))
        )
        Select(web.find_element(By.ID, "mesReferencia")
            ).select_by_value(Periodo_Ref)

        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "anoReferencia"))
        )
        Select(web.find_element(By.ID, "anoReferencia")
            ).select_by_value(Ano_Ref)
        web.find_element(By.ID, ("convenio")
                        ).send_keys(CONVENIO)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "dataVencimento"))
        )
        sleep(0.2)
        web.find_element(By.ID, ("dataVencimento")
                        ).send_keys(datavencimento)
        

        if INSCRITO == 'optInscritoDest':
            WebDriverWait(web, 10).until(

                EC.presence_of_element_located((By.ID, INSCRITO))
            )
            web.find_element(By.ID, (INSCRITO)
                            ).click()
            WebDriverWait(web, 10).until(
                EC.presence_of_element_located((By.ID, "valor"))
            )
            web.find_element(By.ID, ("valor")
                        ).send_keys(VALOR_TOTAL)
            WebDriverWait(web, 10).until(
                EC.presence_of_element_located((By.ID, "inscricaoEstadualDestinatario"))
            )
            web.find_element(By.ID, ("inscricaoEstadualDestinatario")
                            ).send_keys(IE)
            WebDriverWait(web, 10).until(
                EC.presence_of_element_located((By.ID, "detalheReceita"))
            )
            Select(web.find_element(By.ID, "detalheReceita")
                ).select_by_value("000105")


        else:
            WebDriverWait(web, 10).until(
                EC.presence_of_element_located((By.ID, "tipoValorPrincipal"))
            )
            web.find_element(By.ID, ("tipoValorPrincipal")
                            ).click()
            WebDriverWait(web, 10).until(
                EC.presence_of_element_located((By.ID, "valor"))
            )
            web.find_element(By.ID, ("valor")
                            ).send_keys(VALOR_TOTAL)
            WebDriverWait(web, 10).until(
                EC.presence_of_element_located((By.ID, "detalheReceita"))
            )
            Select(web.find_element(By.ID, "detalheReceita")
                ).select_by_value("000055")

        

        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "dataPagamento"))
        )
        web.find_element(By.ID, ("dataPagamento")
                        ).clear()
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "dataPagamento"))
        )
        sleep(0.2)
        web.find_element(By.ID, ("dataPagamento")
                        ).send_keys(datavencimento)
        
        try:
            while True:
                if not web.execute_script("return window.top.closed"):
                    time.sleep(1)
                else:
                    print("navegador fechado")
                    break
        except:
            print("OK")
    #PRONTO DIFAL E ST
    def estado_PA(self):
        # Ler arquivo xml
        xml_arq
        tree = ET.parse(xml_arq)
        root = tree.getroot()
        ns = {'nfe': 'http://www.portalfiscal.inf.br/nfe'}
        # salvar informaçoes em variaveis
        Cnpj = root.find('.//nfe:NFe/nfe:infNFe/nfe:emit/nfe:CNPJ', ns).text
        Razao_Social = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:xNome', ns).text
        endereco = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:enderEmit/nfe:xLgr', ns).text
        Uf = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:enderEmit/nfe:UF', ns).text
        Cep = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:enderEmit/nfe:CEP', ns).text
        Codigo_Municipio = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:enderEmit/nfe:cMun', ns).text
        Codigo_Municipio = Codigo_Municipio[2:]
        Numero_Telefone = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:enderEmit/nfe:fone', ns).text
        Numero_Telefone = Numero_Telefone[2:]
        # dados para emitir gnre por estado
        Numero_NFE = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:ide/nfe:nNF', ns).text
        Periodo_Ref = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:ide/nfe:dhEmi', ns).text
        valor_difal = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:total/nfe:ICMSTot/nfe:vICMSUFDest', ns).text
        Ano_Ref = Periodo_Ref[:4]
        #dados destinatario

        razao_dest = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:dest/nfe:xNome', ns).text
        codigo_munc_dest = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:dest/nfe:enderDest/nfe:cMun', ns).text
        chave = root.find(
            './/nfe:protNFe/nfe:infProt/nfe:chNFe', ns).text
        
        codigo_munc_dest = codigo_munc_dest[2:]
        Periodo_Ref = Periodo_Ref[5:7]

        print(Periodo_Ref)

        chrome_options = Options()
        chrome_options.add_argument("--incognito")
        web = webdriver.Chrome(chrome_options=chrome_options)
        web.maximize_window()
        web.get("https://www.gnre.pe.gov.br:444/gnre/v/guia/index")


        Select(web.find_element(By.ID, "ufFavorecida")).select_by_value(uf_f)

        sleep(2)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "optGnreSimples"))
        )
        web.find_element(By.ID, ("optGnreSimples")).click()
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "optNaoInscrito"))
        )
        web.find_element(By.ID, ("optNaoInscrito")).click()
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "tipoCNPJ"))
        )
        web.find_element(By.ID, ("tipoCNPJ")).click()
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "documentoEmitente"))
        )
        web.find_element(By.ID, ("documentoEmitente")).send_keys(Cnpj)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "razaoSocialEmitente"))
        )
        web.find_element(By.ID, ("razaoSocialEmitente")).send_keys(Razao_Social)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "razaoSocialEmitente"))
        )
        web.find_element(By.ID, ("enderecoEmitente")).send_keys(endereco)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "ufEmitente"))
        )
        Select(web.find_element(By.ID, "ufEmitente")).select_by_value(Uf)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "municipioEmitente"))
        )
        Select(web.find_element(By.ID, "municipioEmitente")
            ).select_by_value(Codigo_Municipio)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "cepEmitente"))
        )
        web.find_element(By.ID, ("cepEmitente")).send_keys(Cep)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "telefoneEmitente"))
        )
        web.find_element(By.ID, ("telefoneEmitente")).send_keys(Numero_Telefone)

        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "receita"))
        )
        Select(web.find_element(By.ID, "receita")
            ).select_by_value(RECEITA)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "tipoDocOrigem"))
        )
        Select(web.find_element(By.ID, "tipoDocOrigem")
            ).select_by_value('10')
        web.find_element(By.ID, ("numeroDocumentoOrigem")
                        ).send_keys(Numero_NFE)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "mesReferencia"))
        )
        Select(web.find_element(By.ID, "mesReferencia")
            ).select_by_value(Periodo_Ref)

        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "anoReferencia"))
        )
        Select(web.find_element(By.ID, "anoReferencia")
            ).select_by_value(Ano_Ref)
        web.find_element(By.ID, ("convenio")
                        ).send_keys(CONVENIO)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "dataVencimento"))
        )
        web.find_element(By.ID, ("dataVencimento")
                        ).send_keys(datavencimento)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "tipoValorPrincipal"))
        )
        web.find_element(By.ID, ("tipoValorPrincipal")
                        ).click()
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "valor"))
        )
        web.find_element(By.ID, ("valor")
                        ).send_keys(VALOR_TOTAL)
        
        WebDriverWait(web, 10).until(

            EC.presence_of_element_located((By.ID, INSCRITO))
        )
        web.find_element(By.ID, (INSCRITO)
                        ).click()
        
        if INSCRITO == "optInscritoDest":
            WebDriverWait(web, 10).until(
                EC.presence_of_element_located((By.ID, "inscricaoEstadualDestinatario"))
            )
            web.find_element(By.ID, ("inscricaoEstadualDestinatario")
                            ).send_keys(IE)
 
        
        else:
            print(IDENTIFICAO)
            WebDriverWait(web, 10).until(
                EC.presence_of_element_located((By.ID, IDENTIFICAO))
            )
            web.find_element(By.ID, (IDENTIFICAO)
                            ).click()
            WebDriverWait(web, 10).until(
                EC.presence_of_element_located((By.ID, "documentoDestinatario"))
            )
            sleep(0.2)
            web.find_element(By.ID, ("documentoDestinatario")
                            ).send_keys(CPF_CNPJ_DESTINATARIO)
            WebDriverWait(web, 10).until(
                EC.presence_of_element_located((By.ID, "razaoSocialDestinatario"))
            )
            web.find_element(By.ID, ("razaoSocialDestinatario")
                            ).send_keys(razao_dest)
            WebDriverWait(web, 10).until(
                EC.presence_of_element_located((By.ID, "municipioDestinatario"))
            )
            Select(web.find_element(By.ID, "municipioDestinatario")
                ).select_by_value(codigo_munc_dest)
    
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "dataPagamento"))
        )
        web.find_element(By.ID, ("dataPagamento")
                        ).clear()
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "dataPagamento"))
        )
        web.find_element(By.ID, ("dataPagamento")
                        ).send_keys(datavencimento)
        


        try:
            while True:
                if not web.execute_script("return window.top.closed"):
                    time.sleep(1)
                else:
                    print("navegador fechado")
                    break
        except:
            print("OK")
    #PRONTO DIFAL E ST
    def estado_PB(self):
        # Ler arquivo xml
        xml_arq
        tree = ET.parse(xml_arq)
        root = tree.getroot()
        ns = {'nfe': 'http://www.portalfiscal.inf.br/nfe'}
        # salvar informaçoes em variaveis
        Cnpj = root.find('.//nfe:NFe/nfe:infNFe/nfe:emit/nfe:CNPJ', ns).text
        Razao_Social = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:xNome', ns).text
        endereco = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:enderEmit/nfe:xLgr', ns).text
        Uf = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:enderEmit/nfe:UF', ns).text
        Cep = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:enderEmit/nfe:CEP', ns).text
        Codigo_Municipio = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:enderEmit/nfe:cMun', ns).text
        Codigo_Municipio = Codigo_Municipio[2:]
        Numero_Telefone = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:enderEmit/nfe:fone', ns).text
        Numero_Telefone = Numero_Telefone[2:]
        # dados para emitir gnre por estado
        Numero_NFE = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:ide/nfe:nNF', ns).text
        Periodo_Ref = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:ide/nfe:dhEmi', ns).text
        valor_difal = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:total/nfe:ICMSTot/nfe:vICMSUFDest', ns).text
        Ano_Ref = Periodo_Ref[:4]
        #dados destinatario

        razao_dest = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:dest/nfe:xNome', ns).text
        codigo_munc_dest = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:dest/nfe:enderDest/nfe:cMun', ns).text
        chave = root.find(
            './/nfe:protNFe/nfe:infProt/nfe:chNFe', ns).text
        
        codigo_munc_dest = codigo_munc_dest[2:]
        Periodo_Ref = Periodo_Ref[5:7]

        print(Periodo_Ref)

        chrome_options = Options()
        chrome_options.add_argument("--incognito")
        web = webdriver.Chrome(chrome_options=chrome_options)
        web.maximize_window()
        web.get("https://www.gnre.pe.gov.br:444/gnre/v/guia/index")


        Select(web.find_element(By.ID, "ufFavorecida")).select_by_value(uf_f)

        sleep(2)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "optGnreSimples"))
        )
        web.find_element(By.ID, ("optGnreSimples")).click()
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "optNaoInscrito"))
        )
        web.find_element(By.ID, ("optNaoInscrito")).click()
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "tipoCNPJ"))
        )
        web.find_element(By.ID, ("tipoCNPJ")).click()
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "documentoEmitente"))
        )
        web.find_element(By.ID, ("documentoEmitente")).send_keys(Cnpj)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "razaoSocialEmitente"))
        )
        web.find_element(By.ID, ("razaoSocialEmitente")).send_keys(Razao_Social)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "razaoSocialEmitente"))
        )
        web.find_element(By.ID, ("enderecoEmitente")).send_keys(endereco)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "ufEmitente"))
        )
        Select(web.find_element(By.ID, "ufEmitente")).select_by_value(Uf)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "municipioEmitente"))
        )
        Select(web.find_element(By.ID, "municipioEmitente")
            ).select_by_value(Codigo_Municipio)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "cepEmitente"))
        )
        web.find_element(By.ID, ("cepEmitente")).send_keys(Cep)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "telefoneEmitente"))
        )
        web.find_element(By.ID, ("telefoneEmitente")).send_keys(Numero_Telefone)

        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "receita"))
        )
        Select(web.find_element(By.ID, "receita")
            ).select_by_value(RECEITA)
        
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "mesReferencia"))
        )
        Select(web.find_element(By.ID, "mesReferencia")
            ).select_by_value(Periodo_Ref)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "anoReferencia"))
        )
        Select(web.find_element(By.ID, "anoReferencia")
            ).select_by_value(Ano_Ref)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "convenio"))
        )
        web.find_element(By.ID, ("convenio")
                        ).send_keys(CONVENIO)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "dataVencimento"))
        )
        web.find_element(By.ID, ("dataVencimento")
                        ).send_keys(datavencimento)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "valor"))
        )
        web.find_element(By.ID, ("valor")
                        ).send_keys(VALOR_TOTAL)
        
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "campoAdicional00"))
        )
        web.find_element(By.ID, ("campoAdicional00")
                        ).send_keys(chave)



        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "dataPagamento"))
        )

        web.find_element(By.ID, ("dataPagamento")
                        ).clear()
        
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "dataPagamento"))
        )
        web.find_element(By.ID, ("dataPagamento")
                        ).send_keys(datavencimento)
        
        try:
            while True:
                if not web.execute_script("return window.top.closed"):
                    time.sleep(1)
                else:
                    print("navegador fechado")
                    break
        except:
            print("OK")
    #PRONTO DIFAL E ST
    def estado_PE(self):
        # Ler arquivo xml
        xml_arq
        tree = ET.parse(xml_arq)
        root = tree.getroot()
        ns = {'nfe': 'http://www.portalfiscal.inf.br/nfe'}
        # salvar informaçoes em variaveis
        Cnpj = root.find('.//nfe:NFe/nfe:infNFe/nfe:emit/nfe:CNPJ', ns).text
        Razao_Social = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:xNome', ns).text
        endereco = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:enderEmit/nfe:xLgr', ns).text
        Uf = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:enderEmit/nfe:UF', ns).text
        Cep = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:enderEmit/nfe:CEP', ns).text
        Codigo_Municipio = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:enderEmit/nfe:cMun', ns).text
        Codigo_Municipio = Codigo_Municipio[2:]
        Numero_Telefone = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:enderEmit/nfe:fone', ns).text
        Numero_Telefone = Numero_Telefone[2:]
        
        # dados para emitir gnre por estado
        Numero_NFE = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:ide/nfe:nNF', ns).text
        Periodo_Ref = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:ide/nfe:dhEmi', ns).text
        valor_difal = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:total/nfe:ICMSTot/nfe:vICMSUFDest', ns).text
        Ano_Ref = Periodo_Ref[:4]
        #dados destinatario

        razao_dest = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:dest/nfe:xNome', ns).text
        codigo_munc_dest = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:dest/nfe:enderDest/nfe:cMun', ns).text
        chave = root.find(
            './/nfe:protNFe/nfe:infProt/nfe:chNFe', ns).text
        
        codigo_munc_dest = codigo_munc_dest[2:]
        Periodo_Ref = Periodo_Ref[5:7]


        chrome_options = Options()
        chrome_options.add_argument("--incognito")
        web = webdriver.Chrome(chrome_options=chrome_options)
        web.maximize_window()
        web.get("https://www.gnre.pe.gov.br:444/gnre/v/guia/index")


        Select(web.find_element(By.ID, "ufFavorecida")).select_by_value(uf_f)

        sleep(2)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "optGnreSimples"))
        )
        web.find_element(By.ID, ("optGnreSimples")).click()
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "optNaoInscrito"))
        )
        web.find_element(By.ID, ("optNaoInscrito")).click()
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "tipoCNPJ"))
        )
        web.find_element(By.ID, ("tipoCNPJ")).click()
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "documentoEmitente"))
        )
        web.find_element(By.ID, ("documentoEmitente")).send_keys(Cnpj)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "razaoSocialEmitente"))
        )
        web.find_element(By.ID, ("razaoSocialEmitente")).send_keys(Razao_Social)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "razaoSocialEmitente"))
        )
        web.find_element(By.ID, ("enderecoEmitente")).send_keys(endereco)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "ufEmitente"))
        )
        Select(web.find_element(By.ID, "ufEmitente")).select_by_value(Uf)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "municipioEmitente"))
        )
        Select(web.find_element(By.ID, "municipioEmitente")
            ).select_by_value(Codigo_Municipio)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "cepEmitente"))
        )
        web.find_element(By.ID, ("cepEmitente")).send_keys(Cep)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "telefoneEmitente"))
        )
        web.find_element(By.ID, ("telefoneEmitente")).send_keys(Numero_Telefone)

        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "receita"))
        )
        Select(web.find_element(By.ID, "receita")
            ).select_by_value(RECEITA)
        
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "dataVencimento"))
        )
        sleep(0.25)
        web.find_element(By.ID, ("dataVencimento")
                        ).send_keys(datavencimento)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "valor"))
        )
        web.find_element(By.ID, ("valor")
                        ).send_keys(VALOR_TOTAL)
        
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, INSCRITO))
        )
        web.find_element(By.ID, (INSCRITO)
                        ).click()
        #SE FOR INSCRITO NA UF
        if INSCRITO == "optInscritoDest":
            web.find_element(By.ID, ("convenio")
                        ).send_keys(CONVENIO)
            WebDriverWait(web, 10).until(
                EC.presence_of_element_located((By.ID, "inscricaoEstadualDestinatario"))
            )
            web.find_element(By.ID, ("inscricaoEstadualDestinatario")
                            ).send_keys(IE)
            WebDriverWait(web, 10).until(
                EC.presence_of_element_located((By.ID, "produto"))
            )
            Select(web.find_element(By.ID, "produto")
                ).select_by_value("22")
            
            WebDriverWait(web, 10).until(
                EC.presence_of_element_located((By.ID, "tipoDocOrigem"))
            )
            Select(web.find_element(By.ID, "tipoDocOrigem")
                ).select_by_value('22')
            web.find_element(By.ID, ("numeroDocumentoOrigem")
                            ).send_keys(chave)
        else:
            WebDriverWait(web, 10).until(
                EC.presence_of_element_located((By.ID, "tipoDocOrigem"))
            )
            Select(web.find_element(By.ID, "tipoDocOrigem")
                ).select_by_value('24')
            web.find_element(By.ID, ("numeroDocumentoOrigem")
                            ).send_keys(chave)
            print(IDENTIFICAO)
            WebDriverWait(web, 10).until(
                EC.presence_of_element_located((By.ID, IDENTIFICAO))
            )
            web.find_element(By.ID, (IDENTIFICAO)
                            ).click()
            WebDriverWait(web, 10).until(
                EC.presence_of_element_located((By.ID, "documentoDestinatario"))
            )
            sleep(0.2)
            web.find_element(By.ID, ("documentoDestinatario")
                            ).send_keys(CPF_CNPJ_DESTINATARIO)
            WebDriverWait(web, 10).until(
                EC.presence_of_element_located((By.ID, "razaoSocialDestinatario"))
            )
            web.find_element(By.ID, ("razaoSocialDestinatario")
                            ).send_keys(razao_dest)
            WebDriverWait(web, 10).until(
                EC.presence_of_element_located((By.ID, "municipioDestinatario"))
            )
            Select(web.find_element(By.ID, "municipioDestinatario")
                ).select_by_value(codigo_munc_dest)
        
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "dataPagamento"))
        )
        web.find_element(By.ID, ("dataPagamento")
                        ).clear()
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "dataPagamento"))
        )
        
        web.find_element(By.ID, ("dataPagamento")
                        ).send_keys(datavencimento)

        
        try:
            while True:
                if not web.execute_script("return window.top.closed"):
                    time.sleep(1)
                else:
                    print("navegador fechado")
                    break
        except:
            print("OK")
    #PRONTO DIFAL E ST
    def estado_PI(self):
        # Ler arquivo xml
        xml_arq
        tree = ET.parse(xml_arq)
        root = tree.getroot()
        ns = {'nfe': 'http://www.portalfiscal.inf.br/nfe'}
        # salvar informaçoes em variaveis
        Cnpj = root.find('.//nfe:NFe/nfe:infNFe/nfe:emit/nfe:CNPJ', ns).text
        Razao_Social = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:xNome', ns).text
        endereco = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:enderEmit/nfe:xLgr', ns).text
        Uf = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:enderEmit/nfe:UF', ns).text
        Cep = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:enderEmit/nfe:CEP', ns).text
        Codigo_Municipio = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:enderEmit/nfe:cMun', ns).text
        Codigo_Municipio = Codigo_Municipio[2:]
        Numero_Telefone = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:enderEmit/nfe:fone', ns).text
        Numero_Telefone = Numero_Telefone[2:]
        # dados para emitir gnre por estado
        Numero_NFE = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:ide/nfe:nNF', ns).text
        Periodo_Ref = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:ide/nfe:dhEmi', ns).text
        valor_difal = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:total/nfe:ICMSTot/nfe:vICMSUFDest', ns).text
        Ano_Ref = Periodo_Ref[:4]
        #dados destinatario

        razao_dest = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:dest/nfe:xNome', ns).text
        codigo_munc_dest = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:dest/nfe:enderDest/nfe:cMun', ns).text
        chave = root.find(
            './/nfe:protNFe/nfe:infProt/nfe:chNFe', ns).text
        
        codigo_munc_dest = codigo_munc_dest[2:]
        Periodo_Ref = Periodo_Ref[5:7]

        print(Periodo_Ref)

        chrome_options = Options()
        chrome_options.add_argument("--incognito")
        web = webdriver.Chrome(chrome_options=chrome_options)
        web.maximize_window()
        web.get("https://www.gnre.pe.gov.br:444/gnre/v/guia/index")


        Select(web.find_element(By.ID, "ufFavorecida")).select_by_value(uf_f)

        sleep(2)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "optGnreSimples"))
        )
        web.find_element(By.ID, ("optGnreSimples")).click()
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "optNaoInscrito"))
        )
        web.find_element(By.ID, ("optNaoInscrito")).click()
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "tipoCNPJ"))
        )
        web.find_element(By.ID, ("tipoCNPJ")).click()
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "documentoEmitente"))
        )
        web.find_element(By.ID, ("documentoEmitente")).send_keys(Cnpj)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "razaoSocialEmitente"))
        )
        web.find_element(By.ID, ("razaoSocialEmitente")).send_keys(Razao_Social)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "razaoSocialEmitente"))
        )
        web.find_element(By.ID, ("enderecoEmitente")).send_keys(endereco)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "ufEmitente"))
        )
        Select(web.find_element(By.ID, "ufEmitente")).select_by_value(Uf)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "municipioEmitente"))
        )
        Select(web.find_element(By.ID, "municipioEmitente")
            ).select_by_value(Codigo_Municipio)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "cepEmitente"))
        )
        web.find_element(By.ID, ("cepEmitente")).send_keys(Cep)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "telefoneEmitente"))
        )
        web.find_element(By.ID, ("telefoneEmitente")).send_keys(Numero_Telefone)

        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "receita"))
        )
        Select(web.find_element(By.ID, "receita")
            ).select_by_value(RECEITA)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "tipoDocOrigem"))
        )
        Select(web.find_element(By.ID, "tipoDocOrigem")
            ).select_by_value('10')
        web.find_element(By.ID, ("numeroDocumentoOrigem")
                        ).send_keys(Numero_NFE)

        web.find_element(By.ID, ("convenio")
                        ).send_keys(CONVENIO)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "dataVencimento"))
        )
        web.find_element(By.ID, ("dataVencimento")
                        ).send_keys(datavencimento)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "tipoValorPrincipal"))
        )
        web.find_element(By.ID, ("tipoValorPrincipal")
                        ).click()
        
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "valor"))
        )
        web.find_element(By.ID, ("valor")
                        ).send_keys(VALOR_TOTAL)
        
        WebDriverWait(web, 10).until(

            EC.presence_of_element_located((By.ID, INSCRITO))
        )
        web.find_element(By.ID, (INSCRITO)
                        ).click()
        
        #SE FOR INSCRITO NA UF
  
        if INSCRITO == "optInscritoDest":
            WebDriverWait(web, 10).until(
                EC.presence_of_element_located((By.ID, "inscricaoEstadualDestinatario"))
            )
            web.find_element(By.ID, ("inscricaoEstadualDestinatario")
                            ).send_keys(IE)
            WebDriverWait(web, 10).until(
                EC.presence_of_element_located((By.ID, "produto"))
            )
            Select(web.find_element(By.ID, "produto")
                ).select_by_value("22")
        else:
            WebDriverWait(web, 10).until(
                EC.presence_of_element_located((By.ID, IDENTIFICAO))
            )
            web.find_element(By.ID, (IDENTIFICAO)
                            ).click()
            
            WebDriverWait(web, 10).until(
                EC.presence_of_element_located((By.ID, "documentoDestinatario"))
            )
            web.find_element(By.ID, ("documentoDestinatario")
                            ).send_keys(CPF_CNPJ_DESTINATARIO)
            WebDriverWait(web, 10).until(
                EC.presence_of_element_located((By.ID, "razaoSocialDestinatario"))
            )
            web.find_element(By.ID, ("razaoSocialDestinatario")
                            ).send_keys(razao_dest)
            WebDriverWait(web, 10).until(
                EC.presence_of_element_located((By.ID, "municipioDestinatario"))
            )
            Select(web.find_element(By.ID, "municipioDestinatario")
                ).select_by_value(codigo_munc_dest)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "dataPagamento"))
        )
        web.find_element(By.ID, ("dataPagamento")
                        ).clear()
        
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "dataPagamento"))
        )
        web.find_element(By.ID, ("dataPagamento")
                        ).send_keys(datavencimento)
        try:
            while True:
                if not web.execute_script("return window.top.closed"):
                    time.sleep(1)
                else:
                    print("navegador fechado")
                    break
        except:
            print("OK")
    #PRONTO DIFAL E ST
    def estado_PR(self):
        # Ler arquivo xml
        xml_arq
        tree = ET.parse(xml_arq)
        root = tree.getroot()
        ns = {'nfe': 'http://www.portalfiscal.inf.br/nfe'}
        # salvar informaçoes em variaveis
        Cnpj = root.find('.//nfe:NFe/nfe:infNFe/nfe:emit/nfe:CNPJ', ns).text
        Razao_Social = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:xNome', ns).text
        endereco = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:enderEmit/nfe:xLgr', ns).text
        Uf = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:enderEmit/nfe:UF', ns).text
        Cep = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:enderEmit/nfe:CEP', ns).text
        Codigo_Municipio = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:enderEmit/nfe:cMun', ns).text
        Codigo_Municipio = Codigo_Municipio[2:]
        Numero_Telefone = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:enderEmit/nfe:fone', ns).text
        Numero_Telefone = Numero_Telefone[2:]
        # dados para emitir gnre por estado
        Numero_NFE = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:ide/nfe:nNF', ns).text
        Periodo_Ref = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:ide/nfe:dhEmi', ns).text
        valor_difal = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:total/nfe:ICMSTot/nfe:vICMSUFDest', ns).text
        Ano_Ref = Periodo_Ref[:4]
        #dados destinatario

        razao_dest = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:dest/nfe:xNome', ns).text
        codigo_munc_dest = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:dest/nfe:enderDest/nfe:cMun', ns).text
        chave = root.find(
            './/nfe:protNFe/nfe:infProt/nfe:chNFe', ns).text

        chrome_options = Options()
        chrome_options.add_argument("--incognito")
        web = webdriver.Chrome(chrome_options=chrome_options)
        web.maximize_window()
        web.get("https://www.gnre.pe.gov.br:444/gnre/v/guia/index")


        Select(web.find_element(By.ID, "ufFavorecida")).select_by_value(uf_f)

        sleep(2)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "optGnreSimples"))
        )
        web.find_element(By.ID, ("optGnreSimples")).click()
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "optNaoInscrito"))
        )
        web.find_element(By.ID, ("optNaoInscrito")).click()
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "tipoCNPJ"))
        )
        web.find_element(By.ID, ("tipoCNPJ")).click()
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "documentoEmitente"))
        )
        web.find_element(By.ID, ("documentoEmitente")).send_keys(Cnpj)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "razaoSocialEmitente"))
        )
        web.find_element(By.ID, ("razaoSocialEmitente")).send_keys(Razao_Social)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "razaoSocialEmitente"))
        )
        web.find_element(By.ID, ("enderecoEmitente")).send_keys(endereco)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "ufEmitente"))
        )
        Select(web.find_element(By.ID, "ufEmitente")).select_by_value(Uf)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "municipioEmitente"))
        )
        Select(web.find_element(By.ID, "municipioEmitente")
            ).select_by_value(Codigo_Municipio)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "cepEmitente"))
        )
        web.find_element(By.ID, ("cepEmitente")).send_keys(Cep)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "telefoneEmitente"))
        )
        web.find_element(By.ID, ("telefoneEmitente")).send_keys(Numero_Telefone)

        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "receita"))
        )
        Select(web.find_element(By.ID, "receita")
            ).select_by_value(RECEITA)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "tipoDocOrigem"))
        )
        Select(web.find_element(By.ID, "tipoDocOrigem")
            ).select_by_value('10')
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "numeroDocumentoOrigem"))
        )
        web.find_element(By.ID, ("numeroDocumentoOrigem")).send_keys(Numero_NFE)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "convenio"))
        )
        web.find_element(By.ID, ("convenio")).send_keys(CONVENIO)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "dataVencimento"))
        )
        web.find_element(By.ID, ("dataVencimento")).send_keys(datavencimento)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "valor"))
        )
        web.find_element(By.ID, ("valor")).send_keys(VALOR_TOTAL)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "campoAdicional00"))
        )
        web.find_element(By.ID, ("campoAdicional00")).send_keys(chave)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "dataPagamento"))
        )
        web.find_element(By.ID, ("dataPagamento")).clear()
        sleep(0.2)
        web.find_element(By.ID, ("dataPagamento")).send_keys(datavencimento)
        
        
        try:
            while True:
                if not web.execute_script("return window.top.closed"):
                    time.sleep(1)
                else:
                    print("navegador fechado")
                    break
        except:
            print("OK")
    #PRONTO DIFAL E ST
    def estado_RJ(self):
        # Ler arquivo xml
        xml_arq
        tree = ET.parse(xml_arq)
        root = tree.getroot()
        ns = {'nfe': 'http://www.portalfiscal.inf.br/nfe'}
        # salvar informaçoes em variaveis
        Cnpj = root.find('.//nfe:NFe/nfe:infNFe/nfe:emit/nfe:CNPJ', ns).text
        Razao_Social = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:xNome', ns).text
        endereco = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:enderEmit/nfe:xLgr', ns).text
        Uf = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:enderEmit/nfe:UF', ns).text
        Cep = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:enderEmit/nfe:CEP', ns).text
        Codigo_Municipio = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:enderEmit/nfe:cMun', ns).text
        Codigo_Municipio = Codigo_Municipio[2:]
        Numero_Telefone = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:enderEmit/nfe:fone', ns).text
        Numero_Telefone = Numero_Telefone[2:]
        # dados para emitir gnre por estado
        Numero_NFE = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:ide/nfe:nNF', ns).text
        Periodo_Ref = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:ide/nfe:dhEmi', ns).text
        valor_difal = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:total/nfe:ICMSTot/nfe:vICMSUFDest', ns).text
        print(Periodo_Ref)
        Ano_Ref = Periodo_Ref[:4]
        Emissao_nota = Periodo_Ref[8:10] +'/' + Periodo_Ref[5:7] + '/' + Periodo_Ref[:4]
        print(Emissao_nota)

        #dados destinatario

        razao_dest = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:dest/nfe:xNome', ns).text
        codigo_munc_dest = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:dest/nfe:enderDest/nfe:cMun', ns).text
        chave = root.find(
            './/nfe:protNFe/nfe:infProt/nfe:chNFe', ns).text
        
        codigo_munc_dest = codigo_munc_dest[2:]
        Periodo_Ref = Periodo_Ref[5:7]
        chrome_options = Options()
        chrome_options.add_argument("--incognito")
        web = webdriver.Chrome(chrome_options=chrome_options)
        web.maximize_window()
        web.get("https://www.gnre.pe.gov.br:444/gnre/v/guia/index")


        Select(web.find_element(By.ID, "ufFavorecida")).select_by_value(uf_f)

        sleep(2)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "optGnreSimples"))
        )
        web.find_element(By.ID, ("optGnreSimples")).click()
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "optNaoInscrito"))
        )
        web.find_element(By.ID, ("optNaoInscrito")).click()
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "tipoCNPJ"))
        )
        web.find_element(By.ID, ("tipoCNPJ")).click()
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "documentoEmitente"))
        )
        web.find_element(By.ID, ("documentoEmitente")).send_keys(Cnpj)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "razaoSocialEmitente"))
        )
        web.find_element(By.ID, ("razaoSocialEmitente")).send_keys(Razao_Social)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "razaoSocialEmitente"))
        )
        web.find_element(By.ID, ("enderecoEmitente")).send_keys(endereco)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "ufEmitente"))
        )
        Select(web.find_element(By.ID, "ufEmitente")).select_by_value(Uf)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "municipioEmitente"))
        )
        Select(web.find_element(By.ID, "municipioEmitente")
            ).select_by_value(Codigo_Municipio)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "cepEmitente"))
        )
        web.find_element(By.ID, ("cepEmitente")).send_keys(Cep)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "telefoneEmitente"))
        )
        web.find_element(By.ID, ("telefoneEmitente")).send_keys(Numero_Telefone)

        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "receita"))
        )
        Select(web.find_element(By.ID, "receita")
            ).select_by_value(RECEITA)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "produto"))
        )
        Select(web.find_element(By.ID, "produto")
            ).select_by_value('90')
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "tipoDocOrigem"))
        )
        Select(web.find_element(By.ID, "tipoDocOrigem")
            ).select_by_value('24')
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "numeroDocumentoOrigem"))
        )
        web.find_element(By.ID, ("numeroDocumentoOrigem")).send_keys(chave)

        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "dataVencimento"))
        )
        web.find_element(By.ID, ("dataVencimento")).send_keys(datavencimento)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "valor"))
        )
        web.find_element(By.ID, ("valor")).send_keys(VALOR_TOTAL)
        WebDriverWait(web, 10).until(

            EC.presence_of_element_located((By.ID, INSCRITO))
        )
        web.find_element(By.ID, (INSCRITO)
                        ).click()
        #SE FOR INSCRITO NA UF
  
        if INSCRITO == "optInscritoDest":
            WebDriverWait(web, 10).until(
                EC.presence_of_element_located((By.ID, "inscricaoEstadualDestinatario"))
            )
            web.find_element(By.ID, ("inscricaoEstadualDestinatario")
                            ).send_keys(IE)
        else:
            WebDriverWait(web, 10).until(
                EC.presence_of_element_located((By.ID, IDENTIFICAO))
            )
            web.find_element(By.ID, (IDENTIFICAO)
                            ).click()
            
            WebDriverWait(web, 10).until(
                EC.presence_of_element_located((By.ID, "documentoDestinatario"))
            )
            web.find_element(By.ID, ("documentoDestinatario")
                            ).send_keys(CPF_CNPJ_DESTINATARIO)
            WebDriverWait(web, 10).until(
                EC.presence_of_element_located((By.ID, "razaoSocialDestinatario"))
            )
            web.find_element(By.ID, ("razaoSocialDestinatario")
                            ).send_keys(razao_dest)
            WebDriverWait(web, 10).until(
                EC.presence_of_element_located((By.ID, "municipioDestinatario"))
            )
            Select(web.find_element(By.ID, "municipioDestinatario")
                ).select_by_value(codigo_munc_dest)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "campoAdicional00"))
        )
        web.find_element(By.ID, ("campoAdicional00")
                        ).send_keys(Emissao_nota)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "dataPagamento"))
        )
        web.find_element(By.ID, ("dataPagamento")
                        ).clear()
        sleep(0.2)
        web.find_element(By.ID, ("dataPagamento")
                        ).send_keys(datavencimento)



        try:
            while True:
                if not web.execute_script("return window.top.closed"):
                    time.sleep(1)
                else:
                    print("navegador fechado")
                    break
        except:
            print("OK")
    #PRONTO DIFAL E ST
    def estado_RN(self):
          # Ler arquivo xml
        xml_arq
        tree = ET.parse(xml_arq)
        root = tree.getroot()
        ns = {'nfe': 'http://www.portalfiscal.inf.br/nfe'}
        # salvar informaçoes em variaveis
        Cnpj = root.find('.//nfe:NFe/nfe:infNFe/nfe:emit/nfe:CNPJ', ns).text
        Razao_Social = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:xNome', ns).text
        endereco = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:enderEmit/nfe:xLgr', ns).text
        Uf = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:enderEmit/nfe:UF', ns).text
        Cep = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:enderEmit/nfe:CEP', ns).text
        Codigo_Municipio = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:enderEmit/nfe:cMun', ns).text
        Codigo_Municipio = Codigo_Municipio[2:]
        Numero_Telefone = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:enderEmit/nfe:fone', ns).text
        Numero_Telefone = Numero_Telefone[2:]
        
        # dados para emitir gnre por estado
        Numero_NFE = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:ide/nfe:nNF', ns).text
        Periodo_Ref = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:ide/nfe:dhEmi', ns).text
        valor_difal = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:total/nfe:ICMSTot/nfe:vICMSUFDest', ns).text
        Ano_Ref = Periodo_Ref[:4]
        #dados destinatario

        razao_dest = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:dest/nfe:xNome', ns).text
        codigo_munc_dest = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:dest/nfe:enderDest/nfe:cMun', ns).text
        chave = root.find(
            './/nfe:protNFe/nfe:infProt/nfe:chNFe', ns).text
        
        codigo_munc_dest = codigo_munc_dest[2:]
        Periodo_Ref = Periodo_Ref[5:7]


        chrome_options = Options()
        chrome_options.add_argument("--incognito")
        web = webdriver.Chrome(chrome_options=chrome_options)
        web.maximize_window()
        web.get("https://www.gnre.pe.gov.br:444/gnre/v/guia/index")


        Select(web.find_element(By.ID, "ufFavorecida")).select_by_value(uf_f)

        sleep(2)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "optGnreSimples"))
        )
        web.find_element(By.ID, ("optGnreSimples")).click()
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "optNaoInscrito"))
        )
        web.find_element(By.ID, ("optNaoInscrito")).click()
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "tipoCNPJ"))
        )
        web.find_element(By.ID, ("tipoCNPJ")).click()
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "documentoEmitente"))
        )
        web.find_element(By.ID, ("documentoEmitente")).send_keys(Cnpj)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "razaoSocialEmitente"))
        )
        web.find_element(By.ID, ("razaoSocialEmitente")).send_keys(Razao_Social)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "razaoSocialEmitente"))
        )
        web.find_element(By.ID, ("enderecoEmitente")).send_keys(endereco)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "ufEmitente"))
        )
        Select(web.find_element(By.ID, "ufEmitente")).select_by_value(Uf)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "municipioEmitente"))
        )
        Select(web.find_element(By.ID, "municipioEmitente")
            ).select_by_value(Codigo_Municipio)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "cepEmitente"))
        )
        web.find_element(By.ID, ("cepEmitente")).send_keys(Cep)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "telefoneEmitente"))
        )
        web.find_element(By.ID, ("telefoneEmitente")).send_keys(Numero_Telefone)

        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "receita"))
        )
        Select(web.find_element(By.ID, "receita")
            ).select_by_value(RECEITA)

        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "mesReferencia"))
        )
        Select(web.find_element(By.ID, "mesReferencia")
            ).select_by_value(Periodo_Ref)

        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "anoReferencia"))
        )
        Select(web.find_element(By.ID, "anoReferencia")
            ).select_by_value(Ano_Ref)
        web.find_element(By.ID, ("convenio")
                        ).send_keys(CONVENIO)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "dataVencimento"))
        )
        sleep(0.2)
        web.find_element(By.ID, ("dataVencimento")
                        ).send_keys(datavencimento)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "valor"))
        )
        web.find_element(By.ID, ("valor")
                        ).send_keys(VALOR_TOTAL)
        
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, INSCRITO))
        )
        web.find_element(By.ID, (INSCRITO)
                        ).click()
        
        #SE FOR INSCRITO NA UF
  
        if INSCRITO == "optInscritoDest":
            WebDriverWait(web, 10).until(
                EC.presence_of_element_located((By.ID, "inscricaoEstadualDestinatario"))
            )
            web.find_element(By.ID, ("inscricaoEstadualDestinatario")
                            ).send_keys(IE)
            WebDriverWait(web, 10).until(
                EC.presence_of_element_located((By.ID, "campoAdicional00"))
            )
            web.find_element(By.ID, ("campoAdicional00")
                            ).send_keys(chave)
        
        else:
            print(IDENTIFICAO)
            WebDriverWait(web, 10).until(
                EC.presence_of_element_located((By.ID, IDENTIFICAO))
            )
            web.find_element(By.ID, (IDENTIFICAO)
                            ).click()
            WebDriverWait(web, 10).until(
                EC.presence_of_element_located((By.ID, "documentoDestinatario"))
            )
            sleep(0.2)
            web.find_element(By.ID, ("documentoDestinatario")
                            ).send_keys(CPF_CNPJ_DESTINATARIO)
            WebDriverWait(web, 10).until(
                EC.presence_of_element_located((By.ID, "razaoSocialDestinatario"))
            )
            web.find_element(By.ID, ("razaoSocialDestinatario")
                            ).send_keys(razao_dest)
            WebDriverWait(web, 10).until(
                EC.presence_of_element_located((By.ID, "municipioDestinatario"))
            )
            Select(web.find_element(By.ID, "municipioDestinatario")
                ).select_by_value(codigo_munc_dest)
            WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "tipoDocOrigem"))
            )
            Select(web.find_element(By.ID, "tipoDocOrigem")
                ).select_by_value('22')
            web.find_element(By.ID, ("numeroDocumentoOrigem")
                            ).send_keys(chave)
        
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "dataPagamento"))
        )
        web.find_element(By.ID, ("dataPagamento")
                        ).clear()
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "dataPagamento"))
        )
        
        web.find_element(By.ID, ("dataPagamento")
                        ).send_keys(datavencimento)
        


        try:
            while True:
                if not web.execute_script("return window.top.closed"):
                    time.sleep(1)
                else:
                    print("navegador fechado")
                    break
        except:
            print("OK")
    #PRONTO DIFAL E ST
    def estado_RO(self):
       # Ler arquivo xml
        xml_arq
        tree = ET.parse(xml_arq)
        root = tree.getroot()
        ns = {'nfe': 'http://www.portalfiscal.inf.br/nfe'}
        # salvar informaçoes em variaveis
        Cnpj = root.find('.//nfe:NFe/nfe:infNFe/nfe:emit/nfe:CNPJ', ns).text
        Razao_Social = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:xNome', ns).text
        endereco = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:enderEmit/nfe:xLgr', ns).text
        Uf = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:enderEmit/nfe:UF', ns).text
        Cep = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:enderEmit/nfe:CEP', ns).text
        Codigo_Municipio = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:enderEmit/nfe:cMun', ns).text
        Codigo_Municipio = Codigo_Municipio[2:]
        Numero_Telefone = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:enderEmit/nfe:fone', ns).text
        Numero_Telefone = Numero_Telefone[2:]
        # dados para emitir gnre por estado
        Numero_NFE = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:ide/nfe:nNF', ns).text
        Periodo_Ref = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:ide/nfe:dhEmi', ns).text
        valor_difal = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:total/nfe:ICMSTot/nfe:vICMSUFDest', ns).text
        Ano_Ref = Periodo_Ref[:4]
        #dados destinatario

        razao_dest = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:dest/nfe:xNome', ns).text
        codigo_munc_dest = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:dest/nfe:enderDest/nfe:cMun', ns).text
        chave = root.find(
            './/nfe:protNFe/nfe:infProt/nfe:chNFe', ns).text
        
        codigo_munc_dest = codigo_munc_dest[2:]
        Periodo_Ref = Periodo_Ref[5:7]

        print(Periodo_Ref)

        chrome_options = Options()
        chrome_options.add_argument("--incognito")
        web = webdriver.Chrome(chrome_options=chrome_options)
        web.maximize_window()
        web.get("https://www.gnre.pe.gov.br:444/gnre/v/guia/index")


        Select(web.find_element(By.ID, "ufFavorecida")).select_by_value(uf_f)

        sleep(2)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "optGnreSimples"))
        )
        web.find_element(By.ID, ("optGnreSimples")).click()
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "optNaoInscrito"))
        )
        web.find_element(By.ID, ("optNaoInscrito")).click()
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "tipoCNPJ"))
        )
        web.find_element(By.ID, ("tipoCNPJ")).click()
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "documentoEmitente"))
        )
        web.find_element(By.ID, ("documentoEmitente")).send_keys(Cnpj)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "razaoSocialEmitente"))
        )
        web.find_element(By.ID, ("razaoSocialEmitente")).send_keys(Razao_Social)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "razaoSocialEmitente"))
        )
        web.find_element(By.ID, ("enderecoEmitente")).send_keys(endereco)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "ufEmitente"))
        )
        Select(web.find_element(By.ID, "ufEmitente")).select_by_value(Uf)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "municipioEmitente"))
        )
        Select(web.find_element(By.ID, "municipioEmitente")
            ).select_by_value(Codigo_Municipio)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "cepEmitente"))
        )
        web.find_element(By.ID, ("cepEmitente")).send_keys(Cep)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "telefoneEmitente"))
        )
        web.find_element(By.ID, ("telefoneEmitente")).send_keys(Numero_Telefone)

        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "receita"))
        )
        Select(web.find_element(By.ID, "receita")
            ).select_by_value(RECEITA)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "tipoDocOrigem"))
        )
        Select(web.find_element(By.ID, "tipoDocOrigem")
            ).select_by_value('10')
        web.find_element(By.ID, ("numeroDocumentoOrigem")
                        ).send_keys(Numero_NFE)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "mesReferencia"))
        )
        Select(web.find_element(By.ID, "mesReferencia")
            ).select_by_value(Periodo_Ref)

        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "anoReferencia"))
        )
        Select(web.find_element(By.ID, "anoReferencia")
            ).select_by_value(Ano_Ref)
        web.find_element(By.ID, ("convenio")
                        ).send_keys(CONVENIO)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "dataVencimento"))
        )
        web.find_element(By.ID, ("dataVencimento")
                        ).send_keys(datavencimento)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "valor"))
        )
        web.find_element(By.ID, ("valor")
                        ).send_keys(VALOR_TOTAL)
        
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "campoAdicional00"))
        )
        web.find_element(By.ID, ("campoAdicional00")
                        ).send_keys(chave)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "dataPagamento"))
        )
        web.find_element(By.ID, ("dataPagamento")
                        ).clear()
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "dataPagamento"))
        )
        web.find_element(By.ID, ("dataPagamento")
                        ).send_keys(datavencimento)
    
        try:
            while True:
                if not web.execute_script("return window.top.closed"):
                    time.sleep(1)
                else:
                    print("navegador fechado")
                    break
        except:
            print("OK")
    #PRONTO DIFAL E ST
    def estado_RR(self):
        # Ler arquivo xml
        xml_arq
        tree = ET.parse(xml_arq)
        root = tree.getroot()
        ns = {'nfe': 'http://www.portalfiscal.inf.br/nfe'}
        # salvar informaçoes em variaveis
        Cnpj = root.find('.//nfe:NFe/nfe:infNFe/nfe:emit/nfe:CNPJ', ns).text
        Razao_Social = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:xNome', ns).text
        endereco = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:enderEmit/nfe:xLgr', ns).text
        Uf = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:enderEmit/nfe:UF', ns).text
        Cep = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:enderEmit/nfe:CEP', ns).text
        Codigo_Municipio = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:enderEmit/nfe:cMun', ns).text
        Codigo_Municipio = Codigo_Municipio[2:]
        Numero_Telefone = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:enderEmit/nfe:fone', ns).text
        Numero_Telefone = Numero_Telefone[2:]
        
        # dados para emitir gnre por estado
        Numero_NFE = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:ide/nfe:nNF', ns).text
        Periodo_Ref = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:ide/nfe:dhEmi', ns).text
        valor_difal = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:total/nfe:ICMSTot/nfe:vICMSUFDest', ns).text
        Ano_Ref = Periodo_Ref[:4]
        #dados destinatario

        razao_dest = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:dest/nfe:xNome', ns).text
        codigo_munc_dest = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:dest/nfe:enderDest/nfe:cMun', ns).text
        chave = root.find(
            './/nfe:protNFe/nfe:infProt/nfe:chNFe', ns).text
        
        codigo_munc_dest = codigo_munc_dest[2:]
        Periodo_Ref = Periodo_Ref[5:7]


        chrome_options = Options()
        chrome_options.add_argument("--incognito")
        web = webdriver.Chrome(chrome_options=chrome_options)
        web.maximize_window()
        web.get("https://www.gnre.pe.gov.br:444/gnre/v/guia/index")


        Select(web.find_element(By.ID, "ufFavorecida")).select_by_value(uf_f)

        sleep(2)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "optGnreSimples"))
        )
        web.find_element(By.ID, ("optGnreSimples")).click()
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "optNaoInscrito"))
        )
        web.find_element(By.ID, ("optNaoInscrito")).click()
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "tipoCNPJ"))
        )
        web.find_element(By.ID, ("tipoCNPJ")).click()
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "documentoEmitente"))
        )
        web.find_element(By.ID, ("documentoEmitente")).send_keys(Cnpj)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "razaoSocialEmitente"))
        )
        web.find_element(By.ID, ("razaoSocialEmitente")).send_keys(Razao_Social)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "razaoSocialEmitente"))
        )
        web.find_element(By.ID, ("enderecoEmitente")).send_keys(endereco)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "ufEmitente"))
        )
        Select(web.find_element(By.ID, "ufEmitente")).select_by_value(Uf)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "municipioEmitente"))
        )
        Select(web.find_element(By.ID, "municipioEmitente")
            ).select_by_value(Codigo_Municipio)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "cepEmitente"))
        )
        sleep(0.5)
        web.find_element(By.ID, ("cepEmitente")).send_keys(Cep)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "telefoneEmitente"))
        )
        sleep(0.5)
        web.find_element(By.ID, ("telefoneEmitente")).send_keys(Numero_Telefone)
        sleep(0.5)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "receita"))
        )
        Select(web.find_element(By.ID, "receita")
            ).select_by_value(RECEITA)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "tipoDocOrigem"))
        )
        Select(web.find_element(By.ID, "tipoDocOrigem")
            ).select_by_value('10')
        web.find_element(By.ID, ("numeroDocumentoOrigem")
                        ).send_keys(Numero_NFE)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "mesReferencia"))
        )
        sleep(0.5)
        Select(web.find_element(By.ID, "mesReferencia")
            ).select_by_value(Periodo_Ref)

        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "anoReferencia"))
        )
        Select(web.find_element(By.ID, "anoReferencia")
            ).select_by_value(Ano_Ref)
        web.find_element(By.ID, ("convenio")
                        ).send_keys(CONVENIO)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "dataVencimento"))
        )
        sleep(0.5)
        web.find_element(By.ID, ("dataVencimento")
                        ).send_keys(datavencimento)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "tipoValorPrincipal"))
        )
        web.find_element(By.ID, ("tipoValorPrincipal")
                        ).click()
        
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "valor"))
        )
        web.find_element(By.ID, ("valor")
                        ).send_keys(VALOR_TOTAL)
        

        
        #SE FOR INSCRITO NA UF
        sleep(0.5)
        if INSCRITO == "optInscritoDest":
            WebDriverWait(web, 10).until(
                EC.presence_of_element_located((By.ID, "produto"))
            )
            Select(web.find_element(By.ID, "produto")
                ).select_by_value("22")
            sleep(0.5)
        else:
            pass
        
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "campoAdicional00"))
        )
        sleep(0.5)
        web.find_element(By.ID, ("campoAdicional00")
                        ).send_keys(chave)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "dataPagamento"))
        )
        sleep(0.5)
        web.find_element(By.ID, ("dataPagamento")
                        ).clear()
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "dataPagamento"))
        )
        sleep(0.5)
        web.find_element(By.ID, ("dataPagamento")
                        ).send_keys(datavencimento)
        
        try:
            while True:
                if not web.execute_script("return window.top.closed"):
                    time.sleep(1)
                else:
                    print("navegador fechado")
                    break
        except:
            print("OK")
    #PRONTO DIFAL E ST
    def estado_RS(self):
        # Ler arquivo xml
        xml_arq
        tree = ET.parse(xml_arq)
        root = tree.getroot()
        ns = {'nfe': 'http://www.portalfiscal.inf.br/nfe'}
        # salvar informaçoes em variaveis
        Cnpj = root.find('.//nfe:NFe/nfe:infNFe/nfe:emit/nfe:CNPJ', ns).text
        Razao_Social = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:xNome', ns).text
        endereco = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:enderEmit/nfe:xLgr', ns).text
        Uf = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:enderEmit/nfe:UF', ns).text
        Cep = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:enderEmit/nfe:CEP', ns).text
        Codigo_Municipio = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:enderEmit/nfe:cMun', ns).text
        Codigo_Municipio = Codigo_Municipio[2:]
        Numero_Telefone = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:enderEmit/nfe:fone', ns).text
        Numero_Telefone = Numero_Telefone[2:]
        # dados para emitir gnre por estado
        Numero_NFE = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:ide/nfe:nNF', ns).text
        Periodo_Ref = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:ide/nfe:dhEmi', ns).text
        valor_difal = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:total/nfe:ICMSTot/nfe:vICMSUFDest', ns).text
        Ano_Ref = Periodo_Ref[:4]
        #dados destinatario

        razao_dest = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:dest/nfe:xNome', ns).text
        codigo_munc_dest = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:dest/nfe:enderDest/nfe:cMun', ns).text
        chave = root.find(
            './/nfe:protNFe/nfe:infProt/nfe:chNFe', ns).text
        
        codigo_munc_dest = codigo_munc_dest[2:]
        Periodo_Ref = Periodo_Ref[5:7]

        print(Periodo_Ref)

        chrome_options = Options()
        chrome_options.add_argument("--incognito")
        web = webdriver.Chrome(chrome_options=chrome_options)
        web.maximize_window()
        web.get("https://www.gnre.pe.gov.br:444/gnre/v/guia/index")


        Select(web.find_element(By.ID, "ufFavorecida")).select_by_value(uf_f)

        sleep(2)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "optGnreSimples"))
        )
        web.find_element(By.ID, ("optGnreSimples")).click()
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "optNaoInscrito"))
        )
        web.find_element(By.ID, ("optNaoInscrito")).click()
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "tipoCNPJ"))
        )
        web.find_element(By.ID, ("tipoCNPJ")).click()
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "documentoEmitente"))
        )
        web.find_element(By.ID, ("documentoEmitente")).send_keys(Cnpj)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "razaoSocialEmitente"))
        )
        web.find_element(By.ID, ("razaoSocialEmitente")).send_keys(Razao_Social)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "razaoSocialEmitente"))
        )
        web.find_element(By.ID, ("enderecoEmitente")).send_keys(endereco)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "ufEmitente"))
        )
        Select(web.find_element(By.ID, "ufEmitente")).select_by_value(Uf)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "municipioEmitente"))
        )
        Select(web.find_element(By.ID, "municipioEmitente")
            ).select_by_value(Codigo_Municipio)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "cepEmitente"))
        )
        web.find_element(By.ID, ("cepEmitente")).send_keys(Cep)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "telefoneEmitente"))
        )
        web.find_element(By.ID, ("telefoneEmitente")).send_keys(Numero_Telefone)

        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "receita"))
        )
        Select(web.find_element(By.ID, "receita")
            ).select_by_value(RECEITA)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "tipoDocOrigem"))
        )
        Select(web.find_element(By.ID, "tipoDocOrigem")
            ).select_by_value('22')
        web.find_element(By.ID, ("numeroDocumentoOrigem")
                        ).send_keys(chave)

        web.find_element(By.ID, ("convenio")
                        ).send_keys(CONVENIO)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "dataVencimento"))
        )
        sleep(0.2)
        web.find_element(By.ID, ("dataVencimento")
                        ).send_keys(datavencimento)
        
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "valor"))
        )
        web.find_element(By.ID, ("valor")
                        ).send_keys(VALOR_TOTAL)
        
        WebDriverWait(web, 10).until(

            EC.presence_of_element_located((By.ID, INSCRITO))
        )
        web.find_element(By.ID, (INSCRITO)
                        ).click()
        if INSCRITO == "optInscritoDest":
            WebDriverWait(web, 10).until(
                EC.presence_of_element_located((By.ID, "inscricaoEstadualDestinatario"))
            )
            web.find_element(By.ID, ("inscricaoEstadualDestinatario")
                            ).send_keys(IE)
        else:
            WebDriverWait(web, 10).until(
                EC.presence_of_element_located((By.ID, IDENTIFICAO))
            )
            web.find_element(By.ID, (IDENTIFICAO)
                            ).click()
    
            WebDriverWait(web, 10).until(
                EC.presence_of_element_located((By.ID, "documentoDestinatario"))
            )
            web.find_element(By.ID, ("documentoDestinatario")
                            ).send_keys(CPF_CNPJ_DESTINATARIO)
            WebDriverWait(web, 10).until(
                EC.presence_of_element_located((By.ID, "razaoSocialDestinatario"))
            )
            web.find_element(By.ID, ("razaoSocialDestinatario")
                            ).send_keys(razao_dest)
            WebDriverWait(web, 10).until(
                EC.presence_of_element_located((By.ID, "municipioDestinatario"))
            )
            Select(web.find_element(By.ID, "municipioDestinatario")
                ).select_by_value(codigo_munc_dest)
        
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "dataPagamento"))
        )
        web.find_element(By.ID, ("dataPagamento")
                        ).clear()
        sleep(0.2)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "dataPagamento"))
        )
        web.find_element(By.ID, ("dataPagamento")
                        ).send_keys(datavencimento)
        


        try:
            while True:
                if not web.execute_script("return window.top.closed"):
                    time.sleep(1)
                else:
                    print("navegador fechado")
                    break
        except:
            print("OK")
    #PRONTO DIFAL E ST
    def estado_SC(self):
        # Ler arquivo xml
        xml_arq
        tree = ET.parse(xml_arq)
        root = tree.getroot()
        ns = {'nfe': 'http://www.portalfiscal.inf.br/nfe'}
        # salvar informaçoes em variaveis
        Cnpj = root.find('.//nfe:NFe/nfe:infNFe/nfe:emit/nfe:CNPJ', ns).text
        Razao_Social = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:xNome', ns).text
        endereco = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:enderEmit/nfe:xLgr', ns).text
        chave = root.find(
            './/nfe:protNFe/nfe:infProt/nfe:chNFe', ns).text
        Uf = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:enderEmit/nfe:UF', ns).text
        Cep = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:enderEmit/nfe:CEP', ns).text
        Codigo_Municipio = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:enderEmit/nfe:cMun', ns).text
        Codigo_Municipio = Codigo_Municipio[2:]
        Numero_Telefone = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:enderEmit/nfe:fone', ns).text
        Numero_Telefone = Numero_Telefone[2:]
        valor_difal = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:total/nfe:ICMSTot/nfe:vICMSUFDest', ns).text

        razao_dest = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:dest/nfe:xNome', ns).text
        codigo_munc_dest = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:dest/nfe:enderDest/nfe:cMun', ns).text
        codigo_munc_dest = codigo_munc_dest[2:]
        chrome_options = Options()
        chrome_options.add_argument("--incognito")
        web = webdriver.Chrome(chrome_options=chrome_options)
        web.maximize_window()
        web.get("https://www.gnre.pe.gov.br:444/gnre/v/guia/index")


        Select(web.find_element(By.ID, "ufFavorecida")).select_by_value(uf_f)

        sleep(2)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "optGnreSimples"))
        )
        web.find_element(By.ID, ("optGnreSimples")).click()
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "optNaoInscrito"))
        )
        web.find_element(By.ID, ("optNaoInscrito")).click()
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "tipoCNPJ"))
        )
        web.find_element(By.ID, ("tipoCNPJ")).click()
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "documentoEmitente"))
        )
        web.find_element(By.ID, ("documentoEmitente")).send_keys(Cnpj)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "razaoSocialEmitente"))
        )
        web.find_element(By.ID, ("razaoSocialEmitente")).send_keys(Razao_Social)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "razaoSocialEmitente"))
        )
        web.find_element(By.ID, ("enderecoEmitente")).send_keys(endereco)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "ufEmitente"))
        )
        Select(web.find_element(By.ID, "ufEmitente")).select_by_value(Uf)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "municipioEmitente"))
        )
        Select(web.find_element(By.ID, "municipioEmitente")
            ).select_by_value(Codigo_Municipio)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "cepEmitente"))
        )
        web.find_element(By.ID, ("cepEmitente")).send_keys(Cep)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "telefoneEmitente"))
        )
        sleep(0.1)
        web.find_element(By.ID, ("telefoneEmitente")).send_keys(Numero_Telefone)

        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "receita"))
        )
        Select(web.find_element(By.ID, "receita")
            ).select_by_value(RECEITA)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "tipoDocOrigem"))
        )
        Select(web.find_element(By.ID, "tipoDocOrigem")
            ).select_by_value('24')
        
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "numeroDocumentoOrigem"))
        )
        web.find_element(By.ID, ("numeroDocumentoOrigem")).send_keys(chave)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "dataVencimento"))
        )
        web.find_element(By.ID, ("dataVencimento")).send_keys(datavencimento)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "valor"))
        )
        web.find_element(By.ID, ("valor")).send_keys(VALOR_TOTAL)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "dataPagamento"))
        )
        web.find_element(By.ID, ("dataPagamento")
                        ).clear()
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "dataPagamento"))
        )
        web.find_element(By.ID, ("dataPagamento")
                        ).clear()
        sleep(0.2)
        web.find_element(By.ID, ("dataPagamento")
                        ).send_keys(datavencimento)

        
        try:
            while True:
                if not web.execute_script("return window.top.closed"):
                    time.sleep(1)
                else:
                    print("navegador fechado")
                    break
        except:
            print("OK")
    #PRONTO DIFAL E ST
    def estado_SE(self):
        # Ler arquivo xml
        xml_arq
        tree = ET.parse(xml_arq)
        root = tree.getroot()
        ns = {'nfe': 'http://www.portalfiscal.inf.br/nfe'}
        # salvar informaçoes em variaveis
        Cnpj = root.find('.//nfe:NFe/nfe:infNFe/nfe:emit/nfe:CNPJ', ns).text
        Razao_Social = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:xNome', ns).text
        endereco = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:enderEmit/nfe:xLgr', ns).text
        Uf = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:enderEmit/nfe:UF', ns).text
        Cep = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:enderEmit/nfe:CEP', ns).text
        Codigo_Municipio = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:enderEmit/nfe:cMun', ns).text
        Codigo_Municipio = Codigo_Municipio[2:]
        Numero_Telefone = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:enderEmit/nfe:fone', ns).text
        Numero_Telefone = Numero_Telefone[2:]
        
        # dados para emitir gnre por estado
        Numero_NFE = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:ide/nfe:nNF', ns).text
        Periodo_Ref = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:ide/nfe:dhEmi', ns).text
        valor_difal = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:total/nfe:ICMSTot/nfe:vICMSUFDest', ns).text
        Ano_Ref = Periodo_Ref[:4]
        #dados destinatario

        razao_dest = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:dest/nfe:xNome', ns).text
        codigo_munc_dest = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:dest/nfe:enderDest/nfe:cMun', ns).text
        chave = root.find(
            './/nfe:protNFe/nfe:infProt/nfe:chNFe', ns).text
        
        codigo_munc_dest = codigo_munc_dest[2:]
        Periodo_Ref = Periodo_Ref[5:7]


        chrome_options = Options()
        chrome_options.add_argument("--incognito")
        web = webdriver.Chrome(chrome_options=chrome_options)
        web.maximize_window()
        web.get("https://www.gnre.pe.gov.br:444/gnre/v/guia/index")


        Select(web.find_element(By.ID, "ufFavorecida")).select_by_value(uf_f)

        sleep(2)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "optGnreSimples"))
        )
        web.find_element(By.ID, ("optGnreSimples")).click()
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "optNaoInscrito"))
        )
        web.find_element(By.ID, ("optNaoInscrito")).click()
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "tipoCNPJ"))
        )
        web.find_element(By.ID, ("tipoCNPJ")).click()
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "documentoEmitente"))
        )
        web.find_element(By.ID, ("documentoEmitente")).send_keys(Cnpj)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "razaoSocialEmitente"))
        )
        web.find_element(By.ID, ("razaoSocialEmitente")).send_keys(Razao_Social)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "razaoSocialEmitente"))
        )
        web.find_element(By.ID, ("enderecoEmitente")).send_keys(endereco)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "ufEmitente"))
        )
        Select(web.find_element(By.ID, "ufEmitente")).select_by_value(Uf)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "municipioEmitente"))
        )
        Select(web.find_element(By.ID, "municipioEmitente")
            ).select_by_value(Codigo_Municipio)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "cepEmitente"))
        )
        web.find_element(By.ID, ("cepEmitente")).send_keys(Cep)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "telefoneEmitente"))
        )
        web.find_element(By.ID, ("telefoneEmitente")).send_keys(Numero_Telefone)

        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "receita"))
        )
        Select(web.find_element(By.ID, "receita")
            ).select_by_value(RECEITA)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "tipoDocOrigem"))
        )
        Select(web.find_element(By.ID, "tipoDocOrigem")
            ).select_by_value('10')
        web.find_element(By.ID, ("numeroDocumentoOrigem")
                        ).send_keys(Numero_NFE)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "mesReferencia"))
        )
        Select(web.find_element(By.ID, "mesReferencia")
            ).select_by_value(Periodo_Ref)

        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "anoReferencia"))
        )
        Select(web.find_element(By.ID, "anoReferencia")
            ).select_by_value(Ano_Ref)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "dataVencimento"))
        )
        sleep(0.2)
        web.find_element(By.ID, ("dataVencimento")
                        ).send_keys(datavencimento)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "valor"))
        )
        web.find_element(By.ID, ("valor")
                        ).send_keys(VALOR_TOTAL)
        
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, INSCRITO))
        )
        web.find_element(By.ID, (INSCRITO)
                        ).click()
        
        #SE FOR INSCRITO NA UF
  
        if INSCRITO == "optInscritoDest":
            WebDriverWait(web, 10).until(
                EC.presence_of_element_located((By.ID, "inscricaoEstadualDestinatario"))
            )
            web.find_element(By.ID, ("inscricaoEstadualDestinatario")
                            ).send_keys(IE)
            web.find_element(By.ID, ("convenio")
                        ).send_keys(CONVENIO)

        
        else:
            print(IDENTIFICAO)
            WebDriverWait(web, 10).until(
                EC.presence_of_element_located((By.ID, IDENTIFICAO))
            )
            web.find_element(By.ID, (IDENTIFICAO)
                            ).click()
            WebDriverWait(web, 10).until(
                EC.presence_of_element_located((By.ID, "documentoDestinatario"))
            )
            sleep(0.2)
            web.find_element(By.ID, ("documentoDestinatario")
                            ).send_keys(CPF_CNPJ_DESTINATARIO)
            WebDriverWait(web, 10).until(
                EC.presence_of_element_located((By.ID, "razaoSocialDestinatario"))
            )
            web.find_element(By.ID, ("razaoSocialDestinatario")
                            ).send_keys(razao_dest)
            WebDriverWait(web, 10).until(
                EC.presence_of_element_located((By.ID, "municipioDestinatario"))
            )
            Select(web.find_element(By.ID, "municipioDestinatario")
                ).select_by_value(codigo_munc_dest)
        
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "campoAdicional00"))
        )
        sleep(0.2)
        web.find_element(By.ID, ("campoAdicional00")
                        ).send_keys(chave)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "dataPagamento"))
        )
        web.find_element(By.ID, ("dataPagamento")
                        ).clear()
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "dataPagamento"))
        )
        
        web.find_element(By.ID, ("dataPagamento")
                        ).send_keys(datavencimento)
        


        try:
            while True:
                if not web.execute_script("return window.top.closed"):
                    time.sleep(1)
                else:
                    print("navegador fechado")
                    break
        except:
            print("OK")
    #PRONTO DIFAL E ST
    def estado_TO(self):
        # Ler arquivo xml
        
        xml_arq
        tree = ET.parse(xml_arq)
        root = tree.getroot()
        ns = {'nfe': 'http://www.portalfiscal.inf.br/nfe'}
        # salvar informaçoes em variaveis
        Cnpj = root.find('.//nfe:NFe/nfe:infNFe/nfe:emit/nfe:CNPJ', ns).text
        Razao_Social = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:xNome', ns).text
        endereco = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:enderEmit/nfe:xLgr', ns).text
        Uf = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:enderEmit/nfe:UF', ns).text
        Cep = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:enderEmit/nfe:CEP', ns).text
        Codigo_Municipio = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:enderEmit/nfe:cMun', ns).text
        Codigo_Municipio = Codigo_Municipio[2:]
        Numero_Telefone = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:enderEmit/nfe:fone', ns).text
        Numero_Telefone = Numero_Telefone[2:]
        # dados para emitir gnre por estado
        Numero_NFE = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:ide/nfe:nNF', ns).text
        Periodo_Ref = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:ide/nfe:dhEmi', ns).text
        valor_difal = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:total/nfe:ICMSTot/nfe:vICMSUFDest', ns).text
        Ano_Ref = Periodo_Ref[:4]
        #dados destinatario

        razao_dest = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:dest/nfe:xNome', ns).text
        codigo_munc_dest = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:dest/nfe:enderDest/nfe:cMun', ns).text
        chave = root.find(
            './/nfe:protNFe/nfe:infProt/nfe:chNFe', ns).text
        
        codigo_munc_dest = codigo_munc_dest[2:]
        Periodo_Ref = Periodo_Ref[5:7]

        print(Periodo_Ref)

        chrome_options = Options()
        chrome_options.add_argument("--incognito")
        web = webdriver.Chrome(chrome_options=chrome_options)
        web.maximize_window()
        web.get("https://www.gnre.pe.gov.br:444/gnre/v/guia/index")


        Select(web.find_element(By.ID, "ufFavorecida")).select_by_value(uf_f)

        sleep(2)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "optGnreSimples"))
        )
        web.find_element(By.ID, ("optGnreSimples")).click()
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "optNaoInscrito"))
        )
        web.find_element(By.ID, ("optNaoInscrito")).click()
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "tipoCNPJ"))
        )
        web.find_element(By.ID, ("tipoCNPJ")).click()
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "documentoEmitente"))
        )
        web.find_element(By.ID, ("documentoEmitente")).send_keys(Cnpj)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "razaoSocialEmitente"))
        )
        web.find_element(By.ID, ("razaoSocialEmitente")).send_keys(Razao_Social)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "razaoSocialEmitente"))
        )
        web.find_element(By.ID, ("enderecoEmitente")).send_keys(endereco)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "ufEmitente"))
        )
        Select(web.find_element(By.ID, "ufEmitente")).select_by_value(Uf)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "municipioEmitente"))
        )
        Select(web.find_element(By.ID, "municipioEmitente")
            ).select_by_value(Codigo_Municipio)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "cepEmitente"))
        )
        web.find_element(By.ID, ("cepEmitente")).send_keys(Cep)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "telefoneEmitente"))
        )
        web.find_element(By.ID, ("telefoneEmitente")).send_keys(Numero_Telefone)

        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "receita"))
        )
        Select(web.find_element(By.ID, "receita")
            ).select_by_value(RECEITA)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "tipoDocOrigem"))
        )
        Select(web.find_element(By.ID, "tipoDocOrigem")
            ).select_by_value('10')
        web.find_element(By.ID, ("numeroDocumentoOrigem")
                        ).send_keys(Numero_NFE)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "mesReferencia"))
        )
        Select(web.find_element(By.ID, "mesReferencia")
            ).select_by_value(Periodo_Ref)

        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "anoReferencia"))
        )
        Select(web.find_element(By.ID, "anoReferencia")
            ).select_by_value(Ano_Ref)
        web.find_element(By.ID, ("convenio")
                        ).send_keys(CONVENIO)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "dataVencimento"))
        )
        sleep(0.9)
        web.find_element(By.ID, ("dataVencimento")
                        ).send_keys(datavencimento)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "tipoValorPrincipal"))
        )
        web.find_element(By.ID, ("tipoValorPrincipal")
                        ).click()
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "valor"))
        )
        web.find_element(By.ID, ("valor")
                        ).send_keys(VALOR_TOTAL)
        
        WebDriverWait(web, 10).until(

            EC.presence_of_element_located((By.ID, INSCRITO))
        )
        web.find_element(By.ID, (INSCRITO)
                        ).click()
        if INSCRITO == 'optInscritoDest':
            WebDriverWait(web, 10).until(
                EC.presence_of_element_located((By.ID, "inscricaoEstadualDestinatario"))
            )
            web.find_element(By.ID, ("inscricaoEstadualDestinatario")
                            ).send_keys(IE)
            WebDriverWait(web, 10).until(
                EC.presence_of_element_located((By.ID, "detalheReceita"))
            )
            Select(web.find_element(By.ID, "detalheReceita")
                ).select_by_value("000005")
            WebDriverWait(web, 10).until(
                EC.presence_of_element_located((By.ID, "produto"))
            )
            Select(web.find_element(By.ID, "produto")
                ).select_by_value("22")

        else:
            WebDriverWait(web, 10).until(
                EC.presence_of_element_located((By.ID, IDENTIFICAO))
            )
            web.find_element(By.ID, (IDENTIFICAO)
                            ).click()
            WebDriverWait(web, 10).until(
                EC.presence_of_element_located((By.ID, "documentoDestinatario"))
            )
            web.find_element(By.ID, ("documentoDestinatario")
                            ).send_keys(CPF_CNPJ_DESTINATARIO)
            WebDriverWait(web, 10).until(
                EC.presence_of_element_located((By.ID, "razaoSocialDestinatario"))
            )
            web.find_element(By.ID, ("razaoSocialDestinatario")
                            ).send_keys(razao_dest)
            WebDriverWait(web, 10).until(
                EC.presence_of_element_located((By.ID, "municipioDestinatario"))
            )
            Select(web.find_element(By.ID, "municipioDestinatario")
                ).select_by_value(codigo_munc_dest)
        
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "campoAdicional00"))
        )
        sleep(0.9)
        web.find_element(By.ID, ("campoAdicional00")
                        ).send_keys(chave)
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "dataPagamento"))
        )
        web.find_element(By.ID, ("dataPagamento")
                        ).clear()
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "dataPagamento"))
        )
        sleep(0.2)
        web.find_element(By.ID, ("dataPagamento")
                        ).send_keys(datavencimento)
        


        try:
            while True:
                if not web.execute_script("return window.top.closed"):
                    time.sleep(1)
                else:
                    print("navegador fechado")
                    break
        except:
            print("OK")
    #PRONTO DIFAL E ST
    def estado_ES(self):
        # Ler arquivo xml
        
        xml_arq
        tree = ET.parse(xml_arq)
        root = tree.getroot()
        ns = {'nfe': 'http://www.portalfiscal.inf.br/nfe'}
        # salvar informaçoes em variaveis
        Cnpj = root.find('.//nfe:NFe/nfe:infNFe/nfe:emit/nfe:CNPJ', ns).text
        Razao_Social = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:xNome', ns).text
        endereco = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:enderEmit/nfe:xLgr', ns).text
        Uf = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:enderEmit/nfe:UF', ns).text
        Cep = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:enderEmit/nfe:CEP', ns).text
        Codigo_Municipio = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:enderEmit/nfe:cMun', ns).text
        Codigo_Municipio = Codigo_Municipio[2:]
        Numero_Telefone = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:enderEmit/nfe:fone', ns).text
        Numero_Telefone = Numero_Telefone[2:]
        # dados para emitir gnre por estado
        Numero_NFE = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:ide/nfe:nNF', ns).text
        Periodo_Ref = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:ide/nfe:dhEmi', ns).text
        valor_difal = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:total/nfe:ICMSTot/nfe:vICMSUFDest', ns).text
        Mes_Ref = Periodo_Ref[5:7]
        Ano_Ref = Periodo_Ref[:4]
        Referencia = Mes_Ref+"/"+Ano_Ref
        #dados destinatario

        razao_dest = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:dest/nfe:xNome', ns).text
        codigo_munc_dest = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:dest/nfe:enderDest/nfe:cMun', ns).text
        chave = root.find(
            './/nfe:protNFe/nfe:infProt/nfe:chNFe', ns).text
        
        cod = codigo_munc_dest
        Periodo_Ref = Periodo_Ref[5:7]

        print(Periodo_Ref)
        chrome_options = Options()
        chrome_options.add_argument("--incognito")
        web = webdriver.Chrome(chrome_options=chrome_options)
        web.maximize_window()
        web.get("https://internet.sefaz.es.gov.br/agenciavirtual/area_publica/e-dua/icms.php")
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "numIdentificacao"))
        )
        web.find_element(By.ID, ("numIdentificacao")).send_keys(Cnpj)
        if RECEITA == "100102":
            WebDriverWait(web, 10).until(
                EC.presence_of_element_located((By.ID, "servico"))
            )
            Select(web.find_element(By.ID, "servico")
                ).select_by_value('1439')
        else:
            WebDriverWait(web, 10).until(
                EC.presence_of_element_located((By.ID, "servico"))
            )
            Select(web.find_element(By.ID, "servico")
                ).select_by_value('1463')
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "periodoReferencia"))
        )
        web.find_element(By.ID, ("periodoReferencia")).send_keys(Referencia)

        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "dataVencimento"))
        )
        web.find_element(By.ID, ("dataVencimento")).send_keys(datavencimento)
        
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "valorImposto"))
        )
        web.find_element(By.ID, ("valorImposto")).send_keys(VALOR_TOTAL)
        
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "dscInformacao"))
        )
        web.find_element(By.ID, ("dscInformacao")).send_keys(chave)

        WebDriverWait(web, 1000).until(
            EC.presence_of_element_located((By.ID, "addMunicipio"))
        )   
        if cod == '3200102':	
            cod = '56014'
        elif cod == '3200169':	
            cod = '57177'
        elif cod == '3200136':	
            cod = '57339'
        elif cod == '3200201':	
            cod = '56030'
        elif cod == '3200300':	
            cod = '56057'
        elif cod == '3200359':	
            cod = '57193'
        elif cod == '3200409':	
            cod = '56073'
        elif cod == '3200508':	
            cod = '56090'
        elif cod == '3200607':	
            cod = '56111'
        elif cod == '3200706':	
            cod = '56138'
        elif cod == '3200805':	
            cod = '56154'
        elif cod == '3200904':	
            cod = '56170'
        elif cod == '3201001':	
            cod = '56197'
        elif cod == '3201100':	
            cod = '56219'
        elif cod == '3201159':	
            cod = '7587'
        elif cod == '3201209':	
            cod = '56235'
        elif cod == '3201308':	
            cod = '56251'
        elif cod == '3201407':	
            cod = '56278'
        elif cod == '3201506':	
            cod = '56294'
        elif cod == '3201605':	
            cod = '56316'
        elif cod == '3201704':	
            cod = '56332'
        elif cod == '3201803':	
            cod = '56359'
        elif cod == '3201902':	
            cod = '56375'
        elif cod == '3202009':	
            cod = '56391'
        elif cod == '3202108':	
            cod = '56413'
        elif cod == '3202207':	
            cod = '56430'
        elif cod == '3202256':	
            cod = '11142'
        elif cod == '3202306':	
            cod = '56456'
        elif cod == '3202405':	
            cod = '56472'
        elif cod == '3202454':	
            cod = '57096'
        elif cod == '3202504':	
            cod = '56499'
        elif cod == '3202553':	
            cod = '60119'
        elif cod == '3202603':	
            cod = '56510'
        elif cod == '3202652':	
            cod = '29319'
        elif cod == '3202702':	
            cod = '56537'
        elif cod == '3202801':	
            cod = '56553'
        elif cod == '3202900':	
            cod = '56570'
        elif cod == '3203007':	
            cod = '56596'
        elif cod == '3203056':	
            cod = '57134'
        elif cod == '3203106':	
            cod = '56618'
        elif cod == '3203130':	
            cod = '57215'
        elif cod == '3203163':	
            cod = '57231'
        elif cod == '3203205':	
            cod = '56634'
        elif cod == '3203304':	
            cod = '56650'
        elif cod == '3203320':	
            cod = '7609'
        elif cod == '3203346':	
            cod = '29297'
        elif cod == '3203353':	
            cod = '57070'
        elif cod == '3203403':	
            cod = '56677'
        elif cod == '3203502':	
            cod = '56693'
        elif cod == '3203601':	
            cod = '56715'
        elif cod == '3203700':	
            cod = '56731'
        elif cod == '3203809':	
            cod = '56758'
        elif cod == '3203908':	
            cod = '56774'
        elif cod == '3204005':	
            cod = '56790'
        elif cod == '3204054':	
            cod = '57150'
        elif cod == '3204104':	
            cod = '56812'
        elif cod == '3204203':	
            cod = '56839'
        elif cod == '3204252':	
            cod = '7625'
        elif cod == '3204302':	
            cod = '56855'
        elif cod == '3204351':	
            cod = '57118'
        elif cod == '3204401':	
            cod = '56871'
        elif cod == '3204500':	
            cod = '56898'
        elif cod == '3204559':	
            cod = '57258'
        elif cod == '3204609':	
            cod = '56910'
        elif cod == '3204658':	
            cod = '29335'
        elif cod == '3204708':	
            cod = '56936'
        elif cod == '3204807':	
            cod = '56952'
        elif cod == '3204906':	
            cod = '56979'
        elif cod == '3204955':	
            cod = '7641'
        elif cod == '3205002':	
            cod = '56995'
        elif cod == '3205010':	
            cod = '7668'
        elif cod == '3205036':	
            cod = '57274'
        elif cod == '3205069':	
            cod = '57290'
        elif cod == '3205101':	
            cod = '57010'
        elif cod == '3205150':	
            cod = '29351'
        elif cod == '3205176':	
            cod = '7684'
        elif cod == '3205200':	
            cod = '57037'
        elif cod == '3205309':	
            cod = '57053'
        WebDriverWait(web, 10).until(
                EC.presence_of_element_located((By.ID, "addMunicipio"))
            )
        Select(web.find_element(By.ID, "addMunicipio")
                ).select_by_value(cod)


















        


        try:
            while True:
                if not web.execute_script("return window.top.closed"):
                    time.sleep(1)
                else:
                    print("navegador fechado")
                    break
        except:
            print("OK")
    #PRONTO DIFAL E ST
    def estado_SP(self):
        # Ler arquivo xml
        
        xml_arq
        tree = ET.parse(xml_arq)
        root = tree.getroot()
        ns = {'nfe': 'http://www.portalfiscal.inf.br/nfe'}
        # salvar informaçoes em variaveis
        Cnpj = root.find('.//nfe:NFe/nfe:infNFe/nfe:emit/nfe:CNPJ', ns).text
        Razao_Social = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:xNome', ns).text
        endereco = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:enderEmit/nfe:xLgr', ns).text
        Uf = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:enderEmit/nfe:UF', ns).text
        Cep = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:enderEmit/nfe:CEP', ns).text
        Codigo_Municipio = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:enderEmit/nfe:cMun', ns).text
        Codigo_Municipio = Codigo_Municipio[2:]
        Numero_Telefone = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:enderEmit/nfe:fone', ns).text
        Numero_Telefone = Numero_Telefone[2:]
        # dados para emitir gnre por estado
        Numero_NFE = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:ide/nfe:nNF', ns).text
        Periodo_Ref = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:ide/nfe:dhEmi', ns).text
        valor_difal = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:total/nfe:ICMSTot/nfe:vICMSUFDest', ns).text
        Mes_Ref = Periodo_Ref[5:7]
        Ano_Ref = Periodo_Ref[:4]
        Referencia = Mes_Ref+"/"+Ano_Ref
        #dados destinatario
        cidade = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:emit/nfe:enderEmit/nfe:xMun', ns).text
        razao_dest = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:dest/nfe:xNome', ns).text
        codigo_munc_dest = root.find(
            './/nfe:NFe/nfe:infNFe/nfe:dest/nfe:enderDest/nfe:cMun', ns).text
        chave = root.find(
            './/nfe:protNFe/nfe:infProt/nfe:chNFe', ns).text
        
        codigo_munc_dest = codigo_munc_dest[2:]
        Periodo_Ref = Periodo_Ref[5:7]

        print(Periodo_Ref)

        chrome_options = Options()
        chrome_options.add_argument("--incognito")
        web = webdriver.Chrome(chrome_options=chrome_options)
        web.maximize_window()
        web.get("https://www4.fazenda.sp.gov.br/DareICMS/DareAvulso")
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "txtCriterioConsulta"))
        )
        sleep(0.9)
        web.find_element(By.ID, ("txtCriterioConsulta")).send_keys(Cnpj)

        sleep(2)
        number = 1
        while number != 5 :
            try:
                web.find_element(By.ID, ("txtRazaoSocial")).clear()
                number = 5
            except:
                sleep(1)

        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "txtRazaoSocial"))
        )
        web.find_element(By.ID, ("txtRazaoSocial")).send_keys(Razao_Social)

        #TELEFONE
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "txtTelefone"))
        )
        web.find_element(By.ID, ("txtTelefone")).clear()
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "txtTelefone"))
        )
        web.find_element(By.ID, ("txtTelefone")).send_keys(Numero_Telefone)
        #ENDEREÇO
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "txtEndereco"))
        )
        web.find_element(By.ID, ("txtEndereco")).clear()
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "txtEndereco"))
        )
        web.find_element(By.ID, ("txtEndereco")).send_keys(endereco)
        #CIDADE
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "txtCidade"))
        )
        web.find_element(By.ID, ("txtCidade")).clear()
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, "txtCidade"))
        )
        web.find_element(By.ID, ("txtCidade")).send_keys(cidade)
        WebDriverWait(web, 10).until(
                EC.presence_of_element_located((By.ID, "ddlUF"))
            )
        Select(web.find_element(By.ID, "ddlUF")
                ).select_by_value(Uf)
        if RECEITA == "100102":
            WebDriverWait(web, 10).until(
                    EC.presence_of_element_located((By.ID, "ddlTipoDebito"))
                )
            Select(web.find_element(By.ID, "ddlTipoDebito")
                    ).select_by_value('10101')
        
        else:
            WebDriverWait(web, 10).until(
                    EC.presence_of_element_located((By.ID, "ddlTipoDebito"))
                )
            Select(web.find_element(By.ID, "ddlTipoDebito")
                    ).select_by_value('24701')
            
        WebDriverWait(web, 10).until(
                EC.presence_of_element_located((By.ID, "txtReferencia"))
            )
        web.find_element(By.ID, "txtReferencia").send_keys(Referencia)
        WebDriverWait(web, 10).until(
                EC.presence_of_element_located((By.ID, "txtVencimento"))
            )
        web.find_element(By.ID, "txtVencimento").send_keys(datavencimento)
        WebDriverWait(web, 10).until(
                EC.presence_of_element_located((By.ID, "txtCampoEspecifico1"))
            )
        web.find_element(By.ID, "txtCampoEspecifico1").send_keys(Numero_NFE)
        WebDriverWait(web, 10).until(
                EC.presence_of_element_located((By.ID, "txtValorCalculo"))
            )
        web.find_element(By.ID, "txtValorCalculo").send_keys(VALOR_TOTAL)
        WebDriverWait(web, 10).until(
                EC.presence_of_element_located((By.ID, "txtObservacao"))
            )
            
        web.find_element(By.ID, "txtObservacao").send_keys(chave)
        WebDriverWait(web, 10).until(
                EC.presence_of_element_located((By.ID, "btnCalcular"))
            )
        sleep(1.5)
        web.find_element(By.ID, "btnCalcular").click()




















        try:
            while True:
                if not web.execute_script("return window.top.closed"):
                    time.sleep(1)
                else:
                    print("navegador fechado")
                    break
        except:
            print("OK")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Main()
    window.show()
    app.exec()
