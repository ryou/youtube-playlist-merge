# coding: utf-8
import os
import subprocess

class PlaylistMovieMaker:
    def __init__(self, dest_fullpath):
        self.DOWNLOAD_DIRECTORY = 'original'
        self.CONVERT_DIRECTORY = 'conv'
        self.dest_fullpath = dest_fullpath
        self.download_directory_fullpath = self.dest_fullpath + '/' + self.DOWNLOAD_DIRECTORY
        self.convert_directory_fullpath = self.dest_fullpath + '/' + self.CONVERT_DIRECTORY
        os.mkdir(self.download_directory_fullpath)
        os.mkdir(self.convert_directory_fullpath)

    def download(self, playlist_url):
        o = self.download_directory_fullpath + '/%(playlist_index)02d.%(ext)s'
        print(o)
        result = subprocess.check_output([
            'youtube-dl',
            '-f', 'bestvideo[height<=720]+bestaudio/best[height<=720]',
            playlist_url,
            '-o', o
        ])

    def convert(self):
        download_file_list = os.listdir(self.download_directory_fullpath)

        for file in download_file_list:
            input_file_fullpath = self.download_directory_fullpath + '/' + file
            input_file_name_without_ext = os.path.splitext(file)[0]
            output_file_fullpath = self.convert_directory_fullpath + '/' + input_file_name_without_ext + '.mp4'
            result = subprocess.check_output([
                'ffmpeg',
                '-i', input_file_fullpath,
                '-r', '20',
                '-vf', 'yadif=deint=interlaced, scale=w=trunc(ih*dar/2)*2:h=trunc(ih/2)*2, setsar=1/1, scale=w=1280:h=720:force_original_aspect_ratio=1, pad=w=1280:h=720:x=(ow-iw)/2:y=(oh-ih)/2:color=#000000',
                '-pix_fmt', 'yuv420p',
                '-ab', '384k',
                '-ar', '48000',
                output_file_fullpath
            ])

    def concat(self):
        convert_file_list = os.listdir(self.convert_directory_fullpath)
        convert_file_list.sort()

        # listファイル作成
        list_fp = open(self.dest_fullpath + '/list.txt', 'w')
        for filename in convert_file_list:
            file_fullpath = self.convert_directory_fullpath + '/' + filename
            list_fp.write('file ' + file_fullpath + '\n')
        list_fp.close()

        result = subprocess.check_output([
            'ffmpeg',
            '-f', 'concat',
            '-safe', '0',
            '-i', self.dest_fullpath + '/list.txt',
            '-c', 'copy',
            self.dest_fullpath + '/merge.mp4'
        ])
