import os
import time
import smtplib
from selenium import *
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import sys
import pytube
from simple_youtube_api.Channel import Channel
from simple_youtube_api.LocalVideo import LocalVideo

##CONFIGURANDO JANELA##
servico = Service(ChromeDriverManager().install())
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
# chrome_options.add_argument("--window-size=1920,1080")

##link:  https://www.youtube.com/watch?v=FmrasWVUvC0&list=PLLT61SHdeQXuxTYMoLSTrT0kRCChHpc0W   ##

##ENTRANDO NO LINK E PEGANDO DADOS###
while True:
    link = input("Cole o link do vídeo:\n")
    if link != None:
        link = link
        break

#EXTRAIR TITULO E DESCRIÇÃO#
janela = webdriver.Chrome(service=servico, options=chrome_options)
janela.get('{}'.format(link))
time.sleep(2)
titulo = janela.find_element('xpath', '//*[@id="title"]/h1/yt-formatted-string')
time.sleep(2)
janela.find_element('xpath', '//*[@id="expand"]').click()
time.sleep(2)
descricao = janela.find_element('xpath', '//*[@id="description-inline-expander"]')
descricao = descricao.text
titulomais = ("Copia python")
titulo = titulo.text + titulomais

janela.close()

##BAIXAR VIDEO##
yt = pytube.YouTube(link)
yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download(filename='video.mp4')

channel = Channel()
channel.login("client_server.json", "credentials.storage")

# setting up the video that is going to be uploaded
video = LocalVideo(file_path="video.mp4")

# setting snippet
video.set_title(titulo)
video.set_description(descricao)
video.set_tags(["this", "tag"])
video.set_category("education")
video.set_default_language("pt-BR")

# setting status
video.set_embeddable(True)
video.set_license("creativeCommon")
video.set_privacy_status("public")
video.set_public_stats_viewable(True)

# setting thumbnail
#video.set_thumbnail_path("test_thumb.png")
video.set_playlist("PLDjcYN-DQyqTeSzCg-54m4stTVyQaJrGi")

channel.add_video_to_playlist

# uploading video and printing the results
video = channel.upload_video(video)
print(video)

# liking video
video.like()






