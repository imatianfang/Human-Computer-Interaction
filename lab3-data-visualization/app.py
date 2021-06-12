import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from dash.dependencies import Input, Output, State

import plotly.express as px

from fileReader import *

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

df = pd.read_csv("dataset/black-friday/BlackFriday.csv")

file = read_file()

# 获取商品分类
product_category_1, product_category_2, product_category_3 = get_product_category_1()

# 导航栏
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("About",
                                href="https://github.com/imatianfang/Human-Computer-Interaction/tree/main/lab3-data-visualization")),
    ],
    brand="Black Friday",
    brand_href="",
    sticky="top",
)

# 种类选择
category_card = dbc.Card(
    [
        dbc.CardHeader("Category"),
        dbc.CardBody(
            [
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
                    html.Div([
                        dbc.Button("Submit", color="primary", id="Submit-btn", n_clicks=0,
                                   className="mr-1", style={"margin": "20px"}),
                    ],
                        style={"text-align": "center"})

                ])
            ]
        ),
    ]
)

# 散点图
scatter_plot = dbc.Card(
    [
        dbc.CardHeader("sale-price-scatter-plot"),
        dbc.CardBody(
            [
                # 散点图
                dcc.Graph(
                    id='sale-price-scatter-plot',
                )
            ]
        ),
    ]
)

# 柱状图
bar_chart = dbc.Card(
    [
        dbc.CardHeader("age-sex-purchase-bar-chart"),
        dbc.CardBody(
            [
                # 柱状图
                dcc.Graph(
                    id='age-sex-purchase-bar-chart'
                )
            ]
        ),
    ]
)

# 折线图-饼状图
tabs = html.Div(
    [
        dbc.Tabs(
            [
                dbc.Tab(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                dcc.Graph(
                                    id='age-purchase-pie-chart',
                                    animate=True
                                ),
                            ]
                        )
                    ),
                    label="age-purchase-pie-chart",
                    style={"padding": "10px"},
                ),
                dbc.Tab(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                dcc.Graph(
                                    id='city-live-sale-line-chart'
                                )
                            ]
                        )
                    ),
                    label="city-live-time-sale-line-chart",
                    style={"padding": "10px"},
                ),
            ]
        ),
    ]
)

# 界面
app.layout = html.Div([
    navbar,
    dbc.Container(
        [
            html.Div(
                [
                    html.Div(
                        [
                            category_card
                        ],
                        style={"width": "25%", "float": "left", "margin": "0 20px 0 0"}
                    ),
                    html.Div(
                        [
                            scatter_plot,
                        ],
                        style={"width": "70%", "float": "left"}
                    )
                ],
                style={"width": "100%", "float": "left", "margin": "10px 0 20px 0"},
            ),
            html.Div(
                [
                    html.Div(
                        [
                            bar_chart,
                        ],
                        style={"width": "50%", "float": "left", "margin": "0 20px 0 0"}
                    ),
                    html.Div(
                        [
                            tabs,
                        ],
                        style={"width": "45%", "float": "left"}
                    )
                ]
            )
        ]),

])

app.title = "Black-Friday"


# 折线图
@app.callback(
    Output('city-live-sale-line-chart', 'figure'),
    Input('Submit-btn', 'n_clicks'),
    State('category_1', 'value'),
    State('category_2', 'value'),
    State('category_3', 'value')
)
def update_city_live_sale_line_chart(n_clicks, category_1, category_2, category_3):
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

    line_fig = px.line(line_df, x='LiveYears', y='Sales', color='Cities')

    return line_fig


# 散点图
@app.callback(
    Output('sale-price-scatter-plot', 'figure'),
    Input('Submit-btn', 'n_clicks'),
    State('category_1', 'value'),
    State('category_2', 'value'),
    State('category_3', 'value')
)
def update_sale_price_scatter_plot(n_clicks, category_1, category_2, category_3):
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
                             log_x=True)
    return scatter_fig


# 柱状图
@app.callback(
    Output('age-sex-purchase-bar-chart', 'figure'),
    Input('Submit-btn', 'n_clicks'),
    State('category_1', 'value'),
    State('category_2', 'value'),
    State('category_3', 'value')
)
def update_age_sex_purchase_bar_chart(n_clicks, category_1, category_2, category_3):
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
        "Gender": sex
    })

    bar_fig = px.bar(bar_df, x="Age", y="Purchase", color="Gender", barmode="group")

    return bar_fig


# 饼状图
@app.callback(
    Output('age-purchase-pie-chart', 'figure'),
    Input('Submit-btn', 'n_clicks'),
    State('category_1', 'value'),
    State('category_2', 'value'),
    State('category_3', 'value')
)
def update_age_purchase_pie_chart(n_clicks, category_1, category_2, category_3):
    new_file = read_file()
    new_file = file_filter(new_file, category_1, category_2, category_3)

    [content_purchase_list] = get_age_purchase(new_file)

    # print([content_age_category, content_purchase_list])

    pie_df = pd.DataFrame({
        "Labels": content_age_category,
        "Purchase": content_purchase_list,
    })

    pie_fig = px.pie(pie_df, names="Labels", values="Purchase")

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
