from src.ui.common import CommonTheme
import PySimpleGUI as sg

class PleaseWait(CommonTheme):
    def __init__(self):
        super().__init__()
        self._main_window = None
        self._layout = None

    def layout(self):
        if not self._layout:
            self._layout = [
                [sg.Text("Please Wait: Monero RPC Server Is Starting", key="wait_text", font=(self.font, 18), background_color=self.ui_overall_background)],
                [sg.Text("                                   This may take a few minutes on first launch.", key="wait_text2", font=(self.font, 10), background_color=self.ui_overall_background)]
              ]
        return self._layout

    def main_window(self):
        if not self._main_window:
            self._main_window = sg.Window("Waiting", self.layout(), finalize=True, keep_on_top=True, no_titlebar=True, grab_anywhere=True)
        return self._main_window

    def open(self):
        self.main_window()

    def update(self):
        return self._main_window.read(timeout=100)

    def close(self):
        self._main_window.close()