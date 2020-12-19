"""
Cube collision avoidance game

Made using Python 3.7
           Pygame 1.9.6
           PyOpenGL 3.1.5

"""


import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import random

vertices = (        #This tuple predefines the vertices of cube
    (1,-1,-1),
    (1,1,-1),
    (-1, 1, -1),
    (-1,-1,-1),
    (1,-1,1),
    (1,1,1),
    (-1,-1,1),
    (-1,1,1)
)

edges = (   #This tuple predefines how the vertices connect as edges
    (0,1),
    (0,3),
    (0,4),
    (2,1),
    (2,3),
    (2,7),
    (6,3),
    (6,4),
    (6,7),
    (5,1),
    (5,4),
    (5,7),
)

surfaces= (     #This tuple defines how the vertices connect as a surface
    (0,1,2,3),
    (3,2,7,6),
    (6,7,5,4),
    (4,5,1,0),
    (1,5,7,2),
    (4,0,3,6),
)

colors = (      #This tuple defines the colors that will be used to color the cube

    (1,0,0),
    (0,1,0),
    (0,0,1),
    (0,16,0),
    (1,1,1),
    (0,1,1),
    (1,0,0),
    (0,1,0),
    (0,0,1),
    (0,0,0),
    (1,1,1),
    (0,1,1),

)


def set_Vertices(max_distance, min_distance):
    #This function is used to make multiple cubes in random locations

    x_offset = random.randrange(-10,10)
    y_offset = random.randrange(-10,10)
    z_offset = random.randrange(-1*max_distance,-1*min_distance)

    new_Vertices = []

    for vertex in vertices:
        new_vertex_x = vertex[0] + x_offset
        new_vertex_y = vertex[1] + y_offset
        new_vertex_z = vertex[2] + z_offset

        new_Vertices.append((new_vertex_x,new_vertex_y,new_vertex_z))


    return new_Vertices



def Cube(vertices):
    #This function uses the vertices to define a new cube

    glBegin(GL_QUADS)
    colorChoice = 0

    for surface in surfaces:
        colorChoice = 0
        for vertex in surface:
            colorChoice+=1
            glColor3fv(colors[colorChoice])
            glVertex3fv(vertices[vertex])
    glEnd()


    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()

def main():
    pygame.init()
    display = (800,600)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)

    max_distance = 100      #This is the maximum distance away from the camera that a new cube can be made
    min_distance = 50       #This is the minimum distance away from the camera that a new cube can be made

    gluPerspective(45,(display[0]/display[1]), 0.1, min_distance)       #defines view frustrum
    glEnable(GL_DEPTH_TEST)                                             #adds depth to cubes so they look solid
    #glTranslatef(random.randrange(-5,5),random.randrange(-5,5),-40.0)  #randomly places viewing position at start of game

    x_move = 0      #Used to control how player will move
    y_move = 0      #Used to control how player will move


    cube_dict = {}  #dictionary where cubes will be stored

    for num in range(20):
        cube_dict[num] = set_Vertices(max_distance,min_distance)    #creates 20 cubes in random locations


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()



            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_move = 0.3
                if event.key == pygame.K_RIGHT:
                    x_move = -0.3
                if event.key == pygame.K_UP:
                    y_move = -0.3
                if event.key == pygame.K_DOWN:
                    y_move = 0.3

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_move = 0
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    x_move = 0


        pos = glGetDoublev(GL_MODELVIEW_MATRIX)     #gets position of viewing camera

        camera_x = pos[3][0]
        camera_y = pos[3][1]
        camera_z = pos[3][2]

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        glTranslatef(x_move,y_move,.5)                  #moves the player based on whether Left or Right key is pressed and moves player through z direction as game continues


        for new_cube in cube_dict:
            Cube(cube_dict[new_cube])   #creates cubes from cube_dict based on vertices

        for cube in cube_dict:
            if camera_z <= cube_dict[cube][0][2]:
                print("passed a cube")              #checks if cube has been passed

                cube_dict[cube] = set_Vertices(int(-1*(camera_z-max_distance)),int(-1*(camera_z-min_distance))) #creates a new cube if a cube has been passed




        pygame.display.flip()
        pygame.time.wait(10)

main()

