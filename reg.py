import re

def read_config_file(config_file_path):
    with open(config_file_path, 'r') as file:
        return file.read()

def extract_ssl_info(config_content, partner_name):
    ssl_info = {}
    match_ssl = re.search(fr'CFTSSL\s+ID\s*=\s*\'DSSL{partner_name}.*?VERSION\s*=\s*\'([^\']+)\'.*?USERCID\s*=\s*\'([^\']+)\'', config_content, re.DOTALL)
    if match_ssl:
        ssl_info['VERSION'] = match_ssl.group(1)
        ssl_info['USERCID'] = match_ssl.group(2)
    return ssl_info

def extract_root_cid(config_content):
    root_cid = []
    root_cid_matches = re.search(fr'ROOTCID\s*=\s*\((.*?)\)', config_content, re.DOTALL)
    if root_cid_matches:
        root_cid_items = re.findall(r"'([^']+)'", root_cid_matches.group(1))
        root_cid = [item.strip() for item in root_cid_items]
    return root_cid

def extract_sap(config_content, partner_name):
    sap = None
    match_sap = re.search(fr'CFTPART\s+ID\s*=\s*\'{partner_name}\'.*?SAP\s*=\s*\(\s*\'(\d+)\'\)', config_content, re.DOTALL)
    if match_sap:
        sap = match_sap.group(1)
    return sap

def extract_host(config_content, partner_name):
    host = None
    match_ip = re.search(fr'CFTTCP\s+ID\s*=\s*\'{partner_name}\'.*?HOST\s*=\s*\(\s*\'([\d\.]+)\'\)', config_content, re.DOTALL)
    if match_ip:
        host = match_ip.group(1)
    return host

def get_idf_type_by_partner(config_content, partner_name):
    idf_type = None
    match_idf = re.search(fr'CFTIDF\s+ID\s*=\s*\'{partner_name}\'.*?TYPE\s*=\s*\'([^\']+)\'', config_content, re.DOTALL)
    if match_idf:
        idf_type = match_idf.group(1)
    return idf_type



def extract_partner_info(config_content, partner_name):
    ssl_info = extract_ssl_info(config_content, partner_name)
    root_cid = extract_root_cid(config_content)
    sap = extract_sap(config_content, partner_name)
    host = extract_host(config_content, partner_name)
    idf_type = get_idf_type_by_partner(config_content, partner_name)

    partner_info = {
        'VERSION': ssl_info.get('VERSION'),
        'USERCID': ssl_info.get('USERCID'),
        'ROOTCID': root_cid,
        'SAP': sap,
        'HOST': host,
        'IDF_TYPE': idf_type
    }

    return partner_info

def main():
    config_file_path = r'C:\Users\fguent\Desktop\cft.cfg'
    partner_name = 'PLCLCLY1'

    config_content = read_config_file(config_file_path)
    partner_info = extract_partner_info(config_content, partner_name)

    if partner_info:
        sap = partner_info.get('SAP')
        host = partner_info.get('HOST')
        if sap and host:
            print(f"Informations pour le partenaire '{partner_name}':")
            print(f"   Version SSL: {partner_info.get('VERSION')}")
            print(f"   User CID: {partner_info.get('USERCID')}")
            print(f"   Root CID: ({', '.join(partner_info.get('ROOTCID', []))})")
            print(f"   IDF Type: {partner_info.get('IDF_TYPE')}")
            print(f"   SAP HOST: {sap}:{host}")
        else:
            print(f"Le partenaire '{partner_name}' n'a pas de port SAP ou d'adresse IP associé dans le fichier de configuration.")
    else:
        print(f"Aucune information trouvée pour le partenaire '{partner_name}' dans le fichier de configuration.")

if __name__ == "__main__":
    main()










