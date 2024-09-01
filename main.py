import time
from utils import to_title_string, name_decantation, when_medicals_are_expiring, check_whether_medicals_are_expired_or_will_expire_in_14_days
from datetime import datetime, timedelta
from sel_portal_helper import SelPortalHelper
from librus_portal_helper import LibrusPortalHelper
from gmail_helper import GmailPortalHelper

# Listy zawodników przypisane do trenerów
cielo_athletes = ["Zakens Gabriela", "POLODY ESTERA", "SIEPKA ZOFIA", "JAGŁOWSKI DAWID", "OLEJNICZAK MATEUSZ", 
                  "SZMIDCHEN ALAN", "BERG MARIA", "LECHOWICZ MIKOŁAJ", "HEYMANN PATRYK", "SMYKAJ ANTONINA", 
                  "BARTOSZEWSKA MARTA", "KRZEŚNIAK JAKUB", "DOPIERAŁA PIOTR", "DROST STANISŁAW", "MADELSKA NATALIA", 
                  "MAKOWSKA BLANKA", "Sumisławska Aleksandra", "SEWIŁO MARTYNA", "MROCZEK DOMINIK", "HOROWSKA ZUZANNA", 
                  "KUBIAK ZUZANNA", "KUREK ANTONI", "MALICKA MAJA", "Moros Bruno", "NOGALSKA IGA"]

marcins_athletes = ["CHLIAHTENKO TIMOFEY", "CUDZIŁO MICHAŁ", "CZŁAPA BLANKA", "JUSZKIEWICZ-ZAPATA PIOTR", 
                    "KRYŚCIAK WOJCIECH", "KUREK FRANCISZEK", "LASKOWSKI FILIP", "LATANOWICZ NATALIA", "MALOVYCHKO FILIP", 
                    "MARKIEWICZ IGNACY", "MAZURKIEWICZ MARTYNA", "MIKOŁAJCZAK HELENA", "OCZUJDA DANIEL", "PRACHARCZYK MAKS", 
                    "RÓG ALEKSANDRA", "SMYKAJ KATARZYNA", "STEFANIAK KAROLINA", "TERTOŃ SZYMON", "Wiśniewski Leszek", 
                    "WOJCIECHOWSKI ANTONI", "WÓJCIK MARTA"]

elas_athletes = ["SHVETS MYKHAILO", "Brazhnyk Dmytro", "Jedwabny Maciej", "Zygnarowska Michalina", "Wrzeszczyńska Marta", 
                 "NOGAJ ALICJA", "KRUCKI KAJETAN", "KOLAŃCZYK WIKTORIA", "Nowicka Weronika"]

def main():
    # Logowanie do portalu SEL i pobranie danych zawodników
    sel_helper = SelPortalHelper()
    coaches = sel_helper.log_in_to_sel(cielo_athletes, marcins_athletes, elas_athletes)
    time.sleep(3)

    counter = 1
    for coach in coaches:
        time.sleep(3)
        print("Maciej i Młody" if counter == 0 else "Marcin" if counter == 1 else "Ela")
        
        if counter == 0 and coach:
            portal_helper = LibrusPortalHelper()
            portal_helper.log_in("10620900", "Krakus1998!")
            subject = "Książeczka zdrowia"
            
            for key, value in coach.items():
                print(f"{key} {value}")
                athletename = to_title_string(key)
                message = (f"Dzień Dobry\n\n"
                           f"przypominamy że badania {name_decantation(athletename)} {value}\n"
                           f"prosilibyśmy o ich jak najszybsze wykonanie i dostarczenie nam zdjęć ważnej książeczki sportowej\n"
                           f"Z poważaniem,\n"
                           f"trenerzy\n"
                           f"Maciej Waliński\n"
                           f"Waldek Krakowiak\n")
                portal_helper.send_message(athletename, subject, message)
            
            portal_helper.close()
            print("Wysłane do rodziców")
        
        elif counter == 1 and coach:
            gmail = GmailPortalHelper()
            subject_for_marcin = "Badania Sportowe"
            message_for_marcin = "Cześć Marcin, \n\nWysyłam Ci listę twoich zawodników, którzy mają nieważne karty sportowca, lub ich ważność wygasa w ciągu 14 dni:"
            
            for key, value in coach.items():
                message_for_marcin += f"\n{to_title_string(key)} badania {value}"
            
            message_for_marcin += "\nPozdrawiam,\nWaldek Krakowiak"
            receiver = "wkrak98@gmail.com"
            gmail.send_email(subject_for_marcin, message_for_marcin, receiver)
            print("Wysłane do Marcina")
        
        elif counter == 2 and coach:
            gmail = GmailPortalHelper()
            subject_for_ela = "Badania Sportowe"
            message_for_ela = "Cześć,\n\nWysyłam Ci listę twoich zawodników, którzy mają nieważne karty sportowca, lub ich ważność wygasa w ciągu 14 dni:"
            
            for key, value in coach.items():
                message_for_ela += f"\n{to_title_string(key)} badania {value}"
            
            message_for_ela += "\n\nPozdrawiam,\nWaldek Krakowiak"
            receiver = "wkrak98@gmail.com"
            gmail.send_email(subject_for_ela, message_for_ela, receiver)
            print("Wysłane do mamy")
        
        if counter == 2:
            print("Zakończono")
        
        counter += 1

if __name__ == "__main__":
    main()
