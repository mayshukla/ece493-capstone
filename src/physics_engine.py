"""
The PhysicsEngine class is part of the implementation of the following requirements:

FR8 - Agent.RangedAttack
FR10 - Agent.PositionState
FR11 - Agent.Movement
FR12 - Movement.Direction
FR13 - Movement.Speed
FR14 - Map.Walls
"""

import pymunk
import pymunk.pygame_util
import pygame
import pymunk.vec2d
from src.globals import *
from src.agent_state import AgentState
from src.obstacle import Obstacle
from src.projectile_state import ProjectileState
from src.vector2 import Vector2

class PhysicsEngine:
    """
    A wrapper around the pymunk physics engine. Tracks the positions and velocities of objects over time. Handles collisions between objects.
    """
    COLLISION_TYPE_1 = 1
    SPACE_WIDTH = 1074
    SPACE_HEIGHT = 700

    def __init__(self) -> None:
        # Create space for bodies
        self.space = pymunk.Space()
        # Gravity will not be present by default
        self.space.gravity = 0, 0

        # Create collision handlers
        # Bodies can be given "collision types" and the collisions between the different types can be handled differently
        self.collision_handler = self.space.add_collision_handler(PhysicsEngine.COLLISION_TYPE_1, PhysicsEngine.COLLISION_TYPE_1)
        self.collision_handler.begin = self.begin_collision_handler
        self.collision_handler.separate = self.separate_collision_handler

        # Object state classes that will be continuously updated
        self.object_states = []

        # Dictionary mapping object ids to their pymunk bodies
        self.bodies = {}

        # add game boundaries to the physics space
        self.set_boundaries()

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
        object_id_1 = self._get_body_id(arbiter.shapes[0].body)
        object_id_2 = self._get_body_id(arbiter.shapes[1].body)

        if object_id_1 is None or object_id_2 is None:
            return False

        object_state_1 = self._get_object_state_from_id(object_id_1)
        object_state_2 = self._get_object_state_from_id(object_id_2)
        
        if object_state_1 is None or object_state_2 is None:
            return False

        if (not (isinstance(object_state_1, ProjectileState) and isinstance(object_state_2, AgentState))) \
            and (not (isinstance(object_state_1, AgentState) and isinstance(object_state_2, ProjectileState))):
            # stop the objects from moving
            arbiter.shapes[0].body.velocity = (0, 0)
            arbiter.shapes[1].body.velocity = (0, 0)
        print(f"Collision between object ids: {object_id_1} and {object_id_2}")
        print(f"Collision between object states: {object_state_1} and {object_state_2}")
        # call the optional callback function
        if "collision_callback" in data:
            data["collision_callback"](object_state_1, object_state_2, arbiter.contact_point_set.points[0].point_a)
        return True

    def separate_collision_handler(self, arbiter, space, data):
        """
        Called once when two objects that collided have now separated.

        Args:
            arbiter: Contains information about the objects that collided.
            space: Contains information about all objects currently instantiated. This is the same as self.space.
            data: A dict that contains any additional parameters.
        Returns:
            True if the collision should be processed normally.
            False if the collision should be ignored.
        """
        object_id_1 = self._get_body_id(arbiter.shapes[0].body)
        object_id_2 = self._get_body_id(arbiter.shapes[1].body)
        object_state_1 = self._get_object_state_from_id(object_id_1)
        object_state_2 = self._get_object_state_from_id(object_id_2)
        if "separate_callback" in data:
            data["separate_callback"](object_state_1, object_state_2)
        return True

    def add_on_collision_callback(self, callback):
        """
        Adds a callback function that will be called in "begin_collision_handler".
        """
        self.collision_handler.data["collision_callback"] = callback

    def add_on_separate_callback(self, callback):
        """
        Adds a callback function that will be called in "separate_collision_handler".
        """
        self.collision_handler.data["separate_callback"] = callback

    def init_renderer(self):
        """Initialize the pygame renderer. This is for debug purposes only"""
        # use pygame for testing
        pygame.init()
        size = PhysicsEngine.SPACE_WIDTH, PhysicsEngine.SPACE_HEIGHT
        self.screen = pygame.display.set_mode(size)
        self.draw_options = pymunk.pygame_util.DrawOptions(self.screen)

    def render_tick(self):
        """Update the pygame render. This should be called in the game loop."""
        GRAY = (220, 220, 220)
        self.screen.fill(GRAY)
        self.space.debug_draw(self.draw_options)
        pygame.display.update()

    def run_render_test(self):
        """
        Renders the current space using pygame. This is for debug purposes only.
        """
        # use pygame for testing
        GRAY = (220, 220, 220)
        pygame.init()
        size = PhysicsEngine.SPACE_WIDTH, PhysicsEngine.SPACE_HEIGHT
        screen = pygame.display.set_mode(size)
        draw_options = pymunk.pygame_util.DrawOptions(screen)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.screen.fill(GRAY)
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
        circle.collision_type = PhysicsEngine.COLLISION_TYPE_1
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

        circle = pymunk.Circle(agent_body, radius=AGENT_RADIUS)
        circle.elasticity = 0
        circle.collision_type = PhysicsEngine.COLLISION_TYPE_1
        circle.filter = pymunk.ShapeFilter(
            group=self._id_to_collision_group(agent_state.id)
        )
        self.space.add(agent_body, circle)

        if agent_state.id in self.bodies:
            raise ValueError(f"Duplicate id {agent_state.id} found")
        self.bodies[agent_state.id] = agent_body
        self.object_states.append(agent_state)
        print(f"added agent {agent_state.id}")

    def add_obstacle(self, obstacle):
        """
        Adds an obstacle to the physics space.

        Args:
            obstacle: an Obstacle object that will be used to determine the position and shape of the obstacle
        """
        obstacle_body = pymunk.Body(mass=0, moment=0, body_type=pymunk.Body.STATIC)
        obstacle_body.position = (obstacle.position.x, obstacle.position.y)

        if obstacle.id in self.bodies:
            raise ValueError(f"Duplicate id {obstacle.id} found")
        self.bodies[obstacle.id] = obstacle_body
        self.object_states.append(obstacle)

        self.space.add(obstacle_body)

        # TODO: make the obstacle shapes match the obstacle sprites
        lower_left_point = (-obstacle.width/2, -obstacle.height/2)
        upper_left_point = (-obstacle.width/2, +obstacle.height/2)
        upper_right_point = (+obstacle.width/2, +obstacle.height/2)
        lower_right_point = (+obstacle.width/2, -obstacle.height/2)
        vectices = [lower_left_point, upper_left_point, upper_right_point, lower_right_point]

        rect = pymunk.Poly(obstacle_body, vectices)
        rect.collision_type = PhysicsEngine.COLLISION_TYPE_1
        self.space.add(rect)

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
        circle.collision_type = PhysicsEngine.COLLISION_TYPE_1
        circle.filter = pymunk.ShapeFilter(
            # Ignore collisions between an agent and its own projectile
            group=self._id_to_collision_group(projectile_state.attackerId),
            categories=0b1,
            # Ignore collisions between any 2 projectiles
            mask=pymunk.ShapeFilter.ALL_MASKS() ^ 0b1
        )

        if projectile_state.id in self.bodies:
            raise ValueError(f"Duplicate id {projectile_state.id} found")
        self.bodies[projectile_state.id] = projectile_body
        self.object_states.append(projectile_state)

        self.space.add(projectile_body, circle)

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
        for object_state in self.object_states:
            if object_state.id not in self.bodies:
                self.object_states.remove(object_state)
                continue
            # Update velocity of objects such as agents that may have been
            # updated by game logic (e.g. a call to Agent.set_movement_speed)
            if not isinstance(object_state, Obstacle):
                object_body = self.bodies[object_state.id]
                object_body.velocity = (object_state.velocity.x, object_state.velocity.y)

        self.space.step(time_increment)

        for object_state in self.object_states:
            if object_state.id not in self.bodies:
                self.object_states.remove(object_state)
                continue
            object_body = self.bodies[object_state.id]
            object_state.position.x = object_body.position[0]
            object_state.position.y = object_body.position[1]
            if not isinstance(object_state, Obstacle):
                object_state.velocity.x = object_body.velocity[0]
                object_state.velocity.y = object_body.velocity[1]

    def _get_body_id(self, body):
        """
        Returns the object_state id that corresponds to the pymunk body. If the body cannot be found returns None.
        """
        for id in self.bodies:
            if self.bodies[id] == body:
                return id
        return None

    def _get_object_state_from_id(self, id):
        """
        Returns the object_state with the corresponding id. Returns None if an object with the passed in id cannot be found.
        """
        return next((object_state for object_state in self.object_states if object_state.id == id), None)

    def _id_to_collision_group(self, _id):
        """Converts an ObjectState id value to a group to use with
        pymunk.ShapeFilter
        """

        # Add one to ensure that group is not zero.
        # Group value of zero does not filter anything:
        #   http://www.pymunk.org/en/latest/pymunk.html#pymunk.ShapeFilter.group
        return _id + 1

    def scan_area(self, position, distance):
        """
        Locates all objects within a specified distance of a given position.

        Arguments:
            position: A Vector2 object specifiying the point around which to search for objects.
            distance: A float specifiying the maximum distance away from the point to search for objects.

        Returns: a list containing the object_state for each object that was located. If no objects were located the list will be empty.
        """
        query = self.space.point_query([position.x, position.y], distance, pymunk.ShapeFilter())
        hits = []
        for hit in query:
            id = self._get_body_id(hit.shape.body)
            object = self._get_object_state_from_id(id)
            hits.append(object)
        return hits

    def set_boundaries(self):
        """
        Initializes the boundaries of the game as obstacles in the physics space.
        """
        left_boundary_obstacle = Obstacle(-1, Vector2(0, 0), 0, 0)
        left_boundary_body = pymunk.Body(mass=0, moment=0, body_type=pymunk.Body.STATIC)
        self.bodies[-1] = left_boundary_body
        self.object_states.append(left_boundary_obstacle)
        left_boundary_segment = pymunk.Segment(left_boundary_body, (0, 0), (0, PhysicsEngine.SPACE_HEIGHT), 40)
        left_boundary_segment.collision_type = PhysicsEngine.COLLISION_TYPE_1
        self.space.add(left_boundary_body, left_boundary_segment)

        right_boundary_obstacle = Obstacle(-2, Vector2(0, 0), 0, 0)
        right_boundary_body = pymunk.Body(mass=0, moment=0, body_type=pymunk.Body.STATIC)
        self.bodies[-2] = right_boundary_body
        self.object_states.append(right_boundary_obstacle)
        right_boundary_segment = pymunk.Segment(right_boundary_body, (PhysicsEngine.SPACE_WIDTH, 0), (PhysicsEngine.SPACE_WIDTH, PhysicsEngine.SPACE_HEIGHT), 100)
        right_boundary_segment.collision_type = PhysicsEngine.COLLISION_TYPE_1
        self.space.add(right_boundary_body, right_boundary_segment)

        upper_boundary_obstacle = Obstacle(-3, Vector2(0, 0), 0, 0)
        upper_boundary_body = pymunk.Body(mass=0, moment=0, body_type=pymunk.Body.STATIC)
        self.bodies[-3] = upper_boundary_body
        self.object_states.append(upper_boundary_obstacle)
        upper_boundary_segment = pymunk.Segment(upper_boundary_body, (0, PhysicsEngine.SPACE_HEIGHT), (PhysicsEngine.SPACE_WIDTH, PhysicsEngine.SPACE_HEIGHT), 20)
        upper_boundary_segment.collision_type = PhysicsEngine.COLLISION_TYPE_1
        self.space.add(upper_boundary_body, upper_boundary_segment)

        lower_boundary_obstacle = Obstacle(-4, Vector2(0, 0), 0, 0)
        lower_boundary_body = pymunk.Body(mass=0, moment=0, body_type=pymunk.Body.STATIC)
        self.bodies[-4] = lower_boundary_body
        self.object_states.append(lower_boundary_obstacle)
        lower_boundary_segment = pymunk.Segment(lower_boundary_body, (0, 0), (PhysicsEngine.SPACE_WIDTH, 0), 40)
        lower_boundary_segment.collision_type = PhysicsEngine.COLLISION_TYPE_1
        self.space.add(lower_boundary_body, lower_boundary_segment)


if __name__ == '__main__':
    pe = PhysicsEngine()

    from vector2 import *
    from object_state import *
    from agent_state import AgentState
    #from obstacle import Obstacle

    agent_state = AgentState(1, Vector2(80, 500), Vector2(50, 0), 30)
    #obstacle = Obstacle(2, Vector2(100, 70), 30, 30)
    pe.add_agent(agent_state)
    #pe.add_obstacle(obstacle)
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

    def callback(x, y):
        print("callback!")

    pe.add_on_collision_callback(callback)
    pe.run_render_test()

    # categories can be used to ignore some collisions, like an agent and their own bullet
    '''circle2.filter = pymunk.ShapeFilter(categories=0b1)

    # can query area around a point for shapes
    # useful for implementing scan functions
    query = pe.space.point_query(point=body.position, max_distance=500, shape_filter=pymunk.ShapeFilter())
    print(query)

    query = pe.space.point_query(point=body.position, max_distance=500, shape_filter=pymunk.ShapeFilter(mask=pymunk.ShapeFilter.ALL_MASKS() ^ 0b1))
    print(query)'''
