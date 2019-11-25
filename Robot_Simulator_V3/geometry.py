# Funktionen zur Berechnung von geometrischen Aufgabenstellungen in 2D wie
# Abstand Punkt-Punkt, Punkt-Gerade, Punkt-Segment und
# Schnittpunkte von Geraden, Segmenten und Strahlen.
#
# Geometrische Objekte als Python-Tupel:
#
# + Punkt: p = (x,y)
#
# + Gerade: line = ((x1,y1), (x2,y2)). In 2-Punkt-Form.
#
# + Segment: seg = ((x1,y1), (x2,y2))
#
# + Strahl: ray = ((x,y), theta). Punkt und Richtung theta in rad.
#
# O. Bittel; 11.09.2019; Python 3.5


import math


# Distanz von Punkt p zu Punkt q
def dist(p, q):
    (x1,y1) = p
    (x2,y2) = q
    dx = x1 - x2
    dy = y1 - y2
    return math.sqrt(dx * dx + dy * dy)


# Distanz von Punkt p zur Geraden line.
# Beachte: Distanz ist vorzeichenbehaftet.
# Falls p in derselben Halbebene liegt wie der Ursprung, ist d negativ sonst positiv.
def distPointLineWithSign(p, line):
    (px,py) = p
    ((vx, vy), (wx, wy)) = line  # line definiert durch Punkte v und w

    # Hessesche Normalform für Gerade line bestimmen und damit Abstand berechnen.
    # ax + by = c mit a^2 + b^2 = 1 und c >= 0
    # Siehe https://de.wikipedia.org/wiki/Hessesche_Normalform
    dx = wx - vx
    dy = wy - vy
    l = math.sqrt(dx * dx + dy * dy)
    c = vy*dx - vx*dy
    sign = 1
    if c < 0:
        sign = -1
    a = -sign*dy/l
    b = sign*dx/l
    c = sign*c/l
    return a*px + b*py - c


# Liefert Vektor n,
# wobei n senkrecht zur Geraden g ist und
# n in Richtung g zeigt und
# die Länge von n gleich dem Abstand von p zu g ist.
def normalToLine(p, line):
    (px,py) = p
    ((vx, vy), (wx, wy)) = line  # line definiert durch Punkte v und w

    # Hessesche Normalform für Gerade line bestimmen und damit Abstand berechnen.
    # ax + by = c mit a^2 + b^2 = 1 und c >= 0
    # Siehe https://de.wikipedia.org/wiki/Hessesche_Normalform
    dx = wx - vx
    dy = wy - vy
    l = math.sqrt(dx * dx + dy * dy)
    c = vy*dx - vx*dy
    sign = 1
    if c < 0:
        sign = -1
    a = -sign*dy/l
    b = sign*dx/l
    c = sign*c/l
    dist = a*px + b*py - c
    return (-dist*a, -dist*b)


# Distanz von Punkt p zum Segment seg.
def distPointSegment(p, seg):
    (px,py) = p
    ((vx, vy), (wx, wy)) = seg  # seg definiert durch Punkte v und w
    dx = wx - vx
    dy = wy - vy
    ip = intersectLineSegment((p,(px+dy,py-dx)), seg)
    if ip is None:
        # print "ip = None: "
        d1 = dist(p,(vx, vy))
        d2 = dist(p,(wx, wy))
        if d1 <= d2:
            return d1
        else:
            return d2
    else:
        return dist(p,ip)


# Liefert Punkt q auf einer Geraden line, der am nächsten zum Punkt p liegt.
def neareastPointOnLine(p, line):
    (px, py) = p
    ((vx, vy), (wx, wy)) = line  # seg definiert durch Punkte v und w
    dx = wx - vx
    dy = wy - vy
    line_p = (p,(px+dy,py-dx))
    return intersectLines(line, line_p)


# Schnittpunkt zweier Geraden.
# Bei Parallelität wird None zurückgeliefert.
def intersectLines(line1, line2):
    ((px,py),(qx,qy)) = line1 # line1 definiert durch Punkte p und q
    ((vx,vy),(wx,wy)) = line2 # line2 definiert durch Punkte v und w
    dx1 = qx - px
    dy1 = qy - py
    dx2 = wx - vx
    dy2 = wy - vy

    # prüfe ob Geraden fast parallel
    # (Kreuzprodukt der Richtungsvektoren der Geraden fast 0)
    det = dx2*dy1 - dx1*dy2
    if math.fabs(det) < 1e-03:
        return None

    # Parmeterformen der Geraden p + k1*d1 und v + k2*d2
    # gleichsetzen und k1 und k2 mit Cramersche Regel berechnen
    #det1 = dx2*(vy-py) - dy2*(vx-px)
    det2 = dx1*(vy-py) - dy1*(vx-px)
    #k1 = det1/det
    k2 = det2/det

    return vx + k2 * dx2, vy + k2 * dy2


# Schnittpunkt Gerade und Segment.
# Bei Parallelität oder kein Schnittpunkt wird None zurückgeliefert.
def intersectLineSegment(line, seg):
    ((px,py),(qx,qy)) = line # line definiert durch Punkte p und q
    ((vx,vy),(wx,wy)) = seg # seg definiert durch Punkte v und w
    dx1 = qx - px
    dy1 = qy - py
    dx2 = wx - vx
    dy2 = wy - vy

    # prüfe ob Geraden fast parallel
    # (Kreuzprodukt der Richtungsvektoren der Geraden fast 0)
    det = dx2*dy1 - dx1*dy2
    if math.fabs(det) < 1e-03:
        return None

    # Parmeterformen der Geraden p + k1*d1 und v + k2*d2
    # gleichsetzen und k1 und k2 mit Cramersche Regel berechnen
    det1 = dx2*(vy-py) - dy2*(vx-px)
    det2 = dx1*(vy-py) - dy1*(vx-px)
    #k1 = det1/det
    k2 = det2/det

    if k2 < 0 or k2 > 1:
        return None
    else:
        return (vx+k2*dx2, vy+k2*dy2)


