

class Budget():
    ''' Create, Delete, and Manage Budgets '''

    def __init__(self): 
        ''' Each budget has one of these '''
        self.name = None # User Generated
        self.bud_type = None # Weekly, Yearly, Other
        self.total = 0.00

        # Initiating a list for expenses
        self.expense_list = []
    # class OtherBudget(): # For now will be for a future update
    #     '''
    #     sets bud_type
    #     sets timeframe (maybe)
    #     '''
    #     def __init__(self):
    #         super().__init__()
    #         self.bud_type = "other"

    class ExpenseBudget():
        '''
        each expense has a 
            name/type of expense
            amount
        '''
        def __init__(self):
            '''Initilize expense'''
            super().__init__()
            self.exp_name = str
            self.exp_amount = float

        def create_expense(self):
            '''Set the information for the expense'''
            self.exp_name = input("Expense Name: ")
            self.exp_amount = float(input("Expected Expense Amount: $"))

        def return_expense_info(self):
            return f'{self.exp_name}: ${self.exp_amount:.02f}'
        
        def edit_expense_info(self, edit):
            '''edit is what is being edited'''
            if edit == 'name':
                self.exp_name = input('New Expense Name: ')
            else:
                self.exp_amount = float(input('New Expected Expense amount: $'))

        def set_expense(self, summary):
            '''takes a summary list [name, amount] and sets the expense'''
            self.exp_name = summary[0]
            self.exp_amount = float(summary[1])

        def get_expense_info(self):
            '''returns [name, amount] for an expense'''
            return [self.exp_name, self.exp_amount]
            
    def create_budget_name(self):
        self.name = input('Name this Budget: ')

    def add_expense(self):
        '''Add an expense to the budget'''
        expense = self.ExpenseBudget()
        expense.create_expense()
        expense_info = expense.get_expense_info()
        self.total += expense_info[1]
        self.expense_list.append(expense)

    def edit_expense_full(self):
        ''' choose to edit or delete an expense'''
        self.view_budget()
        
        print('\nWould you like to:')
        print('1. Add an expense')
        print('2. Edit an expense')
        print('3. Delete an expense')
        choice = input('Enter your choice: ')
        print('=========================')

        if choice == '1':
            self.add_expense()
        elif choice == '2':
            self.edit_expense()
        elif choice == '3':
            self.delete_expense()
        else:
            print('Choice is out of range. You will be redirected to edit Expense.')
            self.edit_expense() 

    def edit_expense(self):
        ''' edit the details of an expense '''
        exp_index = int(input('Input the index of the expense you want to edit: ')) - 1
        expense = self.expense_list[exp_index] # Extract the epxense
        
        # Edit the expense
        print('\nWould you like to:')
        print('1. Edit the name')
        print('2. Edit the amount')
        choice = input('Enter your choice: ')
        print('=========================')

        if choice == '1':
            expense.edit_expense_info('name')
        elif choice == '2':
            expense.edit_expense_info('amount')
        
        # Replace the expense
        self.expense_list[exp_index] = expense

    def delete_expense(self):
        ''' Deletes the chosen expense '''
        exp_index = int(input('Input the index of the expense you want to delete: ')) - 1
        del self.expense_list[exp_index]
    
    def view_budget(self): # Being problem child
        ''' View the entire budget and the expected total'''
        print(f'{self.name}')
        i = 1
        for expense in self.expense_list: # expense info: [name, amount]
            print(f'{i}. {expense.return_expense_info()}')
            i+=1
            
        print(f'\nTotal: ${self.total:.2f}')

    def set_information(self, cloud_dict):
        ''' Reorginize the information after getting it from the cloud'''
        self.bud_type = cloud_dict['type']
        self.name = cloud_dict['name']
        self.total = cloud_dict['total']

    def set_expenses(self, cloud_dict):
        ''' Reorganize the expenses for editing from the cloud '''
        expense_list = [] #this is a list of lists
        for item in cloud_dict:
            working_list = []
            working_list.append(item)
            working_list.append(cloud_dict[item]) # switching the dictionary to a list for ease of access to the key (name of expense)
            expense_list.append(working_list)

        for item in expense_list:
            expense = self.ExpenseBudget()
            expense.set_expense(item)
            if expense not in self.expense_list:
                self.expense_list.append(expense) # this is a list of expenses

    def get_cloud_summary(self):
        '''
        returns: {type, name, total}
        '''
        cloud_dict = {'type': self.bud_type, 
                       'name': self.name, 
                       'total': self.total}
        return cloud_dict
    
    def get_cloud_expense(self): 
        '''
        returns: {name: total}
        '''
        cloud_dict = {}
        for expense in self.expense_list:
            info = expense.get_expense_info()
            cloud_dict[info[0]] = info[1]

        return cloud_dict

    def edit_information(self, edit_type): 
        '''type is the information that is being edited'''
        if edit_type == 'name':
            self.name = input('New Budget name: ')
        elif edit_type == 'expenses':
            self.edit_expense_full()

    def return_summary(self):
        '''Prints the name and total of an income'''
        return f'{self.name}: ${self.total:.2f}'
        
''' Child Classes '''
class WeeklyBudget(Budget):
    ''' 
    Child Class of Budget
    sets type
    '''
    def __init__(self):
        super().__init__()
        self.bud_type = "weekly"

class YearlyBudget(Budget):
    '''
    Chlid Class of Budget
    sets type
    '''
    def __init__(self):
        super().__init__()
        self.bud_type = "yearly"
