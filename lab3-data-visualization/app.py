import dash
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
from dash.dependencies import Input, Output, State

import plotly.graph_objs as go
import plotly.express as px

import pandas as pd

from fileReader import *

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# tab标签的css
tabs_styles = {'height': '44px'}
tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'fontWeight': 'bold'
}
tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#119DFF',
    'color': 'white',
    'padding': '6px'
}

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

df = pd.read_csv("dataset/black-friday/BlackFriday.csv")

file = read_file()

# 获取商品分类
product_category_1, product_category_2, product_category_3 = get_product_category_1()

# 界面
app.layout = html.Div([
    html.Div([
        html.Div([
            html.Div([
                html.Label("Product Category1"),
                dcc.Dropdown(
                    id="category_1",
                    options=[{
                        "label": i,
                        "value": i
                    } for i in product_category_1],
                    value="All",
                ),
                html.Label("Product Category2"),
                dcc.Dropdown(
                    id="category_2",
                ),
                html.Label("Product Category3"),
                dcc.Dropdown(
                    id="category_3",
                ),
            ],
                style={
                    # "border": "2px black solid"
                }),
            # 散点图
            dcc.Graph(
                id='sale-price-scatter-plot',
            )
        ],
            style={
                "width": "49%",
                "display": "inline-block",
            }),
        html.Div([
            # 柱状图
            html.Div([
                dcc.Graph(
                    id='age-sex-purchase-bar-chart'
                )
            ]),
            dcc.Tabs(
                id="tabs",
                style=tabs_styles,
                children=[
                    # tab1
                    dcc.Tab(
                        label="Purchase in black five of all ages",
                        style=tab_style,
                        selected_style=tab_selected_style,
                        children=[
                            html.Div([
                                dcc.Graph(
                                    id='age-purchase-pie-chart',
                                    animate=True
                                ),
                            ]),
                        ]
                    ),
                    # tab2
                    dcc.Tab(
                        label="Residence time and purchase of each city",
                        style=tab_style,
                        selected_style=tab_selected_style,
                        children=[
                            html.Div([
                                # 折线图
                                dcc.Graph(
                                    id='city-live-sale-line-chart'
                                )
                            ])
                        ]
                    )
                ]
            )
        ],
            style={
                "width": "49%",
                "float": "right",
                "display": "inline-block"
            })
    ])
])

app.title = "Black-Friday"


# 折线图
@app.callback(
    Output('city-live-sale-line-chart', 'figure'),
    Input('category_1', 'value'),
    Input('category_2', 'value'),
    Input('category_3', 'value')
)
def update_city_live_sale_line_chart(category_1, category_2, category_3):
    new_file = read_file()
    new_file = file_filter(new_file, category_1, category_2, category_3)

    sales = get_line_char(new_file)

    cities_for_line_chart = []

    for i in range(len(cities)):
        for j in range(len(stay_in_current_city_years)):
            cities_for_line_chart.append(cities[i])

    line_df = pd.DataFrame({
        "Sales": sales,
        "LiveYears": stay_in_current_city_years * len(cities),
        "Cities": cities_for_line_chart,
    })

    line_fig = px.line(line_df, x='LiveYears', y='Sales', color='Cities', title="city-live-time-sale-line-chart")

    return line_fig


# 散点图
@app.callback(
    Output('sale-price-scatter-plot', 'figure'),
    Input('category_1', 'value'),
    Input('category_2', 'value'),
    Input('category_3', 'value')
)
def update_sale_price_scatter_plot(category_1, category_2, category_3):
    new_file = read_file()
    new_file = file_filter(new_file, category_1, category_2, category_3)

    [product_id, product_sales, product_price, product_total, product_category] = get_sales_price(new_file)

    scatter_df = pd.DataFrame({
        "ProductId": product_id,
        "ProductSales": product_sales,
        "ProductPrice": product_price,
        "ProductTotal": product_total,
        "ProductCategory": product_category,
    })

    scatter_fig = px.scatter(scatter_df, x="ProductSales", y="ProductPrice",
                             size="ProductTotal", color="ProductCategory", hover_name="ProductId",
                             title="sale-price-scatter-plot",
                             log_x=True, size_max=60, height=750)
    return scatter_fig


# 柱状图
@app.callback(
    Output('age-sex-purchase-bar-chart', 'figure'),
    Input('category_1', 'value'),
    Input('category_2', 'value'),
    Input('category_3', 'value')
)
def update_age_sex_purchase_bar_chart(category_1, category_2, category_3):
    new_file = read_file()
    new_file = file_filter(new_file, category_1, category_2, category_3)

    [x, y] = get_age_sex_purchase(new_file)

    sex = []

    for i in range(len(content_age_category) * 2):
        if i < 7:
            sex.append('M')
        else:
            sex.append('F')

    bar_df = pd.DataFrame({
        "Age": content_age_category + content_age_category,
        "Purchase": x + y,
        "Sex": sex
    })

    bar_fig = px.bar(bar_df, x="Age", y="Purchase", color="Sex", barmode="group", title="age-sex-purchase-bar-chart")

    return bar_fig


# 饼状图
@app.callback(
    Output('age-purchase-pie-chart', 'figure'),
    Input('category_1', 'value'),
    Input('category_2', 'value'),
    Input('category_3', 'value')
)
def update_age_purchase_pie_chart(category_1, category_2, category_3):
    new_file = read_file()
    new_file = file_filter(new_file, category_1, category_2, category_3)

    [content_purchase_list] = get_age_purchase(new_file)

    # print([content_age_category, content_purchase_list])

    pie_df = pd.DataFrame({
        "Labels": content_age_category,
        "Purchase": content_purchase_list,
    })

    pie_fig = px.pie(pie_df, names="Labels", values="Purchase", title="age-purchase-pie-chart")

    return pie_fig


# 设置category2
@app.callback(
    Output('category_2', 'options'),
    Input('category_1', 'value'))
def set_category_2_options(category_1):
    if category_1 == "All":
        return [{"label": "All", "value": "All"}]
    return [{'label': i, 'value': i} for i in product_category_2[int(category_1)]]


@app.callback(
    Output('category_2', 'value'),
    Input('category_2', 'options'))
def set_category_2_value(available_options):
    return available_options[0]['value']


# 设置category3
@app.callback(
    Output('category_3', 'options'),
    Input('category_1', 'value'),
    Input('category_2', 'value'))
def set_category_3_options(category_1, category_2):
    if category_1 == "All" or category_2 == "All":
        return [{"label": "All", "value": "All"}]
    return [{'label': i, 'value': i} for i in product_category_3[int(category_2)]]


@app.callback(
    Output('category_3', 'value'),
    Input('category_3', 'options'))
def set_category_3_value(available_options):
    return available_options[0]['value']


if __name__ == '__main__':
    app.run_server(debug=True)
