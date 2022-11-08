import os
from pytube import YouTube
from pytube.cli import on_progress
from pytube import Playlist
from moviepy.editor import * 

def get_video(yt):
    stream = yt.streams.filter(file_extension='mp4', progressive=True, type='video')
    video = stream.get_highest_resolution()
    return video

def converte(video):
    nome = video.title
    if(nome.find("'") != -1):
        nome = nome.replace("'", "")
    
    if(nome.find("/") != -1):
        nome = nome.replace("/", "")
    
    if(nome.find("?") != -1):
        nome = nome.replace("?", "")

    if(nome.find(":") != -1):
        nome = nome.replace(":", "")

    if(nome.find(".") != -1):
        nome = nome.replace(".", "")
        
    if(nome.find(",") != -1):
        nome = nome.replace(",", "")
        

    if(os.path.exists('/home/felipe/YTDownloader/' + nome + '.mp4')):
        videoclip = VideoFileClip('/home/felipe/YTDownloader/' + nome + '.mp4')
        audioclip = videoclip.audio
        audioclip.write_audiofile('/home/felipe/YTDownloader/' + nome + '.mp3')
        videoclip.close()
        audioclip.close()
        os.remove('/home/felipe/YTDownloader/' + nome + '.mp4')
    
    else:
        print(nome, ' : arquivo não encontrado.')


while(True):
    url = input('Link do vídeo: ')
    
    if(url == 'close'):
        quit()
    
    controle = int(input('Formato (Áudio[1] Vídeo[2]): '))

    if(url.find('/playlist') != -1 or url.find('&list') != -1):
        pl = Playlist(url)
        print('Playlist: s')
        
        for i in pl.videos:
            i.register_on_progress_callback(on_progress)
            i = get_video(i)
            i.download('/home/felipe/YTDownloader')

            if(controle == 1):
                converte(i)



    else:
        yt = YouTube(url, on_progress_callback=on_progress)
        print(yt.title)
        print("Playlist: n")

        video = get_video(yt)
        video.download('/home/felipe/YTDownloader')

        if(controle == 1):
            converte(video)

    print('\n')
        





