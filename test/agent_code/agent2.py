import math
import random

class Agent2(Agent):
    angle = 20
    speed = 250

    random_movement_timer = 30 * 2
    random_cooldown_timer = 0

    def run(self):
        Agent2.random_movement_timer -= 1
        if Agent2.random_movement_timer <= 0:
            self.randomize_movement()
            Agent2.random_movement_timer = 30 * 2
            Agent2.random_cooldown_timer = 30
        if Agent2.random_cooldown_timer > 0:
            Agent2.random_cooldown_timer -= 1

        self.set_movement_speed(Agent2.speed)
        if Agent2.random_cooldown_timer <= 0:
            self.set_movement_direction(Agent2.angle)

    def randomize_movement(self):
        Agent2.angle = random.random() * 360
        self.set_movement_direction(Agent2.angle)

    def on_obstacle_hit(self):
        # Change direction when an obstacle is hit
        Agent2.angle -= 180
        Agent2.angle %= 360

    def on_enemy_scanned(self, enemy_position):
        self.activate_shield()
        # shoot towards enemy when they are near
        distance = (enemy_position.x - self.get_position().x, enemy_position.y - self.get_position().y)
        angle = math.degrees(math.atan2(distance[1], distance[0]))
        self.attack_ranged(angle)
        # run away from the enemy!
        Agent2.angle = 180 - angle
        Agent2.angle %= 180

    def on_damage_taken(self):
        # activate shield and change direction when hit
        self.activate_shield()
        Agent2.angle -= 45