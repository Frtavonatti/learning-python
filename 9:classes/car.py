# Exercise 9.9
class Car():
  def __init__(self, make, model, year):
    self.make = make
    self.model = model
    self.year = year
    self.odometer = 0
    self.gas_tank = 0

  def fill_tank(self):
    self.gas_tank = 100
  def drive(self, miles):
    self.odometer += miles
    self.gas_tank -= miles
  def update_odometer(self, miles):
    self.odometer = miles
  def get_odometer(self):
    return self.odometer
  def get_gas_tank(self):
    return self.gas_tank

class Battery():
  def __init__(self, size=75):
    self.size = size
    self.charge = 0

  def charge_battery(self):
    self.charge = 100
  def discharge_battery(self):
    self.charge = 0
  def get_charge(self):
    return self.charge
  def get_size(self):
    return self.size
  def upgrade_battery(self):
    if self.size < 85:
      self.size = 85

class ElectricCar(Car):
  def __init__(self, make, model, year):
    super().__init__(make, model, year)
    self.battery = Battery()

  def fill_tank(self):
    print("This car doesn't have a gas tank!")
  def drive(self, miles):
    if self.battery.get_charge() >= miles:
      self.odometer += miles
      self.battery.charge -= miles
    else:
      print("Not enough charge to drive that far!")
  def get_battery(self):
    return self.battery

tesla = ElectricCar("Tesla", "Model S", 2019)
print('Tesla Battery Size: ', tesla.battery.get_size())
tesla.battery.upgrade_battery()
print('Updated Battery Size: ', tesla.battery.get_size())
