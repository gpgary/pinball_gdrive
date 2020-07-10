import pyglet
import time
import threading   


############################### gif animation #################################
def run_download_gif(status):
    print('In run_download_gif function')
    #p = subprocess.Popen(run_end_message())
    animation = pyglet.image.load_animation('C:\\GDrive_download\\atgames_loading.gif')
    animSprite = pyglet.sprite.Sprite(animation)        
    
    #window = pyglet.window.Window(width=w, height=h)
    display = pyglet.canvas.Display()    
    device_screen = display.get_default_screen()
    screen_width = device_screen.width
    #print('Your resolution width = ' + screen_width)
    screen_height = device_screen.height
    #print('Your resolution height = ' + screen_height)
    #window = pyglet.window.Window(width=800, height=600)
    #window = pyglet.window.Window(width=screen_width, height=screen_height)
    window = pyglet.window.Window(fullscreen=True, screen=device_screen)

    label = pyglet.text.Label('Google Drive Synchronizing',
        font_name = 'Arial',
        font_size = 24,
        #x=200, 
        #y=560,
        anchor_x = 'center', 
        anchor_y = 'top'
    )
    
    r,g,b,alpha = 0,0,0,0
    
    pyglet.gl.glClearColor(r,g,b,alpha)
    
    @window.event
    def on_draw():
        window.clear()        
        label.draw()
        animSprite.draw() 

    @window.event
    def on_close():
        print('close window !!!!')
                   
    if status == 'start':
        print('start loading page')
        pyglet.app.run()                        
    else:
        print('end loading page')
        on_close()


def run_end_message():
    print('run end message')
    end_window = pyglet.window.Window(width=512, height=256)

    label = pyglet.text.Label('Google Drive Sync Completed',
        font_name = 'Arial',
        font_size = 24,
        x=30, 
        y=128,
        #anchor_x = 'center', 
        #anchor_y = 'top'
    )    

    @end_window.event
    def on_draw():
        #end_window.clear()
        label.draw()        

    pyglet.clock.schedule_interval(run_end_message, 3.0)
    pyglet.app.run()


def main_process():
    for i in range(5):
        print("Main thread:", i)
        time.sleep(1)        
        


if __name__ == '__main__':

    t_loading_page = threading.Thread(target=run_download_gif,args=('start',))
    #t_loading_page = threading.Thread(target=main_process)
    t_loading_page.start()
    #run_download_gif('start')

    main_process()
    print('End main process')
    #t_loading_page = threading.Thread(target=run_download_gif,args=('stop',))
    #t_loading_page.start()
    #pyglet.app.exit()
    run_download_gif('stop')
    print('End loading page')
    #t_loading_page = threading.Thread(target=run_end_message)
    #t_loading_page.start() 
    run_end_message()
    #pyglet.app.exit()
    exit()
    