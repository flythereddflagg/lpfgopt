let N_RESULTS: u32 = 7;

struct lpfgopt_data{
    f: fn(&std::Vec<f64>, u32) -> f64,   // the objective function
    g: fn(&std::Vec<f64>, u32) -> f64,   // the constraint function
    xlen: u32,                           // the number of args in f and g
    points: u32,                         // the number of points for optimization

    lower: &std::Vec<f64>,               // the lower bounds; length = xlen
    upper: &std::Vec<f64>,               // the upper bounds; length = xlen
    pointset: &std::Vec<&std::Vec<f64>>, // point set; shape = (points, xlen)
    free_pointset: bool,                 // (bool) free the pointset when done?
    objs: &std::Vec<f64>,                // the objective function values; length = po

    discrete: &std::Vec<u32>,            // array of discrete indices
    discretelen: u32,                    // length of discrete

    nfev: u32,                           // number of function evaluations
    maxcv: f64,                          // maximum constraint violation

    besti: u32,                          // the index of the best point
    worsti: u32,                         // the index of the worst point
    error: f64,                          // the value of the convergence error
    tol: f64,                            // convergence tolerance
    big: f64,                            // punishing number. A big, positive number.
}






fn main() {
    println!("Hello, world!");
}
