from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import math

WIDTH, HEIGHT = 800, 600

START_X, START_Y = 145, 105
ballX, ballY = START_X, START_Y
ballR = 17

vx, vy = 0, 0
gravity = 600

shooting = False
dragging = False

mouseX, mouseY = 0, 0

keyboardAiming = False
keyboardPower = 120
keyboardAngle = math.radians(45)

rimX1, rimX2 = 610, 690
rimY = 365

result = ""
resultTimer = 0


def drawCircle(x, y, radius, color, alpha=1):
    glColor4f(color[0], color[1], color[2], alpha)

    glBegin(GL_TRIANGLE_FAN)
    glVertex2f(x, y)

    for i in range(361):
        angle = math.radians(i)
        glVertex2f(
            x + radius * math.cos(angle),
            y + radius * math.sin(angle)
        )

    glEnd()


def drawOutline(x, y, radius, color, width=2):
    glColor3f(*color)
    glLineWidth(width)

    glBegin(GL_LINE_LOOP)

    for i in range(361):
        angle = math.radians(i)
        glVertex2f(
            x + radius * math.cos(angle),
            y + radius * math.sin(angle)
        )

    glEnd()


def drawBackground():
    # Background gradient
    glBegin(GL_QUADS)

    glColor3f(0.12, 0.19, 0.31)
    glVertex2f(0, 600)

    glColor3f(0.27, 0.39, 0.52)
    glVertex2f(800, 600)

    glColor3f(0.52, 0.61, 0.68)
    glVertex2f(800, 65)

    glColor3f(0.35, 0.47, 0.57)
    glVertex2f(0, 65)

    glEnd()

    # Soft background lights
    drawCircle(160, 460, 100, (0.4, 0.65, 0.8), 0.08)
    drawCircle(680, 490, 120, (0.5, 0.7, 0.9), 0.07)

    # Wooden floor
    glBegin(GL_QUADS)

    glColor3f(0.55, 0.28, 0.12)
    glVertex2f(0, 0)
    glVertex2f(800, 0)

    glColor3f(0.88, 0.56, 0.29)
    glVertex2f(800, 65)
    glVertex2f(0, 65)

    glEnd()

    # Floor markings
    glColor4f(1, 0.85, 0.65, 0.25)
    glLineWidth(1)

    glBegin(GL_LINES)

    for x in range(0, 801, 80):
        glVertex2f(x, 0)
        glVertex2f(x, 65)

    glEnd()

    glColor3f(1, 0.88, 0.7)
    glLineWidth(3)

    glBegin(GL_LINES)
    glVertex2f(0, 65)
    glVertex2f(800, 65)
    glEnd()


def drawBall():
    # Ball shadow
    drawCircle(ballX + 5, 69, 22, (0.05, 0.04, 0.03), 0.25)

    # Ball glow
    drawCircle(ballX, ballY, ballR + 8, (1, 0.35, 0.05), 0.13)

    # Ball body
    glBegin(GL_TRIANGLE_FAN)

    glColor3f(1.0, 0.65, 0.18)
    glVertex2f(ballX - 5, ballY + 7)

    glColor3f(0.95, 0.25, 0.01)

    for i in range(361):
        angle = math.radians(i)
        glVertex2f(
            ballX + ballR * math.cos(angle),
            ballY + ballR * math.sin(angle)
        )

    glEnd()

    # Ball outline
    drawOutline(ballX, ballY, ballR, (0.22, 0.08, 0.02), 2)

    # Curved basketball lines
    glColor3f(0.22, 0.08, 0.02)
    glLineWidth(1.8)

    glBegin(GL_LINE_STRIP)

    for i in range(101):
        angle = math.radians(-90 + i * 1.8)
        glVertex2f(
            ballX + 8 * math.cos(angle),
            ballY + ballR * math.sin(angle)
        )

    glEnd()

    glBegin(GL_LINE_STRIP)

    for i in range(101):
        angle = math.radians(-90 + i * 1.8)
        glVertex2f(
            ballX - 8 * math.cos(angle),
            ballY + ballR * math.sin(angle)
        )

    glEnd()

    glBegin(GL_LINE_STRIP)

    for i in range(101):
        angle = math.radians(i * 1.8)
        glVertex2f(
            ballX + ballR * math.cos(angle),
            ballY + 5 * math.sin(angle)
        )

    glEnd()


