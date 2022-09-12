import pygame as pg
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

cubeVertices = ((0,0,0),(0,0,1),(0,1,1),(0,1,0))
cubeEdges = ((0,1),(1,2),(2,3),(3,0))

def generateOutline(cubeVertices):
    for i in range(0,len(cubeVertices)):
        


def wireCube():
    glBegin(GL_LINES)
    for cubeEdge in cubeEdges:
        for cubeVertex in cubeEdge:
            glVertex3fv(cubeVertices[cubeVertex])
    glEnd()

def main():
    pg.init()
    display = (1680, 1050)
    pg.display.set_mode(display, DOUBLEBUF|OPENGL)

    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)

    glTranslatef(0.0, 0.0, -5)

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()

        glRotatef(1, 1, 1, 1)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        glColor3f(255,255,255)
        wireCube()
        glColor3f(0,0,255)
        #solidCube()
        pg.display.flip()
        pg.time.wait(10)

if __name__ == "__main__":
    main()