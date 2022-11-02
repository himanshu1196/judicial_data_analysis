import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import time
import datetime
import re
# %matplotlib inline


def check_constant_state_code():
    state_keys = pd.read_csv('keys/_/cases_state_key.csv')
    state_names = state_keys.state_name.unique()
    for state in state_names:
        state_codes = state_keys[state_keys['state_name'] == state].state_code.unique()
        if len(state_codes) > 1:
            print(len(state_codes), state_codes, state)
            return False
    
    state_district_keys = pd.read_csv('keys/_/cases_district_key.csv')
    state_codes = state_keys.state_code.unique()
    for sc in state_codes:
        data = state_district_keys[state_district_keys['state_code'] == sc]
        dist_names = data.district_name.unique()
        for dist in dist_names:
            dist_codes = data[data['district_name'] == dist].dist_code.unique()
            if len(dist_codes) > 1:
                print(len(dist_codes), dist_codes, dist, sc)
                return False
    #statecodes and dist codes haven't changed over time, return true
    return True


def get_judge_tenures_for(state_code):
    judges_clean = pd.read_csv('judges_clean.csv')
    judges_clean = judges_clean[judges_clean['state_code'] == state_code]
    
    state_district_keys = pd.read_csv('keys/_/cases_district_key.csv')
    dist_codes = state_district_keys[state_district_keys['state_code'] == state_code]['dist_code'].unique()
    
    date_for_20 = re.compile('^..-..-20[0-9][0-9]')
    
    judge_tenures = pd.DataFrame(columns = ['state_code', 'dist_code', 'court_no', 'ddl_judge_id', 'appointment_duration'])
    
    for dist_code in dist_codes:
        dist_judges = judges_clean[judges_clean['dist_code'] == dist_code]
        null_end_date = dist_judges['end_date'].isnull()
        for idx, row in dist_judges.iterrows():
            if not null_end_date[idx] and date_for_20.match(row['end_date']):
                duration = (datetime.datetime.strptime(row['end_date'],"%d-%m-%Y")  - datetime.datetime.strptime(row['start_date'],"%d-%m-%Y")).days
                judge_tenures.loc[len(judge_tenures.index)] = [state_code, dist_code, row['court_no'], row['ddl_judge_id'], duration]
            elif null_end_date[idx]:
                duration = (datetime.datetime.strptime('02-03-2022',"%d-%m-%Y")  - datetime.datetime.strptime(row['start_date'],"%d-%m-%Y")).days
                judge_tenures.loc[len(judge_tenures.index)] = [state_code, dist_code, row['court_no'], row['ddl_judge_id'], duration]
    
#     date_deltas = judge_tenures[judge_tenures['dist_code'] == 30]['appointment_duration']
#     plt.hist(date_deltas, bins = 40)
#     plt.title('Karnataka_YADGIR')
#     plt.xlabel('Appointment duration')
#     plt.ylabel('Number of judges')
    return judge_tenures

def get_judge_tenures_for_year(judges_clean, state_code, year):
    judges_clean = judges_clean[judges_clean['start_date'].str.contains(year)]
#     print(judges_clean[:3])
#     print(judges_clean[-3:])
#     print('------\n')
    
    state_district_keys = pd.read_csv('keys/_/cases_district_key.csv')
    dist_codes = state_district_keys[state_district_keys['state_code'] == state_code]['dist_code'].unique()
    
    date_for_20 = re.compile('^..-..-20[0-9][0-9]')
    
    judge_tenures = pd.DataFrame(columns = ['year', 'state_code', 'dist_code', 'court_no', 'ddl_judge_id', 'appointment_duration'])
    
    for dist_code in dist_codes:
        dist_judges = judges_clean[judges_clean['dist_code'] == dist_code]
        null_end_date = dist_judges['end_date'].isnull()
        for idx, row in dist_judges.iterrows():
            if (not null_end_date[idx]) and date_for_20.match(row['end_date']):
                duration = (datetime.datetime.strptime(row['end_date'],"%d-%m-%Y")  - datetime.datetime.strptime(row['start_date'],"%d-%m-%Y")).days
                judge_tenures.loc[len(judge_tenures.index)] = [year, state_code, dist_code, row['court_no'], row['ddl_judge_id'], duration]
            elif null_end_date[idx]:
                duration = (datetime.datetime.strptime('02-03-2022',"%d-%m-%Y")  - datetime.datetime.strptime(row['start_date'],"%d-%m-%Y")).days
                judge_tenures.loc[len(judge_tenures.index)] = [year, state_code, dist_code, row['court_no'], row['ddl_judge_id'], duration]
    
    
    return judge_tenures


def analyze_dist_wise_judge_tenures_for(state_code):
    jt = get_judge_tenures_for(state_code)
    state_district_keys = pd.read_csv('keys/_/cases_district_key.csv')
    dist_codes = state_district_keys[state_district_keys['state_code'] == state_code]['dist_code'].unique()
    
    
    judge_tenures = pd.DataFrame(columns = ['state_code', 'dist_code', 'mean_appointment_duration', 'median_appointment_duration'])    
        
    for dist_code in dist_codes:
        dist_data = jt[jt['dist_code'] == dist_code]
        mean_duration = np.mean(dist_data['appointment_duration'])
        median_duration = np.median(dist_data['appointment_duration'])
        judge_tenures.loc[len(judge_tenures.index)] = [state_code, dist_code, mean_duration, median_duration]
    
    judge_tenures_by_year = pd.DataFrame(columns = ['year', 'state_code', 'num_appointments', 'mean_appointment_duration', 'median_appointment_duration'])    
    
    years = [f'20{i}' for i in range(10, 19)]
    judges_clean = pd.read_csv('judges_clean.csv')
    for year in years:
        jt_for_year = get_judge_tenures_for_year(judges_clean, state_code, year)
        state_data = jt_for_year[jt_for_year['state_code'] == state_code]
        num_appointments = len(state_data)
        mean_duration = np.mean(state_data['appointment_duration'])
        median_duration = np.median(state_data['appointment_duration'])
        judge_tenures_by_year.loc[len(judge_tenures_by_year.index)] = [year, state_code, num_appointments, mean_duration, median_duration]
            
#     date_deltas = judge_tenures[judge_tenures['dist_code'] == 30]['appointment_duration']
#     plt.hist(date_deltas, bins = 40)
#     plt.title('Karnataka_YADGIR')
#     plt.xlabel('Appointment duration')
#     plt.ylabel('Number of judges')
    print(judge_tenures_by_year)
    return judge_tenures, judge_tenures_by_year

def analyze_year_dist_wise_judge_tenures_for(state_code):
    jt = get_judge_tenures_for(state_code)
    state_district_keys = pd.read_csv('keys/_/cases_district_key.csv')
    dist_codes = state_district_keys[state_district_keys['state_code'] == state_code]['dist_code'].unique()
    
    
#     judge_tenures = pd.DataFrame(columns = ['state_code', 'dist_code', 'mean_appointment_duration', 'median_appointment_duration'])    
        
#     for dist_code in dist_codes:
#         dist_data = jt[jt['dist_code'] == dist_code]
#         mean_duration = np.mean(dist_data['appointment_duration'])
#         median_duration = np.median(dist_data['appointment_duration'])
#         judge_tenures.loc[len(judge_tenures.index)] = [state_code, dist_code, mean_duration, median_duration]
    
    judge_tenures_by_year_and_dist = pd.DataFrame(columns = ['year', 'state_code', 'dist_code', 'num_appointments', 'mean_appointment_duration', 'median_appointment_duration'])    
    
    years = [f'20{i}' for i in range(10, 19)]
    judges_clean = pd.read_csv('judges_clean.csv')
    for year in years:
        jt_for_year = get_judge_tenures_for_year(judges_clean, state_code, year)
        state_data = jt_for_year[jt_for_year['state_code'] == state_code]
        for dist_code in dist_codes:
            dist_data = state_data[state_data['dist_code'] == dist_code]
            num_appointments = len(dist_data)
            mean_duration = np.mean(dist_data['appointment_duration'])
            median_duration = np.median(dist_data['appointment_duration'])
            judge_tenures_by_year_and_dist.loc[len(judge_tenures_by_year_and_dist.index)] = [year, state_code, dist_code, num_appointments, mean_duration, median_duration]
            
