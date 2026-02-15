import vlc
import time

# Caminho do arquivo de vídeo
video_path = "alfassist2.mp4"

# Cria uma instância do player
player = vlc.MediaPlayer(video_path)

# Inicia a reprodução
player.play()
# Mantém o player rodando enquanto o vídeo toca
time.sleep(0.2)  # Aqui, o tempo é ajustado conforme o vídeo
player.pause()
player.set_time(46000) # Tela feliz opção esquerda
time.sleep(0.2)

while True:
    # Define o tempo inicial
    #player.set_time(100) # Tela inicial
    #player.set_time(8000) # Tela triste opções passear ou comer 
    #player.set_time(11000) # Tela triste opção esquerda
    #player.set_time(17000) # Tela triste opção direita

    # player.set_time(21000) # Tela feliz opções olhar tv ou brincar
    #player.set_time(26000) # Tela feliz opção esquerda
    #player.set_time(31000) # Tela feliz opção direita

    #player.set_time(36000) # Tela dor opções dor de barriga e dor de dente
    #player.set_time(41000) # Tela dor opção esquerda
    #player.set_time(46000) # Tela dor opção direita
    time.sleep(0.2)

