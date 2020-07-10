
from __future__ import print_function
import httplib2
import os, io , shutil ,sys
from pynput.keyboard import Controller
import auth
import pyglet
import threading
import multiprocessing
import time
import tkinter as tk
import tkinter.font as tkFont
#import tkinter.messagebox
import hashlib
import math

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from apiclient.http import MediaFileUpload, MediaIoBaseDownload
try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

#import tk_test
# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/drive-python-quickstart.json
# SCOPES = 'https://www.googleapis.com/auth/drive'
SCOPES = 'https://www.googleapis.com/auth/drive.readonly'
CLIENT_SECRET_FILE = 'C:\\GDrive_download\\client_secret.json'
APPLICATION_NAME = 'Drive API Python Quickstart'
pUCE_download_path = 'C:\\GDrive_download\\download\\'
pUCE_extraced_path = 'C:\\GDrive_download\\extracted\\'

authInst = auth.auth(SCOPES,CLIENT_SECRET_FILE,APPLICATION_NAME)
credentials = authInst.getCredentials()

http = credentials.authorize(httplib2.Http())
drive_service = discovery.build('drive', 'v3', http=http)
os.system('taskkill /F /IM chrome.exe')
print('Authonticated !!!!!!')


def listFiles(size):
    results = drive_service.files().list(
        pageSize=size,fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])
    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            print('{0} ({1})'.format(item['name'], item['id']))


def downloadFile(file_id,filepath):    
    if not os.path.exists(pUCE_download_path):
        os.makedirs(pUCE_download_path)

    print('download target '+file_id+' filepath '+filepath)
    request = drive_service.files().get_media(fileId=file_id)    
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print("Download %d%%." % int(status.progress() * 100))        
        with io.open(filepath,'wb') as f:
            fh.seek(0)
            f.write(fh.read())                    


def searchFile(size,query):    
    name = ''
    fieldId = ''
    results = drive_service.files().list(
    pageSize=size,fields="nextPageToken, files(id, name, kind, mimeType)",q=query).execute()
    items = results.get('files', [])    
    if not items:
        print('No files found.')
    else:
        print('Files:')        
        for item in items:
            print(item)
            print('{0} ({1})'.format(item['name'], item['id']))
            downloadFile(item['id'],pUCE_download_path+item['name'])
            print('End downlaod '+item['name']+' !!')
            extractFile(item['name'])

    print('End download google drive files')        


def extractFile(path):    
    print('Start extract file : '+ path)    
    if not os.path.exists(pUCE_extraced_path):
        os.makedirs(pUCE_extraced_path)

    # extract .pUCE file
    if ".pUCE" in path:        
        print('Extract pUCE filePath = '+ pUCE_extraced_path + ' fileName = ' + os.path.splitext(path)[0])        
        unsquashfs_command = 'C:\\GDrive_download\\unsquashfs\\unsquashfs.exe -f -d ' + pUCE_extraced_path + os.path.splitext(path)[0] + ' ' + pUCE_download_path + os.path.basename(path)
        print(unsquashfs_command)
        os.system(unsquashfs_command)

        #check extract pUCE file success
        if not os.path.exists(pUCE_extraced_path+os.path.splitext(path)[0]):
            print(os.path.basename(path)+' extract fail !!!')
        else:
            moveFile(os.path.splitext(path)[0])

    # extract UCE2 file
    if ".UCE2" in path:                
        UCE2_games_path = 'C:\\Games\\'
        game_hash_name = md5_hash(path)
        print ("%s %s" % (game_hash_name, path))        
        if not os.path.exists(UCE2_games_path + game_hash_name):
            os.makedirs(UCE2_games_path + game_hash_name)
    
        unsquashfs_command = 'C:\\GDrive_download\\unsquashfs\\unsquashfs.exe -f -d ' + UCE2_games_path + game_hash_name + ' ' + pUCE_download_path + path
        print(unsquashfs_command)
        os.system(unsquashfs_command)
    #move_comman = 'C:\\GDrive_download\\pUCEUnpackerNew\\'
    #os.chdir(move_comman)
    #print(os.system('dir'))
    #unpakcer_command = 'C:\\GDrive_download\\pUCEUnpackerNew\\pUCE_Unpacker.exe ' + pUCE_download_path + os.path.basename(path)
    #os.system(unpakcer_command)


