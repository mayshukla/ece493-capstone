import math
class Agent1(Agent):
    """Enter your code here ..."""
    angle = 0
    movement = 50
    def run(self):
        self.set_movement_speed(Agent1.movement)
        self.set_movement_direction(Agent1.angle)
    def on_obstacle_hit(self):
        Agent1.angle += 90
    def on_enemy_scanned(self, enemy_position):
        # shoot towards enemy when they are near
        distance = (enemy_position.x - self.get_position().x, enemy_position.y - self.get_position().y)
        angle = math.atan2(distance[1], distance[0])
        self.attack_ranged(angle)
        # pursue the enemy!
        Agent1.angle = angle
    def on_damage_taken(self):
        # activate shield and change direction when hit
        self.activate_shield()
        Agent1.angle -= 45