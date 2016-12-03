#matplotlib inline
#import requests
import sys
import matplotlib.pyplot as plt
import matplotlib.backends.backend_pdf
import matplotlib
import pandas as pd
import seaborn as sns
from matplotlib.patches import Circle, Rectangle, Arc
from local_libs.option_d import test_cm as viridis # another file i have
#from PIL import Image
import os
import numpy as np
from scipy.misc import imread
from PyPDF2 import PdfFileMerger

''' libraries needed to run '''
'''
python 2.7
matplotlib
pandas
seaborn
option_d file (local file not library)
PIL
os
'''

''' ONLY CHANGE VARABLES WITHIN PROPERTIES COMMENT!!! '''

'''PROPERTIES BELOW'''
#Change this to input file name, must be CSV file created by StoreShots.py
input_file_name = "input.csv"
heat_map_type = "basic" #OPTIONS: basic, hex, coolwarm, blue
sections = True
expanded_shot_points = True
'''PROPERTIES ABOVE'''


basic_makes_and_misses = []
basic_points_per_shot = []
files = []
position_locations = [(0,23),(120,23),(0,120),(-120,23),(-185,23),(-145,140),(0,200),(145,140),(185,23),(245,23),(200,210),(0,275),(-200,210),(-245,23)]
position_points = [2,2,2,2,2,2,2,2,2,3,3,3,3,3]