#     print(judge_tenures_by_year)
    return judge_tenures_by_year_and_dist

def analyze_case_pendency_per_year(state_code):
    years = [f'20{i}' for i in range(10, 19)]
    per_year_disposal_counts = {}
    per_year_data = {}
    pendency_rates_per_year = pd.DataFrame(columns = ['year', 'state_code', 'num_instituted', 'num_disposed', 'num_disposed_from_instituted', 'clearance_rate', 'pending_count'])
    
    for year in years:
        per_year_disposal_counts[year] = 0
    
    
    for year in years:
        case_data = pd.read_csv(f'cases/_/cases_{year}.csv')
        case_data = case_data[case_data['state_code'] == state_code]
        instituted_cases = case_data[case_data['date_of_filing'].str.contains(year)]
        case_data = case_data[case_data['date_of_decision'].notnull()]
        num_instituted = len(instituted_cases)
        for year2 in years:
            disposed_cases = case_data[case_data['date_of_decision'].str.contains(year2)]
            per_year_disposal_counts[year2] = per_year_disposal_counts[year2] + len(disposed_cases)
        disposed_instituted_cases = instituted_cases[instituted_cases['date_of_decision'].notnull()]
        num_disposed_from_instituted = len(disposed_instituted_cases[disposed_instituted_cases['date_of_decision'].str.contains(year)])
        
        clearance_rate = num_disposed_from_instituted / num_instituted
        pending_count = num_instituted - num_disposed_from_instituted
        
        per_year_data[year] = [year, state_code, num_instituted, -1, num_disposed_from_instituted, clearance_rate, pending_count]
        
    for year in years:
        data = per_year_data[year]
        data[3] = per_year_disposal_counts[year]
        pendency_rates_per_year.loc[len(pendency_rates_per_year.index)] = data
    
    return pendency_rates_per_year

def analyze_dist_wise_case_pendency_per_year(state_code):
    years = [f'20{i}' for i in range(10, 19)]
    per_year_disposal_counts = {}
    per_year_data = {}
    dist_wise_pendency_rates_per_year = pd.DataFrame(columns = ['year', 'state_code', 'dist_code', 'num_instituted', 'num_disposed', 'num_disposed_from_instituted', 'clearance_rate', 'pending_count', 'new_clearance_rate'])
    
    state_district_keys = pd.read_csv('keys/_/cases_district_key.csv')
    dist_codes = state_district_keys[state_district_keys['state_code'] == state_code]['dist_code'].unique()
    
    for year in years:
        per_year_data[year] = {}
        per_year_disposal_counts[year] = {}
        for dist_code in dist_codes:
            per_year_disposal_counts[year][dist_code] = 0
            per_year_data[year][dist_code] = []
    
    
    for year in years:
        case_data = pd.read_csv(f'cases/_/cases_{year}.csv')
        case_data = case_data[case_data['state_code'] == state_code]
        
        for dist_code in dist_codes:
            dist_case_data = case_data[case_data['dist_code'] == dist_code]
            instituted_cases = dist_case_data[dist_case_data['date_of_filing'].str.contains(year)]
            dist_case_data = dist_case_data[dist_case_data['date_of_decision'].notnull()]
            num_instituted = len(instituted_cases)
            for year2 in years:
                disposed_cases = dist_case_data[dist_case_data['date_of_decision'].str.contains(year2)]
                per_year_disposal_counts[year2][dist_code] = per_year_disposal_counts[year2][dist_code] + len(disposed_cases)
            disposed_instituted_cases = instituted_cases[instituted_cases['date_of_decision'].notnull()]
            num_disposed_from_instituted = len(disposed_instituted_cases[disposed_instituted_cases['date_of_decision'].str.contains(year)])

            clearance_rate = num_disposed_from_instituted / num_instituted
            pending_count = num_instituted - num_disposed_from_instituted

            per_year_data[year][dist_code] = [year, state_code, dist_code, num_instituted, -1, num_disposed_from_instituted, clearance_rate, pending_count, 0.0]

    for year in years:
        for dist_code in dist_codes:
            data = per_year_data[year][dist_code]
            data[4] = per_year_disposal_counts[year][dist_code]
            data[8] = data[4] / data[3]
            dist_wise_pendency_rates_per_year.loc[len(dist_wise_pendency_rates_per_year.index)] = data

    return dist_wise_pendency_rates_per_year


def analyze_year_wise_case_durations(state_code):
    date_for_20 = re.compile('^20[0-9][0-9]-..-..')
    years = [f'20{i}' for i in range(10, 19)]
    year_wise_case_durations = pd.DataFrame(columns = ['year', 'state_code', 'median_days_to_decision', 'mean_days_to_decision'])
    
    for year in years:
        case_data = pd.read_csv(f'cases/_/cases_{year}.csv')
        case_data = case_data[case_data['state_code'] == state_code]
        
        case_data = case_data[case_data['date_of_decision'].notnull()] #disposed cases
        date_deltas = [(datetime.datetime.strptime(end_date,"%Y-%m-%d") - datetime.datetime.strptime(start_date,"%Y-%m-%d")).days for end_date, start_date in zip(case_data['date_of_decision'], case_data['date_of_filing']) if (date_for_20.match(end_date) and date_for_20.match(start_date) and (datetime.datetime.strptime(end_date,"%Y-%m-%d") - datetime.datetime.strptime(start_date,"%Y-%m-%d")).days > 0)]
        median = np.median(date_deltas)
        mean = np.mean(date_deltas)
        year_wise_case_durations.loc[len(year_wise_case_durations.index)] = [year, state_code, median, mean]
        
    year_wise_case_durations.to_csv(f'generated/year_wise_case_duration_stats_SC_{state_code}.csv')
    return year_wise_case_durations

