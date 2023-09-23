<h1 align="center">Discord Quiz Bot</h1>

<div align="center">

  [![License](https://img.shields.io/badge/license-MIT-blue.svg)](/LICENSE)

</div>

---

<p align="center"> Compete with your friends to guess the names of ground vehicles from the popular game <a href = "https://warthunder.com/">War Thunder</a>!
    <br> 
</p>

## Table of Contents
+ [About](#about)
+ [How it works](#working)
+ [Usage](#usage)
+ [Getting Started](#getting_started)
+ [Running the bot](#running)
+ [Built Using](#built_using)
+ [Authors](#authors)
+ [Acknowledgements](#acknowledgement)

## About <a name = "about"></a>
This is a small personal Discord bot created for fun. The bot accesses a JSON database generated from crawling the <a href = "https://wiki.warthunder.com/Main_Page">War Thunder wiki</a>. Users are able to randomly retrieve a ground vehicle or start a quiz to guess the name of random vehicles.

<h4>Correct guess</h4>

![Correct](https://i.imgur.com/5VRWz04.png)

<h4>Incorrect guess</h4>

![Incorrect](https://i.imgur.com/ADVhRKU.png)

## How it works <a name = "working"></a>

There are two separate programs: a web crawler and the Discord bot.

Running the web crawler would pull all the ground vehicles' data from the wiki, including the URL of the cover image. A JSON file would be generated to store all of the data.

The Discord bot follows the <a href = "https://github.com/Rapptz/discord.py">Discord.py</a> library taking commands to do different actions. The bot mainly plays around with the ground vehicle data from the JSON file.

Created with Python 3.11.4.

## Usage <a name = "usage"></a>

Currently there are three commands.
```
$ping
```
To test whether the bot is online.

### Examples:

```
$random
```
To get a random vehicle from the wiki.

```
$guess
```
To retrieve a random vehicle image and begin guessing. After 10 seconds, the bot would show the users who got the prompt correct, along with the vehicle information.

## Getting Started <a name = "getting_started"></a>
The following is the entire process to get the bot ready. The bot is not public and cannot be invited. Do create your own bot first by following <a href = "https://discordpy.readthedocs.io/en/stable/discord.html">this guide</a>.

### Prerequisites

Clone the repo to your local machine and <a href = "https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/">create a virtual environment</a>. Then install the required APIs by running:

```
py -m pip install -r requirements.txt
```

## Running the bot <a name = "running"></a>
Run the web scraper by first entering the directory

> cd wikiscraper

Then run the command. The '-O' argument overwrites the existing JSON data file, which is what we want over the '-o' argument that appends.

> scrapy wikiTank -O tankList.json

After the scraping is done, go back to the root project folder and start the Discord bot. 

```
cd ..
py quiz-bot.py
```

## Built Using <a name = "built_using"></a>
+ [discord.py](https://github.com/Rapptz/discord.py) - Discord Wrapper

## Authors <a name = "authors"></a>
+ [@Zexiaa](https://github.com/zexiaa) - Idea & Initial work

## Acknowledgements <a name = "acknowledgement"></a>
+ README file template from [The Documentation Compendium](https://github.com/kylelobo/The-Documentation-Compendium/tree/master)
