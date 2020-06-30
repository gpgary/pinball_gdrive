
from __future__ import print_function
import httplib2
import os, io , shutil
from pynput.keyboard import Controller

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
import auth
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
# control keyboard press ctrl+w to close browser tab
keyboard = Controller()
print('Start close tab')
with keyboard.pressed(keyboard._Key.ctrl):
    keyboard.press('w')
keyboard.release(keyboard._Key.ctrl)
keyboard.release('w')
print('End close tab')

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

    exit()


def extractFile(path):
    if not os.path.exists(pUCE_extraced_path):
        os.makedirs(pUCE_extraced_path)
    print('Extract pUCE filePath = '+ pUCE_extraced_path + ' fileName = ' + os.path.splitext(path)[0])
    unsquashfs_command = 'C:\\GDrive_download\\unsquashfs\\unsquashfs.exe -f -d ' + pUCE_extraced_path + os.path.splitext(path)[0] + ' ' + pUCE_download_path + os.path.basename(path)
    print(unsquashfs_command)
    os.system(unsquashfs_command)
    #check extract pUCE file success
    if not os.path.exists(pUCE_extraced_path+os.path.splitext(path)[0]):
        print(os.path.basename(path)+' extract fail !!!')
    else:
        moveFile(os.path.splitext(path)[0])


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
    
searchFile(10,"name contains '.pUCE'")