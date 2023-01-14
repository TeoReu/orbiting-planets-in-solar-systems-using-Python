# solarsystem.py

import itertools
import math
import numpy as np


# Solar System Bodies
class SolarSystemBody():
    min_display_size = 200
    display_log_base = 1.1
    def __init__(
            self,
            solar_system,
            mass,
            position=(0, 0),
            velocity=(0, 0),
    ):
        super().__init__()
        self.history = []
        self.mass = mass
        self.position = position
        self.velocity = velocity
        self.display_size = max(
            math.log(self.mass, self.display_log_base),
            self.min_display_size,
        )
        solar_system.add_body(self)

    def move(self):
        self.history.append([self.position[0], self.position[1]])
        self.position = (self.position[0] + self.velocity[0], self.position[1] + self.velocity[1])

    def distance(self, planet):
        value = math.sqrt((self.position[0] - planet.position[0])**2 + (self.position[1] - planet.position[1])**2)
        #print(value)
        return value

    def towards(self, planet):
        x = planet.position[0]
        y = planet.position[1]
        x = x - self.position[0]
        y = y - self.position[1]
        return round(math.atan2(y,x)*180.0/math.pi, 10) % 360.0


class Sun(SolarSystemBody):
    def __init__(
            self,
            solar_system,
            mass,
            position=(0, 0),
            velocity=(0, 0),
    ):
        super().__init__(solar_system, mass, position, velocity)
        self.color = "yellow"



class Planet(SolarSystemBody):
    colours = itertools.cycle(["red", "green", "blue"])

    def __init__(
            self,
            solar_system,
            mass,
            position=(0, 0),
            velocity=(0, 0),
    ):
        super().__init__(solar_system, mass, position, velocity)
        self.color= next(Planet.colours)
        angle = math.atan2(self.position[1], self.position[0])

        cos = math.cos(angle)
        sin = math.sin(angle)

        self.velocity = (sin * self.velocity, cos * self.velocity)

class Earth(SolarSystemBody):

    def __init__(
            self,
            solar_system,
            mass,
            sun,
            position=(0, 0),

    ):
        super().__init__(solar_system, mass, position, sun)
        self.velocity = (0, math.sqrt(sun.mass / self.distance(sun)))
        self.color = "pink"