# Schnittpunkt zweier Segmente.
# Bei Parallelität oder kein Schnittpunkt wird None zurückgeliefert.
def intersectSegments(seg1, seg2):
    ((px,py),(qx,qy)) = seg1 # seg1 definiert durch Punkte p und q
    ((vx,vy),(wx,wy)) = seg2 # seg2 definiert durch Punkte v und w
    dx1 = qx - px
    dy1 = qy - py
    dx2 = wx - vx
    dy2 = wy - vy

    # prüfe ob Geraden fast parallel
    # (Kreuzprodukt der Richtungsvektoren der Geraden fast 0)
    det = dx2*dy1 - dx1*dy2
    if math.fabs(det) < 1e-03:
        return None

    # Parmeterformen der Geraden p + k1*d1 und v + k2*d2
    # gleichsetzen und k1 und k2 mit Cramersche Regel berechnen
    det1 = dx2*(vy-py) - dy2*(vx-px)
    det2 = dx1*(vy-py) - dy1*(vx-px)
    k1 = det1/det
    k2 = det2/det

    if k1 < 0 or k1 > 1:
        return None
    elif k2 < 0 or k2 > 1:
        return None
    else:
        return (vx+k2*dx2, vy+k2*dy2)


# Schnittpunkt Strahl und Segment.
# Bei Parallelität oder kein Schnittpunkt wird None zurückgeliefert.
def intersectRaySegment(ray, seg):
    ((px,py),theta) = ray # ray definiert durch Punkte p und Steigung theta
    ((vx,vy),(wx,wy)) = seg # seg definiert durch Punkte v und w
    dx1 = math.cos(theta)
    dy1 = math.sin(theta)
    dx2 = wx - vx
    dy2 = wy - vy

    # prüfe ob Geraden fast parallel
    # (Kreuzprodukt der Richtungsvektoren der Geraden fast 0)
    det = dx2*dy1 - dx1*dy2
    if math.fabs(det) < 1e-03:
        return None

    # Parmeterformen der Geraden p + k1*d1 und v + k2*d2
    # gleichsetzen und k1 und k2 mit Cramersche Regel berechnen
    det1 = dx2*(vy-py) - dy2*(vx-px)
    det2 = dx1*(vy-py) - dy1*(vx-px)
    k1 = det1/det
    k2 = det2/det

    if k2 < 0 or k2 > 1:
        return None
    elif k1 < 0:
        return None
    else:
        return (vx+k2*dx2, vy+k2*dy2)


# Distanz von Punkt p zu Segment seg
def dist_point_seg(p, seg):
    (x1,y1) = p
    (x2,y2) = q
    dx = x1 - x2
    dy = y1 - y2
    return math.sqrt(dx * dx + dy * dy)


if __name__ == "__main__":
    p = (1,2)
    q = (2,3)
    pl = [1, 2]
    ql = [2, 3]

    print(dist(p,q))
    print(dist(pl, ql))

    line1 = ((1,0),(2,1))
    line2 = ((0,2),(2,1))
    seg = line2
    seg1 = ((1.5, -1), (1.5, 1))
    seg2 = ((1, 0), (2, 0))
    seg3 = ((1.5, 0.5), (1.5, 1))
    ray = ((1,0),math.atan2(1.1,1))

    print(intersectLines(line1,line2))
    print(intersectLineSegment(line1, seg))
    print(intersectRaySegment(ray, seg))
    print(distPointLineWithSign(p,line1))
    print(distPointLineWithSign((3,0),line1))
    print(distPointLineWithSign((1,0),line1))
    print("intersectSegments: ", intersectSegments(seg1, seg2))
    print("intersectSegments: ", intersectSegments(seg2, seg3))

    print("distPointSegment: ", distPointSegment((0.5, 1), seg2))
    print("distPointSegment: ", distPointSegment((1.0, 1), seg2))
    print("distPointSegment: ", distPointSegment((1.5, 1), seg2))
    print("distPointSegment: ", distPointSegment((2.0, 1), seg2))
    print("distPointSegment: ", distPointSegment((2.5, 1), seg2))

    print("distPointSegment: ", distPointSegment((0.5, -1), seg2))
    print("distPointSegment: ", distPointSegment((1.0, -1), seg2))
    print("distPointSegment: ", distPointSegment((1.5, -1), seg2))
    print("distPointSegment: ", distPointSegment((2.0, -1), seg2))
    print("distPointSegment: ", distPointSegment((2.5, -1), seg2))

    print("neareastPointOnLine: ", neareastPointOnLine((2, 0.0), line1))
    print("neareastPointOnLine: ", neareastPointOnLine((1, 0.0), line1))
    print("neareastPointOnLine: ", neareastPointOnLine((1, 0.5), line1))

    print("distPointLineWithSign: ", distPointLineWithSign((0, 1), line1))
    print("distPointLineWithSign: ", distPointLineWithSign((2, 0), line1))
    print("normalToLine: ", normalToLine((0, 1), line1))
    print("normalToLine: ", normalToLine((2, 0), line1))

