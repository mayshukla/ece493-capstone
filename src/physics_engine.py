



from numpy import square
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
        # Create space for bodies
        self.space = pymunk.Space()
        # Gravity will not be present by default
        self.space.gravity = 0, 0

        # Create collision handlers
        # Bodies can be given "collision types" and the collisions between the different types can be handled differently
        self.collision_handler = self.space.add_collision_handler(COLLISION_TYPE_1, COLLISION_TYPE_1)
        self.collision_handler.begin = self.begin_collision_handler
        
        # Other collision handler functions that are called at different stages of the collision
        # collision_handler.post_solve =
        # collision_handler.pre_solve = 
        # collision_handler.separate = 

        # Object state classes that will be continuously updated
        self.object_states = []

        # Dictionary mapping object ids to their pymunk bodies
        self.bodies = {}

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
            # TODO: Pass the collided objects to the callback
            data["callback"]()
        return True

    def addOnCollisionCallback(self, callback):
        """
        Adds a callback function that will be called in "begin_collision_handler".
        """
        self.collision_handler.data["callback"] = callback

    def run_render_test(self):
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

    def create_circle(self, center, radius):
        """
        Adds a body with a circle shape to the space.
        Args:
            center: A touple containg the coordinates for the center of the circle (x, y)
            radius: The radius of the circle.
        """
        body = pymunk.Body(mass=0, moment=0, body_type=pymunk.Body.KINEMATIC)
        body.position = center[0], center[1]
        circle = pymunk.Circle(body, radius=radius)
        circle.elasticity = 0
        circle.collision_type = COLLISION_TYPE_1
        self.space.add(body, circle)
        return circle

    def add_agent(self, agent_state):
        """
        Adds an agent to the physics space.

        Args:
            agent_state: AgentState object that will be used to determine the initial position and velocity of the agent.
        """
        agent_body = pymunk.Body(mass=0, moment=0, body_type=pymunk.Body.KINEMATIC)
        agent_body.position = (agent_state.position.x, agent_state.position.y)
        agent_body.velocity = (agent_state.velocity.x, agent_state.velocity.y)

        # TODO: Make the shape(s) for the agent match the agent sprite. The shape(s) will be the hitbox for the sprite.
        circle = pymunk.Circle(agent_body, radius=30)
        circle.elasticity = 0
        circle.collision_type = COLLISION_TYPE_1
        self.space.add(agent_body, circle)

        if agent_state.id in self.bodies:
            raise ValueError(f"Duplicate id {agent_state.id} found")
        self.bodies[agent_state.id] = agent_body
        self.object_states.append(agent_state)

    def add_obstacle(self, obstacle):
        """
        Adds an obstacle to the physics space.

        Args:
            obstacle: an Obstacle object that will be used to determine the position and shape of the obstacle
        """
        obstacle_body = pymunk.Body(mass=0, moment=0, body_type=pymunk.Body.STATIC)
        obstacle_body.position = (obstacle.position.x, obstacle.position.y)
        self.space.add(obstacle_body)

        # TODO: make the obstacle shapes match the obstacle sprites
        lower_left_point = (obstacle.position.x - obstacle.width/2, obstacle.position.y - obstacle.height/2)
        upper_left_point = (obstacle.position.x - obstacle.width/2, obstacle.position.y + obstacle.height/2)
        upper_right_point = (obstacle.position.x + obstacle.width/2, obstacle.position.y + obstacle.height/2)
        lower_right_point = (obstacle.position.x + obstacle.width/2, obstacle.position.y - obstacle.height/2)
        start_points = [lower_left_point, upper_left_point, upper_right_point, lower_right_point]
        end_points = [upper_left_point, upper_right_point, lower_right_point, lower_left_point]
        
        for i in range(4):
            segment = pymunk.Segment(obstacle_body, start_points[i], end_points[i], 5)
            segment.collision_type = COLLISION_TYPE_1
            self.space.add(segment)

    def add_projectile(self, projectile_state):
        """
        Adds a projectile to the physics space.

        Args:
            projectile_state: a ProjectileState object that will be used to determine the initial position and velocity
        """
        projectile_body = pymunk.Body(mass=0, moment=0, body_type=pymunk.Body.KINEMATIC)
        projectile_body.position = (projectile_state.position.x, projectile_state.position.y)
        projectile_body.velocity = (projectile_state.velocity.x, projectile_state.velocity.y)

        # TODO: Make the shape(s) for the projectile match the projectile sprite. The shape(s) will be the hitbox for the sprite.
        circle = pymunk.Circle(projectile_body, radius=5)
        circle.elasticity = 0
        circle.collision_type = COLLISION_TYPE_1
        self.space.add(projectile_body, circle)

        if projectile_state.id in self.bodies:
            raise ValueError(f"Duplicate id {projectile_state.id} found")
        self.bodies[projectile_state.id] = projectile_body
        self.object_states.append(projectile_state)

    def remove_object(self, object_id):
        """
        Removes the object from the physics space.

        Args:
            object_id: the id of the object to be removed

        returns:
            True: if the object was removed.
            False: if an object with the provided id was not found.
        """
        if object_id not in self.bodies:
            return False
        body = self.bodies.pop(object_id)

        # remove all shapes attached to the body
        for shape in body.shapes:
            self.space.remove(shape)

        # remove the body itself
        self.space.remove(body)

        return True

    def step(self, time_increment):
        """
        Advances the physics space forward by the provided time increment. Object positions will be updated based on their current velocities.
        Updates all dynamic object states. Collision callbacks may be called during the step.

        Args:
            time_increment: the amount of time to advance all objects in the physics space
        """
        self.space.step(time_increment)

        for object_state in self.object_states:
            if object_state.id not in self.bodies:
                self.object_states.remove(object_state)
                continue
            object_body = self.bodies[object_state.id]
            object_state.position.x = object_body.position[0]
            object_state.position.y = object_body.position[1]
            object_state.velocity.x = object_body.velocity[0]
            object_state.velocity.y = object_body.velocity[1]