def drawBasket():
    # Backboard shadow
    glColor4f(0.05, 0.08, 0.12, 0.25)
    glLineWidth(9)

    glBegin(GL_LINE_LOOP)
    glVertex2f(704, 305)
    glVertex2f(704, 425)
    glVertex2f(790, 425)
    glVertex2f(790, 305)
    glEnd()

    # Backboard
    glColor3f(0.95, 0.97, 1)
    glLineWidth(5)

    glBegin(GL_LINE_LOOP)
    glVertex2f(700, 310)
    glVertex2f(700, 420)
    glVertex2f(785, 420)
    glVertex2f(785, 310)
    glEnd()

    # Small rectangle on the backboard
    glColor3f(0.75, 0.83, 0.9)
    glLineWidth(2)

    glBegin(GL_LINE_LOOP)
    glVertex2f(710, 325)
    glVertex2f(710, 365)
    glVertex2f(755, 365)
    glVertex2f(755, 325)
    glEnd()

    # Basket support
    glColor3f(0.35, 0.4, 0.45)
    glLineWidth(8)

    glBegin(GL_LINES)
    glVertex2f(785, 350)
    glVertex2f(800, 350)
    glEnd()

    # Rim glow
    glColor4f(1, 0.2, 0.02, 0.22)
    glLineWidth(12)

    glBegin(GL_LINES)
    glVertex2f(rimX1, rimY)
    glVertex2f(rimX2, rimY)
    glEnd()

    # Basket rim
    glColor3f(1, 0.16, 0.02)
    glLineWidth(5)

    glBegin(GL_LINE_LOOP)

    for i in range(361):
        angle = math.radians(i)
        glVertex2f(
            650 + 40 * math.cos(angle),
            rimY + 7 * math.sin(angle)
        )

    glEnd()

    # Net
    glColor3f(0.96, 0.97, 1)
    glLineWidth(1.6)

    glBegin(GL_LINES)

    for i in range(7):
        x = rimX1 + i * (80 / 6)
        bottomX = 650 + (x - 650) * 0.65

        glVertex2f(x, rimY)
        glVertex2f(bottomX, rimY - 48)

    for i in range(6):
        x1 = rimX1 + i * (80 / 6)
        x2 = rimX1 + (i + 1) * (80 / 6)

        glVertex2f(
            650 + (x1 - 650) * 0.65,
            rimY - 48
        )

        glVertex2f(
            650 + (x2 - 650) * 0.65,
            rimY - 48
        )

    glEnd()


def getShotVelocity():
    if keyboardAiming:
        speed = min(keyboardPower * 5.5, 900)

        return (
            speed * math.cos(keyboardAngle),
            speed * math.sin(keyboardAngle)
        )

    dx = ballX - mouseX
    dy = ballY - mouseY

    distance = math.sqrt(dx ** 2 + dy ** 2)
    speed = min(distance * 5.5, 900)

    angle = math.atan2(dy, dx)

    return (
        speed * math.cos(angle),
        speed * math.sin(angle)
    )


def drawTrajectory():
    if not dragging and not keyboardAiming:
        return

    pvx, pvy = getShotVelocity()

    if pvx <= 0 or pvy <= 0:
        return

    groundY = 65 + ballR

    # Estimate the full flight time
    totalTime = (
        pvy + math.sqrt(
            pvy ** 2 + 2 * gravity * (ballY - groundY)
        )
    ) / gravity

    shortTime = totalTime * 0.20

    # Show only the first part of the path
    glPointSize(5)
    glBegin(GL_POINTS)

    for i in range(1, 16):
        t = shortTime * i / 15

        x = ballX + pvx * t
        y = ballY + pvy * t - 0.5 * gravity * t ** 2

        if y < groundY or x > WIDTH:
            break

        glColor4f(1, 0.9, 0.35, 1 - i / 20)
        glVertex2f(x, y)

    glEnd()

    # Mark the predicted position at basket height
    d = pvy ** 2 - 2 * gravity * (rimY - ballY)

    if d >= 0:
        t = (pvy + math.sqrt(d)) / gravity
        targetX = ballX + pvx * t

        drawCircle(targetX, rimY, 13, (1, 0.9, 0.1), 0.2)
        drawCircle(targetX, rimY, 5, (1, 0.95, 0.1))
        drawOutline(targetX, rimY, 10, (1, 0.95, 0.4), 2)


def drawPowerDot():
    if not dragging and not keyboardAiming:
        return

    # Get the current aiming position
    if keyboardAiming:
        aimX = ballX - keyboardPower * math.cos(keyboardAngle)
        aimY = ballY - keyboardPower * math.sin(keyboardAngle)
    else:
        aimX = mouseX
        aimY = mouseY

    dx = ballX - aimX
    dy = ballY - aimY
    distance = math.sqrt(dx ** 2 + dy ** 2)

    if distance < 65:
        color = (0.2, 0.9, 1)
    elif distance < 120:
        color = (1, 0.85, 0.1)
    else:
        color = (1, 0.25, 0.1)

    # Power indicator
    drawCircle(aimX, aimY, 15, color, 0.2)
    drawCircle(aimX, aimY, 7, color)
    drawOutline(aimX, aimY, 13, color, 2)

    glColor4f(1, 1, 1, 0.3)
    glLineWidth(1.5)

    glBegin(GL_LINES)
    glVertex2f(ballX, ballY)
    glVertex2f(aimX, aimY)
    glEnd()


def drawText(x, y, message, color):
    glColor3f(*color)
    glRasterPos2f(x, y)

    for ch in message:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(ch))


def finishShot(message):
    global shooting, result, resultTimer

    if not shooting:
        return

    shooting = False
    result = message
    resultTimer = 3.0


