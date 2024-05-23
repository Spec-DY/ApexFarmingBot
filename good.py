import pyautogui
import pygetwindow as gw
import time

PROGRAM_TITLE = "Apex Legends"
NO_TITLE_ERROR = "Window titled '{}' not found."
START_STATUS = True
RESOLUTION_1080 = 1080
RESOLUTION_1440 = 1440


def auto_click_button(conf_level: float, pic_name: str, max_retires: int, move_speed: int) -> None:
    """
    It continuously click the provided pic_name with a conf_level.
    break after click
    if pic not found loop again
    
    Arguments:
    conf_level(float) : confidence level of how the actually button will look like the provided picture
    pic_name(str): name of the button screenshot

    Returns:
    None

    """
    count = 0
    while True:
        try:
            x, y = pyautogui.locateCenterOnScreen(pic_name, confidence = conf_level)
            if x is not None and y is not None:
                pyautogui.moveTo(x, y, duration = move_speed)
                pyautogui.click()
                print(f"Clicked on {pic_name} successfully.")
                return True
        except pyautogui.ImageNotFoundException:
            count = count + 1
            print(f"Button in {pic_name} could not be located. Retry {max_retires - count} times...")
            if count >= max_retires :
                return False
            time.sleep(1)

def get_resolution() -> int:
    """
    get resolution from prompt
    either 1080(1k) or 1440(2k)

    Returns: resolution(int): 1080 or 1440

    """
    try:
        resolution = pyautogui.prompt(f"输入分辨率, 1k为1080, 2k为1440: {RESOLUTION_1080}或{RESOLUTION_1440}", title = "Resolution")
        resolution = int(resolution)
        if resolution not in (RESOLUTION_1080, RESOLUTION_1440):
            return None
        return resolution
    except (TypeError, ValueError):
        return None

def find_and_open_from_taskbar(window_title: str) -> None:
    """
    Finds a window by its title and restores it if minimized. If not minimized, it will minimize and then restore it.

    Parameters:
    - window_title (str): The title of the window to find and restore.

    Returns:
    - None
    """
    try:
        # Attempt to get the first window matching the provided title.
        window = gw.getWindowsWithTitle(window_title)[0]
        if window.isMinimized:  # Check if the window is currently minimized.
            window.restore()  # Restore the window if it is minimized.
        else:  # If the window is not minimized,
            window.minimize()  # First minimize it,
            time.sleep(1)  # wait for a second,
            window.restore()  # and then restore it to ensure it's visible on screen.
    except IndexError:  # Handle the case where no window with the given title is found.
        print(NO_TITLE_ERROR.format(window_title))
        return False
    
def ejection(pic_name: str, conf_level: float):
    while True:
        try:
            x = pyautogui.locateOnScreen(pic_name, confidence = conf_level)
            if x is not None:
                # commented for test case
                # uncomment this to jump to the middle of map
                time.sleep(12)
                pyautogui.click()
                print("ejected")
                break
        except pyautogui.ImageNotFoundException:
            # uncomment below for test case
            # current_time = time.localtime()
            # seconds = current_time.tm_sec
            # print(f"Look for Ejection Button lasting {seconds} seconds...")
            time.sleep(0.25)

def choose_legend(conf_level: float, legend_name: str, max_tries: int) -> int:
    count = 0
    while True:
        try:
            x, y = pyautogui.locateCenterOnScreen(legend_name, confidence = conf_level)
            if x is not None and y is not None:
                pyautogui.moveTo(x, y, duration= 0.25)
                pyautogui.middleClick()
                time.sleep(1)
                print("corresponding legend clicked")
                # resolution defined as 1080 here

                # back to main menu
                auto_click_button(0.7, f"./1080/mainMenu.png", 3, 0.25)
                break
        except pyautogui.ImageNotFoundException:

            count += 1
            if count >= max_tries:
                print("choose legend fail, return")
                return False
            time.sleep(0.25)


def parse_legends(user_input: str) -> list:
    if not user_input:
        return []

    parts = user_input.split()
    legends_list = []

    for i in range(0, len(parts), 2):
        try:
            name = parts[i]
            times = int(parts[i + 1])
            legends_list.append([name, times])
        except (IndexError, ValueError):
            print(f"Error parsing input: {user_input}")
            return []
    print(legends_list)
    return legends_list


def infinite_click(conf_level: float, pic_name: str) -> None:
    """
    It continuously click the provided pic_name.
    """
    count = 0
    while True:
        try:
            x, y = pyautogui.locateCenterOnScreen(pic_name, confidence = conf_level)
            if x is not None and y is not None:
                pyautogui.moveTo(x, y, duration = 0.25)
                pyautogui.click()
                print(f"Clicked on {pic_name} button.")
                return True
        except pyautogui.ImageNotFoundException:
            time.sleep(1)
            count += 1
            print(f"Looked for {pic_name} button for {count} times...")


def move_and_hold_on_image(image_path, hold_duration=2):
    """
    Moves the mouse to the center of an image, clicks, and holds the mouse button down for a specified duration.

    Parameters:
    - image_path (str): Path to the image file.
    - hold_duration (int): Duration in seconds to hold the mouse button down.

    Returns:
    - None
    """
    try:
        # Locate the image on the screen
        x, y = pyautogui.locateCenterOnScreen(image_path, confidence=0.8)
        if x is not None and y is not None:
            pyautogui.moveTo(x, y, duration=0.5)  # Move the cursor to the image
            pyautogui.mouseDown()                # Press and hold the left mouse button
            time.sleep(hold_duration)            # Hold the mouse button down for the duration specified
            pyautogui.mouseUp()                  # Release the mouse button
        else:
            print("Image not found on the screen.")
    except pyautogui.ImageNotFoundException:
        print("The image file does not exist or cannot be found.")
    except Exception as e:
        print(f"An error occurred: {e}")



