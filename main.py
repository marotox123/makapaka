import os
import ctypes
import pandas as pd
import subprocess
import psutil
GREEN = "\033[92m"
RED = "\033[91m"
BLUE = "\033[94m"
RESET = "\033[0m"
logo = f"""
{BLUE}
 _____ ______   ________  ___  __    ________          ________  ________  ___  __    ________
|\   _ \  _   \|\   __  \|\  \|\  \ |\   __  \        |\   __  \|\   __  \|\  \|\  \ |\   __  \
\ \  \\\__\ \  \ \  \|\  \ \  \/  /|\ \  \|\  \       \ \  \|\  \ \  \|\  \ \  \/  /|\ \  \|\  \
 \ \  \\|__| \  \ \   __  \ \   ___  \ \   __  \       \ \   ____\ \   __  \ \   ___  \ \   __  \
  \ \  \    \ \  \ \  \ \  \ \  \\ \  \ \  \ \  \       \ \  \___|\ \  \ \  \ \  \\ \  \ \  \ \  \
   \ \__\    \ \__\ \__\ \__\ \__\\ \__\ \__\ \__\       \ \__\    \ \__\ \__\ \__\\ \__\ \__\ \__\
    \|__|     \|__|\|__|\|__|\|__| \|__|\|__|\|__|        \|__|     \|__|\|__|\|__| \|__|\|__|\|__|
{RESET}
"""
tekst_pod_logo = f"{BLUE}Program który wszytko robi za ciebie{RESET}"
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False
def create_user_account(username, password, admin=False):
    def check_user_exists(username):
        try:
            result = subprocess.run(f'net user {username}', shell=True, check=True)
            return result.returncode == 0
        except subprocess.CalledProcessError:
            return False
    def delete_user_account(username):
        try:
            subprocess.run(f'net user {username} /delete', shell=True, check=True)
            print(f'{GREEN}Konto {username} zostało usunięte: SUCCESS{RESET}')
        except Exception as e:
            print(f'{RED}Nie udało się usunąć konta {username}: FAILED{RESET}')
            print(str(e))
    if check_user_exists(username):
        delete_user_account(username)
    try:
        if admin:
            subprocess.run(f'net user {username} {password} /add /active:yes /expires:never /passwordreq:yes',
                           shell=True, check=True)
            subprocess.run(f'net localgroup Administratorzy {username} /add', shell=True, check=True)
            print(f'{GREEN}Konto {username} z uprawnieniami administratora zostało utworzone: SUCCESS{RESET}')
        else:
            subprocess.run(f'net user {username} {password} /add /active:yes /expires:never /passwordreq:yes',
                           shell=True, check=True)
            print(f'{GREEN}Konto {username} z ograniczonymi uprawnieniami zostało utworzone: SUCCESS{RESET}')
    except Exception as e:
        print(f'{RED}Nie udało się utworzyć konta {username}: FAILED{RESET}')
        print(str(e))
def create_user_group(group_name, usernames):
    def check_group_exists(group_name):
        try:
            result = subprocess.run(f'net localgroup {group_name}', shell=True, check=True)
            return result.returncode == 0
        except subprocess.CalledProcessError:
            return False
    def delete_user_group(group_name):
        try:
            subprocess.run(f'net localgroup {group_name} /delete', shell=True, check=True)
            print(f'{GREEN}Grupa {group_name} została usunięta: SUCCESS{RESET}')
        except subprocess.CalledProcessError:
            print(f'{RED}Grupa {group_name} nie istnieje lub nie udało się jej usunąć: FAILED{RESET}')
        except Exception as e:
            print(f'{RED}Błąd: {e}{RESET}')
    if check_group_exists(group_name):
        delete_user_group(group_name)
    try:
        subprocess.run(f'net localgroup {group_name} /add', shell=True, check=True)
        for user in usernames:
            subprocess.run(f'net localgroup {group_name} {user} /add', shell=True, check=True)
        print(f'{GREEN}Grupa {group_name} została utworzona i przypisano do niej użytkowników: SUCCESS{RESET}')
    except subprocess.CalledProcessError as e:
        print(f'{RED}Nie udało się utworzyć grupy lub przypisać użytkowników: {e}{RESET}')
    except Exception as e:
        print(f'{RED}Nieoczekiwany błąd: {e}{RESET}')
def set_folder_options():
    try:
        subprocess.run(
            'REG ADD "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\CabinetState" /v "Settings" /t REG_BINARY /d "0000000000000000" /f',
            shell=True, check=True)
        print(
            f'{GREEN}Ustawienia folderów zostały zmienione, aby otwierać każdy folder w osobnym oknie: SUCCESS{RESET}')
    except Exception as e:
        print(f'{RED}Nie udało się zmienić ustawień folderów: FAILED{RESET}')
        print(str(e))
