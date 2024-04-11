from turtle import *
from time import time
import math
tracer(0)
speed(0)
colormode(255)
def sine(a):
    return math.sin(math.radians(a))
def cosine(a):
    return math.cos(math.radians(a))
def hex_to_rgb(hex_color):
  hex_color = hex_color.lstrip('#')
  return list(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))

def fakeline(x1, y1, z1, x2, y2, z2, points):
    global X1, Y1, Z1, X2, Y2, Z2
    setpoint1((x1 - cam_x), (y1 - cam_y), (z1 - cam_z))
    setpoint2((x2 - cam_x), (y2 - cam_y), (z2 - cam_z))
    setpoint1((Z1 * cam_dir_y_sin) + (X1 * cam_dir_y_cos), Y1, (Z1 * cam_dir_y_cos) - (X1 * cam_dir_y_sin))
    setpoint2((Z2 * cam_dir_y_sin) + (X2 * cam_dir_y_cos), Y2, (Z2 * cam_dir_y_cos) - (X2 * cam_dir_y_sin))
    setpoint1(X1, (Y1 * cam_dir_x_cos) - (Z1 * cam_dir_x_sin), (Y1 * cam_dir_x_sin) + (Z1 * cam_dir_x_cos))
    setpoint2(X2, (Y2 * cam_dir_x_cos) - (Z2 * cam_dir_x_sin), (Y2 * cam_dir_x_sin) + (Z2 * cam_dir_x_cos))
    if (Z1 < near_plane) and (Z2 < near_plane):
        return []
    else:
        z_clipping()
        try:
            points.append(view_factor * (X1/Z1))
            points.append(view_factor * (Y1/Z1))
            points.append(view_factor * (X2/Z2))
            points.append(view_factor * (Y2/Z2))
        except:
            pass
        return points
def line(x1, y1, x2, y2):
        penup()
        goto(x1, y1)
        pendown()
        goto(x2, y2)
        penup()
def drawtriangle(dist, x1, y1, z1, x2, y2, z2, x3, y3, z3, color, pcolor=""):
    color = hex_to_rgb(color)
    pcolor = hex_to_rgb(pcolor)
    if dist > 150:
        factor = 150 / dist
    else:
        factor = 1
    color[0] = int(color[0] * factor)
    color[1] = int(color[1] * factor)
    color[2] = int(color[2] * factor)
    pcolor[0] = int(pcolor[0] * factor)
    pcolor[1] = int(pcolor[1] * factor)
    pcolor[2] = int(pcolor[2] * factor)
    fillcolor(color)
    if pcolor != "":
        pencolor(pcolor)
    points = fakeline(x1, y1, z1, x2, y2, z2, [])
    points = fakeline(x2, y2, z2, x3, y3, z3, points)
    points = fakeline(x3, y3, z3, x1, y1, z1, points)
    points = fakeline(x1, y1, z1, x2, y2, z2, points)
    i = 0
    if points != None:
        n = len(points)
    else:
        n = 0
    begin_fill()
    while i < n:
        pensize(2)
        line(points[i % n], points[(i + 1) % n], points[(i + 2) % n], points[(i + 3) % n])
        i += 2
    end_fill()
def addtriangle(x1, y1, z1, x2, y2, z2, x3, y3, z3, color, pcolor=""):
    i = 0
    x_avg = (x1 + x2 + x3) / 3
    y_avg = (y1 + y2 + y3) / 3
    z_avg = (z1 + z2 + z3) / 3
    dist = float((((x_avg - cam_x) ** 2) + ((y_avg - cam_y) ** 2) + ((z_avg - cam_z) ** 2)) ** 0.5)
    while dist < triangles[i][0]:
        i += 1
    triangles.insert(i, [dist, x1, y1, z1, x2, y2, z2, x3, y3, z3, color, pcolor])
def draw():
    global triangles
    while len(triangles) > 2:
            drawtriangle(triangles[1][0], triangles[1][1], triangles[1][2], triangles[1][3], triangles[1][4], triangles[1][5], triangles[1][6], triangles[1][7], triangles[1][8], triangles[1][9], triangles[1][10], triangles[1][11])
            triangles.pop(1)
    pencolor("#FFFFFF")
    pensize(8)
    penup()
    goto(30, 0)
    pendown()
    goto(7, 0)
    penup()
    goto(-30, 0)
    pendown()
    goto(-7, 0)
    penup()
    goto(0, 30)
    pendown()
    goto(0, 7)
    penup()
    goto(0, -30)
    pendown()
    goto(0, -7)
    pencolor("#808080")
    pensize(3)
    penup()
    goto(30, 0)
    pendown()
    goto(7, 0)
    penup()
    goto(-30, 0)
    pendown()
    goto(-7, 0)
    penup()
    goto(0, 30)
    pendown()
    goto(0, 7)
    penup()
    goto(0, -30)
    pendown()
    goto(0, -7)
    penup()
    update()
