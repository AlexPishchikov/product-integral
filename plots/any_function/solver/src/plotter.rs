use gnuplot::*;


pub fn draw_plot(coords : &Vec<(Vec<f64>, Vec<f64>)>) {
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
