# Overview

This project is primarily to learn more about cloud databases and how to interact with them. The program is the first steps at developing a finacial manager. With this program, a user is able to create, edit, and delete all of the following: expenses, incomes, and budgets.

When a user creates an expense, the expense is marked with a date. The user does have the option to use a shortcut to simply use the current date on their device.

A user can create three different types of income: one time, weekly, and salary. One time incomes are for payments that do not automatically reocur. Weekly incomes cover work that has an hourly wage. Salary incomes cover work that has a yearly salary.

A user can also create two types of budgets: weekly and yearly. As the names would sugest, weekly budgets are more for each week while yearly are for the enitre year.

{Video is in progress}

[Software Demo Video](http://youtube.link.goes.here)

# Cloud Database

{Describe the cloud database you are using.}

This project uses Firestore which is a part of Google Firebase.

The database impliments the use of these seven collections

- expense
- single
- hourly
- salary
- weekly
- yearly
- budgetexpenses

The expense collection stores expenses by the name generated by the user. Each expense document stores an expense's date, name, and total.

The single, hourly, and salary collections store income information by the name generated by the user. All income documents store an income's name, total, and type. Hourly documents also store an income's wage and hours.

The weekly, yearly, and budgetexpenses store budget related information. The weekly and yearly collections store a summary of a budget by the name generated by the user. The summary stores a budget's name, total, and type. The specific expense information of each budget is stored in the budgetexpenses collection by a name generated by the type and name of the budget. Each budgetexpenses document store the name and total of each expense of the given budget.

# Development Environment

- Python 3.10
- DateTime
- Google Firebase
- Visual Stdio Code
- Git and Github

# Useful Websites

- [Get started with Cloud Firestore | Firebase](https://firebase.google.com/docs/firestore/quickstart)
- [Add data to Cloud Firestore | Firebase](https://firebase.google.com/docs/firestore/manage-data/add-data)
- [Get data with Cloud Firestore | Firebase](https://firebase.google.com/docs/firestore/query-data/get-data)
- [Delete data from Cloud Firestore | Firebase](https://firebase.google.com/docs/firestore/manage-data/delete-data)
- [Convert date to MM/DD/YYYY format in Python](https://www.mytecbits.com/internet/python/convert-date-to-mm-dd-yyyy)
- [Constructors in Python - GeeksforGeeks](https://www.geeksforgeeks.org/constructors-in-python/)
- [Difference between List and Array in Python - GeeksforGeeks](https://www.geeksforgeeks.org/difference-between-list-and-array-in-python/)
- [NoSQL Tutorial: What is, Types of NoSQL Databases & Example](https://www.guru99.com/nosql-tutorial.html)

# Future Work

- A date based storing and querying system for Expenses
- Alter the save name of expenses to include the date for reocuring expenses
- Creation of budgets that are not weekly or yearly
- Using weekly budgets to generate a mockup for yearly and vice versa
- Budgets interacting with expenses and income for ease of reference
- Fixing various bugs