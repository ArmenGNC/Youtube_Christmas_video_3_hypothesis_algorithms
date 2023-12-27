# Import libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import spiceypy.spiceypy as sp
import Calendars as ca
import dictionary as d


class Jesus_BirthDate_by_conjunction_method():

    def __init__(self, minimum_year, maximum_year, simplify_with_AU, langage_used, planet_1,planet_2):

        self.AU = 149597870.700  # km     1 Astronomic Unit (AU) = 149597870.700 km (or 150000000)
        self.minimum_year = minimum_year  # -10
        self.maximum_year = maximum_year  # 0
        self.list_julian_date = list(range(self.minimum_year, self.maximum_year))  # Interval with the researched years
        self.simplify_with_AU = simplify_with_AU  # False
        self.language_used = langage_used  # 'English' # Choose between English or French
        self.planet_1 = planet_1
        self.planet_2 = planet_2


    # Methods
    def Check_if_leap_year(self,year):

        ''' This method checks leap years. It perfectly works  for positive years. For negative years, there's a correction to applu bu hasn't been done here.'''

        if (year % 4 == 0 and year % 100 != 0 or year % 400 == 0):
            leap_year = True
        else:
            leap_year = False

        return leap_year

    def Date_to_str_SPICE(self,year,month,day,hour):

        ''' The goal of this method is to string a date. '''
        # Year character for SPICE
        str_year = ""
        if np.sign(year) == 1:
            str_year = str(year) + " AD"
        elif np.sign(year) == -1:
            str_year = str(-1*year) + " BC"
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

    def Conjunctions_with_global_day(self, year, simplify_with_AU, first_planet, second_planet):

        '''

        The goal of this method is to determine the angle between the two planets as seen from the Earth.

        '''

        # Check if the year is a leap year
        leap_year = self.Check_if_leap_year(year)

        all_conjunction_list_1 = []
        all_months_list = []
        all_days_list = []
        all_hours_list = []
        list_pos_earth = []  # List of cartesian position of Earth (list of an array)
        list_pos_venus = []  # List of cartesian position of Venus (list of an array)

        # '''
        #
        #     DE435 : Time span covered by ephemeris:
        #     1549-DEC-21 00:00 to   2650-JAN-25 00:00
        #
        #     DE441 : Time span covered by ephemeris:
        #     06-MAY--13200 00:00 to   30-JUL-1969 00:00
        #
        # '''


        # Loading kernels
        spice_files = ["./kernels/spk/de441.bsp","./kernels/spk/de441_part-2.bsp" ,"./kernels/spk/de431_part-1.bsp", "./kernels/lsk/naif0012.tls",
                       "./kernels/pck/de_403_masses.tpc"]
        sp.furnsh(spice_files)


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
                    # SPICE METHOD use
                    try:
                        str_date = self.Date_to_str_SPICE(year, i + 1, j + 1, k)
                        # print(str_date)
                        et = sp.str2et(str_date)
                        # print(et)

                        # Planet Earth position at these date
                        # # Positions
                        jup_pos_spice, other_jup = sp.spkpos(self.planet_1, et, "J2000", "NONE", "EARTH")
                        sat_pos_spice, other_sat = sp.spkpos(self.planet_2, et, "J2000", "NONE", "EARTH")

                        # Conjunction angle between the two planets
                        norm_jup_spice = jup_pos_spice / np.linalg.norm(jup_pos_spice)
                        norm_sat_spice = sat_pos_spice / np.linalg.norm(sat_pos_spice)

                        angle_sep = np.arccos(np.dot(norm_jup_spice, norm_sat_spice)) * 180 / np.pi

                        all_months_list.append(i + 1)
                        all_days_list.append(j + 1)
                        all_hours_list.append(k)
                        if simplify_with_AU == True:
                            all_conjunction_list_1.append(angle_sep)
                            list_pos_earth.append(jup_pos_spice/self.AU)
                            list_pos_venus.append(sat_pos_spice/self.AU)
                        else:
                            all_conjunction_list_1.append(angle_sep)
                            list_pos_earth.append(jup_pos_spice)
                            list_pos_venus.append(sat_pos_spice)

                        del str_date
                        del et
                    except:
                        pass
                        # print(" No leap year detected ! ")

        return all_months_list, all_days_list, all_hours_list, all_conjunction_list_1, list_pos_earth, list_pos_venus

    def Find_index_in_list(self, array, value):

        ''' This method aims to find an index thanks to a value stored inside a list'''

        index_value = 0

        for i in range(len(array)):

            if array[i] == value:
                index_value = i
                break
            else:
                pass

        return index_value

    def Determine_date_within_theyear_where_tiniest_angle(self, month_list, day_list, hour_list, angle_1_list,plan_1_list, plan_2_list):

        ''' The goal of this method is to determine the minimum conjunction angle in a given year '''

        # Minimum conjunction angle 1 in the year
        min_angle_1 = min(angle_1_list)

        # # Minimum conjunction angle 2 in the year
        # min_angle_2 = min(angle_2_list)

        # Determine the index in the list of the minimum conjunction angle 1 in the year
        index_of_minimum_distance = self.Find_index_in_list(angle_1_list, min_angle_1)

        # # Determine the index in the list of the minimum conjunction angle 2 in the year
        # index_of_minimum_distance = self.Find_index_in_list(angle_1_list, min_angle_2)

        # Determine the date
        exact_month, exact_day, exact_hour, exact_plan_1_pos, exact_plan_2_pos = month_list[index_of_minimum_distance], \
                                                                               day_list[index_of_minimum_distance], \
                                                                               hour_list[index_of_minimum_distance], \
                                                                               plan_1_list[index_of_minimum_distance], \
                                                                               plan_2_list[index_of_minimum_distance]

        return exact_month, exact_day, exact_hour, min_angle_1, exact_plan_1_pos, exact_plan_2_pos

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

    def Calculation_conjunction_angles_and_dates(self):

        # Algorithm
        # On a period we determine, for each year ,the nearest angle between Planete1 and Planete2
        Global_angle_list_1 = []
        Global_day_list = []
        list_year = []
        each_year_line = []
        count = 0
        arranged_elements = []
        numeric_date_for_3D_plot = []
        minimum_angle_list = []
        list_max_angle_for_plot_each_year = []


        for i in range(len(self.list_julian_date)):

            # Within the year, search the month at which we have the closest conjunction angle between Venus and the Earth
            month_list, day_list, hour_list, angle_1_list, plan1_list, plan2_list = self.Conjunctions_with_global_day(
                self.list_julian_date[i], self.simplify_with_AU, self.planet_1, self.planet_2)

            # For each year choose the date at which we have the minimum conjunction angle between Planete1 and Planete2
            exact_month, exact_day, exact_hour, minimum_angle, exact_plan_1_pos, exact_plan_2_pos = self.Determine_date_within_theyear_where_tiniest_angle(
                month_list, day_list, hour_list, angle_1_list, plan1_list, plan2_list)

            # Date expressed as a char for angle 1
            date_char_gregorian, date_char_julian, date_char_hebrew = self.Determine_char_date(self.list_julian_date[i], exact_month, exact_day, exact_hour,
                                                 self.language_used)

            # Put in a dataframe
            data_total = [date_char_gregorian, date_char_julian, date_char_hebrew, minimum_angle, exact_plan_1_pos[0], exact_plan_1_pos[1],
                    exact_plan_1_pos[2], exact_plan_2_pos[0], exact_plan_2_pos[1],
                    exact_plan_2_pos[2]]

            # Determining the maximum angle for plot scale
            list_max_angle_for_plot_each_year.append(max(angle_1_list))

            # Append
            list_year.append(self.list_julian_date[i])
            for j in range(len(hour_list)):
                Global_day_list.append(hour_list[j] + count)
            each_year_line.append(count)
            Global_angle_list_1.extend(angle_1_list)
            numeric_date_for_3D_plot.append([self.list_julian_date[i], exact_month, exact_day, exact_hour, date_char_gregorian])
            minimum_angle_list.append(minimum_angle)

            count += 8760

            # Append the list of elements (in the dataframe)
            arranged_elements.append(data_total)

        # Maximum value for the scale of the plot (we put it as a global so that we can easily use it)
        global maximum_for_plot_scale
        maximum_for_plot_scale = max(list_max_angle_for_plot_each_year)

        # Store the results in a pandas DataFrame structure
        if self.simplify_with_AU == True:
            df = pd.DataFrame(np.array(arranged_elements), columns=d.column_simplified_by_AU_conjunction[self.language_used])
        elif self.simplify_with_AU == False:
            df = pd.DataFrame(np.array(arranged_elements), columns=d.column_not_simplified_by_AU_conjunction[self.language_used])

        else:
            pass

        return Global_angle_list_1, each_year_line, Global_day_list, numeric_date_for_3D_plot, df , minimum_angle_list

    def Plot_angle_curves_in_timy_interval(self, Global_angle_list_1, each_year_line,save_plot):

        plt.figure()
        plt.plot(Global_angle_list_1, 'b')
        # for i in range(len(each_year_line)):
        #     plt.plot([each_year_line[i], each_year_line[i]], [0, maximum_for_plot_scale], 'r', linewidth=3)

        if self.language_used == "English":
            plt.xlabel(" Hours ellapsed since year " + str(self.minimum_year) + " [in hours] ")
            plt.ylabel(" Conjunction angle [deg] ")
            plt.title(" Conjunction angle between " + self.planet_1 + " and " + self.planet_2 + " [deg] ", fontsize=18)
            plt.grid(alpha=0.5)
        elif self.language_used == "French":
            plt.xlabel(" Nombre d'heures écoulées depuis l'année " + str(self.minimum_year) + " [en heures] ")
            plt.ylabel(" Angle de conjonction [deg] ")
            plt.title(" Angle de conjonction entre " + self.planet_1 + " et " + self.planet_2 + " [deg] ", fontsize=18)
            plt.grid(alpha=0.5)
        # plt.xlim([0, max(Global_day_list)])
        # plt.ylim([0, maximum_for_plot_scale])
        if save_plot == True:
            plt.savefig('conjunction_angle_curves_in_timy_interval.png')
        else:
            pass
        plt.show()

        return None

    def Build_the_text_document(self,df,minimum_year,maximum_year, langage_used):

        ''' This method writes results in text file.'''

        if langage_used == "English":
            f = open("Jupiter_Saturn_conjunction.txt",'w')
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
            f = open("Jupiter_Saturn_conjunction.txt", 'w',encoding = 'utf-8')
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