def resetBall():
    global ballX, ballY, vx, vy
    global shooting, dragging, keyboardAiming
    global keyboardPower, keyboardAngle
    global result, resultTimer

    ballX = START_X
    ballY = START_Y

    vx = 0
    vy = 0

    shooting = False
    dragging = False
    keyboardAiming = False

    keyboardPower = 120
    keyboardAngle = math.radians(45)

    result = ""
    resultTimer = 0


def update(value):
    global ballX, ballY, vx, vy, resultTimer

    dt = 0.016

    if shooting:
        previousX = ballX
        previousY = ballY

        # Apply gravity and move the ball
        vy -= gravity * dt
        ballX += vx * dt
        ballY += vy * dt

        # Check when the ball passes the rim while falling
        if previousY > rimY and ballY <= rimY and vy < 0:
            ratio = (previousY - rimY) / (previousY - ballY)
            crossingX = previousX + (ballX - previousX) * ratio

            # The ball must fit between the two sides of the rim
            if rimX1 + ballR <= crossingX <= rimX2 - ballR:
                finishShot("HIT!")
            else:
                finishShot("MISS!")

        # Check if the ball touches the floor
        if shooting and ballY - ballR <= 65:
            finishShot("MISS!")

        # Check if the ball leaves the window
        if shooting and (
            ballX > WIDTH + ballR
            or ballY > HEIGHT + ballR
            or ballX < -ballR
        ):
            finishShot("MISS!")

    elif result != "":
        resultTimer -= dt

        if resultTimer <= 0:
            resetBall()

    glutPostRedisplay()
    glutTimerFunc(16, update, 0)


def mouseClick(button, state, x, y):
    global dragging, mouseX, mouseY
    global vx, vy, shooting, keyboardAiming

    worldY = HEIGHT - y

    if button == GLUT_LEFT_BUTTON:

        # Start dragging when the ball is clicked
        if state == GLUT_DOWN and not shooting and result == "":
            distance = math.sqrt(
                (x - ballX) ** 2 + (worldY - ballY) ** 2
            )

            if distance <= ballR + 20:
                dragging = True
                keyboardAiming = False
                mouseX = x
                mouseY = worldY

        # Release the mouse to shoot
        elif state == GLUT_UP and dragging:
            mouseX = x
            mouseY = worldY

            vx, vy = getShotVelocity()

            if vx > 0 and vy > 0:
                shooting = True

            dragging = False

    glutPostRedisplay()


def mouseMotion(x, y):
    global mouseX, mouseY

    if dragging:
        mouseX = x
        mouseY = HEIGHT - y
        glutPostRedisplay()


def keyboard(key, x, y):
    global keyboardAiming, keyboardPower, keyboardAngle
    global vx, vy, shooting

    if key == b'r':
        resetBall()

    elif key in (b'w', b's', b'a', b'd'):

        if not shooting and result == "":
            keyboardAiming = True

            if key == b'w':
                keyboardPower = min(keyboardPower + 10, 160)

            elif key == b's':
                keyboardPower = max(keyboardPower - 10, 30)

            elif key == b'a':
                keyboardAngle = max(
                    keyboardAngle - math.radians(3),
                    math.radians(15)
                )

            elif key == b'd':
                keyboardAngle = min(
                    keyboardAngle + math.radians(3),
                    math.radians(75)
                )

    elif key == b' ':

        if keyboardAiming and not shooting and result == "":
            vx, vy = getShotVelocity()

            if vx > 0 and vy > 0:
                shooting = True
                keyboardAiming = False

    elif key == b'\x1b':
        glutLeaveMainLoop()

    glutPostRedisplay()


def showScreen():
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()

    drawBackground()
    drawBasket()
    drawTrajectory()
    drawPowerDot()
    drawBall()

    # Display the shot result
    if result == "HIT!":
        drawText(370, 510, "HIT!", (0.1, 1, 0.2))

    elif result == "MISS!":
        drawText(365, 510, "MISS!", (1, 0.15, 0.1))

    elif not shooting:
        drawText(
            270, 550,
            "Drag to shoot | WASD aim | SPACE shoot",
            (1, 1, 1)
        )

    glutSwapBuffers()


def init():
    glClearColor(0.12, 0.19, 0.31, 1)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, WIDTH, 0, HEIGHT, -1, 1)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    glShadeModel(GL_SMOOTH)

    # Enable transparency for glow effects
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    # Smooth out the lines
    glEnable(GL_LINE_SMOOTH)
    glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)


def main():
    glutInit()
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE)
    glutInitWindowSize(WIDTH, HEIGHT)
    glutInitWindowPosition(200, 100)

    glutCreateWindow(b"Basketball Shooting Game")

    init()

    glutDisplayFunc(showScreen)
    glutMouseFunc(mouseClick)
    glutMotionFunc(mouseMotion)
    glutKeyboardFunc(keyboard)

    glutTimerFunc(16, update, 0)
    glutMainLoop()


main()