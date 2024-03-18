# Importation du module d'expressions régulières
import re

def get_idf_type_by_partner(config_content, partner_name):
    lines = config_content.split('\n')
    found_partner = False
    idf_types = []  # Initialisation de la liste des types IDF à vide
    send_count = 0
    recv_count = 0
    for line in lines:
        if 'PART' in line and partner_name in line:
            found_partner = True
            print("Ligne du partenaire:", line)
        elif found_partner and 'TYPE' in line:
            idf_type = line.split('=')[1].strip().strip("'")
            idf_types.append(idf_type)
            if idf_type == 'SEND':
                send_count += 1
            elif idf_type == 'RECEIVE':
                recv_count += 1
    print("Types IDF trouvés:", idf_types)
    # Construire la chaîne de type de flux avec le nombre total de SEND et RECEIVE
    type_str = ''
    if send_count > 0:
        type_str += f"{send_count} SEND"
    if recv_count > 0:
        if type_str:
            type_str += ', '
        type_str += f"{recv_count} RECEIVE"
    # Si la liste contient à la fois 'SEND' et 'RECEIVE', retourner 'SEND,RECEIVE'
    if send_count > 0 and recv_count > 0:
        return 'SEND,RECEIVE'
    # Sinon, retourner la chaîne de type de flux ou 'UNKNOWN' s'il n'y a pas de type valide
    elif type_str:
        return type_str
    else:
        return 'UNKNOWN'

def main():
    config_file_path = r'C:\Users\fguent\Desktop\TESTREG\cft.cfg'
    partner_name = 'PLCLCLY1'

    with open(config_file_path, 'r') as file:
        config_content = file.read()

    partner_flux = get_idf_type_by_partner(config_content, partner_name)
    
    # Filtrer les types de flux pour inclure uniquement SEND et RECEIVE
    filtered_flux = [flux for flux in partner_flux.split(', ') if flux in ['SEND', 'RECEIVE']]

    if filtered_flux:
        print(f"Types de flux pour le partenaire '{partner_name}': {', '.join(filtered_flux)}")
    else:
        print(f"Aucun type de flux trouvé pour le partenaire '{partner_name}'.")

if __name__ == "__main__":
    main()
