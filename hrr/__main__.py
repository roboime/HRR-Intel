from hrr.robo import Robo

def main(self):
    robo = Robo().compile()
    try:
        input("Pressione ENTER para iniciar a corrida ")
        robo.corrida()
    except KeyboardInterrupt:
        print(" CTRL+C detectado. O loop foi interrompido.")
        serial = robo.serial()
        while(1):
            serial.parar()
        
if __name__ == "__main__":
    main()
        

