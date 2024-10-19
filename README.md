# Zeotap Assignments
Task 1 : Rule Engine with AST

Objective: Develop a rule engine application with a 3-tier architecture (UI, API, Backend, and Data) to determine user eligibility based on attributes such as age, department, income, and spend. The system utilizes an Abstract Syntax Tree (AST) for representing conditional rules and allows dynamic creation, modification, and combination of these rules.

Key Components:

Data Structure:
AST is used to represent logical rules.
Example node structure with fields for type, left, right, and value.

Data Storage:
Defines a database schema to store rules and metadata.

API Design:
Functions include create_rule, combine_rules, and evaluate_rule for rule creation, combining, and evaluating user data against the rules.

Test Cases:
Includes creating rules, combining them, and evaluating rules against sample user data.

Bonus:
Error handling, rule validation, modification, and user-defined functions are considered advanced features.

Task 2: Real-Time Data Processing System for Weather Monitoring

Objective: Build a real-time system to monitor weather conditions using the OpenWeatherMap API, process the data into daily summaries using rollups and aggregates, and provide configurable alert thresholds for specific weather conditions.

Key Features:

Data Source:
Retrieves weather data for Indian metros at configurable intervals.
Focuses on parameters such as temperature, perceived temperature, and weather conditions.

Processing and Analysis:
Data from the API is processed, with temperature converted to Celsius.

Rollups and Aggregates:
Provides daily weather summaries, including average, max, and min temperatures, and the dominant weather condition.

Alerting System:
User-configurable thresholds for temperature and weather conditions, triggering alerts when breached.

Visualizations:
Displays daily weather summaries and triggered alerts.

Test Cases:
Tests include system setup, data retrieval, temperature conversion, daily summaries, and alert thresholds.

Evaluation Criteria
Functionality and correctness.
Accuracy in data parsing, temperature conversion, and summary calculations.
Efficiency in data retrieval.
Completeness of test cases.
Code clarity and maintainability.
Bonus for additional features like forecasting and extended weather parameters.