def draw_court(ax=None, color='black', lw=3, outer_lines=False):
    # If an axes object isn't provided to plot onto, just get current one
    if ax is None:
        ax = plt.gca()

    # Create the various parts of an NBA basketball court

    # Create the basketball hoop
    # Diameter of a hoop is 18" so it has a radius of 9", which is a value
    # 7.5 in our coordinate system
    hoop = Circle((0, 0), radius=7.5, linewidth=lw, color=color, fill=False)

    # Create backboard
    backboard = Rectangle((-30, -7.5), 60, -1, linewidth=lw, color=color)

    # The paint
    # Create the outer box 0f the paint, width=16ft, height=19ft
    outer_box = Rectangle((-80, -47.5), 160, 190, linewidth=lw, color=color,
                          fill=False)
    # Create the inner box of the paint, widt=12ft, height=19ft
    inner_box = Rectangle((-60, -47.5), 120, 190, linewidth=lw, color=color,
                          fill=False)

    # Create free throw top arc
    top_free_throw = Arc((0, 142.5), 120, 120, theta1=0, theta2=180,
                         linewidth=lw, color=color, fill=False)
    # Create free throw bottom arc
    bottom_free_throw = Arc((0, 142.5), 120, 120, theta1=180, theta2=0,
                            linewidth=lw, color=color, linestyle='dashed')
    # Restricted Zone, it is an arc with 4ft radius from center of the hoop
    restricted = Arc((0, 0), 80, 80, theta1=0, theta2=180, linewidth=lw,
                     color=color)

    # Three point line
    # Create the side 3pt lines, they are 14ft long before they begin to arc
    corner_three_a = Rectangle((-220, -47.5), 0, 140, linewidth=lw,
                               color=color)
    corner_three_b = Rectangle((220, -47.5), 0, 140, linewidth=lw, color=color)
    # 3pt arc - center of arc will be the hoop, arc is 23'9" away from hoop
    # I just played around with the theta values until they lined up with the 
    # threes
    three_arc = Arc((0, 0), 475, 475, theta1=22, theta2=158, linewidth=lw,
                    color=color)

    # Center Court
    center_outer_arc = Arc((0, 422.5), 120, 120, theta1=180, theta2=0,
                           linewidth=lw, color=color)
    center_inner_arc = Arc((0, 422.5), 40, 40, theta1=180, theta2=0,
                           linewidth=lw, color=color)

    # List of the court elements to be plotted onto the axes
    court_elements = [hoop, backboard, outer_box, inner_box, top_free_throw,
                      bottom_free_throw, restricted, corner_three_a,
                      corner_three_b, three_arc, center_outer_arc,
                      center_inner_arc]

    if outer_lines:
        # Draw the half court line, baseline and side out bound lines
        outer_lines = Rectangle((-250, -47.5), 500, 470, linewidth=lw,
                                color=color, fill=False)
        court_elements.append(outer_lines)

    ''' bens attempt at making section lines '''
    if sections:
        sec_color = "white"
        s1 = Circle((0, 0), radius=70, linewidth=3, color=sec_color, fill=False)
        court_elements.append(s1)
        s2 = Circle((0, 0), radius=165, linewidth=3, color=sec_color, fill=False)
        court_elements.append(s2)
        s3 = Arc((80, 81), 95, 0, angle=50, linewidth=3, color=sec_color)
        court_elements.append(s3)
        s4 = Arc((-80, 81), 95, 0, angle=-50, linewidth=3, color=sec_color)
        court_elements.append(s4)
        s3 = Arc((89, 176), 76, 0, angle=50, linewidth=3, color=sec_color)
        court_elements.append(s3)
        s4 = Arc((-89, 176), 76, 0, angle=-50, linewidth=3, color=sec_color)
        court_elements.append(s4)
        s5 = three_arc = Arc((0, 0), 475, 475, theta1=22, theta2=158, linewidth=3, color="black")
        court_elements.append(s5)
        s6 = Rectangle((-220, -47.5), 0, 140, linewidth=3, color="black")
        court_elements.append(s6)
        s7 = Rectangle((220, -47.5), 0, 140, linewidth=3, color="black")
        court_elements.append(s7)
        s8 = Arc((185, 75), 86, 0, angle=50, linewidth=3, color=sec_color)
        court_elements.append(s8)
        s9 = Arc((-185, 75), 86, 0, angle=-50, linewidth=3, color=sec_color)
        court_elements.append(s9)
        s10 = Circle((0, 0), radius=350, linewidth=3, color=sec_color, fill=False)
        court_elements.append(s10)
        s11 = Arc((232, 94), 30, 0, angle=0, linewidth=3, color=sec_color)
        court_elements.append(s11)
        s12 = Arc((-232, 94), 30, 0, angle=0, linewidth=3, color=sec_color)
        court_elements.append(s12)
        s13 = Arc((110, 270), 120, 0, angle=50, linewidth=3, color=sec_color)
        court_elements.append(s13)
        s14 = Arc((-110, 270), 120, 0, angle=-50, linewidth=3, color=sec_color)
        court_elements.append(s14)
    # Add the court elements onto the axes
    for element in court_elements:
        ax.add_patch(element)

    return ax

def get_norm(made, avgs, stds, avgs_pt, stds_pt): 
    basic_makes_and_misses = []
    basic_points_per_shot = []
    i=0
    while i < len(position_num):
        if stds[i] == 0:
            stds[i]+=0.000001 #almost no stddev, this is a bad solution, but yeah.
        percent = (float(made[i]) - avgs[i])/stds[i]
        basic_makes_and_misses.append(percent)
        #print made[i], avgs[i], stds[i], avgs_pt[i], stds_pt[i]
        if stds_pt[i] == 0:
            stds_pt[i]+=0.000001
        points_eff = ((float(made[i])*float(position_points[i])/10)-avgs_pt[i])/stds_pt[i]
        basic_points_per_shot.append(points_eff)
        i+=1
        
    return basic_makes_and_misses, basic_points_per_shot

def convert_input_file(input_file_name):
    with open(input_file_name) as f:
        content = [x.strip().split(",") for x in f]
        kids = content.pop(0)
        del kids[0]
        kids.append(None) # dummy 
        position_num = [x[0] for x in content]
        
        makes = []
        y=0
        for k in kids:
            makes.append([x[y] for x in content])
            y+=1
        del makes[0]  
    return kids, makes, position_num
    
