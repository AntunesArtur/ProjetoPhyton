import json
import os
from datetime import datetime, timedelta
from beaupy import select

# Funções para carregar e salvar dados

# def load_data(filename):
#     with open(f'data/{filename}', 'r') as file:
#         return json.load(file)

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
        cliente = next(c for c in listCliente if c['id'] == booking['cliente_id'])
        automovel = next(a for a in listAutomovel if a['id'] == booking['automovel_id'])
        print(f"Booking data início: {booking['data_inicio']} | data fim: {booking['data_fim']} ({booking['numeroDias']} dias)")
        print(f"Cliente: {cliente['nome']}")
        print(f"Automóvel: {automovel['marca']} - {automovel['matricula']}")
        print(f"Total: {booking['precoReserva']} €\n")

# Função principal do menu
# def main_menu():
#     while True:
#         choice = select(
#             "Selecione uma opção:",
#             [
#                 "Gerenciar Clientes",
#                 "Gerenciar Automóveis",
#                 "Gerenciar Bookings",
#                 "Listar Clientes",
#                 "Listar Automóveis",
#                 "Listar Bookings",
#                 "Pesquisar Automóvel",
#                 "Pesquisar Cliente",
#                 "Sair"
#             ]
#         )

#         if choice == "Gerenciar Clientes":
#             manage_list(listCliente, 'listcliente.json')
#         elif choice == "Gerenciar Automóveis":
#             manage_list(listAutomovel, 'listautomovel.json')
#         elif choice == "Gerenciar Bookings":
#             manage_list(listBooking, 'listbooking.json')
#         elif choice == "Listar Clientes":
#             list_clientes()
#         elif choice == "Listar Automóveis":
#             list_automoveis()
#         elif choice == "Listar Bookings":
#             list_bookings()
#         elif choice == "Pesquisar Automóvel":
#             search_automovel()
#         elif choice == "Pesquisar Cliente":
#             search_cliente()
#         elif choice == "Sair":
#             break

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
        choice = select("Selecione uma opção:", options)

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








def manage_list(lista, filename):
    while True:
        choice = select(
            "Selecione uma opção:",
            ["Adicionar", "Atualizar", "Remover", "Voltar"]
        )

        if choice == "Adicionar":
            # Implementar adição de item
            pass
        elif choice == "Atualizar":
            # Implementar atualização de item
            pass
        elif choice == "Remover":
            # Implementar remoção de item
            pass
        elif choice == "Voltar":
            break

    save_data(filename, lista)

def search_automovel():
    # Implementar pesquisa de automóvel
    pass

def search_cliente():
    # Implementar pesquisa de cliente
    pass

if __name__ == "__main__":
    main_menu()