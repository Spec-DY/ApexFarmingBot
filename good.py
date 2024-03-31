import pyautogui
import pygetwindow as gw
import time

PROGRAM_TITLE = "Apex Legends"
NO_TITLE_ERROR = "Window titled '{}' not found."
RESOLUTION2K = (200, 1300)
RESOLUTION1K = (100, 650)

def auto_click_ready() -> None:
    """
    Continuously clicks at the bottom left corner of the screen at specified intervals.

    Parameters:
    - none

    Returns:
    - None
    """
    x, y = pyautogui.locateCenterOnScreen("ready.png", confidence= 0.9)
    pyautogui.moveTo(x, y, duration = 1)
    pyautogui.click()

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
    while True:
        auto_click_ready()

if __name__ == "__main__":
    main()  # Execute the main function if this script is run as the main program.
