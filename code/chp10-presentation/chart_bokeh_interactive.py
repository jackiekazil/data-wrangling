from bokeh.plotting import ColumnDataSource, figure, show, output_file
from bokeh.models import HoverTool

# NOTE: For this chart, you will also need the 'africa_cpi_cl' table from
# Chapter 9.


TOOLS = "pan,reset,hover"


def scatter_point(chart, x, y, source, marker_type):
    chart.scatter(x, y, source=source, marker=marker_type,
                  line_color="#6666ee", fill_color="#ee6666",
                  fill_alpha=0.7, size=10)

chart = figure(title="Perceived Corruption and Child Labor in Africa",
               tools=TOOLS)

output_file("scatter_int_plot.html")

for row in africa_cpi_cl.rows:
    column_source = ColumnDataSource(
        data={'country': [row['Country / Territory']]})
    scatter_point(chart, float(row['CPI 2013 Score']),
                  float(row['Total (%)']), column_source, 'circle')

hover = chart.select(dict(type=HoverTool))
hover.tooltips = [
    ("Country", "@country"),
    ("CPI Score", "$x"),
    ("Child Labor (%)", "$y"),
]

show(chart)
