import json
import os
import beaupy
from datetime import datetime, timedelta

# Constantes para tipos de itens
CLIENTE = 'cliente'
AUTOMOVEL = 'automóvel'
BOOKING = 'booking'

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
    max_id = max(item['id'] for item in lista if 'id' in item)
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
        print(f"ID: {cliente['id']}, Nome: {cliente['nome']}, NIF: {cliente['nif']}, Data de Nascimento: {cliente['dataNascimento']}")

def list_automoveis():
    for automovel in listAutomovel:
        print(f"ID: {automovel['id']}, Matrícula: {automovel['matricula']}, Marca: {automovel['marca']}, Modelo: {automovel['modelo']}")

def list_bookings():
    for booking in listBooking:
        cliente = next((c for c in listCliente if c['id'] == booking.get('cliente_id')), None)
        automovel = next((a for a in listAutomovel if a['id'] == booking.get('automovel_id')), None)
        
        print(f"ID: {booking.get('id', 'N/A')}, "
              f"Data início: {booking.get('data_inicio', 'N/A')} | "
              f"Data fim: {booking.get('data_fim', 'N/A')} "
              f"({booking.get('numeroDias', 'N/A')} dias)")
        
        if cliente:
            print(f"Cliente: {cliente['nome']}")
        else:
            print("Cliente: Não encontrado")
        
        if automovel:
            print(f"Automóvel: {automovel['marca']} - {automovel['matricula']}")
        else:
            print("Automóvel: Não encontrado")
        
        print(f"Total: {booking.get('precoReserva', 'N/A')} €\n")

# Funções de validação
def validate_input_string(msg):
    while True:
        val = input(msg).strip()
        if val:
            return val
        print("Erro: Valor em branco. Tem de inserir um valor.")

def validate_input_int(msg):
    while True:
        try:
            return int(input(msg))
        except ValueError:
            print("Erro: deverá colocar um valor numérico.")

def validate_input_float(msg):
    while True:
        try:
            return float(input(msg))
        except ValueError:
            print("Erro: deverá colocar um valor numérico (pode incluir casas decimais).")

def validate_input_date(msg):
    while True:
        date_str = input(msg)
        try:
            return datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            print("Erro: formato de data inválido. Use AAAA-MM-DD.")

# Função principal do menu
def main_menu():
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
                sub_menu_listas()
            case 1:
                sub_menu_listagens()
            case 2:
                sub_menu_pesquisas()
            case 3:
                break
            case _:
                print("\nErro: opção inválida!\n")

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
                list_clientes()
                if beaupy.confirm("Deseja editar clientes?"):
                    sub_menu_edicao(CLIENTE)
            case 1:
                list_automoveis()
                if beaupy.confirm("Deseja editar automóveis?"):
                    sub_menu_edicao(AUTOMOVEL)
            case 2:
                list_bookings()
                if beaupy.confirm("Deseja editar bookings?"):
                    sub_menu_edicao(BOOKING)
            case 3:
                break
            case _:
                print("\nErro: opção inválida!\n")

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
                list_clientes()
            case 1:
                list_automoveis()
            case 2:
                list_bookings()
            case 3:
                break
            case _:
                print("\nErro: opção inválida!\n")

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

