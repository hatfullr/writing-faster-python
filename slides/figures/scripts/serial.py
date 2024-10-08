import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import os
import maputil
import matplotlib.animation

plt.style.use(os.path.realpath('resources/noaxes.mplstyle'))

background = 'resources/streets.jpg'

debug = False

fps = 30
duration = 10

frames = int(duration * fps)
dt = float(duration) / frames

def update(frame, traveller, traveller_position, traveller_direction, traveller_vision):
    traveller.update(dt)
    traveller_position.set_offsets(traveller.position)

    if debug:
        try:
            r = 100
            p = traveller.position + traveller.direction * r
            traveller_direction.set_xdata([traveller.position[0], p[0]])
            traveller_direction.set_ydata([traveller.position[1], p[1]])

            bounds = [bound for bound in traveller._boundaries if traveller.is_boundary_valid_direction(bound)]

            positions = []
            for x,y in bounds:
                positions += [[x,y], traveller.position, [np.nan, np.nan]]
            positions = np.asarray(positions)
            traveller_vision.set_xdata(positions[:,0])
            traveller_vision.set_ydata(positions[:,1])
        except: pass
    
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


    traveller = maputil.Traveller(
        map,
        [398, 590],
        maputil.Map.UP,
        size = 10,
        hold_direction_duration = 0.5,
        direction_lerp = 0.5,
        vision_cone = 90,
        speed = 100,
    )
    
    traveller_position = ax.scatter(
        *traveller.position,
        color = 'k',
        s = 10,
        lw = 0,
    )

    if debug:
        traveller_direction = ax.plot([np.nan], [np.nan], color = 'r')[0]
        traveller_vision = ax.plot([np.nan], [np.nan], color = 'cyan')[0]
    
    anim = matplotlib.animation.FuncAnimation(
        fig = fig,
        func = update,
        fargs = (traveller,traveller_position, traveller_direction, traveller_vision,),
        frames = frames,
    )

    anim.save('serial.gif', fps= fps)
    
    plt.show()
