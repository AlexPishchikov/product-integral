use gnuplot::*;
use std::process;

use crate::PlotType;

pub fn draw_plot(coords : &Vec<(Vec<f64>, Vec<f64>)>, plot_type : PlotType) {
    let mut fg = Figure::new();

    let point_size = if plot_type.points {0.4} else {0.0};

    fg.axes2d()
        .lines_points(&coords[0].0, &coords[0].1, &[Caption("function"), PointSize(point_size), PointSymbol('O'), Color("red")])
        .lines_points(&coords[1].0, &coords[1].1, &[Caption("derivative"), PointSize(point_size), PointSymbol('O'), Color("blue")])
        .lines_points(&coords[2].0, &coords[2].1, &[Caption("integral"), PointSize(point_size), PointSymbol('O'), Color("green")])
        .set_y_ticks(Some((Auto, 2)), &[], &[])
        .set_grid_options(true, &[LineStyle(Solid), Color("black")])
        .set_x_grid(true)
        .set_y_grid(true);

    let save_plot = fg.save_to_svg("../../plot.svg", 800, 400);
    match save_plot {
        Ok(_) => {},
        Err(save_plot) => {
            eprintln!("{:?}", save_plot);
            process::exit(1);
        },
    }
}
