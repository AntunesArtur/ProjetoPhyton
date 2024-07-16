import json
import os
import beaupy
from datetime import datetime, timedelta

# Funções para carregar e salvar dados
def load_data(filename):
    filepath = f'data/{filename}'
    if not os.path.exists(filepath):
        print(f"Arquivo {filename} não encontrado. Criando novo arquivo.")
        return []
    with open(filepath, 'r') as file:
        content = file.read()
        if not content:
            print(f"Arquivo {filename} está vazio. Retornando lista vazia.")
            return []
        try:
            return json.loads(content)
        except json.JSONDecodeError as e:
            print(f"Erro ao decodificar {filename}: {e}")
            print("Retornando lista vazia.")
            return []

def save_data(filename, data):
    with open(f'data/{filename}', 'w') as file:
        json.dump(data, file, indent=2)

# Carregar dados
listCliente = load_data('listcliente.json')
listAutomovel = load_data('listautomovel.json')
listBooking = load_data('listbooking.json')

# Função para obter o próximo ID disponível
def get_next_id(lista):
    if not lista:
        return 1
    max_id = 0
    for item in lista:
        if 'id' in item and isinstance(item['id'], int) and item['id'] > max_id:
            max_id = item['id']
    return max_id + 1

# Funções de gerenciamento de listas
def add_item(lista, item):
    if 'id' not in item or not isinstance(item['id'], int):
        item['id'] = get_next_id(lista)
    lista.append(item)
    return item['id']

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
        print(f"ID: {cliente['id']}, Nome: {cliente['nome']}, NIF: {cliente['nif']},Data de Nascimento: {cliente['dataNascimento']}")

def list_automoveis():
    for automovel in listAutomovel:
        print(f"ID: {automovel['id']}, Matrícula: {automovel['matricula']}, Marca: {automovel['marca']}, Modelo: {automovel['modelo']}")

def list_bookings():
    for index, booking in enumerate(listBooking, start=1):
        cliente = next((c for c in listCliente if c['id'] == booking.get('cliente_id')), None)
        automovel = next((a for a in listAutomovel if a['id'] == booking.get('automovel_id')), None)
        if cliente and automovel:
            booking_id = booking.get('id', f"N/A (índice: {index})")
            print(f"ID: {booking_id}, Data início: {booking.get('data_inicio', 'N/A')} | "
                  f"Data fim: {booking.get('data_fim', 'N/A')} "
                  f"({booking.get('numeroDias', 'N/A')} dias)")
            print(f"Cliente: {cliente['nome']}")
            print(f"Automóvel: {automovel['marca']} - {automovel['matricula']}")
            print(f"Total: {booking.get('precoReserva', 'N/A')} €\n")

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
                #pass
                list_clientes()
            case 1:
                #pass
                list_automoveis()
            case 2:
                #pass
                list_bookings()
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
                search_automovel()
            case 1:
                search_cliente()
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
                new_item = get_item_data('cliente')
                add_item(listCliente, new_item)   #função para adicionar novo cliente 
                save_data('listcliente.json', listCliente)
            case 1:
                new_item = get_item_data('automóvel')
                add_item(listAutomovel, new_item)     #função novo automovel
                save_data('listautomovel.json', listAutomovel)
            case 2:
                new_item = get_item_data('booking')
                add_item(listBooking, new_item)        #função nobo booking
                save_data('listbooking.json', listBooking)
            case 3:
                break
            case _:
                print("\nErro: opção inválida!\n")
def manage_list(lista, filename, item_type):
    options = ["Adicionar", "Atualizar", "Remover", "Voltar"]
    list_clientes()
    
    while True:
        choice = display_menu(options)
        
        if choice == "Adicionar":
            new_item = get_item_data(item_type)
            new_id = add_item(lista, new_item)
            print(f"Item adicionado com ID: {new_id}")
        elif choice == "Atualizar":
            id_to_update = int(input("Digite o ID do item a ser atualizado: "))
            item_to_update = next((item for item in lista if item['id'] == id_to_update), None)
            if item_to_update:
                updated_data = update_item_data(item_to_update, item_type)
                update_item(lista, id_to_update, updated_data)
                print("Item atualizado com sucesso.")
            else:
                print(f"Item com ID {id_to_update} não encontrado.")
        elif choice == "Remover":
            id_to_remove = int(input("Digite o ID do item a ser removido: "))
            remove_item(lista, id_to_remove)
            print("Item removido com sucesso.")
        elif choice == "Voltar":
            break

    save_data(filename, lista)

