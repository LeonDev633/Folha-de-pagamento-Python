from sqlalchemy import Column, Integer, Float, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from os import system
from dataclasses import dataclass

system("cls||clear")

BD = create_engine("sqlite:///bancodedados.db")

Session = sessionmaker(bind=BD)
session = Session()

Base = declarative_base()

@dataclass
class Trabalhador(Base):
    __tablename__ = "trabalhadores"
    nome = Column(String)
    sobrenome = Column(String)
    cpf = Column(Integer,primary_key=True)
    salario = Column(Float)
    dependente = Column(Integer)
    senha = Column(String)

def verificando_cpf():
    while True:
        cpf = int(input("Informe seu CPF"))
        id_usuario = session.query(Trabalhador).filter(Trabalhador.cpf == cpf)
        if id_usuario in None:
            break
        else:
            print("CPF já cadastrado")
    return cpf

def cadastro ():
    
    cpf = verificando_cpf()

    funcionario = Trabalhador(
        nome = input("Insira um nome: "),
        sobrenome = input("Insira um sobrenome: "),
        cpf = cpf,
        salario = float(input("Insira o salario bruto: ")),
        filhos = int(input("Informe a quantidade de filhos: ")),
        senha = input("Crie uma senha: ")
    )
    session.add(funcionario)
    session.commit()

def menu ():
    print("="*20)
    print("""
1- ADICIONAR FUNCIONARIO
2- CALCULO SALARIAL""")
    print("="*20)

def desconto_inss (salario):
    if salario <= 1100:
        desconto = (salario*0.075)
        return desconto
    elif salario <= 2203.48:
        desconto = (salario*0.09)
        return desconto
    elif salario <= 3305.22:
        desconto = (salario*0.12)
        return desconto
    elif salario <= 6433.57:
        desconto = (salario*0.14)
        return desconto
    else:
        desconto = 854.36
        return 

def imposto_de_renda(salario,dependentes):
    if salario <= 2259.20:
        deducao = 0
        desconto = 0
        return deducao, desconto 
    elif salario <= 2826.65:
        deducao = dependentes *189*59
        desconto = (salario*0.75)
        return deducao, desconto 
    elif salario <= 3751.05:
        deducao = dependentes *189*59
        desconto = (salario*0.15)
        return deducao, desconto 
    elif salario <= 4664.68:
        deducao = dependentes *189*59
        desconto = (salario*0.225)
        return deducao, desconto 
    else:
        deducao = dependentes *189*59
        desconto = (salario*0.275)
        return deducao, desconto 

while True:
    menu()
    opcao = int(input("Informe a opção desejada: "))
    if opcao == 1:
        while True:
            cadastro()
            opcao1 = int(input("Deseja adicionar outro funcionario ? \n1-SIM \n2-NÃO"))
            if opcao1 == 2:
                break
    elif opcao == 2:
        cpf_usuario = verificando_cpf()
        usuario = session.query(Trabalhador).filter_by(cpf = cpf_usuario)
        dependentes = usuario.depente
        salario_bruto = usuario.salario
        


    
    else:
        print("Opção invalida.")
