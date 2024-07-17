import json
import os
import beaupy
from datetime import datetime, timedelta
import re

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
                sub_menu_edicao(op)
            case 1:
                 # inserir novo sub menu de edição
                sub_menu_edicao(op)
            case 2:
                 # inserir novo sub  menu de edição
                 sub_menu_edicao(op)
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
                "1 - Pesquisa alugueres por Automóvel com ajuda", 
                "2 - Pesquisa alugueres por Automóvel",
                "3 - Pesquisa alugueres por Cliente com ajuda",    
                "4 - Pesquisa alugueres por Cliente",             
                "5 - Sair"
                  ]
    while True:
        op = beaupy.select(listaMenus, cursor="=>", cursor_style="red", return_index=True)
        match op:
            case 0:
                    # inserir função de listagem de alugueres por automóvel
                    sub_sub_menu_pesquisas(listAutomovel, 'matricula')
            case 1:
                    # inserir função de listagem de alugueres por automóvel
                    search_automovel()
            case 2:
                    # inserir função de listagem de alugueres por cliente 
                    sub_sub_menu_pesquisas(listCliente, 'nome') 
            case 3:
                    # inserir função de listagem de alugueres por cliente
                    search_cliente()             
            case 4:
                break
            case _:
                print("\nErro: opção inválida!\n")

def sub_sub_menu_pesquisas(lst, key):
    
    listMenus = list_menu(lst, key)
    while True:
        op = beaupy.select(listMenus, cursor="=>", cursor_style="red", return_index=True)
        match op:
                case _ if op < len(listMenus) -1:
                    pass
                    # inserir função que vai apresentar objeto e alugueres
                case _ if op == len(listMenus)-1:                    
                    break
                case _:
                    print("\nErro: opção inválida!\n")       


# Função sub menu edição com beaupy
def sub_menu_edicao(op_menu_listas):
    
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
                match op_menu_listas:
                    case 0:
                        new_item = get_item_data(op_menu_listas)
                        add_item(listCliente, new_item)   #função para adicionar novo cliente 
                        save_data('listcliente.json', listCliente)
                    case 1:
                        new_item = get_item_data(op_menu_listas)
                        add_item(listAutomovel, new_item)     #função novo automovel
                        save_data('listautomovel.json', listAutomovel)
                        # fazer o mesmo procedimento do ponto anterior
                    case 2:
                        new_item = get_item_data(op_menu_listas)
                        add_item(listBooking, new_item)        #função nobo booking
                        # fazer o mesmo procedimento do ponto anterior
                        save_data('listbooking.json', listBooking)
                    case _:
                        print("\nErro: opção inválida!\n")
                        # usar as funções que o Francisco alterou. è necessário passar do menú anterior por um parâmetro na função sub_menu_edicao
                        # o valor escolhido (cliente, automóvel ou booking) para criar um case e usar a função correta para introdução dos dados
            case 1:
                # lista=[]
                match op_menu_listas:
                    case 0:
                        lista=listCliente
                        id_to_update = int(input("Digite o ID do item a ser atualizado: ")) 
                        item_to_update = next((item for item in lista if item['id'] == id_to_update), None)
                        if item_to_update:
                            updated_data = update_item_data(item_to_update, op_menu_listas)
                            update_item(lista, id_to_update, updated_data)
                            print("Item atualizado com sucesso.")
                        else:
                            print(f"Item com ID {id_to_update} não encontrado.")
                        save_data('listcliente.json', lista)
                    case 1:
                        lista=listAutomovel
                        id_to_update = int(input("Digite o ID do item a ser atualizado: ")) 
                        item_to_update = next((item for item in lista if item['id'] == id_to_update), None)
                        if item_to_update:
                            updated_data = update_item_data(item_to_update, op_menu_listas)
                            update_item(lista, id_to_update, updated_data)
                            print("Item atualizado com sucesso.")
                        else:
                            print(f"Item com ID {id_to_update} não encontrado.")
                        save_data('listautomovel.json', lista)
                    case 2:
                        lista=listBooking
                        id_to_update = int(input("Digite o ID do item a ser atualizado: ")) 
                        item_to_update = next((item for item in lista if item['id'] == id_to_update), None)
                        if item_to_update:
                            updated_data = update_item_data(item_to_update, op_menu_listas)
                            update_item(lista, id_to_update, updated_data)
                            print("Item atualizado com sucesso.")
                        else:
                            print(f"Item com ID {id_to_update} não encontrado.")
                        save_data('listbooking.json', lista)
                    case _:
                        print("\nErro: opção inválida!\n")
                
            case 2:
                 match op_menu_listas:
                    case 0:
                        remove_item_main(listCliente,'listcliente.json')
                    case 1:
                        remove_item_main(listAutomovel,'listautomovel.json')
                    case 2:
                        remove_item_main(listBooking,'listbooking.json')
                    case _:
                        print("\nErro: opção inválida!\n")
            case 3:
                break
            case _:
                print("\nErro: opção inválida!\n")
                
