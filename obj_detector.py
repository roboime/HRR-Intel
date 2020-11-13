def obj_detector(img): #Argumento imagem #Retorno o ponto médio da linha mais baixa(xmed,ymed)
    image=cv2.imread(img)
    
    #HLS filtro
    lower=np.array([0,0,0])
    upper=np.array([30,255,255])
    
    #A placa nos envia a imagem rotacionada, vamos então aqui rotacionar a imagem usando o centro como origem:
    (alt, lar) = image.shape[:2] #captura altura e largura
    centro = (lar // 2, alt // 2) #acha o centro
    
    M = cv2.getRotationMatrix2D(centro, 180, 1.0) #Gerar matriz de rotação
    image = cv2.warpAffine(image, M, (lar, alt)) #Comando para rotacionar
    
    image1 = cv2.blur(image, (7, 7)) #Suavizar a imagem utilizando blur
    
    hls = cv2.cvtColor(image1, cv2.COLOR_BGR2HLS) #Converter o COLORSPACE
    orangemask=cv2.inRange(hls, lower,upper) #Criação da mascara para objetos laranja
    
    edges=cv2.Canny(orangemask,100,240,apertureSize=3) #Usamos o canny para pegar os contornos

    #cv2.imwrite('edges'+str(n+1)+".jpeg",edges)
    #cv2.imwrite('mask'+str(n+1)+".jpeg",orangemask)
    
    minLineLength=130 #Parametro da HoughLines
    
    #Utlizar HoughLinesP para retornar x1 y1 x2 y2
    lines = cv2.HoughLinesP(edges,rho=1,theta=np.pi/180, threshold=100,lines=np.array([]), minLineLength=minLineLength,maxLineGap=20)
    
    #a = número de linhas (matriz)
    #b = número de linhas da lista 
    #c = 4, pois é a DIM
    
    a,b,c = lines.shape
    
    # A padronização dos eixos no OpenCV é o eixo y para baixo, portanto ymax=-1 da sempre valores maiores que os medidos
    ymax1=-1 
    ymax2=-1
    k1=10000 #Os k são variaveis temporarias para associar aos pontos 
    k2=10000
    print('atenção!!!')
    for i in range(a): #Loop para achar a reta com y máximo
        if lines[i][0][1]>ymax1:
            ymax1=lines[i][0][1]
            k1=i
        if lines[i][0][3]>ymax2:
            ymax2=lines[i][0][3]
            k2=i
    medy=(ymax1+ymax2)/2 #Ponto médio em y
    medx=(lines[k1][0][0]+lines[k2][0][2])/2 #Ponto médio em x
        


    #for i in range(a):

        #ang=(180/np.pi)*np.arctan((lines[i][0][3]-lines[i][0][1])/(lines[i][0][2]-lines[i][0][0]))
        #print(ang)
        #if abs(ang)<20:
            #cv2.line(image, (lines[i][0][0], lines[i][0][1]), (lines[i][0][2], lines[i][0][3]), (0, 0, 255), 3, cv2.LINE_AA)
        #cv2.imwrite('teste'+".jpeg",image)
        
    return medx, medy
