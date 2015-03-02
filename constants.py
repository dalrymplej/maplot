# constants.py
"""
File containing constants to be used in various WW2100 graphics scripts.
"""
import datetime
import math

day_of_year_jan1 = 1
day_of_year_jan31 = 31
day_of_year_feb1 = 32
day_of_year_feb28 = 59
day_of_year_mar1 = 60
day_of_year_mar15 = 74
day_of_year_mar16 = 75
day_of_year_mar31 = 90
day_of_year_apr1 = 91
day_of_year_apr15 = 105
day_of_year_apr16 = 106
day_of_year_apr30 = 120
day_of_year_may1 = 121
day_of_year_may15 = 135
day_of_year_may16 = 136
day_of_year_may31 = 151
day_of_year_jun1 = 152
day_of_year_jun15 = 166
day_of_year_jun16 = 167
day_of_year_jun30 = 181
day_of_year_jul1 = 182
day_of_year_jul15 = 196
day_of_year_jul16 = 197
day_of_year_jul31 = 212
day_of_year_aug1 = 213
day_of_year_aug15 = 227
day_of_year_aug16 = 228
day_of_year_aug31 = 243
day_of_year_sep1 = 244
day_of_year_sep15 = 258
day_of_year_sep16 = 259
day_of_year_sep30 = 273
day_of_year_oct1 = 274
day_of_year_oct15 = 288
day_of_year_oct16 = 289
day_of_year_oct31 = 304
day_of_year_nov1 = 305
day_of_year_nov30 = 334
day_of_year_dec1 = 335
day_of_year_dec31 = 365

Jan1_1900 = datetime.date(1900,1,1)
Jan1_2010 = datetime.date(2010,1,1)

cfs_to_m3 = 0.0283168   #Cubic feet per second to cubic meters per second
F_to_C = 1.0/1.8        #Fahrenheit to Celcius
in_to_mm = 25.4         #Inches to milimeters
acft_to_m3 = 1233.48
acftperday_to_m3s = acft_to_m3/86400.
seconds_in_yr = 86400.*365.25
days_in_yr = 365
ft_to_m = 0.3048
Willamette_Basin_area = 29728.*1.e6  # m2
Willamette_Basin_area_at_PDX = 11200.*math.pow(5280.*.3048,2) #11200 sq mi @ PDX
seconds_in_day = 86400.
days_in_15_yrs = 15*365
days_in_30_yrs = 30*365
days_in_60_yrs = 60*365
