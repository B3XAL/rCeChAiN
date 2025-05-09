# rCeChAiN

**rCeChAiN** is a tool that facilitates the exploitation of deserialization vulnerabilities. It allows to generate and sign malicious cookies to execute remote code by exploiting pre-built gadget strings. It is designed to be used in security testing environments, such as CTFs or penetration tests, to attack PHP applications vulnerable to this type of exploitation.

## Features

- **Automatic generation of Payloads:** It uses tools such as PHPGGC to generate serialized PHP objects containing remote code execution (RCE) payloads.
  
- **Automatic Cookie Signing:** Generates malicious cookies correctly signed using a secret key obtained from a deserialization vulnerability.
  
- **Simple Interface:** Generates payloads and cookies with a single command, which facilitates the exploitation process.

- **Multiple Exploitation Methods:** Now supports payload generation for PHP, Ruby, and Java deserialization vulnerabilities.

- **Flexibility and Extensibility:** Users can generate custom payloads for exploitation using predefined chains in multiple languages (PHP, Ruby, Java).

- **Serialized Cookie Detection:** Identify and detect serialized cookies in various formats (PHP, Ruby, Java) by decoding and checking the format, helping users understand the serialization method used in web applications.
  

## Requirements

- Python 3.X
- PHPGGC
- Docker (for Ruby and Java payload generation)

## Installation

1. **Clone the repository:**

   `git clone https://github.com/B3XAL/rCeChAiN.git`

   `cd rCeChAiN`

   `chmod +x rCeChAiN.py apache_commons.sh php_pre-built_gadget_chain.py ruby_pre-built_gadget_chain.py identify.py`
   
3. **Install dependencies:**

   Make sure you have Python 3.x and pip installed..

   `pip install -r requirements.txt`
   
4. **Install PHPGGC & xclip:**

   `sudo apt install phpggc xclip -y`

## Example of Use

1. **rCeChAiN**

   `sudo python3 rCeChAiN.py`

   ![Paso 1](./images/1.png)

   - After running python3 rCeChAiN.py, you can choose from the following exploitation methods:

     - PHP - Pre-built gadget chain (SECRET_KEY)
     - JAVA - Deserialization with Apache Commons
     - RUBY - Pre-built gadget chain 2.X 3.X

3. **PHP Payload Generation:**
   
   - All Cookies generated will be saved in cookies.txt and copied to your clipboard.
  
   ![Paso 2](./images/2.png)

   **Use in Burpsuite ( Intruder ):**

   ![Paso 3](./images/3.png)

   - Working payloads will use the payload name as a subdomain on the collaborator server, making it easier to identify the successful payload.
     
   ![Paso 4](./images/4.png)

   **Customization:**
   - It will ask us if any of them have been successfully exploited and if so, it will allow us to do so.
  
   ![Paso 5](./images/5.png)
   
   - **Data exfiltration of a particular file**

   ![Paso 6](./images/6.png)

   ![Paso 7](./images/7.png)

   - **Custom payload creation**

   ![Paso 8](./images/8.png)

   ![Paso 9](./images/9.png)

   Calling the latter if successfully executed to success.burpcollaborator

4. **Java Deserialization with Apache Commons:**

   - If you select Java, payloads will be generated using a custom tool that i created in another project specifically for Java deserialization vulnerabilities. This tool automates the process of generating malicious Java objects.

5. **Ruby Payload Generation:**

   - Ruby payloads are generated using pre-built gadget chains for versions 2.x and 3.x.
  
**Customization:**
You will be asked if any payload has been successfully executed, allowing for additional actions such as:

   - Data exfiltration of a particular file
   - Custom payload creation 

## Contributions

If you have any improvements or suggestions, feel free to contribute! You can open an **Issue** or make a **Pull Request** with your changes.

## License

This project is under the **MIT License**. See the file [LICENSE](LICENSE) para más detalles.

---

*by b3xal*

