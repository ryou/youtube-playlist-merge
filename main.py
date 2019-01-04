# coding: utf-8
import os
from libs.playlist_movie_maker import PlaylistMovieMaker

def mkdir_if_not_exist(directory_full_path):
    if not os.path.isdir(directory_full_path):
        os.mkdir(directory_full_path)

exec_directory = os.getcwd()
data_directory_fullpath = exec_directory + '/movie_data'
mkdir_if_not_exist(data_directory_fullpath)
dest_directory = raw_input('データを配置するディレクトリ名を入力してください：')
dest_fullpath = data_directory_fullpath + '/' + dest_directory
os.mkdir(dest_fullpath)

movie_maker = PlaylistMovieMaker(dest_fullpath)
playlist_url = raw_input('ダウンロードするプレイリストのURLを入力してください：')
movie_maker.download(playlist_url)
movie_maker.convert()
movie_maker.concat()
