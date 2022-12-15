Diagramme de bifurcation:
    Paramètres:
        Commencer la diagramme de bifurcation à 25s

        teta = -pi/2
        omega = 0
        temps = np.arange(0, 100.0005, 0.005)
        gamma = np.linspace(1.06, 1.087, 2000)
        driving_ang_freq = 2pi
        driving_delta = 0
        g = 9.8
        l = g/(9 pi**2)
        m = 1
        damping = m * sqrt(g/l) / 2

    Paramètres:
        Commencer le diagramme de bifurcation à 20s.

        teta = -pi/2
        omega = 0
        temps = np.arange(0, 100.0005, 0.005)
        gamma = np.linspace(1.06, 1.53, 10000)
        driving_ang_freq = 2pi
        driving_delta = 0
        g = 9.8
        l = g/(9 pi**2)
        m = 1
        damping = m * sqrt(g/l) / 2


fft VS gamma:
    Paramètres:
        variable = [of.round_to_precision(gam, 8) for gam in np.linspace(1.06, 1.53, 10000)]
        variable = [variable[i*10] for i in range(1000)]
        variable_name = "gamma"
        ajout_dans_le_titre = "l'amplitude de la force externe"
        y_label = r"$\gamma$"
        temps = [of.round_to_precision(t, 8) for t in np.arange(0, 100.0005, 0.005)]
