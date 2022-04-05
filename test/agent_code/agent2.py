import math

class Agent2(Agent):
    angle = 20
    speed = 250

    def run(self):
        self.set_movement_speed(Agent2.speed)
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