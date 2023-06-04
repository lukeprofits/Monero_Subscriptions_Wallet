# Monero Subscriptions Wallet
![Supported OS](https://img.shields.io/badge/Supported%20OS-Windows%20/%20Mac%20/%20Linux-blueviolet.svg)
![Version 1.1.0](https://img.shields.io/badge/Version-1.1.0-blue.svg)
![Python 3.8+](https://img.shields.io/badge/Python-3.8+-brightgreen.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Uses](https://img.shields.io/badge/Uses-Monero%20RPC-orange.svg)

A Monero wallet that automatically pays subscriptions.

<p align="center">
  <br><img src="Example.jpg" alt="Description of the photo"><br>
</p>


# How To Use:

(Video Coming Soon)

* Make sure you have [Python 3.8](https://www.python.org/downloads/) or newer installed
* [Download the Monero Subscripton Wallet files](https://github.com/lukeprofits/Monero_Subscriptions_Wallet/archive/refs/heads/main.zip) extract all the files from the .zip you downloaded and put them in a folder
* [Download the Monero CLI Wallet](https://www.getmonero.org/downloads/#cli), extract all the files from the .zip you downloaded and put them in the same folder

* Optional: Download and install [the font Nunito Sans](https://fonts.google.com/specimen/Nunito+Sans)
* On Windows, double click the "Windows_Launcher" file
* On Mac/Linux, run the "Mac_Linux_Launcher" file 
* Or if you are comfortable with the terminal, on any OS open your console and enter the command: `python Monero_Subscriptions_Wallet.py`
* On Linux there are some required clipboard packages. For non-wayland sessions they are: xclip and xsel, for wayland sessions it is: wl-clipboard. Make sure to install them with your package manager.


# Donate
If you use this, send me some XMR. It took weeks to develop, and I did not ask for, or recieve any [CCS funding](https://ccs.getmonero.org/) for this project.

XMR: `4At3X5rvVypTofgmueN9s9QtrzdRe5BueFrskAZi17BoYbhzysozzoMFB6zWnTKdGC6AxEAbEE5czFR3hbEEJbsm4hCeX2S`


$1/mo XMR donation: `monero-subscription:H4sIAJEcZGQC/12Oy07DMBBFfyXymqI8mqCyS5oECQQSbaGlm8h2po2FH5HtFGzEvxN3yaxm7j3SmR9EJ2OV6DgmwNF9hPaYc7BRDRfgagQd1Upiy5RENxEyMJfadF9XKODL0maHXF/e3bhTp7OY4GVlVq9W+34DeTVBq81neWTJXaU+yOCdUd6r57Yq/F7unvqHdVF+NyVpmpz6dpMN8/ZIjFgOazik2yClk9YgqQu6t20dIizUJIM/uY3nc8ROgLQd6wMT/5vr4xZr2/XYQiDSOM0Wcb5IitARxjmT5446ymFmnJmZLP79A+WbtpUcAQAA`


$10/mo XMR donation: `monero-subscription:H4sIAIMbZGQC/12OXU+DMBSG/wrh2pkCAzPvYICJRhO36eZuSFvOBrEfpC3T1vjfbXfpuTrnfZ/kOT8xnbWRvGOYAIvvo3iPGQMT1XABJidQUS0FNqMU8U0Ua/Cl0t3XFQr4sjTZIVeXdzvt5OnMZ3hZ6dWrUa7fQF7N0Cr9WR7H5K6SH2RwVkvn5HNbFW4vdk/9w7oov5uSNE1OXbvJBr89Es2XwxoO6TZI6awUCGqD7m1bhwhzOYvgT9At8veELQdhurEPEPo3188NVqbrsYFApCjNFihfJEXoyMjYKM4dtZSBZ6z2TIZ+/wAVPrHVHQEAAA==`


$25/mo XMR donation: `monero-subscription:H4sIAB8cZGQC/12Oy07DMBBFfyXymiI3qYPKLmkSJBBItIUWNpHjDI2FH5HtFGzEvxN3yaxm7j3SmR/EJuu0bAXtQKDbBB2oEOCSCs4g9AgmqbSijmuFrhJkYS6Nbb8uUMRXhcuOxJxf/bjXHyc5wdParp+dCf0WSDlBY+xn8c6XN6V+64bgrQ5BPzZlHg5q/9DfbfLiuy66uiYsNNtsmLf7zsrVsIFjuotSNhkDivmoe9lVMaJSTyr6U3KN53ukXoJyLe8jhP/N5XNHjWt76iASKU6zBSaLZR67jgvB1allngmYGW9nJsO/f8u/kXcdAQAA`


# Tools For Merchants
* Recommended: [Monero Subscription Code Creator Website](https://monerosub.tux.pizza/)
* [Monero Subscription Code Creator Application](https://github.com/lukeprofits/Monero_Subscription_Code_Creator)
* More "useful" monero-subscription integration tools coming soon...


# Documentation For Merchants
* [How To Create `monero-subscription` codes](https://github.com/lukeprofits/Monero_Subscriptions_Standard)


## Features
* Automatically send recurring payments without a middleman
* Add subscriptions from merchants, or create them manaually
* Send donations to your favorite content creators (or developers) on a set schedule
* Supports Subscriptions Billing: Daily, Weekly, Monthly, Yearly, or anything in between!


## Works On
- Windows
- Linux
- Mac - Testing Needed


## Requirements
* [Python 3.8](https://www.python.org/downloads/) or above
* [Monero CLI Wallet](https://www.getmonero.org/downloads/#cli)
* [monero_usd_price](https://github.com/lukeprofits/Monero-USD-Price)
* [psutil](https://github.com/giampaolo/psutil)
* [qrcode](https://github.com/lincolnloop/python-qrcode)
* [requests](https://github.com/psf/requests)
* [PySimpleGUI](https://github.com/PySimpleGUI/PySimpleGUI)
* [lxml](https://github.com/lxml/lxml)
* [clipboard](https://pypi.org/project/clipboard)
* [Pillow](https://pypi.org/project/Pillow/) 


## License
[MIT](https://github.com/Equim-chan/vanity-monero/blob/master/LICENSE)
