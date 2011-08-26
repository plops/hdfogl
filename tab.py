import tables
import time
from numpy import *
import threading
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *



f=tables.openFile("/home/martin/data/23_8_mtA488_GSH15series_A.h5")
print "data loaded"
dat=f.root.ImageData

#amin(dat[:,:,3])

#cast['uint8'](255*(dat[:,1,3]-amin(dat[:,1,3]))/(amax(dat[:,1,3])-amin(dat[:,1,3])))

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


def next_power_of_two(n):
    i=1
    while(i<n):
        i=i*2
    return i



count=0 

tex=-1

def load_texture():
    global count
    global tex
    global dat
    if count==0:
        count=count+1
        if tex>=0:
            glDeleteTextures(tex)
            print "delete old texture"
            
        print "new texture"
        glEnable(GL_TEXTURE_2D)
        tex=glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D,int(tex))
        # glMatrixMode(GL_COLOR_MATRIX)
        # glScaled(10,10,10)
        glTexImage2D(GL_TEXTURE_2D,0,GL_LUMINANCE,
                     next_power_of_two(dat.shape[1]),
                     next_power_of_two(dat.shape[2]),0,
                     GL_LUMINANCE,GL_UNSIGNED_BYTE,0)
        glTexSubImage2D(GL_TEXTURE_2D,0,0,0,
                        dat.shape[1],dat.shape[2],
                        GL_LUMINANCE,GL_UNSIGNED_BYTE,
                        norm_u8(dat[12,:,:]))
    # glMatrixMode(GL_MODELVIEW)
    

def drawfun():
    glClearColor(1,0,0,1)
    load_texture()
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    glColor4d(1,1,1,1)
    glTranslated(12,12,0)
    glScaled(dat.shape[1],dat.shape[2],1)
    glBegin(GL_QUADS)
    x=1 #dat.shape[1]
    y=1 #dat.shape[2]
    for v in [[0,0],[x,0],[x,y],[0,y]]:
        glVertex2d(*v)
        glTexCoord2d(*v)
    glEnd()
    time.sleep(1/30.)
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