def analyze_year_wise_judge_count(state_code):
    date_for_20 = re.compile('^..-..-20[0-9][0-9]')
    
    judges_clean = pd.read_csv('judges_clean.csv')
    judges_clean = judges_clean[judges_clean['state_code'] == state_code]
    
    years = [f'20{i}' for i in range(10, 19)]
    
    year_wise_duration = {}
    for year in years:
        year_wise_duration[year] = 0
    
    null_end_date = judges_clean['end_date'].isnull()
    for idx, row in judges_clean.iterrows():
        if not null_end_date[idx]:
            if date_for_20.match(row['start_date']) and date_for_20.match(row['end_date']):
                start_year = int(row['start_date'][-4:])
                end_year = int(row['end_date'][-4:])
                if end_year < 2010:
                    continue
                for year in range(max(start_year, 2010), min(end_year + 1, 2019)):
                    if (start_year == end_year):
                        year_wise_duration[str(year)] = year_wise_duration[str(year)] + (datetime.datetime.strptime(row['end_date'],"%d-%m-%Y")  - datetime.datetime.strptime(row['start_date'],"%d-%m-%Y")).days
                    elif (year == start_year):
                        year_wise_duration[str(year)] = year_wise_duration[str(year)] + (datetime.datetime.strptime(f'31-12-{start_year}',"%d-%m-%Y")  - datetime.datetime.strptime(row['start_date'],"%d-%m-%Y")).days
                    elif (year == end_year):
                        year_wise_duration[str(year)] = year_wise_duration[str(year)] + (datetime.datetime.strptime(row['end_date'],"%d-%m-%Y")  - datetime.datetime.strptime(f'01-01-{end_year}',"%d-%m-%Y")).days
                    else:
                        year_wise_duration[str(year)] = year_wise_duration[str(year)] + 365
        else:
            if date_for_20.match(row['start_date']):
                start_year = int(row['start_date'][-4:])
                end_year = 2021
                for year in range(max(start_year, 2010), 2019):
                    if (start_year == end_year):
                        year_wise_duration[str(year)] = year_wise_duration[str(year)] + (datetime.datetime.strptime(row['end_date'],"%d-%m-%Y")  - datetime.datetime.strptime(row['start_date'],"%d-%m-%Y")).days
                    elif (year == start_year):
                        year_wise_duration[str(year)] = year_wise_duration[str(year)] + (datetime.datetime.strptime(f'31-12-{start_year}',"%d-%m-%Y")  - datetime.datetime.strptime(row['start_date'],"%d-%m-%Y")).days
                    else:
                        year_wise_duration[str(year)] = year_wise_duration[str(year)] + 365
    
    year_wise_judge_counts = pd.DataFrame(columns = ['state_code', 'year', 'total_judge_days', 'avg_judge_count'])
    for year in years:
        year_wise_judge_counts.loc[len(year_wise_judge_counts.index)] = [state_code, year, year_wise_duration[year], year_wise_duration[year]/365]
    
    year_wise_judge_counts.to_csv(f'generated/sc_{state_code}_year_wise_judge_counts.csv')


def analyze_year_dist_wise_judge_counts_for(state_code):
    date_for_20 = re.compile('^..-..-20[0-9][0-9]')
    
    judges_clean = pd.read_csv('judges_clean.csv')
    judges_clean = judges_clean[judges_clean['state_code'] == state_code]
    
    state_district_keys = pd.read_csv('keys/_/cases_district_key.csv')
    dist_codes = state_district_keys[state_district_keys['state_code'] == state_code]['dist_code'].unique()
    
    years = [f'20{i}' for i in range(10, 19)]
    
    year_dist_wise_duration = {}
    for year in years:
        dist_wise_duration = {}
        for dc in dist_codes:
            dist_wise_duration[dc] = 0
        year_dist_wise_duration[year] = dist_wise_duration
    
    for dc in dist_codes:
        dist_data = judges_clean[judges_clean['dist_code'] == dc]
        null_end_date = dist_data['end_date'].isnull()
        for idx, row in dist_data.iterrows():
            if not null_end_date[idx]:
                if date_for_20.match(row['start_date']) and date_for_20.match(row['end_date']):
                    start_year = int(row['start_date'][-4:])
                    end_year = int(row['end_date'][-4:])
                    if end_year < 2010:
                        continue
                    for year in range(max(start_year, 2010), min(end_year + 1, 2019)):
                        if (start_year == end_year):
                            year_dist_wise_duration[str(year)][dc] = year_dist_wise_duration[str(year)][dc] + (datetime.datetime.strptime(row['end_date'],"%d-%m-%Y")  - datetime.datetime.strptime(row['start_date'],"%d-%m-%Y")).days
                        elif (year == start_year):
                            year_dist_wise_duration[str(year)][dc] = year_dist_wise_duration[str(year)][dc] + (datetime.datetime.strptime(f'31-12-{start_year}',"%d-%m-%Y")  - datetime.datetime.strptime(row['start_date'],"%d-%m-%Y")).days
                        elif (year == end_year):
                            year_dist_wise_duration[str(year)][dc] = year_dist_wise_duration[str(year)][dc] + (datetime.datetime.strptime(row['end_date'],"%d-%m-%Y")  - datetime.datetime.strptime(f'01-01-{end_year}',"%d-%m-%Y")).days
                        else:
                            year_dist_wise_duration[str(year)][dc] = year_dist_wise_duration[str(year)][dc] + 365
            else:
                if date_for_20.match(row['start_date']):
                    start_year = int(row['start_date'][-4:])
                    end_year = 2021
                    for year in range(max(start_year, 2010), 2019):
                        if (start_year == end_year):
                            year_dist_wise_duration[str(year)][dc] = year_dist_wise_duration[str(year)][dc] + (datetime.datetime.strptime(row['end_date'],"%d-%m-%Y")  - datetime.datetime.strptime(row['start_date'],"%d-%m-%Y")).days
                        elif (year == start_year):
                            year_dist_wise_duration[str(year)][dc] = year_dist_wise_duration[str(year)][dc] + (datetime.datetime.strptime(f'31-12-{start_year}',"%d-%m-%Y")  - datetime.datetime.strptime(row['start_date'],"%d-%m-%Y")).days
                        else:
                            year_dist_wise_duration[str(year)][dc] = year_dist_wise_duration[str(year)][dc] + 365
    
    year_dist_wise_judge_counts = pd.DataFrame(columns = ['state_code', 'year', 'dist_code', 'total_judge_days', 'avg_judge_count'])
    for year in years:
        for dc in dist_codes:
            year_dist_wise_judge_counts.loc[len(year_dist_wise_judge_counts.index)] = [state_code, year, dc, year_dist_wise_duration[year][dc], year_dist_wise_duration[year][dc]/365]
    
    year_dist_wise_judge_counts.to_csv(f'generated/sc_{state_code}_year_dist_wise_judge_counts.csv')

    
def analyze_court_wise_case_durations_for(state_code, year):
    date_for_2010 = re.compile('2010-*')
    date_for_20 = re.compile('^20[0-9][0-9]-*')
    case_durations = pd.DataFrame(columns = ['year', 'state_code', 'dist_code', 'court_no', 'median', 'mean', 'case_count'])
    
    case_data = pd.read_csv(f'cases/_/cases_{year}.csv')
    state_cases = case_data[case_data['state_code'] == state_code]
    case_data = 0
    for dist_code in range(1, 77):
        dist_cases = state_cases[state_cases['dist_code'] == dist_code]
        if len(dist_cases) == 0:
            continue
        for court_no in range(1, 75):
            court_cases = dist_cases[dist_cases['court_no'] == court_no]
            if len(court_cases) == 0:
                continue
            case_count = len(court_cases)
            #ignores cases with null end dates
            case_date_deltas = [(datetime.datetime.strptime(end_date,"%Y-%m-%d") - datetime.datetime.strptime(start_date,"%Y-%m-%d")).days for end_date, start_date in zip(court_cases['date_of_decision'][court_cases['date_of_decision'].notnull()], court_cases['date_of_filing'][court_cases['date_of_decision'].notnull()]) if (date_for_20.match(end_date) and (datetime.datetime.strptime(end_date,"%Y-%m-%d") - datetime.datetime.strptime(start_date,"%Y-%m-%d")).days > 0)]
            if (len(case_date_deltas) > 0):
                median = np.median(case_date_deltas)
                mean = np.mean(case_date_deltas)

                #save transfer info for court
                case_durations.loc[len(case_durations.index)] = [year, state_code, dist_code, court_no, median, mean, case_count]
    
    f = plt.figure()
    f.set_figwidth(10)
    f.set_figheight(10)
    plt.hist(case_durations['median'][case_durations['case_count'] > 1000], bins = 40)
    plt.title(f'Distribution across courts with at least 1000 cases in {year}')
    plt.xlabel('Median number of days to decision')
    plt.ylabel('Number of courts')
    plt.savefig(f'generated/median_distribution_{year}_SC_{state_code}.png')
    

def group_judge_tenures_by_dist_for(state_code, year):
    jt = get_judge_tenures_for(state_code)
    state_district_keys = pd.read_csv('keys/_/cases_district_key.csv')
    dist_codes = state_district_keys[state_district_keys['state_code'] == state_code]['dist_code'].unique()
    
