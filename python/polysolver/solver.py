import cmath, math
EPS=1e-12
def is_zero(x): return abs(x)<EPS
def solve_quadratic(a,b,c):
    if is_zero(a):
        if is_zero(b): return []
        return [-c/b]
    disc=cmath.sqrt(b*b-4*a*c)
    q=-0.5*(b+disc if b>0 else b-disc)
    x1=q/a
    x2=c/q if not is_zero(q) else x1
    return [x1,x2]
def solve_cubic(a,b,c,d):
    if is_zero(a): return solve_quadratic(b,c,d)
    b/=a; c/=a; d/=a
    p=c-b*b/3
    q=2*b**3/27-b*c/3+d
    disc=(q/2)**2+(p/3)**3
    if disc>EPS:
        sqrt_d=cmath.sqrt(disc)
        u=(-q/2+sqrt_d)**(1/3)
        v=(-q/2-sqrt_d)**(1/3)
        x1=u+v-b/3
        omega=complex(-0.5,math.sqrt(3)/2)
        x2=u*omega+v*omega.conjugate()-b/3
        x3=u*omega.conjugate()+v*omega-b/3
        return [x1,x2,x3]
    elif is_zero(disc):
        u=(-q/2)**(1/3)
        return [2*u-b/3,-u-b/3,-u-b/3]
    else:
        r=math.sqrt(-p**3/27)
        phi=math.acos(-q/(2*r))
        t=2*(r**(1/3))
        return [
            t*math.cos(phi/3)-b/3,
            t*math.cos((phi+2*math.pi)/3)-b/3,
            t*math.cos((phi+4*math.pi)/3)-b/3]
