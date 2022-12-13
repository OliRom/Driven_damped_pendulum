Diagramme de bifurcation:
    Paramètres:
        Commencer la diagramme de bifurcation à ???s (25?)
        teta = -pi/2
        omega = 0
        temps = np.arange(0, 1000.0005, 0.005)
        gamma = np.linspace(1.06, 1.087, 200)
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
