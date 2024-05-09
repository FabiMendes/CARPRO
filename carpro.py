from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime, timedelta

Base = declarative_base()

class Carro(Base):
    __tablename__ = 'carro'
    id = Column(Integer, primary_key=True)
    modelo = Column(String)
    tipo = Column(String)  # Exemplo: SUV, Sedan, Hatchback
    disponivel = Column(Integer)

class Cliente(Base):
    __tablename__ = 'cliente'
    id = Column(Integer, primary_key=True)
    nome = Column(String)
    cpf = Column(String, unique=True)

class Aluguel(Base):
    __tablename__ = 'aluguel'
    id = Column(Integer, primary_key=True)
    cliente_id = Column(Integer, ForeignKey('cliente.id'))
    carro_id = Column(Integer, ForeignKey('carro.id'))
    data_inicio = Column(DateTime, default=datetime.now())
    data_fim = Column(DateTime)
    preco_total = Column(Integer)

    cliente = relationship("Cliente", back_populates="alugueis")
    carro = relationship("Carro", back_populates="alugueis")

    def calcular_preco(self):
        dias = (self.data_fim - self.data_inicio).days
        preco_dia = 100
        preco_seguro = 200
        self.preco_total = (preco_dia * dias) + preco_seguro

Cliente.alugueis = relationship("Aluguel", order_by=Aluguel.id, back_populates="cliente")
Carro.alugueis = relationship("Aluguel", order_by=Aluguel.id, back_populates="carro")

engine = create_engine('mysql://root:iMpct2v@localhost/carpro', echo=True)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# Exemplo de uso:

# Cadastro de cliente
cliente1 = Cliente(nome='João', cpf='12345678900')
session.add(cliente1)

# Cadastro de carro
carro1 = Carro(modelo='Fiat Argo', tipo='Hatchback', disponivel=1)
session.add(carro1)

# Aluguel de carro
aluguel1 = Aluguel(cliente_id=1, carro_id=1, data_fim=datetime.now() + timedelta(days=5))
aluguel1.calcular_preco()
session.add(aluguel1)

# Consulta geral de carros disponíveis
carros_disponiveis = session.query(Carro).filter(Carro.disponivel > 0).all()
for carro in carros_disponiveis:
    print(carro.modelo)

# Consulta de cliente pelo ID
cliente_id = 1
cliente = session.query(Cliente).filter(Cliente.id == cliente_id).first()
print(cliente.nome)

# Devolução de carro
aluguel_devolvido = session.query(Aluguel).filter(Aluguel.cliente_id == cliente_id).first()
carro_devolvido = session.query(Carro).filter(Carro.id == aluguel_devolvido.carro_id).first()
carro_devolvido.disponivel += 1
session.delete(aluguel_devolvido)

# Renovação de aluguel
renovar_aluguel = input("Deseja renovar o aluguel do carro? (sim/não): ")
if renovar_aluguel.lower() == 'sim':
    aluguel1.data_fim += timedelta(days=5)
    aluguel1.calcular_preco()
    session.commit()

# Exclusão de carro
carro_excluido = session.query(Carro).filter(Carro.id == 1).first()
session.delete(carro_excluido)

session.commit()
