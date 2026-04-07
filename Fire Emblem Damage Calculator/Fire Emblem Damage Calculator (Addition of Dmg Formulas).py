import random

class Character:
    def __init__(self, name, strength, magic, defense, resistance, hp, max_hp, skill, crit_rate, weapon_type, weapon_mt, element=None, is_ranged=False, speed=10, is_dragon=False):
        self.name = name
        self.strength = strength
        self.magic = magic
        self.defense = defense
        self.resistance = resistance
        self.hp = hp
        self.max_hp = max_hp
        self.skill = skill  # Affects hit chance
        self.crit_rate = crit_rate  # Affects crit chance
        self.weapon_type = weapon_type  # Weapon type: "sword", "axe", "lance", "bow", or "magic"
        self.weapon_mt = weapon_mt  # Might (MT) of the weapon
        self.element = element  # Elemental magic type (anima, dark, light)
        self.is_ranged = is_ranged  # Whether the character is using a ranged weapon (bow)
        self.speed = speed  # Speed affects follow-up attacks
        self.is_dragon = is_dragon  # Whether the character is transformed into a dragon
        self.status = None  # Current status effect (poison, sleep, etc.)

    def attack(self, target, weapon_type, critical=False, terrain=None):
        # Apply terrain effects
        self.apply_terrain_effects(terrain)

        # Check if the attack hits
        hit_chance = self.skill + 30  # Base skill + a fixed bonus
        hit_roll = random.randint(1, 100)
        if hit_roll > hit_chance:
            return (0, "Miss", False, "No counter-attack", False)

        # Check for critical hit
        crit_chance = self.crit_rate
        crit_roll = random.randint(1, 100)
        is_critical = False
        if crit_roll <= crit_chance:
            is_critical = True
            critical = True

        # Calculate damage based on weapon type
        if weapon_type in ["sword", "axe", "lance", "bow"]:
            attack = self.strength
            target_defense = target.defense
            damage = (attack + self.weapon_mt) - target_defense
        elif weapon_type == "magic":
            attack = self.magic
            target_defense = target.resistance
            if self.element:
                damage = self.apply_elemental_affinity(target, attack)
            else:
                damage = attack - target_defense
        else:
            print(f"Error: Invalid weapon type '{weapon_type}'!")
            return (0, "Error", False, "No counter-attack", False)

        if damage < 0:
            damage = 0

        damage = self.apply_weapon_triangle(target, damage)

        if critical:
            damage *= 2

        target.hp -= damage

        target_dead = target.hp <= 0

        counter_attack_result = self.calculate_counter_attack(target)

        hit_result = "Hit" if hit_roll <= hit_chance else "Miss"
        crit_result = "Critical hit!" if is_critical else "No critical"

        return (damage, hit_result, crit_result, counter_attack_result, target_dead)

    def apply_elemental_affinity(self, target, attack):
        element_advantage = {
            "anima": {"dark": 0.8, "light": 1.2},
            "dark": {"light": 0.8, "anima": 1.2},
            "light": {"anima": 0.8, "dark": 1.2},
        }

        if self.element in element_advantage:
            if target.element in element_advantage[self.element]:
                damage_multiplier = element_advantage[self.element][target.element]
                attack *= damage_multiplier
                print(f"{self.name}'s {self.element.capitalize()} magic is {'strong' if damage_multiplier > 1 else 'weak'} against {target.name}'s {target.element.capitalize()} magic!")

        return attack

    def apply_weapon_triangle(self, target, damage):
        weapon_advantage = {
            "sword": {"axe": 1.2, "lance": 0.8, "bow": 1.0, "magic": 1.0},
            "axe": {"lance": 1.2, "sword": 0.8, "bow": 1.0, "magic": 1.0},
            "lance": {"sword": 1.2, "axe": 0.8, "bow": 1.0, "magic": 1.0},
            "bow": {"sword": 0.8, "axe": 0.8, "lance": 0.8, "magic": 1.0},
            "magic": {"sword": 1.0, "axe": 1.0, "lance": 1.0, "bow": 1.0}
        }

        if self.weapon_type in weapon_advantage:
            if target.weapon_type in weapon_advantage[self.weapon_type]:
                damage_multiplier = weapon_advantage[self.weapon_type][target.weapon_type]
                damage *= damage_multiplier
                print(f"{self.name}'s {self.weapon_type.capitalize()} is {'strong' if damage_multiplier > 1 else 'weak'} against {target.name}'s {target.weapon_type.capitalize()}!")

        return damage

    def calculate_counter_attack(self, target):
        if self.is_ranged and target.is_ranged:
            return "No counter-attack"

        if target.is_ranged:
            return "No counter-attack"
        
        if target.weapon_type in ["sword", "axe", "lance"]:
            return self.execute_counter_attack(target)
        return "No counter-attack"

    def execute_counter_attack(self, target):
        print(f"{target.name} counter-attacks!")
        damage, hit_result, crit_result, _, target_dead = target.attack(self, target.weapon_type, critical=False)
        if target_dead:
            print(f"{target.name} has been defeated!")
        return f"Counter-attack! {target.name} deals {damage} damage."

    def apply_terrain_effects(self, terrain):
        if terrain == "forest":
            self.defense += 2
            self.skill += 5
            print(f"{self.name} is in the forest! Defense and skill increased.")
        elif terrain == "mountain":
            self.defense += 4
            print(f"{self.name} is on the mountain! Defense increased.")
        elif terrain == "water":
            self.defense -= 2
            self.speed -= 2
            print(f"{self.name} is in the water! Defense and speed reduced.")
        elif terrain == "open ground":
            print(f"{self.name} is on open ground. No terrain effects.")

    def heal(self, amount):
        self.hp += amount
        if self.hp > self.max_hp:
            self.hp = self.max_hp
        print(f"{self.name} heals for {amount} HP! Current HP: {self.hp}")

