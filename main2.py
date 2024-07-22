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

def update_item(lista, id, new_data):
    for item in lista:
        if item['id'] == id:
            item.update(new_data)
            break

# Funções de listagem
def list_clientes():
    # Cabeçalho com largura fixa para cada coluna
    print(f"{'ID':<5} {'Nome':<20} {'NIF':<10} {'Data de Nascimento':<15}")
    # Dados formatados
    for cliente in listCliente:
        print(f"{cliente['id']:<5} {cliente['nome']:<20} {cliente['nif']:<10} {cliente['dataNascimento']:<15}")
    # for cliente in listCliente:
    #     print(f"ID: {cliente['id']}, Nome: {cliente['nome']}, NIF: {cliente['nif']},Data de Nascimento: {cliente['dataNascimento']}")

def list_automoveis():
    for automovel in listAutomovel:
        print(f"ID: {automovel['id']}, Matrícula: {automovel['matricula']}, Marca: {automovel['marca']}, Modelo: {automovel['modelo']}")

def list_bookings():
    # Obtém a data atual
    data_atual = datetime.now().date()
    
    for booking in listBooking:
        # Converte a data de início do booking para um objeto date
        data_inicio = datetime.strptime(booking.get('data_inicio', ''), "%Y-%m-%d").date()
        
        # Verifica se a data de início é futura
        if data_inicio > data_atual:
            cliente = next((c for c in listCliente if c['id'] == booking.get('cliente_id')), None)
            automovel = next((a for a in listAutomovel if a['id'] == booking.get('automovel_id')), None)
            
            if cliente and automovel:
                print(f"Booking data início: {booking.get('data_inicio', 'N/A')} | "
                      f"data fim: {booking.get('data_fim', 'N/A')} "
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
        print()
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

# Função sub menu listas com beaupy
def sub_menu_listas():   
    listaMenus = [
                "1 - Clientes", 
                "2 - Automóveis",
                "3 - Bookings",
                "4 - Sair"
                  ]
    while True:
        print()
        op = beaupy.select(listaMenus, cursor="=>", cursor_style="red", return_index=True)
        match op:
            case 0:
                sub_menu_edicao(op)
            case 1:
                sub_menu_edicao(op)
            case 2:
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
        print()
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
        print()
        op = beaupy.select(listaMenus, cursor="=>", cursor_style="red", return_index=True)
        match op:
            case 0:
                    sub_sub_menu_pesquisas(listAutomovel, 'matricula', op)
            case 1:
                    matricula = input_matricula()
                    search_automovel(matricula)
            case 2:
                    sub_sub_menu_pesquisas(listCliente, 'nome', op) 
            case 3:
                    nif = input_nif()
                    search_cliente(nif, listAutomovel)             
            case 4:
                break
            case _:
                print("\nErro: opção inválida!\n")

def sub_sub_menu_pesquisas(lst, key, op_menu):    
    listFiltrated = list_filtrated(lst, key)
    listMenus = list_menu(listFiltrated, key)
    while True:
        print()
        op = beaupy.select(listMenus, cursor="=>", cursor_style="red", return_index=True)
        match op:
                case _ if op < len(listMenus) -1:
                    #para opção "Pesquisa alugueres por Automóvel com ajuda"
                    if op_menu == 0: 
                        item_value = listMenus[op]
                        search_automovel(item_value)
                    #para opção "Pesquisa alugueres por Cliente com ajuda"
                    if op_menu == 2:
                        item_value = listFiltrated[op]['nif']
                        search_cliente(item_value, listAutomovel)
                case _ if op == len(listMenus)-1:
                    break
                case _:
                    print("\nErro: opção inválida!\n")

def menu_pesquisas_id(lst, key):
    listFiltrated = list_filtrated(lst, key)
    listMenus = list_menu(listFiltrated, key)
    while True:
        print()
        op = beaupy.select(listMenus, cursor="=>", cursor_style="red", return_index=True)
        match op:
                case _ if op < len(listMenus) -1:
                    item_value = listFiltrated[op]["id"]
                    return item_value
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
        print()
        op = beaupy.select(listaMenus, cursor="=>", cursor_style="red", return_index=True)
        match op:
            case 0:
                match op_menu_listas:
                    case 0:
                        new_item = get_item_data(op_menu_listas)
                        add_item(listCliente, new_item)
                        save_data('listcliente.json', listCliente)
                    case 1:
                        new_item = get_item_data(op_menu_listas)
                        add_item(listAutomovel, new_item)
                        save_data('listautomovel.json', listAutomovel)
                    case 2:
                        new_item = get_item_data(op_menu_listas)
                        add_item(listBooking, new_item)
                        save_data('listbooking.json', listBooking)
                    case _:
                        print("\nErro: opção inválida!\n")
            case 1:
                match op_menu_listas:
                    case 0:
                        update_item_menu(listCliente, "listcliente.json", op_menu_listas,"nome")
                    case 1:
                        update_item_menu(listAutomovel, "listautomovel.json", op_menu_listas,"matricula")
                    case 2:
                        update_item_menu(listBooking, "listbooking.json", op_menu_listas,"id")
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

#Funções para atualização de dados nos ficheiros
def update_item_menu(list,filename,op_menu_listas,key):
    lista=list
    #id_to_update = int(input("Digite o ID do item a ser atualizado: "))
    id_to_update = menu_pesquisas_id(lista, key)
    item_to_update = next((item for item in lista if item['id'] == id_to_update), None)
    if item_to_update:
        updated_data = update_item_data(item_to_update, op_menu_listas)
        update_item(lista, id_to_update, updated_data)
        print("Item atualizado com sucesso.")
        save_data(filename, lista)
    else:
        print(f"Item com ID {id_to_update} não encontrado.")

def remove_item_main(lista, filename):
    id_to_remove = int(input("Digite o ID do item a ser removido: "))
    lista[:] = [item for item in lista if item['id'] != id_to_remove]
    print("Item removido com sucesso.")
    save_data(filename, lista)

#funções do francisco validação de dados
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

def validate_matricula(matricula):
    matpattern = r'^[A-Z]{2}-\d{2}-[A-Z]{2}$'
    if re.match(matpattern, matricula): # alterar para permitir maiúsculas e minúsculas if re.match(matpattern, matricula, re.IGNORECASE):
        return True
    else:
        return False

 #Recolhe e valida dados para o novo item (cliente, automovel ou booking)
def get_item_data(item_type):
    if item_type == 0:
        while True: #em principio este ciclo não é necessario 
            nome = input("Nome: ") # convém validar se o nome não fica a vazio
            while True:
                nif = input("NIF: ")
                if not validate_nif(nif):
                    print("NIF inválido. Deve ter 9 dígitos.")
                else:
                    list = [val["nif"] for val in listCliente]
                    if nif in list:
                        print("NIF existente.")
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
                    list = [val["telefone"] for val in listCliente]
                    if telefone in list:
                        print("Telefone existente.")
                    else:
                        break
            while True:
                email = input("Email: ")
                if not validate_email(email):
                    print("Email inválido.")
                else:
                    list = [val["email"] for val in listCliente]
                    if email in list:
                        print("E-mail existente.")
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
 
    if item_type == 1:
        while True:
            while True:
                matricula = input("Matrícula: ")
                if not validate_matricula(matricula):
                    print("Matrícula inválida.")
                else:
                    list = [val["matricula"] for val in listAutomovel]
                    if matricula in list:
                        print("Matricula existente.")
                    else:
                        break
            modelo = input("Modelo: ")
            while not modelo:
                print("Modelo não pode estar vazio.")
                modelo = input("Modelo: ")
            marca = input("Marca: ")  
            while not marca:
                print("Marca não pode estar vazia.")
                marca = input("Marca: ")
            cor = input("Cor: ")
            while not cor:
                print("Cor não pode estar vazia.")
                cor = input("Cor: ")
            while True:
                try:
                    portas = int(input("Número de Portas: "))
                    if portas <= 0:
                        print("O número de portas deve ser maior que zero.")
                    else:
                        break
                except ValueError:
                    print("Por favor, insira um número inteiro válido para o número de portas.")
            while True:
                try:
                    precoDiario = float(input("Preço Diário: "))
                    if precoDiario <= 0:
                        print("O preço diário deve ser maior que zero.")
                    else:
                        break
                except ValueError:
                    print("Por favor, insira um número válido para o preço diário.")
            while True:
                try:
                    cilindrada = int(input("Cilindrada: "))
                    if cilindrada <= 0:
                        print("A cilindrada deve ser maior que zero.")
                    else:
                        break
                except ValueError:
                    print("Por favor, insira um número inteiro válido para a cilindrada.")
            while True:
                try:
                    potencia = int(input("Potência: "))
                    if potencia <= 0:
                        print("A potência deve ser maior que zero.")
                    else:
                        break
                except ValueError:
                    print("Por favor, insira um número inteiro válido para a potência.")
            break

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

    if item_type == 2:
        #data_inicio = validate_input_date("Data de Início (AAAA-MM-DD): ")
        #data_fim = validate_input_date("Data de Fim (AAAA-MM-DD): ")
        #cliente_id = validate_input_int("ID do Cliente: ")
        #automovel_id = validate_input_int("ID do Automóvel: ")

        while True:
            data_inicio = input("Data de Inicio (DD-MM-AAAA): ")
            if not validate_date(data_inicio):
                print("Data de inicio inválida. Use o formato DD-MM-AAAA.")
            else:
                break
        while True:
            data_fim = input("Data de Fim (DD-MM-AAAA): ")
            if not validate_date(data_fim):
                print("Data de fim inválida. Use o formato DD-MM-AAAA.")
            else:
                break

        cliente_id = menu_pesquisas_id(listCliente,"nome")
        automovel_id = menu_pesquisas_id(listAutomovel,"matricula")
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

#função para criar listagens dos menus beaupy

def list_menu(lst, key):
    try:
        list_temp = [val[key] for val in lst]
    except:
        pass   
    list_temp.append('Sair')
    if list_temp:
        return list_temp
    else:
        return []
    
def list_menu_teste(lst, key):
    try:
        list_temp = [f"{val["data_inicio"]}-{val["data_fim"]}-{val["numeroDias"]}" for val in lst]
    except:
        pass   
    list_temp.append('Sair')
    if list_temp:
        return list_temp
    else:
        return []

#função para obter lista sem linhas que possam ter problemas de ausência de chave
def list_filtrated(lst, key):
    list_temp = [val for val in lst if isinstance(val, dict) and key in val]
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
    
    if item_type == 2:
        if updated_item['data_inicio'] != item['data_inicio'] or updated_item['data_fim'] != item['data_fim']:
            updated_item['numeroDias'] = calculate_num_days(updated_item['data_inicio'], updated_item['data_fim'])
            updated_item['precoReserva'] = calculate_booking_price(updated_item['numeroDias'], updated_item['automovel_id'])

    return updated_item

#Calcula o preço total de uma reserva, e aplica descontos baseados na duração
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
# Pesquisa um automóvel por matrícula e mostra os dados com os ultimos 5 alugueres

#função para validar entrada de matrícula
def input_matricula():
    while True:
        matricula = input("Digite a matrícula do automóvel: ")
        if not validate_matricula(matricula):
                print("Matrícula inválida.")
        else:
            break 
    return matricula 

#função para validar entrada de NIF
def input_nif():
    while True:
        nif = input("Digite o NIF do cliente: ")        
        if not validate_nif(nif):
            print("NIF inválido. Deve ter 9 dígitos.")
        else:
            nif = int(nif)            
            break
    return nif       


def search_automovel(matricula):    
    for automovel in listAutomovel:
        if automovel['matricula'].upper() == matricula.upper():
            print(f"Dados do automóvel:")
            for key, value in automovel.items():
                print(f"{key}: {value}")
            print("\nÚltimos 5 alugueres:")
            bookings = [b for b in listBooking if int(b["automovel_id"]) == int(automovel["id"]) and  datetime.strptime(b["data_fim"], "%Y-%m-%d").date() < datetime.now().date()]
            for booking in sorted(bookings, key=lambda x: x['data_inicio'], reverse=True)[:5]:
                print(f"Data: {booking['data_inicio']} a {booking['data_fim']}")
            if bookings == []:
                print(f"Não existem alugueres!")  
            return          
    print("Automóvel não encontrado.")

# Pesquisa um cliente por NIF e retorna os dados e os últimos 5 alugueres
def search_cliente(nif, listAutomoveis):   
    for cliente in listCliente:
        if int(cliente['nif']) == nif:
            print()
            print(f"Dados do cliente:")
            for key, value in cliente.items():
                if key != 'id':                    
                    print(f"{key}: {value}")
            print("\nÚltimos 5 alugueres:")
            bookings = [b for b in listBooking if b['cliente_id'] == cliente['id'] and datetime.strptime(b["data_fim"], "%Y-%m-%d").date() < datetime.now().date()]
            for booking in sorted(bookings, key=lambda x: x['data_inicio'], reverse=True)[:5]:
                print(f"Data: {booking['data_inicio']} a {booking['data_fim']} Matrícula: {first_or_default(listAutomoveis, 'id', booking['automovel_id'])} Número dias: {booking['numeroDias']} Preço reserva: {booking['precoReserva']} €")                                
            return
    print("Cliente não encontrado.")

#função para pesquisa de matrícula com base no id do automóvel
def first_or_default(list, key, value, default=None):
    for val in list:
        if val[key] == value:
            return val['matricula']
    return default


# Carregar dados
listCliente = load_data('listcliente.json')
listAutomovel = load_data('listautomovel.json')
listBooking = load_data('listbooking.json')

main_menu2()