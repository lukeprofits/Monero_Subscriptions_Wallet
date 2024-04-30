import customtkinter as ctk
from src.interfaces.view import View
import config as cfg
import styles

class WelcomeView(View):
    def build(self):
        def selected_currency_callback(choice):
            cfg.CURRENT_SEND_CURRENT_AMOUNT = choice

        self._app.geometry(styles.WELCOME_VIEW_GEOMETRY)

        # Title
        label = self.add(ctk.CTkLabel(self._app, text='Welcome to the Subscriptions Wallet!', font=styles.HEADINGS_FONT_SIZE))
        label.grid(row=0, column=0, columnspan=3, padx=10, pady=(15, 0), sticky="ew")

        # To make this look better, I am adding spaces after to get the lines to line up
        info_text = '''
    We're thrilled that you've chosen to use our Free and Open Source Software.
    Before you get started, there are a few important things you should know:     

    1. Monero Subscriptions Wallet is currently in beta. Your feedback is 
       valuable to us in making this software better. Please let us know if
       you encounter any issues or, if you are a developer,                        
       help resolve them! All the code is on GitHub.                                    

    2. Monero Subscriptions Wallet is intended to be a secondary wallet, 
        rather than your primary one. As an internet-connected hot wallet,
        its security is only as robust as your computer's. We suggest         
        using it as a side-wallet, maintaining just enough balance               
        for your subscriptions.                                                                          

    3. By using this software, you understand and agree that you are       
        doing so at your own risk. The developers cannot be held                
        responsible for any lost funds.                                                             

    Enjoy using the Monero Subscriptions Wallet, thank you for your support,      
    and if you are a Python developer, help us improve the project!                       

    https://github.com/lukeprofits/Monero_Subscriptions_Wallet      
    '''
        info = self.add(ctk.CTkLabel(self._app, text=info_text))
        info.grid(row=1, column=0, columnspan=3, padx=10, pady=0, sticky="ew")

        # Send button
        ok_button = self.add(ctk.CTkButton(self._app, text="Okay", corner_radius=15, command=self.open_main))
        ok_button.grid(row=2, column=0, columnspan=3, padx=120, pady=(5, 10), sticky="ew")

        return self

    def open_main(self):
        self._app.switch_view('main')
