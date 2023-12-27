'''

The goal of this script is to determine an approximation of the Jesus' birth date using
the closest distance between Earth and Venus (or the evening star).


'''

#Import libraries
import numpy as np
import prototypeKeplerBC_with_params as pk
import matplotlib.pyplot as plt
import pandas as pd
import spiceypy.spiceypy as sp
import Calendars as ca
import dictionary as d

plt.style.use('dark_background')


class Jesus_BirthDate_by_EarthVenus_distance_method():

    # Initialization of variables
    def __init__(self, minimum_year, maximum_year, simplify_with_AU, langage_used, planet_1,planet_2):

        self.AU = 149597870.700  # km     1 Astronomic Unit (AU) = 149597870.700 km (or 150000000)
        self.minimum_year = int(minimum_year)  # -10
        self.maximum_year = int(maximum_year)  # 0
        self.list_julian_date = list(range(self.minimum_year, self.maximum_year))  # Interval with the researched years
        self.simplify_with_AU = simplify_with_AU  # False
        self.language_used = langage_used  # 'English' # Choose between English or French
        self.planet_1 = planet_1
        self.planet_2 = planet_2
        # Class instantiation
        self.kepler = pk.Solar_System()  # Instantiate solar system class


    # Methods
    def Check_if_leap_year(self,year):

        ''' This method checks leap years. It perfectly works  for positive years. For negative years, there's a correction to applu bu hasn't been done here.'''

        leap_year = False

        if (year % 4 == 0 and year % 100 != 0 or year % 400 == 0):
            leap_year = True
        else:
            leap_year = False

        return leap_year

    def Date_to_str_SPICE(self, year, month, day, hour):

        ''' The goal of this function is to string a date. '''
        # Year character for SPICE
        str_year = ""
        if np.sign(year) == 1:
            str_year = str(year) + " AD"
        elif np.sign(year) == -1:
            str_year = str(-1 * year) + " BC"
        else:
            pass

        str_month = ""

        if month == 1:
            str_month = "Jan"
        elif month == 2:
            str_month = "Feb"
        elif month == 3:
            str_month = "Mar"
        elif month == 4:
            str_month = "Apr"
        elif month == 5:
            str_month = "May"
        elif month == 6:
            str_month = "Jun"
        elif month == 7:
            str_month = "Jul"
        elif month == 8:
            str_month = "Aug"
        elif month == 9:
            str_month = "Sep"
        elif month == 10:
            str_month = "Oct"
        elif month == 11:
            str_month = "Nov"
        elif month == 12:
            str_month = "Dec"
        else:
            pass

        str_new_hour = ""

        if len(str(hour)) == 1:
            str_new_hour = "0" + str(hour)
        else:
            str_new_hour = str(hour)

        str_date = str_year + " " + str_month + " " + str(day) + ", " + str_new_hour + ":00:00 UTC"

        return str_date

    def Closest_distance_with_global_day(self, year, simplify_with_AU, first_planet, second_planet):

        '''

        The goal of this method is to calculate distance between Venus and Earth in a time interval.

        '''

        all_distances_list = []
        all_months_list = []
        all_days_list = []
        all_hours_list = []
        list_pos_earth = []  # List of cartesian position of Earth (list of an array)
        list_pos_venus = []  # List of cartesian position of Venus (list of an array)


            # Loading kernels
        spice_files = ["./kernels/spk/de441.bsp","./kernels/spk/de441_part-2.bsp","./kernels/spk/de431_part-1.bsp", "./kernels/lsk/naif0012.tls",
                       "./kernels/pck/de_403_masses.tpc"]
        sp.furnsh(spice_files)



        # Leap year determination
        leap_year = self.Check_if_leap_year(year)

        for i in range(12):
            # Test if a month is even or odd
            if (i + 1) % 2 == 1 and (i+1) < 9:
                length_day = 31
            elif (i + 1) % 2 == 0 and (i+1) != 2 and (i+1)<8:
                length_day = 30
            # For August
            elif (i + 1) % 2 == 0 and (i+1) == 8:
                length_day = 31
            # For September
            elif (i + 1) % 2 == 1 and (i+1) == 9:
                length_day = 30
            # For October
            elif (i + 1) % 2 == 0 and (i+1) == 10:
                length_day = 31
            # For November
            elif (i + 1) % 2 == 1 and (i+1) == 11:
                length_day = 30
            # For December
            elif (i + 1) % 2 == 0 and (i+1) == 12:
                length_day = 31
            # For November
            elif (i + 1) % 2 == 1 and (i+1) == 11:
                length_day = 30
            # For leap year and February
            elif leap_year == True and (i+1) == 2:
                length_day = 29
            # For no leap year and February
            elif leap_year == False and (i+1) == 2:
                length_day = 28
            else:
                pass
            for j in range(length_day):
                for k in range(24):
                    # Using SPICE
                    try:
                        str_date = self.Date_to_str_SPICE(year, i + 1, j + 1, k)
                        # print(str_date)
                        et = sp.str2et(str_date)
                        # print(et)

                        # Planet Earth position at these date
                        # # Positions
                        plan1_pos_spice, other_jup = sp.spkpos(self.planet_1, et, "J2000", "NONE", "SUN")
                        plan2_pos_spice, other_sat = sp.spkpos(self.planet_2, et, "J2000", "NONE", "SUN")

                        # Distance between the two planets
                        distance = np.linalg.norm(plan2_pos_spice - plan1_pos_spice)

                        all_months_list.append(i + 1)
                        all_days_list.append(j + 1)
                        all_hours_list.append(k)
                        if simplify_with_AU == True:
                            all_distances_list.append(distance/self.AU)
                            list_pos_earth.append(plan2_pos_spice/self.AU)
                            list_pos_venus.append(plan1_pos_spice/self.AU)
                        else:
                            all_distances_list.append(distance)
                            list_pos_earth.append(plan2_pos_spice)
                            list_pos_venus.append(plan1_pos_spice)

                    except:
                        pass


        return all_months_list, all_days_list, all_hours_list, all_distances_list, list_pos_earth, list_pos_venus

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

    def Determine_date_within_theyear_where_tiniest_distance(self, month_list, day_list, hour_list, distance_list,
                                                             earth_list, venus_list):

        # Minimum distance in the year
        min_dist = min(distance_list)

        # Determine the index in the list of the minimum distance in the year
        index_of_minimum_distance = self.Find_index_in_list(distance_list, min_dist)

        # Determine the date
        exact_month, exact_day, exact_hour, exact_earth_pos, exact_venus_pos = month_list[index_of_minimum_distance], \
                                                                               day_list[index_of_minimum_distance], \
                                                                               hour_list[index_of_minimum_distance], \
                                                                               earth_list[index_of_minimum_distance], \
                                                                               venus_list[index_of_minimum_distance]

        return exact_month, exact_day, exact_hour, min_dist, exact_earth_pos, exact_venus_pos

    def Determine_char_date(self, year, exact_month, exact_day, exact_hour, language):

        '''
            This method convert dates and render them as characters

        '''

        str_full_date_gregorian = ""
        str_full_date_julian = ""
        str_full_date_hebrew = ""


        # Convert from gregorian to julian days
        decimal_day, A_new, M_new, Q_new = ca.From_gregorian_calendar_to_julian_days(year, exact_month, exact_day)


        # Convert in hebrew calendar
        A_heb,M_heb,D_heb = ca.From_julian_days_to_hebrew_calendar(decimal_day)


        # # Select a month among calendars (Month)
        str_month_gregorian = (d.structure_month[language])[exact_month-1]
        try:
            str_month_julian = (d.structure_month[language])[M_new-1]
        except:
            str_month_julian = " ______ "
        try:
            str_month_hebrew = (d.structure_month["Hebrew_phon"])[M_heb-1]
        except:
            str_month_hebrew = " ______ "

        int_day_gregorian =exact_day
        int_day_julian = Q_new
        int_day_hebrew = D_heb

        # Hours
        int_hour_gregorian = exact_hour
        int_hour_julian = 0


        # Determining the string date
        if language == "English":

            str_full_date_gregorian = str_month_gregorian + " " + str(int_day_gregorian) + ", " + str(year) + ", " + str(int_hour_gregorian) + ":00:00 UTC+00"
            str_full_date_julian = str_month_julian + " " + str(int_day_julian) + ", " + str(A_new) + ", " + str(int_hour_julian) + ":00:00 UTC+00"
            str_full_date_hebrew = str_month_hebrew + " " + str(int_day_hebrew) + ", " + str(A_heb)


        elif language == "French":

            str_full_date_gregorian = str(int_day_gregorian) + " " + str_month_gregorian + " " + str(year) + ", " + str(int_hour_gregorian) + ":00:00 UTC+00"
            str_full_date_julian = str(int_day_julian) + " " + str_month_julian + " " + str(A_new) + ", " + str(int_hour_julian) + ":00:00 UTC+00"
            str_full_date_hebrew = str(int_day_hebrew) + " " + str_month_hebrew + " " + str(A_heb)


        return str_full_date_gregorian, str_full_date_julian, str_full_date_hebrew

    def Calculation_distances_and_dates(self):


        # Algorithm
        # On a period we determine, for each year ,the nearest position between Venus and Earth
        Global_distance_list = []
        Global_day_list = []
        list_year = []
        each_year_line = []
        count = 0
        arranged_elements = []
        numeric_date_for_3D_plot = []
        minimum_distance_list = []
        list_max_dist_for_plot_each_year = []


        for i in range(len(self.list_julian_date)):

            # Within the year, search the month at which we have the closest distance between Venus and the Earth
            month_list, day_list, hour_list, distance_list, earth_list, venus_list = self.Closest_distance_with_global_day(
                self.list_julian_date[i], self.simplify_with_AU, self.planet_1, self.planet_2)

            # For each year choose the date at which we have the minimum distance between Earth and Mars
            exact_month, exact_day, exact_hour, minimum_distance, exact_earth_pos, exact_venus_pos = self.Determine_date_within_theyear_where_tiniest_distance(
                month_list, day_list, hour_list, distance_list, earth_list, venus_list)

            # Date expressed as a char
            date_char_greg,date_char_ju , date_char_heb = self.Determine_char_date(self.list_julian_date[i], exact_month, exact_day, exact_hour,
                                                 self.language_used)

            # Put in a dataframe
            data = [date_char_greg,date_char_ju ,date_char_heb, minimum_distance, exact_earth_pos[0], exact_earth_pos[1],
                    exact_earth_pos[2], exact_venus_pos[0], exact_venus_pos[1],
                    exact_venus_pos[2]]

            # Determining the maximum distance for plot scale
            list_max_dist_for_plot_each_year.append(max(distance_list))


            # Append
            list_year.append(self.list_julian_date[i])
            for j in range(len(hour_list)):
                Global_day_list.append(hour_list[j] + count)
            each_year_line.append(count)
            Global_distance_list.extend(distance_list)
            numeric_date_for_3D_plot.append([self.list_julian_date[i], exact_month, exact_day, exact_hour, date_char_greg])  # A correction to make to be in an exact form
            minimum_distance_list.append(minimum_distance)

            count += 8760

            # Append the list of elements (in the dataframe)
            arranged_elements.append(data)

        # Maximum value for the scale of the plot (we put it as a global so that we can easily use it)
        global maximum_for_plot_scale
        maximum_for_plot_scale = max(list_max_dist_for_plot_each_year)

        # Store the results in a pandas DataFrame structure
        if self.simplify_with_AU == True:
            df = pd.DataFrame(np.array(arranged_elements), columns=d.column_simplified_by_AU_Venus[self.language_used])
        elif self.simplify_with_AU == False:
            df = pd.DataFrame(np.array(arranged_elements), columns=d.column_not_simplified_by_AU_Venus[self.language_used])

        else:
            pass

        return Global_distance_list, each_year_line, Global_day_list, numeric_date_for_3D_plot, df , minimum_distance

    def Plot_distances_curves_in_timy_interval(self, Global_distance_list, each_year_line, Global_day_list,save_plot):

        plt.figure()
        # axes = plt.gca()
        plt.plot(Global_distance_list, 'b')
        for i in range(len(each_year_line)):
            plt.plot([each_year_line[i], each_year_line[i]], [0, maximum_for_plot_scale], 'r', linewidth=3)
            # text_label_for_plot.append((str(list_julian_date[i]) + " BC"))

        if self.simplify_with_AU == False:
            if self.language_used == "English":
                plt.xlabel(" Hours ellapsed since year " + str(self.minimum_year) + " [in hours] ")
                plt.ylabel(" Distance [km] ")
                plt.title(" Distance between " + self.planet_1 + " and " + self.planet_2 + " [km] ", fontsize=18)
            elif self.language_used == "French":
                plt.xlabel(" Nombre d'heures écoulées depuis l'année " + str(self.minimum_year) + " [en heures] ")
                plt.ylabel(" Distance [km] ")
                plt.title(" Distance entre " + self.planet_1 + " et " + self.planet_2 + " [km] ", fontsize=18)

        elif self.simplify_with_AU == True:
            if self.language_used == "English":
                plt.xlabel(" Hours ellapsed since year " + str(self.minimum_year) + " [in hours] ")
                plt.ylabel(" Distance (xAU) [km] ")
                plt.title(" Distance between " + self.planet_1 + " and " + self.planet_2 + " (xAU) [km] ", fontsize=18)
            elif self.language_used == "French":
                plt.xlabel(" Nombre d'heures écoulées depuis l'année " + str(self.minimum_year) + " [en heures] ")
                plt.ylabel(" Distance (xAU) [km] ")
                plt.title(" Distance entre " + self.planet_1 + " and " + self.planet_2 + " (xAU) [km] ", fontsize=18)
        else:
            pass
        # axes.xaxis.set_ticks(range(len(each_year_line)))
        # axes.xaxis.set_ticklabels(text_label_for_plot)
        plt.grid(alpha=0.5)
        plt.xlim([0, max(Global_day_list)])
        plt.ylim([0, maximum_for_plot_scale])
        if save_plot == True:
            plt.savefig('distance_curve_in_timy_interval.png')
        else:
            pass
        plt.show()

        return None

    def Plot_each_date_in_3D(self, numeric_date):

        ''' The goal of this function is to visualize the planet's position at a specific date. '''

        a = ["go", "mo", "bo", "ro"]
        b = ["g-", "m-", "b-", "r-"]

        for k in range(len(numeric_date)):

            fig = plt.figure()
            ax = fig.gca(projection='3d')
            t = self.kepler.t(
                self.kepler.dateJulienne(numeric_date[k][0], numeric_date[k][1], numeric_date[k][2], numeric_date[k][3],
                                         0, 0))
            i = 0
            # Sun plot
            ax.scatter([0], [0], [0], c='y', s=700, label=" Sun ")
            for planete in ["Mercury", "Venus", "Earth","Mars"]:  # ["Mercury","Venus","Earth","Mars","Jupiter", "Saturn","Uranus","Neptune","Pluto"]:
                (X, Y, Z) = self.kepler.ellipse_XYZ(planete, t)
                ax.plot3D(X, Y, Z, b[i], label=planete + " orbit")
                (X, Y, Z) = self.kepler.position_XYZ(planete, t)
                ax.plot3D([X], [Y], [Z], a[i], label=planete)
                i += 1

            ax.set_xlabel('X ')
            ax.set_ylabel(' Y ')
            ax.set_zlabel(' Z ')
            # Title
            gather_txt = " Solar system at epoch " + numeric_date[k][4]
            ax.set_title(gather_txt)
            # plt.axis([-2, 2, -2, 2])
            plt.legend(loc="upper right")
            plt.show()
        #
        return None

    def Build_the_text_document(self,df,minimum_year,maximum_year, langage_used):

        ''' This method writes results in text file.'''

        if langage_used == "English":
            f = open("VenusEarth_distance.txt",'w')
            f.write(" Here are the results : \n")
            f.write(" Parameters used : \n")
            f.write(" _ Minimum year taken into account = " + " January 1st " + str(minimum_year) + " 00:00:00 UTC (Gregorian calendar) \n")
            f.write(" _ Maximum year taken into account = " + " December 31th " + str(maximum_year) + " 23:00:00 UTC (Gregorian calendar) \n")
            f.write(" _ 1 AU = 149597870.700 km (or 150000000 km)\n")
            f.write(" All coordinates are expressed in J2000 reference frame.\n")
            f.write("\n")
            df_string = df.to_string(header=True, index=True)
            f.write(df_string)
        elif langage_used == "French":
            f = open("VenusEarth_distance.txt", 'w',encoding = 'utf-8')
            f.write(" Voici les résultats : \n")
            f.write(" Paramètres utilisés : \n")
            f.write(" _ Année minimum = " + " 1er janvier " + str(minimum_year) + " 00:00:00 UTC (calendrier grégorien) \n")
            f.write(" _ Année maximum = " + " 31 décembre " + str(maximum_year) + " 23:00:00 UTC (calendrier grégorien) \n")
            f.write(" _ 1 AU = 149597870.700 km (or 150000000 km)\n")
            f.write(" Toutes les coordonnées sont exprimées dans le repère J2000.\n")
            f.write("\n")
            df_string = df.to_string(header=True, index=True)
            f.write(df_string)
            f.close()

        return None