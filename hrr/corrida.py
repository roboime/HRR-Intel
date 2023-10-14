from robo import FactoryRobo

def main(self):
    factory = FactoryRobo()
    print(factory)
    robo = factory.make_robo()
    try:
        self.robo.corrida()
    except KeyboardInterrupt:
        print(" CTRL+C detectado. O loop foi interrompido.")
        serial = factory.serial()
        while(1):
            serial.parar()
        
if __name__ == "__main__":
    main()
        

