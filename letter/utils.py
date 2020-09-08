from .converter import convertToWords
import math

def get_basic_annually(salary_annually):
    return math.floor((40/100)*salary_annually)


def get_house_rent_allowance_annually(salary_annually):
    return math.floor((16/100)*salary_annually)


def get_city_allowance_annually(salary_annually):
    return math.floor((8/100)*salary_annually)


def get_conveyance_allowance_annually(salary_annually):
    return math.floor((4/100)*salary_annually)


def get_children_education_allowance_annually(salary_annually):
    return math.floor((4/100)*salary_annually)


def get_medical_allowance_annually(salary_annually):
    return math.floor((4/100)*salary_annually)


def get_special_allowance_annually(salary_annually):
    return math.floor((24/100)*salary_annually)


def get_gross_annually(basic_annual,
    house_rent_allowance_annual,city_allowance_annual,
    conveyance_allowance_annual,children_education_allowance_annual,
    medical_allowance_annual,special_allowance_annual):
    gross_salary_annually = math.floor((
        basic_annual+house_rent_allowance_annual+city_allowance_annual+conveyance_allowance_annual+
        children_education_allowance_annual+medical_allowance_annual+special_allowance_annual
    ))
    return gross_salary_annually


def get_pf_annually(salary_annually):
    return math.floor((4.8/100)*salary_annually)


def get_tds_annually(salary_annually):
    if salary_annually <= 250000:
        return 0

    elif salary_annually > 250000 and salary_annually <= 500000:
        return math.floor((5/100)*salary_annually)

    elif salary_annually > 500000 and salary_annually <= 1000000:
        return math.floor((12500+((20/100)*(salary_annually-500000))))

    else:
        return math.floor((12500+100000+((30/100)*(salary_annually-1000000))))


def get_net_salary_annually(gross_salary_annually,pf_annually,tds_annually):
    return math.floor(gross_salary_annually-(pf_annually+tds_annually))
