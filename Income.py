

class Income:
    ''' Create, Delete, and Manage Incomes '''

    def __init__(self): 
        ''' Each income has one of these '''
        self.name = None # User Generated
        self.type = None # Single, Hourly, Salary
        self.total = None # calculated for hourly

    def create_information(self):
        '''Orignial Creation of information'''
        print('Warning: Names must be unique')
        self.name = input('Name for this Income: ')
        self.total = float(input('Income Amount: $'))

    def set_information(self, cloud_dict):
        '''
        convert from cloud dictionary to income
        '''
        self.type = cloud_dict['type']
        self.name = cloud_dict['name']
        self.total = cloud_dict['total']
        
    def get_cloud_summary(self):
        '''
        dictionary for the cloud
        {type, name, total}
        '''
        cloud_dict = {'type': self.type, 
                       'name': self.name, 
                       'total': self.total}
        return cloud_dict
    
    def edit_information(self, type):
        '''type is the information that is being edited'''
        if type == 'name':
            self.name = input('New Income name: ')
        elif type == 'total':
            self.total = float(input('New total: '))

    def return_summary(self):
        '''Prints the name and total of an income'''
        return f'{self.name}: ${self.total:.2f}'

''' Child Classes '''
class SingleIncome(Income): 
    '''
    sets type
    '''
    def __init__(self):
        super().__init__()
        self.type = "single"

class HourlyIncome(Income):
    ''' 
    sets type
    '''
    def __init__(self):
        super().__init__()
        self.type = "hourly"
        self.wage = None
        self.hours = None

    def create_information(self):
        '''Orignial Creation of information'''
        print('Warning: Income names must be unique')
        self.name = input('Name this income: ')
        self.wage = float(input('Wage: $'))
        print('Note: When inputting hours, DO NOT include unpaid breaks or lunches')
        self.hours = float(input('Hours per week: '))
        self.total = self.wage*self.hours

    def set_information(self, cloud_dict):
        '''
        convert from cloud dictionary to income
        '''
        self.type = cloud_dict['type']
        self.name = cloud_dict['name']
        self.total = cloud_dict['total']
        self.wage = cloud_dict['wage']
        self.hours = cloud_dict['hours']
        
    def get_cloud_summary(self):
        '''
        dictionary for the cloud
        {type, name, total, wage, hours}
        '''
        cloud_dict = {'type': self.type, 
                       'name': self.name, 
                       'total': self.total, 
                       'wage': self.wage, 
                       'hours': self.hours}
        return cloud_dict

    def edit_information(self, type):
        '''type is the information that is being edited'''
        if type == 'name':
            self.name = input('New Income name: ')
        elif type == 'total':
            self.wage = float(input('New Wage: $'))
            print('Note: When inputting hours, DO NOT include unpaid breaks or lunches')
            self.hours = float(input('New Hours per Week: '))
            self.total = self.wage*self.hours

    def generate_yearly_income(self):
        '''
        Calculates an estimated yearly income
        returns (estimated weekly total) * 52
        '''
        return self.total * 52

class SalaryIncome(Income):
    '''
    sets type
    '''
    def __init__(self):
        super().__init__()
        self.type = "salary"

    def generate_weekly_income(self):
        ''' 
        Calculates an estimated weekly income
        returns salary / 52
        '''
        return self.total / 52
    