def setup_stats(made):
    i=0
    basic_makes_and_misses = []
    basic_points_per_shot = []
    while i < len(position_num):
            percent = float(made[i])/10
            basic_makes_and_misses.append(percent)
            points_eff = float(made[i])*int(position_points[i])
            basic_points_per_shot.append(points_eff)
            i+=1
    return basic_makes_and_misses, basic_points_per_shot
            
if __name__ == "__main__":
    print "Generating plot from input.csv..."
    try:
        os.remove("./converted_input_file.temp.csv")
    except OSError:
        pass
    
    kids, makes, position_num = convert_input_file(input_file_name)
    points = []
    running_sum = [0]*len(makes[0]); running_sum2 = [0]*len(makes[0])
    if heat_map_type != "basic":
        data = pd.read_csv(input_file_name)
        #shot_df = pd.DataFrame(shots, columns=headers)
        shot_df = data
        # View the head of the DataFrame and all its columns
        from IPython.display import display
        with pd.option_context('display.max_columns', None):
            display(shot_df.head())

    if heat_map_type == "basic":
        #store_all_scores("all_makes_and_misses.csv", "all_points.csv")
        # heatmap based on makes vs misses
        #norm = matplotlib.colors.Normalize(vmin=0, vmax=1)
        k_num = 0
        while k_num < len(kids)-1:
            print "Processing...", kids[k_num]
            plt.clf()
            basic_makes_and_misses, basic_points_per_shot = setup_stats(makes[k_num])
            ax = plt.subplot()#joint_shot_chart.ax_joint
            draw_court(ax)
            basic_makes_and_misses = [float(u) for u in basic_makes_and_misses]
            xs = [p[0] for p in position_locations]
            ys = [p[1] for p in position_locations]
            plt.scatter(xs, ys, s=800, c=basic_makes_and_misses, cmap="coolwarm")
            plt.clim(0,1)
            
            cbar = plt.colorbar(ticks=[0, 0.5, 1])
            cbar.ax.set_yticklabels(['0%', '50%', '100%'])
            img = imread("./images/wood.jpg")
            plt.imshow(img, extent=[-450, 450, 450, -450])

            # Adjust the axis limits and orientation of the plot in order
            # to plot half court, with the hoop by the top of the plot
            ax.set_xlim(-250,250)
            ax.set_ylim(422.5, -47.5)

            # Get rid of axis labels and tick marks
            ax.set_xlabel('')
            ax.set_ylabel('')
            ax.tick_params(labelbottom='off', labelleft='off')
            plt.title("%s Makes per Location"%(kids[k_num]))

            with matplotlib.backends.backend_pdf.PdfPages("%s_temp.pdf"%(kids[k_num])) as pdf:
                files.append("%s_temp.pdf"%(kids[k_num]))
                pdf.savefig()
                plt.close()

            
            #plt.show()

            #heatmap based on points
            plt.clf()
            ax = plt.subplot()#joint_shot_chart.ax_joint
            draw_court(ax)
            basic_points_per_shot = [float(u)/10 for u in basic_points_per_shot]
            xs = [p[0] for p in position_locations]
            ys = [p[1] for p in position_locations]
            plt.scatter(xs, ys, s=800, c=basic_points_per_shot, cmap="coolwarm")
            plt.clim(0,3)
            
            cbar = plt.colorbar(ticks=[0, 1.5, 3])
            #cbar.ax.set_yticklabels(['0%', '50%', '100%'])
            img = imread("./images/wood.jpg")
            plt.imshow(img, extent=[-450, 450, 450, -450])

            
            # Adjust the axis limits and orientation of the plot in order
            # to plot half court, with the hoop by the top of the plot
            ax.set_xlim(-250,250)
            ax.set_ylim(422.5, -47.5)

            # Get rid of axis labels and tick marks
            ax.set_xlabel('')
            ax.set_ylabel('')
            ax.tick_params(labelbottom='off', labelleft='off')
            plt.title("%s Point Efficiency (Points per Shot)"%(kids[k_num]))

            with matplotlib.backends.backend_pdf.PdfPages("%s_temp2.pdf"%(kids[k_num])) as pdf:
                files.append("%s_temp2.pdf"%(kids[k_num]))
                pdf.savefig()
                plt.close()
            
            #plt.show()
            k_num+=1

            bb = 0
            for b in basic_makes_and_misses:
                running_sum[bb]+=b
                bb+=1
            pp = 0
            for p in basic_points_per_shot:
                running_sum2[pp]+=p
                pp+=1
            points.append(basic_points_per_shot)
           
        makes_avgs = [float(rs)/len(kids) for rs in running_sum]
        #makes_avgs = ["{0:.2f}".format(fl) for fl in makes_avgs]
        makes_avgs = [float(fl) for fl in makes_avgs]
        makes_avgs = makes_avgs[:14]
        pts_avgs = [float(rs2)/len(kids) for rs2 in running_sum2]
        pts_avgs = pts_avgs[:14]

        plt.clf()
        ax = plt.subplot()#joint_shot_chart.ax_joint
        draw_court(ax)
        xs = [p[0] for p in position_locations]
        ys = [p[1] for p in position_locations]
        plt.scatter(xs, ys, s=800, c=makes_avgs, cmap="coolwarm")
        plt.clim(0,1)
        
        cbar = plt.colorbar(ticks=[0, 0.5, 1])
        cbar.ax.set_yticklabels(['0%', '50%', '100%'])
        img = imread("./images/wood.jpg")
        plt.imshow(img, extent=[-450, 450, 450, -450])

        
        # Adjust the axis limits and orientation of the plot in order
        # to plot half court, with the hoop by the top of the plot
        ax.set_xlim(-250,250)
        ax.set_ylim(422.5, -47.5)

        # Get rid of axis labels and tick marks
        ax.set_xlabel('')
        ax.set_ylabel('')
        ax.tick_params(labelbottom='off', labelleft='off')
        plt.title("Average Makes per Location")

        with matplotlib.backends.backend_pdf.PdfPages("average_temp.pdf") as pdf:
            files.append("average_temp.pdf")
            pdf.savefig()
            plt.close()
            
        plt.clf()
        ax = plt.subplot()#joint_shot_chart.ax_joint
        draw_court(ax)
        xs = [p[0] for p in position_locations]
        ys = [p[1] for p in position_locations]
        plt.scatter(xs, ys, s=800, c=pts_avgs, cmap="coolwarm")
        plt.clim(0,3)
        
        cbar = plt.colorbar(ticks=[0, 1.5, 3])
        #cbar.ax.set_yticklabels(['0%', '50%', '100%'])
        img = imread("./images/wood.jpg")
        plt.imshow(img, extent=[-450, 450, 450, -450])

        
        # Adjust the axis limits and orientation of the plot in order
        # to plot half court, with the hoop by the top of the plot
        ax.set_xlim(-250,250)
        ax.set_ylim(422.5, -47.5)

        # Get rid of axis labels and tick marks
        ax.set_xlabel('')
        ax.set_ylabel('')
        ax.tick_params(labelbottom='off', labelleft='off')
        plt.title("Average Point Efficiency (Points per Shot)")

        with matplotlib.backends.backend_pdf.PdfPages("average_temp2.pdf") as pdf:
            files.append("average_temp2.pdf")
            pdf.savefig()
            plt.close()

