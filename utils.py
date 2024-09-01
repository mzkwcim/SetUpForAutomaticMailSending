from datetime import datetime, timedelta

def check_whether_medicals_are_expired_or_will_expire_in_14_days(date_string):
    date = datetime.strptime(date_string, "%Y-%m-%d")
    new_date = date - timedelta(days=14)
    today = datetime.today()
    return new_date < today

def when_medicals_are_expiring(date_string):
    date = datetime.strptime(date_string, "%Y-%m-%d")
    today = datetime.today()
    output = date.strftime("%Y-%m-%d")
    return f"wygasły {output}" if date < today else f"wygasają {output}"

def to_title_string(fullname):
    words = fullname.split()
    return " ".join([word.capitalize() for word in words]).replace(",", "")

def name_decantation(fullname):
    firstname = fullname.split(" ")[1]
    first_to_second_decantation = {
        "Marta": "Marty", "Maria": "Marii", "Piotr": "Piotra", "Stanisław": "Stasia",
        "Patryk": "Patryka", "Dawid": "Dawida", "Jakub": "Kuby", "Mikołaj": "Mikołaja",
        "Natalia": "Natalii", "Blanka": "Blanki", "Bruno": "Bruna", "Mateusz": "Mateusza",
        "Estera": "Estery", "Zofia": "Zosi", "Antonina": "Tosi", "Alan": "Alana",
        "Gabriela": "Gabrysi", "Zuzanna": "Zuzy", "Antoni": "Antka", "Dominik": "Dominika",
        "Iga": "Igi", "Martyna": "Martyny", "Maja": "Mai", "Aleksandra": "Oli"
    }
    return first_to_second_decantation.get(firstname, firstname)
