import os
import pyfiglet

# Console output colors
GREEN = "\033[92m"
WHITE = "\033[97m"
RESET = "\033[0m"
ORANGE = "\033[38;5;214m"  # Color naranja (similar al naranja)
RED = "\033[91m"           # Color rojo

# Banner with pyfiglet
def banner():
    ascii_banner = pyfiglet.figlet_format("rCeChAiN")
    print(f"{GREEN}{ascii_banner}{RESET}")
    print("V1.2")
    print("by b3xal")
#    print("-" * 80)

# Function to display the menu with colored options
def show_menu():
    print()
    print("-" * 80)
    print("\nOptions:\n")
    print(f"{ORANGE}1.{RESET} PHP - Pre-built gadget chain (SECRET_KEY)")
    print(f"{ORANGE}2.{RESET} JAVA - Deserialization with Apache Commons")
    print(f"{ORANGE}3.{RESET} RUBY - Pre-built gadget chain 2.X 3.X")
    print(f"{ORANGE}4.{RESET} Identify serialized format")
    print(f"{RED}5. Exit{RESET}\n")

# Function to execute external scripts and return to menu
def run_script(script_name):
    os.system(f"python3 {script_name}")

# Main Loop
first_run = True  # Variable to track the first run

while True:
    if first_run:
        banner()  # Show the banner on first run
        first_run = False  # After the first run, this will be False
    
    show_menu()  # Show the menu

    option = input("Select an option: ").strip()

    if option == "1":
        run_script("php_pre-built_gadget_chain.py")
    elif option == "2":
        os.system(f"bash apache_commons.sh")
    elif option == "3":
        run_script("ruby_pre-built_gadget_chain.py")
    elif option == "4":
        run_script("identify.py")
    elif option == "5":
        print(f"\n{RED}Exiting...{RESET}\n")
        break
    else:
        print("\nInvalid option. Please try again.\n")