##        # get stds, this looks crazy, but I was in a hurry :( 
##        make_stds = [];pts_stds =[]
##        flipped = []
##        [flipped.append([]) for flip in xrange(14)]
##        flippedp = []
##        [flippedp.append([]) for flip in xrange(14)]
##
##        for m_col in makes:
##            el=0
##            while el < len(m_col):
##                flipped[el].append(m_col[el])
##                el+=1
##        for m_row in flipped:
##            m_row = map(float, m_row)
##            make_stds.append(np.std(m_row))
##        # same logic as above, but var changes, this should be modularized
##        for p_col in points:
##            elp=0
##            while elp < len(m_col):
##                flippedp[elp].append(p_col[elp])
##                elp+=1
##        for p_row in flippedp:
##            p_row = map(float,p_row)
##            pts_stds.append(np.std(p_row))
##                            
##        k_num = 0
##        while k_num < len(kids)-1:
##            plt.clf()
##            norm_makes_and_misses, norm_points_per_shot = get_norm(makes[k_num],makes_avgs, make_stds, pts_avgs, pts_stds)
##            ax = plt.subplot()#joint_shot_chart.ax_joint
##            draw_court(ax)
##            norm_points_per_shot = [int(u) for u in norm_points_per_shot]
##            xs = [p[0] for p in position_locations]
##            ys = [p[1] for p in position_locations]
##            plt.scatter(xs, ys, s=800, c=norm_points_per_shot, cmap="coolwarm")
##            plt.clim(0,5)
##            
##            plt.colorbar()
##            img = imread("./images/wood.jpg")
##            plt.imshow(img, extent=[-450, 450, 450, -450])
##
##            
##            # Adjust the axis limits and orientation of the plot in order
##            # to plot half court, with the hoop by the top of the plot
##            ax.set_xlim(-250,250)
##            ax.set_ylim(422.5, -47.5)
##
##            # Get rid of axis labels and tick marks
##            ax.set_xlabel('')
##            ax.set_ylabel('')
##            ax.tick_params(labelbottom='off', labelleft='off')
##            plt.title("Normalized %s Point Efficiency (Points per Shot)"%(kids[k_num]))
##
##            with matplotlib.backends.backend_pdf.PdfPages("%s_temp2_norm.pdf"%(kids[k_num])) as pdf:
##                files.append("%s_temp2_norm.pdf"%(kids[k_num]))
##                pdf.savefig()
##                plt.close()
##
##            #plt.show()
##            
##            plt.clf()
##            ax = plt.subplot()#joint_shot_chart.ax_joint
##            draw_court(ax)
##            norm_makes_and_misses = [float(u) for u in norm_makes_and_misses]
##            xs = [p[0] for p in position_locations]
##            ys = [p[1] for p in position_locations]
##            plt.scatter(xs, ys, s=800, c=norm_makes_and_misses, cmap="coolwarm")
##            plt.clim(0,5)
##            
##            plt.colorbar()
##            img = imread("./images/wood.jpg")
##            plt.imshow(img, extent=[-450, 450, 450, -450])
##
##            
##            # Adjust the axis limits and orientation of the plot in order
##            # to plot half court, with the hoop by the top of the plot
##            ax.set_xlim(-250,250)
##            ax.set_ylim(422.5, -47.5)
##
##            # Get rid of axis labels and tick marks
##            ax.set_xlabel('')
##            ax.set_ylabel('')
##            ax.tick_params(labelbottom='off', labelleft='off')
##            plt.title("Normalized %s Makes per Location"%(kids[k_num]))
##
##            with matplotlib.backends.backend_pdf.PdfPages("%s_temp_norm.pdf"%(kids[k_num])) as pdf:
##                files.append("%s_temp_norm.pdf"%(kids[k_num]))
##                pdf.savefig()
##                plt.close()
##            k_num+=1

        print "removing temp files... do not close...."
        pdfs = files
        pdfs.sort()
        outfile = PdfFileMerger()
        [outfile.append(open(f, 'rb')) for f in pdfs]
        outfile.write(open('result.pdf', 'wb'))
        [os.remove(fo) for fo in pdfs]
        outfile.close()
        plt.close('all')
        #sys.exit(-1) #yeah i shouldnt have to do this but whatever
        
