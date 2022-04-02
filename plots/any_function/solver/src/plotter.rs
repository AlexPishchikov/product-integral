use gnuplot::*;
use std::process;

pub fn draw_plot(coords : &Vec<(Vec<f64>, Vec<f64>)>) {
    let mut fg = Figure::new();

    fg.axes2d()
        .lines(&coords[0].0, &coords[0].1, &[LineWidth(2.0), Color("red"), Caption("function")])
        .lines(&coords[2].0, &coords[2].1, &[LineWidth(2.0), Color("green"), Caption("integral")])
        .lines(&coords[1].0, &coords[1].1, &[LineWidth(2.0), Color("blue"), Caption("derivative")])
        // .points(&coords[0].0, &coords[0].1, &[PointSize(0.8), PointSymbol('.'), Color("red")])
        // .points(&coords[2].0, &coords[2].1, &[PointSize(0.8), PointSymbol('.'), Color("green")])
        // .points(&coords[1].0, &coords[1].1, &[PointSize(0.8), PointSymbol('.'), Color("blue")])
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
