from root.source import robo

if __name__ == "__main__":
    robo_obstaculo = robo.Robo(robo.Estado(), robo.Imu(), robo.SensorDistancia, robo.Visao())
    try:
        robo_obstaculo.corrida_obstaculo()
    except KeyboardInterrupt:
        print(" CTRL+C detectado. O loop foi interrompido.")
        robo.estado.trocar_estado("PARAR")