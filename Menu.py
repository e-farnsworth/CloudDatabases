import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

from Income import SingleIncome, HourlyIncome, SalaryIncome
from Expense import Expense
from Budget import WeeklyBudget, YearlyBudget

cred = credentials.Certificate("JSONFiles/finance-manager-b9e75-firebase-adminsdk-yxfff-447a73af8b.json")
finance_app = firebase_admin.initialize_app(cred)

db = firestore.client() # Data Base


def push_to_cloud(cloud_dict, expense=False):
    ''' 
    Takes a prepared dictionary and boolean expense
    saves dictionary to the cloud
    '''
    name = cloud_dict['name']
    
    if expense == True:
        save_type = 'expense'
    else:
        save_type = cloud_dict['type']

    db.collection(save_type).document(f'{name}').set(cloud_dict)

    return

def delete_from_cloud(cloud_dict, expense=False):
    ''' 
    Takes a prepared dictionary and boolean expense
    deletes the selected document
    '''
    name = cloud_dict['name']
    
    if expense == True:
        col_name = 'expense'
    else:
        col_name = cloud_dict['type']

    db.collection(col_name).document(f'{name}').delete()
    return

def get_all_from_cloud(col_name):
    '''
    gets all the documents from a collection returns a list of dictionaries

    Collection names:
    - 'single' (income)
    - 'hourly' (income)
    - 'salary' (income)
    - 'weekly' (budget)
    - 'yearly' (budget)
    - 'expense' (expense)
    - 'budgetexpenses' (expenses for a budget)

    Use get_one_from_cloud for information in 'budgetexpenses'
    '''
    docs = db.collection(col_name).stream() # gets all of the documents from the called collection.
    dict_list = [] # list of dictionaries
    for doc in docs:
        dict_doc = doc.to_dict()
        dict_list.append(dict_doc)
    
    return dict_list

def get_one_from_cloud(doc_name, col_name='budgetexpenses'):
    '''
    Used mainly to get the specific budget expense information
    '''
    doc_ref = db.collection(col_name).document(doc_name)
    doc = doc_ref.get()
    if doc.exists:
        cloud_dict = doc.to_dict()
        return cloud_dict
    else:
        print('No Such Document')
        return