#     plt.hist(jt['appointment_duration'], bins = 40)
    
    judge_tenures = pd.DataFrame(columns = ['state_code', 'dist_code', 'tenure_S_count', 'tenure_M_count', 'tenure_L_count', 'tenure_S_fraction', 'tenure_M_fraction', 'tenure_L_fraction'])    
        
    for dist_code in dist_codes:
        dist_data = jt[jt['dist_code'] == dist_code]
        s = len(dist_data[dist_data['appointment_duration'] < 730])
        m = len(dist_data[dist_data['appointment_duration'].between(730, 1825)])
        l = len(dist_data[dist_data['appointment_duration'] > 1825])
        total = s + m + l
#         mean_duration = np.mean(dist_data['appointment_duration'])
#         median_duration = np.median(dist_data['appointment_duration'])
        judge_tenures.loc[len(judge_tenures.index)] = [state_code, dist_code, s, m, l, s/total, m/total, l/total]
    
    judge_tenures.to_csv(f'generated/sc_{state_code}_tenure_group_counts_by_dist.csv')
    return judge_tenures


def group_case_durations_for_each_year(state_code):
    date_for_20 = re.compile('^20[0-9][0-9]-..-..')
    years = [f'20{i}' for i in range(10, 19)]
    year_wise_case_duration_counts = pd.DataFrame(columns = ['year', 'state_code', 'duration_A', 'duration_B', 'duration_C', 'duration_D', 'duration_E', 'duration_A_fraction', 'duration_B_fraction', 'duration_C_fraction', 'duration_D_fraction', 'duration_E_fraction'])
    #A,B,C,D,E = 0-1,1-3,3-5,5-10,10+ years
    for year in years:
        case_data = pd.read_csv(f'cases/_/cases_{year}.csv')
        case_data = case_data[case_data['state_code'] == state_code]
        
        #set null decision dates to current date
        case_data.loc[case_data['date_of_decision'].isnull(), 'date_of_decision'] = '2022-03-02'
        date_deltas = np.array([(datetime.datetime.strptime(end_date,"%Y-%m-%d") - datetime.datetime.strptime(start_date,"%Y-%m-%d")).days for end_date, start_date in zip(case_data['date_of_decision'], case_data['date_of_filing']) if (date_for_20.match(end_date) and date_for_20.match(start_date) and (datetime.datetime.strptime(end_date,"%Y-%m-%d") - datetime.datetime.strptime(start_date,"%Y-%m-%d")).days > 0)])
        
        a = np.sum((date_deltas < 365).astype(int))
        b = np.sum((date_deltas >= 365).astype(int) * (date_deltas < 365*3).astype(int))
        c = np.sum((date_deltas >= 365*3).astype(int) * (date_deltas < 365*5).astype(int))
        d = np.sum((date_deltas >= 365*5).astype(int) * (date_deltas < 365*10).astype(int))
        e = np.sum((date_deltas >= 365*10).astype(int))
        total = a + b + c + d + e
        year_wise_case_duration_counts.loc[len(year_wise_case_duration_counts.index)] = [year, state_code, a, b, c, d, e, a/total, b/total, c/total, d/total, e/total]
        
    year_wise_case_duration_counts.to_csv(f'generated/sc_{state_code}_case_duration_group_counts_by_year.csv')
    return year_wise_case_duration_counts


def analyze_dist_court_wise_tenures_and_productivity(state_dist_court_tuples,si=1,di=2,ci=3,savefile='generated/district_court_tenure_and_judge_stats.csv'):
    
#     for each district_court calculate (tenure, work strength)
    
#     group sdc_tup in ll, lh, hl, hh  (tenure, work strength)
    
#     study productivity (disposal/clearance rate, time to decision) each group separately
    date_for_20 = re.compile('^..-..-20[0-9][0-9]')
    
    judges_clean = pd.read_csv('judges_clean.csv')
    
    dist_court_stats = pd.DataFrame(columns = ['state_code', 'dist_code', 'court_no', 'total_judge_days', 'avg_judge_count', 'mean_tenure_days', 'median_tenure_days', 'num_judges', 'num_valid_entries'])
    
    for row in state_dist_court_tuples.itertuples():
        s,d,c = row[si], row[di], row[ci]
        court_data = judges_clean[judges_clean['state_code'] == s]
        court_data = court_data[court_data['dist_code'] == d]
        court_data = court_data[court_data['court_no'] == c]
        null_end_date =  court_data['end_date'].isnull()
#         print(null_end_date)
        court_tenure_days = []
        court_working_days = 0.0
        min_contribution_start_date = '31-12-2018'
        max_contribution_end_date = '01-01-2010'
        
        for idx, row in court_data.iterrows():
            if not null_end_date[idx]:
                if date_for_20.match(row['start_date']) and date_for_20.match(row['end_date']):
                    tenure_days = (datetime.datetime.strptime(row['end_date'],"%d-%m-%Y")  - datetime.datetime.strptime(row['start_date'],"%d-%m-%Y")).days
                    if (tenure_days > 0):
                        court_tenure_days.append(tenure_days)
                    
                    start_year = int(row['start_date'][-4:])
                    end_year = int(row['end_date'][-4:])
                    
                    if end_year < 2010:
                        continue
                    
                    contribution_start_date = row['start_date']
                    contribution_end_date = row['end_date']

                    if start_year < 2010:
                        contribution_start_date = '01-01-2010'
                    
                    if end_year > 2018:
                        contribution_end_date = '31-12-2018'
                    
                    if (datetime.datetime.strptime(contribution_start_date,"%d-%m-%Y")  - datetime.datetime.strptime(min_contribution_start_date,"%d-%m-%Y")).days < 0:
                        min_contribution_start_date = contribution_start_date
                        
                    if (datetime.datetime.strptime(contribution_end_date,"%d-%m-%Y")  - datetime.datetime.strptime(max_contribution_end_date,"%d-%m-%Y")).days > 0:
                        max_contribution_end_date = contribution_end_date
                    #number of working days contributed by the judge over the period 2010-2018
                    contribution_days = (datetime.datetime.strptime(contribution_end_date,"%d-%m-%Y")  - datetime.datetime.strptime(contribution_start_date,"%d-%m-%Y")).days
            else:
                if date_for_20.match(row['start_date']):
                    #Calculate tenure statistics across courts assuming the judge still held the position on 31-12-2020 (2018 + 2 years)
                    tenure_days = (datetime.datetime.strptime('31-12-2020',"%d-%m-%Y")  - datetime.datetime.strptime(row['start_date'],"%d-%m-%Y")).days
                    if (tenure_days > 0):
                        court_tenure_days.append(tenure_days)
                    
                    start_year = int(row['start_date'][-4:])
                    
                    contribution_start_date = row['start_date']
                    contribution_end_date = '31-12-2018'

                    
                    if start_year < 2010:
                        contribution_start_date = '01-01-2010'
                    
                    if (datetime.datetime.strptime(contribution_start_date,"%d-%m-%Y")  - datetime.datetime.strptime(min_contribution_start_date,"%d-%m-%Y")).days < 0:
                        min_contribution_start_date = contribution_start_date
                        
                    max_contribution_end_date = contribution_end_date
                    #number of working days contributed by the judge over the period 2010-2018
                    contribution_days = (datetime.datetime.strptime(contribution_end_date,"%d-%m-%Y")  - datetime.datetime.strptime(contribution_start_date,"%d-%m-%Y")).days
                    
            if contribution_days > 0:
                court_working_days += contribution_days
        
        if len(court_tenure_days) != 0:
            max_contribution_period = (datetime.datetime.strptime(max_contribution_end_date,"%d-%m-%Y")  - datetime.datetime.strptime(min_contribution_start_date,"%d-%m-%Y")).days
            dist_court_stats.loc[len(dist_court_stats.index)] = [s, d, c, court_working_days, court_working_days/(max_contribution_period), np.mean(court_tenure_days), np.median(court_tenure_days), len(court_data), len(court_tenure_days)]
    
    dist_court_stats.to_csv(savefile)
    
    #plot data for analysis
    print('median of median tenures: ', np.median(dist_court_stats['median_tenure_days']))
    print('median of average daily judge strengths: ', np.median(dist_court_stats['avg_judge_count']))
    return dist_court_stats
    
    
