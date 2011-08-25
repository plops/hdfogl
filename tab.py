import tables
from numpy import *
import threading
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *



f=tables.openFile("/home/martin/data/23_8_mtA488GSH15series_B.h5")
dat=f.root.ImageData

amin(dat[:,:,3])

cast['uint8'](255*(dat[:,1,3]-amin(dat[:,1,3]))/(amax(dat[:,1,3])-amin(dat[:,1,3])))

def norm_u8(a):
    mi=amin(a)
    ma=amax(a)
    s=255/(ma-mi)
    return cast['uint8'](s*(a-mi))

window=0

def init(w,h):
    glClearColor(0,0,0,0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0,w,h,0,-1,1)
    glMatrixMode(GL_MODELVIEW)

def reset_count():
    count=0 

reset_count()

tex=-1


def drawfun():
    global count
    global tex
    glClearColor(1,0,0,1)
    if count==0:
        count=count+1
        if tex>=0:
            glDeleteTextures(tex)
        glEnable(GL_TEXTURE_2D)
        tex=glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D,int(tex))
       # glMatrixMode(GL_COLOR_MATRIX)
       # glScaled(10,10,10)
        glTexImage2D(GL_TEXTURE_2D,0,GL_LUMINANCE,dat.shape[1],dat.shape[2],0,
                     GL_LUMINANCE,GL_UNSIGNED_BYTE,norm_u8(dat[10,:,:]))
       # glMatrixMode(GL_MODELVIEW)
        
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    glColor4d(1,1,1,1)
    glTranslated(0,0,0)
    glBegin(GL_QUADS)
    x=dat.shape[1]
    y=dat.shape[2]
    for v in [[0,0],[x,0],[x,y],[0,y]]:
        glVertex2d(*v)
        glTexCoord2d(*v)
    glEnd()
    glutSwapBuffers()
    
def draw():
    drawfun()

def main():
    global window
    glutInit("")
    glutInitDisplayMode(GLUT_RGBA|GLUT_DOUBLE|GLUT_ALPHA)
    glutInitWindowSize(640,480)
    window=glutCreateWindow("test")
    glutDisplayFunc(draw)
    glutIdleFunc(draw)
    init(640,480)
    glutMainLoop()


class mainthread(threading.Thread):
    def run(self):
        main()


m = mainthread()
# m.start()
