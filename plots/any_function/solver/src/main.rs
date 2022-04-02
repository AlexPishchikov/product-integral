use std::env;

mod input_parser;
mod calculator;
mod plotter;

use crate::input_parser::parse_input_params;
use crate::input_parser::{FunctionParams, PlotType};

use crate::calculator::calculate;

use crate::plotter::draw_plot;


fn main() {
    let args : Vec<String> = env::args().skip(1).collect();

    let (function_params, plot_type) : (FunctionParams, PlotType) = parse_input_params(args);

    draw_plot(&calculate(&function_params, &plot_type), plot_type);
}