def group_courts_by_tenure_and_strength(dist_court_stats, median_tenure, median_strength):
    low_tenures = dist_court_stats[dist_court_stats['median_tenure_days'] < median_tenure]
    high_tenures = dist_court_stats[dist_court_stats['median_tenure_days'] >= median_tenure]
    low_tenures_low_strength = low_tenures[low_tenures['avg_judge_count'] < median_strength]
    low_tenures_high_strength = low_tenures[low_tenures['avg_judge_count'] >= median_strength]
    high_tenures_low_strength = high_tenures[high_tenures['avg_judge_count'] < median_strength]
    high_tenures_high_strength = high_tenures[high_tenures['avg_judge_count'] >= median_strength]

    return low_tenures_low_strength, low_tenures_high_strength, high_tenures_low_strength, high_tenures_high_strength


def get_case_stats_for_courts(state_dist_court_tuples, cases_base_path, sc_idx, dc_idx, cn_idx, save_file):
    date_for_20 = re.compile('^20[0-9][0-9]-..-..')

#     study productivity (disposal/clearance rate, time to decision)
    dist_court_case_stats = pd.DataFrame(columns = ['state_code', 'dist_code', 'court_no', 'total_cases', 'total_valid_cases', 'median_decision_days', 'mean_decision_days'])
    years = [f'20{i}' for i in range(10,19)]
    
    court_stats_dict = {}
    for year in years:
        print(f'Processing cases for year : {year}')
        case_data = pd.read_csv(f'{cases_base_path}/cases_acts_{year}.csv') #read large case data to memory
        for row in state_dist_court_tuples.itertuples():
            s,d,c = row[sc_idx], row[dc_idx], row[cn_idx]
            #get all cases files in sdc
            court_data = case_data[case_data['state_code'] == s]
            court_data = court_data[court_data['dist_code'] == d]
            court_data = court_data[court_data['court_no'] == c]
        
            #get time to decision for each case; (31-12-2020 - filing date for cases with null end dates)
            #court_data['date_of_decision'] = court_data['date_of_decision'].fillna('2020-12-31')
            #only consider disposed cases
            court_data = court_data[court_data['date_of_decision'].notnull()]
            total_cases = len(court_data)
            date_deltas = [(datetime.datetime.strptime(end_date,"%Y-%m-%d") - datetime.datetime.strptime(start_date,"%Y-%m-%d")).days for end_date, start_date in zip(court_data['date_of_decision'], court_data['date_of_filing']) if (date_for_20.match(end_date) and date_for_20.match(start_date) and (datetime.datetime.strptime(end_date,"%Y-%m-%d") - datetime.datetime.strptime(start_date,"%Y-%m-%d")).days > 0)]
            total_valid_cases = len(date_deltas)

            if (s,d,c) not in court_stats_dict.keys():
                court_stats_dict[(s,d,c)] = (total_cases, total_valid_cases, date_deltas)
            else:
                curr_tuple = court_stats_dict[(s,d,c)]
                curr_tuple[2].extend(date_deltas)
                court_stats_dict[(s,d,c)] = (curr_tuple[0] + total_cases, curr_tuple[1] + total_valid_cases, curr_tuple[2])
    
    for sdc in court_stats_dict.keys():
        #calculate median, mean of time to decision
        total_cases, total_valid_cases, date_deltas = court_stats_dict[sdc]
        if (total_valid_cases == 0):
            dist_court_case_stats.loc[len(dist_court_case_stats.index)] = [sdc[0], sdc[1], sdc[2], total_cases, total_valid_cases, -1, -1]
            continue
        dist_court_case_stats.loc[len(dist_court_case_stats.index)] = [sdc[0], sdc[1], sdc[2], total_cases, total_valid_cases, np.median(date_deltas), np.mean(date_deltas)]
        
    dist_court_case_stats.to_csv(save_file)
    return dist_court_case_stats
    
    
def analyze_dist_court_wise_case_pendency_per_year(state_dist_court_df, cases_base_path,sc_idx, dc_idx, cn_idx, save_file):
    date_for_20 = re.compile('^20[0-9][0-9]-..-..')
    years = [f'20{i}' for i in range(10, 19)]
    per_year_disposal_counts = {}
    per_year_data = {}
    dist_court_wise_pendency_rates_per_year = pd.DataFrame(columns = ['year', 'state_code', 'dist_code', 'court_no', 'num_instituted', 'num_disposed', 'num_disposed_from_instituted', 'clearance_rate', 'pending_count', 'new_clearance_rate', 'median_decision_days', 'mean_decision_days'])
    #can include yearwise mean and median days to decision
    for year in years:
        per_year_data[year] = {}
        per_year_disposal_counts[year] = {}
        for row in state_dist_court_df.itertuples():
            key = (row[sc_idx], row[dc_idx], row[cn_idx])
            per_year_disposal_counts[year][key] = 0
            per_year_data[year][key] = []
    
    
    for year in years:
        print(f'Processing cases for year : {year}')
        case_data = pd.read_csv(f'{cases_base_path}/cases_acts_{year}.csv')
        
        for row in state_dist_court_df.itertuples():
            key = (row[sc_idx], row[dc_idx], row[cn_idx])
            s,d,c = row[sc_idx], row[dc_idx], row[cn_idx]
            
            
            court_case_data = case_data[case_data['state_code'] == s]
            court_case_data = court_case_data[court_case_data['dist_code'] == d]
            court_case_data = court_case_data[court_case_data['court_no'] == c]
            
            instituted_cases = court_case_data[court_case_data['date_of_filing'].str.contains(year)]
            court_case_data = court_case_data[court_case_data['date_of_decision'].notnull()]
            num_instituted = len(instituted_cases)
            
            for year2 in years:
                disposed_cases = court_case_data[court_case_data['date_of_decision'].str.contains(year2)]
                per_year_disposal_counts[year2][key] = per_year_disposal_counts[year2][key] + len(disposed_cases)
            disposed_instituted_cases = instituted_cases[instituted_cases['date_of_decision'].notnull()]
            num_disposed_from_instituted = len(disposed_instituted_cases[disposed_instituted_cases['date_of_decision'].str.contains(year)])

            if (num_instituted == 0):
                clearance_rate = -1.0
                median_decision_days = -1
                mean_decision_days = -1
            else:
                clearance_rate = num_disposed_from_instituted / num_instituted
                date_deltas = [(datetime.datetime.strptime(end_date,"%Y-%m-%d") - datetime.datetime.strptime(start_date,"%Y-%m-%d")).days for end_date, start_date in zip(court_case_data['date_of_decision'], court_case_data['date_of_filing']) if (date_for_20.match(end_date) and date_for_20.match(start_date) and (datetime.datetime.strptime(end_date,"%Y-%m-%d") - datetime.datetime.strptime(start_date,"%Y-%m-%d")).days > 0)]
                median_decision_days = -1
                mean_decision_days = -1
                if len(date_deltas) != 0:
                    median_decision_days = np.median(date_deltas)
                    mean_decision_days = np.mean(date_deltas)
            pending_count = num_instituted - num_disposed_from_instituted

            per_year_data[year][key] = [year, s, d, c, num_instituted, -1, num_disposed_from_instituted, clearance_rate, pending_count, 0.0, median_decision_days, mean_decision_days]

    for year in years:
        for row in state_dist_court_df.itertuples():
            key = (row[sc_idx], row[dc_idx], row[cn_idx])
            s,d,c = row[sc_idx], row[dc_idx], row[cn_idx]
            
            data = per_year_data[year][key]
            data[5] = per_year_disposal_counts[year][key]
            if data[4] == 0:
                data[9] = -1
            else:
                data[9] = data[5] / data[4]
            
            dist_court_wise_pendency_rates_per_year.loc[len(dist_court_wise_pendency_rates_per_year.index)] = data

    dist_court_wise_pendency_rates_per_year.to_csv(save_file)
    return dist_court_wise_pendency_rates_per_year


