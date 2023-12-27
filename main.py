# Import libraries
import matplotlib.pyplot as plt
import Birth_with_VenusEarth_distance as ve
import Birth_with_comets_distance as c
import Birth_with_planets_conjunction as conj
plt.style.use('dark_background')


def Execute_method_VenusEarth_distance():

    ''' In this function, distance between Venus and Earth is calculated. The library used is SPICEYPY. Here are some information:

        _ Tool = The SPICEYPY library is used
        - langage_used = "French" or "English"
        _ planet choice = "Mercury", "Venus", "Earth", "MARS BARYCENTER", "JUPITER BARYCENTER", "SATURN BARYCENTER" , "URANUS BARYCENTER", "NEPTUNE BARYCENTER", "PLUTO BARYCENTER"
        _ simplify_with_AU = True or False. If true, the distances will be given in Astronomic Unit (AU). Otherwise, distances will be give in km
        _ 1 AU = 149597870.700 km (or 150000000 km)
        _ minimum_year and maximum_year are integers


        The time interval is located between 06-MAY--13200 00:00 and 15-MAR-17191 00:00 (SPICEYPY library use)

    '''

    # # # Instantiation Venus, Earth class
    minimum_year, maximum_year, simplify_with_AU, langage_used, planet_1, planet_2 = -10,-2,False,'French', "Earth", "Venus"
    instance_ve = ve.Jesus_BirthDate_by_EarthVenus_distance_method(minimum_year, maximum_year, simplify_with_AU, langage_used, planet_1, planet_2)

    Global_distance_list, each_year_line, Global_day_list, numeric_date_for_3D_plot, df, min_dist_planets_each_year = instance_ve.Calculation_distances_and_dates()

    # Plots
    instance_ve.Plot_distances_curves_in_timy_interval(Global_distance_list,each_year_line,Global_day_list,True)  # Revoir ces courbes
    # instance_ve.Plot_each_date_in_3D(numeric_date_for_3D_plot)


    # Store results in a text
    instance_ve.Build_the_text_document(df,minimum_year,maximum_year,langage_used)

    del Global_distance_list
    del each_year_line
    del Global_day_list
    del numeric_date_for_3D_plot
    del df

    return None

def Execute_method_comets_illumination():

    '''
         In this function, distance between Venus and Earth is calculated. The library used is SPICEYPY. Here are some information:
         _
         The choice of the minimum_year and maximum_year must be added by 1. Indeed, Jesus_BirthDate_by_comets_distance class takes dates at year 0 whereas
         It is not possible to do it for the other functions (Execute_method_VenusEarth_distance and Execute_method_JupiterSaturn_conjunction) because
         the SPICEYPY library doesn't take the dates at year 0.
         For example, if you want a minimum_year set to -3, you have to add 1. Minimum_year = 2 in this example.

         Instead of minimum_year = -6 and maximum_year = -4, we will use minimum_year = -5 and maximum_year = -3

    '''


    # Threshold
    max_born = 2000000.0    # 246883194.91 [in km]

    # Instantiation with comets
    minimum_year, maximum_year, simplify_with_UA, langage_used = -5,-3,True,'French'
    instance_class_comet = c.Jesus_BirthDate_by_comets_distance_method(minimum_year, maximum_year, simplify_with_UA, langage_used,max_born)
    instance_comet, candidate_name, strcture_data_comet = instance_class_comet.Calculation_comete_positions()

    # Print result in a document
    instance_class_comet.Build_the_text_document(strcture_data_comet,max_born,minimum_year, maximum_year, langage_used)

    print(" Nombre de candidats potentiels : ", len(candidate_name))
    print(" Nom des candidats : ", candidate_name)

    return None

