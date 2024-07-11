import json
import os
import beaupy
from datetime import datetime, timedelta

# Funções para carregar e salvar dados
def load_data(filename):
    filepath = f'data/{filename}'
    if not os.path.exists(filepath):
        return []
    with open(filepath, 'r') as file:
        content = file.read()
        if not content:
            return []
        return json.loads(content)

def save_data(filename, data):
    with open(f'data/{filename}', 'w') as file:
        json.dump(data, file, indent=2)

# Carregar dados
listCliente = load_data('listcliente.json')
listAutomovel = load_data('listautomovel.json')
listBooking = load_data('listbooking.json')

# Funções de gerenciamento de listas
def add_item(lista, item):
    lista.append(item)

def update_item(lista, id, new_data):
    for item in lista:
        if item['id'] == id:
            item.update(new_data)
            break

def remove_item(lista, id):
    lista[:] = [item for item in lista if item['id'] != id]

# Funções de listagem
def list_clientes():
    for cliente in listCliente:
        print(f"ID: {cliente['id']}, Nome: {cliente['nome']}, NIF: {cliente['nif']}")

def list_automoveis():
    for automovel in listAutomovel:
        print(f"ID: {automovel['id']}, Matrícula: {automovel['matricula']}, Marca: {automovel['marca']}, Modelo: {automovel['modelo']}")

def list_bookings():
    for booking in listBooking:
        cliente = next((c for c in listCliente if c['id'] == booking['cliente_id']), None)
        automovel = next((a for a in listAutomovel if a['id'] == booking['automovel_id']), None)
        if cliente and automovel:
            print(f"Booking data início: {booking['data_inicio']} | data fim: {booking['data_fim']} ({booking['numeroDias']} dias)")
            print(f"Cliente: {cliente['nome']}")
            print(f"Automóvel: {automovel['marca']} - {automovel['matricula']}")
            print(f"Total: {booking['precoReserva']} €\n")

# Função para exibir menu e obter escolha
def display_menu(options):
    for i, option in enumerate(options, 1):
        print(f"{i}. {option}")
    while True:
        try:
            choice = int(input("Escolha uma opção: "))
            if 1 <= choice <= len(options):
                return options[choice - 1]
            else:
                print("Opção inválida. Tente novamente.")
        except ValueError:
            print("Por favor, digite um número.")

# Função principal do menu
def main_menu():
    options = [
        "Gerenciar Clientes",
        "Gerenciar Automóveis",
        "Gerenciar Bookings",
        "Listar Clientes",
        "Listar Automóveis",
        "Listar Bookings",
        "Pesquisar Automóvel",
        "Pesquisar Cliente",
        "Sair"
    ]   
    while True:
        choice = display_menu(options)
        
        if choice == "Gerenciar Clientes":
            manage_list(listCliente, 'listcliente.json', 'cliente')
        elif choice == "Gerenciar Automóveis":
            manage_list(listAutomovel, 'listautomovel.json', 'automóvel')
        elif choice == "Gerenciar Bookings":
            manage_list(listBooking, 'listbooking.json', 'booking')
        elif choice == "Listar Clientes":
            list_clientes()
        elif choice == "Listar Automóveis":
            list_automoveis()
        elif choice == "Listar Bookings":
            list_bookings()
        elif choice == "Pesquisar Automóvel":
            search_automovel()
        elif choice == "Pesquisar Cliente":
            search_cliente()
        elif choice == "Sair":
            break

# Função principal do menu com beaupy
def main_menu2():   
    
    listaMenus = [
                "1 - Gerir Listas", 
                "2 - Listagens",
                "3 - Pesquisas",
                "4 - Sair"
                  ]
    while True:
        op = beaupy.select(listaMenus, cursor="=>", cursor_style="red", return_index=True)
        match op:
            case 0:
                # inserir novo sub menu com listas
                sub_menu_listas()
            case 1:
                #inserir novo sub menu com tipos listagens
                sub_menu_listagens()
            case 2:
                #inserir novo sub menu com tipos pesquisas
                sub_menu_pesquisas()
            case 3:
                break
            case _:
                print("\nErro: opção inválida!\n")

# Função sub menu listas com beaupy
def sub_menu_listas():   
    
    listaMenus = [
                "1 - Clientes", 
                "2 - Automóveis",
                "3 - Bookings",
                "4 - Sair"
                  ]
    while True:
        op = beaupy.select(listaMenus, cursor="=>", cursor_style="red", return_index=True)
        match op:
            case 0:
                # inserir novo sub menu de edição
                sub_menu_edicao()
            case 1:
                 # inserir novo sub menu de edição
                sub_menu_edicao()
            case 2:
                 # inserir novo sub  menu de edição
                 sub_menu_edicao()
            case 3:
                break
            case _:
                print("\nErro: opção inválida!\n")