def analyze_dist_court_wise_tenures_by_year(state_dist_court_df):
#     for each court, for each year, find the judges who were active, calculate their median.
    years = [f'20{i}' for i in range(10,19)]
    judges = pd.read_csv('judges_clean.csv')
    date_for_20 = re.compile('^..-..-20[0-9][0-9]')
    dist_court_wise_tenures_by_year = pd.DataFrame(columns = ['year', 'state_code', 'dist_code', 'court_no', 'total_judge_count', 'median_tenure', 'mean_tenure', 'weighted_mean_tenure', 'avg_judge_count'])
    
    for row in state_dist_court_df.itertuples():
        s,d,c = row[1], row[2], row[3]
#         print('checking ',s,d,c)
        court_judges = judges[judges['state_code'] == s]
        court_judges = court_judges[court_judges['dist_code'] == d]
        court_judges = court_judges[court_judges['court_no'] == c]
        null_end_dates = court_judges['end_date'].isnull()
        for year in years:
            active_judges = []
            weights = []
            for idx, cj_row in court_judges.iterrows():
                contribution_weight = 1
                if ((not null_end_dates[idx] and not date_for_20.match(cj_row['end_date'])) or (not date_for_20.match(cj_row['start_date']))):
                    #invalid data, move to next row
                    continue
                if (not null_end_dates[idx] and (datetime.datetime.strptime(cj_row['end_date'],"%d-%m-%Y")  - datetime.datetime.strptime(cj_row['start_date'],"%d-%m-%Y")).days < 0):
                    #invalid data, move to next row
                    continue
                #if judge was active on any day in <year>
                if (null_end_dates[idx]):
#                     active if start date is before 31-12-year
                    if ((datetime.datetime.strptime(f'31-12-{year}',"%d-%m-%Y")  - datetime.datetime.strptime(cj_row['start_date'],"%d-%m-%Y")).days >= 0):
                        term = (datetime.datetime.strptime(f'31-12-2020',"%d-%m-%Y")  - datetime.datetime.strptime(cj_row['start_date'],"%d-%m-%Y")).days
                        contribution_weight = (datetime.datetime.strptime(f'31-12-{year}',"%d-%m-%Y")  - datetime.datetime.strptime(cj_row['start_date'],"%d-%m-%Y")).days/365
                        contribution_weight = min(1, contribution_weight)
                        active_judges.append(term)
                        weights.append(contribution_weight)
                else:
                    
#                     if end date after 31-12-year
                    if ((datetime.datetime.strptime(cj_row['end_date'],"%d-%m-%Y")  - datetime.datetime.strptime(f'31-12-{year}',"%d-%m-%Y")).days >= 0):
#                         active if start date is before 31-12-year
                        if ((datetime.datetime.strptime(f'31-12-{year}',"%d-%m-%Y")  - datetime.datetime.strptime(cj_row['start_date'],"%d-%m-%Y")).days >= 0):
                            term = (datetime.datetime.strptime(cj_row['end_date'],"%d-%m-%Y")  - datetime.datetime.strptime(cj_row['start_date'],"%d-%m-%Y")).days
                            contribution_weight = (datetime.datetime.strptime(f'31-12-{year}',"%d-%m-%Y")  - datetime.datetime.strptime(cj_row['start_date'],"%d-%m-%Y")).days/365
                            contribution_weight = min(1,contribution_weight)
                            active_judges.append(term)
                            weights.append(contribution_weight)
                    else:
#                         if end date between 01-01-year and 31-12-year:
                        if ((datetime.datetime.strptime(f'31-12-{year}',"%d-%m-%Y")  - datetime.datetime.strptime(cj_row['end_date'],"%d-%m-%Y")).days * (datetime.datetime.strptime(f'01-01-{year}',"%d-%m-%Y")  - datetime.datetime.strptime(cj_row['end_date'],"%d-%m-%Y")).days <= 0):
                            term = (datetime.datetime.strptime(cj_row['end_date'],"%d-%m-%Y")  - datetime.datetime.strptime(cj_row['start_date'],"%d-%m-%Y")).days
                            contribution_weight = (datetime.datetime.strptime(cj_row['end_date'],"%d-%m-%Y")  - datetime.datetime.strptime(cj_row['start_date'],"%d-%m-%Y")).days/365
                            max_contribution_weight = (datetime.datetime.strptime(cj_row['end_date'],"%d-%m-%Y")  - datetime.datetime.strptime(f'01-01-{year}',"%d-%m-%Y")).days/365
                            contribution_weight = min(max_contribution_weight,contribution_weight)
                            active_judges.append(term)
                            weights.append(contribution_weight)
            count = len(active_judges)
            if (count == 0):
                continue
            median = np.median(np.array(active_judges))
            mean = np.mean(np.array(active_judges))
            avg_daily_judge_count = np.sum(np.array(weights))
            weighted_mean = np.sum(np.array(active_judges) * np.array(weights)) / avg_daily_judge_count
            dist_court_wise_tenures_by_year.loc[len(dist_court_wise_tenures_by_year.index)] = [year, s, d, c, count, median, mean, weighted_mean, avg_daily_judge_count]
            
    
#     dist_court_wise_tenures_by_year.to_csv('generated/dist_court_wise_tenures_by_year.csv')
    return dist_court_wise_tenures_by_year


def plotDateDeltas(caseData, title):
    date_for_20 = re.compile('^20[0-9][0-9]-*')
    date_deltas = [(datetime.datetime.strptime(end_date,"%Y-%m-%d") - datetime.datetime.strptime(start_date,"%Y-%m-%d")).days for end_date, start_date in zip(caseData['date_of_decision'][caseData['date_of_decision'].notnull()], caseData['date_of_filing'][caseData['date_of_decision'].notnull()]) if (date_for_20.match(end_date) and (datetime.datetime.strptime(end_date,"%Y-%m-%d") - datetime.datetime.strptime(start_date,"%Y-%m-%d")).days > 0)]
    date_deltas_df = pd.DataFrame(date_deltas)
#     print(f'mean : {np.mean(date_deltas)}')
#     print(f'median : {np.median(date_deltas)}')
#     print(date_deltas_df.describe())
    plt.hist(date_deltas, bins = 40)
    plt.title(title)
    plt.xlabel('Days to decision')
    plt.ylabel('Number of cases')

    
def analyzeActIdsByYearState(years):
    #IPC, MV, NI
    #Criminal Cases, Motor Vehicles Act, Negotiable Items
#     years = [f'20{i}' for i in range(10,12)]

    date_for_20 = re.compile('^20[0-9][0-9]-*')

