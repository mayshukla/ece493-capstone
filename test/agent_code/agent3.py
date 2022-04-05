import math

class Agent3(Agent):
    angle = 20
    speed = 250

    def run(self):
        # if the enemy is not near deactivate shield so that it is ready when needed
        if self.is_shield_activated() and (len(self.get_agents_position()) == 0) and (self.get_shield_time() < 8):
            self.deactivate_shield()
        self.set_movement_speed(Agent3.speed)
        self.set_movement_direction(Agent3.angle)

    def on_obstacle_scanned(self, obstacle_position):
        # Change direction when an obstacle is scanned
        rel_position = (obstacle_position.x - self.get_position().x, obstacle_position.y - self.get_position().y)
        angle = math.degrees(math.atan2(rel_position[1], rel_position[0]))
        Agent3.angle = 0 - angle

    def on_enemy_scanned(self, enemy_position):
        # shoot towards enemy when they are near
        rel_position = (enemy_position.x - self.get_position().x, enemy_position.y - self.get_position().y)
        angle = math.degrees(math.atan2(rel_position[1], rel_position[0]))
        self.attack_ranged(angle)
        distance = math.sqrt(rel_position[0] ** 2 + rel_position[1] ** 2)
        # if the enemies health is low, pursue them aggressively
        if self.get_agents_health()[0] <= 30:
            Agent3.angle = angle
        elif distance < 200 and self.get_health() <= 30:
            # avoid getting too close when health is low
            Agent3.angle -= 180
            Agent3.angle %= 360

    def on_damage_taken(self):
        if self.get_shield_cooldown_time() > 10:
            # if the shield still has a long cooldown time, change direction
            Agent3.angle -= 180
            Agent3.angle %= 360
        # activate shield when hit
        self.activate_shield()