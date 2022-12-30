from pytube import YouTube, Playlist
from pytube.cli import on_progress
from moviepy.editor import *
import re
import os
from enum import Enum


class Format (Enum):
    AUDIO = 1
    VIDEO = 2


PATH = '/home/felipe/Música/'
SPECIAL_CHARACTERS = "['/\?:.,!~@$%]"


def main():
    while (True):
        video_url = input('URL do vídeo: ')
        format = int(input('Formato (áudio[1] vídeo[2]): '))

        if is_playlist(video_url):
            print('Playlist: Sim')
            youtube_playlist = Playlist(video_url)
            playlist_process(youtube_playlist, format)

        else:
            print('Playlist: Não')
            youtube_video = YouTube(
                video_url, on_progress_callback=on_progress)
            single_file_process(youtube_video, format)

        print('\n')


def is_playlist(video_url):
    if '/playlist' in video_url or '&list' in video_url:
        return True

    return False


def playlist_process(youtube_playlist, format):
    print(youtube_playlist)
    for youtube_video in youtube_playlist.videos:
        youtube_video.register_on_progress_callback(on_progress)
        single_file_process(youtube_video, format)


def single_file_process(youtube_video, format):
    print(f'Título do vídeo: {youtube_video.title}')
    mp4_video = get_mp4_video_from_youtube_video(youtube_video)
    mp4_video.download(PATH)

    if format == Format.AUDIO.value:
        convert_mp4_in_mp3(mp4_video)


def get_mp4_video_from_youtube_video(youtube_video):
    print('Getting streams ...')
    youtube_streams = youtube_video.streams.filter(
        file_extension='mp4', progressive=True, type='video')
    mp4_video = youtube_streams.get_highest_resolution()

    return mp4_video


def convert_mp4_in_mp3(mp4_video):
    print('Convertendo...')
    video_title = remove_special_characters(mp4_video.title)
    base_path = PATH + video_title
    video_file_path = base_path + '.mp4'
    audio_file_path = base_path + '.mp3'

    if os.path.exists(video_file_path):
        video_file_clip = VideoFileClip(video_file_path)
        audio_clip = video_file_clip.audio
        audio_clip.write_audiofile(audio_file_path)

        video_file_clip.close()
        audio_clip.close()
        os.remove(video_file_path)

        return

    print(f'Arquivo {video_file_path} não encontrado')


def remove_special_characters(string):
    return re.sub(SPECIAL_CHARACTERS, "", string)


if __name__ == '__main__':
    main()
