import pymunk
import pymunk.pygame_util
import pygame
import pymunk.vec2d

COLLISION_TYPE_1 = 1

class PhysicsEngine:
    """
    A wrapper around the pymunk physics engine. Tracks the positions and velocities of objects over time. Handles collisions between objects.
    """
    def __init__(self) -> None:
        # create space for bodies
        self.space = pymunk.Space() # can be threaded
        self.space.gravity = 0, 0 # gravity will not be present by default

        # create collision handlers
        # bodies can be given "collision types" and the collision between the different types can be handled differently
        # can use this to handle agent and wall collision separately
        self.collision_handler = self.space.add_collision_handler(COLLISION_TYPE_1, COLLISION_TYPE_1)
        self.collision_handler.begin = self.begin_collision_handler
        
        # collision_handler.post_solve =
        # collision_handler.pre_solve = 
        # collision_handler.separate = 

    def begin_collision_handler(self, arbiter, space, data):
        """
        Called when two objects collide for the first time. 

        Args:
            arbiter: Contains information about the objects that collided.
            space: Contains information about all objects currently instantiated. This is the same as self.space.
            data: A dict that contains any additional parameters.
        Returns:
            True if the collision should be processed normally.
            False if the collision should be ignored.
        """
        # stop the objects from moving
        arbiter.shapes[0].body.velocity = (0, 0)
        arbiter.shapes[1].body.velocity = (0, 0)
        print("Collision!")
        # call the optional callback function
        if "callback" in data:
            data["callback"]()
        return True

    def addOnCollisionCallback(self, callback):
        """
        Adds a callback function that will be called in "begin_collision_handler".
        """
        self.collision_handler.data["callback"] = callback

    def run_test(self):
        """
        Renders the current space using pygame. This is for debug purposes only.
        """
        # use pygame for testing
        GRAY = (220, 220, 220)
        pygame.init()
        size = 640, 240
        screen = pygame.display.set_mode(size)
        draw_options = pymunk.pygame_util.DrawOptions(screen)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            screen.fill(GRAY)
            self.space.debug_draw(draw_options)
            pygame.display.update()

            # step forward in time
            self.space.step(0.01)

        pygame.quit()

    def get_shapes(self):
        """
        Returns information about all shapes in the current space.
        """
        return self.space.shapes

    def get_bodies(self):
        """
        Returns information about all bodies in the current space (one body can be associated with many shapes).
        """
        return self.space.bodies


if __name__ == '__main__':
    pe = PhysicsEngine()

    # 3 types of bodies
    # static -> efficient for bodies that don't move, like walls
    # dynamic/default -> mass, inertia, force, elasticity used for movement
    # kinematic -> our code always sets the velocity
    body = pymunk.Body(mass=1, moment=10, body_type=pymunk.Body.KINEMATIC)
    body.position = 100, 200

    # velocity is an x, y vector
    body.velocity = (5, 0)

    # can use force too...
    # body.apply_impulse_at_local_point((100, 0))

    circle = pymunk.Circle(body, radius=30)
    circle.elasticity = 0
    circle.collision_type = 1

    body2 = pymunk.Body(mass=1, moment=10, body_type=pymunk.Body.KINEMATIC)
    body2.position = 300, 200
    body2.velocty = 0,0

    circle2 = pymunk.Circle(body2, radius=30)
    circle2.elasticity = 0
    circle2.collision_type = 1

    pe.space.add(body, circle, body2, circle2)

    def callback():
        print("callback!")

    pe.addOnCollisionCallback(callback)
    pe.run_test()

    # categories can be used to ignore some collisions, like an agent and their own bullet
    circle2.filter = pymunk.ShapeFilter(categories=0b1)

    # can query area around a point for shapes
    # useful for implementing scan functions 
    query = pe.space.point_query(point=body.position, max_distance=500, shape_filter=pymunk.ShapeFilter())
    print(query)

    query = pe.space.point_query(point=body.position, max_distance=500, shape_filter=pymunk.ShapeFilter(mask=pymunk.ShapeFilter.ALL_MASKS() ^ 0b1))
    print(query)