def hide_control_panel_applets():
    try:
        subprocess.run(
            'REG ADD "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\Explorer" /v "DisallowCpl" /t REG_SZ /d "1" /f',
            shell=True, check=True)
        subprocess.run(
            'REG ADD "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\Explorer\\DisallowCpl" /v "0" /t REG_SZ /d "timedate.cpl" /f',
            shell=True, check=True)
        print(
            f'{GREEN}Ukryto aplety Panelu Sterowania, pozostawiając dostęp tylko do apletu "Data i godzina": SUCCESS{RESET}')
    except Exception as e:
        print(f'{RED}Nie udało się ukryć apletów Panelu Sterowania: FAILED{RESET}')
        print(str(e))
def create_folder():
    try:
        os.makedirs(r'C:\PACJENCI', exist_ok=True)
        print(f'{GREEN}Folder C:\\PACJENCI został utworzony: SUCCESS{RESET}')
    except Exception as e:
        print(f'{RED}Nie udało się utworzyć folderu C:\\PACJENCI: FAILED{RESET}')
        print(str(e))
def backup_registry_key():
    try:
        subprocess.run(r'reg export HKLM C:\PACJENCI\copy_HKLM.reg /y', shell=True, check=True)
        print(f'{GREEN}Kopia klucza rejestru HKLM została zapisana w C:\\PACJENCI\\copy_HKLM.reg: SUCCESS{RESET}')
    except Exception as e:
        print(f'{RED}Nie udało się wykonać kopii klucza rejestru: FAILED{RESET}')
        print(str(e))
def set_virtual_memory():
    try:
        ram_in_mb = psutil.virtual_memory().total // (1024 * 1024)
        virtual_memory_size = int(ram_in_mb * 1.5)
        subprocess.run(
            f'wmic pagefileset where name="C:\\\\pagefile.sys" set InitialSize={virtual_memory_size},MaximumSize={virtual_memory_size}',
            shell=True, check=True)
        print(f'{GREEN}Pamięć wirtualna została ustawiona na {virtual_memory_size} MB: SUCCESS{RESET}')
    except subprocess.CalledProcessError as e:
        print(f'{RED}Błąd podczas wykonywania komendy systemowej: {e}{RESET}')
    except Exception as e:
        print(f'{RED}Nie udało się ustawić pamięci wirtualnej: {e}{RESET}')
def enforce_password_change():
    try:
        subprocess.run('net accounts /maxpwage:15', shell=True, check=True)
        print(f'{GREEN}Wymuszono zmianę haseł co 15 dni: SUCCESS{RESET}')
    except Exception as e:
        print(f'{RED}Nie udało się wymusić zmiany haseł: FAILED{RESET}')
        print(str(e))
def install_printer(printer_name, model_name):
    try:
        subprocess.run(
            f'rundll32 printui.dll,PrintUIEntry /if /b "{printer_name}" /f "{model_name}" /r "LPT1:" /m "{model_name}"',
            shell=True, check=True)
        print(f'Drukarka {printer_name} została zainstalowana: SUCCESS')
    except Exception as e:
        print(f'Nie udało się zainstalować drukarki: FAILED')
        print(str(e))
def configure_printer_access_and_permissions(printer_name="Wirtualna_Drukarka"):
    try:
        subprocess.run(f'icacls "C:\\Windows\\System32\\spool\\PRINTERS" /grant Przychodnia:(M)', shell=True,
                       check=True)
        subprocess.run(f'icacls "C:\\Windows\\System32\\spool\\PRINTERS" /grant Przychodnia:(P)', shell=True,
                       check=True)
        print(f'{GREEN}Grupa Przychodnia uzyskała dostęp do zarządzania i drukowania: SUCCESS{RESET}')
        subprocess.run(f'schtasks /create /tn "AllowPrinterAccess" /tr "icacls C:\\Windows\\System32\\spool\\PRINTERS '
                       f'/grant Everyone:(F)" /sc daily /st 16:00 /et 23:00', shell=True, check=True)
        print(f'{GREEN}Drukarka jest dostępna dla wszystkich użytkowników w godzinach 16:00-23:00: SUCCESS{RESET}')
    except subprocess.CalledProcessError as e:
        print(f'{RED}Nie udało się przydzielić uprawnień lub skonfigurować dostępu: {e}{RESET}')
    except Exception as e:
        print(f'{RED}Błąd: {e}{RESET}')
