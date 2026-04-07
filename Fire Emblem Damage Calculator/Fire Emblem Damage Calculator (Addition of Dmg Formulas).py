class Character:
    def __init__(self, name, strength, magic, defense, resistance, hp):
        self.name = name
        self.strength = strength
        self.magic = magic
        self.defense = defense
        self.resistance = resistance
        self.hp = hp

    def attack(self, target, weapon_type, critical=False):
        """
        Calculates damage dealt to the target.
        weapon_type: "physical" or "magical"
        critical: Boolean to indicate if it's a critical hit
        """
        if weapon_type == "physical":
            attack = self.strength
            target_defense = target.defense
        elif weapon_type == "magical":
            attack = self.magic
            target_defense = target.resistance
        else:
            print("Invalid weapon type!")
            return 0
        
        damage = attack - target_defense
        if damage < 0:
            damage = 0
        
        # Double damage if critical hit
        if critical:
            damage *= 2
        
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
    return Character(name, strength, magic, defense, resistance, hp)

def main():
    print("Welcome to the Fire Emblem Damage Calculator!")

    # Get stats for player and enemy
    player = get_character_stats("Player")
    enemy = get_character_stats("Enemy")

    # Ask for the weapon type
    weapon_type = input("Enter weapon type (physical or magical): ").lower()

    # Ask if it's a critical hit
    critical_input = input("Is it a critical hit? (yes/no): ").lower()
    critical = True if critical_input == "yes" else False

    # Calculate damage
    damage = player.attack(enemy, weapon_type, critical)
    print(f"{player.name} attacks {enemy.name} for {damage} damage!")

    # Optionally show critical hit result
    if critical:
        print(f"Critical hit! {player.name} dealt double damage.")

if __name__ == "__main__":
    main()