if __name__ == '__main__':
    pe = PhysicsEngine()

    from agent_state import *
    from vector2 import *
    from obstacle import *

    agent_state = AgentState(1, Vector2(100, 200), Vector2(0, 100), 10)
    obstacle = Obstacle(2, Vector2(100, 300), 10, 10)
    pe.add_agent(agent_state)
    pe.add_obstacle(obstacle)
    #assert(self.callback.called)
    #assert(len(self.pe.space.bodies) == 2)

    # 3 types of bodies
    # static -> efficient for bodies that don't move, like walls
    # dynamic/default -> mass, inertia, force, elasticity used for movement
    # kinematic -> our code always sets the velocity
    #body = pymunk.Body(mass=0, moment=0, body_type=pymunk.Body.STATIC)
    #body.position = 300, 200


    # can use force too...
    #body.apply_impulse_at_local_point((100, 0))

    #circle = pymunk.Circle(body, radius=30)
    #circle.elasticity = 0
    #circle.collision_type = 1

    #circle1 = pe.create_circle((100, 200), 30)
    #circle1.body.velocity = (5, 0)
    #circle2 = pe.create_circle((300, 200), 30)

    #pe.space.add(body, circle)

    def callback():
        print("callback!")

    pe.addOnCollisionCallback(callback)
    pe.run_render_test()

    # categories can be used to ignore some collisions, like an agent and their own bullet
    '''circle2.filter = pymunk.ShapeFilter(categories=0b1)

    # can query area around a point for shapes
    # useful for implementing scan functions 
    query = pe.space.point_query(point=body.position, max_distance=500, shape_filter=pymunk.ShapeFilter())
    print(query)

    query = pe.space.point_query(point=body.position, max_distance=500, shape_filter=pymunk.ShapeFilter(mask=pymunk.ShapeFilter.ALL_MASKS() ^ 0b1))
    print(query)'''