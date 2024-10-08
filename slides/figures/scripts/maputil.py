import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors
import copy
import random

# For two given colors, if the vector distance between them exceeds this
# threshold then an edge is detected. We compare edge_threshold to the fraction
# of the color vector distance to the maximum color value in the image.
edge_threshold = 0.3


def get_color_difference(color1, color2):
    color1 = np.asarray(color1)
    color2 = np.asarray(color2)
    return 2*np.abs(color1 - color2) / (np.abs(color1) + np.abs(color2))


class Map(object):
    LEFT = np.array([1, 0])
    RIGHT = np.array([-1, 0])
    UP = np.array([0, -1])
    DOWN = np.array([0, 1])

    RIGHT_UP = np.array([np.sqrt(2), -np.sqrt(2)])
    RIGHT_DOWN = np.array([np.sqrt(2), np.sqrt(2)])
    LEFT_DOWN = np.array([-np.sqrt(2), np.sqrt(2)])
    LEFT_UP = np.array([np.sqrt(2), -np.sqrt(2)])
    
    def __init__(
            self,
            filename : str,
            road_color : list | tuple | np.ndarray = np.asarray([255,255,0]), # yellow
    ):
        self.image = plt.imread(filename).astype(int)
        self.road_color = np.asarray(road_color).astype(int)

    def get_color(self, index):
        return self.image[index[0], index[1]]

    def get_indices_of_color(self, color : list | tuple | np.ndarray):
        indices = []
        for i, row in enumerate(self.image):
            for j, pixel in enumerate(row):
                if (pixel[0] == color[0] and
                    pixel[1] == color[1] and
                    pixel[2] == color[2]):
                    indices += [[i, j]]
        return np.asarray(indices, dtype = int)

    def set_color(self, indices, color):
        indices = np.asarray(indices)
        self.image[indices[:,0], indices[:,1]] = color

    def get_max_color(self):
        return np.amax(self.image, axis = 0)[0]
    
    def is_position_oob(self, position : list | tuple | np.ndarray):
        position = np.asarray(position)[::-1]
        return (
            (position[0] < 0 or position[0] > self.image.shape[0]) or
            (position[1] < 0 or position[1] > self.image.shape[1])
        )

    def clamp_position(self, position : list | tuple | np.ndarray):
        position = np.asarray(position)[::-1]
        return np.asarray([
            min(max(position[0], 0), self.image.shape[0]),
            min(max(position[1], 0), self.image.shape[1]),
        ])[::-1]


class Traveller(object):
    def __init__(
            self,
            map : Map,
            position : list | tuple | np.ndarray,
            direction : list | tuple | np.ndarray,
            vision_cone : float | int = 90,
            hold_direction_duration : float | int = 0,
            direction_lerp : float = 0.5,
            size : float | int = 10,
            speed : float | int = 0.1,
    ):
        self.map = map
        self.position = np.asarray(position).astype(int)
        self.direction = np.asarray(direction).astype(float)
        self.vision_cone = vision_cone
        self.hold_direction_duration = hold_direction_duration
        self.direction_lerp = direction_lerp
        self.size = size
        self._speed = speed
        
        self.speed = copy.deepcopy(self._speed)
        
        self.time_alive = 0
        self._direction_timer = 0
        
        self._boundaries = None
        self._boundary_weights = None
        self._boundary_distances = None
        self._boundary_angles = None
        self._boundary_directions = None

        self._previous_dt = None

        self.update_boundaries()
        self.snap_to_road()

    def update(self, dt):
        self.time_alive += dt
        self._direction_timer += dt

        self.direction /= np.sqrt((self.direction**2).sum())
        
        self.position += self.direction * self.speed * dt
        
        self.update_boundaries()
        
        #if self._direction_timer >= self.hold_direction_duration:
        self.change_direction()
        
        self._previous_dt = copy.deepcopy(dt)
    
    def update_boundaries(
            self,
            edge_threshold = edge_threshold,
    ):
        angle = np.arctan2(self.direction[1], self.direction[0])
        thetas = np.linspace(angle - np.pi, angle + np.pi, 101)[:-1]
        directions = np.column_stack((np.cos(thetas), np.sin(thetas)))
        
        self._boundaries = np.full((len(thetas), 2), np.nan) # xy positions
        
        max_steps = int(np.sqrt((np.asarray(self.map.image.shape)**2).sum())) + 1
        max_color = self.map.get_max_color()
        
        for i, direction in enumerate(directions):
            trials = (self.position + direction * np.arange(max_steps)[:,None]).astype(int).tolist()
            for j, trial in enumerate(trials):
                if self.map.is_position_oob(trial):
                    trials = trials[:j - 1]
                    break
            else: continue
            trials = np.asarray(trials)

            for j, trial in enumerate(trials):
                try:
                    color = self.map.image[trial[1], trial[0]]
                except: continue
                if (get_color_difference(self.map.road_color, color) > edge_threshold).any():
                    self._boundaries[i] = trials[j - 1]
                    break
            else: self._boundaries[i] = trials[-1]

        offset = self._boundaries - self.position # destination - position
        self._boundary_distances = np.sqrt(np.sum(offset**2, axis = -1))
        self._boundary_directions = offset / self._boundary_distances[:,None]
        self._boundary_weights = self._boundary_distances / np.nanmax(self._boundary_distances)
        self._boundary_angles = (angle + thetas) * 180 / np.pi

        # Make sure our speed is never so high that we can hit a boundary
        if self._previous_dt is not None:
            speeds = self._boundary_distances / self._previous_dt
            weights = copy.deepcopy(self._boundary_distances)
            weights /= np.amax(weights)
            #weights = np.exp(weights)
            speed = np.sum(speeds * self._boundary_weights) / np.sum(self._boundary_weights)
            #print(self._speed, speed)
            #speed = np.mean(self._boundary_distances) / self._previous_dt
            #self.speed = min(self._speed, speed)
    
    def snap_to_road(self):
        weights = 1 - self._boundary_weights
        self.position = (self._boundaries * weights[:,None]).sum(axis = 0) / weights.sum()

    def is_direction_valid(self, direction):
        cosdtheta = np.dot(direction, self.direction)
        dtheta = np.arccos(cosdtheta) * 180 / np.pi
        return dtheta <= 0.5 * self.vision_cone
    
    def is_boundary_valid_direction(self, boundary):
        offset = boundary - self.position
        distance = np.sqrt((offset**2).sum())

        if distance <= self.size: return False
        
        direction = offset / distance
        return self.is_direction_valid(direction)
    
    def get_valid_directions(self):
        r""" Find the valid directions that the Traveller can go from its 
        current position down a road. """
        for i, boundary in enumerate(self._boundaries):
            if not self.is_boundary_valid_direction(boundary): continue
            yield self._boundary_directions[i], i
    
    def change_direction(self):
        self._direction_timer = 0

        directions = []
        distances = []
        for direction, i in self.get_valid_directions():
            directions += [copy.deepcopy(direction)]
            distances += [copy.deepcopy(self._boundary_distances[i])]
        
        if len(directions) == 0:
            # Turn around
            self.direction = -copy.deepcopy(self.direction)
            return

        distances = np.asarray(distances)
        directions = np.asarray(directions)
        
        weights1 = distances / np.amax(distances)
        weights2 = np.asarray([0.5 * (1 + np.dot(self.direction, direction)) for direction in directions])
        
        weights = weights1 * weights2
        
        self.direction = (directions * weights[:,None]).sum(axis = 0)
        #self.direction /= np.sqrt((self.direction**2).sum())
        
