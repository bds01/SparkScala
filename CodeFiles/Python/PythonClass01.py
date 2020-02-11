class Employee:

    def __init__(self, first, last, pay):
        self.first = first
        self.last = last
        self.pay = pay
        self.email = first+'.'+last+'@company.com'
        
    def Fullname(self):
        return '{} {}'.format(self.first, self.last)


emp_1 = Employee('Earl','Thomas',300000)
emp_2 = Employee('Kareem','Hunt',200000)

print(emp_1.email)
print(emp_1.pay)
print(emp_1.Fullname())
print(Employee.Fullname(emp_1))
