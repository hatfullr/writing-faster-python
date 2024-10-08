import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import os
import maputil
import matplotlib.animation
import serial

plt.style.use(os.path.realpath('resources/noaxes.mplstyle'))

background = serial.background

fps = serial.fps
duration = serial.duration

frames = int(duration * fps)
dt = float(duration) / frames

start_positions = np.asarray([
    [398, 590],
    [376, 30],
    [158, 602],
    [600, 40],
    [600, 260],
    [10, 520],
])
start_directions = np.asarray([
    maputil.Map.UP,
    maputil.Map.LEFT_DOWN,
    maputil.Map.RIGHT_DOWN,
    maputil.Map.LEFT_DOWN,
    maputil.Map.LEFT,
    maputil.Map.RIGHT_UP,
])

def update(frame, travellers, traveller_positions):
    for traveller, traveller_position in zip(travellers, traveller_positions):
        traveller.update(dt)
        traveller_position.set_offsets(traveller.position)
    
if __name__ == '__main__':
    traveller_direction = None
    traveller_vision = None
    
    map = maputil.Map(
        background,
        road_color = [255, 255, 164],
    )

    fig, ax = plt.subplots(
        figsize = np.asarray(map.image.shape[:2]) / matplotlib.rcParams['figure.dpi'],
    )
    
    ax.imshow(map.image)

    travellers = []
    traveller_positions = []
    for position, direction in zip(start_positions, start_directions):
        travellers += [maputil.Traveller(
            map,
            position,
            direction,
            size = 10,
            hold_direction_duration = 0.5,
            direction_lerp = 0.5,
            vision_cone = 90,
            speed = 100,
        )]
        
        traveller_positions += [ax.scatter(
            *position,
            color = 'k',
            s = 10,
            lw = 0,
        )]
    
    anim = matplotlib.animation.FuncAnimation(
        fig = fig,
        func = update,
        fargs = (travellers,traveller_positions),
        frames = frames,
    )

    anim.save('parallel.gif', fps= fps)
    
    plt.show()
