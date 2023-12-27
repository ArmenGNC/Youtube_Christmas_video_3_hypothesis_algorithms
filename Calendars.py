
'''
    Dates en jours julien est le decimal
    Dates en calendrier julien est A,M,D,H,Mi,S

    The value JJ is given by kepler.DJ(year,month,day,hour,minute,second)

'''

# Additional functions
def MoledA_calculation(A):

    ''' This function aims to calculate the MoledA parameter. '''

    MoledA = 347605 + (3444371 / 4924800) + A * (365 + 24311 / 98496) + ((12 * A + 5) % 19) * (1 + 272953 / 492480)

    return MoledA

def alpha_Ea_Fa_calculation(A,MoledA):

    # Caclculation of the julian day of Roch Hachana for year A
    alpha = (12*A + 5)%19

    # Calculation of Ea
    Ea = int(MoledA)
    Fa = MoledA - int(MoledA)

    return alpha, Ea, Fa

def Rha_calculation(alpha,Ea,Fa):

    # Calculation of RHa
    if Ea%7 == 1 or Ea%7 == 3 or Ea%7 == 5:
        Rha = Ea + 2
    elif Ea%7 == 0 and alpha >=7 and Fa>= 311676/492480:
        Rha = Ea + 3
    elif Ea%7 == 6 and alpha>=12 and Fa>= 442111/492480:
        Rha = Ea + 2
    else:
        Rha = Ea + 1

    return Rha

def Determination_of_intermediate_constants(L):

    ''' This functions aims to choose constants relative to L value. '''

    if L == 353:
        m0 = 4
        d = 88
        r = 5
        Z = 324
        W = 11
    elif L == 354:
        m0 = 7
        d = 177
        r = 5
        Z = 325
        W = 11
    elif L == 355:
        m0 = 3
        d = 60
        r = 5
        Z = 325
        W = 11
    elif L == 383:
        m0 = 4
        d = 88
        r = 4
        Z = 325
        W = 11
    elif L == 384:
        m0 = 8
        d = 207
        r = 5
        Z = 325
        W = 11
    elif L == 385:
        m0 = 3
        d = 60
        r = 7
        Z = 266
        W = 9

    return m0,d,r,Z,W

def From_decimal_to_hms(decimal_day):

    ''' The goal of this function is to convert a decimal time to its respective hour, minute and second '''
    # Determining the day
    day = int(decimal_day)

    # Determining the hour
    hour_decimal = 24*(decimal_day - int(decimal_day))
    hour = int(hour_decimal)

    # Determining the minute
    minute_decimal = 60*(hour_decimal - int(hour_decimal))
    minute = int(minute_decimal)

    # Determining the second
    second_decimal = 60*(minute_decimal - int(minute_decimal))
    second = int(minute_decimal)


    return day,hour,minute,second

# Gregorian calendar
def From_gregorian_calendar_to_julian_days(YY,MM,DD):

    ''' To get the right use of the calendar conversion function. The algorithm used has been retrieved from this
         website : http://lwh.free.fr/pages/algo/calendriers/calendrier_gregorien.htm

        This calendar starts from January 1st -4712 12:00:00

         This function aims to convert from a gregorian calendar to a julian day.

         Inputs :
         A : year
         M : month
         D : day

         '''

    if MM > 2:
        y = YY
        m = MM
    elif MM ==1 or MM ==2:
        y = YY-1
        m = MM + 12
    else:
        pass

    B = 0

    if YY >1582 and MM >10 and DD>15:
        A = int(y/100)
        B = 2 - A + int(A/4)

    else:
        pass

    # Calculation of JJ
    JJ = int(365.25*y) + int(30.6001*(m+1)) + DD+1720994.5 + B


    # # For Q (quantième)
    # Q = int(275*m / 9) - 2 * int(MM + 9) / 12 + DD - 30 # ordinary days
    # Q = int(275*m / 9) - int(MM + 9) / 12 + DD - 30 # for leap years

    return JJ, y, m, DD

def From_julian_days_to_gregorian_calendar(JJ):

    '''

    The goal of this function is to convert a julian date to a gregorian date
    Some indication on Wikipedia's website (https://fr.wikipedia.org/wiki/Jour_julien) :

    Inputs :
    JJ is the decimal part

    '''

    # Partie JJ
    Z = int(JJ)
    F = JJ - int(JJ)

    if Z <  2299161:
        S = Z
    elif Z >=  2299161:
        alpha = int((Z-1867216.25)/36524.25)
        S = Z+1+alpha - int(alpha/4)
    else:
        pass

    # Other calculation
    B = S +1524
    C = int((B-122.1)/365.25)
    D = int(365.25*C)
    E = int((B-D)/30.6001)

    # Day
    Q = B-D-int(30.6001*E) + F

    # Month number
    if E <14:
        M = E-1
    elif E == 14 or E == 15:
        M = E - 13
    else:
        pass

    # Year
    if M > 2:
        A = C - 4716
    elif M == 1 or M == 2:
        A = C - 4715
    else:
        pass

    # Determining day, hour , minute, second
    day, hour, minute, second = From_decimal_to_hms(Q)

    return A,M,int(Q), hour, minute, second

# Julian calendar
def From_julian_calendar_to_julian_days(A,M,Q):

    '''

    The goal of this function is to convert julian calendar to julian days

    Inputs :
    A : julian year
    M : julian month
    Q : julian day

    Output :
    JJ : julian days
    '''

    if M > 2:
        pass
    elif M ==1 or M ==2:
        A = A - 1
        M = M + 12
    else:
        pass

    JJ = int((1461*A + 6884472)/4) + int((153*M - 457)/5) + Q - 1

    return JJ



    return None