def install_and_configure_printer(printer_name="Wirtualna_Drukarka", port_name="LPT1:",
                                  model_name="Generic / Text Only"):
    try:
        subprocess.run(f'rundll32 printui.dll,PrintUIEntry /if /b "{printer_name}" /r "{port_name}" /m "{model_name}"',
                       shell=True, check=True)
        print(f'{GREEN}Drukarka {printer_name} została zainstalowana: SUCCESS{RESET}')
        subprocess.run(f'rundll32 printui.dll,PrintUIEntry /Xs /n "{printer_name}" attributes shared=TRUE', shell=True,
                       check=True)
        print(f'{GREEN}Drukarka {printer_name} została skonfigurowana jako współdzielona: SUCCESS{RESET}')
        configure_printer_access_and_permissions(printer_name)
    except subprocess.CalledProcessError as e:
        print(f'{RED}Nie udało się zainstalować lub skonfigurować drukarki {printer_name}: {e}{RESET}')
    except Exception as e:
        print(f'{RED}Błąd: {e}{RESET}')
def create_folder_file_and_restore_access(folder_path, file_name):
    try:
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            print(f'Folder {folder_path} został utworzony: SUCCESS')
        else:
            print(f'Folder {folder_path} już istnieje: ALREADY EXISTS')
        file_path = os.path.join(folder_path, file_name)
        if not os.path.exists(file_path):
            with open(file_path, 'w') as file:
                file.write("Dane pacjentów\n")
            print(f'Plik {file_name} został utworzony: SUCCESS')
        else:
            print(f'Plik {file_name} już istnieje: ALREADY EXISTS')
        restore_file_access(file_path)
    except Exception as e:
        print(f'Nie udało się utworzyć folderu lub pliku: FAILED')
        print(str(e))
def restore_file_access(file_path):
    try:
        subprocess.run(f'icacls "{file_path}" /grant Everyone:F', shell=True, check=True)
        print(f'Dostęp do pliku {file_path} został przywrócony: SUCCESS')
    except Exception as e:
        print(f'Nie udało się przywrócić dostępu do pliku: FAILED')
        print(str(e))
def create_user_excel_file(file_name, users):
    folder_path = r'C:\DANE'
    try:
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            print(f'Folder {folder_path} został utworzony: SUCCESS')
        else:
            print(f'Folder {folder_path} już istnieje: ALREADY EXISTS')
        file_path = os.path.join(folder_path, file_name)
        df = pd.DataFrame(users, columns=["Nazwa użytkownika", "Hasło", "Admin"])
        df.to_excel(file_path, index=False)
        print(f'Plik {file_name} z użytkownikami został utworzony: SUCCESS')
    except Exception as e:
        print(f'Nie udało się utworzyć pliku Excel: FAILED')
        print(str(e))
users = [
    ["Lekarz", "Lekarz2023!", True],
    ["Recepcja", "Recepcja2023!", False]
]
def generate_cost_estimate():
    data_cennik = {
        "Lp.": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        "Nazwa usługi": [
            "Karta graficzna", "Karta sieciowa", "Instalacja i konfiguracja programu",
            "Instalacja systemu Windows/ Linux/ Mac", "Instalacja aktualizacji do systemu",
            "Testowanie oprogramowania", "Wymiana podzespołu", "Przetestowanie wydajności systemu",
            "Instalacja i konfiguracja drukarki", "Konfiguracja systemu"
        ],
        "Wartość usługi netto (w zł)": [250, 30, 20, 110, 10, 10, 20, 20, 30, 35],
        "Wartość usługi brutto (w zł)": []
    }
    for i in data_cennik["Wartość usługi netto (w zł)"]:
        brutto = round(i * 1.23, 2)
        data_cennik["Wartość usługi brutto (w zł)"].append(brutto)
    df_cennik = pd.DataFrame(data_cennik)
    with pd.ExcelWriter(r"C:/PACJENCI/kosztorys_uslug_komputerowych.xlsx") as writer:
        df_cennik.to_excel(writer, sheet_name="Kosztorys Usług", index=False)
    print(f'{GREEN}Kosztorys został wygenerowany i zapisany jako kosztorys_uslug_komputerowych.xlsx: SUCCESS{RESET}')
if is_admin():
    print(logo)
    print(tekst_pod_logo)
    create_user_account("Lekarz", "Lekarz2023!", admin=True)
    create_user_account("Recepcja", "Recepcja2023!", admin=False)
    create_user_group("Przychodnia", ["Lekarz", "Recepcja"])
    set_folder_options()
    hide_control_panel_applets()
    create_folder()
    backup_registry_key()
    set_virtual_memory()
    enforce_password_change()
    install_and_configure_printer(printer_name="Wirtualna_Drukarka")
    create_folder_file_and_restore_access(r'C:\DANE', 'pacjenci.odt')
    create_user_excel_file('konta_uzytkownikow.xlsx', users)
    generate_cost_estimate()
else:
    print(f'{RED}Brak uprawnień administratora. Program zostanie zamknięty.{RESET}')