def z_clipping():
    if (Z1 < near_plane) or (Z2 < near_plane):
        percent = (near_plane - Z1)/(Z2 - Z1)
        if Z1 < near_plane:
            setpoint1((X1 + ((X2 - X1) * percent)), (Y1 + ((Y2 - Y1) * percent)), near_plane)
        elif Z2 < near_plane:
            setpoint2((X1 + ((X2 - X1) * percent)), (Y1 + ((Y2 - Y1) * percent)), near_plane)
def setpoint1(x1, y1, z1):
    global X1, Y1, Z1
    X1 = float(x1)
    Y1 = float(y1)
    Z1 = float(z1)
def setpoint2(x2, y2, z2):
    global X2, Y2, Z2
    X2 = float(x2)
    Y2 = float(y2)
    Z2 = float(z2)
cam_x, cam_y, cam_z = 0, 0, 0
cam_dir_x, cam_dir_y = 0, 0
view_factor, near_plane = 500, 1
triangles = [[math.inf],[0 - math.inf]]
keysPressed = {
    'up' : False,
    'down' : False,
    'left' : False,
    'right' : False,
    'y' : False,
    'b' : False,
    'w' : False,
    'a' : False,
    's' : False,
    'd' : False
}
def UP():
    global keysPressed
    keysPressed["w"] = True
def NO_UP():
    global keysPressed
    keysPressed["w"] = False
def DOWN():
    global keysPressed
    keysPressed["s"] = True
def NO_DOWN():
    global keysPressed
    keysPressed["s"] = False
def LEFT():
    global keysPressed
    keysPressed["a"] = True
def NO_LEFT():
    global keysPressed
    keysPressed["a"] = False
def RIGHT():
    global keysPressed
    keysPressed["d"] = True
def NO_RIGHT():
    global keysPressed
    keysPressed["d"] = False
def MUP():
    global keysPressed
    keysPressed["y"] = True
def NO_MUP():
    global keysPressed
    keysPressed["y"] = False
def MDOWN():
    global keysPressed
    keysPressed["b"] = True
def NO_MDOWN():
    global keysPressed
    keysPressed["b"] = False
    
def TUP():
    global keysPressed
    keysPressed["up"] = True
def NO_TUP():
    global keysPressed
    keysPressed["up"] = False
def TDOWN():
    global keysPressed
    keysPressed["down"] = True
def NO_TDOWN():
    global keysPressed
    keysPressed["down"] = False
def TLEFT():
    global keysPressed
    keysPressed["left"] = True
def NO_TLEFT():
    global keysPressed
    keysPressed["left"] = False
def TRIGHT():
    global keysPressed
    keysPressed["right"] = True
def NO_TRIGHT():
    global keysPressed
    keysPressed["right"] = False
listen()
onkeypress(UP, "w")
onkeyrelease(NO_UP, "w")
onkeypress(DOWN, "s")
onkeyrelease(NO_DOWN, "s")
onkeypress(LEFT, "a")
onkeyrelease(NO_LEFT, "a")
onkeypress(RIGHT, "d")
onkeyrelease(NO_RIGHT, "d")
onkeypress(MUP, "y")
onkeyrelease(NO_MUP, "y")
onkeypress(MDOWN, "b")
onkeyrelease(NO_MDOWN, "b")
lastTick = 0
delta = 1
def deltatiming():
    global delta
    global lastTick
    delta = (time() * 120) - lastTick
    lastTick = time() * 120
