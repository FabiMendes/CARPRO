class Veiculo:
    def _init_(self, modelo, ano, preco_diaria):
        self.modelo = modelo
        self.ano = ano
        self.preco_diaria = preco_diaria
        self.alugado = False

    def alugar(self):
        if not self.alugado:
            self.alugado = True
            print(f"{self.modelo} alugado com sucesso!")
        else:
            print(f"{self.modelo} já está alugado.")

    def devolver(self):
        if self.alugado:
            self.alugado = False
            print(f"{self.modelo} devolvido com sucesso!")
        else:
            print(f"{self.modelo} não está alugado.")

    


class Carro(Veiculo):
    def _init_(self, modelo, ano, preco_diaria, cor, marca, transmissao, tipo_combustivel):
        super()._init_(modelo, ano, preco_diaria)
        self.cor = cor
        self.marca = marca
        self.transmissao = transmissao
        self.tipo_combustivel = tipo_combustivel

    def _str_(self):
        return (f"Modelo: {self.modelo}, Ano: {self.ano}, Preço Diária: {self.preco_diaria}, "
                f"Cor: {self.cor}, Marca: {self.marca}, Transmissão: {self.transmissao}, "
                f"Tipo Combustível: {self.tipo_combustivel}")

class Locadora:
    def _init_(self):
        self.veiculos = {}
        self.clientes = {}

    def adicionar_veiculo(self, veiculo):
        self.veiculos[veiculo.modelo] = veiculo
        print(f"Veículo {veiculo.modelo} adicionado à locadora.")

    def excluir_veiculo(self, modelo):
        if modelo in self.veiculos:
            del self.veiculos[modelo]
            print(f"Veículo {modelo} excluído da locadora.")
        else:
            print("Veículo não encontrado na locadora.")

    def alugar_veiculo(self, modelo):
        if modelo in self.veiculos:
            veiculo = self.veiculos[modelo]
            veiculo.alugar()
        else:
            print("Veículo não encontrado na locadora.")

    def devolver_veiculo(self, modelo):
        if modelo in self.veiculos:
            veiculo = self.veiculos[modelo]
            veiculo.devolver()
        else:
            print("Veículo não encontrado na locadora.")

    def adicionar_cliente(self, nome, sobrenome, idade):
        cliente = cadastrar_cliente(nome, sobrenome, idade)
        self.clientes[nome + " " + sobrenome] = cliente
        print(f"Cliente {nome} {sobrenome} adicionado à locadora.")

    def excluir_cliente(self, nome):
        if nome in self.clientes:
            del self.clientes[nome]
            print(f"Cliente {nome} removido da locadora.")
        else:
            print("Cliente não encontrado na locadora.")

class cadastrar_cliente:
    def _init_(self, nome, sobrenome, idade):
        self.nome = nome
        self.sobrenome = sobrenome
        self.idade = idade

    def pessoa(self):
        if self.idade < 18:
            print("Você não pode alugar um carro.")
        else:
            print("Você pode alugar um carro.")


def menu(locadora):
    while True:
        print("\nSistema de Locadora de Veículos")
        print("1. Adicionar Veículo")
        print("2. Alugar Veículo")
        print("3. Devolver Veículo")
        print("4. Adicionar Cliente")
        print("5. Excluir Cliente")
        print("6. Sair")

        opcao = input("\nEscolha uma opção: ")

        if opcao == "1":
            modelo = input("Digite o modelo do veículo: ")
            ano = input("Digite o ano do veículo: ")
            preco_diaria = input("Digite o preço da diária do veículo: ")
            cor = input("Digite a cor do veículo: ")
            marca = input("Digite a marca do veículo: ")
            transmissao = input("Digite o tipo de transmissão do veículo: ")
            tipo_combustivel = input("Digite o tipo de combustível do veículo: ")
            carro = Carro(modelo, ano, preco_diaria, cor, marca, transmissao, tipo_combustivel)
            locadora.adicionar_veiculo(carro)

        # Implemente as outras opções do menu de acordo com as funcionalidades do seu sistema

        elif opcao == "6":
            print("Saindo do sistema. Até logo!")
            break

        else:
            print("Opção inválida. Por favor, escolha uma opção válida.")

