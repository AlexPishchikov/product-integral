use std::process;

pub struct FunctionParams {
    pub f : String,
    pub n : f64,
    pub c : f64,
    pub a : f64,
    pub b : f64,
    pub h : f64,
}

pub struct PlotType {
    pub function   : bool,
    pub derivative : bool,
    pub integral   : bool,
    pub points     : bool,
}


pub fn parse_input_params(args : Vec<String>) -> (FunctionParams, PlotType) {
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
            derivative : true,
            integral   : true,
            points     : false,
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
    plot_type.derivative = if input_plot_type.chars().nth(1) == Some('1') {true} else {false};
    plot_type.integral   = if input_plot_type.chars().nth(2) == Some('1') {true} else {false};
    plot_type.points     = if input_plot_type.chars().nth(3) == Some('1') {true} else {false};

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
