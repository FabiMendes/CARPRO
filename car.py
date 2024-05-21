# Importações das bibliotecas necessárias
from sqlalchemy.orm import declarative_base # Aqui importa a classe base para definição de classes de mapeamento
from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean # importa os tipos de colunas e chaves estrangeiras
from sqlalchemy import create_engine # imporyando a função para criar o engine do banco de dados
from sqlalchemy.orm import sessionmaker, relationship # importando as funções para criar sessões e definir relacionamentos
import sys # importando a biblioteca sys para interação com o sistema operacional
from tabulate import tabulate # importando a função p criar tabela formatada (a do terminal)
from art import text2art # importando a função text2art para criar arte ASCII a partir do texto

# Definição da base do SQLAlchemy
Base = declarative_base()

# Definição das classes representando as tabelas
class Carro(Base):
    __tablename__ = "Carros" #nome da tabela de carros

    placa = Column('PLACA', String, primary_key=True) #coluna para a placa de carros
    nome = Column('NOME', String) #nome do carro
    disponibilidade = Column('DISPONIBILIDADE', Boolean, default=True) #disponibilidade do car
    marca = Column('MARCA', String) #marca do carro

#relacionamento da tabela aluguel com carro
    alugueis = relationship("Aluguel", back_populates="carro")
    
# método para representação de texto da classe carro
    def __repr__(self):
        return f"<Carro(placa={self.placa}, nome={self.nome}, disponibilidade={self.disponibilidade}, marca={self.marca})>"

class Cliente(Base):
    __tablename__ = "Clientes" #nomeda tabela

    doc = Column('DOC', Integer, primary_key=True) #documento do cliente CNH
    nomecliente = Column('NOMECLIENTE', String) #coluna de nome do cliete e o tipo
    idade = Column('IDADE', Integer) 
    qntd = Column('QTND', Integer, default=0)

#relacionamento daa tabela aluguel com cliente
    alugueis = relationship("Aluguel", back_populates="cliente")

# método para representação de texto da classe carro
    def __repr__(self):
        return f"<Cliente(doc={self.doc}, nomecliente={self.nomecliente}, idade={self.idade}, qntd={self.qntd})>"

class Aluguel(Base):
    __tablename__ = "Aluguel" 
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    dias = Column('DIAS', Integer)
    valor = Column('VALOR', Float)
    cliente_id = Column('CLIENTE_ID', Integer, ForeignKey("Clientes.DOC"))
    carro_id = Column('CARRO_ID', String, ForeignKey("Carros.PLACA"))

#relação das tabelas cliente e carro
    cliente = relationship("Cliente", back_populates="alugueis")
    carro = relationship("Carro", back_populates="alugueis")

    def __repr__(self):
        return f"<Aluguel(id={self.id}, dias={self.dias}, valor={self.valor}, cliente_id={self.cliente_id}, carro_id={self.carro_id})>"

# Configuração do engine do banco de dados SQLite
engine = create_engine('sqlite:///carpro.db')

# Criação das tabelas no banco de dados
Base.metadata.create_all(engine)

# Criação da sessão
Session = sessionmaker(bind=engine)
session = Session()

# func p cadastrar o cliente
def cadastrar_cliente(nomecliente, doc, idade):
    try:
        # cria um novo objeto Cliente com os dados fornecidos
        novo_cliente = Cliente(nomecliente=nomecliente, doc=doc, idade=idade)
        # adc o novo cliente à sessão
        session.add(novo_cliente)
        # faz o commit para manter as mudanças no banco de dados
        session.commit()
        print(f"Cliente {nomecliente} cadastrado com sucesso!")
    except Exception as e:
        # se der erro, traz uma mensagem de erro e reverte a transação
        print(f"Erro ao cadastrar cliente: {e}")
        session.rollback()

def cadastrar_carro(placa, nome, marca, disponibilidade):
    try:
        print(f"Cadastrando carro: placa={placa}, nome={nome}, marca={marca}, disponibilidade={disponibilidade}")
        novo_carro = Carro(placa=placa, nome=nome, marca=marca, disponibilidade=disponibilidade)
        session.add(novo_carro)
        session.commit()
        print(f"Carro {nome} cadastrado com sucesso!")
    except Exception as e:
        print(f"Erro ao cadastrar carro: {e}")
        session.rollback()

def calcular_preco(dias):
    preco_dia = 100
    return preco_dia * dias

def consulta_geral():
    try:
        # Consulta todos os clientes, carros e aluguéis na sessão
        clientes = session.query(Cliente).all()
        carros = session.query(Carro).all()
        alugueis = session.query(Aluguel).all()
        return {
            # Retorna um dicionário contendo as listas de clientes, carros e aluguéis
            "clientes": clientes,
            "carros": carros,
            "alugueis": alugueis
        }
    except Exception as e:
        print(f"Erro na consulta geral: {e}")
        # se der ruim, vemm uma mensagem de erro e retorna None
        return None

