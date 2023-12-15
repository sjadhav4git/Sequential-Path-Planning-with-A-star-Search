import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
import random
import json
import matplotlib.patches as patches

class Movements():
    def detailed_viewer(self, frame_interval):
        with open ("src/database/detailed_final_path.json","r") as json_file:
            data = json.load(json_file)
        
        # Create a function to update the line during animation
        points = data['final_path']
        X,Y,Z =[],[],[]
        for pt in points:
            X.append(pt[0])
            Y.append(pt[1])
            Z.append(pt[2])



        # import data from joint_var.json
        with open("src/database/joint_var.json","r") as json_read:
            data = json.load(json_read)
        
        joint_var_locations = data["joint_var_locations"]

        Xs = []
        Ys = []
        Zs = []
        for itr in joint_var_locations:
            xs = [0]
            ys = [0]
            zs = [0]
            for pt in itr:
                xs.append(pt[0])
                ys.append(pt[1])
                zs.append(pt[2])
            Xs.append(xs)
            Ys.append(ys)
            Zs.append(zs)

    
                


        def update(frame):
        # def update(frame, line, ax, box):
            ax.cla()  # Clear the previous frame
            ax.set_xlabel('X Label')
            ax.set_ylabel('Y Label')
            ax.set_zlabel('Z Label')
            ax.set_title('3D Line Animation')
            
            ax.grid(False, which = 'both',linestyle = '.',linewidth = 0.5)
            # Fix the axis limits
            ax.set_xlim(-100, 200)  # Set X-axis limits from 0 to 5
            ax.set_ylim(0, 300)  # Set Y-axis limits from 0 to 7
            ax.set_zlim(0, 300)  # Set Z-axis limits from 0 to 4
            # ax.set_facecolor('#e6f7ff')
            ax.set_facecolor('gray')

            ax.w_xaxis.line.set_color("green")
            ax.w_yaxis.line.set_color("blue")
            ax.w_zaxis.line.set_color("red")

            colors = 'bgrcmyk'
            random_color = random.choice(colors)
            if Z[frame]==35:
                clr = 'g'
            elif Z[frame]==10:
                clr = 'r'
            else:
                clr ='b'

            if frame > 20 and frame <= len(X)-21:
                lower_lim = frame-20
            elif frame <= 20:
                lower_lim = 0
            else:
                lower_lim = frame-(len(X)-frame)
            
            
            
            ax.plot(X[lower_lim:frame], Y[lower_lim:frame], Z[lower_lim:frame], marker='', color="b", label='Line')

            ax.plot(Xs[frame], Ys[frame], Zs[frame], marker='o', color='g',linewidth = 5, label='Line')
            
            ax.scatter(X[frame],Y[frame],Z[frame],color='r',marker ='o', label = 'dot')
            
            info_text = f'Frame: {frame}/{len(X) - 1}'  # Customize the information as needed
            info_X = f"X: {X[frame-1]}"
            info_Y = f"Y: {Y[frame-1]}"
            info_Z = f"Z: {Z[frame-1]}"

            ax.text(7, 1, 1, info_text, fontsize=12, color='red')
            ax.text(100,50,0, info_X, fontsize = 12, color ='b')
            ax.text(100,50,-20, info_Y, fontsize = 12, color ='b')
            ax.text(100,50,-40, info_Z, fontsize = 12, color ='b')


            for ind,ele in enumerate(all_locations):
                # info = str(ind)
                ax.text(ele[0],ele[1],ele[2], ind+1, fontsize = 9, color ='k')
                ax.scatter(ele[0],ele[1],10,color='k',marker ='.', label = 'dot')
           
            if frame == len(X) - 1:
                # for i in range(20):
                #     lower_lim = frame-i
                #     print (lower_lim,frame)
                #     ax.plot(X[lower_lim:frame], Y[lower_lim:frame], Z[lower_lim:frame], marker='', color=clr, label='Line')
                #     ax.scatter(X[frame],Y[frame],Z[frame],color='r',marker ='o', label = 'dot')
                ani.event_source.stop()

            return ax

        # Create a 3D plot
        fig = plt.figure(figsize=(10,10))
        ax = fig.add_subplot(111, projection='3d',position = [0,0,1,1])
        
        # -------------
        x_cords = [Int for Int in range(-65,61,30)]
        y_cords = [Int for Int in range(240,119,-30)]
        all_locations = []
        z = 0
        i = 1
        for y in y_cords:
            for x in x_cords:
                all_locations.append([x,y,z])
                i += 1
                ax.text(x,y,z,'Q',fontsize = 15,color='k')
        # -------------
        # Set the number of frames for the animation
        num_frames = len(X)

        
        # Create the animation
        ani = FuncAnimation(fig, update, frames=num_frames, interval=frame_interval, blit=False)
        plt.show()
