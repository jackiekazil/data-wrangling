from bokeh.plotting import figure, show, output_file

# NOTE: You'll need to have 'africa_cpi_cl' table from Chapter 9 to use this
# code.


def scatter_point(chart, x, y, marker_type):
    chart.scatter(x, y, marker=marker_type, line_color="#6666ee",
                  fill_color="#ee6666", fill_alpha=0.7, size=10)

chart = figure(title="Perceived Corruption and Child Labor in Africa")
output_file("scatter_plot.html")

for row in africa_cpi_cl.rows:
    scatter_point(chart, float(row['CPI 2013 Score']),
                  float(row['Total (%)']), 'circle')

show(chart)