def main() -> None:
    """
    Main function that orchestrates the finding and opening of a window from the taskbar,
    and continuously clicking at the bottom left corner of the screen.

    Parameters:
    - None

    Returns:
    - None
    """
    # resolution get
    resolution = 1080

    # disable resolution selection
    # resolution = get_resolution()
    # if resolution is None:
    #     return
    
    # get user input
    user_input = pyautogui.prompt("输入英雄空格次数, 例如:'baolei 3 waji 10',也可以不输入", title="Choose Legends")
    legend_names = parse_legends(user_input)

    # ready button tracker
    ready_clicked_times = 0
    # open window
    status = find_and_open_from_taskbar(PROGRAM_TITLE)  # Open program from task bar
    if status == False:
        return
    time.sleep(1)


    
    # temperally disable start phase
    # start phase
    # if auto_click_button(0.6, f"./{resolution}/start.png", 1, 0.5):
    #     # solo play
    #     auto_click_button(0.8, f"./{resolution}/fillTeam.png", 4, 0.25)
    # else:
    #     # solo play
    #     auto_click_button(0.8, f"./{resolution}/fillTeam.png", 1, 0.25)

    while True:
        
        auto_click_button(0.8, f"./{resolution}/fillTeam.png", 1, 0.25)
        print(legend_names)
        if legend_names is not None:
            # legend
            for legend, times in legend_names:
                current_count = 0
                while current_count < times:
                    try:
                        # choose legend
                        auto_click_button(0.8, f"./{resolution}/legendTab.png", 20, 0.5)
                        choose_legend(0.7, f"./{resolution}/legends/{legend}.png", 20)
                        print(f"{legend} in {times - current_count} times")
                        # ready
                        status = infinite_click(0.9, f"./{resolution}/ready.png")
                        if status == True:
                            ready_clicked_times += 1
                        # eject
                        ejection(f"./{resolution}/eject.png", 0.6)
                        # game end back to main manu
                        auto_click_button(0.7, f"./{resolution}/endBack.png", 2400, 0.25)
                        auto_click_button(0.6, f"./{resolution}/endBack.png", 1, 0.25)

                        # for new season
                        move_and_hold_on_image(f"./{resolution}/newbackhold1.png", hold_duration=2)
                        
                        
                        auto_click_button(0.9, f"./{resolution}/endContinue.png", 60, 0.25)  # new: consider 2nd place or 1st
                        auto_click_button(0.9, f"./{resolution}/endContinue2.png", 5, 0.25)

                        # random rewards
                        
                        auto_click_button(0.9, f"./{resolution}/closeRewards.png", 1, 0.25)
                        auto_click_button(0.9, f"./{resolution}/closeRewards2.png", 1, 0.25)
                        

                        auto_click_button(0.6, f"./{resolution}/continue.png", 1, 0.25)
                        auto_click_button(0.6, f"./{resolution}/continue2.png", 1, 0.25)

                        # personal info tab close
                        auto_click_button(0.6, f"./{resolution}/personalInfoBack.png", 2, 0.25)

                        # buy pass notice close
                        auto_click_button(0.6, f"./{resolution}/buyPassNotice.png", 2, 0.25)
                        
                        current_count += 1
                        print(f"Current main while loop end but next still going: {current_count < times}")
                    except KeyboardInterrupt:
                        print(f"Clicked READY button {ready_clicked_times} times!")
                        return
            legend_names = None
        else:
            try:
                # No Legends Chose Game Process
                # ready
                status = infinite_click(0.9, f"./{resolution}/ready.png")
                if status == True:
                    ready_clicked_times += 1
                # eject
                ejection(f"./{resolution}/eject.png", 0.6)
                # game end back to main manu
                auto_click_button(0.7, f"./{resolution}/endBack.png", 2400, 0.25)
                
                auto_click_button(0.6, f"./{resolution}/endBack.png", 1, 0.25)
                move_and_hold_on_image(f"./{resolution}/newbackhold1.png", hold_duration=2)
                auto_click_button(0.9, f"./{resolution}/endContinue.png", 60, 0.25)  # new: consider 2nd place or 1st
                auto_click_button(0.9, f"./{resolution}/endContinue2.png", 5, 0.25)

                # random rewards
                
                auto_click_button(0.9, f"./{resolution}/closeRewards.png", 1, 0.25)
                auto_click_button(0.9, f"./{resolution}/closeRewards2.png", 1, 0.25)
                

                auto_click_button(0.6, f"./{resolution}/continue.png", 1, 0.25)
                auto_click_button(0.6, f"./{resolution}/continue2.png", 1, 0.25)

                # personal info tab close
                auto_click_button(0.6, f"./{resolution}/personalInfoBack.png", 2, 0.25)

                # buy pass notice close
                auto_click_button(0.6, f"./{resolution}/buyPassNotice.png", 2, 0.25)
            except KeyboardInterrupt:
                print(f"Clicked READY button {ready_clicked_times} times!")
                return





if __name__ == "__main__":
    main()
