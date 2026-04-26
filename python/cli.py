from polysolver import solve_quadratic, solve_cubic
choice=input("1) Quadratic\n2) Cubic\nChoose: ")
if choice=="1":
    a,b,c=map(float,input("a b c: ").split())
    print(solve_quadratic(a,b,c))
elif choice=="2":
    a,b,c,d=map(float,input("a b c d: ").split())
    print(solve_cubic(a,b,c,d))
