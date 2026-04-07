import random

class Character:
    def __init__(self, name, strength, magic, defense, resistance, hp, max_hp, skill, crit_rate, weapon_type, is_ranged=False, speed=10, skills=None, is_dragon=False):
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
        self.skills = skills if skills else []  # List of skills the character has
        self.is_dragon = is_dragon  # Whether the character is transformed into a dragon
        self.status = None  # Current status effect (poison, sleep, etc.)
    
    def attack(self, target, weapon_type, critical=False):
        # Check if the attack hits, considering hit chance and possible skills like "Astra"
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

        # Apply skills like "Astra" (multiple attacks)
        if "Astra" in self.skills:
            follow_up_damage = self.follow_up_attack(target)
            return (damage, "Hit", "No critical", counter_attack_result, follow_up_damage)

        hit_result = "Hit" if hit_roll <= hit_chance else "Miss"
        crit_result = "Critical hit!" if is_critical else "No critical"

        return (damage, hit_result, crit_result, counter_attack_result)

    def follow_up_attack(self, target):
        """Performs a follow-up attack if the character's speed is greater than the enemy's."""
        if self.speed > target.speed:
            print(f"{self.name} performs a follow-up attack!")
            return self.strength  # Damage from the follow-up attack
        return 0

    # Other methods remain unchanged

