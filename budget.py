class Category:

  def __init__(self, category):
    self.category = category
    self.ledger = []

  # When the budget object is printed it should display:
  # - A title line of 30 characters where the name of the category is centered in a line of * characters.
  # - A list of the items in the ledger.
  #   Each line should show the description and amount.
  #   The first 23 characters of the description should be displayed, then the amount.
  #   The amount should be right aligned, contain two decimal places, and display a maximum of 7 characters.
  # - A line displaying the category total.
  def __str__(self):

    category_line = self.category.center(30, '*') + '\n'

    ledger_items = ''
    for ledger_item in self.ledger:

      # NOT PROUD OF THIS!
      ledger_line = ''
      description = ledger_item.get('description')[0:23].ljust(23)
      amount = ('{0:.2f}'.format(ledger_item.get('amount'))).rjust(7)
      ledger_line = description + amount + '\n'

      ledger_items += ledger_line

    total_line = 'Total: ' + str(self.get_balance())

    return category_line + ledger_items + total_line

  def deposit(self, amount, description=''):
    self.ledger.append({'amount': amount, 'description': description})

  # A withdraw method that is similar to the deposit method,
  # but the amount passed in should be stored in the ledger as a negative number.
  # If there are not enough funds, nothing should be added to the ledger.
  # This method should return True if the withdrawal took place, and False otherwise.
  def withdraw(self, amount, description=''):

    if self.check_funds(amount):
      self.ledger.append({'amount': -abs(amount), 'description': description})
      return True
    else:
      return False

  # A get_balance method that returns the current balance of the budget category
  # based on the deposits and withdrawals that have occurred.
  def get_balance(self):

    balance = 0

    for i in range(0, len(self.ledger)):
      balance += float(self.ledger[i].get('amount'))

    return balance

  # A transfer method that accepts an amount and another budget category as arguments.
  # The method should add a withdrawal with the amount
  # and the description "Transfer to [Destination Budget Category]".
  # The method should then add a deposit to the other budget category with the amount
  # and the description "Transfer from [Source Budget Category]".
  # If there are not enough funds, nothing should be added to either ledgers.
  # This method should return True if the transfer took place, and False otherwise.
  def transfer(self, amount, category):

    if self.check_funds(amount):
      description_withdraw = 'Transfer to ' + category.category
      description_deposit = 'Transfer from ' + self.category
      self.withdraw(amount, description=description_withdraw)
      category.deposit(amount, description_deposit)
      return True
    else:
      return False

  # A check_funds method that accepts an amount as an argument.
  # It returns False if the amount is greater than the balance of the budget category
  # and returns True otherwise.
  # This method should be used by both the withdraw method and transfer method.
  def check_funds(self, amount):

    balance = self.get_balance()
    if amount > balance:
      return False
    else:
      return True


# Besides the Category class, create a function (outside of the class)
# called create_spend_chart that takes a list of categories as an argument.
# It should return a string that is a bar chart.
# The chart should show the percentage spent in each category passed in to the function.
# The percentage spent should be calculated only with withdrawals and not with deposits.
def create_spend_chart(categories):

  # It's about the percentage of the spendings in one category against all spendings
  spendings_total = get_spendings_total(categories)

  # Now that I have all spendings I have to get the percentage of the individual spendings
  # Storing the information as alist of dictionaries
  percentages = []

  for category in categories:

    percentage = {
      'category': category.category,
      'percentage': abs((get_spendings(category) / spendings_total) * 100)
    }

    percentages.append(percentage)

  # Create percentage lines
  percentage_lines = ""

  # txt.rjust(20)
  i = 100
  while i >= 0:
    percentage_line = (str(i) + '|').rjust(4)
    for item in percentages:      
      if item.get('percentage') > i:        
        percentage_line += ' o '
      else:
        percentage_line += '   '

    percentage_line += ' \n'
    percentage_lines += percentage_line
    i = i - 10

  # Do I need to handle the line length based on the number of categories?
  # entries in spending_percentages?
  # Apparently not.
  divider_line = '    ----------\n'

  # print the categories
  # what if I just extract the category names first
  category_names = []

  for spending_percentage in percentages:
    category_names.append(spending_percentage.get('category'))

  # get max lenght nad make all categories same length
  maxlen = len(max(category_names, key=len))

  category_names_adjusted = [
    line.ljust(maxlen, ' ') for line in category_names
  ]

  # zip the category names
  category_names_adjusted_zipped = zip(*category_names_adjusted)

  category_lines = ""
  # print them vertically
  for i in category_names_adjusted_zipped:
    line = '    '
    for j in range(0, len(list(i))):
      line += ' ' + list(i)[j] + ' '
      
    line += ' \n' 
    
    category_lines += line

  header_line = 'Percentage spent by category\n'

  return header_line + percentage_lines + divider_line + category_lines.rstrip('\n')
  


###################################################################
# Gets the total spendings of a category
###################################################################
def get_spendings(category):
  spendings_per_category = 0
  for ledger in category.ledger:
    amount = ledger.get('amount')
    # spending (not deposit)
    if amount < 0:
      spendings_per_category += abs(amount)

  return spendings_per_category


###################################################################
# Gets the total spendings (all categories)
###################################################################
def get_spendings_total(categories):
  total_spendings = 0

  for category in categories:
    total_spendings += get_spendings(category)

  return total_spendings
