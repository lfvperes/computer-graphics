# SCC0250 - Computacao grafica
# 2021/1, turma B
# Exercicio pratico 1
# Luis Filipe Vasconcelos Peres
# 10310641
# github.com/lfvperes/computer-graphics

import glfw, math
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np

# initializing window
glfw.init()
glfw.window_hint(glfw.VISIBLE, glfw.FALSE)
window = glfw.create_window(600, 600, "Exercício prático 1 - Luis F. V. Peres - MINERVA CAASO", None, None)
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
    uniform vec4 color;
    void main(){
        gl_FragColor = color;
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

minerva = np.multiply(
    ([
        # triangle strip (quadrilateral) - black
        (294, 125),     # 0
        (294, 177),     # 1
        (102, 232),     # 3
        (115, 273),     # 2

        # triangle strip - black
        (157, 375),     # 8
        (286, 375),     # 7
        (120, 279),     # 9
        (286, 298),     # 6
        (294, 184),     # 4
        (467, 298),     # 5

        # triangle strip - white
        (179, 431),     # 16
        (157, 375),     # 8
        (273, 467),     # 15
        (286, 375),     # 7
        (306, 408),     # 14
        (286, 298),     # 6
        (387, 408),     # 13

        # triangle strip - white
        (387, 408),     # 13
        (286, 298),     # 6
        (387, 366),     # 12
        (409, 298),     # 10
        (409, 366),     # 11

        # line strip - black
        (409, 298),     # 10
        (409, 366),     # 11
        (387, 366),     # 12
        (387, 408),     # 13
        (306, 408),     # 14
        (273, 467),     # 15
        (179, 431),     # 16
        (157, 375),     # 8

        # line - black
        (353, 319),     # 17
        (375, 319),     # 18

        # align and normalize
    ] - np.repeat([(270, 280)], 32, axis=0)), 
[1/500, -1/500])

yellow_square = [
    # triangle strip (square) - yellow
    ( 0.8, 0.8),
    (-0.8, 0.8),
    ( 0.8,-0.8),
    (-0.8,-0.8)
]

dots = [
    # vertices - yellow
    ( 0.6, 0.6),
    (-0.6, 0.6),
    ( 0.6,-0.6),
    (-0.6,-0.6)
]

# parameters for circle
num_circle_vertices = 64
pi = 3.14
counter = 0
radius = 0.6
angle = 0.0 

circle = np.zeros((num_circle_vertices,2))

for counter in range(num_circle_vertices):
    angle += 2 * pi / num_circle_vertices 
    x = math.cos(angle) * radius
    y = math.sin(angle) * radius
    circle[counter] = [x,y]

# preparing space for 3 two-dimensional vertices
vertices = np.zeros(
    len(minerva) + len(yellow_square) + len(dots) + len(circle), 
    [("position", np.float32, 2)])

# filling coordinates
vertices['position'] = np.concatenate(
    (minerva, yellow_square, dots, circle),
    axis=0)

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

# store 'position' location from the GPU
loc = glGetAttribLocation(program, "position")
glEnableVertexAttribArray(loc)

# indicate location
glVertexAttribPointer(loc, 2, GL_FLOAT, False, stride, offset)

glfw.show_window(window)

loc_color = glGetUniformLocation(program, "color")
# window main loop
while not glfw.window_should_close(window):

    glfw.poll_events()

    glClear(GL_COLOR_BUFFER_BIT)
    glClearColor(1.0, 1.0, 1.0, 1.0)

    # black
    glUniform4f(loc_color, 0.0, 0.0, 0.0, 1.0)
    glDrawArrays(GL_TRIANGLE_STRIP, 32, 4)  # SQUARE
    
    # yellow
    glUniform4f(loc_color, 1.0, 1.0, 0.0, 1.0)
    glDrawArrays(GL_TRIANGLE_FAN, 41, 64)   # CIRCLE

    # black 
    glUniform4f(loc_color, 0.0, 0.0, 0.0, 1.0)
    glDrawArrays(GL_TRIANGLE_STRIP, 0, 4)   # TRIANGLES
    glDrawArrays(GL_TRIANGLE_STRIP, 4, 6)

    # white 
    glUniform4f(loc_color, 1.0, 1.0, 1.0, 1.0)
    glDrawArrays(GL_TRIANGLE_STRIP, 10, 7)  # TRIANGLES
    glDrawArrays(GL_TRIANGLE_STRIP, 17, 5)
    glDrawArrays(GL_POINTS, 36, 4)          # VERTEX

    # black 
    glUniform4f(loc_color, 0.0, 0.0, 0.0, 1.0)
    glDrawArrays(GL_LINE_STRIP, 22, 8)      # LINES
    glDrawArrays(GL_LINES, 30, 2)


    glfw.swap_buffers(window)

glfw.terminate()
