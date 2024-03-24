# bot code goes here
from Game.Skills import *
from Game.projectiles import *
from ScriptingHelp.usefulFunctions import *
from Game.playerActions import defense_actions, attack_actions, projectile_actions
from Game.gameSettings import HP, LEFTBORDER, RIGHTBORDER, LEFTSTART, RIGHTSTART, PARRYSTUN
from random import randint, random
import itertools
from random import sample
from collections import deque
# Define your Q-Learning agent class
from collections import deque
import json
class QLearningAgent:
    def __init__(self, num_actions, num_states, initial_epsilon=0.5, min_epsilon=0.01, decay_rate=0.995,
                 learning_rate=0.4, discount_factor=0.3, memory_capacity=10000, batch_size=32):
        self.num_actions = num_actions
        self.num_states = num_states
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.epsilon = initial_epsilon
        self.min_epsilon = min_epsilon
        self.decay_rate = decay_rate
        self.q_table = [[0] * num_actions for _ in range(num_states)]
        self.memory = deque(maxlen=memory_capacity)
        self.batch_size = batch_size

    def choose_action(self, state):
        if random() < self.epsilon:
            return randint(0, self.num_actions - 1)
        else:
            return self.get_best_action(state)

    def get_best_action(self, state):
        return self.q_table[state].index(max(self.q_table[state]))

    def update_q_table(self, state, action, reward, next_state):
        best_next_action = self.get_best_action(next_state)
        td_target = reward + self.discount_factor * self.q_table[next_state][best_next_action]
        td_error = td_target - self.q_table[state][action]
        self.q_table[state][action] += self.learning_rate * td_error

    def decay_epsilon(self):
        self.epsilon = max(self.min_epsilon, self.epsilon * self.decay_rate)

    def store_experience(self, state, action, reward, next_state):
        self.memory.append((state, action, reward, next_state))

    def sample_experience(self):
        return sample(self.memory, min(len(self.memory), self.batch_size))

    def learn_from_replay(self):
        if len(self.memory) >= self.batch_size:
            experiences = self.sample_experience()
            for state, action, reward, next_state in experiences:
                self.update_q_table(state, action, reward, next_state)
                
# PRIMARY CAN BE: Teleport, Super Saiyan, Meditate, Dash Attack, Uppercut, One Punch
# SECONDARY CAN BE : Hadoken, Grenade, Boomerang, Bear Trap

# TODO FOR PARTICIPANT: Set primary and secondary skill here
PRIMARY_SKILL = DashAttackSkill
#SECONDARY_SKILL = SuperSaiyanSkill
SECONDARY_SKILL = Hadoken

JUMP = ("move", (0,1))
FORWARD = ("move", (1,0))
BACK = ("move", (-1,0))
JUMP_FORWARD = ("move", (1,1))
JUMP_BACKWARD = ("move", (-1, 1))

# attacks and block
LIGHT = ("light",)
HEAVY = ("heavy",)
BLOCK = ("block",)

PRIMARY = get_skill(PRIMARY_SKILL)
SECONDARY = get_skill(SECONDARY_SKILL)
CANCEL = ("skill_cancel", )

# no move, aka no input
NOMOVE = "NoMove"
# for testing
moves = SECONDARY,
moves_iter = iter(moves)

agent = QLearningAgent(num_actions=13, num_states=2) 