def moveFile(target):
    print('Start move '+ target +' files to pinball folder')
    pinball_path = 'C:\\Visual Pinball\\'
    # move rom file
    source_files = os.listdir(pUCE_extraced_path + target+'\\rom\\')    
    for file in source_files:
        if file.endswith('.zip'):
            # shutil.move(pUCE_extraced_path + target+'\\rom\\*.zip',pinball_path+'VPinMAME\\roms\\')        
            shutil.move(os.path.join(pUCE_extraced_path + target + '\\rom\\',file), os.path.join(pinball_path + 'VPinMAME\\roms\\',file))

    source_files = os.listdir(pUCE_extraced_path + target+'\\table\\')
    for file in source_files:
        # move nv file
        if file.endswith('.nv'):            
            # shutil.move(pUCE_extraced_path + target+'\\table\\*.nv',pinball_path+'VPinMAME\\nvram\\')
            shutil.move(os.path.join(pUCE_extraced_path + target + '\\table\\',file), os.path.join(pinball_path + 'VPinMAME\\nvram\\',file))

        # move cfg file
        if file.endswith('.cfg'):            
            # shutil.move(pUCE_extraced_path + target+'\\table\\*.cfg',pinball_path+'VPinMAME\\cfg\\')
            shutil.move(os.path.join(pUCE_extraced_path + target + '\\table\\',file), os.path.join(pinball_path + 'VPinMAME\\cfg\\',file))

        # move vpx file
        if file.endswith('.vpx'):                
            # shutil.move(pUCE_extraced_path + target+'\\table\\*.vpx',pinball_path+'Tables\\')
            shutil.move(os.path.join(pUCE_extraced_path + target + '\\table\\',file), os.path.join(pinball_path + 'Tables\\',file))

    # move directb2s file
    source_files = os.listdir(pUCE_extraced_path + target+'\\backglass\\')
    for file in source_files:        
        if file.endswith('.directb2s'):            
            # shutil.move(pUCE_extraced_path + target+'\\table\\*.directb2s',pinball_path+'Tables\\')
            shutil.move(os.path.join(pUCE_extraced_path + target + '\\backglass\\',file), os.path.join(pinball_path + 'Tables\\',file))

    print('End move '+ pUCE_extraced_path + target)        


def md5_hash(fileName):
    print('Start md5 hash file : ' + pUCE_download_path + fileName)
    m = hashlib.md5()
    try:
        fd = open(pUCE_download_path + fileName,"rb")
    except IOError:
        print ("Reading file has problem:", pUCE_download_path + fileName)
        return
    x = fd.read()
    fd.close()
    m.update(x)
    return m.hexdigest().upper()


def run_download_gif():
    animation = pyglet.image.load_animation('C:\\GDrive_download\\atgames_loading.gif')
    animSprite = pyglet.sprite.Sprite(animation)
    
    display = pyglet.canvas.Display()    
    device_screen = display.get_default_screen()

    window = pyglet.window.Window(fullscreen=True, screen=device_screen)
        
    r,g,b,alpha = 0,0,0,0
    
    pyglet.gl.glClearColor(r,g,b,alpha)
    
    @window.event
    def on_draw():
        window.clear()
        animSprite.draw() 

    pyglet.app.run()
    print('end pyglet app run')
    pyglet.app.exit()     

    

def run_end_message():
    window = pyglet.window.Window(width=512, height=256)

    label = pyglet.text.Label('Google Drive Sync Completed',
        font_name = 'Arial',
        font_size = 24,
        x=30, 
        y=128,
    )    
    
    @window.event    
    def on_draw():
        window.clear()
        label.draw()  
    
    pyglet.clock.schedule_interval(run_end_message, 3.0)    
    pyglet.app.run()    

    

t = threading.Thread(target=run_download_gif)
t.start()
# download .pUCE files
searchFile(100,"name contains '.pUCE'")
# download UCE2 files
searchFile(100,"name contains '.UCE2'")
pyglet.app.exit()
# show google sync finish message box
#tkinter.messagebox.showinfo(title = 'download message', message = 'Google Drive Sync Completed !!!')

window = tk.Tk()
window.title('Message')
screen_width = math.ceil(window.winfo_screenwidth()/2) - 256
screen_height = math.ceil(window.winfo_screenheight()/2) - 64
geometry = '512x64+'+ str(screen_width) +'+'+ str(screen_height)
print('Screen : '+geometry)
# screen size
#window.geometry('512x64+548+476')
window.geometry(geometry)
window.configure(background='white')
# font
font_style = tkFont.Font(family="Arial", size=24)
label = tk.Label(window, text='Google Drive Sync Completed !!!', font=font_style)
label.pack()
window.after(3000, lambda : window.destroy())
window.mainloop()
exit()