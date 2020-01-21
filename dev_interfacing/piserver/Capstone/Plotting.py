import matplotlib.pyplot as plt
import matplotlib.animation as animation

############################################
########### PLOTTING #######################
############################################


def resetStartPos():
    global start_pos
    start_pos = 0;
    
# Parameters
X_LEN = 500         # Number of points to display
Y_RANGE = [0, 0.3]  # Range of possible Y values to display

# Create figure for plotting
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
xs = list(range(0, X_LEN))
ys = [0] * X_LEN
ax.set_ylim(Y_RANGE)

# Create a blank line. We will update the line in animate
line, = ax.plot(xs, ys)

def updateList(ys,data):
    global start_pos, next_start
    
    ys_len = len(ys)
    data_len = len(data)
   
    next_start = start_pos+data_len



    if next_start >= ys_len:
        start_pos=0
    else:
        for i in range(data_len):
            ys[start_pos+i] = data[i]
        start_pos=next_start

    return ys
    
def animate(i, ys):
    
    
    # Add y to list
    
    data = readByte()

    ys = updateList(ys,parseDataList(data))
  
    print(ys)
    # # Limit y list to set number of items
    # ys = ys[-X_LEN:]

    # Update line with new Y values
    line.set_ydata(ys)

    return line,