def alugar_carro(cliente_id, carro_id, dias):
    try:
        # vê o cliente e o carro na sessão
        cliente = session.query(Cliente).filter_by(doc=cliente_id).first()
        carro = session.query(Carro).filter_by(placa=carro_id).first()
         # olha se o cliente e o carro existem
        if cliente and carro:
            if carro.disponibilidade: # olha se o carro está disponível para aluguel
                novo_aluguel = Aluguel( # calcula o valor do aluguel multiplicados pelos dias fornecidos
                    dias=dias, 
                    valor=calcular_preco(dias),
                    cliente_id=cliente.doc, 
                    carro_id=carro_id
                )
                carro.disponibilidade = False # altera o carro p indisponível
                cliente.qntd += 1  # muda a quantidade de aluguéis do cliente
                session.add(novo_aluguel) # coloca o novo aluguel à sessão
                session.commit()
                # traz uma mensagem de sucesso
                print(f"Carro da placa {carro_id} alugado para o cliente {cliente_id} por {dias} dias. Valor total: {novo_aluguel.valor}")
            else:
                print('O carro já está alugado')
        else:
            print("Aluguel não pode ser realizado. Verifique se o cliente e o carro existem e se o carro está disponível.")
    except Exception as e: #se der erro
        print(f"Erro ao alugar carro: {e}")
        session.rollback()

#def da func para devolver um carro alugado por um cliente
def devolver_carro(cliente_id, carro_id):
    try: #olha se o aluguel correspondente ao cliente e ao carro na sessão
        aluguel = session.query(Aluguel).filter_by(cliente_id=cliente_id, carro_id=carro_id).first() # vê se o aluguel existe
        if aluguel: # consulta o carro na sessão e marca como disponível
            carro = session.query(Carro).filter_by(placa=carro_id).first()
            carro.disponibilidade = True
            # consulta o cliente e atualiza a quantidade de aluguéis
            cliente = session.query(Cliente).filter_by(doc=cliente_id).first()
            cliente.qntd -= 1
            # tira o aluguel da sessão
            session.delete(aluguel)
            session.commit()
            print(f"Carro de placa {carro_id} devolvido pelo cliente {cliente_id}.")
        else:
            print("O carro não foi alugado por este cliente.")
    except Exception as e:
        print(f"Erro ao devolver carro: {e}")
        session.rollback()

def menu_cliente():
    while True:
        user_icon = """\n_👤_"""
        print(user_icon)
        print("\n1. Alugar Carro")
        print("2. Devolver Carro")
        print("3. Sair")
    
        opcao = input("\nEscolha uma opção: ")

        if opcao == "1":
            try:
                cliente_id = int(input('ID do Cliente: '))
                carro_id = input('Placa do Carro: ')
                dias = int(input('Dias: '))
                alugar_carro(cliente_id, carro_id, dias)
            except ValueError:
                print("Entrada inválida. Tente novamente.")
        elif opcao == "2":
            try:
                cliente_id = int(input('ID do Cliente: '))
                carro_id = input('Placa do Carro: ')
                devolver_carro(cliente_id, carro_id)
            except ValueError:
                print("Entrada inválida. Tente novamente.")
        elif opcao == "3":
            break
        else:
            print("Opção inválida, tente novamente.")

def menu_prestador():
    while True:
        road_car_icon = "\n_🚗_"

        print(road_car_icon)
        print("1. Cadastrar Cliente")
        print("2. Cadastrar Carro")
        print("3. Consultar Cliente")
        print("4. Consultar Carro")
        print("5. Sair")
    
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            try:
                nomecliente = input('Nome do Cliente: ')
                doc = int(input('Documento: '))
                idade = int(input('Idade: '))
                cadastrar_cliente(nomecliente, doc, idade)
            except ValueError:
                print("Entrada inválida. Tente novamente.")
        elif opcao == "2":
            try:
                placa = input('Placa: ')
                nome = input('Nome: ')
                disponibilidade = input('Disponibilidade (True/False): ') == 'True'
                marca = input('Marca: ')
                cadastrar_carro(placa, nome, marca, disponibilidade)
            except ValueError:
                print("Entrada inválida. Tente novamente.")
        elif opcao == "3":
            try:
                clientes = session.query(Cliente).all()
                tabela = [[cliente.doc, cliente.nomecliente, cliente.idade, cliente.qntd] for cliente in clientes]
                print(tabulate(tabela, headers=["Documento", "Nome", "Idade", "Quantidade"]))
            except Exception as e:
                print(f"Erro ao consultar clientes: {e}")
        elif opcao == "4":
            try:
                carros = session.query(Carro).all()
                tabela = [[carro.placa, carro.nome, carro.marca, carro.disponibilidade] for carro in carros]
                print(tabulate(tabela, headers=["Placa", "Nome", "Marca", "Disponibilidade"]))
            except Exception as e:
                print(f"Erro ao consultar carros: {e}")
        elif opcao == "5":
            break
        else:
            print("Opção inválida, tente novamente.")

def menu_principal():
    while True:
        print("" + text2art("CARPRO"))
        road_car_icon = "_____🚗_____"

        print(road_car_icon)

        print("\n1. Sou Cliente")

        print("2. Sou Prestador")
        print("3. Sair")
    
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            menu_cliente()
        elif opcao == "2":
            menu_prestador()
        elif opcao == "3":
            break
        else:
            print("Opção inválida, tente novamente.")

# Iniciar o menu principal
if __name__ == "__main__":
    menu_principal()
