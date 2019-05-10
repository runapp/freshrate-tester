import pyglet
from pyglet.gl import *
import pyglet.window.key as keys


class HelloWorldWindow(pyglet.window.Window):
    def __init__(self, name, fps, width=None, height=None):
        super(HelloWorldWindow, self).__init__(width=width, height=height, vsync=False)
        # Run "self.update" 128 frames a second and set FPS limit to 128.
        pyglet.clock.schedule_interval(self.update, 1.0/fps)
        pyglet.clock.set_fps_limit(fps)
        self.name = name
        self.fps_display = pyglet.clock.ClockDisplay()
        self.fps = fps
        self.poses = [0., 0., 0.]
        self.frame_cnt = 0
        glClearColor(0.0, 0.0, 0.0, 0.0)
        glEnableClientState(GL_VERTEX_ARRAY)

    def on_resize(self, width, height):
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, 1, 0, 1, -1, 1)
        glMatrixMode(GL_MODELVIEW)

    def update(self, dt):
        self.frame_cnt = (self.frame_cnt+1) & 0xffff
        dx = dt*0.6
        self.poses[0] += dx
        if self.poses[0] >= 1:
            self.poses[0] -= 1.2

        if (self.frame_cnt & 1) == 0:
            self.poses[1] = self.poses[0]
            if (self.frame_cnt & 3) == 0:
                self.poses[2] = self.poses[0]

    @staticmethod
    def rect2quad(x, y, sz):
        return [x, y, x+sz, y, x+sz, y+sz, x, y+sz]

    def on_draw(self):
        pyglet.clock.tick()
        x0, x1, x2 = self.poses
        y0, y1, y2 = 0.1, 0.4, 0.7
        sz = 0.2

        data = self.rect2quad(x0, y0, sz)
        data.extend(self.rect2quad(x1, y1, sz))
        data.extend(self.rect2quad(x2, y2, sz))

        glClear(GL_COLOR_BUFFER_BIT)
        pyglet.graphics.draw(len(data) >> 1, pyglet.gl.GL_QUADS, ('v2f', data))
        self.fps_display.draw()

import sys
w = HelloWorldWindow("fps-test", int(sys.argv[1]), 800, 800)
pyglet.app.run()