# Solar System
class SolarSystem:
    def __init__(self, width, height):
        self.biggest_distance_loss = 0
        self.biggest_angle_loss = 0

        self.accumulated_angle_loss = 0
        self.accumulated_distance_loss = 0

        self.second_planet_radius = None
        #self.solar_system
        self.bodies = []
        self.period = []

        self.rotations = 0
        self.passed = False

    def add_body(self, body):
        self.bodies.append(body)

    def remove_body(self, body):
        #body.clear()
        self.bodies.remove(body)

    def update_all(self):
        for body in self.bodies:
            body.move()

        self.biggest_distance_loss_three_body()
        self.biggest_angle_loss_three_body()
        #self.solar_system.update()

    @staticmethod
    def accelerate_due_to_gravity(
            first: SolarSystemBody,
            second: SolarSystemBody,
    ):
        force = first.mass * second.mass / first.distance(second) ** 2
        angle = first.towards(second)
        reverse = 1
        for body in first, second:
            acceleration = force / body.mass
            acc_x = acceleration * math.cos(math.radians(angle))
            acc_y = acceleration * math.sin(math.radians(angle))
            body.velocity = (
                body.velocity[0] + (reverse * acc_x),
                body.velocity[1] + (reverse * acc_y),
            )
            reverse = -1

    def check_collision(self, first, second):
        if isinstance(first, Planet) and isinstance(second, Planet):
            return
        if first.distance(second) < 1: #first.display_size/2 + second.display_size/2:
            for body in first, second:
                if isinstance(body, Planet):
                    continue
                    #print('colision')
                    #self.remove_body(body)
                    #self.biggest_angle_loss = 50


    def calculate_all_body_interactions(self):
        bodies_copy = self.bodies.copy()
        for idx, first in enumerate(bodies_copy):
            for second in bodies_copy[idx + 1:]:
                self.accelerate_due_to_gravity(first, second)
                self.check_collision(first, second)

    def biggest_distance_loss_three_body(self):
        #print(self.bodies)
        for body in self.bodies:
            body_initial_radius = math.sqrt(body.history[0][0] ** 2 + body.history[0][1] ** 2)
            body_present_radius = math.sqrt(body.position[0]**2 + body.position[1]**2)
            loss_radius = math.log(abs(body_initial_radius - body_present_radius)+3)

            self.accumulated_distance_loss += loss_radius
            if loss_radius > self.biggest_distance_loss:
                self.biggest_distance_loss = loss_radius

    def biggest_angle_loss_three_body(self):
        if len(self.bodies) != 3:
            print("To use angle loss, there needs to only be 3 planets")
            return 0
        else:
            # Works only if sun is added first, earth second, then "satellite"
            earth = self.bodies[1]
            satelitte = self.bodies[2]

            initial_unit_vector_earth = earth.history[0] / np.linalg.norm(earth.history[0])
            initial_unit_vector_satelitte = satelitte.history[0] / np.linalg.norm(satelitte.history[0])
            dot_product = np.dot(initial_unit_vector_earth, initial_unit_vector_satelitte)
            initial_angle = np.arccos(dot_product)

            current_unit_vector_earth = earth.position / np.linalg.norm(earth.position)
            current_unit_vector_satelitte = satelitte.position / np.linalg.norm(satelitte.position)
            dot_product_2 = np.dot(current_unit_vector_earth, current_unit_vector_satelitte)
            current_angle = np.arccos(dot_product_2)

            angle_diff = abs(initial_angle - current_angle)

            if angle_diff > self.biggest_angle_loss:
                self.biggest_angle_loss = angle_diff

            # initial_unit_vector_earth2 = [x*-1 for x in earth.history[0]] / np.linalg.norm([x*-1 for x in earth.history[0]])
            # initial_unit_vector_satelitte2 = [x-y for x,y in zip(satelitte.history[0],earth.history[0])] / np.linalg.norm([x-y for x,y in zip(satelitte.history[0],earth.history[0])])
            # dot_product2 = np.dot(initial_unit_vector_earth2, initial_unit_vector_satelitte2)
            # initial_angle2 = np.arccos(dot_product2)
            #
            # current_unit_vector_earth2 = [x*-1 for x in earth.position] / np.linalg.norm([x*-1 for x in earth.position])
            # current_unit_vector_satelitte2 = [x-y for x,y in zip(satelitte.position,earth.position)] / np.linalg.norm([x-y for x,y in zip(satelitte.position,earth.position)])
            # dot_product_2 = np.dot(current_unit_vector_earth2, current_unit_vector_satelitte2)
            # current_angle2 = np.arccos(dot_product_2)
            #
            # angle_diff2 = abs(initial_angle2 - current_angle2)


            # if angle_diff > 3.10 and not self.passed:
            #     self.rotations += 1
            #     self.passed = True
            #
            # if  3.14/2 < angle_diff < 3.14/2 + 0.1 and satelitte.position[1] < 0:
            #     self.passed = False
            #
            # if self.rotations > 0:
            #     #print("hello")
            #     if satelitte.position[1] < 0:
            #         self.accumulated_angle_loss += math.pi*self.rotations + math.pi-angle_diff
            #     else:
            #         self.accumulated_angle_loss += math.pi * self.rotations + math.pi + angle_diff
            #
            # else:
            #     self.accumulated_angle_loss += angle_diff
            #
            #
            # if self.rotations > 0:
            #     #print("hello")
            #     if satelitte.position[1] < 0:
            #         diff = math.pi*self.rotations + math.pi-angle_diff
            #     else:
            #         diff = math.pi * self.rotations + math.pi + angle_diff
            #
            # else:
            #     diff = angle_diff
            #
            # if diff > self.biggest_angle_loss:
            #     self.biggest_angle_loss = diff





            # if angle_diff2 > 3.10 and not self.passed:
            #     self.rotations += 1
            #     self.passed = True
            #
            # if  3.14/2 < angle_diff2 < 3.14/2 + 0.1 and satelitte.position[1] < 0:
            #     self.passed = False
            #
            # if self.rotations > 0:
            #     #print("hello")
            #     if satelitte.position[1] < 0:
            #         self.accumulated_angle_loss += math.pi*self.rotations + math.pi-angle_diff
            #     else:
            #         self.accumulated_angle_loss += math.pi * self.rotations + math.pi + angle_diff
            #
            # else:
            #     self.accumulated_angle_loss += angle_diff
            #
            #
            # if self.rotations > 0:
            #     #print("hello")
            #     if satelitte.position[1] < 0:
            #         diff = math.pi*self.rotations + math.pi-angle_diff
            #     else:
            #         diff = math.pi * self.rotations + math.pi + angle_diff
            #
            # else:
            #     diff = angle_diff
            #
            # if diff > self.biggest_angle_loss:
            #     self.biggest_angle_loss = diff




            # combined_diff = angle_diff2 + angle_diff
            #
            # if angle_diff2 > self.biggest_angle_loss:
            #     self.biggest_angle_loss = angle_diff2




    def get_biggest_distance_loss(self, iterations):
        for i in range(iterations):
            self.calculate_all_body_interactions()
            self.update_all()

        return np.float(self.biggest_distance_loss)

    def accumulated_distance_and_angle_loss_three_body(self, iterations):
        for i in range(iterations):
            self.calculate_all_body_interactions()
            self.update_all()

        return math.log2(np.float(self.accumulated_distance_loss)) + math.log2(np.float(self.accumulated_angle_loss))#*4

    def distance_and_angle_loss_three_body(self, iterations):
        for i in range(iterations):
            self.calculate_all_body_interactions()
            self.update_all()

        print(np.float(self.biggest_angle_loss))
        #return np.float(self.biggest_angle_loss)
        return np.float(self.biggest_distance_loss) + np.float(self.biggest_angle_loss)*4

    def period_distance(self,x,y):
        min = math.inf
        for x1,y1 in self.period:
            distance = math.sqrt((x1 - x)**2 + (y1 - y)**2)
            if distance < min:
                min = distance
        return min

    # Does not account for period rotation which seems to be crucial, as this gives poor results
    def period_loss(self):
        period_finished = False
        half = False
        satelitte = self.bodies[2]
        accumulated_loss = 0
        for i in range(1000):
            x, y = satelitte.position
            self.calculate_all_body_interactions()
            self.update_all()
            if period_finished:
                accumulated_loss += self.period_distance(x,y)
            else:
                if i == 0:
                    continue
                if y > 0:
                    half = True
                if y < 0 and half:
                    period_finished = True
                self.period.append((x,y))

        print(math.log10(accumulated_loss))
        return math.log10(accumulated_loss)



