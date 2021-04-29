# SCC0250 - Computacao grafica
# 2021/1
# Exercicio pratico 1
# github.com/lfvperes/computer-graphics

import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np

# initializing window
glfw.init()
glfw.window_hint(glfw.VISIBLE, glfw.FALSE)
window = glfw.create_window(720, 600, "Pontos", None, None)
glfw.make_context_current(window)

# event capture callbacks
def key_event(window,key,scancode,action,mods):
    print('[key event] key=',key)
    print('[key event] scancode=',scancode)
    print('[key event] action=',action)
    print('[key event] mods=',mods)
    print('-------')
    
def mouse_event(window,button,action,mods):
    print('[mouse event] button=',button)
    print('[mouse event] action=',action)
    print('[mouse event] mods=',mods)
    print('-------')

glfw.set_key_callback(window,key_event)
glfw.set_mouse_button_callback(window,mouse_event)

# vertex shader, vertices coordinates
vertex_code = """
    attribute vec2 position;
    void main(){
        gl_Position = vec4(position,0.0,1.0);
    }
"""
# fragment shader, fragment colors
fragment_code = """
    void main(){
        gl_FragColor = vec4(0.0,0.0,0.0,1.0);
    }
"""

# requesting slots from GPU
program = glCreateProgram()
vertex = glCreateShader(GL_VERTEX_SHADER)
fragment = glCreateShader(GL_FRAGMENT_SHADER)
# link sources
glShaderSource(vertex, vertex_code)
glShaderSource(fragment, fragment_code)

# compiling vertex shader
glCompileShader(vertex)
if not glGetShaderiv(vertex, GL_COMPILE_STATUS):
    err = glGetShaderInfoLog(vertex).decode()
    print(err)
    raise RuntimeError("Erro de compilacao no Vertex Shader")

# compiling fragment shader
glCompileShader(fragment)
if not glGetShaderiv(fragment, GL_COMPILE_STATUS):
    err = glGetShaderInfoLog(fragment).decode()
    print(err)
    raise RuntimeError("Erro de compilcao do Fragment Shader")

# attaching compiled objects to main 
glAttachShader(program, vertex)
glAttachShader(program, fragment)

# linking program
glLinkProgram(program)
if not glGetProgramiv(program, GL_LINK_STATUS):
    print(glGetProgramInfoLog(program))
    raise RuntimeError('Linking error')

glUseProgram(program)   # make default

# preparing space for 3 two-dimensional vertices
vertices = np.zeros(3, [("position", np.float32, 2)])

# filling coordinates
vertices['position'] = [
    ( 0.0,  0.0),       # vertex 0    
    (+0.5, +0.5),       # vertex 1    
    (-0.5, -0.5)        # vertex 2
]

# request buffer slot from GPU
buffer = glGenBuffers(1)
# make default
glBindBuffer(GL_ARRAY_BUFFER, buffer)

# upload vertices data
glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_DYNAMIC_DRAW)
glBindBuffer(GL_ARRAY_BUFFER, buffer)

# defining initial byte and data offset
stride = vertices.strides[0]
offset = ctypes.c_void_p(0)

# request 'position' location in the GPU
loc = glGetAttribLocation(program, "position")
glEnableVertexAttribArray(loc)

# indicate location
glVertexAttribPointer(loc, 2, GL_FLOAT, False, stride, offset)

glfw.show_window(window)

# window main loop
while not glfw.window_should_close(window):

    glfw.poll_events()

    glClear(GL_COLOR_BUFFER_BIT)
    glClearColor(1.0, 1.0, 1.0, 1.0)

    # drawing vertices
    glDrawArrays(GL_POINTS, 0, 3)

    glfw.swap_buffers(window)

glfw.terminate()
