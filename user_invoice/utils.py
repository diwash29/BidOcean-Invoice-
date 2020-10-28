import calendar
from datetime import datetime
from leave.models import LeaveRequest
from .models import Invoice, ProductionReport


def get_first_n_last_day(year,month):
	first_n_last = calendar.monthrange(year, month)
	first_day    = datetime.strptime(str(year)+"-"+str(month)+"-"+str('01'),"%Y-%m-%d").date()
	last_day     = datetime.strptime(str(year)+"-"+str(month)+"-"+str(first_n_last[1]),"%Y-%m-%d").date()
	return (first_day, last_day)


def listToString(s):  
    
    # initialize an empty string 
    str1 = ""  
    
    # traverse in the string   
    for ele in s:  
        str1 += ele   
    
    # return string   
    return str1 


def count_leaves(employee, date):
	current_month  = date.month
	current_year   = date.year
	start_end_date = get_first_n_last_day(current_year, current_month) 
	app_leaves     = LeaveRequest.objects.filter(employee=employee, status=1, from_date__gte=start_end_date[0], from_date__lte=start_end_date[1])
	leaves = 0
	if not app_leaves:
	    leaves = leaves
	else: 
	    for l in app_leaves:
	    	if int(l.requesting_days)>int(l.available_days):
	        	leaves += int(l.requesting_days) - int(l.available_days)
	return leaves    

def count_file_uploads(employee, date):
	current_month      = date.month
	current_year       = date.year
	start_end_date     = get_first_n_last_day(current_year, current_month) 
	file_uploads_query = ProductionReport.objects.filter(employee=employee, date__gte=start_end_date[0], date__lte=start_end_date[1])
	file_upload = 0
	if not file_uploads_query:
	    file_upload = file_upload
	else: 
	    for f in file_uploads_query:
	    	file_upload += int(f.file_attach)
	return file_upload    	    

def check_invoice(employee):
	today          = datetime.today()
	current_month  = today.month
	current_year   = today.year
	start_end_date = get_first_n_last_day(today.year, today.month) 
	# print(start_end_date)
	invoice        = Invoice.objects.filter(emp_ownwer=employee, monthdate__gte=start_end_date[0], monthdate__lte=start_end_date[1])
	if not invoice:
		return None
	else:
		return invoice[0].pk



class Currency_convertor: 
    # empty dict to store the conversion rates 
    rates = {}  
    def __init__(self, url): 
        data = requests.get(url).json() 
  
        # Extracting only the rates from the json data 
        self.rates = data["rates"]  
  
    # function to do a simple cross multiplication between  
    # the amount and the conversion rates 
    def convert(self, from_currency, to_currency, amount): 
        initial_amount = amount 
        if from_currency != 'EUR' : 
            amount = amount / self.rates[from_currency] 
  
        # limiting the precision to 2 decimal places 
        amount = round(amount * self.rates[to_currency]) 
        return amount		
