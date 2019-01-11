# Automated Whatsapp Cricket Commentary

A python script that fetches live cricket commentary from a source(I've used ESPN Cricinfo), and sends it to a contact on Whatsapp automatically, at regular intervals.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

You'll need to have an installation of Python installed on your system, download from [here](https://www.python.org/downloads/).

Easily configurable as per one's own use-case, can change -
- Schedule interval (can be in seconds/minutes/hours/days, refer [Schedule Docs](https://schedule.readthedocs.io/en/stable/)).
- Match URL - in [properties.py](properties.py).
`(P.S.: ESPN Cricinfo only. Will have to dig into the HTML again for another site, for now I'm fine with just this one!)`
- Display options.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

<h3>Have fun! :)<h3>