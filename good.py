import pyautogui
import pygetwindow as gw
import time

PROGRAM_TITLE = "Apex Legends"
NO_TITLE_ERROR = "Window titled '{}' not found."
START_STATUS = True


def auto_click_button(conf_level: float, pic_name: str, max_retires: int) -> None:
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
            x, y = pyautogui.locateCenterOnScreen(pic_name, confidence=conf_level)
            if x is not None and y is not None:
                time.sleep(1)
                pyautogui.moveTo(x, y, duration=1)
                pyautogui.click()
                print(f"Clicked on {pic_name} successfully.")
                break
        except pyautogui.ImageNotFoundException:
            count = count + 1
            print(f"Button in {pic_name} could not be located. Retry {max_retires - count} times...")
            if count >= max_retires :
                break

def auto_click_ready() -> None:
    auto_click_button(0.9, "ready.png", 5)

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

def main() -> None:
    """
    Main function that orchestrates the finding and opening of a window from the taskbar,
    and continuously clicking at the bottom left corner of the screen.

    Parameters:
    - None

    Returns:
    - None
    """
    status = find_and_open_from_taskbar(PROGRAM_TITLE)  # Open program from task bar
    if status == False:
        return
    time.sleep(2)
    auto_click_button(0.6, "start.png", 2)
    while True:
        auto_click_ready()
        print("ALLDONE")
        time.sleep(300)
        

if __name__ == "__main__":
    main()  # Execute the main function if this script is run as the main program.
