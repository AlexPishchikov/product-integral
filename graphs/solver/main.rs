use std::env;
use std::process;
use std::fs::File;
use std::io::Write;
use std::f32::consts::E;

pub struct FunctionParams {
    pub f : fn(f32, f32, f32) -> f32,
    pub df : fn(f32, f32, f32) -> f32,
    pub n : f32,
    pub c : f32,
    pub a : f32,
    pub b : f32,
    pub h : f32,
}

pub struct GraphType {
    pub function : bool,
    pub integral : bool,
    pub derivative : bool,
}

fn power_function(x : f32, n : f32, c : f32) -> f32 {
    return c * x.powf(n);
}

fn exponential_function(x : f32, n : f32, c : f32) -> f32 {
    return E.powf(n * x + c);
}

fn power_function_derivative(x : f32, n : f32, c : f32) -> f32 {
    return c * n * x.powf(n - 1.0);
}

fn exponential_function_derivative(x : f32, n : f32, c : f32) -> f32 {
    return n * E.powf(n * x + c);
}

fn parse_input_params(args : Vec<String>) -> (FunctionParams, GraphType) {
    let mut function_params : FunctionParams = {
        FunctionParams {
            f : power_function,
            df : power_function_derivative,
            n : 0.0,
            c : 0.0,
            a : 1.0,
            b : 3.0,
            h : 0.01,
        }
    };

    let mut graph_type : GraphType = {
        GraphType {
            function : true,
            integral : true,
            derivative : true,
        }
    };

    let input_graph_type : &str = &args[1];

    let input_f = args[0].parse::<i32>();
    let input_n = args[2].parse::<f32>();
    let input_c = args[3].parse::<f32>();
    let input_a = args[4].parse::<f32>();
    let input_b = args[5].parse::<f32>();
    let input_h = args[6].parse::<f32>();

    graph_type.function = if input_graph_type.chars().nth(0) == Some('1') {true} else {false};
    graph_type.integral = if input_graph_type.chars().nth(1) == Some('1') {true} else {false};
    graph_type.derivative = if input_graph_type.chars().nth(2) == Some('1') {true} else {false};

    match input_f {
        Ok(input_f) => {
            function_params.f = if input_f == 0 { power_function } else { exponential_function };
            function_params.df = if input_f == 0 { power_function_derivative } else { exponential_function_derivative }
        },
        Err(input_f) => {
            eprintln!("{:?}", input_f);
            process::exit(1);
        },
    }

    match input_n {
        Ok(input_n) => function_params.n = input_n,
        Err(input_n) => {
            eprintln!("{:?}", input_n);
            process::exit(1);
        },
    }

    match input_c {
        Ok(input_c) => function_params.c = input_c,
        Err(input_c) => {
            eprintln!("{:?}", input_c);
            process::exit(1);
        },
    }

    match input_a {
        Ok(input_a) => function_params.a = input_a,
        Err(input_a) => {
            eprintln!("{:?}", input_a);
            process::exit(1);
        },
    }

    match input_b {
        Ok(input_b) => function_params.b = input_b,
        Err(input_b) => {
            eprintln!("{:?}", input_b);
            process::exit(1);
        },
    }

    match input_h {
        Ok(input_h) => function_params.h = input_h,
        Err(input_h) => {
            eprintln!("{:?}", input_h);
            process::exit(1);
        },
    }

    return (function_params, graph_type);
}

fn calculate_function_coords(function_params : &FunctionParams) {
    let mut output = File::create("function_coords").unwrap();
    let mut i : f32 = function_params.a;
    while i < function_params.b {
        writeln!(&mut output, "{} {}", i, (function_params.f)(i, function_params.n, function_params.c)).unwrap();
        i += function_params.h;
    }
}

fn calculate_derivative_coords(function_params : &FunctionParams) {
    let mut output = File::create("derivative_coords").unwrap();
    let mut i : f32 = function_params.a;
    while i < function_params.b {
        writeln!(&mut output, "{} {}", i, E.powf(((function_params.df)(i, function_params.n, function_params.c))/(function_params.f)(i, function_params.n, function_params.c))).unwrap();
        i += function_params.h;
    }
}

fn calculate_integral_coords(function_params : &FunctionParams) {
    let mut output = File::create("integral_coords").unwrap();
    let mut i : f32 = function_params.a;
    let mut integral : f32 = 1.0;
    while i < function_params.b {
        integral *= ((function_params.f)(i, function_params.n, function_params.c)).powf(function_params.h);
        writeln!(&mut output, "{} {}", i, integral).unwrap();
        i += function_params.h;
    }
}

fn main() {
    let args : Vec<String> = env::args().skip(1).collect();
    let (function_params, graph_type) : (FunctionParams, GraphType) = parse_input_params(args);

    if graph_type.function {
        calculate_function_coords(&function_params);
    }

    if graph_type.integral {
        calculate_integral_coords(&function_params);
    }

    if graph_type.derivative {
        calculate_derivative_coords(&function_params);
    }
}
