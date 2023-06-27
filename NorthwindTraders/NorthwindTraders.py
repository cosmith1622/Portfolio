import pandas as pd
import numpy as np
import sqlite3
import csv

categories = pd.read_csv('Data\categories.csv',encoding = 'utf-8')
print(categories.columns)
print(categories.head(10))

customers = pd.read_csv('Data\customers.csv',encoding = 'ISO-8859-1')
customers.rename(columns={'city':'customer_city', 'country':'customer_country', 'companyName':'customerName'}, inplace=True)
print(customers.columns)
print(customers.head(10))


employees = pd.read_csv('Data\employees.csv',encoding = 'utf-8')
employees.rename(columns={'city':'employee_city', 'country':'employee_country'}, inplace=True)
print(employees.columns)
print(employees.head(10))
conn = sqlite3.connect(':memory:')
employees.to_sql('employees', conn, index=False)
query_string = '''
    With employee_list(employeeID,employeeName,employeeTitle, employee_city, employee_country,managerName,managerTitle,managerCity, managerCountry,path,reportsTo) AS(
        Select 
            employeeID,
            employeeName,
            title as employeeTitle,
            employee_city,
            employee_country,
            NULL,
            NULL,
            NULL,
            NULL,
            employeeName as path,
            reportsTo

        From employees
        where reportsTo is null
        union all
        Select 
            emp2.employeeID,
            emp2.employeeName,
            emp2.title as employeeTitle,
            emp2.employee_city,
            emp2.employee_country,
            employee_list.employeeName as managerName,
            employee_list.employeeTitle as managerTitle,
            employee_list.employee_city as managerCity,
            employee_list.employee_country as managerCountry,
            employee_list.path || ',' || emp2.employeeName as path,
            emp2.reportsTo
        From employees emp2, employee_list
        where emp2.reportsTo = employee_list.employeeID
        
    )
    Select
        employeeID,
        employeeName,
        employeeTitle,
        employee_city,
        employee_country,
        managerName,
        managerTitle,
        Case when managerCity is null then employee_city else managerCity end as managerCity,
        Case when managerCountry is null then employee_country else managerCountry end as managerCountry,
        path,
        reportsTo
    From employee_list;
'''
employees = pd.read_sql_query(query_string, conn)
print(employees.head(10))

order_details = pd.read_csv('Data\order_details.csv',encoding = 'utf-8')
order_details.rename(columns={'unitPrice':'order_details_unit_price'}, inplace=True)
order_details['Revenue'] = (order_details['order_details_unit_price']  - order_details['discount'])* order_details['quantity']
print(order_details.columns)
print(order_details.head(10))

orders = pd.read_csv('Data\orders.csv',encoding = 'utf-8')
print(orders.columns)
print(orders.head(10))

products = pd.read_csv('Data\products.csv',encoding = 'ISO-8859-1')
products.rename(columns={'unitPrice':'product_unit_price'}, inplace=True)
print(products.columns)
print(products.head(10))


shippers = pd.read_csv('Data\shippers.csv',encoding = 'utf-8')
shippers.rename(columns={'companyName':'shipperName'}, inplace=True)
print(shippers.columns)
print(shippers.head(10))

df = employees.merge(right=orders, how='left',on='employeeID')
print(df.head(10))
print(df.columns)

df = df.merge(right=customers, on='customerID')
print(df.head(10))
print(df.columns)

df = df.merge(right=order_details, on='orderID')
print(df.head(10))
print(df.columns)

df = df.merge(right=products,on='productID')
print(df.head(10))
print(df.columns)

df = df.merge(right=categories, on='categoryID')
print(df.head(10))
print(df.columns)

df = df.merge(right=shippers, on='shipperID')
print(df.head(10))
print(df.columns)

df.to_csv('Data\data.csv')
