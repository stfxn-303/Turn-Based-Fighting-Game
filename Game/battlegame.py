import random
from datetime import datetime

# Constants for attack and defense values
WARRIOR_ATK_RANGE = (5, 20)
TANKER_ATK_RANGE = (1, 10)
WARRIOR_DEF_RANGE = (1, 10)
TANKER_DEF_RANGE = (5, 15)
STARTING_HP = 100
EXP_THRESHOLD = 100
TEAM_LIMIT = 3
AI_WARRIOR_ATK_RANGE = (5, 20)  
AI_TANKER_ATK_RANGE = (1, 10)   
AI_WARRIOR_DEF_RANGE = (1, 10) 
AI_TANKER_DEF_RANGE = (5, 15) 

# Unit class representing each character
class Unit:
    def __init__(self, name, role, is_ai=False):
        self.name = name
        self.role = role
        self.is_ai = is_ai  # Add a flag to determine if the unit is AI
        self.hp = STARTING_HP
        self.exp = 0
        self.level = 1

                # Attack and defense values based on role
        if role == "Warrior":
            self.atk = random.randint(*WARRIOR_ATK_RANGE)
            self.defense = random.randint(*WARRIOR_DEF_RANGE)
        elif role == "Tanker":
            self.atk = random.randint(*TANKER_ATK_RANGE)
            self.defense = random.randint(*TANKER_DEF_RANGE)
        elif role == "AI_Warrior":  # AI Warrior defense
            self.atk = random.randint(*WARRIOR_ATK_RANGE)
            self.defense = random.randint(*AI_WARRIOR_DEF_RANGE)
        elif role == "AI_Tanker":  # AI Tanker defense
            self.atk = random.randint(*TANKER_ATK_RANGE)
            self.defense = random.randint(*AI_TANKER_DEF_RANGE)


    def attack(self, target):
        random_damage = random.randint(-5, 5)  # Add some randomness to the damage
        total_damage = max(0, self.atk - target.defense + random_damage)
        target.hp -= total_damage
        exp_earned = total_damage * (0.2 if total_damage > 10 else 0.5)
        self.exp += exp_earned
        if self.exp >= EXP_THRESHOLD:
            self.level_up()
        return total_damage, exp_earned

    def level_up(self):
        self.level += 1
        self.exp = 0

    def is_alive(self):
        return self.hp > 0

# Game class to manage game actions and events
# Game class to manage game actions and events
class Game:
    def __init__(self, player_team, ai_team):
        self.player_team = player_team
        self.ai_team = ai_team
        self.event_log = []

    def check_game_over(self):
                # Check if all members of the player team or AI team are dead
        if all(not unit.is_alive() for unit in self.player_team):
            return True  # Game over if player team is all dead
        if all(not unit.is_alive() for unit in self.ai_team):
            return True  # Game over if AI team is all dead
        return False  # Game is still ongoing

    def record_event(self, event):
        self.event_log.append(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {event}")

    def restart_game(self):
        for unit in self.player_team + self.ai_team:
            unit.hp = STARTING_HP  # Assuming this is a constant value
            unit.exp = 0
            unit.level = 1
        self.event_log = []

    def ai_turn(self):
        # AI selects a living unit
        ai_unit = random.choice([unit for unit in self.ai_team if unit.is_alive()])
        # AI selects a living target from the player's team
        player_target = random.choice([unit for unit in self.player_team if unit.is_alive()])
        
        # Perform AI attack
        damage, exp_earned = ai_unit.attack(player_target)
        event = f"{ai_unit.name} attacked {player_target.name} and inflicted {damage} damage."
        self.record_event(event)

def ai_turn(self):
    ai_unit = random.choice([unit for unit in self.ai_team if unit.is_alive()])  # Choose a random AI unit
    player_target = random.choice([unit for unit in self.player_team if unit.is_alive()])  # Choose a random player unit

    # AI performs an attack on a player unit
    damage, exp_gain = ai_unit.attack(player_target)

    # Log the attack
    event = f"{datetime.now()} - {ai_unit.name} inflicted {damage} damage on {player_target.name}."
    self.record_event(event)

    def is_game_over(self):
        return all(not unit.is_alive() for unit in self.player_team) or all(not unit.is_alive() for unit in self.ai_team)

    def determine_winner(self):
        if all(not unit.is_alive() for unit in self.ai_team):
            return "Player Team"
        elif all(not unit.is_alive() for unit in self.player_team):
            return "AI Team"
        return None

    def record_event(self, event):
        self.event_log.append(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {event}")

    def save_log(self):
        with open("game_log.txt", "w") as file:
            file.write("\n".join(self.event_log))



# Function to build a team with specified role names
def build_team(name_prefix):
    team = []
    for i in range(TEAM_LIMIT):
        role = random.choice(["Warrior", "Tanker"])
        team.append(Unit(name=f"{name_prefix}{i}", role=role))
    return team