def remove_item_main(lista, filename):
    id_to_remove = int(input("Digite o ID do item a ser removido: "))
    lista[:] = [item for item in lista if item['id'] != id]
    print("Item removido com sucesso.")
    save_data(filename, lista)

#funções do francisco 
def validate_date(date_text, format="%d-%m-%Y"):
    try:
        datetime.strptime(date_text, format)
        return True
    except ValueError:
        return False
 
def validate_email(email):
    regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(regex, email) is not None
 
def validate_nif(nif):
    return nif.isdigit() and len(nif) == 9
 
def validate_telefone(telefone):
    return telefone.isdigit() and len(telefone) in [9, 10]
 
def calculate_num_days(data_inicio, data_fim):
    start_date = datetime.strptime(data_inicio, "%Y-%m-%d")
    end_date = datetime.strptime(data_fim, "%Y-%m-%d")
    return (end_date - start_date).days
 
def get_item_data(item_type):
    if item_type == 0:
        while True:
            nome = input("Nome: ")
            while True:
                nif = input("NIF: ")
                if not validate_nif(nif):
                    print("NIF inválido. Deve ter 9 dígitos.")
                else:
                    break
            while True:
                dataNascimento = input("Data de Nascimento (DD-MM-AAAA): ")
                if not validate_date(dataNascimento):
                    print("Data de nascimento inválida. Use o formato DD-MM-AAAA.")
                else:
                    break
            while True:
                telefone = input("Telefone: ")
                if not validate_telefone(telefone):
                    print("Telefone inválido. Deve ter 9 ou 10 dígitos.")
                else:
                    break
            while True:
                email = input("Email: ")
                if not validate_email(email):
                    print("Email inválido.")
                else:
                    break
            break
 
        return {
            "nome": nome,
            "nif": nif,
            "dataNascimento": dataNascimento,
            "telefone": telefone,
            "email": email
        }
 
    elif item_type == 1:
        while True:
            matricula = input("Matrícula: ")
            marca = input("Marca: ")
            modelo = input("Modelo: ")
            cor = input("Cor: ")
            try:
                portas = int(input("Número de Portas: "))
                precoDiario = float(input("Preço Diário: "))
                cilindrada = int(input("Cilindrada: "))
                potencia = int(input("Potência: "))
                break
            except ValueError:
                print("Entrada inválida. Verifique se os valores numéricos foram digitados corretamente.")
                continue
 
        return {
            "matricula": matricula,
            "marca": marca,
            "modelo": modelo,
            "cor": cor,
            "portas": portas,
            "precoDiario": precoDiario,
            "cilindrada": cilindrada,
            "potencia": potencia
        }


def list_menu(lst, key):
    list_temp = [val[key] for val in lst if isinstance(val, dict) and key in val]
    list_temp.append('Sair')
    if list_temp:
        return list_temp
    else:
        return []


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
    
    if item_type == 2: #refere se ao booking
        # Recalcular numeroDias e precoReserva se as datas foram alteradas
        if updated_item['data_inicio'] != item['data_inicio'] or updated_item['data_fim'] != item['data_fim']:
            updated_item['numeroDias'] = calculate_num_days(updated_item['data_inicio'], updated_item['data_fim'])
            updated_item['precoReserva'] = calculate_booking_price(updated_item['numeroDias'], updated_item['automovel_id'])

    return updated_item

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
            bookings = [b for b in listBooking if int(b["automovel_id"]) == int(automovel["id"])]
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

main_menu2()