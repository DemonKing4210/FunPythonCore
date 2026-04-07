import random

class Character:
    def __init__(self, name, strength, magic, defense, resistance, hp, max_hp, skill, crit_rate, weapon_type, is_ranged=False, speed=10, is_dragon=False):
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
        self.is_ranged = is_ranged  # Whether the character is using a ranged weapon (bow)
        self.speed = speed  # Speed affects follow-up attacks
        self.is_dragon = is_dragon  # Whether the character is transformed into a dragon
        self.status = None  # Current status effect (poison, sleep, etc.)

    def attack(self, target, weapon_type, critical=False, terrain=None):
        """
        Calculates damage dealt to the target considering terrain, follow-up attacks, and critical hits.
        weapon_type: The weapon used by the attacker
        critical: Boolean to indicate if it's a critical hit
        terrain: The terrain the battle is taking place on (affects defense and avoidance)
        Returns: (Damage, Hit result, Crit result, Counter-Attack result)
        """

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
        if weapon_type == "physical":
            attack = self.strength
            target_defense = target.defense
        elif weapon_type == "magical":
            attack = self.magic
            target_defense = target.resistance
        else:
            print("Invalid weapon type!")
            return (0, "Error", False, "No counter-attack", False)

        damage = attack - target_defense
        if damage < 0:
            damage = 0
        
        # Weapon triangle advantage (simplified here)
        damage = self.apply_weapon_triangle(target, damage)

        # Double damage if critical hit
        if critical:
            damage *= 2

        # Determine if the enemy can counter-attack
        counter_attack_result = self.calculate_counter_attack(target)

        # Apply follow-up attack if speed is greater
        follow_up_damage = 0
        if self.speed > target.speed:
            print(f"{self.name} performs a follow-up attack!")
            follow_up_damage = self.strength  # Follow-up attack damage

        # Apply damage to the target
        target.hp -= damage + follow_up_damage

        # Check if the target dies after the attack
        target_dead = target.hp <= 0

        hit_result = "Hit" if hit_roll <= hit_chance else "Miss"
        crit_result = "Critical hit!" if is_critical else "No critical"

        return (damage + follow_up_damage, hit_result, crit_result, counter_attack_result, target_dead)

    def apply_weapon_triangle(self, target, damage):
        """Applies the weapon triangle advantage or disadvantage."""
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
        damage, _, _, _, target_dead = target.attack(self, target.weapon_type, critical=False)
        if target_dead:
            print(f"{target.name} has been defeated!")
        return f"Counter-attack! {target.name} deals {damage} damage."

    def apply_terrain_effects(self, terrain):
        """Modifies stats based on the terrain."""
        if terrain == "forest":
            self.defense += 2  # Forest boosts defense
            self.skill += 5  # Forest increases avoidance (hit chance)
            print(f"{self.name} is in the forest! Defense and skill increased.")

        elif terrain == "mountain":
            self.defense += 4  # Mountain boosts defense
            print(f"{self.name} is on the mountain! Defense increased.")

        elif terrain == "water":
            self.defense -= 2  # Water reduces defense
            self.speed -= 2  # Water reduces movement
            print(f"{self.name} is in the water! Defense and speed reduced.")

        elif terrain == "open ground":
            print(f"{self.name} is on open ground. No terrain effects.")

    def heal(self, amount):
        """Heals the character by the specified amount."""
        self.hp += amount
        if self.hp > self.max_hp:
            self.hp = self.max_hp
        print(f"{self.name} heals for {amount} HP! Current HP: {self.hp}")

def get_character_stats(role):
    """Helper function to get stats for either player or enemy."""
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
    weapon_type = input(f"What is {role}'s weapon type? (sword, axe, lance, bow, or magic): ").lower()
    is_ranged = False
    if weapon_type == "bow":
        is_ranged = True
    return Character(name, strength, magic, defense, resistance, hp, max_hp, skill, crit_rate, weapon_type, is_ranged)

def main():
    print("Welcome to the Fire Emblem Damage Calculator!")

    # Get stats for player and enemy
    player = get_character_stats("Player")
    enemy = get_character_stats("Enemy")

    # Ask for the weapon type
    weapon_type = input("Enter weapon type (physical or magical): ").lower()

    # Ask for the terrain type
    terrain = input("Enter terrain type (forest, mountain, water, open ground): ").lower()

    # Calculate damage with RNG for hit/miss/crit and counter-attack
    damage, hit_result, crit_result, counter_attack_result, player_dead = player.attack(enemy, weapon_type, critical=False, terrain=terrain)

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

    # Check if the player or enemy died
    if player_dead:
        print(f"{player.name} has been defeated!")
        return
    if enemy.hp <= 0:
        print(f"{enemy.name} has been defeated!")
        return

    # If neither died, continue the battle
    print(f"{player.name} and {enemy.name} are still standing...")

if __name__ == "__main__":
    main()
