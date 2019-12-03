# import matplotlib.pyplot as plt
# import matplotlib.animation as animation
# import time
# import numpy as np
# from matplotlib import style

# graph_data = [1,2,4,3,2,1,3,2,1,3,2,1]
# WINDOW_SIZE = 10 # samples per window. 

# FPS = 20
# refresh_rate = 1/FPS
# style.use('fivethirtyeight')

# fig = plt.figure()
# ax1 = fig.add_subplot(1,1,1)

# def shift_window(samples, new_sample):
#     new_window = samples[1:]
#     new_window.append(new_sample)
#     return new_window


# def animate(i):
#     global graph_data
#     xs=[]
#     ys=[]
#     graph_data = shift_window(graph_data,np.random.randint(1,5))
#     ys = graph_data
#     xs=range(len(graph_data))
#     ax1.clear()
#     ax1.plot(xs,ys)

# ani = animation.FuncAnimation(fig,animate)
# plt.show()


import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation

# First set up the figure, the axis, and the plot element we want to animate
fig = plt.figure()
ax = plt.axes(xlim=(0, 2), ylim=(-2, 2))
line, = ax.plot([], [], lw=2)

# initialization function: plot the background of each frame
def init():
    line.set_data([], [])
    return line,

# animation function.  This is called sequentially
def animate(i):
    x = np.linspace(0, 2, 1000)
    y = np.sin(2 * np.pi * (x - 0.01 * i))
    line.set_data(x, y)
    return line,

# call the animator.  blit=True means only re-draw the parts that have changed.
anim = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=200, interval=20, blit=True)

# save the animation as an mp4.  This requires ffmpeg or mencoder to be
# installed.  The extra_args ensure that the x264 codec is used, so that
# the video can be embedded in html5.  You may need to adjust this for
# your system: for more information, see
# http://matplotlib.sourceforge.net/api/animation_api.html
anim.save('basic_animation.mp4', fps=30, extra_args=['-vcodec', 'libx264'])

plt.show()