def sub_menu_edicao(item_type):
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
                new_item = get_item_data(item_type)
                if item_type == CLIENTE:
                    add_item(listCliente, new_item)
                    save_data('listcliente.json', listCliente)
                elif item_type == AUTOMOVEL:
                    add_item(listAutomovel, new_item)
                    save_data('listautomovel.json', listAutomovel)
                elif item_type == BOOKING:
                    add_item(listBooking, new_item)
                    save_data('listbooking.json', listBooking)
                print(f"Novo {item_type} adicionado com sucesso.")
            case 1:
                id_to_update = validate_input_int(f"Digite o ID do {item_type} a ser atualizado: ")
                if item_type == CLIENTE:
                    item_to_update = next((item for item in listCliente if item['id'] == id_to_update), None)
                    if item_to_update:
                        updated_data = update_item_data(item_to_update, item_type)
                        update_item(listCliente, id_to_update, updated_data)
                        save_data('listcliente.json', listCliente)
                        print(f"Cliente atualizado com sucesso.")
                    else:
                        print(f"Cliente com ID {id_to_update} não encontrado.")
                elif item_type == AUTOMOVEL:
                    item_to_update = next((item for item in listAutomovel if item['id'] == id_to_update), None)
                    if item_to_update:
                        updated_data = update_item_data(item_to_update, item_type)
                        update_item(listAutomovel, id_to_update, updated_data)
                        save_data('listautomovel.json', listAutomovel)
                        print(f"Automóvel atualizado com sucesso.")
                    else:
                        print(f"Automóvel com ID {id_to_update} não encontrado.")
                elif item_type == BOOKING:
                    item_to_update = next((item for item in listBooking if item['id'] == id_to_update), None)
                    if item_to_update:
                        updated_data = update_item_data(item_to_update, item_type)
                        update_item(listBooking, id_to_update, updated_data)
                        save_data('listbooking.json', listBooking)
                        print(f"Booking atualizado com sucesso.")
                    else:
                        print(f"Booking com ID {id_to_update} não encontrado.")
            case 2:
                id_to_remove = validate_input_int(f"Digite o ID do {item_type} a ser removido: ")
                if item_type == CLIENTE:
                    remove_item(listCliente, id_to_remove)
                    save_data('listcliente.json', listCliente)
                elif item_type == AUTOMOVEL:
                    remove_item(listAutomovel, id_to_remove)
                    save_data('listautomovel.json', listAutomovel)
                elif item_type == BOOKING:
                    remove_item(listBooking, id_to_remove)
                    save_data('listbooking.json', listBooking)
                print(f"{item_type.capitalize()} removido com sucesso.")
            case 3:
                break
            case _:
                print("\nErro: opção inválida!\n")

def get_item_data(item_type):
    if item_type == CLIENTE:
        return {
            "nome": validate_input_string("Nome: "),
            "nif": validate_input_string("NIF: "),
            "dataNascimento": validate_input_date("Data de Nascimento (AAAA-MM-DD): ").strftime("%Y-%m-%d"),
            "telefone": validate_input_string("Telefone: "),
            "email": validate_input_string("Email: ")
        }
    elif item_type == AUTOMOVEL:
        return {
            "matricula": validate_input_string("Matrícula: "),
            "marca": validate_input_string("Marca: "),
            "modelo": validate_input_string("Modelo: "),
            "cor": validate_input_string("Cor: "),
            "portas": validate_input_int("Número de Portas: "),
            "precoDiario": validate_input_float("Preço Diário: "),
            "cilindrada": validate_input_int("Cilindrada: "),
            "potencia": validate_input_int("Potência: ")
        }
    elif item_type == BOOKING:
        data_inicio = validate_input_date("Data de Início (AAAA-MM-DD): ")
        data_fim = validate_input_date("Data de Fim (AAAA-MM-DD): ")
        cliente_id = validate_input_int("ID do Cliente: ")
        automovel_id = validate_input_int("ID do Automóvel: ")
        
        num_dias = calculate_num_days(data_inicio, data_fim)
        preco_reserva = calculate_booking_price(num_dias, automovel_id)
        
        return {
            "data_inicio": data_inicio.strftime("%Y-%m-%d"),
            "data_fim": data_fim.strftime("%Y-%m-%d"),
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
            if beaupy.confirm(f"Deseja alterar o campo '{key}'?"):
                if key in ['portas', 'cilindrada', 'potencia']:
                    updated_item[key] = validate_input_int(f"Novo valor para {key}: ")
                elif key == 'precoDiario':
                    updated_item[key] = validate_input_float(f"Novo valor para {key}: ")
                elif key in ['data_inicio', 'data_fim', 'dataNascimento']:
                    updated_item[key] = validate_input_date(f"Novo valor para {key} (AAAA-MM-DD): ").strftime("%Y-%m-%d")
                else:
                    updated_item[key] = validate_input_string(f"Novo valor para {key}: ")
    
    if item_type == BOOKING:
        # Recalcular numeroDias e precoReserva se as datas foram alteradas
        if updated_item['data_inicio'] != item['data_inicio'] or updated_item['data_fim'] != item['data_fim']:
            updated_item['numeroDias'] = calculate_num_days(datetime.strptime(updated_item['data_inicio'], "%Y-%m-%d").date(),
                                                           datetime.strptime(updated_item['data_fim'], "%Y-%m-%d").date())
            updated_item['precoReserva'] = calculate_booking_price(updated_item['numeroDias'], updated_item['automovel_id'])

    return updated_item

def calculate_num_days(data_inicio, data_fim):
    return (data_fim - data_inicio).days + 1

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
    matricula = validate_input_string("Digite a matrícula do automóvel: ").upper()
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
    nif = validate_input_string("Digite o NIF do cliente: ")
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

if __name__ == "__main__":
    fix_existing_data()
    main_menu()