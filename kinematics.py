from math import asin, sin, cos, tan, radians, acos, degrees

g = 9.81


# обработатьь отрицательные случаи

def y(h, v0, t):
    return h + v0*t - g*t*t/2


def x(v0, a, tf):
    a = radians(a)
    return v0*cos(a)*tf


def find_tf(h, v0, a):
    a = radians(a)
    return (v0*sin(a) + (2*g*h + v0*v0*sin(a)*sin(a))**0.5)/g


def find_Hmax(h, v0, a):
    a = radians(a)
    return h + v0*v0*sin(a)*sin(a)/2/g


def find_v0y(h, tf):
    return g*tf/2 - h/2


def find_v0y_from_H(h, H, a):
    return (2*g*(H-h))**0.5/sin(a)


def find_h(v0, tf):
    return g*tf*tf/2 - v0*tf


def find_h_from_H(v0, H):
    return H - v0*v0/2/g


def find_v0_from_tf(tf, H):
    return 2*g*tf + (2*g*H)**0.5


def v0_from_H_a_h(H, a, h):
    a = radians(a)
    return (2 * g * (H - h)) ** 0.5 / sin(a)


def v0_from_h_a_tf(h, a, t):
    a = radians(a)
    return g*t/2/sin(a) - h/sin(a)/t


def vo_from_S_a_tf(S, a, tf):
    a = radians(a)
    return S/cos(a)/tf


def v0_from_H_a_tf(H, a, t):
    a = radians(a)
    return (g*t - (2*g*H)**0.5)/sin(a)


def v0_from_H_a_S(H, a, S):
    a = radians(a)
    return ((2*cos(a)**2*g*H + 2*g*S*sin(2*a))**0.5 - cos(a)*(2*g*H)**0.5) / sin(2*a)


def v0_from_h_tf_S(h, t, S):
    return (S*S*(g*t*t-2*h)**2 + 4*t**4)**0.5/t/S


def v0_from_S_a_h(S, a, h):
    a = radians(a)
    return ((cos(a)**2 * h**2 + 10 * S**3 * sin(2*a))**0.5 - cos(a)*h)/S/sin(2*a)


def h_from_v0_H_a(v0, H, a):
    a = radians(a)
    h = H - v0*v0*sin(a)*sin(a)/2/g
    if h < 1:
        return 0
    else:
        return h


def h_from_v0_S_a(v0, S, a):
    a = radians(a)
    h = g*S**2/(2*v0**2*cos(a)**2) - tan(a)*S
    if h < 1:
        return 0
    else:
        return h


def h_from_H_tf(H, t):
    h = ((32*g*t*t*H)**0.5 - 2*g*t*t)/4
    if h < 1:
        return 0
    else:
        return h


def h_from_v0_tf_a(v0, t, a):
    a = radians(a)
    h = (g*t*t - 2*v0*sin(a)*t)/2
    if h < 1:
        return 0
    else:
        return h


def alpha_from_H_tf_h(H, tf, h):
    return asin((2*g*(H-h))**0.5 + (2*g*H)**0.5)/tf/g


def alpha_from_H_h_v0(H, h, v0):
    return degrees(asin((2*g*(H-h))**0.5 / v0))


def alpha_from_S_tf_v0(S, t, v0):
    return degrees(acos(S/v0/t))
