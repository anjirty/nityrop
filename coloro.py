
try:
    import os
    import time
    import string
    import zipfile
    import rarfile
    import itertools
    import string
    import argparse
    import pikepdf
    from termcolor import colored
    import threading
    from pathlib import Path
except ImportError as e:
    print('Please install the following modules: {}'.format(e))

def generate_passwords(min_length, max_length, char_set):
    """Generates a list of passwords within the specified parameters."""
    passwords = []
    for length in range(min_length, max_length + 1):
        passwords.extend(''.join(x) for x in itertools.product(char_set, repeat=length))
    return passwords


def write_to_file(file_path, password, file_name, file_type):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        if f"To access {file_name}, use the password {password}\n" in lines:
            time.sleep(2)
            print(colored(f'To access {file_name}, use the password {password}\n', 'blue'))
               
        else:
            with open(f"{file_type.upper()}.txt", 'a') as file:
                time.sleep(2)
                file.write(f"To access {file_name}, use the password {password}\n")
                print(colored(f'To access {file_name}, use the password {password}\n', 'green'))


def decrypt_zip(zip_file, passwords):
    """Attempts to decrypt the ZIP file with a list of passwords."""
    with zipfile.ZipFile(zip_file) as f:
        for password in passwords:
            try:
                path = zip_file
                pathx = Path(path).stem + '.zip'
                f.extractall(pwd=password.encode())
                write_to_file("ZIP.txt", password, pathx, "zip")
                return password
            except (zipfile.BadZipFile, RuntimeError):
                print(colored(f"[-] Incorrect Password: {password}", 'red', attrs=['bold']))
                os.system('cls' if os.name == 'nt' else 'clear')
    print(colored('[!] No valid passwords were found', 'red', attrs=['bold']))


def decrypt_rar(rar_file, passwords):
    """Attempts to decrypt the RAR file with a list of passwords."""
    with rarfile.RarFile(rar_file) as f:
        for password in passwords:
            try:
                path = rar_file
                pathx = Path(path).stem + '.rar'
                f.extractall(pwd=password.encode())
                print(colored(f"[+] Password found: {password}. File: {pathx}", 'green', attrs=['bold']))
                write_to_file("RAR.txt", password, pathx, "rar")
                return password
            except (rarfile.BadRarFile, RuntimeError):
                print(colored(f"[-] Incorrect Password: {password}. File: {rar_file}", 'red', attrs=['bold']))
                os.system('cls' if os.name == 'nt' else 'clear')
    print(colored('[!] No valid passwords were found', 'red', attrs=['bold']))


def decrypt_pdf(pdf_file, passwords):
    """Attempts to brute force the PDF file with a list of passwords using pikepdf."""
    for password in passwords:
        try:
            with pikepdf.open(pdf_file, password=password) as pdf:
                path = pdf_file
                pathx = Path(path).stem + '.pdf'
                write_to_file("PDF.txt", password, pathx, "pdf")
                return password
        except pikepdf.PasswordError:
            print(colored(f"[-] Incorrect Password: {password}", 'red', attrs=['bold']))
            os.system('cls' if os.name == 'nt' else 'clear')
    print(colored('[!] No valid passwords were found !!', 'red', attrs=['bold']))


def decrypt_files(file_type, file_path, passwords):
    if file_type == 'zip':
        return decrypt_zip(file_path, passwords)
    elif file_type == 'rar':
        return decrypt_rar(file_path, passwords)
    elif file_type == 'pdf':
        return decrypt_pdf(file_path, passwords)
    else:
        print(colored(f"[!] Error: Invalid file format. Please try with a ZIP, RAR, or PDF file.", "red", attrs=["bold"]))
        return None


def main():
    # Define arguments and parse command line options
    parser = argparse.ArgumentParser(description="Decrypt ZIP, RAR, or PDF files using a password list or generation")
    parser.add_argument("-t", "--type", required=True, choices=['zip', 'rar', 'pdf'],
                        help="Type of file to decrypt (zip, rar, or pdf)")
    parser.add_argument("-f", "--file", required=True, nargs='+', help="Path to the ZIP, RAR, or PDF file(s)")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-l", "--list", help="Path to a password list file (optional)")
    group.add_argument("-g", "--generate", action="store_true", help="Generate passwords (default: False)")
    parser.add_argument("-min", "--min-length", type=int, default=6, required=False,
                        help="Minimum length of passwords to generate")
    parser.add_argument("-max", "--max-length", type=int, default=12, required=False,
                        help="Maximum length of passwords to generate")
    parser.add_argument("-c", "--char-set", type=str, default=string.ascii_letters + string.digits, required=False,
                        help="Character set to use for password generation")
    args = parser.parse_args()

    # Validate file(s)
    for file_path in args.file:
        if not os.path.isfile(file_path):
            print(colored(f"[!] Error: File '{file_path}' not found.", 'red', attrs=['bold']))
            exit(1)

    # Disable unused arguments if neither list nor generation is chosen
    if not args.list and not args.generate:
        args.generate = False
        args.list = None
        args.min_length = 4
        args.max_length = 12
        args.char_set = string.ascii_letters + string.digits

    # Choose password source and proceed with decryption
    if args.list:
        try:
            with open(args.list) as f:
                passwords = [line.strip() for line in f]
        except FileNotFoundError:
            print(colored(f"[!] Error: Password list file '{args.list}' not found.", 'red', attrs=['bold']))
            exit(1)
        print(f"[=] Using passwords from file '{args.list}':")
    elif args.generate:
        passwords = generate_passwords(args.min_length, args.max_length, args.char_set)
        print(f"[=] Generated {len(passwords)} passwords:")
    else:
        print(colored(f"[!] Error: Please specify either a password list file or use the generation option.", 'red',
                      attrs=['bold']))
        exit(1)

    # Create threads for each file
    threads = []
    for file_path in args.file:
        t = threading.Thread(target=decrypt_files, args=(args.type, file_path, passwords))
        threads.append(t)
        t.start()

    # Wait for all threads to finish
    for t in threads:
        t.join()


if __name__ == "__main__":
    main()
