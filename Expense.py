from datetime import date

class Expense:
    ''' Create, Delete, and Manage Expenses '''

    def __init__(self): 
        ''' Each expense has one of these '''
        self.name = None # User Generated
        self.total = None
        self.date = None

    def create_information(self):
        '''Used to initially set expense information'''
        self.name = input("Expense Type: ")
        self.total = float(input("Expense Amount: $"))
        print('If you would like to use today\'s date, type \"T\" instead')
        self.date = input('Date of Expense (MM/DD/YYYY): ')
        if self.date == 'T':
            self.date = date.today()
            self.date = date.strftime(self.date, "%m/%d/%Y")

    def set_information(self, cloud_dict):
        '''Used to convert from cloud to Expense'''
        self.date = cloud_dict['date']
        self.name = cloud_dict['name']
        self.total = cloud_dict['total']

    def get_cloud_summary(self):
        ''' 
        Formats the date
        returns: [foramted date, name, expense total]
        '''
        cloud_dict = {'date': self.date, 
                       'name': self.name, 
                       'total': self.total}
        return cloud_dict
    
    def edit_information(self, type):
        '''type is the information that is being edited'''
        if type == 'date':
            print('If you would like to use today\'s date, type \"T\" instead')
            self.date = input('New Date of Expense (MM/DD/YYYY): ')
        elif type == 'name':
            self.name = input("New Expense Type: ")
        elif type == 'total':
            self.total = float(input("New Expense Amount: $"))

    def return_summary(self):
        '''Prints the name and total of an income'''
        return f'{self.name} ({self.date}): ${self.total:.2f}'