def get_item_data(item_type):
    if item_type == 'cliente':
        return {
            "nome": input("Nome: "),
            "nif": input("NIF: "),
            "dataNascimento": input("Data de Nascimento (DD-MM-AAAA): "),
            "telefone": input("Telefone: "),
            "email": input("Email: ")
        }
    elif item_type == 'automóvel':
        return {
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
        data_inicio = input("Data de Início (AAAA-MM-DD): ")
        data_fim = input("Data de Fim (AAAA-MM-DD): ")
        cliente_id = int(input("ID do Cliente: "))
        automovel_id = int(input("ID do Automóvel: "))
        
        num_dias = calculate_num_days(data_inicio, data_fim)
        preco_reserva = calculate_booking_price(num_dias, automovel_id)
        
        return {
            "data_inicio": data_inicio,
            "data_fim": data_fim,
            "cliente_id": cliente_id,
            "automovel_id": automovel_id,
            "precoReserva": preco_reserva,
            "numeroDias": num_dias
        }

def update_item_data(item, item_type):
    updated_item = item.copy()
    print("Dados atuais:")
    for key, value in item.items():
        if key != 'id':
            print(f"{key}: {value}")
            if input(f"Deseja alterar o campo '{key}'? (s/n): ").lower() == 's':
                if key in ['portas', 'cilindrada', 'potencia']:
                    updated_item[key] = int(input(f"Novo valor para {key}: "))
                elif key == 'precoDiario':
                    updated_item[key] = float(input(f"Novo valor para {key}: "))
                else:
                    updated_item[key] = input(f"Novo valor para {key}: ")
    
    if item_type == 'booking':
        # Recalcular numeroDias e precoReserva se as datas foram alteradas
        if updated_item['data_inicio'] != item['data_inicio'] or updated_item['data_fim'] != item['data_fim']:
            updated_item['numeroDias'] = calculate_num_days(updated_item['data_inicio'], updated_item['data_fim'])
            updated_item['precoReserva'] = calculate_booking_price(updated_item['numeroDias'], updated_item['automovel_id'])

    return updated_item

def calculate_num_days(data_inicio, data_fim):
    d1 = datetime.strptime(data_inicio, "%Y-%m-%d")
    d2 = datetime.strptime(data_fim, "%Y-%m-%d")
    return (d2 - d1).days + 1

def calculate_booking_price(num_dias, automovel_id):
    automovel = next((a for a in listAutomovel if a['id'] == automovel_id), None)
    if not automovel:
        print("Automóvel não encontrado. Usando preço padrão.")
        preco_diario = 50  # Preço padrão
    else:
        preco_diario = automovel['precoDiario']
    
    preco_total = preco_diario * num_dias
    
    # Aplicar desconto
    if num_dias <= 4:
        desconto = 0
    elif 5 <= num_dias <= 8:
        desconto = 0.15
    else:
        desconto = 0.25
    
    return preco_total * (1 - desconto)

def search_automovel():
    matricula = input("Digite a matrícula do automóvel: ").upper()
    for automovel in listAutomovel:
        if automovel['matricula'].upper() == matricula:
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
        if cliente['nif'] == nif:
            print(f"Dados do cliente:")
            for key, value in cliente.items():
                print(f"{key}: {value}")
            print("\nÚltimos 5 alugueres:")
            bookings = [b for b in listBooking if b['cliente_id'] == cliente['id']]
            for booking in sorted(bookings, key=lambda x: x['data_inicio'], reverse=True)[:5]:
                print(f"Data: {booking['data_inicio']} a {booking['data_fim']}")
            return
    print("Cliente não encontrado.")

def fix_existing_data():
    global listCliente, listAutomovel, listBooking
    
    for lista in [listCliente, listAutomovel, listBooking]:
        for item in lista:
            if 'id' not in item:
                item['id'] = get_next_id(lista)
    
    save_data('listcliente.json', listCliente)
    save_data('listautomovel.json', listAutomovel)
    save_data('listbooking.json', listBooking)
    print("Dados existentes corrigidos e salvos.")


def funcao_teste():
    texto = 'atum-peixe'
    pesquisa = '-p'

    if pesquisa in texto:
        print("verdadeiro")
    else:
        print("falso")

def validate_input_string(msg): # em "msg" passar o texto a apre
    while True:
        try:
            val = input(msg)
        except:
            print(f"\nErro: Não inseriu o valor.\n")
        if not val.strip() == "": #para controlar se o campo está a vazio ou só com espaços
            return val
        else:            
            print(f"\nErro: Valor em branco. Tem de inserir um valor.\n")

def validate_input_int(msg):
    while True:
        try:
            val = int(input(msg))
            return val
        except:
            print(f"\nErro: deverá colocar um valor numérico.\n")

if __name__ == "__main__":
    # main_menu()
    main_menu2()