#     act_family = 'IPC'
#     act_family = 'MV'
    act_family = 'IPC'
    actFamilyDf = pd.read_csv(f'generated/filtered{act_family}Acts.csv')
    acts_sections = pd.read_csv('acts_sections.csv')
    acts_sections.drop(['section', 'bailable_ipc', 'number_sections_ipc', 'criminal'], axis = 1)
    acts_sections = acts_sections[acts_sections['ddl_case_id'].notnull()]
    acts_sections = acts_sections[acts_sections['act'].notnull()]

    ipcActsSections = acts_sections.merge(actFamilyDf, how = 'inner', on = ['act'])
    del acts_sections

    result = pd.DataFrame(columns = ['year', 'state_code', 'act_family', 'num_cases', 'median_decision_days', 'mean_decision_days', 'A_count', 'B_count', 'C_count', 'D_count', 'E_count'])

    for year in years:
        print(f'Processing year {year}')
        caseData = pd.read_csv(f'cases/_/cases_{year}.csv')
        # ddl_case_id	year	state_code	dist_code	court_no	date_of_filing	date_of_decision
        caseData.drop(['cino', 'judge_position', 'female_defendant', 'female_petitioner', 'female_adv_def', 'female_adv_pet', 'type_name', 'purpose_name', 'disp_name', 'date_first_list', 'date_last_list', 'date_next_list'], axis = 1)

        actFamilyCases = caseData.merge(ipcActsSections, how = 'inner', on = ['ddl_case_id'])
        del caseData

        stateCodes = actFamilyCases['state_code'].unique()
        for sc in stateCodes:
            stateCases = actFamilyCases[actFamilyCases['state_code'] == sc]
            date_deltas = [(datetime.datetime.strptime(end_date,"%Y-%m-%d") - datetime.datetime.strptime(start_date,"%Y-%m-%d")).days for end_date, start_date in zip(stateCases['date_of_decision'][stateCases['date_of_decision'].notnull()], stateCases['date_of_filing'][stateCases['date_of_decision'].notnull()]) if (date_for_20.match(end_date) and (datetime.datetime.strptime(end_date,"%Y-%m-%d") - datetime.datetime.strptime(start_date,"%Y-%m-%d")).days > 0)]

            date_deltas = np.array(date_deltas)
            aCount = np.sum(date_deltas <= 1 * 365)
            bCount = np.sum(date_deltas <= 3 * 365) - aCount
            cCount = np.sum(date_deltas <= 5 * 365) - (aCount + bCount)
            dCount = np.sum(date_deltas <= 10 * 365) - (aCount + bCount + cCount)
            eCount = np.sum(date_deltas > 10 * 365)
            if len(date_deltas) != 0:
                result.loc[len(result.index)] = [year, sc, act_family, len(date_deltas), np.median(date_deltas), np.mean(date_deltas), aCount, bCount, cCount, dCount, eCount]

    result.to_csv(f'generated/{act_family}_case_stats_by_year_state_{years[0]}.csv')

    
def analyzeActIdsByCourt():
    #IPC, MV, NI
    #Criminal Cases, Motor Vehicles Act, Negotiable Items
    years = [f'20{i}' for i in range(10,19)]
    
    date_for_20 = re.compile('^20[0-9][0-9]-*')
    
    act_family = 'NI'
    actFamilyDf = pd.read_csv(f'generated/filtered{act_family}Acts.csv')

    
    acts_sections = pd.read_csv('acts_sections.csv')
    acts_sections.drop(['section', 'bailable_ipc', 'number_sections_ipc', 'criminal'], axis = 1)
    acts_sections = acts_sections[acts_sections['ddl_case_id'].notnull()]
    acts_sections = acts_sections[acts_sections['act'].notnull()]

    actFamilyActsSections = acts_sections.merge(actFamilyDf, how = 'inner', on = ['act'])
    del acts_sections
    
    result = pd.DataFrame(columns = ['year', 'state_code', 'dist_code', 'court_no', 'act_family', 'num_cases', 'median_decision_days', 'mean_decision_days', 'A_count', 'B_count', 'C_count', 'D_count', 'E_count'])
    
    for year in years:
        print(f'Processing year : {year}')
        caseData = pd.read_csv(f'cases/_/cases_{year}.csv')
        # ddl_case_id	year	state_code	dist_code	court_no	date_of_filing	date_of_decision
        caseData.drop(['cino', 'judge_position', 'female_defendant', 'female_petitioner', 'female_adv_def', 'female_adv_pet', 'type_name', 'purpose_name', 'disp_name', 'date_first_list', 'date_last_list', 'date_next_list'], axis = 1)

        actFamilyCases = caseData.merge(actFamilyActsSections, how = 'inner', on = ['ddl_case_id'])
        print('Length of caseData : ', len(caseData))
        print('Length of actFamilyCases : ', len(actFamilyCases))
        del caseData
        
        stateCodes = actFamilyCases['state_code'].unique()
        for sc in stateCodes:
            stateCases = actFamilyCases[actFamilyCases['state_code'] == sc]
            dist_codes = stateCases['dist_code'].unique()
            for dc in dist_codes:
                distCases = stateCases[stateCases['dist_code'] == dc]
                court_nos = distCases['court_no'].unique()
                for cn in court_nos:
                    courtCases = distCases[distCases['court_no'] == cn]
                    date_deltas = [(datetime.datetime.strptime(end_date,"%Y-%m-%d") - datetime.datetime.strptime(start_date,"%Y-%m-%d")).days for end_date, start_date in zip(courtCases['date_of_decision'][courtCases['date_of_decision'].notnull()], courtCases['date_of_filing'][courtCases['date_of_decision'].notnull()]) if (date_for_20.match(end_date) and (datetime.datetime.strptime(end_date,"%Y-%m-%d") - datetime.datetime.strptime(start_date,"%Y-%m-%d")).days > 0)]
            
                    date_deltas = np.array(date_deltas)
                    aCount = np.sum(date_deltas <= 1 * 365)
                    bCount = np.sum(date_deltas <= 3 * 365) - aCount
                    cCount = np.sum(date_deltas <= 5 * 365) - (aCount + bCount)
                    dCount = np.sum(date_deltas <= 10 * 365) - (aCount + bCount + cCount)
                    eCount = np.sum(date_deltas > 10 * 365)
                    if len(date_deltas) != 0:
                        result.loc[len(result.index)] = [year, sc, dc, cn, act_family, len(date_deltas), np.median(date_deltas), np.mean(date_deltas), aCount, bCount, cCount, dCount, eCount]
    
    result.to_csv(f'generated/{act_family}_case_stats_by_year_court.csv')
    
    
def analyzeFilingToFirstList():
    date_for_20 = re.compile('^20[0-9][0-9]-*')

    years = [f'20{i}' for i in range(10,19)]
    for year in years:

        caseData = pd.read_csv(f'cases/_/cases_{year}.csv')
        caseData = caseData[caseData['date_of_filing'].notnull()]
        caseData = caseData[caseData['date_first_list'].notnull()]
        dateDeltas = [(datetime.datetime.strptime(first_list,"%Y-%m-%d") - datetime.datetime.strptime(start_date,"%Y-%m-%d")).days for first_list, start_date in zip(caseData['date_first_list'],
            caseData['date_of_filing']) if (date_for_20.match(first_list) and date_for_20.match(start_date) and (datetime.datetime.strptime(first_list,"%Y-%m-%d") - datetime.datetime.strptime(start_date,"%Y-%m-%d")).days > 0)]
        dateDeltas = np.array(dateDeltas)
        f = plt.figure()
        f.set_figwidth(10)
        f.set_figheight(10)
        plt.hist(dateDeltas[dateDeltas < 3650], bins = 40)
        plt.xlabel('Number of days')
        plt.ylabel('Number of cases')
        plt.title(f'Year : {year}')
        print(f'Year : {year}')
        print('median : ', np.median(dateDeltas))
        print('mean : ', np.mean(dateDeltas))
        plt.savefig(f'generated/first_listening_{year}.png')
        

