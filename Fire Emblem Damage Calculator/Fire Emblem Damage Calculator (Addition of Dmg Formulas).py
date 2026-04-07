import random

class Character:
    def __init__(self, name, strength, magic, defense, resistance, hp, skill, crit_rate):
        self.name = name
        self.strength = strength
        self.magic = magic
        self.defense = defense
        self.resistance = resistance
        self.hp = hp
        self.skill = skill  # This will affect hit chance
        self.crit_rate = crit_rate  # This will affect crit chance

    def attack(self, target, weapon_type, critical=False):
        """
        Calculates damage dealt to the target.
        weapon_type: "physical" or "magical"
        critical: Boolean to indicate if it's a critical hit
        Returns: (Damage, Hit result, Crit result)
        """
        hit_chance = self.skill + 30  # Base skill + a fixed bonus
        crit_chance = self.crit_rate  # Weapon or character-based critical rate
        
        # Roll for hit chance
        hit_roll = random.randint(1, 100)
        if hit_roll > hit_chance:
            return (0, "Miss", False)
        
        # Determine if it's a critical hit
        crit_roll = random.randint(1, 100)
        is_critical = False
        if crit_roll <= crit_chance:
            is_critical = True
            critical = True  # If we hit, and crit is true, calculate as critical
        
        # Calculate damage
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
        
        # Double damage if critical hit
        if critical:
            damage *= 2

        hit_result = "Hit" if hit_roll <= hit_chance else "Miss"
        crit_result = "Critical hit!" if is_critical else "No critical"

        return (damage, hit_result, crit_result)

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
    return Character(name, strength, magic, defense, resistance, hp, skill, crit_rate)

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