# TODO FOR PARTICIPANT: WRITE YOUR WINNING BOT
class Script:
    def __init__(self):
        self.primary = PRIMARY_SKILL
        self.secondary = SECONDARY_SKILL
        self.previous_state = None
        self.previous_action = None
        self.previous_player_hp = 0
        self.previous_enemy_hp = 0
        self.training_steps = 0 
    # DO NOT TOUCH
    def init_player_skills(self):
        return self.primary, self.secondary
    
    def combo(self, distance, enemyblockstatus):
        combodashattack = [BACK, JUMP_BACKWARD, PRIMARY]
        if distance <= 5 and not enemyblockstatus:
            return combodashattack
        else:
            return []

    def handle_enemy_projectiles(self, player, enemy, enemy_projectiles):
        if enemy_projectiles:
            if get_projectile_type(enemy_projectiles[0]) == Grenade:
                if get_distance(player, enemy) < 3:
                    return JUMP_BACKWARD
            else:
                return JUMP_FORWARD
        return None

    def game_won_by_agent(self, player, enemy):
        return get_hp(player) > get_hp(enemy) and get_hp(enemy) <= 0

    def damage_dealt_to_opponent(self, player, enemy):
        return get_last_move(player) in (HEAVY, LIGHT, PRIMARY, SECONDARY) and self.previous_enemy_hp == get_hp(enemy)

    def agent_avoids_damage(self, player, enemy, prev_player_hp):
        return get_last_move(enemy) in (HEAVY, LIGHT, PRIMARY, SECONDARY) and prev_player_hp == get_hp(player)

    def game_lost_by_agent(self, player, enemy):
        return get_hp(player) <= 0

    def agent_takes_damage(self, player, enemy):
        return get_hp(player) < self.previous_player_hp

    def agent_remains_inactive(self):
        return self.previous_action == NOMOVE

    def is_enemy_hit(self, player, enemy, enemy_projectiles):
        if not get_block_status(enemy): 
            player_last_move = get_last_move(player)
            if player_last_move in (LIGHT, HEAVY) and get_distance(player, enemy) <= prim_range(player):
                return True
            elif player_last_move == SECONDARY:
                for proj in enemy_projectiles:
                    if get_projectile_type(proj) == get_secondary_skill(player):
                        proj_pos = get_proj_pos(proj)
                        if proj_pos[0] == get_pos(enemy)[0]:
                            return True
            return False

    def primary_hit(self, player, enemy):
        if get_last_move(player) == PRIMARY and get_hp(enemy) < previous_enemy_hp:
            return True
        return False

    def is_hit_by_consecutive_light_attacks(self, player, enemy):
        enemy_last_move = get_last_move(enemy)
        if enemy_last_move == LIGHT and get_hp(player) < self.previous_player_hp:  
            # Check if the player's last move was a light attack and player's HP decreased
            self.consecutive_light_hits += 1
        else:
            self.consecutive_light_hits = 0  # Reset consecutive hit count if last move was not a light attack
        
        self.previous_player_hp = get_hp(player)  # Update previous player's HP
        
        return self.consecutive_light_hits > 1

        
    def calculate_reward(self, player, enemy, player_projectiles, enemy_projectiles):
        reward = 0
        hp_difference = get_hp(player) - get_hp(enemy)
        # Check if the game has been won by the agent
        if hp_difference > 0:
            reward += 50
        else:
            reward -= 30
            
        if self.game_won_by_agent(player, enemy):
            reward += 70
                
        # Check if damage was dealt to the opponent
        if self.damage_dealt_to_opponent(player, enemy):
            reward += 20
                
        # Check if the agent successfully avoided taking damage
        if self.agent_avoids_damage(player, enemy, self.previous_player_hp):
            reward += 10
                
        # Check if the game was lost by the agent
        if self.game_lost_by_agent(player, enemy):
            reward -= 100
                
        # Check if the agent took damage
        if self.agent_takes_damage(player, enemy):
            reward -= 50
                
        # Penalize inactivity
        if self.agent_remains_inactive():
            reward -= 5

        if self.is_hit_by_consecutive_light_attacks(player,enemy):
            reward -= 10

        if self.primary_hit(player, enemy):
            reward +=30
        return reward

    
    # MAIN FUNCTION that returns a single move to the game manager
    def get_move(self, player, enemy, player_projectiles, enemy_projectiles):
        # Assuming your state space has 2 states (for demonstration)
        # You need to define your own state representation
        # Example: state = 0 if player's health is higher else 1
        state = 0 if get_hp(player) > get_hp(enemy) else 1
        agent.decay_epsilon() 
        # Choose action using Q-Learning agent
        action = agent.choose_action(state)
        self.previous_player_hp = get_hp(player)
        self.previous_enemy_hp = get_hp(enemy)
        
        # Check for combo actions
        is_jumping = get_last_move(player) in JUMP
        is_enemy_jumping = get_last_move(enemy) in JUMP
        combo_actions = [
            ([PRIMARY], lambda distance, is_jumping: distance < 7 and not is_jumping),
            ([PRIMARY, LIGHT], lambda distance, is_jumping: distance < 7 and not is_jumping),
            ([PRIMARY, HEAVY], lambda distance, is_jumping: distance < 7 and not is_jumping),
            ([PRIMARY, BLOCK], lambda distance, is_jumping: distance < 7 and not is_jumping),
            ([PRIMARY, JUMP_FORWARD], lambda distance, is_jumping: False),
            ([PRIMARY, JUMP_BACKWARD], lambda distance, is_jumping: False),
            ([PRIMARY, PRIMARY], lambda distance, is_jumping: distance < 7 and not is_jumping),
            ([PRIMARY, SECONDARY], lambda distance, is_jumping: distance < 7 and not is_jumping),
            ([PRIMARY, CANCEL], lambda distance, is_jumping: distance < 7 and not is_jumping),
            ([PRIMARY, NOMOVE], lambda distance, is_jumping: distance < 7 and not is_jumping),
        ]

        if SECONDARY == SuperSaiyanSkill:
            combo_actions = [
                ([SECONDARY], lambda is_jumping: is_jumping and get_last_move(player) == BACK),
                ([LIGHT], lambda distance, is_jumping: distance < 3 and not is_jumping),
                ([LIGHT, PRIMARY], lambda distance, is_jumping: distance < 3 and not is_jumping)
        ]
        elif SECONDARY == Hadoken:
            combo_actions.extend([
                ([SECONDARY], lambda is_jumping: is_jumping),
                ([SECONDARY], lambda is_jumping: not is_jumping),
                ([SECONDARY, LIGHT], lambda is_jumping: is_jumping),
                ([SECONDARY, HEAVY], lambda is_jumping: is_jumping),
                ([SECONDARY, BLOCK], lambda is_jumping: is_jumping),
                ([SECONDARY, JUMP_FORWARD], lambda is_jumping: not is_jumping),
                ([SECONDARY, JUMP_BACKWARD], lambda is_jumping: not is_jumping),
                ([SECONDARY, PRIMARY], lambda is_jumping: is_jumping),
                ([SECONDARY, SECONDARY], lambda is_jumping: is_jumping),
                ([SECONDARY, CANCEL], lambda is_jumping: is_jumping),
                ([SECONDARY, NOMOVE], lambda is_jumping: is_jumping),
            ])

        #action
        # Execute action based on chosen action
        if action == 0:
            move = FORWARD
        elif action == 1:
            move = BACK
        elif action == 2:
            move = LIGHT
        elif action == 3:
            move = HEAVY
        elif action == 4:
            move = BLOCK
        elif action == 5:
            move = JUMP
        elif action == 6:
            move = JUMP_BACKWARD
        elif action == 7:
            move = JUMP_FORWARD
        elif action == 8:
            move = PRIMARY
        elif action == 9:
            move = SECONDARY
        elif action ==10:
            move = CANCEL
        elif action ==11:
            move = self.combo(get_distance(player, enemy), get_block_status(enemy))
        elif action ==12:
            move = self.handle_enemy_projectiles(player, enemy, enemy_projectiles)
        elif action == 13:
            for combo_action, condition in combo_actions:
                if condition(get_distance(player, enemy), is_jumping):
                    move = combo_action
                    break
        else:
            move = NOMOVE     
        # Update Q-table if this is not the first move
        if self.previous_state is not None:
            reward = self.calculate_reward(player, enemy, player_projectiles, enemy_projectiles)
            #agent.update_q_table(self.previous_state, self.previous_action, reward, state)
            agent.store_experience(self.previous_state, self.previous_action, reward, state)
        # Store current state and action as previous state and action for the next iteration
        self.previous_state = state
        self.previous_action = action
        agent.learn_from_replay()
        return move


