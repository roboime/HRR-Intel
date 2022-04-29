

if __name__ == "__main__":
    robo_corrida = Robo(Estado(), Imu(), None, Visao())
    robo_corrida.corrida()