# Função sub menu listagens com beaupy
def sub_menu_listagens():   
    
    listaMenus = [
                "1 - Listagem de Clientes", 
                "2 - Listagem de Automóveis",
                "3 - Listagem de Bookings",
                "4 - Sair"
                  ]
    while True:
        op = beaupy.select(listaMenus, cursor="=>", cursor_style="red", return_index=True)
        match op:
            case 0:
                pass
                # inserir função de listagem de clientes
            case 1:
                pass
                 # inserir função de listagem de automóveis
            case 2:
                pass
                 # inserir função de listagem de bookings
            case 3:
                break
            case _:
                print("\nErro: opção inválida!\n")

# Função sub menu Pesquisas com beaupy
def sub_menu_pesquisas():   
    
    listaMenus = [
                "1 - Pesquisa alugueres por Automóvel", 
                "2 - Pesquisa alugueres por Cliente",                
                "3 - Sair"
                  ]
    while True:
        op = beaupy.select(listaMenus, cursor="=>", cursor_style="red", return_index=True)
        match op:
            case 0:
                pass
                # inserir função de listagem de alugueres por automóvel
            case 1:
                pass
                 # inserir função de listagem de alugueres por cliente            
            case 2:
                break
            case _:
                print("\nErro: opção inválida!\n")

# Função sub menu edição com beaupy
def sub_menu_edicao():   
    
    listaMenus = [
                "1 - Novo", 
                "2 - Atualizar",
                "3 - Remover",
                "4 - Sair"
                  ]
    while True:
        op = beaupy.select(listaMenus, cursor="=>", cursor_style="red", return_index=True)
        match op:
            case 0:
                pass
                # inserir função para inserir novo cliente automóvel ou booking
            case 1:
                pass
                 # inserir função para alterar cliente automóvel ou booking
            case 2:
                pass
                 # inserir função para remover cliente automóvel ou booking
            case 3:
                break
            case _:
                print("\nErro: opção inválida!\n")

def manage_list(lista, filename, item_type):
    options = ["Adicionar", "Atualizar", "Remover", "Voltar"]
    
    while True:
        choice = display_menu(options)
        
        if choice == "Adicionar":
            new_item = get_item_data(item_type)
            add_item(lista, new_item)
        elif choice == "Atualizar":
            id_to_update = input("Digite o ID do item a ser atualizado: ")
            updated_data = get_item_data(item_type, update=True)
            update_item(lista, id_to_update, updated_data)
        elif choice == "Remover":
            id_to_remove = input("Digite o ID do item a ser removido: ")
            remove_item(lista, id_to_remove)
        elif choice == "Voltar":
            break

    save_data(filename, lista)

def get_item_data(item_type, update=False):
    if item_type == 'cliente':
        return {
            "id": input("ID: ") if not update else None,
            "nome": input("Nome: "),
            "nif": input("NIF: "),
            "dataNascimento": input("Data de Nascimento (DD-MM-AAAA): "),
            "telefone": input("Telefone: "),
            "email": input("Email: ")
        }
    elif item_type == 'automóvel':
        return {
            "id": input("ID: ") if not update else None,
            "matricula": input("Matrícula: "),
            "marca": input("Marca: "),
            "modelo": input("Modelo: "),
            "cor": input("Cor: "),
            "portas": int(input("Número de Portas: ")),
            "precoDiario": float(input("Preço Diário: ")),
            "cilindrada": int(input("Cilindrada: ")),
            "potencia": int(input("Potência: "))
        }
    elif item_type == 'booking':
        return {
            "data_inicio": input("Data de Início (AAAA-MM-DD): "),
            "data_fim": input("Data de Fim (AAAA-MM-DD): "),
            "cliente_id": input("ID do Cliente: "),
            "automovel_id": input("ID do Automóvel: "),
            "precoReserva": calculate_booking_price(),
            "numeroDias": calculate_num_days()
        }

def calculate_booking_price():
    # Implementar cálculo do preço da reserva com desconto
    return 0  # Placeholder

def calculate_num_days():
    # Implementar cálculo do número de dias da reserva
    return 0  # Placeholder

def search_automovel():
    matricula = input("Digite a matrícula do automóvel: ")
    for automovel in listAutomovel:
        if automovel['matricula'] == matricula:
            print(f"Dados do automóvel:")
            for key, value in automovel.items():
                print(f"{key}: {value}")
            print("\nÚltimos 5 alugueres:")
            bookings = [b for b in listBooking if b['automovel_id'] == automovel['id']]
            for booking in sorted(bookings, key=lambda x: x['data_inicio'], reverse=True)[:5]:
                print(f"Data: {booking['data_inicio']} a {booking['data_fim']}")
            return
    print("Automóvel não encontrado.")

def search_cliente():
    nif = input("Digite o NIF do cliente: ")
    for cliente in listCliente:
        if str(cliente['nif']) == nif:
            print(f"Dados do cliente:")
            for key, value in cliente.items():
                print(f"{key}: {value}")
            print("\nÚltimos 5 alugueres:")
            bookings = [b for b in listBooking if b['cliente_id'] == cliente['id']]
            for booking in sorted(bookings, key=lambda x: x['data_inicio'], reverse=True)[:5]:
                print(f"Data: {booking['data_inicio']} a {booking['data_fim']}")
            return
    print("Cliente não encontrado.")

if __name__ == "__main__":
    # main_menu()
    main_menu2()