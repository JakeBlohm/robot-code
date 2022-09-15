import pygame as pg
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

cubeVertices = ((0,0,0),(0,1,0),(1,2,0),(1,1.8,0))

def generateOutline(cubeVertices):
    cubeEdges = []
    for i in range(0,len(cubeVertices)-1):
        cubeEdges.append((i,i+1))
    return cubeEdges
        
cubeEdges = generateOutline(cubeVertices)

def wireCube(cubeEdges, cubeVertices):
    glBegin(GL_LINES)
    for cubeEdge in cubeEdges:
        for cubeVertex in cubeEdge:
            glVertex3fv(cubeVertices[cubeVertex])
    glEnd()

def main():
    pg.init()
    display = (1280, 800)
    pg.display.set_mode(display, DOUBLEBUF|OPENGL)

    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)

    glTranslatef(0.0, -1, -5)
    rotX = 0
    rotY = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            elif event.type == pg.KEYDOWN:
                match(event.key):
                    case pg.K_w:
                        rotX += 1
                    case pg.K_a:
                        rotY += 1
                    case pg.K_s:
                        rotX += -1
                    case pg.K_d:
                        rotY += -1
            elif event.type == pg.KEYUP:
                match(event.key):
                    case pg.K_w:
                        rotX -= 1
                    case pg.K_a:
                        rotY -= 1
                    case pg.K_s:
                        rotX -= -1
                    case pg.K_d:
                        rotY -= -1
        glRotatef(rotX*1, 1, 0, 0)
        glRotatef(rotY*1, 0, 1, 0)
        cubeEdges = generateOutline(cubeVertices)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        glColor3f(255,255,255)
        glLineWidth(5)
        wireCube(cubeEdges, cubeVertices)
        #glColor3f(0,0,255)
        #solidCube()
        pg.display.flip()
        pg.time.wait(10)

if __name__ == "__main__":
    main()