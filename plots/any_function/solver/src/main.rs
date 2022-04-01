use std::env;
use std::process;

use meval::*;
use gnuplot::*;

pub struct FunctionParams {
    pub f : String,
    pub n : f64,
    pub c : f64,
    pub a : f64,
    pub b : f64,
    pub h : f64,
}

pub struct PlotType {
    pub function : bool,
    pub integral : bool,
    pub derivative : bool,
}

fn parse_input_params(args : Vec<String>) -> (FunctionParams, PlotType) {
    let mut function_params : FunctionParams = {
        FunctionParams {
            f : "x".to_string(),
            n : 1.0,
            c : 1.0,
            a : 1.0,
            b : 3.0,
            h : 0.1,
        }
    };

    let mut plot_type : PlotType = {
        PlotType {
            function   : true,
            integral   : true,
            derivative : true,
        }
    };

    if args.len() == 0 {
        return (function_params, plot_type);
    }

    let input_plot_type : &str = &args[1];

    let input_f = args[0].parse::<String>();

    let input_n = args[2].parse::<f64>();
    let input_c = args[3].parse::<f64>();
    let input_a = args[4].parse::<f64>();
    let input_b = args[5].parse::<f64>();
    let input_h = args[6].parse::<f64>();

    plot_type.function   = if input_plot_type.chars().nth(0) == Some('1') {true} else {false};
    plot_type.integral   = if input_plot_type.chars().nth(1) == Some('1') {true} else {false};
    plot_type.derivative = if input_plot_type.chars().nth(2) == Some('1') {true} else {false};

    match input_f {
        Ok(input_f) => {
            function_params.f = input_f;
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

fn draw_plot(coords : &Vec<(Vec<f64>, Vec<f64>)>) {
    let mut fg = Figure::new();

    // if coords[0].0.len() > 0 {
    //     fg.axes2d().lines(&coords[0].0, &coords[0].1, &[LineWidth(2.0), Color("red"), Caption("function")]);
    // }

    // if coords[1].0.len() > 0 {
    //     fg.axes2d().lines(&coords[1].0, &coords[1].1, &[LineWidth(2.0), Color("blue"), Caption("derivative")]);
    // }

    // if coords[2].0.len() > 0 {
    //     fg.axes2d().lines(&coords[2].0, &coords[2].1, &[LineWidth(2.0), Color("green"), Caption("integral")]);
    // }

    fg.axes2d()
        .lines(&coords[0].0, &coords[0].1, &[LineWidth(2.0), Color("red"), Caption("function")])
        .lines(&coords[2].0, &coords[2].1, &[LineWidth(2.0), Color("green"), Caption("integral")])
        .lines(&coords[1].0, &coords[1].1, &[LineWidth(2.0), Color("blue"), Caption("derivative")])
        .set_y_ticks(Some((Auto, 2)), &[], &[])
        .set_grid_options(true, &[LineStyle(Solid), Color("black")])
        .set_x_grid(true)
        .set_y_grid(true);

    fg.save_to_svg("../../plot.svg", 800, 400);
}


fn main() {
    let args : Vec<String> = env::args().skip(1).collect();

    let (function_params, plot_type) : (FunctionParams, PlotType) = parse_input_params(args);

    let mut coords : Vec<(Vec<f64>, Vec<f64>)> = Vec::new();


    if plot_type.function {
        coords.push(calculate_function_coords(&function_params));
    }
    else {
        coords.push((Vec::new(), Vec::new()))
    }

    if plot_type.derivative {
        coords.push(calculate_derivative_coords(&function_params));
    }
    else {
        coords.push((Vec::new(), Vec::new()))
    }

    if plot_type.integral {
        coords.push(calculate_integral_coords(&function_params));
    }
    else {
        coords.push((Vec::new(), Vec::new()))
    }

    draw_plot(&coords);
}
