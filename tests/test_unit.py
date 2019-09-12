from lpfgopt.leapfrog import LeapFrog

def test_unit():
    """
    General use unit test
    """

    def _f_test(x, offset):
        return 2.0 * x[0]**2 + x[1]**2 + offset
    
    _g1 = lambda x: x[0] + 3

    _intvls = [
        [-10.0, 10.0],
        [-10.0, 10.0]]

    _starting_points = [
        [-3.269716623,   -7.930871],
        [-0.301065303,   2.3311285],
        [-7.378448241,   6.1100162],
        [-0.191330390,   7.0158780],
        [-7.217230801,   -8.815178],
        [-6.878029799,   4.0923533],
        [-4.587077226,   9.0630253],
        [-9.755670223,   -8.901648],
        [4.9019506940,   -3.184652],
        [-7.532104399,   1.6987271],
        [5.4372269021,   0.5777975],
        [-7.739404401,   9.8297502],
        [0.5493843932,   5.6662483],
        [9.2385537811,   -7.513752],
        [-1.295963317,   -4.268123],
        [7.7269409075,   1.4205298],
        [-4.322107922,   6.0013770],
        [-7.112370271,   9.4093474],
        [1.9372210724,   7.5056536],
        [7.0920413003,  -9.8860190]]
    
    options = {
        "fun"         : _f_test, 
        "bounds"      : _intvls,
        "args"        : (3.0,),
        "points"      : len(_starting_points),
        "fconstraint" : _g1,
        "discrete"    : [0,1],
        "maxit"       : 5000,
        "tol"         : 1e-3,
        "seedval"     : 1235,
        "pointset"    : _starting_points
        }
    
    # Constrained and discrete optimization -----------------------------------    
    lf = LeapFrog(**options)
    
    print("\nCONSTRAINED AND DISCRETE OPTIMIZATION:\nBEFORE:")
    print(lf)        
    solution = lf.minimize() 
    print("AFTER:")
    print(lf)
    
    print("\nPoint Set:")
    for i in solution['pointset']:
        print(i)
    print()
    
    check = [21.0, -3, 0]
    for i in range(len(solution["best"])):
        assert solution["best"][i] == check[i], f"Unit test failed on {i}"
