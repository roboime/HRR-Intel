from root.source import robo

if __name__ == "__main__":
    robo_degrau = robo.Robo(robo.Estado(), robo.Imu(), None, robo.Visao())
    try:
        robo_degrau.corrida_degrau()
    except KeyboardInterrupt:
        print(" CTRL+C detectado. O loop foi interrompido.")
        robo.estado.trocar_estado(PARAR)