def From_julian_days_to_julian_calendar(JJ):

    '''

    The goal of this function is to convert a julian date to a julian calendar
    Some indication on Wikipedia's website (https://fr.wikipedia.org/wiki/Jour_julien) :

    Inputs :
    JJ is the decimal part

    '''

    # Calculation of A
    A = int((4*JJ - 6884469)/1461)

    # Calculation of R2
    R2 = JJ-int((1461*A + 6884472)/4)

    # Calculation of M
    M = int((5*R2 + 461)/153)

    # Calculation of R1
    R1 = R2 - int((153*M - 457)/5)

    # Calculation of Q
    Q = R1 + 1

    # For A and M
    if M == 13 or M ==14:
        A = A + 1
        M = M - 12
    elif M < 13:
        pass
    else:
        pass

    # Determining day, hour , minute, second
    day, hour, minute, second = From_decimal_to_hms(Q)

    return A,M,day, hour, minute, second

# Hebrew calendar
def From_hebrew_calendar_to_julian_days(A,M,Q):

    '''

    The goal of this function is to convert hebrew calendar to julian days

    Inputs :
    A : hebrew year
    M : hebrew month
    Q : hebrew day

    Output :
    JJ : julian days
    '''

    # Calculation of MoledA
    MoledA = MoledA_calculation(A)

    # alpha, Ea, Fa
    alpha, Ea, Fa = alpha_Ea_Fa_calculation(A, MoledA)

    # Calculation of Rha
    Rha = Rha_calculation(alpha,Ea,Fa)

    # Calculation of Rha+1
    A_plus_1 = A + 1
    MoledA_plus_1 = MoledA_calculation(A_plus_1)

    # alpha, Ea, Fa
    alpha_plus_1, Ea_plus_1, Fa_plus_1 = alpha_Ea_Fa_calculation(A_plus_1, MoledA_plus_1)

    # Calculation of Rha
    Rha_plus_1 = Rha_calculation(alpha_plus_1, Ea_plus_1, Fa_plus_1)

    # Calculation of L
    L = Rha_plus_1 - Rha

    # Determination of intermediate constants
    m0, d, r, Z, W = Determination_of_intermediate_constants(L)

    #
    if M >= m0:
        A_prime = 0
        M_prime = M
    else:
        A_prime = -1
        M_prime = M + int(13 + ((6-alpha)/19))

    # Calculation of JJ
    JJ = Rha + L*A_prime + d + int((Z*M_prime + r - Z*m0)/W) + Q - 1

    return JJ

def From_julian_days_to_hebrew_calendar(JJ):
    '''

    The goal of this function is to convert a julian date to a hebrew calendar
    Some indication on Wikipedia's website (https://fr.wikipedia.org/wiki/Jour_julien) :

    Inputs :
    JJ is the decimal part

    '''

    # Number of ellapsed days since the Creation
    J0 = JJ - 347997

    # Number of mean month since the Creation
    m = int(J0/(29 + (13753/25920)))

    # A
    A = int((19*m + 252)/235)

    # Roh Hachana for A year in Julian days
    MoledA = MoledA_calculation(A)

    # alpha, Ea, Fa
    alpha, Ea, Fa = alpha_Ea_Fa_calculation(A, MoledA)

    # Calculation of Rha
    Rha = Rha_calculation(alpha,Ea,Fa)

    # print(" JJ is : ", JJ)
    # print(" A : ", A)
    # print(" MoledA : ", MoledA)
    # print(" alpha : ", alpha)
    # print(" Ea : ", Ea)
    # print(" Fa : ", Fa)

    # Final calculation of the year A of the hebrew calendar
    if Rha > JJ:

        A = A-1
        # Re calculation of the parameters
        MoledA = MoledA_calculation(A)

        # alpha, Ea, Fa
        alpha, Ea, Fa = alpha_Ea_Fa_calculation(A, MoledA)

        # Calculation of Rha
        Rha = Rha_calculation(alpha, Ea, Fa)
    else:
        pass

    # Calculation of the length L of the hebrew year A
    # Calculation of Rha_plus_1
    A_plus_1 = A+1
    MoledA_plus_1 = MoledA_calculation(A_plus_1)

    # alpha, Ea, Fa
    alpha_plus_1, Ea_plus_1, Fa_plus_1 = alpha_Ea_Fa_calculation(A_plus_1, MoledA_plus_1)

    # Calculation of Rha
    Rha_plus_1 = Rha_calculation(alpha_plus_1, Ea_plus_1, Fa_plus_1)

    # Calculation of L
    L = Rha_plus_1 - Rha

    # Determination of intermediate constants
    m0, d, r, Z, W = Determination_of_intermediate_constants(L)

    # Calculation of M and Q
    JH = JJ - Rha
    A1 = int((JH-d)/L)
    R2 = JH - int(L*A1 + d)
    m1 = int((W*R2 + W + Z*m0-r-1)/Z)

    if A1 == 0:
        M = m1
    if A1 == -1:
        M = m1 - int(12 + L/360)
    else:
        pass

    # Calculation of Q
    Q = (R2 - int((Z*m1+r-Z*m0)/W)) + 1

    if int(Q):
        Q = 1
    else:
        Q = int(Q)

    return A,M, Q