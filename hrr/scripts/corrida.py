from ..hrr import estado, imu, robo, visao

if __name__ == "__main__":
    robo_corrida = robo.Robo(estado = estado.Estado(),
        imu = imu.Imu(),
        visao = visao.Visao(),
        alinhamento= robo.Alinhamento_imu)
    try:
        robo_corrida.corrida()
    except KeyboardInterrupt:
        print(" CTRL+C detectado. O loop foi interrompido.")
        robo.estado.trocar_estado("PARAR")
        