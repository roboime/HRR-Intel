from source import robo

if __name__ == "__main__":
    robo_corrida = robo.Robo(estado = robo.Estado(), imu = robo.Imu(), visao = robo.Visao())
    try:
        robo_corrida.corrida()
    except KeyboardInterrupt:
        print(" CTRL+C detectado. O loop foi interrompido.")
        robo.estado.trocar_estado("PARAR")