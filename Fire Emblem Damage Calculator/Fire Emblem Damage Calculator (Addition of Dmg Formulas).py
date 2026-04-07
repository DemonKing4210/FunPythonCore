import random

class Character:
    def __init__(self, name, strength, magic, defense, resistance, hp, skill, crit_rate, weapon_type, is_ranged=False):
        self.name = name
        self.strength = strength
        self.magic = magic
        self.defense = defense
        self.resistance = resistance
        self.hp = hp
        self.skill = skill  # Affects hit chance
        self.crit_rate = crit_rate  # Affects crit chance
        self.weapon_type = weapon_type  # Weapon type: "sword", "axe", "lance", or "bow"
        self.is_ranged = is_ranged  # Whether the character is using a ranged weapon (bow)

    def attack(self, target, weapon_type, critical=False):
        """
        Calculates damage dealt to the target.
        weapon_type: The weapon used by the attacker
        critical: Boolean to indicate if it's a critical hit
        Returns: (Damage, Hit result, Crit result, Counter-Attack result)
        """
        # Check if the attack hits
        hit_chance = self.skill + 30  # Base skill + a fixed bonus
        hit_roll = random.randint(1, 100)
        if hit_roll > hit_chance:
            return (0, "Miss", False, "No counter-attack")

        # Check for critical hit
        crit_chance = self.crit_rate
        crit_roll = random.randint(1, 100)
        is_critical = False
        if crit_roll <= crit_chance:
            is_critical = True
            critical = True  # If we hit, and crit is true, calculate as critical

        # Determine the damage based on weapon type
        if weapon_type == "physical":
            attack = self.strength
            target_defense = target.defense
        elif weapon_type == "magical":
            attack = self.magic
            target_defense = target.resistance
        else:
            print("Invalid weapon type!")
            return (0, "Error", False, "No counter-attack")

        damage = attack - target_defense
        if damage < 0:
            damage = 0
        
        # Weapon triangle advantage
        damage = self.apply_weapon_triangle(target, damage)

        # Double damage if critical hit
        if critical:
            damage *= 2

        # Determine if the enemy can counter-attack
        counter_attack_result = self.calculate_counter_attack(target)

        hit_result = "Hit" if hit_roll <= hit_chance else "Miss"
        crit_result = "Critical hit!" if is_critical else "No critical"

        return (damage, hit_result, crit_result, counter_attack_result)

    def apply_weapon_triangle(self, target, damage):
        """Applies the weapon triangle advantage or disadvantage."""
        # Strengths and weaknesses in the weapon triangle
        weapon_advantage = {
            "sword": {"axe": 1.2, "lance": 0.8, "bow": 1.0},  # Sword > Axe, Sword < Lance
            "axe": {"lance": 1.2, "sword": 0.8, "bow": 1.0},  # Axe > Lance, Axe < Sword
            "lance": {"sword": 1.2, "axe": 0.8, "bow": 1.0},  # Lance > Sword, Lance < Axe
            "bow": {"sword": 0.8, "axe": 0.8, "lance": 0.8}   # Bow < Sword, Bow < Axe, Bow < Lance
        }

        if self.weapon_type in weapon_advantage:
            if target.weapon_type in weapon_advantage[self.weapon_type]:
                damage_multiplier = weapon_advantage[self.weapon_type][target.weapon_type]
                damage *= damage_multiplier
                print(f"{self.name}'s {self.weapon_type.capitalize()} is {'strong' if damage_multiplier > 1 else 'weak'} against {target.name}'s {target.weapon_type.capitalize()}!")

        return damage

    def calculate_counter_attack(self, target):
        """Determines if the target can counter-attack."""
        if target.is_ranged:
            return "No counter-attack"  # Bows cannot counter-attack in close combat
        
        # If the attacker is using a melee weapon and the target is within range
        if target.weapon_type in ["sword", "axe", "lance"]:
            return self.execute_counter_attack(target)
        return "No counter-attack"

    def execute_counter_attack(self, target):
        """Performs the counter-attack and returns its result."""
        print(f"{target.name} counter-attacks!")
        # Perform counter-attack using the target's weapon
        damage, _, _, _ = target.attack(self, target.weapon_type, critical=False)
        return f"Counter-attack! {target.name} deals {damage} damage."

def get_character_stats(role):
    """Helper function to get stats for either player or enemy."""
    print(f"Enter stats for {role}:")
    name = input(f"Name of the {role}: ")
    strength = int(input(f"Strength (for physical attacks) of {role}: "))
    magic = int(input(f"Magic (for magical attacks) of {role}: "))
    defense = int(input(f"Defense (for physical attacks) of {role}: "))
    resistance = int(input(f"Resistance (for magical attacks) of {role}: "))
    hp = int(input(f"HP of {role}: "))
    skill = int(input(f"Skill (affects hit chance) of {role}: "))
    crit_rate = int(input(f"Critical rate (chance of crit) of {role}: "))
    weapon_type = input(f"What is {role}'s weapon type? (sword, axe, lance, or bow): ").lower()
    is_ranged = False
    if weapon_type == "bow":
        is_ranged = True
    return Character(name, strength, magic, defense, resistance, hp, skill, crit_rate, weapon_type, is_ranged)

def main():
    print("Welcome to the Fire Emblem Damage Calculator!")

    # Get stats for player and enemy
    player = get_character_stats("Player")
    enemy = get_character_stats("Enemy")

    # Ask for the weapon type
    weapon_type = input("Enter weapon type (physical or magical): ").lower()

    # Calculate damage with RNG for hit/miss/crit and counter-attack
    damage, hit_result, crit_result, counter_attack_result = player.attack(enemy, weapon_type)

    # Output the results
    print(f"{player.name} attacks {enemy.name}!")
    print(f"Result: {hit_result}")
    if hit_result == "Hit":
        print(f"Damage dealt: {damage}")
        print(f"{crit_result}")
    else:
        print("No damage was dealt.")

    # Output counter-attack result
    print(counter_attack_result)

if __name__ == "__main__":
    main()
