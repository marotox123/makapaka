
# Program do Automatyzacji Konfiguracji Systemu

![Logo programu](logo.png)

## Opis programu

Program, który automatyzuje tworzenie kont użytkowników, grup, konfiguruje system, instaluje drukarki oraz generuje kosztorys. Działa na systemie Windows z uprawnieniami administratora.

**UWAGA: Program modyfikuje system operacyjny oraz ustawienia rejestru. NIE URUCHAMIAJ GO NA PRAWDZIWYCH URZĄDZENIACH produkcyjnych lub ważnych komputerach! Używaj go wyłącznie w środowisku testowym!**

---

## Wymagania

- Python 3.x
- Uprawnienia administratora na systemie Windows

### Biblioteki Pythona

Aby zainstalować wymagane biblioteki, uruchom poniższą komendę:

```bash
pip install pandas
```

---

## Instrukcje instalacji

1. Sklonuj repozytorium:

   ```bash
   git clone https://github.com/marotox123/nazwa-repozytorium.git
   ```

2. Wejdź do folderu projektu:

   ```bash
   cd nazwa-repozytorium
   ```

3. Zainstaluj wymagane biblioteki Pythona:

   ```bash
   pip install pandas
   ```

---

## Jak uruchomić

**Przed uruchomieniem upewnij się, że masz uprawnienia administratora!**

1. Uruchom program z poziomu konsoli:

   ```bash
   python main.py
   ```

   Program sprawdzi, czy masz uprawnienia administratora i automatycznie wykona szereg zadań, takich jak:
   - Tworzenie kont użytkowników ("Lekarz" i "Recepcja")
   - Tworzenie grupy "Przychodnia"
   - Konfiguracja systemu Windows, np. zmiana ustawień folderów i Panelu Sterowania
   - Instalacja i konfiguracja drukarki
   - Generowanie kosztorysu usług komputerowych

---

## Ważne informacje

- Program wykonuje operacje na systemie, takie jak modyfikacje rejestru oraz ustawienia systemowe. Może to spowodować zmiany w konfiguracji twojego komputera. **Używaj tego narzędzia tylko w środowiskach testowych.**
  
- **Nie uruchamiaj programu na prawdziwych urządzeniach produkcyjnych** bez pełnej świadomości efektów jego działania!

---

## Autorzy

- marotox123

---

## Licencja

Ten projekt jest objęty licencją GNU General Public License v3.0 — szczegóły znajdziesz w pliku LICENSE.

---

To wszystko! Jeżeli masz jakiekolwiek pytania lub napotkałeś problemy, otwórz "Issue" w tym repozytorium.
