from source.robo import robo

if __name__ == "__main__":
    robo_corrida = robo.Robo()
    try:
        robo_corrida.corrida()
    except KeyboardInterrupt:
        print(" CTRL+C detectado. O loop foi interrompido.")
        robo.estado.trocar_estado("PARAR")