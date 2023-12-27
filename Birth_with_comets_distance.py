# Import libraries
import numpy as np
import prototypeKeplerBC_with_params as pk
from scipy.integrate import odeint
import Calendars as c
import pandas as pd
import dictionary as d


''' ---------------------------------------- Birth date with the comets -------------------------------------------- '''

class Jesus_BirthDate_by_comets_distance_method():

    # Variables
    def __init__(self, minimum_year, maximum_year, simplify_with_AU, langage_used,max_born):

        self.AU = 149597870.700  # km     1 Astronomic Unit (AU) = 149597870.700 km (or 150000000)
        self.minimum_year = int(minimum_year)
        self.maximum_year = int(maximum_year)
        self.list_julian_date = list(range(self.minimum_year, self.maximum_year))
        self.simplify_with_AU = simplify_with_AU  # False
        self.language_used = langage_used  # 'English' # Choose between English or French
        # Class instantiation
        self.kepler = pk.Solar_System()  # Instantiate solar system class
        self.maximum_born = max_born

    # Methods
    def Calculation_distance_Earth_comets(self, time_array,comet_positions):

        ''' The goal of this method is to determine the distance bewtween Earth and a comet during a period of time '''

        # List
        distance = []

        # List of a comet's coordinates (cartesian coordinates)
        x_sun_comet , y_sun_comet , z_sun_comet = comet_positions[:,0] , comet_positions[:,1] , comet_positions[:,2]   # in AU


        # Calculating the distance between Earth and a comet (in the list of comet)
        for i in range(len(time_array)):

            # Earth's position at the mentioned dates in the time_array list
            (X_Sun_Earth, Y_Sun_Earth, Z_Sun_Earth) = self.kepler.position_XYZ("Earth", time_array[i])   # in AU

            # Distances between Earth and comet in a specified date [in km]
            distance_Earth_comet = (np.sqrt((x_sun_comet[i] - X_Sun_Earth)**2 + (y_sun_comet[i] - Y_Sun_Earth)**2 + (z_sun_comet[i] - Z_Sun_Earth)**2))*self.AU


            distance.append(distance_Earth_comet)

        # Minimum distance for one comet in a period of time
        minimum_distance = min(distance)

        # Date at which we have the minimum distance
        index_minimum_distance = self.Find_index_in_list(distance,minimum_distance)
        date_for_minimum_distance = time_array[index_minimum_distance]

        return distance, minimum_distance, date_for_minimum_distance

    def Find_index_in_list(self,array,value):

        ''' This method aims to find an index thanks to a value stored inside a list'''

        index_value = 0

        for i in range(len(array)):

            if array[i] == value:
                index_value = i
                break
            else:
                pass

        return index_value

    def Create_structure_of_data(self,date_min_distance,comet_name,minimum_distance):

        ''' This method converts dates. '''

        # Convert dates in julian, gregorian and hebrew calendar
        # From julian date since J2000 to julian days
        JJ = 36525 * date_min_distance + 2451545

        # Convert in a julian calendar
        year_comet_julian, month_comet_julian, day_comet_julian, hour_comet_julian, minute_comet_julian, second_comet_julian = c.From_julian_days_to_julian_calendar(
            JJ)
        # Convert in a gregorian calendar
        year_comet_gregorian, month_comet_gregorian, day_comet_gregorian, hour_comet_gregorian, minute_comet_gregorian, second_comet_gregorian = c.From_julian_days_to_gregorian_calendar(
            JJ)
        # Convert in a gregorian calendar
        year_comet_hebrew, month_comet_hebrew, day_comet_hebrew = c.From_julian_days_to_hebrew_calendar(
            JJ)

        # For the year we must add 1 to the result because initialy we remove one as the solar system calss takes the 0 year into account.
        # char dates
        if self.language_used == "French":
            char_julian_date = str(day_comet_julian) + " " + (d.structure_month[self.language_used])[
                month_comet_julian - 1] + " " + str(year_comet_julian+1)
            char_gregorian_date = str(day_comet_gregorian) + " " + (d.structure_month[self.language_used])[
                month_comet_gregorian - 1] + " " + str(year_comet_gregorian+1)
            char_hebrew_date = str(day_comet_hebrew) + " " + (d.structure_month["Hebrew_phon"])[
                month_comet_hebrew - 1] + " " + str(year_comet_hebrew+1)

        elif self.language_used == "English":
            char_julian_date = (d.structure_month[self.language_used])[
                                   month_comet_julian - 1] + " " + str(day_comet_julian) + " " + str(
                year_comet_julian+1)
            char_gregorian_date = (d.structure_month[self.language_used])[
                                      month_comet_gregorian - 1] + " " + str(day_comet_gregorian) + " " + str(
                year_comet_gregorian+1)
            char_hebrew_date = (d.structure_month["Hebrew_phon"])[
                                   month_comet_hebrew - 1] + " " + str(day_comet_hebrew) + " " + str(
                year_comet_hebrew+1)

        else:
            pass

        # Data to gather all dates and distances
        data_full = [char_gregorian_date, char_julian_date, char_hebrew_date, comet_name, str(minimum_distance)]


        return data_full

    def Calculation_comete_positions(self):

        '''

        The goal of this method is to determine comets position and to pick their minimum distance with Earth in time interval
        A theshold is applied to pick only data of interest

        '''

        # Retrieve all comet's codes (Don't forget to remove [0:1])
        codes = (pk.Solar_System().retrieve_comete_code)    # [0:1]

        print(" Nombre de comètes " , len(codes))

        # Times
        t_start = self.kepler.t(self.kepler.dateJulienne(self.minimum_year, 1, 1, 12, 0, 0))  # kepler.comete_dj[code]
        t_end = self.kepler.t(self.kepler.dateJulienne(self.maximum_year, 12, 31, 12, 0, 0))  # kepler.comete_dj[code]
        temps = np.linspace(t_start, t_end, 2000)


        # Lists
        Yi_gathered = []
        Potential_candidate_name , Potential_candidate_distance , Potential_candidate_date_julian = [] , [] , []
        arranged_elements = []

        for code in range(len(codes)):

            # Initial conditions
            Yi = self.kepler.comete_Yi[codes[code]]

            # Calculating comet positions
            planetes = ["Mercury", "Venus", "Earth", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune"]
            Y = odeint(pk.systeme_comete, Yi, temps, args=(self.kepler, planetes), atol=1e-12, rtol=1e-6)

            # Calculation distance between the comet and Earth and determining its minimum distance with Earth in the timy period
            distance, minimum_distance, date_min_distance = self.Calculation_distance_Earth_comets(temps,Y)

            # We choose if we want a distance in UA or km
            if self.simplify_with_AU == True:
                minimum_distance_to_retrieve = minimum_distance/self.AU
            elif self.simplify_with_AU == False:
                minimum_distance_to_retrieve = minimum_distance
            else:
                pass

            # Comparition with the minimum distance
            if minimum_distance <= self.maximum_born:
                Potential_candidate_name.append(codes[code])
                Potential_candidate_distance.append(minimum_distance_to_retrieve)
                # For calendars
                Potential_candidate_date_julian.append(date_min_distance)
                # Create the structure in which we will get the dates, comet's name and the minimum distance between Earth and the comet
                data_comet = self.Create_structure_of_data(date_min_distance, codes[code], minimum_distance_to_retrieve)
                arranged_elements.append(data_comet)

            else:
                pass

            Yi_gathered.append(Y)

        # We take minimum distance in AU
        if self.simplify_with_AU == True:
            df = pd.DataFrame(np.array(arranged_elements), columns=d.column_simplified_by_AU_comets[self.language_used])
        # We take minimum distance in km
        elif self.simplify_with_AU == False:
            df = pd.DataFrame(np.array(arranged_elements), columns=d.column_not_simplified_by_AU_comets[self.language_used])


        return Yi_gathered, Potential_candidate_name, df

    def Build_the_text_document(self,df,maximum_born,minimum_year,maximum_year, langage_used):

        ''' This method writes results in text file.'''

        if langage_used == "English":
            f = open("EarthComets_distances.txt",'w')
            f.write(" Here are the results : \n")
            f.write(" Parameters used : \n")
            f.write(" _ Threshold = " + str(maximum_born) + " km (comet(s) located between 0 km to " + str(maximum_born) + " km from the Earth) \n")
            f.write(" _ Minimum year taken into account = " + " January 1st " + str(minimum_year) + " 12:00:00 UTC (Julian calendar) \n")
            f.write(" _ Maximum year taken into account = " + " December 31th " + str(maximum_year) + " 12:00:00 UTC (Julian calendar) \n")
            f.write(" _ 1 AU = 149597870.700 km (or 150000000 km)\n")
            f.write(" All coordinates are expressed in J2000 reference frame.\n")
            f.write("\n")
            df_string = df.to_string(header=True, index=True)
            f.write(df_string)
            f.close()
        elif langage_used == "French":
            f = open("EarthComets_distances.txt",'w',encoding = 'utf-8')
            f.write(" Voici les résultats : \n")
            f.write(" Paramètres utilisés : \n")
            f.write(" _ Seuil = " + str(maximum_born) + " km (comète(s) située(s) entre 0 km et " + str(maximum_born) + " km de la Terre) \n")
            f.write(" _ Année minimum = " + " 1er janvier " + str(minimum_year) + " 12:00:00 UTC (calendrier julien) \n")
            f.write(" _ Année maximum = " + " 31 décembre " + str(maximum_year) + " 12:00:00 UTC (calendrier julien) \n")
            f.write(" _ 1 AU = 149597870.700 km (or 150000000 km)\n")
            f.write(" Toutes les coordonnées sont exprimées dans le repère J2000. \n")
            f.write("\n")
            df_string = df.to_string(header=True, index=True)
            f.write(df_string)
            f.close()

        else:
            pass

        return None