# Lab 3 Report

Black Friday

### Data analysis task for the chosen dataset 

#### Objectives

I use black Friday as the data set for this project. When I first got this dataset, I noticed that it was very large and it was slow to open with Excel. So my first idea is to sort the data. Thanks to its three categories, I classified the dataset.

In this data set, I want to know the relationship between gender and purchase amount; the relationship between age and purchase amount; the relationship between different cities and residential areas and purchase amount; the relationship between commodity price and commodity sales.

So I choose these tags in this csv file : ```User_ID```, ```Product_ID```, ```Gender```, ```Age```, ```City_Category```, ```Stay_In_Current_City_Years```, ```Product_Category_1```, ```Product_Category_2```, ```Product_Category_3```, ```Purchase```.

#### Characteristic

##### Categories

These products have three main categories, such as daily necessities, toiletries, toothbrushes, expressed in numbers. And each category has about eighteen tags.

![image-20210611151516169](Report.assets/image-20210611151516169.png)

So I use ```dcc.Dropdown``` to show all of it.

When you select a high-level tag, the low-level tag will be updated at the same time.

![image-20210611151534543](Report.assets/image-20210611151534543.png)

##### Gender

Man or Woman

I use a bar chart to show how much money people of the same age spend in different genders.

![image-20210611172152071](Report.assets/image-20210611172152071.png)

##### Age

```python
content_age_category = [
    '0-17', '18-25', '26-35',
    '36-45', '46-50', '51-55',
    '55+',
]
```

And I use the pie chart to show the consumption amount of people of different ages.

![image-20210611171855789](Report.assets/image-20210611171855789.png)

##### Cities and Years

This data set has people from four cities and years that people stay in this city.

![image-20210611172359785](Report.assets/image-20210611172359785.png)

I use a line chart to show the data.

![image-20210611172408126](Report.assets/image-20210611172408126.png)

##### Purchase

The purchase amount of a product for a user.

![image-20210611172531752](Report.assets/image-20210611172531752.png)

##### User ID

Corresponding to a user.

##### Product ID

Corresponding to a product.

![image-20210611172649114](Report.assets/image-20210611172649114.png)

##### Other

And there are some tags that i do not use in this dataset, like Marital_Status and Occupation.

### The layout of designed dashboard

First, I've listed the charts I need to use. They are scatter plot, pie chart, line chart and bar chart. Before I start drawing, I need to classify the data set. For the three categories of products, I use three ```dcc.Dropdown()``` components to classify the data displayed in the chart.

After classification, I begin to draw these charts powered by ```plotly.express``` and ```dash_core_components``` , such as ```dcc.Graph()``` 、```px.pie``` 、```px.line``` 、```px.scatter```、```px.bar``` . In this period, I just simply drew them, stacked them on the screen, and did not sort them out.

Then, I made a simple design of the interface on my iPad , and arranged the four charts and the category drop-down box.

Finally, I use ```dash_bootstrap_components``` to beautify my page. 

![image-20210612134611080](Report.assets/image-20210612134611080.png)

![image-20210612134625613](Report.assets/image-20210612134625613.png)

### The patterns revealed in the figures

I draw four graphs for this dataset.

1. Scatter plot

   ![image-20210611173646335](Report.assets/image-20210611173646335.png)

   ![image-20210611173702489](Report.assets/image-20210611173702489.png)

   In this picture, I want to find the relationship between the sales volume and the unit price of goods in the same commodity category.

2. Bar chart

   ![image-20210611173714336](Report.assets/image-20210611173714336.png)

   n this picture, I want to explore the purchasing power of the same age group and different gender on Black Friday

3. Pie chart

   ![image-20210611173742495](Report.assets/image-20210611173742495.png)

   ![image-20210611173800240](Report.assets/image-20210611173800240.png)

   In this picture, I want to explore the purchasing power of different age groups.

4. Line chart

   ![image-20210611173732466](Report.assets/image-20210611173732466.png)
   
   In this picture, I want to explore the influence of the same city and different residence time on the consumption of Black Friday.
   
   