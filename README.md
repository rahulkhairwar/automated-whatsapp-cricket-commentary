# Automated Whatsapp Cricket Commentary

A python script that fetches live cricket commentary for a Test/ODI(yet to test for T20, but should work the same) match from an ESPNCricInfo match link, and sends it to a contact on Whatsapp automatically, at regular intervals.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

- You'll need to have a Whatsapp account(of course! 😛).
- You'll need to have an installation of Python installed on your system, download from [here](https://www.python.org/downloads/).
- You'll also need to install the modules used in the script via pip3. These modules are mentioned in [requirements.txt](requirements.txt).
To install all of them at once, open terminal, cd to the project directory and run the command -

`pip3 install -r requirements.txt`

aaaaaand you're good to go.

### Deployment

- In properties.py file, replace "Safari" with "Chrome"/"Firefox", whatever browser you have installed.
- Get the match COMMENTARY(on the match page, there's a "Commentary" tab available on the top) URL from [ESPNCricinfo](http://www.espncricinfo.com), for which you want to get the commentary, and replace the content for the current MATCH_URL in properties.py.
- Change the MATCH_START_HOURS/MINUTES and MATCH_END_HOURS/MINUTES as per the time of your system.
- Then, open terminal, cd to the project folder and run the command -
`python3 automator.py`
- A new browser window will open with web-whatsapp open in it. Scan the QR code on the page through your mobile(make sure your phone is connected to the internet the whole time) -
iOS : Whatsapp -> Settings -> Whatsapp Web/Desktop -> Scan QR Code
Android : Whatsapp -> Settings -> Whatsapp Web -> +
- Wait until all the contacts have loaded on the webpage, then go back to the terminal and write all contacts/group names(CASE SENSITIVE) in the terminal, and press ENTER.
- And you're done! :D

The script is easily configurable as per one's own use-case, can change -
- Schedule interval (can be in seconds/minutes/hours/days, refer [Schedule Docs](https://schedule.readthedocs.io/en/stable/)).
- Match URL - in [properties.py](properties.py).
`(P.S.: ESPN Cricinfo only. Will have to dig into the HTML again for another site, for now I'm fine with just this one!)`
- Display options.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

<h3>Have fun! :)<h3>