def analyzeFilingToFirstListForCourts(courts):
    date_for_20 = re.compile('^20[0-9][0-9]-*')

    years = [f'20{i}' for i in range(10,19)]
    filingListPerYearDf = pd.DataFrame(columns = ['year', 'state_code', 'dist_code', 'court_no', 'mean_days', 'median_days'])
    filingListDf = pd.DataFrame(columns = ['state_code', 'dist_code', 'court_no', 'mean_days', 'median_days'])
    
    allDeltas = {}
    for year in years:
        print(f'Processing year {year}')
        caseData = pd.read_csv(f'generated/filtered_cases/cases_acts_{year}.csv')
        caseData = caseData[caseData['date_of_filing'].notnull()]
        caseData = caseData[caseData['date_first_list'].notnull()]
        
        for idx, row in courts.iterrows():
            court_data = caseData[caseData['state_code'] == row['state_code']]
            court_data = court_data[court_data['dist_code'] == row['dist_code']]
            court_data = court_data[court_data['court_no'] == row['court_no']]
            
            dateDeltas = [(datetime.datetime.strptime(first_list,"%Y-%m-%d") - datetime.datetime.strptime(start_date,"%Y-%m-%d")).days for first_list, start_date in zip(court_data['date_first_list'],
            court_data['date_of_filing']) if (date_for_20.match(first_list) and date_for_20.match(start_date) and (datetime.datetime.strptime(first_list,"%Y-%m-%d") - datetime.datetime.strptime(start_date,"%Y-%m-%d")).days > 0)]
            dateDeltas = np.array(dateDeltas)
            
            if len(dateDeltas) > 0:
                filingListPerYearDf.loc[len(filingListPerYearDf.index)] = [year, row['state_code'], row['dist_code'], row['court_no'], np.mean(dateDeltas), np.median(dateDeltas)]
            
                key = (row['state_code'], row['dist_code'], row['court_no'])
                if key not in allDeltas.keys():
                    allDeltas[key] = list(dateDeltas)
                else:
                    allDeltas[key].extend(dateDeltas)
                    
    for idx, row in courts.iterrows():
        key = (row['state_code'], row['dist_code'], row['court_no'])

        if key in allDeltas.keys():
            dateDeltas = allDeltas[key]
            if len(dateDeltas) > 0:
                filingListDf.loc[len(filingListDf.index)] = [row['state_code'], row['dist_code'], row['court_no'], np.mean(np.array(dateDeltas)), np.median(np.array(dateDeltas))]

            
    filingListDf.to_csv('generated/filingListDf_v2.csv')
    filingListPerYearDf.to_csv('generated/filingListPerYearDf_v2.csv')
            
#         f = plt.figure()
#         f.set_figwidth(10)
#         f.set_figheight(10)
#         plt.hist(dateDeltas[dateDeltas < 3650], bins = 40)
#         plt.xlabel('Number of days')
#         plt.ylabel('Number of cases')
#         plt.title(f'Year : {year}')
#         print(f'Year : {year}')
#         print('median : ', np.median(dateDeltas))
#         print('mean : ', np.mean(dateDeltas))
#         plt.savefig(f'generated/first_listening_{year}.png')

            
    
def getBestAndWorstCourts(caseStats, n = 15, minInstituted = 100, minDisposed = 0, minCount = 2):
    caseStats = caseStats[caseStats['num_instituted'] > minInstituted]
    caseStats = caseStats[caseStats['num_disposed'] > minDisposed]

    years = [f'20{i}' for i in range(10,19)]
    avgRanks = {}
    rankSum = {}
    yearCounts = {}
    for year in years:
        yearStats = caseStats[caseStats['year'] == int(year)]
        yearStats = yearStats.sort_values(by = 'median_decision_days', ascending = True, ignore_index = True)
        for idx, row in yearStats.iterrows():
            key = (row['state_code'], row['dist_code'], row['court_no'])
            if key not in rankSum.keys():
                rankSum[key] = idx
            else:
                rankSum[key] = rankSum[key] + idx
            
            if key not in yearCounts.keys():
                yearCounts[key] = 1
            else:
                yearCounts[key] = yearCounts[key] + 1
    
    for item in rankSum.items():
        if yearCounts[item[0]] >= minCount:
            avgRanks[item[0]] = item[1] / yearCounts[item[0]] # sum of ranks / number of times a key appears
    
    del rankSum
    allItems = [item for item in avgRanks.items()]
    del avgRanks
    allItems = sorted(allItems, key = lambda x : x[1])
    print(allItems[:n])
    print(allItems[-n:])
    
    bestCourts = [t[0] for t in allItems[:n]]
    worstCourts = [t[0] for t in allItems[-n:]]
    return bestCourts, worstCourts

def getRankedCourts(caseStats):
    years = [f'20{i}' for i in range(10,19)]
    rankSum = {}
    for year in years:
        yearStats = caseStats[caseStats['year'] == int(year)]
        yearStats = yearStats.sort_values(by = 'median_decision_days', ascending = True)
        for idx, row in yearStats.iterrows():
            key = (row['state_code'], row['dist_code'], row['court_no'])
            if key not in rankSum.keys():
                rankSum[key] = idx
            else:
                rankSum[key] = rankSum[key] + idx
    
    allItems = [item for item in rankSum.items()]
    del rankSum
    allItems = sorted(allItems, key = lambda x : x[1])
    rankedCourts = [t[0] for t in allItems]
    return rankedCourts

def analyzeCaseAgeDistributionByCourtYear(state_dist_court_df, cases_base_path,sc_idx, dc_idx, cn_idx, save_file):
    years = [f'20{i}' for i in range(10,19)]
    
    date_for_20 = re.compile('^20[0-9][0-9]-*')
    
    result = pd.DataFrame(columns = ['year', 'state_code', 'dist_code', 'court_no', 'num_cases', 'median_decision_days', 'mean_decision_days', 'A_count', 'B_count', 'C_count', 'D_count', 'E_count'])
    
    for year in years:
        print(f'Processing cases for year : {year}')
        case_data = pd.read_csv(f'{cases_base_path}/cases_acts_{year}.csv')
        
        for row in state_dist_court_df.itertuples():
            key = (row[sc_idx], row[dc_idx], row[cn_idx])
            s,d,c = row[sc_idx], row[dc_idx], row[cn_idx]
            
            
            court_case_data = case_data[case_data['state_code'] == s]
            court_case_data = court_case_data[court_case_data['dist_code'] == d]
            court_case_data = court_case_data[court_case_data['court_no'] == c]
                    
            date_deltas = [(datetime.datetime.strptime(end_date,"%Y-%m-%d") - datetime.datetime.strptime(start_date,"%Y-%m-%d")).days for end_date, start_date in zip(court_case_data['date_of_decision'][court_case_data['date_of_decision'].notnull()], court_case_data['date_of_filing'][court_case_data['date_of_decision'].notnull()]) if (date_for_20.match(end_date) and date_for_20.match(start_date) and (datetime.datetime.strptime(end_date,"%Y-%m-%d") - datetime.datetime.strptime(start_date,"%Y-%m-%d")).days > 0)]
            date_deltas = np.array(date_deltas)
            aCount = np.sum(date_deltas <= 1 * 365)
            bCount = np.sum(date_deltas <= 3 * 365) - aCount
            cCount = np.sum(date_deltas <= 5 * 365) - (aCount + bCount)
            dCount = np.sum(date_deltas <= 10 * 365) - (aCount + bCount + cCount)
            eCount = np.sum(date_deltas > 10 * 365)
            if len(date_deltas) != 0:
                result.loc[len(result.index)] = [year, s, d, c, len(date_deltas), np.median(date_deltas), np.mean(date_deltas), aCount, bCount, cCount, dCount, eCount]
    
    result.to_csv(save_file)