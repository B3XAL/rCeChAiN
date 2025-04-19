import base64
import urllib.parse
import re
import json

# Colores para la consola
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
RESET = "\033[0m"

def detect_serialized_cookie(token):
    print(f"\n{YELLOW}Checking token...{RESET}\n")

    # JAVA SERIALIZED DETECTION
    if token.startswith("H4s"):
        print(f"→ Probable {GREEN}Java Serialized Cookie (gzip compressed & base64 encoded){RESET}")
        return
    elif token.startswith("rO0"):
        print(f"→ Probable {GREEN}Java Serialized Cookie (base64 encoded){RESET}")
        return

    # RUBY SERIALIZED DETECTION
    elif token.startswith("BAh"):
        print(f"→ Probable {GREEN}Ruby Marshal-serialized object (base64 encoded){RESET}")
        return

    # Try URL decoding
    try:
        urldecoded = urllib.parse.unquote(token)

        # Detect PHP Serialized Object (URL decoded)
        if re.match(r"^(O:\d+:|a:\d+:|s:\d+:)", urldecoded):
            print(f"→ Probable {GREEN}PHP Serialized Cookie (URL encoded){RESET}")
            return

        # Detect JSON Object (URL decoded)
        if urldecoded.startswith("{") and urldecoded.endswith("}"):
            print(f"→ Tentative {YELLOW}JSON Object (URL encoded){RESET}")
            # Now, let's look for any Base64 encoded fields inside the JSON
            try:
                json_data = json.loads(urldecoded)
                for key, value in json_data.items():
                    # Check if the value is a base64 encoded string
                    if isinstance(value, str) and re.match(r'^[A-Za-z0-9+/=]+$', value):
                        try:
                            # Decode the base64 content
                            base64_decoded = base64.b64decode(value).decode('utf-8', errors='ignore')
                            # Check if the decoded base64 content is a serialized PHP object
                            if re.match(r"^(O:\d+:|a:\d+:|s:\d+:)", base64_decoded):
                                print(f"→ Probable {GREEN}PHP Serialized Cookie inside JSON (Base64 encoded){RESET}")
                                return
                        except Exception:
                            pass
            except json.JSONDecodeError:
                pass

        # Try Base64 decoding after URL decoding
        try:
            decoded = base64.b64decode(urldecoded).decode('utf-8', errors='ignore')

            # Detect PHP Serialized Object (Base64 + URL decoded)
            if re.match(r"^(O:\d+:|a:\d+:|s:\d+:)", decoded):
                print(f"→ Probable {GREEN}PHP Serialized Cookie (Base64 + URL encoded){RESET}")
                return

            # Detect JSON Object (Base64 + URL decoded)
            if decoded.startswith("{") and decoded.endswith("}"):
                try:
                    json_data = json.loads(decoded)
                    print(f"→ Tentative {YELLOW}JSON Object (Base64 + URL encoded){RESET}")
                    # Look for base64 encoded values inside the JSON
                    for key, value in json_data.items():
                        if isinstance(value, str) and re.match(r'^[A-Za-z0-9+/=]+$', value):
                            try:
                                base64_decoded = base64.b64decode(value).decode('utf-8', errors='ignore')
                                if re.match(r"^(O:\d+:|a:\d+:|s:\d+:)", base64_decoded):
                                    print(f"→ Probable {GREEN}PHP Serialized Cookie inside JSON (Base64 encoded){RESET}")
                                    return
                            except Exception:
                                pass
                except json.JSONDecodeError:
                    pass

        except Exception:
            pass

    except Exception:
        pass

    print(f"{RED}→ Could not determine serialization format.{RESET}")


# Pedir token al usuario
token = input("\nEnter the serialized cookie token: ").strip()
detect_serialized_cookie(token)
