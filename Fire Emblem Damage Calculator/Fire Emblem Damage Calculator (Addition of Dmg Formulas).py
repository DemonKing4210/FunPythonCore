import random

class Character:
    def __init__(self, name, strength, magic, defense, resistance, hp, skill, crit_rate, weapon_type):
        self.name = name
        self.strength = strength
        self.magic = magic
        self.defense = defense
        self.resistance = resistance
        self.hp = hp
        self.skill = skill  # Affects hit chance
        self.crit_rate = crit_rate  # Affects crit chance
        self.weapon_type = weapon_type  # Weapon type: "sword", "axe", or "lance"

    def attack(self, target, weapon_type, critical=False):
        """
        Calculates damage dealt to the target.
        weapon_type: The weapon used by the attacker
        critical: Boolean to indicate if it's a critical hit
        Returns: (Damage, Hit result, Crit result)
        """
        # Check if the attack hits
        hit_chance = self.skill + 30  # Base skill + a fixed bonus
        hit_roll = random.randint(1, 100)
        if hit_roll > hit_chance:
            return (0, "Miss", False)

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
            return (0, "Error", False)

        damage = attack - target_defense
        if damage < 0:
            damage = 0
        
        # Weapon triangle advantage
        damage = self.apply_weapon_triangle(target, damage)

        # Double damage if critical hit
        if critical:
            damage *= 2

        hit_result = "Hit" if hit_roll <= hit_chance else "Miss"
        crit_result = "Critical hit!" if is_critical else "No critical"

        return (damage, hit_result, crit_result)

    def apply_weapon_triangle(self, target, damage):
        """Applies the weapon triangle advantage or disadvantage."""
        # Strengths and weaknesses in the weapon triangle
        weapon_advantage = {
            "sword": {"axe": 1.2, "lance": 0.8},  # Sword > Axe, Sword < Lance
            "axe": {"lance": 1.2, "sword": 0.8},  # Axe > Lance, Axe < Sword
            "lance": {"sword": 1.2, "axe": 0.8}   # Lance > Sword, Lance < Axe
        }

        if self.weapon_type in weapon_advantage:
            if target.weapon_type in weapon_advantage[self.weapon_type]:
                damage_multiplier = weapon_advantage[self.weapon_type][target.weapon_type]
                damage *= damage_multiplier
                print(f"{self.name}'s {self.weapon_type.capitalize()} is {'strong' if damage_multiplier > 1 else 'weak'} against {target.name}'s {target.weapon_type.capitalize()}!")

        return damage

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
    weapon_type = input(f"What is {role}'s weapon type? (sword, axe, or lance): ").lower()
    return Character(name, strength, magic, defense, resistance, hp, skill, crit_rate, weapon_type)

def main():
    print("Welcome to the Fire Emblem Damage Calculator!")

    # Get stats for player and enemy
    player = get_character_stats("Player")
    enemy = get_character_stats("Enemy")

    # Ask for the weapon type
    weapon_type = input("Enter weapon type (physical or magical): ").lower()

    # Calculate damage with RNG for hit/miss/crit
    damage, hit_result, crit_result = player.attack(enemy, weapon_type)

    # Output the results
    print(f"{player.name} attacks {enemy.name}!")
    print(f"Result: {hit_result}")
    if hit_result == "Hit":
        print(f"Damage dealt: {damage}")
        print(f"{crit_result}")
    else:
        print("No damage was dealt.")

if __name__ == "__main__":
    main()