''' Menu Class'''
class Menu:

    def __init__(self):
        self.location = "menu main"
        self.choice = '0'
        self.working_list = list # this will store the information that the user is curently working with before pushing changes to the cloud
    
    ''' Main Menu'''
    def main_menu(self):
        self.location = 'menu main'
        print('\nMain Menu\n')
        print('Would you like to:')
        print('1. Open Incomes')
        print('2. Open Expenses')
        print('3. Open Budgets')
        print('4. Quit\n')
        self.make_choice()

    ''' Income Menu '''
    def income_menu(self):
        self.location = 'income main'
        print('\nIncomes Menu\n')
        print('Would you like to:')
        print('1. View Incomes')
        print('2. Add an Income')
        print('3. Back to Menu\n')
        self.make_choice()

    def view_income_menu(self):
        ''' Get information from the cloud and displays '''
        self.location = 'income view'
        self.working_list = [] # make sure there is no residue from another method. Note: clear was giving issues
        print('\nView all Incomes\n')
        
        # Convert the dictionaries back into their respective classes
        print('--One Time Incomes--')
        single_dicts = get_all_from_cloud('single') # all documents in the 'single' collection
        if len(single_dicts) > 0:
            for single_dict in single_dicts:
                new_income = SingleIncome()
                new_income.set_information(single_dict)
                self.working_list.append(new_income)
                print(new_income.return_summary())
        else:
            print('No Saved Information')

        print('--Weekly Incomes---')
        hourly_dicts = get_all_from_cloud('hourly') # all documents in the 'hourly' collection
        if len(hourly_dicts) > 0:
            for hourly_dict in hourly_dicts:
                new_income = HourlyIncome()
                new_income.set_information(hourly_dict)
                self.working_list.append(new_income)
                print(new_income.return_summary())
        else:
            print('No Saved Information')

        print('--Salary Incomes--')
        salary_dicts = get_all_from_cloud('salary') # all documents in the 'salary' collection
        if len(salary_dicts) > 0:
            for salary_dict in salary_dicts:
                new_income = SalaryIncome()
                new_income.set_information(salary_dict)
                self.working_list.append(new_income)
                print(new_income.return_summary())
        else:
            print('No Saved Information')

        if len(self.working_list) == 0:
            self.choice = '0'
            self.nav()

        print('Would you like to:')
        print('1. Edit Income')
        print('2. Back to Menu\n')
        self.make_choice()

    def edit_income_menu(self):
        ''' edit the details of an income '''
        self.location = 'income edit'
        i = 1
        for item in self.working_list: # list all incomes
            print(f'{i}: {item.return_summary()}')
            i+=1
        
        if len(self.working_list) == 0:
            print('No Saved Information')
            self.choice = '0'
            self.nav()

        exp_index = int(input('Input the index of the expense you want to edit: ')) - 1
        income = self.working_list[exp_index] # Extract the epxense
        
        # Edit the income
        print('\nWould you like to:')
        print('1. Edit the name')
        print('2. Edit the amount details')
        print('3. Delete this Income')
        choice = input('Enter your choice: ')
        print('=========================')
        # income list [type, name, total, wage, hours] last two only for 'hourly' types
        if choice == '1': # name is used as the doc name, so have to delete the original instance to properly update
            name_orig = income.get_cloud_summary()
            delete_from_cloud(name_orig) # deleting the original instance
            income.edit_information('name')
            cloud_dict = income.get_cloud_summary()
            push_to_cloud(cloud_dict)
        elif choice == '2': # updating total informaiton
            income.edit_information('total')
            cloud_dict = income.get_cloud_summary()
            push_to_cloud(cloud_dict)
        elif choice == '3':
            del self.working_list[exp_index] # delete from the list to reflect cloud
            cloud_dict = income.get_cloud_summary()
            delete_from_cloud(cloud_dict) # delete from the cloud

        #upload changes to the cloud
        print('Changes Saved')
        print('\nWould you like to:')
        print('1. Edit another Income')
        print('2. Back to Income Menu\n')
        self.make_choice()

    def add_income_menu(self):
        self.location = 'income add'
        print('\nAdd an Income\n')
        print('What type of Income would you like to add?')
        print('1. One time')
        print('2. Weekly')
        print('3. Salary')
        print('4. Back to Menu\n')
        self.make_choice()

    def onetime_income(self):
        '''Add a one time income'''
        self.location = 'income onetime'
        print('\nAdd a One Time type Income\n')
        new_income = SingleIncome()
        new_income.create_information()

        income_dict = new_income.get_cloud_summary()
        push_to_cloud(income_dict)

        print('Income Saved')
        print('\nWould you like to:')
        print('1. Add another Income')
        print('2. Back to Income Menu\n')
        self.make_choice()

    def hourly_income(self):
        self.location = 'income hourly'
        print('\nAdd a Hourly Waged type Income\n')
        new_income = HourlyIncome()
        new_income.create_information()

        income_dict = new_income.get_cloud_summary()
        push_to_cloud(income_dict)
        
        print('Income Saved')
        print('\nWould you like to:')
        print('1. Add another Income')
        print('2. Back to Income Menu\n')
        self.make_choice()

    def salary_income(self):
        self.location = 'income salary'
        print('\nAdd a Salary type Income\n')
        new_income = SalaryIncome()
        new_income.create_information()

        income_dict = new_income.get_cloud_summary()
        push_to_cloud(income_dict)
        
        print('Income Saved')
        print('\nWould you like to:')
        print('1. Add another Income')
        print('2. Back to Income Menu\n')
        self.make_choice()

    ''' Expense Menu '''
    def expense_menu(self):
        self.location = 'expense main'
        print('\nExpenses Menu\n')
        print('Would you like to:')
        print('1. View Expenses')
        print('2. Add an Expense')
        print('3. Back to Menu\n')
        self.make_choice()

    def view_expense_menu(self):
        ''' Get information from the cloud and displays '''
        self.working_list = [] # make sure there is no residue from another method. Note: clear was giving issues
        self.location = 'expense view'
        print('\nView all Expenses\n')
        
        # Convert the dictionaries back into their respective classes
        print('--All Expenses--')
        expense_dicts = get_all_from_cloud('expense') # all documents in the 'expense' collection
        if len(expense_dicts) > 0:
            for expense_dict in expense_dicts:
                new_expense = Expense() 
                new_expense.set_information(expense_dict)
                self.working_list.append(new_expense)
                print(new_expense.return_summary())
        else:
            print('No Saved Information')
            self.choice = '0'
            self.nav()

        print('Would you like to:')
        print('1. Edit an Expense') # edit or delete an expense
        print('2. Back to Menu\n')
        self.make_choice()

    def edit_expense_menu(self):
        ''' edit the details of an expense '''
        self.location = 'expense edit'
        print('\nEdit Expenses\n')
        i = 1
        for item in self.working_list: # list all expenses
            print(f'{i}: {item.return_summary()}')
            i+=1

        exp_index = int(input('Input the index of the expense you want to edit: ')) - 1
        expense = self.working_list[exp_index] # Extract the epxense
        
        # Edit the expense
        print('\nWould you like to:')
        print('1. Edit the date')
        print('2. Edit the name')
        print('3. Edit the amount')
        print('4. Delete this Income')
        choice = input('Enter your choice: ')
        print('=========================')
        # expense list [foramted date, name, expense total]

        if choice == '1':
            expense.edit_information('date')
            cloud_dict = expense.get_cloud_summary()
            push_to_cloud(cloud_dict, True)
        elif choice == '2': # name is used as the doc name, so have to delete the original instance to properly update
            name_orig = expense.get_cloud_summary()
            delete_from_cloud(name_orig, expense=True) # deleting the original instance
            expense.edit_information('name')
            cloud_dict = expense.get_cloud_summary()
            push_to_cloud(cloud_dict, True)
        elif choice == '3':
            expense.edit_information('total')
            cloud_dict = expense.get_cloud_summary()
            push_to_cloud(cloud_dict, True)
        elif choice == '4':
            del self.working_list[exp_index]
            cloud_dict = expense.get_cloud_summary()
            delete_from_cloud(cloud_dict, expense=True)

        #upload changes to the cloud
        print('Changes Saved')
        print('\nWould you like to:')
        print('1. Edit another Expense')
        print('2. Back to Expense Menu\n')
        self.make_choice()

    def add_expense_menu(self):
        self.location = 'expense add'
        print('\nAdd an Expense\n')
        new_expense = Expense()
        new_expense.create_information()
        cloud_dict = new_expense.get_cloud_summary()
        push_to_cloud(cloud_dict, True)
        print('Expense Saved')
        print('\nWould you like to:')
        print('1. Add another Expense')
        print('2. Back to Expenses Menu\n')
        self.make_choice()

    ''' Budget Menu '''
    def budget_menu(self):
        self.location = 'budget main'
        print('\nBudgets Menu\n')
        print('Would you like to:')
        print('1. View Budgets')
        print('2. Add a Budget')
        print('3. Back to Menu\n')
        self.make_choice()
    
    def view_budget_menu(self):
        ''' Get information from the cloud and displays '''
        self.working_list = [] # make sure there is no residue from another method. Note: clear was giving issues
        self.location = 'budget view'
        print('\nView all Expenses\n')
        
        # Convert the dictionaries back into their respective classes
        print('--Weekly Budgets--')
        budgets_dicts = get_all_from_cloud('weekly') # all documents in the 'weekly' collection
        if len(budgets_dicts) > 0:
            for budgets_dict in budgets_dicts:
                new_budget = WeeklyBudget() 
                new_budget.set_information(budgets_dict)
                self.working_list.append(new_budget)
                print(new_budget.return_summary())
        else:
            print('No Saved Information')

        print('--Yearly Budgets--')
        budgets_dicts = get_all_from_cloud('yearly') # all documents in the 'yearly' collection
        if len(budgets_dicts) > 0:
            for budgets_dict in budgets_dicts:
                new_budget = YearlyBudget() 
                new_budget.set_information(budgets_dict)
                self.working_list.append(new_budget)
                print(new_budget.return_summary())
        else:
            print('No Saved Information')

        if len(self.working_list) == 0:
            self.choice = '0'
            self.nav()

        print('Would you like to:')
        print('1. Edit a Budget') # edit or delete an expense
        print('2. Back to Menu\n')
        self.make_choice()

    def edit_budget_menu(self):
        self.location = 'budget edit'
        print('\nEdit a Budget\n')
        i = 1
        for item in self.working_list: # list all budgets
            print(f'{i}: {item.return_summary()}')
            i+=1
        
        if len(self.working_list) == 0:
            print('No Saved Information')
            self.choice = '0'
            self.nav()

        bud_index = int(input('Input the index of the budget you want to edit: ')) - 1
        budget = self.working_list[bud_index] # Extract the Budget
        print('=========================')
        # load the budget details
        working_dict = budget.get_cloud_summary()
        name = working_dict['name']
        bud_type = working_dict['type']
        expenses_dict = get_one_from_cloud(f'{bud_type}{name}')
        if expenses_dict == 'No Such Document':
            print('Error loading Budget Expenses')
            self.choice = '0'
            self.nav()
        else:
            budget.set_expenses(expenses_dict)

        # list the expenses
        budget.view_budget()

        # Edit the expense
        print('\nWould you like to:')
        print('1. Edit the name')
        print('2. Edit Ecpected Expenses')
        print('3. Delete this Budget')
        choice = input('Enter your choice: ')
        print('=========================')
        # budget list [type, name, total, expense list]

        if choice == '1': # name is used as the doc name, so have to delete the original instance to properly update
            name_orig = budget.get_cloud_summary()
            get_name = name_orig['name']
            get_type = name_orig['type']
            exp_orig = f'{get_type}{get_name}'
            orig_expense = get_one_from_cloud(exp_orig)

            delete_from_cloud(name_orig) # deleting the original instance
            db.collection('budgetexpenses').document(exp_orig).delete() # deleting the original expenses
            
            budget.edit_information('name')
            cloud_dict = budget.get_cloud_summary()
            new_type = cloud_dict['type']
            new_name = cloud_dict['name']
            exp_new = f'{new_type}{new_name}' # new name for the expenses
            
            #push the original budget expenses with the new name
            db.collection('budgetexpenses').document(exp_new).set(orig_expense)
            push_to_cloud(cloud_dict)

        elif choice == '2': # edit expensess
            budget.edit_information('expenses')
            name_orig = budget.get_cloud_summary()
            get_name = name_orig['name']
            get_type = name_orig['type']
            name = f'{get_type}{get_name}'

            cloud_dict = budget.get_cloud_summary()
            exp_cloud_dict = budget.get_cloud_expense()
            # Push the changes
            db.collection('budgetexpenses').document(name).set(exp_cloud_dict)
            push_to_cloud(cloud_dict) #in case total changes

        elif choice == '3':
            del self.working_list[bud_index]
            name_orig = budget.get_cloud_summary()
            get_name = name_orig['name']
            get_type = name_orig['type']
            exp_name = f'{get_type}{get_name}'
            
            db.collection('budgetexpenses').document(exp_name).delete() # delete the expenses as well
            delete_from_cloud(name_orig)

        #upload changes to the cloud
        print('Changes Saved')
        print('\nWould you like to:')
        print('1. Edit another Budget')
        print('2. Back to Budget Menu\n')
        self.make_choice()

    def add_budget_menu(self):
        self.location = 'budget add'
        print('\nCreate a Budget\n')
        print('What type of Budget would you like to add?')
        print('1. Weekly')
        print('2. Yearly')
        print('3. Back to Menu\n')
        self.make_choice()

    def weekly_budget(self):
        self.location = 'budget weekly'
        print('\nAdd a Weekly Budget\n')
        new_budget = WeeklyBudget()
        new_budget.create_budget_name()
        budget_done = False
        while budget_done != True:
            print('\nWould you like to:')
            print('1. Add an Expense')
            print('2. Edit an Expense') # edit or delete an expense
            print('3. Save your Budget\n')
            budget_choice = input('Enter your choice: ')
            print('=========================')
            if budget_choice == '1':
                new_budget.add_expense()
            elif budget_choice =='2':
                new_budget.edit_expense_full()
            elif budget_choice == '3':
                budget_done = True
                cloud_dict = new_budget.get_cloud_summary()
                name = cloud_dict['name']
                bud_type = cloud_dict['type']
                push_to_cloud(cloud_dict)
                cloud_dict = new_budget.get_cloud_expense()
                
                db.collection('budgetexpenses').document(f'{bud_type}{name}').set(cloud_dict)
                
                print('Budget Saved')
            else:
                print('Choice is out of range. Please choose again.')
        print('\nWould you like to:')
        print('1. Create another Budget')
        print('2. Back to Budget Menu\n')
        self.make_choice()

    def yearly_budget(self):
        self.location = 'budget yearly'
        print('\nAdd a Yearly Budget\n')
        new_budget = YearlyBudget()
        new_budget.create_budget_name()
        budget_done = False
        while budget_done != True:
            print('\nWould you like to:')
            print('1. Add an Expense')
            print('2. Edit an Expense') # edit or delete an expense
            print('3. Save your Budget\n')
            budget_choice = input('Enter your choice: ')
            print('=========================')
            if budget_choice == '1':
                budget_done = False
                new_budget.add_expense()
            elif budget_choice =='2':
                new_budget.edit_expense_full()
            elif budget_choice == '3':
                budget_done = True
                cloud_dict = new_budget.get_cloud_summary()
                name = cloud_dict['name']
                bud_type = cloud_dict['type']
                push_to_cloud(cloud_dict)
                cloud_dict = new_budget.get_cloud_expense()
                
                db.collection('budgetexpenses').document(f'{bud_type}{name}').set(cloud_dict)
                print('Budget Saved')
            else:
                print('Choice is out of range. Please choose again.')
        print('\nWould you like to:')
        print('1. Create another Budget')
        print('2. Back to Budget Menu\n')
        self.make_choice()

    def make_choice(self):
        '''Uniform question used for navigation question'''
        self.choice = input('Enter your choice: ')
        print('=========================')
        self.nav()

    ''' Navigation '''
    def nav(self):
        '''Handles all navegation'''
        # Main Menu Nav
        if self.location == 'menu main':
            if self.choice == '0': # Initial View
                print('Welcome to your personal Finance Manager')
                self.main_menu()
            if self.choice == '1': # view incomes
                self.income_menu()
            elif self.choice == '2': # view expenses
                self.expense_menu()
            elif self.choice == '3': # view budgets
                self.budget_menu()         
            elif self.choice == '4': # quit
                # end program
                return  
            else:
                print('Choice is out of range. Please choose again.')
                self.main_menu()
        # Income Main Nav
        if self.location == 'income main':
            if self.choice == '1': # view incomes
                self.view_income_menu() 
            elif self.choice == '2': # Add income
                self.add_income_menu()
            elif self.choice == '3': # back to main menu
                self.main_menu()
            else:
                print('Choice is out of range. You will be redirected to the Main Menu.')
                self.main_menu()
        # View Income Nav
        if self.location == 'income view':
            if self.choice == '0': # no incomes saved
                self.income_menu()
            if self.choice == '1': # edit income
                self.edit_income_menu()
            elif self.choice == '2': # back to main menu
                self.main_menu()
            else:
                print('Choice is out of range. You will be redirected to the Main Menu.')
                self.main_menu()
        # Edit Income Nav
        if self.location == 'income edit':
            if self.choice == '1': # edit another income
                self.edit_income_menu()
            elif self.choice == '2': # back to main menu
                self.income_menu()
            else:
                print('Choice is out of range. You will be redirected to the Income Menu.')
                self.income_menu()
        # Add Income Nav
        if self.location == 'income add':
            if self.choice == '1': # add one time income
                self.onetime_income()
            elif self.choice == '2': # add hourly income
                self.hourly_income()
            elif self.choice == '3': # add salary income
                self.salary_income()
            elif self.choice == '4': # back to main menu
                self.main_menu()
            else:
                print('Choice is out of range. You will be redirected to the Main Menu.')
                self.main_menu()
        # After adding Income Nav
        if self.location in ['income onetime', 'income hourly', 'income salary']:
            if self.choice == '1': # Add another income
                self.add_income_menu()
            elif self.choice == '2': # back to main menu
                self.main_menu()
            else:
                print('Choice is out of range. You will be redirected to the Income Menu.')
                self.income_menu()
        # Expense Main Nav
        if self.location == 'expense main':    
            if self.choice == '1': # view expenses
                self.view_expense_menu()
            elif self.choice == '2': # add expense
                self.add_expense_menu()
            elif self.choice == '3': # back to main menu
                self.main_menu()
            else:
                print('Choice is out of range. You will be redirected to the Main Menu.')
                self.main_menu()
        # View Expense Nav
        if self.location == 'expense view':
            if self.choice == '0': # no expenses saved
                self.expense_menu()     
            if self.choice == '1': # Add expense
                self.edit_expense_menu()
            elif self.choice == '2': # back to main menu
                self.main_menu()
            else:
                print('Choice is out of range. You will be redirected to the Main Menu.')
                self.main_menu()
        # Edit Expense Nav
        if self.location == 'expense edit': 
            if self.choice == '1': # edit another expense
                self.edit_expense_menu()
            elif self.choice == '2': # back to expense menu
                self.expense_menu()
            else:
                print('Choice is out of range. You will be redirected to the Main Menu.')
                self.expense_menu()              
        # Add Expense Nav
        if self.location == 'expense add':   
            if self.choice == '1': # Add expense
                self.add_expense_menu()
            elif self.choice == '2': # back to expense menu
                self.expense_menu()
            else:
                print('Choice is out of range. You will be redirected to the Expenses Menu.')
                self.expense_menu()
        # Budget Main Nav
        if self.location == 'budget main':
            if self.choice == '1': # view a budget 
                self.view_budget_menu()
            elif self.choice == '2': # add a budget
                self.add_budget_menu()
            elif self.choice == '3': # back to main menu
                self.main_menu()
            else:
                print('Choice is out of range. You will be redirected to the Main Menu.')
                self.main_menu()
        # View Budget Nav
        if self.location == 'budget view':
            if self.choice == '0': # no budgets saved
                self.budget_menu()   
            if self.choice == '1': # edit a budget 
                self.edit_budget_menu()
            elif self.choice == '2': # add a budget
                self.main_menu()
            else:
                print('Choice is out of range. You will be redirected to the Main Menu.')
                self.main_menu()
        # Edit Budget Nav
        if self.location == 'budget edit':
            if self.choice == '0': # no budgets saved
                self.budget_menu()   
            if self.choice == '1': # edit a budget 
                self.edit_budget_menu()
            elif self.choice == '2': # add a budget
                self.budget_menu()
            else:
                print('Choice is out of range. You will be redirected to the Budget Menu.')
                self.budget_menu()
        # Add Budget Menu
        if self.location == 'budget add':
            if self.choice == '1': # Create weekly budget
                self.weekly_budget()
            elif self.choice == '2': # create yearly budget
                self.yearly_budget()
            elif self.choice == '3': # go back to main menu
                self.main_menu()
            else:
                print('Choice is out of range. You will be redirected to the Main Menu.')
                self.main_menu()
        # After making Budget Nav
        if self.location in ['budget yearly', 'budget weekly']:
            if self.choice == '1': # Create another budget
                self.add_budget_menu()
            elif self.choice == '2': # back to budget menu
                self.budget_menu()
            else:
                print('Choice is out of range. You will be redirected to the Budget Menu.')
                self.budget_menu()

''' Main function'''
def main():
    start_app = Menu()
    start_app.nav()

if __name__ == '__main__':
    main()

'''
Notes for updates
Summary for expenses uses date to call only recent expenses (future update)
Add naming warning to all naming procedures
'''