def Execute_method_JupiterSaturn_conjunction():


    ''' In this function, conjunction between Jupiter and Saturn is calculated. The library used is SPICEYPY. Here are some indication:

        _ Tool = The SPICEYPY library is used
        - langage_used = "French" or "English"
        _ planet choice = "Mercury", "Venus", "Earth", "MARS BARYCENTER", "JUPITER BARYCENTER", "SATURN BARYCENTER" , "URANUS BARYCENTER", "NEPTUNE BARYCENTER", "PLUTO BARYCENTER"
        _ simplify_with_AU = True or False. If true, the distances will be given in Astronomic Unit (AU). Otherwise, distances will be give in km
        _ 1 AU = 149597870.700 km (or 150000000 km)
        _ minimum_year and maximum_year are integers

        The time interval is located between 06-MAY--13200 00:00 and 15-MAR-17191 00:00 (SPICEYPY library use)

    '''


    ## Instantiation conjunction class
    minimum_year, maximum_year, simplify_with_AU, langage_used, planet_1, planet_2 = -10,-1,True,'French', "JUPITER BARYCENTER", "SATURN BARYCENTER"
    instance_conj = conj.Jesus_BirthDate_by_conjunction_method(minimum_year, maximum_year, simplify_with_AU, langage_used, planet_1, planet_2)

    Global_angle_list_1, each_year_line, Global_day_list, numeric_date_for_3D_plot, df_angle, min_angle_planets_each_year = instance_conj.Calculation_conjunction_angles_and_dates()

    # Plots
    instance_conj.Plot_angle_curves_in_timy_interval(Global_angle_list_1,each_year_line,True)  # Revoir ces courbes

    # Results in a text file
    instance_conj.Build_the_text_document(df_angle,minimum_year, maximum_year,langage_used)


    return None


if "__main__":

    # Initialization
    print('Bonjour,')
    print(" Quelle méthode voulez-vous utiliser :")
    print("  _ Méthode 1 : Distance Venus-Terre")
    print("  _ Méthode 2 : Distance Terre-comète")
    print("  _ Méthode 3 : Conjonction planète Jupiter-Saturne")
    print(" Pour séléctionner la méthode, veuillez simplement renseigner le numéro de la méthode.")
    print(" C'est-à-dire 1,2 ou 3 : ")

    valid = False
    count = 0
    while not valid:
        if count == 0:
            pass
        else:
            print(" Essayez encore. Un faux numéro a été renseigné")
        nn = input(" ")
        valid = nn.isdigit()
        count += 1

    choice = int(nn)

    if choice == 1:
        # Method 1 : Venus-Earth distance
        print(" ------------------------------------------- ")
        print(" Exécution de la méthode 1")
        print("...")
        Execute_method_VenusEarth_distance()
        print(" Un fichier 'VenusEarth_distance.txt' contenant les résultats de cette méthode se trouve à votre disposition. ")
        print(" Fin d'exécution de la méthode 1.")
        print(" ------------------------------------------- ")
        print(" Merci d'avoir utilisé l'outil")
    elif choice == 2:
        # Method 2 : Comets distance and illumination
        print(" ------------------------------------------- ")
        print(" Exécution de la méthode 2")
        print("...")
        Execute_method_comets_illumination()
        print(" Un fichier 'EarthComets_distances.txt' contenant les résultats de cette méthode se trouve à votre disposition. ")
        print(" Fin d'exécution de la méthode 2.")
        print(" ------------------------------------------- ")
        print(" Merci d'avoir utilisé l'outil")


    elif choice == 3:
        # Method 3 : Venus-Earth distance
        print(" ------------------------------------------- ")
        print(" Exécution de la méthode 3")
        print("...")
        Execute_method_JupiterSaturn_conjunction()
        print(" Un fichier 'Jupiter_Saturn_conjunction.txt' contenant les résultats de cette méthode se trouve à votre disposition. ")
        print(" Fin d'exécution de la méthode 3.")
        print(" ------------------------------------------- ")
        print(" Merci d'avoir utilisé l'outil")
    else:
        print(" Essayez encore. Un faux numéro a été renseigné")