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
                break
        except pyautogui.ImageNotFoundException:
            count = count + 1
            print(f"Button in {pic_name} could not be located. Retry {max_retires - count} times...")
            time.sleep(1)
            if count >= max_retires :
                break

def get_resolution() -> int:
    """
    get resolution from prompt
    either 1080(1k) or 1440(2k)

    Returns: resolution(int): 1080 or 1440

    """
    try:
        resolution = pyautogui.prompt(f"Enter Resolution: {RESOLUTION_1080}/{RESOLUTION_1440}", title = "Resolution")
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
                time.sleep(12)
                pyautogui.click()
                print("ejected")
                break
        except pyautogui.ImageNotFoundException:
            time.sleep(0.25)

def choose_legend(legend_name: str, conf_level: float) -> int:
    while True:
        try:
            x, y = pyautogui.locateCenterOnScreen(legend_name, confidence = conf_level)
            if x is not None and y is not None:
                pyautogui.moveTo(x, y)
                pyautogui.middleClick()
                pyautogui.hotkey("esc")
                break
        except pyautogui.ImageNotFoundException:
            time.sleep(0.25)


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
    resolution = get_resolution()
    if resolution is None:
        return
    
    # open window
    status = find_and_open_from_taskbar(PROGRAM_TITLE)  # Open program from task bar
    if status == False:
        return
    time.sleep(1)

    # start phase
    if auto_click_button(0.6, f"./{resolution}/start.png", 1, 0.5):
        # solo play
        auto_click_button(0.8, f"./{resolution}/fillTeam.png", 5, 0.5)
    else:
        # solo play
        auto_click_button(0.8, f"./{resolution}/fillTeam.png", 1, 0.5)
    # choose legend
    auto_click_button(0.8, f"./{resolution}/legendTab.png", 1, 0.5)

    # legend
    choose_legend(f"./{resolution}/legends/baolei.png", 0.7)

    while True:
        # ready
        auto_click_button(0.9, f"./{resolution}/ready.png", 20, 0.5)
        # eject
        ejection(f"./{resolution}/eject.png", 0.6)
        # game end back to main manu
        auto_click_button(0.9, f"./{resolution}/endBack.png", 2400, 0.25)
        auto_click_button(0.9, f"./{resolution}/endYes.png", 20, 0.25)
        auto_click_button(0.9, f"./{resolution}/endContinue.png", 30, 0.25)
        auto_click_button(0.9, f"./{resolution}/endContinue2.png", 20, 0.25)


if __name__ == "__main__":
    main()  # Execute the main function if this script is run as the main program.
