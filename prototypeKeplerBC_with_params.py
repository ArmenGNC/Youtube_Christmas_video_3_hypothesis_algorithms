import numpy
import re
import numpy as np

class Solar_System:
    def __init__(self):
        self.epsilon = 1e-6
        f = open("elemntsPlanetesBC.txt", "r")
        self.a = {}
        self.e = {}
        self.I = {}
        self.L = {}
        self.Lperi = {}
        self.Lnode = {}
        self.da = {}
        self.de = {}
        self.dI = {}
        self.dL = {}
        self.dLperi = {}
        self.dLnode = {}
        lines = f.readlines()
        n = 3
        for p in range(9):
            ligne1 = re.split("[\s]+", lines[n])
            ligne2 = re.split("[\s]+", lines[n + 1])
            n += 2
            nom = ligne1[0]
            self.a[nom] = float(ligne1[1])
            self.e[nom] = float(ligne1[2])
            self.I[nom] = float(ligne1[3])
            self.L[nom] = float(ligne1[4])
            self.Lperi[nom] = float(ligne1[5])
            self.Lnode[nom] = float(ligne1[6])
            self.da[nom] = float(ligne2[1])
            self.de[nom] = float(ligne2[2])
            self.dI[nom] = float(ligne2[3])
            self.dL[nom] = float(ligne2[4])
            self.dLperi[nom] = float(ligne2[5])
            self.dLnode[nom] = float(ligne2[6])

        f.close()
        self.lettre = {'Mercury': 'M', 'Venus': 'V', 'Earth': 'T', 'Mars': 'Ma', 'Jupiter': 'J', 'Saturn': 'S',
                       'Uranus': 'U', 'Neptune': 'N', 'Pluto': 'P'}
        self.deg2rad = numpy.pi / 180
        self.rad2deg = 180 / numpy.pi

        self.masse = {}
        self.masse["Mercury"] = 1.0 / 6023600.0
        self.masse["Venus"] = 1.0 / 408523.5
        self.masse["Earth"] = 1.0 / 328900.5
        self.masse["Mars"] = 1.0 / 3098710.0
        self.masse["Jupiter"] = 1.0 / 1047.355
        self.masse["Saturn"] = 1.0 / 3498.5
        self.masse["Uranus"] = 1.0 / 22869.0
        self.masse["Neptune"] = 1.0 / 19314.0
        k = 0.01720209895  # constante de Gauss
        self.k2 = k * k

        # cometes
        self.comete_dj = {}
        self.comete_Yi = {}
        self.comete_e = {}
        self.comete_nom = {}
        self.retrieve_comete_code = []     # To have all comets' code
        f = open("ELTNOM.txt", "r")
        # g = open("cometes.txt","w")
        lines = f.readlines()
        for n in range(0, len(lines), 9):
            ligne1 = re.split("[\s]+", lines[n])
            ligne2 = re.split("[\s]+", lines[n + 1])
            ligne3 = re.split("[\s]+", lines[n + 2])
            ligne4 = re.split("[\s]+", lines[n + 3])
            ligne6 = re.split("[\s]+", lines[n + 5])
            code = lines[n][17:25]
            code = code.replace(" ", "")
            self.retrieve_comete_code.append(code)
            dj = float(ligne2[0])
            self.comete_dj[code] = dj
            self.comete_Yi[code] = [float(ligne3[0]), float(ligne3[1]), float(ligne3[2]), float(ligne4[0]),
                                    float(ligne4[1]), float(ligne4[2])]
            nom = lines[n][27:56]
            nom = nom.replace(" ", "")
            e = float(ligne6[2])
            self.comete_nom[code] = nom
            self.comete_e[code] = e
            # g.write("%s\t%s\t DJ=%0.1f\t e=%0.3f\n"%(code,nom,dj,e))
        # g.close()
        f.close()

        # Additionnal parameters
        self.add_param_b = {}
        self.add_param_c = {}
        self.add_param_s = {}
        self.add_param_f = {}
        f = open("Add_terms_for_3000BC_3000AD.txt", "r")
        lines = f.readlines()
        nir = 2
        for n in range(9):
            ligne1 = re.split("[\s]+", lines[nir])
            nir += 1
            nom = ligne1[0]
            self.add_param_b[nom] = float(ligne1[1])
            self.add_param_c[nom] = float(ligne1[2])
            self.add_param_s[nom] = float(ligne1[3])
            self.add_param_f[nom] = float(ligne1[4])

        f.close()



    def dateJulienne(self, annee, mois, jour, heure, minute, seconde):
        if mois <= 2:
            a = annee - 1
            m = mois + 12
        else:
            a = annee
            m = mois
        b = int(a / 400) - int(a / 100)
        delta_minute = 1.9012852617588972 * 0.00000001
        delta_seconde = delta_minute / 60
        DJ = int(365.25 * a) + int(30.6001 * (
                    m + 1)) + b + 1720996.5 + jour + heure * 1.0 / 24 + delta_minute * minute + delta_seconde * seconde
        return DJ   # Julian date

    def t(self, DJ):
        return (DJ - 2451545) * 1.0 / 36525    # Time ellasped since J2000 in century

    def equationKepler(self, e, M, epsilon):
        E = M
        delta = 1e6
        while delta > epsilon:
            new_E = E - (E - e * numpy.sin(E) - M) / (1 - e * numpy.cos(E))
            delta = abs(new_E - E)
            E = new_E
        return E

    def position_xy(self, planete, t):
        L = self.L[planete] + self.dL[planete] * t
        Lperi = self.Lperi[planete] + self.dLperi[planete] * t
        M = L - Lperi + self.add_param_b[planete]*(t**2) + self.add_param_c[planete]*np.cos(self.add_param_f[planete]*t) + + self.add_param_s[planete]*np.sin(self.add_param_f[planete])
        e = self.e[planete] + self.de[planete]
        E = self.equationKepler(e, M * self.deg2rad, self.epsilon)
        a = self.a[planete] + self.da[planete] * t
        x = a * (numpy.cos(E) - e)
        y = a * numpy.sqrt(1 - e * e) * numpy.sin(E)
        return (x, y)

    def ellipse_xy(self, planete, t, N=1000):
        E = numpy.linspace(0, 2 * numpy.pi, N)
        a = self.a[planete] + self.da[planete] * t
        e = self.e[planete] + self.de[planete]
        x = a * (numpy.cos(E) - e)
        y = a * numpy.sqrt(1 - e * e) * numpy.sin(E)
        return (x, y)

    def xy_XYZ(self, planete, t, x, y):
        I = self.I[planete] + self.dI[planete] * t
        Lperi = self.Lperi[planete] + self.dLperi[planete] * t
        Omega = self.Lnode[planete] + self.dLnode[planete] * t
        I *= self.deg2rad
        Omega *= self.deg2rad
        Lperi *= self.deg2rad
        omega = Lperi - Omega
        cos_omega = numpy.cos(omega)
        sin_omega = numpy.sin(omega)
        R1 = numpy.array([[cos_omega, -sin_omega, 0], [sin_omega, cos_omega, 0], [0, 0, 1]])
        cos_I = numpy.cos(I)
        sin_I = numpy.sin(I)
        R2 = numpy.array([[1, 0, 0], [0, cos_I, -sin_I], [0, sin_I, cos_I]])
        cos_Omega = numpy.cos(Omega)
        sin_Omega = numpy.sin(Omega)
        R3 = numpy.array([[cos_Omega, -sin_Omega, 0], [sin_Omega, cos_Omega, 0], [0, 0, 1]])
        R = numpy.dot(R3, numpy.dot(R2, R1))
        xyz = numpy.array([x, y, 0])
        XYZ = numpy.dot(R, xyz)
        return XYZ

    def position_XYZ(self, planete, t):
        (x, y) = self.position_xy(planete, t)
        return self.xy_XYZ(planete, t, x, y)

    def ellipse_XYZ(self, planete, t, N=1000):
        (x, y) = self.ellipse_xy(planete, t, N)
        X = numpy.zeros(N)
        Y = numpy.zeros(N)
        Z = numpy.zeros(N)
        for k in range(N):
            XYZ = self.xy_XYZ(planete, t, x[k], y[k])
            X[k] = XYZ[0]
            Y[k] = XYZ[1]
            Z[k] = XYZ[2]
        return (X, Y, Z)

    def FramePlanet_to_FrameJ2000(self, planete, t, xyz_inertial_without_obliquity):
        #   r cartesian distance from sun to the planet
        #   t cartesian coordinates in the planet inertial (without obliquity) frame

        r = self.position_XYZ(planete, t)
        T = np.array([[1, 0, 0, r[0]], [0, 1, 0, r[1]], [0, 0, 1, r[2]], [0, 0, 0, 1]])
        xyz_heliocentric = np.array([T[0][0] * xyz_inertial_without_obliquity[0] + T[0][1] *
                                     xyz_inertial_without_obliquity[1] + T[0][2] * xyz_inertial_without_obliquity[2] +
                                     T[0][3] * 1,
                                     T[1][0] * xyz_inertial_without_obliquity[0] + T[1][1] *
                                     xyz_inertial_without_obliquity[1] + T[1][2] * xyz_inertial_without_obliquity[2] +
                                     T[1][3] * 1,
                                     T[2][0] * xyz_inertial_without_obliquity[0] + T[2][1] *
                                     xyz_inertial_without_obliquity[1] + T[2][2] * xyz_inertial_without_obliquity[2] +
                                     T[2][3] * 1,
                                     T[3][0] * xyz_inertial_without_obliquity[0] + T[3][1] *
                                     xyz_inertial_without_obliquity[1] + T[3][2] * xyz_inertial_without_obliquity[2] +
                                     T[3][3] * 1])

        return xyz_heliocentric


def systeme_comete(Y, dj, self, planetes):
    rs3 = numpy.power(Y[0] * Y[0] + Y[1] * Y[1] + Y[2] * Y[2], 1.5)
    Fx = -Y[0] / rs3
    Fy = -Y[1] / rs3
    Fz = -Y[2] / rs3
    for planete in planetes:
        pos = self.position_XYZ(planete, self.t(dj))
        x = Y[0] - pos[0]
        y = Y[1] - pos[1]
        z = Y[2] - pos[2]
        r3 = numpy.power(x * x + y * y + z * z, 1.5)
        Fx -= self.masse[planete] * x / r3
        Fy -= self.masse[planete] * y / r3
        Fz -= self.masse[planete] * z / r3
    return numpy.array([Y[3], Y[4], Y[5], Fx * self.k2, Fy * self.k2, Fz * self.k2])
