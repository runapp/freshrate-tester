#!/usr/bin/env python3
import pyglet
from pyglet.gl import *
import pyglet.window.key as keys


class HelloWorldWindow(pyglet.window.Window):
    def __init__(self, name, fps, fpses, width=None, height=None):
        super(HelloWorldWindow, self).__init__(width=width, height=height, vsync=False)
        # Run "self.update" 128 frames a second and set FPS limit to 128.
        pyglet.clock.schedule_interval(self.update, 1.0/fps)
        pyglet.clock.set_fps_limit(fps)
        self.name = name
        self.fps_display = pyglet.window.FPSDisplay(self)
        self.fps = fps
        self.fpses = fpses
        self.dt_limits = [1./i for i in self.fpses]
        self.dt_cnt = [0.]*len(fpses)
        self.pos = 0
        self.poses = [0.]*len(fpses)
        self.frame_cnt = 0

        self.sz = 0.08
        self.ypos = [0.05+i*((0.9-self.sz)/(len(fpses)-1)) for i in range(len(fpses))]

        self.right_limit = 1+self.sz/2
        self.length = 1.01+self.sz
        self.dt_scale = 0.5*self.length

        glClearColor(0.0, 0.0, 0.0, 1.0)
        glEnableClientState(GL_VERTEX_ARRAY)

    def update(self, dt):
        self.frame_cnt = (self.frame_cnt+1) & 0xffff
        dx = dt*self.dt_scale
        self.pos += dx
        if self.pos >= 1:
            self.pos -= self.length

        for i, dt_limit in enumerate(self.dt_limits):
            self.dt_cnt[i] += dt
            if self.dt_cnt[i] > dt_limit:
                self.dt_cnt[i] -= dt_limit
                self.poses[i] = self.pos

    def rect2quad(self, x, y, sz):
        w, h = self.width, self.height
        return [x*w, y*h, (x+sz)*w, y*h, (x+sz)*w, (y+sz)*h, x*w, (y+sz)*h]

    def on_draw(self):
        pyglet.clock.tick()
        data = []
        for x, y in zip(self.poses, self.ypos):
            data.extend(self.rect2quad(x, y, self.sz))

        glClear(GL_COLOR_BUFFER_BIT)
        pyglet.graphics.draw(len(data) >> 1, pyglet.gl.GL_QUADS, ('v2f', data))
        self.fps_display.draw()


import sys
fps = 120 if len(sys.argv) < 2 else int(sys.argv[1])
fpses = [2, 4, 5, 6, 8, 10, 12, 120]
w = HelloWorldWindow("fps-test", fps, fpses, 800, 800)

pyglet.app.run()
