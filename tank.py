class Tank:
    def __init__(self, armor, penetration, armor_type):
        self.armor = armor
        self.penetration = penetration

        # Vérifie si le type d'armure est valide, sinon on met 'unknown' et on affiche un avertissement
        if armor_type not in ['chobham', 'composite', 'ceramic']:
            print(f"Attention : armure '{armor_type}' non reconnue, je mets 'unknown'")
            self.armor_type = 'unknown'
        else:
            self.armor_type = armor_type
        
        self.name = "Tank"

    def set_name(self, name):
        self.name = name

    def is_vulnerable(self, other_tank):
        # Calcule l'armure réelle selon le type d'armure
        real_armor = self.armor
        if self.armor_type == 'chobham':
            real_armor += 100
        elif self.armor_type in ['composite', 'ceramic']:
            real_armor += 50
        # Si 'unknown', pas d'ajout

        # Retourne True si la pénétration de l'autre tank est supérieure ou égale
        return real_armor <= other_tank.penetration

    def swap_armor(self, other_tank):
        # Échange les valeurs d'armure entre les deux tanks
        temp = other_tank.armor
        other_tank.armor = self.armor
        self.armor = temp

    def __repr__(self):
        # Remplace espaces par tirets et met en minuscules
        return self.name.replace(' ', '-').lower()


# Création de deux tanks avec armure chobham
tank1 = Tank(600, 670, 'chobham')
tank2 = Tank(620, 670, 'chobham')

if tank1.is_vulnerable(tank2):
    print("Tank1 is vulnerable to Tank2")

# Échange des armures
tank1.swap_armor(tank2)

# Création d'une liste de tanks avec un type d'armure pas prévu ('steel')
tank_list = []
for i in range(5):
    t = Tank(400, 400, 'steel')  # 'steel' non valide mais accepte avec warning
    t.set_name(f'Tank_{i}_Small')
    tank_list.append(t)

# Teste la vulnérabilité de chaque tank face à tank1
vuln_tests = []
for tank in tank_list:
    vuln_tests.append(tank.is_vulnerable(tank1))

def test_tank_safe(vuln_results):
    # Affiche dès qu'on trouve un tank vulnérable (safe)
    for vuln in vuln_results:
        if vuln:
            print("At least one tank is safe")
            return
    print("No tank is safe")

test_tank_safe(vuln_tests)
