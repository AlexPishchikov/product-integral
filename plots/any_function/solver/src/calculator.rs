use meval::*;

use crate::input_parser::{FunctionParams, PlotType};


pub fn calculate(function_params : &FunctionParams, plot_type : &PlotType) -> Vec<(Vec<f64>, Vec<f64>)> {
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

    return coords;
}

fn calculate_function_coords(function_params : &FunctionParams) -> (Vec<f64>, Vec<f64>) {
    let mut i : f64 = function_params.a;

    let mut coords_x : Vec<f64> = Vec::new();
    let mut coords_y : Vec<f64> = Vec::new();

    let mut ctx = Context::new();
    ctx.var("n", function_params.n)
       .var("c", function_params.c);
    let func = (function_params.f).parse::<Expr>().unwrap().bind_with_context(ctx, "x").unwrap();

    while i < function_params.b {
        coords_x.push(i);
        coords_y.push(func(i));
        i += function_params.h;
    }

    return (coords_x, coords_y);
}

fn calculate_derivative_coords(function_params : &FunctionParams) -> (Vec<f64>, Vec<f64>) {
    let mut i : f64 = function_params.a;

    let mut coords_x : Vec<f64> = Vec::new();
    let mut coords_y : Vec<f64> = Vec::new();

    let mut ctx = Context::new();
    ctx.var("n", function_params.n)
       .var("c", function_params.c);
    let func = (function_params.f).parse::<Expr>().unwrap().bind_with_context(ctx, "x").unwrap();

    while i < function_params.b {
        coords_x.push(i);
        coords_y.push((func(i + function_params.h) / func(i)).powf(1.0 / function_params.h));
        i += function_params.h;
    }

    return (coords_x, coords_y);
}

fn calculate_integral_coords(function_params : &FunctionParams) -> (Vec<f64>, Vec<f64>) {
    let mut i : f64 = function_params.a;
    let mut integral : f64 = 1.0;

    let mut coords_x : Vec<f64> = Vec::new();
    let mut coords_y : Vec<f64> = Vec::new();

    let mut ctx = Context::new();
    ctx.var("n", function_params.n)
       .var("c", function_params.c);
    let func = (function_params.f).parse::<Expr>().unwrap().bind_with_context(ctx, "x").unwrap();

    while i < function_params.b {
        integral *= func(i).powf(function_params.h);
        coords_x.push(i);
        coords_y.push(integral);
        i += function_params.h;
    }

    return (coords_x, coords_y);
}
