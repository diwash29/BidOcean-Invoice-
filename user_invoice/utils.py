import calendar
from datetime import datetime
from leave.models import LeaveRequest
from .models import Invoice


def get_first_n_last_day(year,month):
	first_n_last = calendar.monthrange(year, month)
	first_day    = datetime.strptime(str(year)+"-"+str(month)+"-"+str(first_n_last[0]),"%Y-%m-%d").date()
	last_day     = datetime.strptime(str(year)+"-"+str(month)+"-"+str(first_n_last[1]),"%Y-%m-%d").date()
	return (first_day, last_day)


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

def check_invoice(employee):
	today          = datetime.today()
	current_month  = today.month
	current_year   = today.year
	start_end_date = get_first_n_last_day(today.year, today.month) 
	invoice        = Invoice.objects.filter(emp_ownwer=employee, monthdate__gte=start_end_date[0], monthdate__lte=start_end_date[1])
	if not invoice:
		return None
	else:
		return invoice[0].pk
