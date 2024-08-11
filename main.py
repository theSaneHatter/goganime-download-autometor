import pyautogui as pag
import time
import math
#ep button : 867-958 = 101x, 776-805 = 29y
#ep button spaceing : 686-697 = 11yx
#ep buttons first button top left corner 470x, 856y
#ep buttons last button first row top left corner : 1069x, 660
#ep row length : 582px
#ep row ep count : 7eps

#play_button_loc = 800x, 650y
#play button desired color : (232, 230, 227)

#nessosary_scrolls to center page : -230

ep_button_dimentions = (88, 29)
ep_row_ep_count = 7
ep_button_spaceing = (11,11)
first_top_left_corner = (472, 852)

play_button_location = (800,650)
play_button_color = (232, 230, 227)

nessosary_scrolls = -230

download_position = (972, 628)
screenshot_path = "C:/Users/jonad/Desktop/Code/gogoanime_downloader/vidstreem_logo.png"

download_link_pos = (1045, 445)

def get_ep_cordanents(button_dimentions, space_dimentions, row_count, episode_number, first_button_top_left):
    

    colloms = math.ceil(episode_number/row_count) 
    print('colloms: ', colloms) 
    y = ((colloms-1) * (button_dimentions[1] + space_dimentions[1])) + first_button_top_left[1] 

    if (episode_number % row_count) == 0:
        x = row_count * (button_dimentions[0] + space_dimentions[0])   + first_button_top_left[0]
     
        
    #idk why tf this be like this, but need manually shift x left 
    x = ( ( (episode_number - ((colloms-1) * row_count))  * (button_dimentions[0] + space_dimentions[0])   ) + first_button_top_left[0]) - (button_dimentions[0] + space_dimentions[0]) 
    # print(f"colloms: {colloms}, row_count: {row_count}")
    # print(f"episode number: {episode_number}, episode_number - (colloms-1*row_count): {episode_number - ((colloms-1) * row_count)}")
    # print(f"(button_dimentions[0] + space_dimentions[0]): {(button_dimentions[0] + space_dimentions[0])}")
        
    
    
    y += round(button_dimentions[1]/2)
    x += round(button_dimentions[0]/2)
    
    print(f'ep {episode_number}s cords: {x},{y}')
    return x,y


def move_to_episode(button_dimentions, space_dimentions, row_count, episode_number, first_button_top_left):
    button_press_cord = get_ep_cordanents(button_dimentions, space_dimentions, row_count, episode_number, first_button_top_left)
    pag.moveTo(button_press_cord)

    while str(pag.position()) == str(button_press_cord):
    
        print(f"\033[33mFailed to arrive @ {button_press_cord}, instead at {pag.position()}... Retrying\033[0m")
        pag.moveTo(button_press_cord)

    print(f"\033[32mMoved To episode {episode_number}'s Button! {button_press_cord} == {pag.position()}\033[0m")

def varaify_page_loaded(play_button_cords, play_button_rgb):
    page_loaded = False
    pag.moveTo(play_button_cords[0]-5, play_button_cords[1])
    color_variat = 50
    count = 0
    pag.scroll(500)
    while not page_loaded:
        px = pag.pixel(play_button_cords[0], play_button_cords[1])
        if abs(play_button_rgb[0] - px[0]) < color_variat and abs(play_button_rgb[1] - px[1]) < color_variat and abs(play_button_rgb[2] - px[2]) < color_variat:
            page_loaded = True
            print('\033[32mPage is loaded!\033[0m')
            break
        else:
            px = pag.pixel(play_button_cords[0], play_button_cords[1])
            print(f'\033[33mPage not loaded! desired rgb: {play_button_rgb}  current color:  {px}\033[0m')        
            pag.moveRel(5,5,.1)
            pag.moveRel(-5,-5,.1)
        
        count +=1

        if count > 50:
            pag.hotkey("ctrl", "r")
            count = 0
            pag.scroll(500)



            
    return True

def center_page(scrolls, play_button_loc):
    pag.moveTo(play_button_loc)
    pag.scroll(500)    
    pag.scroll(scrolls)
    pag.moveTo(play_button_loc[0], play_button_loc[1] + scrolls)

#must start from centered posistion and varaify_page_loaded() has just run
def go_to_download_page(download_pos, play_button_cords, play_button_rgb, scrolls, logo_path):
    
    
    time.sleep(.2)
    pag.click()
    count = 0
    while pag.pixel(play_button_cords[0],play_button_cords[1]) == (0,0,0):
        if count == 0:
            print(f"\033[33mThe video seemes to be taking awhile to load...\033[0m")

        pag.moveRel(5,5,.1)
        pag.moveRel(-5,-5,.1)
        count += 1
        if count > 60:
            print(f"\033[33mReloading&centering page\033[0m")
            varaify_page_loaded(play_button_cords, play_button_rgb)
            center_page(scrolls, play_button_cords)

            count =  0
        if count % 4 == 0:
            pag.click()
        time.sleep(1)
    time.sleep(1)
    pag.click()
    pag.moveTo(download_pos)
    time.sleep(.1)
    pag.click()
    logo_found = False
    count = 0
    while not logo_found:
        logo_found = find_logo(logo_path)
        time.sleep(.5)
        count+=1
        if count > 50:
            pag.click()
            print("\033[33mUnable to find download page, retrying...\033[0m")
            


    print("\033[32mThe Download Page has been found")

def find_logo(logo_path):
    try:
        logo = pag.locateOnScreen(logo_path) 
        return True
    except pag.ImageNotFoundException:
        return False

def rgb_compar(rgb1,rgb2,scope):
    return abs(rgb1[0]-rgb2[0])<=scope and abs(rgb1[1]-rgb2[1])<=scope and abs(rgb1[2]-rgb2[2])<=scope 

def download_from_link(link_pos):
    pag.moveTo(link_pos)
    time.sleep(.2)
    pag.click()
    print("\033[32mAttempted to download episode!\033[0m")

    time.sleep(2)
    pag.hotkey("ctrl", "w")
    return True
    
time.sleep(4)


for episode in range(1,12):
    center_page(nessosary_scrolls, play_button_location)
    move_to_episode(ep_button_dimentions, ep_button_spaceing, ep_row_ep_count, episode, first_top_left_corner)
    pag.click()
    varaify_page_loaded(play_button_location,play_button_color)
    center_page(nessosary_scrolls, play_button_location)
    go_to_download_page(download_position,play_button_location,play_button_color,nessosary_scrolls,screenshot_path)
    download_from_link(download_link_pos)


'''
for ep in range(1,29):
    center_page(nessosary_scrolls, play_button_location)
    move_to_episode(ep_button_dimentions, ep_button_spaceing, ep_row_ep_count, ep, first_top_left_corner)
    pag.click()
    print(f"\033[32mPressed button!\033[0m")
    varaify_page_loaded(play_button_location,play_button_color)
    print('\033[32Page is loaded!\033[0m')
    center_page(nessosary_scrolls, play_button_location)
'''
    

