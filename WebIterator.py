import os
import time
# import numpy as np
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.common.action_chains import ActionChains

PATH_DATA = "./Data"
TIMEOUT = 10  # seconds

URL = {
    "base_url": "https://www.puzzle-binairo.com/",
    "specific_url": "",
    "size_url": {
        6: {
            "easy": "binairo-6x6-easy/",
            "hard": "binairo-6x6-hard/",
        },
        8: {
            "easy": "binairo-8x8-easy/",
            "hard": "binairo-8x8-hard/",
        },
        10: {
            "easy": "binairo-10x10-easy/",
            "hard": "binairo-10x10-hard/",
        },
        14: {
            "easy": "binairo-14x14-easy/",
            "hard": "binairo-14x14-hard/",
        },
        20: {
            "easy": "binairo-20x20-easy/",
            "hard": "binairo-20x20-hard/",
        },
    },
}


class WebInteractor:
    def __init__(self, url, credentials=None):
        self.URL = url
        self._driver = self._driver_setup()
        self._driver.get(self.URL["base_url"])
        self.credentials = credentials
        # Accept and close privacy preference window
        # self._wait(By.XPATH, "/html/body/div[1]/div/div/div/div[2]/div/button[2]", TIMEOUT).click()
    
    # Driver setup for Chrome 
    # def _driver_setup(self):
    #     service = Service()
    #     options = webdriver.ChromeOptions()
    #     options.add_experimental_option("detach", True)
    #     driver = webdriver.Chrome(service=service, options=options)
    #     return driver

    # Driver setup for Microsoft Edge
    def _driver_setup(self):
        from selenium.webdriver.edge.service import Service as EdgeService
        from selenium.webdriver.edge.options import Options as EdgeOptions
        from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

        options = EdgeOptions()
        options.add_experimental_option("detach", True)  # make browser not auto close

        # Hide log debug/error from browser
        options.add_argument("--log-level=3")  # only fatal error will appear
        options.add_argument("--disable-logging")
        options.add_argument("--disable-blink-features=AutomationControlled")
        # options.add_argument("--headless")  # optional: browser not showing

        # Deactive logging internal from Edge
        caps = DesiredCapabilities.EDGE
        caps['goog:loggingPrefs'] = {'browser': 'OFF', 'driver': 'OFF', 'performance': 'OFF'}

        service = EdgeService()  # set default, selenium will automatically search msedgedriver
        driver = webdriver.Edge(service=service, options=options)
        return driver


    def _login(self, credentials):
        # Open login menu
        self._wait(By.ID, "menu-button-user", TIMEOUT).click()

        # Input credentials and click login button
        self._wait(By.NAME, "email", TIMEOUT).send_keys(credentials["email"])
        self._wait(By.NAME, "password", TIMEOUT).send_keys(credentials["password"])
        self._wait(By.CLASS_NAME, "button-login", TIMEOUT).click()

        self._wait(By.ID, "user-cert", TIMEOUT)

    ''' 
        Wait until an element is visible on the page, then retrieve that element.
    '''

    def _wait(self, locator, value, timeout):
        return WebDriverWait(self._driver, timeout).until(EC.visibility_of_element_located((locator, value)))

    '''
        Scrape puzzles with the specified size, difficulty and ID.
        For puzzles larger than 20 in size, the IDs need to be specified since they cannot be accessed randomly. 
    '''

    def scrape_puzzle(self, size, difficulty=None, amount=None, ids=None):
        # If IDs are specified or puzzles larger than 20 in size
        if ids is not None:
            if self.credentials is not None:
                self._login(self.credentials)
            for id in ids:
                # Make sure there are no duplicate
                if not os.path.exists(f"{PATH_DATA}/{size}{difficulty if difficulty is not None else ''}/{id}.txt"):
                    id, borders = self.open_puzzle(size, difficulty, id)
                    self.save_puzzle(id, borders, size, difficulty)
        else:
            scraped = 0
            while scraped < amount:
                id, borders = self.open_puzzle(size, difficulty)
                # Make sure there are no duplicate
                if not os.path.exists(f"{PATH_DATA}/{size}{difficulty if difficulty is not None else ''}/{id}.txt"):
                    self.save_puzzle(id, borders, size, difficulty)
                    scraped += 1
        self.close()

    '''
        This method opens a puzzle with the specified size, difficulty and ID.
        For puzzles larger than size 20, there are no choices for the difficulty. Therefore, the difficulty should not be specified. 
        The method can open:
        - A random puzzle, where the ID should not be specified.
        - A specific puzzle, where the ID should be specified.
            For puzzles larger than size 20, a specific puzzle is accessed by opening the corresponding puzzle's URL and selecting the ID from a select element.

        @return id: string
        @return borders: dict
    '''

    def open_puzzle(self, size, difficulty=None, id=None):

        # Open puzzle #
        url = self.URL["base_url"]

        # Specific puzzles larger than 20 in size
        if size.isnumeric() and id:
            url += self.URL["specific_url"]
        else:
            if size.isnumeric():
                url += self.URL["size_url"][int(size)][difficulty]
            else:
                url += self.URL["size_url"][size]
        self._driver.get(url)

        # Specific puzzles
        if id is not None:
            if size.isnumeric():
                # Input puzzle attributes and click button
                self._wait(By.ID, "specid", TIMEOUT).send_keys(id)
                Select(self._wait(By.ID, "size", TIMEOUT)).select_by_value(self.URL["size_url"][int(size)][difficulty][-1])
                self._wait(By.XPATH, "//*[@id='pageContent']/div[2]/div[2]/form[1]/table/tbody/tr[3]/td[2]/input",
                           TIMEOUT).click()
            else:
                select_element = Select(self._wait(By.NAME, "date", TIMEOUT))
                # Open puzzle only when the specified id exists
                if id in [option.get_attribute("value") for option in select_element.options]:
                    select_element.select_by_value(id)
                    self._wait(By.NAME, "specific", TIMEOUT).click()
                else:
                    return None, None

        # Get puzzle ID #
        if size.isnumeric():
            id = self._wait(By.ID, "puzzleID", TIMEOUT).text
        else:
            id = Select(self._wait(By.NAME, "date", TIMEOUT)).first_selected_option.get_attribute("value")


        WebDriverWait(self._driver, 20).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".task-cell, .cell"))
        )

        cells = self._driver.find_elements(By.CSS_SELECTOR, ".task-cell, .cell.selectable.cell-off")
        
        print(f"Found {len(cells)} cells on the board")

        for idx, c in enumerate(cells[:10]):
            print(f"Cell {idx}: class={c.get_attribute('class')}, text='{c.text}'")

        EMPTY_CELL = -1
        WHITE_CELL = 0
        BLACK_CELL = 1
        special= {"daily": 30,"weekly": 30,"monthly":40}

        if not size.isnumeric():
            size = special[size]
        else:
            size = int(size)

        board = []  # returned 2d list
        row = []  # used for temporary row list
        i = 0

        # Iterate trough every tile on the tiles
        for tile in cells:
            tileClass = tile.get_attribute("class").strip()

            if "cell-0" in tileClass:
                # putih
                row.append(WHITE_CELL)
            elif "cell-1" in tileClass:
                # hitam
                row.append(BLACK_CELL)
            else:
                # kosong
                row.append(EMPTY_CELL)

            if i == size - 1:
                board.append(row)
                row = []
                i = 0
            else:
                i += 1

        # debug print
        print("Board:")
        for r in board:
            print(" ".join(str(x) for x in r))

        # self._driver.close()
        return id, board

    def save_puzzle(self, id, board, size, difficulty=None):
        data = [
            f"{id}\n",
            f"{size} {difficulty if difficulty is not None else ''}\n"
        ]
        for row in board:
            strings = ""
            for column in row:
                strings += str(column) + " "
            data.append(f"{strings}\n")
        path = f"{PATH_DATA}/{size}{difficulty if difficulty is not None else ''}/{id}.txt"
        
        # Ensure the folder is there
        os.makedirs(os.path.dirname(path), exist_ok=True)
        
        file = open(path, "x")
        file.writelines(data)
        file.close()

    def save_answer(self, id, answer, size, difficulty=None):
        board = answer.state.board

        data = [
            f"{id}\n",
            f"{size} {difficulty if difficulty is not None else ''}\n"
        ]
        for row in board:
            strings = ""
            for column in row:
                strings += str(column) + " "
            data.append(f"{strings}\n")

        path = f"./Answer/{size}{difficulty if difficulty is not None else ''}/{id}.txt"

        # Ensure the folder is there
        os.makedirs(os.path.dirname(path), exist_ok=True)

        file = open(path, "w")
        file.writelines(data)
        file.close()

    '''
        Simulate mouse clicks on a specific puzzle cell.
        Selenium's ActionChains to move the mouse pointer to the target cell element on the web page.

        @params cell: WebElement representing the target cell.
        @params clicks: number of times to click the cell (default = 1).
    '''

    def click_cell(self, cell, clicks=1):
        actions = ActionChains(self._driver)
        actions.move_to_element(cell)
        for _ in range(clicks):
            actions.click()
        actions.perform()

    '''
        Input the solved puzzle answer into the web interface.
        The rules for clicking:
        - 1 (BLACK): single right-click
        - 0 (WHITE): double right-click
        - -1 (EMPTY): do nothing
        *Cells with class "task-cell" (predefined) are never clicked

        @params answer: 2-dimensional array of integer
    '''

    def input_answer(self, answer):
        # get all board cells (including regular and task-cells)
        cells = self._driver.find_elements(By.CSS_SELECTOR, ".cell, .task-cell")

        # cells = [c for c in self._driver.find_elements(By.CSS_SELECTOR, ".cell") if "task-cell" not in c.get_attribute("class")]

        flat_answer = [val for row in answer.state.board for val in row]
    
        # debug print
        # print(f"[INFO] Total board cells: {len(flat_answer)}")
        # print(f"[INFO] Total DOM cells: {len(cells)}")
    
        # iterate through each cell and its corresponding board value
        for idx, (cell, val) in enumerate(zip(cells, flat_answer)):
            cell_class = cell.get_attribute("class")
            
            # skip if predefined task-cell
            if "task-cell" in cell_class:
                continue
            
            if val == 1:    # BLACK
                self.click_cell(cell, 1)
            elif val == 0:  # WHUTE
                self.click_cell(cell, 2)
            elif val == -1: # EMPTY
                continue

    '''
        @return answer: 2-dimensional array of integer
    '''

    # def get_answer(self, size, id, difficulty=None):
    #     self.open_puzzle(size, difficulty, id)
    #     self._wait(By.ID, "btnGiveUp", TIMEOUT).click()
    #     alert = WebDriverWait(self._driver, timeout=2).until(lambda d: d.switch_to.alert)
    #     alert.accept()
    #
    #     self._wait(By.CLASS_NAME, "cell", TIMEOUT)
    #     cells = self._driver.find_elements(By.CLASS_NAME, "cell")
    #     answer = []
    #     for i in range(size ** 2):
    #         classes = cells[i].get_attribute("class").split()
    #         if "cell-on" in classes:
    #             answer.append(1)
    #         else:
    #             answer.append(0)
    #     return np.array(answer).reshape(size, size)

    def close(self):
        self._driver.close()

