class QuarterBack:
    def __init__(self, name):
        self._name = name
        self._years = {}
        self._total_years = 0
        self._total_yards = 0
        self._total_touchdowns = 0
        self._total_interceptions = 0

    def add_year(self, year):
        self._years[year.get_year()] = year

    def get_years(self):
        return self._years

    def calculate_total_years(self):
        total_years = 0
        for year in self._years.values():  # iterate through YearStats instances
            total_years += 1
        self._total_years = total_years

    def calculate_total_yards(self):
        total_yards = 0
        for year_stats in self._years.values():
            total_yards += year_stats.get_passing_yards()
        self._total_yards = total_yards


    def calculate_total_touchdowns(self):
        total_touchdowns = 0
        for year in self._years.values():
            total_touchdowns += year.get_touchdowns()
        self._total_touchdowns = total_touchdowns

    def calculate_total_interceptions(self):
        total_interceptions = 0
        for year in self._years.values():
            total_interceptions += year.get_interceptions()
        
        self._total_interceptions = total_interceptions

    def get_name(self):
        return self._name

    def get_total_years(self):
        self.calculate_total_years()
        return self._total_years
    
    def get_total_yards(self):
        self.calculate_total_yards()
        return self._total_yards
    
    def get_total_touchdowns(self):
        self.calculate_total_touchdowns()
        return self._total_touchdowns
    
    def get_total_interceptions(self):
        self.calculate_total_interceptions()
        return self._total_interceptions
    
    def __str__(self):
        total_years = str(self.get_total_years())
        total_yards = str(self.get_total_yards())
        total_touchdowns = str(self.get_total_touchdowns())
        total_interceptions = str(self.get_total_interceptions())
        return "{} - Total Yards: {}, Total Years: {}, Touchdowns: {}, total Interceptions: {}".format(self._name, total_yards, total_years, total_touchdowns, total_interceptions)


class YearStats:
    def __init__(self, year,  passing_yards, touchdowns, interceptions, completed_pass):
        self._year = year
        self._passing_yards = passing_yards
        self._touchdowns = touchdowns
        self._interceptions = interceptions
        self._completed_pass = completed_pass

    def get_passing_yards(self):
        return self._passing_yards
    
    def get_year(self):
        return self._year
    
    def get_touchdowns(self):
        return self._touchdowns
    
    def get_interceptions(self):
        return self._interceptions
    
    def get_completed_pass(self):
        return self._completed_pass
    
    def __str__(self):
        return "{} stats - passing yards: {}, touchdowns: {}, interceptions: {}, completed pass {}%".format(self._year, self._passing_yards, self._touchdowns, self._interceptions, self._completed_pass)

class QuarterbackList:
    def __init__(self):
        self._list = []

    def get_list(self):
        return self._list

    def add_qb(self, qb):
        self._list.append(qb)

    def __contains__(self, qb_name):
        for qb in self._list:
            if qb.get_name() == qb_name:
                return True
        return False

    def get_qb(self, qb_name):
        for qb in self._list:
            if qb.get_name().lower() == qb_name.lower():
                return qb
        
        return None
    
    def get_stats_by_year(self, year):
        qb_stats = {}
        for qb in self._list:
            years_dict = qb.get_years()
            if year in years_dict.keys():
                qb_stats[qb.get_name()] = years_dict[year]
        
        return qb_stats



    

    
    


