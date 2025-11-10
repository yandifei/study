import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from matplotlib.path import Path

def draw_five_star(center, radius, rotation=0):
    angles = np.linspace(0, 2*np.pi, 6)[:-1] + np.pi/2 + rotation
    outer_points = [(center[0] + radius * np.cos(angle), 
                     center[1] + radius * np.sin(angle)) 
                    for angle in angles]
    
    inner_radius = radius * np.sin(np.pi/10) / np.sin(7*np.pi/10)
    inner_angles = angles + np.pi/5
    inner_points = [(center[0] + inner_radius * np.cos(angle), 
                     center[1] + inner_radius * np.sin(angle)) 
                    for angle in inner_angles]
    
    vertices = []
    codes = []
    for i in range(5):
        vertices.append(outer_points[i])
        codes.append(Path.MOVETO if i == 0 else Path.LINETO)
        vertices.append(inner_points[i])
        codes.append(Path.LINETO)
    
    vertices.append(outer_points[0])  
    codes.append(Path.LINETO)
    
    return Path(vertices, codes)

def draw_china_flag(width=900, height=600):
    fig, ax = plt.subplots(1, 1, figsize=(width/100, height/100))
    
    flag_rect = patches.Rectangle((0, 0), width, height, 
                                 facecolor='#DE2910', edgecolor='none')
    ax.add_patch(flag_rect)
    unit_x = width / 30  
    unit_y = height / 20  
    big_star_center = (5 * unit_x, 15 * unit_y)  # 上5下5、左5右10
    big_star_radius = 3 * unit_y
    big_star = draw_five_star(big_star_center, big_star_radius)
    big_star_patch = patches.PathPatch(big_star, facecolor='#FFDE00', 
                                       edgecolor='none')
    ax.add_patch(big_star_patch)
    
    small_star_centers = [
        (10 * unit_x, 18 * unit_y),  
        (12 * unit_x, 16 * unit_y),  
        (12 * unit_x, 13 * unit_y),  
        (10 * unit_x, 11 * unit_y)   
    ]
    
    small_star_radius = 1 * unit_y
    
    for center in small_star_centers:
        dx = big_star_center[0] - center[0]
        dy = big_star_center[1] - center[1]
        angle = np.arctan2(dy, dx) - np.pi/2
        
        small_star = draw_five_star(center, small_star_radius, angle)
        small_star_patch = patches.PathPatch(small_star, facecolor='#FFDE00', 
                                             edgecolor='none')
        ax.add_patch(small_star_patch)
    
    ax.set_xlim(0, width)
    ax.set_ylim(0, height)
    ax.set_aspect('equal')
    ax.axis('off')
    
    plt.tight_layout()
    plt.show()

draw_china_flag()