onkeypress(TUP, "Up")
onkeyrelease(NO_TUP, "Up")
onkeypress(TDOWN, "Down")
onkeyrelease(NO_TDOWN, "Down")
onkeypress(TLEFT, "Left")
onkeyrelease(NO_TLEFT, "Left")
onkeypress(TRIGHT, "Right")
onkeyrelease(NO_TRIGHT, "Right")
bgcolor("black")
while True:
    clear()
    penup()
    hideturtle()
    cam_dir_y_sin = sine(cam_dir_y)
    cam_dir_y_cos = cosine(cam_dir_y)
    cam_dir_x_sin = sine(cam_dir_x)
    cam_dir_x_cos = cosine(cam_dir_x)
    if keysPressed["w"]:
        cam_z += (2 * cam_dir_y_cos) * delta
        cam_x -= (2 * cam_dir_y_sin) * delta
    if keysPressed["s"]:
        cam_z -= (2 * cam_dir_y_cos) * delta
        cam_x += (2 * cam_dir_y_sin) * delta
    if keysPressed["a"]:
        cam_z -= (2 * cam_dir_y_sin) * delta
        cam_x -= (2 * cam_dir_y_cos) * delta
    if keysPressed["d"]:
        cam_z += (2 * cam_dir_y_sin) * delta
        cam_x += (2 * cam_dir_y_cos) * delta
    if keysPressed["y"]:
        cam_y += 2 * delta
    if keysPressed["b"]:
        cam_y -= 2 * delta
    triangles = [[math.inf],[0 - math.inf]]
    if keysPressed["up"]:
        cam_dir_x += 1 * delta
    if keysPressed["down"]:
        cam_dir_x -= 1 * delta
    if keysPressed["left"]:
        cam_dir_y += 1 * delta
    if keysPressed["right"]:
        cam_dir_y -= 1 * delta
    
    addtriangle(-50, 50, 300, -50, -50, 300, 0, 0, 300, "#FF8E55", "#FF8E55")
    addtriangle(50, 50, 300, 50, -50, 300, 0, 0, 300, "#FF8E55", "#FF8E55")
    addtriangle(-50, 50, 300, 50, 50, 300, 0, 0, 300, "#FF8E55", "#FF8E55")
    addtriangle(-50, -50, 300, 50, -50, 300, 0, 0, 300, "#FF8E55", "#FF8E55")
    
    addtriangle(-50, 50, 200, -50, -50, 200, 0, 0, 200, "#FF0000", "#FF0000")
    addtriangle(50, 50, 200, 50, -50, 200, 0, 0, 200, "#FF0000", "#FF0000")
    addtriangle(-50, 50, 200, 50, 50, 200, 0, 0, 200, "#FF0000", "#FF0000")
    addtriangle(-50, -50, 200, 50, -50, 200, 0, 0, 200, "#FF0000", "#FF0000")
    
    addtriangle(-50, 50, 200, -50, 50, 300, -50, 0, 250, "#00FF00", "#00FF00")
    addtriangle(-50, -50, 200, -50, -50, 300, -50, 0, 250, "#00FF00", "#00FF00")
    addtriangle(-50, 50, 200, -50, -50, 200, -50, 0, 250, "#00FF00", "#00FF00")
    addtriangle(-50, 50, 300, -50, -50, 300, -50, 0, 250, "#00FF00", "#00FF00")
    
    addtriangle(50, 50, 200, 50, 50, 300, 50, 0, 250, "#0000FF", "#0000FF")
    addtriangle(50, -50, 200, 50, -50, 300, 50, 0, 250, "#0000FF", "#0000FF")
    addtriangle(50, 50, 200, 50, -50, 200, 50, 0, 250, "#0000FF", "#0000FF")
    addtriangle(50, 50, 300, 50, -50, 300, 50, 0, 250, "#0000FF", "#0000FF")
    
    addtriangle(50, 50, 200, 50, 50, 300, 0, 50, 250, "#FFFF00", "#FFFF00")
    addtriangle(-50, 50, 200, -50, 50, 300, 0, 50, 250, "#FFFF00", "#FFFF00")
    addtriangle(50, 50, 200, -50, 50, 200, 0, 50, 250, "#FFFF00", "#FFFF00")
    addtriangle(50, 50, 300, -50, 50, 300, 0, 50, 250, "#FFFF00", "#FFFF00")
    
    addtriangle(50, -50, 200, 50, -50, 300, 0, -50, 250, "#732BF5", "#732BF5")
    addtriangle(-50, -50, 200, -50, -50, 300, 0, -50, 250, "#732BF5", "#732BF5")
    addtriangle(50, -50, 200, -50, -50, 200, 0, -50, 250, "#732BF5", "#732BF5")
    addtriangle(50, -50, 300, -50, -50, 300, 0, -50, 250, "#732BF5", "#732BF5")
    draw()
    deltatiming()
