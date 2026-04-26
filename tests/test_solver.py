from polysolver import solve_quadratic, solve_cubic
def test_quad():
    r=solve_quadratic(1,-3,2)
    assert sorted([round(x.real,5) for x in r])==[1,2]
def test_cubic():
    r=solve_cubic(1,-6,11,-6)
    assert sorted([round(x.real,5) for x in r])==[1,2,3]
