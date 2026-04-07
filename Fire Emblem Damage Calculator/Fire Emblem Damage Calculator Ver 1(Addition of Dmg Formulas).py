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

def main():
    # Example characters
    attacker = Character(name="Hero", strength=12, magic=5, defense=8, resistance=3, hp=40)
    defender = Character(name="Enemy", strength=10, magic=4, defense=7, resistance=6, hp=35)

    # Weapon type (physical or magical)
    weapon_type = "physical"  # You can also try "magical"

    # Calculate damage
    damage = attacker.attack(defender, weapon_type, critical=False)
    print(f"{attacker.name} attacks {defender.name} for {damage} damage!")

    # With critical hit
    critical_damage = attacker.attack(defender, weapon_type, critical=True)
    print(f"Critical hit! {attacker.name} attacks {defender.name} for {critical_damage} damage!")

if __name__ == "__main__":
    main()
