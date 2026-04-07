def attack(self, target, weapon_type, critical=False, terrain=None):
    """
    Calculates damage dealt to the target considering terrain, follow-up attacks, critical hits, and elemental magic.
    weapon_type: The weapon used by the attacker
    critical: Boolean to indicate if it's a critical hit
    terrain: The terrain the battle is taking place on (affects defense and avoidance)
    Returns: (Damage, Hit result, Crit result, Counter-Attack result, Target Dead)
    """
    # Apply terrain effects
    self.apply_terrain_effects(terrain)

    # Check if the attack hits
    hit_chance = self.skill + 30  # Base skill + a fixed bonus
    hit_roll = random.randint(1, 100)
    hit_result = "Hit" if hit_roll <= hit_chance else "Miss"
    
    if hit_result == "Miss":
        # If the player's attack misses, there's no damage, but still check counter-attack.
        print(f"{self.name}'s attack missed!")
        return (0, hit_result, False, self.calculate_counter_attack(target), False)

    # If the player's attack hits, check for critical hit
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
        damage = (attack + self.weapon_mt) - target_defense
    elif weapon_type == "magical":
        attack = self.magic
        target_defense = target.resistance
        if self.element:
            damage = self.apply_elemental_affinity(target, attack)
        else:
            damage = attack - target_defense
    else:
        print("Invalid weapon type!")
        return (0, "Error", False, "No counter-attack", False)

    # If damage is less than 0, set it to 0 (no negative damage)
    if damage < 0:
        damage = 0

    # Weapon triangle advantage (simplified here)
    damage = self.apply_weapon_triangle(target, damage)

    # Double damage if critical hit
    if critical:
        damage *= 2

    # Apply follow-up attack if speed is greater
    follow_up_damage = 0
    if self.speed > target.speed:
        print(f"{self.name} performs a follow-up attack!")
        follow_up_damage = self.strength  # Follow-up attack damage

    # Apply damage to the target
    target.hp -= damage + follow_up_damage

    # Check if the target dies after the attack
    target_dead = target.hp <= 0

    crit_result = "Critical hit!" if is_critical else "No critical"

    # Calculate counter-attack if the attack hit and the target can counter
    counter_attack_result = self.calculate_counter_attack(target)

    return (damage + follow_up_damage, hit_result, crit_result, counter_attack_result, target_dead)

def calculate_counter_attack(self, target):
    """Determines if the target can counter-attack after the player's attack."""
    if self.is_ranged and target.is_ranged:
        return "No counter-attack"  # Ranged units cannot counter-attack at range

    if target.is_ranged:
        return "No counter-attack"  # Ranged units cannot counter-attack in close combat
    
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
