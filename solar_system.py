# solarsystem.py

import itertools
import math
import numpy as np
import matplotlib.pyplot as plt
import shapely

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
        self.mass = mass
        self.position = position
        self.velocity = velocity
        self.display_size = max(
            math.log(self.mass, self.display_log_base),
            self.min_display_size,
        )
        solar_system.add_body(self)
        self.history = [(position)]


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
        self.color = "y"



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


# Solar System
class SolarSystem:
    def __init__(self, width, height, loss):
        self.loss_type = loss
        self.configuration = None
        self.second_planet_radius = None
        self.bodies = []

        self.loss = 0

    def add_body(self, body):
        self.bodies.append(body)

    def remove_body(self, body):
        self.bodies.remove(body)

    def update_all(self):
        for body in self.bodies:
            body.move()

        if self.loss_type == "center_distance":
            self.biggest_distance_loss()
        elif self.loss_type == "2_body_distance":
            self.two_body_distance_loss()
        elif self.loss_type == "area":
            self.biggest_area_loss()
        else:
            print('No loss')

        #self.solar_system.update()

    @staticmethod
    def accelerate_due_to_gravity(
            first: SolarSystemBody,
            second: SolarSystemBody,
    ):
        if first.distance(second) != 0:
            force = first.mass * second.mass / first.distance(second) ** 2
        else:
            force = first.mass * second.mass / 0.000000001
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
        if first.distance(second) == 0 or second.distance(first) == 0:
            for body in first, second:
                if isinstance(body, Planet):
                    print('colision')
                    self.remove_body(body)
                    self.loss = (1/math.log(len(body.history))) * 10000000
        if first.distance(second) < first.display_size/2 + second.display_size/2:
            for body in first, second:
                if isinstance(body, Planet):
                    print('colision')
                    self.remove_body(body)
                    self.loss = (1/math.log(len(body.history))) * 10000000

    def calculate_all_body_interactions(self):
        #self.biggest_area_loss_for_polygon()


        bodies_copy = self.bodies.copy()
        for idx, first in enumerate(bodies_copy):
            for second in bodies_copy[idx + 1:]:
                self.accelerate_due_to_gravity(first, second)
                self.check_collision(first, second)

    def biggest_distance_loss(self):
        sum = 0
        for body in self.bodies:
            body_initial_radius = math.sqrt(body.history[0][0] ** 2 + body.history[0][1] ** 2)
            body_present_radius = math.sqrt(body.position[0]**2 + body.position[1]**2)
            loss_radius = math.log(abs(body_initial_radius - body_present_radius))
            sum += loss_radius

        if sum > self.loss:
            self.loss = sum


    def biggest_area_loss(self):
        x = []
        y = []

        for body in self.bodies:
            x.append(body.history[0][0])
            y.append(body.history[0][1])

        body_initial_area = shapely.Polygon(zip(x, y)).area

        x = []
        y = []

        for body in self.bodies:
            x.append(body.position[0])
            y.append(body.position[1])

        body_current_area = shapely.Polygon(zip(x,y)).area

        if abs(body_current_area-body_initial_area) > self.loss:
            self.loss = math.log(abs(body_current_area-body_initial_area))


    def two_body_distance_loss(self):
        f = self.bodies[0]
        s = self.bodies[1]

        distance = f.distance(s)


        if distance > self.loss:
            self.loss = distance



    def plot_trajectories_at_times(self, prefix=""):
        fig, ((ax1, ax2, ax3), (ax4, ax5, ax6)) = plt.subplots(2, 3)
        fig.suptitle("Three Suns - System Evolution over iterations")
        for ax, until_time in zip( (ax1, ax2, ax3, ax4, ax5, ax6),[100, 200, 500, 1000, 1200, 1500]):
            for body in self.bodies:
                hist = np.array(body.history[:until_time]).T
                ax.set_title('T = ' + str(until_time))
                ax.plot(hist[0], hist[1])
                ax.scatter(hist[0][0], hist[1][0], s=100)
            ax.plot()

        fig.tight_layout(pad=2)
        fig.show()
        self.name = prefix+str(len(self.bodies)) +"_body_" + str(self.configuration)
        fig.savefig("plots/" +self.name + ".jpg",  dpi=1500)
        #fig.savefig("4_body_[1.01263153e+03,3.03957629e-01,-1.62577369e+00].png",  dpi=1500)



    def plot_trajectories_over_iterations(self):
        for body in self.bodies:
            hist = np.array(body.history).T
            plt.plot(hist[0], hist[1])
            plt.scatter(hist[0][0], hist[1][0], s=100)
        plt.show()

    def plot_trajectories_time(self, until_time):
        for body in self.bodies:
            hist = np.array(body.history[:until_time]).T
            plt.plot(hist[0], hist[1])
            plt.scatter(hist[0][0], hist[1][0], s=10)
        plt.show()

