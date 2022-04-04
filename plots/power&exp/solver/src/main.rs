use std::env;
use std::process;
use std::f64::consts::E;

use crate::plotter::draw_plot;

mod plotter;

pub struct FunctionParams {
    pub f : fn(f64, f64, f64) -> f64,
    pub df : fn(f64, f64, f64) -> f64,
    pub n : f64,
    pub c : f64,
    pub a : f64,
    pub b : f64,
    pub h : f64,
}

pub struct PlotType {
    pub points : bool,
    pub function : bool,
    pub integral : bool,
    pub derivative : bool,
}

fn power_function(x : f64, n : f64, c : f64) -> f64 {
    return c * x.powf(n);
}

fn exponential_function(x : f64, n : f64, c : f64) -> f64 {
    return E.powf(n * x + c);
}

fn power_function_derivative(x : f64, n : f64, c : f64) -> f64 {
    return c * n * x.powf(n - 1.0);
}

fn exponential_function_derivative(x : f64, n : f64, c : f64) -> f64 {
    return n * E.powf(n * x + c);
}

fn parse_input_params(args : Vec<String>) -> (FunctionParams, PlotType) {
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

    let mut plot_type : PlotType = {
        PlotType {
            points : false,
            function : true,
            integral : true,
            derivative : true,
        }
    };

    if args.len() == 0 {
        return (function_params, plot_type);
    }

    let input_plot_type : &str = &args[1];

    let input_f = args[0].parse::<i32>();
    let input_n = args[2].parse::<f64>();
    let input_c = args[3].parse::<f64>();
    let input_a = args[4].parse::<f64>();
    let input_b = args[5].parse::<f64>();
    let input_h = args[6].parse::<f64>();

    plot_type.points = if input_plot_type.chars().nth(0) == Some('1') {true} else {false};
    plot_type.function = if input_plot_type.chars().nth(1) == Some('1') {true} else {false};
    plot_type.integral = if input_plot_type.chars().nth(2) == Some('1') {true} else {false};
    plot_type.derivative = if input_plot_type.chars().nth(3) == Some('1') {true} else {false};

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

    return (function_params, plot_type);
}

fn calculate_function_coords(function_params : &FunctionParams) -> (Vec<f64>, Vec<f64>) {
    let mut i : f64 = function_params.a;

    let mut coords_x : Vec<f64> = Vec::new();
    let mut coords_y : Vec<f64> = Vec::new();

    while i < function_params.b {
        coords_x.push(i);
        coords_y.push((function_params.f)(i, function_params.n, function_params.c));
        i += function_params.h;
    }

    return (coords_x, coords_y);
}

fn calculate_derivative_coords(function_params : &FunctionParams) -> (Vec<f64>, Vec<f64>) {
    let mut i : f64 = function_params.a;

    let mut coords_x : Vec<f64> = Vec::new();
    let mut coords_y : Vec<f64> = Vec::new();

    while i < function_params.b {
        coords_x.push(i);
        coords_y.push(E.powf(((function_params.df)(i, function_params.n, function_params.c))/(function_params.f)(i, function_params.n, function_params.c)));
        i += function_params.h;
    }

    return (coords_x, coords_y);
}

fn calculate_integral_coords(function_params : &FunctionParams) -> (Vec<f64>, Vec<f64>) {
    let mut i : f64 = function_params.a;
    let mut integral : f64 = 1.0;

    let mut coords_x : Vec<f64> = Vec::new();
    let mut coords_y : Vec<f64> = Vec::new();

    while i < function_params.b {
        integral *= ((function_params.f)(i, function_params.n, function_params.c)).powf(function_params.h);
        coords_x.push(i);
        coords_y.push(integral);
        i += function_params.h;
    }

    return (coords_x, coords_y);
}

fn main() {
    let args : Vec<String> = env::args().skip(1).collect();
    let (function_params, plot_type) : (FunctionParams, PlotType) = parse_input_params(args);

    let mut coords : Vec<(Vec<f64>, Vec<f64>)> = Vec::new();

    if plot_type.function {
        coords.push(calculate_function_coords(&function_params));
    }
    else {
        coords.push((vec![function_params.a], vec![function_params.a]));
    }

    if plot_type.derivative {
        coords.push(calculate_derivative_coords(&function_params));
    }
    else {
        coords.push((vec![function_params.a], vec![function_params.a]));
    }

    if plot_type.integral {
        coords.push(calculate_integral_coords(&function_params));
    }
    else {
        coords.push((vec![function_params.a], vec![function_params.a]));
    }

    draw_plot(&coords, plot_type);
}
