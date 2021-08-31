# SCC0250 - Computacao grafica
# 2021/1, turma B
# Exercicio pratico 2, item 1
# Luis Filipe Vasconcelos Peres
# 10310641
# github.com/lfvperes/computer-graphics

'''
2 - Praticando transformacoes geometricas no OpenGL
2.1 - Faca um programa que desenhe um triangulo e aplique transformacao 
geometrica de escala uniforme conforme o seguinte:
* Aumentar o tamanho apos clicar no botao esquerdo do mouse
* Diminuir o tamanho apos clicar no botao direito do mouse
'''

# basic setup
import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np

# init window
w = 720
h = 600

glfw.init()
glfw.window_hint(glfw.VISIBLE, glfw.FALSE)
window = glfw.create_window(w, h, "exercicio-2.1", None, None)
glfw.make_context_current(window)

# vertex shader
vertex_code = """
    attribute vec2 position;
    uniform mat4 mat_transformation;
    void main(){
        gl_Position = mat_transformation * vec4(position, 0.0, 1.0);
    }
"""

# fragment shader
fragment_code = """
    uniform vec4 color;
    void main(){
        gl_FragColor = color;
    }
"""

# request GPU slots
program = glCreateProgram()
vertex = glCreateShader(GL_VERTEX_SHADER)
fragment = glCreateShader(GL_FRAGMENT_SHADER)

# shaders source
glShaderSource(vertex, vertex_code)
glShaderSource(fragment, fragment_code)

# compile shaders
# vertex shader
glCompileShader(vertex)
if not glGetShaderiv(vertex, GL_COMPILE_STATUS):
    error = glGetShaderInfoLog(vertex).decode()
    print(error)
    raise RuntimeError("Erro de compilacao do Vertex Shader")
# fragment shader
glCompileShader(fragment)
if not glGetShaderiv(fragment, GL_COMPILE_STATUS):
    error = glGetShaderInfoLog(fragment).decode()
    print(error)
    raise RuntimeError("Erro de compilacao do Fragment Shader")

# attach objs
glAttachShader(program, vertex)
glAttachShader(program, fragment)

# build
glLinkProgram(program)
if not glGetProgramiv(program, GL_LINK_STATUS):
    print(glGetProgramInfoLog(program))
    raise RuntimeError('Linking error')

# make default
glUseProgram(program)

# organize GPU space
N = 3   # 3 vertices w/ 2 coordinates
vertices = np.zeros(N, [("position", np.float32, 2)])
vertices['position'] = [
    ( 0.0, +0.5),
    (-0.5, -0.5),
    (+0.5, -0.5)
]

# request buffer slot from GPU
buffer = glGenBuffers(1)
# make default
glBindBuffer(GL_ARRAY_BUFFER, buffer)

# upload data
glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_DYNAMIC_DRAW)
glBindBuffer(GL_ARRAY_BUFFER, buffer)

# bind positions
stride = vertices.strides[0]
offset = ctypes.c_void_p(0)

loc = glGetAttribLocation(program, "position")
glEnableVertexAttribArray(loc)

glVertexAttribPointer(loc, 2, GL_FLOAT, False, stride, offset)

# color variable location
loc_color = glGetUniformLocation(program, "color")
R = 1.0
G = 0.0
B = 0.0

# mouse events affecting transformation matrix
s = 1

def mouse_event(window, button, action, mods):
    global s

    # at release (action 0)
    if button == 0 and action == 0: s += 0.1  # increase w/ left button
    if button == 1 and action == 0:           # diminish w/ right button
        s -= 0.1 if s > 0.1 else s            # avoid negative scale

glfw.set_mouse_button_callback(window, mouse_event)

glfw.show_window(window)

while not glfw.window_should_close(window):
    glfw.poll_events()

    glClear(GL_COLOR_BUFFER_BIT)
    glClearColor(1.0, 1.0, 1.0, 1.0)

    mat_scaling = np.array([
          s, 0.0, 0.0,   0,
        0.0,   s, 0.0,   0,
        0.0, 0.0, 1.0, 0.0,
        0.0, 0.0, 0.0, 1.0,
    ], np.float32)

    loc = glGetUniformLocation(program, "mat_transformation")
    glUniformMatrix4fv(loc, 1, GL_TRUE, mat_scaling)

    glDrawArrays(GL_TRIANGLES, 0, len(vertices))
    glUniform4f(loc_color, R, G, B, 1.0)

    glfw.swap_buffers(window)

glfw.terminate()