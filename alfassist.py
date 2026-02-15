import cv2
import threading
import time
from ultralytics import YOLO
import vlc
import mediapipe as mp
import numpy as np

global mutex
mutex = threading.Lock()
detectou= 0
center_rosto=0
confi_feliz=0
confi_triste=0
detectou_exp=0
confidence=0
center_rosto_ant=0
lado=0
calibra_posicao=0
# Inicializar o MediaPipe Selfie Segmentation
mp_selfie_segmentation = mp.solutions.selfie_segmentation.SelfieSegmentation(model_selection=1)

# Caminho do arquivo de vídeo
video_path = "alfassist.mp4"
# Cria uma instância do player
player = vlc.MediaPlayer(video_path)
# Load the YOLOv8 model
model = YOLO("best.pt")
cap = cv2.VideoCapture(0)

# Inicia a reprodução
player.play()
player.set_time(100)
time.sleep(0.2)  # Aqui, o tempo é ajustado conforme o vídeo
player.pause()


# Definindo a primeira task
def task1():
    global center_rosto,detectou_exp,center_rosto_ant, lado, calibra_posicao
    while True:
        if detectou_exp == 3: # EXPRESSÃO DE FELICIDADE
            while lado == 0:
                # Define o tempo inicial
                player.set_time(21000)
                time.sleep(0.2)
                #print("Selecione:")
                if center_rosto > center_rosto_ant + 20 and calibra_posicao == 1:
                    #print("Virou pra esquerda")
                    lado = 2
                if center_rosto < center_rosto_ant - 20 and calibra_posicao == 1:
                    #print("Virou pra direita")
                    lado = 1
                center_rosto_ant = center_rosto
                calibra_posicao = 1
            time.sleep(0.1)
            detectou_exp=0
            if (lado == 2):
                calibra_posicao = 0
                player.set_time(26000)
                time.sleep(3)
            if (lado == 1):
                calibra_posicao = 0
                player.set_time(31000)
                time.sleep(3)            
            lado=0

        elif detectou_exp == 4: # EXPRESSÃO DE DOR
            while lado == 0:
                # Define o tempo inicial
                player.set_time(36000)
                time.sleep(0.2)
                #print("Selecione:")
                if center_rosto > center_rosto_ant + 20 and calibra_posicao == 1:
                    #print("Virou pra esquerda")
                    lado = 2
                if center_rosto < center_rosto_ant - 20 and calibra_posicao == 1:
                    #print("Virou pra direita")
                    lado = 1
                center_rosto_ant = center_rosto
                calibra_posicao = 1
            time.sleep(0.1)
            detectou_exp=0
            if (lado == 2):
                calibra_posicao = 0
                player.set_time(41000)
                time.sleep(3)
            if (lado == 1):
                calibra_posicao = 0
                player.set_time(46000)
                time.sleep(3)            
            lado=0

        elif detectou_exp == 1: # EXPRESSÃO DE TRISTESA
            while lado == 0:
                # Define o tempo inicial
                player.set_time(8000)
                time.sleep(0.2)
                #print("Selecione:")
                if center_rosto > center_rosto_ant + 20 and calibra_posicao == 1:
                    #print("Virou pra esquerda")
                    lado = 2
                if center_rosto < center_rosto_ant - 20 and calibra_posicao == 1:
                    #print("Virou pra direita")
                    lado = 1
                center_rosto_ant = center_rosto
                calibra_posicao = 1
            time.sleep(0.1)
            detectou_exp=0
            if (lado == 2):
                calibra_posicao = 0
                player.set_time(11000)
                time.sleep(3)
            if (lado == 1):
                calibra_posicao = 0
                player.set_time(17000)
                time.sleep(3)            
            lado=0
        else:
            player.set_time(0)
            time.sleep(0.2)


t1 = threading.Thread(target=task1)
# Iniciando as threads
t1.start()

while True:
    # Read a frame from the video
    success, frame = cap.read()
    if success:
        # Criar um fundo branco do mesmo tamanho do frame da webcam
        background_white = np.ones(frame.shape, dtype=np.uint8) * 255  # Fundo branco
        # Converter a imagem BGR para RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # Aplicar segmentação de selfie (detectar a pessoa)
        results = mp_selfie_segmentation.process(frame_rgb)
        # Obter a máscara de segmentação
        mask = results.segmentation_mask
        condition = mask > 0.5  # Definir um limiar para a máscara (ajustar conforme necessário)
        # Criar a imagem final com o fundo branco
        output_image = np.where(condition[..., None], frame, background_white)
        # Run YOLOv8 tracking on the frame, persisting tracks between frames
        results = model.predict(output_image,conf=0.60,verbose= False)
        # Lista para armazenar classes e seus boxes
        detected_objects = []
        # Verificar se há boxes detectados
        if len(results[0].boxes) == 0:  # Se não houver boxes
            with mutex:  # Bloquear o mutex para alterar a variável com segurança
                detectou_exp = 0
                lado=0
        else:
            for result in results[0].boxes:
                cls = int(result.cls)  # Classe do objeto
                x1, y1, x2, y2 = result.xyxy[0].tolist()  # Coordenadas da caixa delimitadora
                confidence = float(result.conf)  # Confiança da detecção (probabilidade)                    
                detected_objects.append({'class': cls,'box': (x1, y1, x2, y2),'confidence': confidence})  # Adiciona a confiança ao dicionário     
                # Exemplo de acesso às classes, coordenadas e probabilidades
                for obj in detected_objects:
                    cls = obj['class']
                    x1, y1, x2, y2 = obj['box']
                    confidence = obj['confidence']
                    center_x = (x1 + x2) / 2   
                    #print(f"Classe: {cls}")    
                    # FELIZ = 1
                    # TRISTE = 4
                    # ROSTO = 3
                    # INDIFERENCA = 2 
                    if cls == 3: # ROSTO
                        with mutex:
                            center_rosto = center_x
                    elif cls == 1 :              # FELICIDADE
                        confi_feliz = confidence
                        with mutex:                            
                            detectou_exp = 3
                    elif cls==4:                 # TRISTEZA 
                        confi_triste = confidence
                        with mutex:
                            detectou_exp = 1
                    elif cls==2:                # INDIFERENÇA
                        with mutex:
                            detectou_exp = 2
                    elif cls==0:                # INDIFERENÇA
                        with mutex:
                            detectou_exp = 4
        # Visualize the results on the frame
        annotated_frame = results[0].plot()
        # Criar uma janela com um nome, aqui "ALFASSIST"
        cv2.namedWindow("ALFASSIST", cv2.WINDOW_NORMAL)
        # Definir a resolução da janela (por exemplo, 800x600 pixels)
        #cv2.resizeWindow("ALFASSIST", 640, 480)
        cv2.resizeWindow("ALFASSIST", 320, 320)
        # Exibir o frame na janela
        cv2.imshow("ALFASSIST", annotated_frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        # Break the loop if the end of the video is reached
        break
# Release the video capture object and close the display window
cap.release()
cv2.destroyAllWindows()