def get_valid_input(prompt, valid_choices):
    """Helper function to ensure user enters a valid input."""
    while True:
        user_input = input(prompt).lower()
        if user_input in valid_choices:
            return user_input
        else:
            print(f"Invalid input. Please enter one of the following: {', '.join(valid_choices)}")

def get_character_stats(role):
    print(f"Enter stats for {role}:")
    name = input(f"Name of the {role}: ")
    strength = int(input(f"Strength (for physical attacks) of {role}: "))
    magic = int(input(f"Magic (for magical attacks) of {role}: "))
    defense = int(input(f"Defense (for physical attacks) of {role}: "))
    resistance = int(input(f"Resistance (for magical attacks) of {role}: "))
    hp = int(input(f"HP of {role}: "))
    max_hp = hp
    skill = int(input(f"Skill (affects hit chance) of {role}: "))
    crit_rate = int(input(f"Critical rate (chance of crit) of {role}: "))
    weapon_type = get_valid_input(f"What is {role}'s weapon type? (sword, axe, lance, bow, or magic): ", ["sword", "axe", "lance", "bow", "magic"])
    weapon_mt = int(input(f"What is the Might (MT) of {role}'s weapon? "))
    is_ranged = False
    if weapon_type == "bow":
        is_ranged = True
    element = None
    if weapon_type == "magic":
        element = get_valid_input(f"What is {role}'s magic element? (anima, dark, light): ", ["anima", "dark", "light"])
    return Character(name, strength, magic, defense, resistance, hp, max_hp, skill, crit_rate, weapon_type, weapon_mt, element, is_ranged)

def main():
    print("Welcome to the Fire Emblem Damage Calculator!")

    while True:
        # Get stats for player and enemy
        player = get_character_stats("Player")
        enemy = get_character_stats("Enemy")

        # Ask for the terrain type
        terrain = get_valid_input("Enter terrain type (forest, mountain, water, open ground): ", ["forest", "mountain", "water", "open ground"])

        # Calculate damage with RNG for hit/miss/crit and counter-attack
        damage, hit_result, crit_result, counter_attack_result, player_dead = player.attack(enemy, player.weapon_type, critical=False, terrain=terrain)

        # Output the results
        print(f"{player.name} attacks {enemy.name}!")
        print(f"Result: {hit_result}")
        if hit_result == "Hit":
            print(f"Damage dealt: {damage}")
            print(f"{crit_result}")
        else:
            print("No damage was dealt.")

        print(counter_attack_result)

        # Check if the player or enemy died
        if player_dead:
            print(f"{player.name} has been defeated!")
            return
        if enemy.hp <= 0:
            print(f"{enemy.name} has been defeated!")

        # Show current health status
        print(f"\n{player.name}'s current HP: {player.hp}/{player.max_hp}")
        print(f"{enemy.name}'s current HP: {enemy.hp}/{enemy.max_hp}\n")

        # Ask if the player wants to run the code again
        play_again = input("Do you want to run the battle again? (y/n): ").lower()
        if play_again != 'y':
            print("Thank you for playing!")
            break

if __name__ == "__main__":
    main()
