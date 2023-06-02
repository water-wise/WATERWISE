# WATERWISE (With Awareness, Technology, and Environmental Responsibility, Water Is Sustainably Ensured)
WATERWISE  is an initiative aimed at addressing the global issue of water scarcity, with a particular focus on the Middle East and North Africa (MENA) region. By promoting Awareness, leveraging Technology, and advocating for Environmental Responsibility, we aim to increase access to sustainable, affordable, and reliable water in underserved MENA communities. Our approach involves developing a model and a mobile application designed to track and predict water usage, identify cost-effective water infrastructure solutions, and provide region-specific tips on environmental responsibility. This strategic tool will enable effective planning for new water infrastructure development and ensure informed, sustainable decisions about water resource allocation.

## Context
Water scarcity is a critical issue affecting numerous regions globally. According to the World Bank, approximately 90% of children in the MENA region reside in areas with high or extremely high water stress. This region, marked by arid and semi-arid climates, limited freshwater resources, rapid population growth, and escalating water demands, calls for immediate action and innovative solutions.

WATERWISE is our response to this pressing challenge. We are committed to creating a platform that raises awareness about water scarcity, encourages the use of sustainable water technology, and promotes environmental responsibility.

## Objectives
The primary objectives of the WATERWISE project are:

1. To develop a predictive model capable of forecasting changes in water data due to climatic variations, and provide the Optimal Cost-Effective Solution (OCES) for constructing water infrastructure.
2. To construct a mobile application integrating the predictive model, enabling real-time tracking and forecasting of water data.
3. To enhance water scarcity awareness and encourage responsible water usage.
4. To propose technology-based solutions to achieve water sustainability.
5. To provide tips on environmental responsibility, focusing on water use efficiency as a solution to water scarcity instead of solely relying on new infrastructure.

## Data
We have collected data on existing desalination plants from [Desaldata](https://desaldata.com). The dataset includes 21,932 entries across 160 columns. However, approximately 50 percent of these records contain missing values for the price variable. Additionally, the dataset presents inconsistencies in the price data due to the representation of about 15 different currencies.

## Data Cleaning
Data cleaning involved:
- Filtering the dataset to include only records with non-missing prices
- Dropping columns with more than 90 percent missing values
- Converting the prices to a base currency (USD)

After cleaning, the dataset was reduced to 10,314 rows and 40 columns. These represent the records for plants contracted between 1944 and 2022, with prices ranging from 8,000 USD to 2.56 billion USD.

## Data Preprocessing
Data preprocessing primarily involved imputation of missing values and encoding of categorical variables. We also utilized custom transformers for specific imputations and feature engineering. The preprocessing steps included:

- **Excluding Leakage Variables**: We eliminated `award date`, `online date`, and `plant status`, as these are not values typically available during forecasting.
- **Removing Correlated and Irrelevant Features**: Variables such as `mgd` and `migd` were redundant as they were merely unit conversions of the `capacity` and `size` variables. The converted price variable (`log_price`) was the only relevant target. Moreover, we assumed that the name of a project would not influence its price.
- **Handling Missing Values**: To impute missing values, we had to distinguish whether the missing entries were unrecorded or simply non-existent. For instance, we found that `thermal_design` contained missing values because only plants using thermal processes would have thermal designs.
- **Feature Scaling and Categorical Encoding**: We used scikit-learn's StandardScaler class to scale numerical features and the OneHotEncoder class to encode categorical features.

## Baseline Model
We established a baseline model to assess if machine learning would be a worthwhile investment. Given the strong correlation between price and size, we used the average values of the different sizes to calculate the mean absolute error. An approximation based on the size of a plant resulted in an error of about 5 million USD.

## Model Building and Evaluation
We evaluated several models in this project, including `LinearRegression`, `Lasso`, `DecisionTreeRegressor`, `RandomForestRegressor`, `ExtraTreesRegressor`, `GradientBoostingRegressor`, `AdaBoostRegressor`, `XGBRegressor`, `LGBMRegressor`, and `CatBoostRegressor`. In the initial training, we considered only categorical features with not more than 10 unique categories. The results showed that the boosting models outperformed the remaining models. To confirm this observation, we reevaluated the models using a 5-fold cross validation pipeline.

To assess the effect of high cardinality columns, we included all categorical columns in the retraining of the `CatBoostRegressor`. We found that the high cardinality columns did not significantly affect the model's performance.

## Feature Engineering
To enhance the performance of the models, we created new features by:
- Combining related features
- Creating ordinal encoding for ordinal categorical features, such as size
- Creating indicator variables, such as `number of bidders` to reflect competition

We retrained the models using these new features and the low cardinality categorical columns (those with 30 unique values). However, these new features did not markedly improve the models' performance.

## Final Model
Based on the training results, we selected the `CatBoostRegressor` as the final model. We then retrained this model using the top 14 most important features from the feature importance plot. Finally, we evaluated the trained model on the unseen test set, yielding a mean absolute error of about 2.3 million USD, consistent with the validation error. We used the preprocessor and final model to build an intuitive online price predictor.

## Prediction Tool (ASFA)
The online prediction tool, named ASFA (Aqua Security for All), uses the pickled model and preprocessor to handle user inputs and generate appropriate predictions. This prediction represents the minimum investment, in US Dollars, required to build a desalination plant with a given set of features.

## Conclusion
The technical specifications of a desalination plant are generally indicative of its price. While location variables like continent might offer some information, a plant’s price is heavily reliant on the salinity of the water to be treated, the desired salinity of the output, the plant's size, the amount of water to be produced, its desalination process, its model, and other technical factors.

## Further Improvements
The validation errors of the final model suggest that the model tends to make larger errors for larger plants and smaller errors for smaller plants. This behavior could be attributed to the fact that large plants constitute less than 10 percent of the plants in the dataset. The models could potentially benefit from a more balanced and representative dataset.

In addition, we could explore the use of neural networks to handle feature combination and uncover more complex relationships.