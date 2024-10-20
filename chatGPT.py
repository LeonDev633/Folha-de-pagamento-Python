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
    nome: str
    sobrenome: str
    cpf: str  # CPF como string
    salario: float
    dependente: int
    senha: str
    
    nome = Column(String)
    sobrenome = Column(String)
    cpf = Column(String, primary_key=True)
    salario = Column(Float)
    dependente = Column(Integer)
    senha = Column(String)

Base.metadata.create_all(BD)

def verificando_cpf():
    while True:
        cpf = input("Informe seu CPF: ")  # CPF tratado como string
        id_usuario = session.query(Trabalhador).filter(Trabalhador.cpf == cpf).first()

        if id_usuario is None:  # CPF não cadastrado
            break
        else:
            print("CPF já cadastrado")
    
    return cpf

def cadastro():
    cpf = verificando_cpf()

    funcionario = Trabalhador(
        nome=input("Insira um nome: "),
        sobrenome=input("Insira um sobrenome: "),
        cpf=cpf,
        salario=float(input("Insira o salário bruto: ")),
        dependente=int(input("Informe a quantidade de dependentes: ")),
        senha=input("Crie uma senha: ")
    )
    session.add(funcionario)
    session.commit()

def menu():
    print("=" * 20)
    print("""
1- ADICIONAR FUNCIONARIO
2- CALCULO SALARIAL""")
    print("=" * 20)

def desconto_inss(salario):
    if salario <= 1100:
        desconto = salario * 0.075
    elif salario <= 2203.48:
        desconto = salario * 0.09
    elif salario <= 3305.22:
        desconto = salario * 0.12
    elif salario <= 6433.57:
        desconto = salario * 0.14
    else:
        desconto = 854.36
    return desconto

def imposto_de_renda(salario, dependentes):
    deducao = dependentes * 189
    if salario <= 2259.20:
        desconto = 0
    elif salario <= 2826.65:
        desconto = salario * 0.075
    elif salario <= 3751.05:
        desconto = salario * 0.15
    elif salario <= 4664.68:
        desconto = salario * 0.225
    else:
        desconto = salario * 0.275
    return deducao, desconto

while True:
    menu()
    opcao = int(input("Informe a opção desejada: "))
    if opcao == 1:
        while True:
            cadastro()
            opcao1 = int(input("Deseja adicionar outro funcionário? \n1-SIM \n2-NÃO: "))
            if opcao1 == 2:
                break
    elif opcao == 2:
        cpf_usuario = input("Informe seu CPF: ")
        usuario = session.query(Trabalhador).filter_by(cpf=cpf_usuario).first()
        if usuario:
            senha = input("Informe sua senha: ")
            if senha == usuario.senha:
                dependentes = usuario.dependente
                salario_bruto = usuario.salario
                inss = desconto_inss(salario_bruto)
                deducao, desconto = imposto_de_renda(salario_bruto, dependentes)
                salario_liquido = salario_bruto - inss - desconto + deducao
                print(f"Salário Líquido: R$ {salario_liquido:.2f}")
            else:
                print("Senha incorreta.")
        else:
            print("Usuário não encontrado.")
    else:
        print("Opção inválida.")
