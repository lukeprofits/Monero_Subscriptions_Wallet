import customtkinter as ctk
from src.interfaces.view import View
import config as cfg

class ReceiveView(View):
    def build(self):
        self.window_label()
        # Back Button
        # unicode back button options: ← ↼ ↽ ⇐ ⇚ ⇦ ⇽ 🔙 ⏴ ◅ ← ⬅ ⬅️⬅ ◄ ◅
        back_button = self.add(ctk.CTkButton(self._app, text="⬅", font=(cfg.font, 24), width=35, height=30, command=self.open_main))
        back_button.grid(row=0, column=0, padx=10, pady=10, sticky="w")

    def window_label(self):
        label = self.add(ctk.CTkLabel(self._app, text="Recieve Window"))
        label.grid(row=0, column=0, columnspan=3, padx=10, pady=5, sticky="ew")
        return label

    def open_main(self):
        self._app.switch_view('main')
