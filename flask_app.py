# Import necessary modules
from flask import Flask, request, render_template_string, json, send_from_directory, Response, redirect
from datetime import datetime
import re
import os
import random

# Create Flask application instance
app = Flask(__name__)

# ============================================
# DATA SECTION - Anime Information (FIXED)
# ============================================

# JSON data containing all anime information with REAL data
jsons = '''
[
    {
        "id": 1,
        "title": "As a Reincarnated Aristocrat, I'll Use My Appraisal Skill",
        "season": "SEASON 2",
        "year": "2024",
        "description": "After being reincarnated as a noble, Ars Louvent uses his unique appraisal skill to find talented individuals and build his territory. In Season 2, Ars faces new challenges as his domain expands and he must navigate political intrigue while uncovering his full potential.",
        "episodes": 12,
        "image_url": "https://raw.githubusercontent.com/princehamzaytprogramming/princetoons/main/static/as-a-reincarnated-aristocrat-ill-use-my-appraisal-skill.png",
        "download_links": [
            {"name": "MEGA", "url": "https://mega.nz/file/uU5VnLyK#JbDXnXHdeNYjQBpSVTObno-OACeGqCrD7W88l6nj_YM"}
        ],
        "anime-type-tags": "season,series,funny,sad,adventure",
        "search-alternatives": "As a Reincarnated Aristocrat I'll Use My Appraisal Skill,as a reincarnated aristocrat i'll use my appraisal skill,Reincarnated Aristocrat"
    },
    {
        "id": 2,
        "title": "The Unaware Atelier Meister",
        "season": "SEASON 1",
        "year": "2024",
        "description": "In a world where magical artifacts are crafted by skilled artisans, a young boy discovers his hidden talent for creating powerful items. Follow his journey as he becomes the legendary Atelier Meister while navigating guild politics and uncovering ancient secrets.",
        "episodes": 12,
        "image_url": "https://raw.githubusercontent.com/princehamzaytprogramming/princetoons/main/static/the-unaware-atelier-meister.png",
        "download_links": [
            {"name": "MEGA", "url": "https://mega.nz/file/EMJkACjY#zDw-rwAApCv3wM-OexhqYoyHynYm-T8esQI6HqaSfIk"}
        ],
        "anime-type-tags": "season,series,fantasy,adventure",
        "search-alternatives": "The Unaware Atelier Meister,unaware atelier meister,atelier meister"
    },
    {
        "id": 3,
        "title": "How To Train Your Dragon",
        "season": "MOVIE",
        "year": "2010",
        "description": "In the Viking village of Berk, young Hiccup must prove himself as a dragon slayer. But when he befriends a dragon named Toothless, he discovers that dragons aren't what they seem. An epic adventure about friendship, courage, and changing the world.",
        "episodes": 1,
        "image_url": "https://raw.githubusercontent.com/princehamzaytprogramming/princetoons/main/static/how-to-train-your-dragon.png",
        "download_links": [
            {"name": "MEGA", "url": "https://mega.nz/#!px532BZB!JCIJ6JDZKJ52Zc-Zz9YXTohpy84_-i-mM--bmVLsA_8"}
        ],
        "anime-type-tags": "movie,adventure,funny",
        "search-alternatives": "How To Train Your Dragon,how to train your dragon,How to Train Your Dragon"
    },
    {
        "id": 4,
        "title": "Boonie Bears The Hidden Protector",
        "season": "MOVIE",
        "year": "2023",
        "description": "Join the beloved Boonie Bears in their latest adventure as they uncover a hidden protector of the forest. When mysterious events threaten their home, Briar and Bramble must team up with new allies to save their beloved forest from destruction.",
        "episodes": 1,
        "image_url": "https://raw.githubusercontent.com/princehamzaytprogramming/princetoons/main/static/boonie-bears-the-hidden-protector.png",
        "download_links": [
            {"name": "MEGA", "url": "https://mega.nz/file/OPBy0IYK#LDuffJ503peOvsRDYtY-RJ4ROkWywJZm2mtzko_qfi8"}
        ],
        "anime-type-tags": "movie,adventure,funny",
        "search-alternatives": "Boonie Bears The Hidden Protector,boonie bears hidden protector,Boonie Bears"
    },
    {
        "id": 5,
        "title": "Raya and the Last Dragon",
        "season": "MOVIE",
        "year": "2021",
        "description": "Long ago, humans and dragons lived together in harmony. But when monsters threatened the land, the dragons sacrificed themselves to save humanity. Now, warrior Raya must track down the last dragon to save her kingdom from the same evil.",
        "episodes": 1,
        "image_url": "https://raw.githubusercontent.com/princehamzaytprogramming/princetoons/main/static/raya-and-the-last-Dragon.png",
        "download_links": [
            {"name": "MEGA", "url": "https://mega.nz/file/hV9Fnb5b#GzdEooG0zYAmYMVR1PP50kauTP8GcdELFoBPZHL8tU0"}
        ],
        "anime-type-tags": "movie,adventure,fantasy",
        "search-alternatives": "Raya and the Last Dragon,raya last dragon,Raya"
    },
    {
        "id": 6,
        "title": "Minions & Monsters",
        "season": "MOVIE",
        "year": "2023",
        "description": "The adorable Minions are back in a brand new adventure! When a group of mischievous monsters threatens the world, it's up to Kevin, Stuart, and Bob to save the day. Filled with laughs, chaos, and heartwarming moments.",
        "episodes": 1,
        "image_url": "https://raw.githubusercontent.com/princehamzaytprogramming/princetoons/main/static/minions-monsters.png",
        "download_links": [
            {"name": "MEGA", "url": "https://mega.nz/file/lEgy2ZoD#JpcyaR8F6yOAY9YwkpNs67gmhbimUXIkJirjX-WcRFU"}
        ],
        "anime-type-tags": "movie,comedy,funny",
        "search-alternatives": "Minions & Monsters,minions monsters,Minions"
    },
    {
        "id": 7,
        "title": "Dragon Ball Daima",
        "season": "SEASON 1",
        "year": "2024",
        "description": "An all-new Dragon Ball series! When Goku and his friends are turned into children by a mysterious conspiracy, they must travel to a new world to find a way to return to normal. Filled with epic battles and new transformations.",
        "episodes": 20,
        "image_url": "https://raw.githubusercontent.com/princehamzaytprogramming/princetoons/main/static/dragon-ball-daima-s1.png",
        "download_links": [
            {"name": "MEGA", "url": "https://mega.nz/#!DoBlkTBK!5aYy1YVP57TN7xLoliEFFoopwCiGxl1Q40hgNbJKW3c"}
        ],
        "anime-type-tags": "season,series,action,adventure",
        "search-alternatives": "Dragon Ball Daima,dragon ball daima,DragonBall Daima"
    },
    {
        "id": 8,
        "title": "Wish Dragon",
        "season": "MOVIE",
        "year": "2021",
        "description": "A young man discovers a magical dragon that can grant wishes. Together, they embark on an unforgettable journey to find his long-lost friend. A heartwarming tale about the true meaning of wishes and friendship.",
        "episodes": 1,
        "image_url": "https://raw.githubusercontent.com/princehamzaytprogramming/princetoons/main/static/wish-dragon.png",
        "download_links": [
            {"name": "MEGA", "url": "https://mega.nz/file/F3oCDABa#67jogzWr8DvYsRZoRCXvwve2l92xuv2K1XMXMw-rlM4"}
        ],
        "anime-type-tags": "movie,adventure,fantasy",
        "search-alternatives": "Wish Dragon,wish dragon,WishDragon"
    },
    {
        "id": 9,
        "title": "Good Bye Dragon Life",
        "season": "SEASON 1",
        "year": "2024",
        "description": "After being betrayed and killed, a legendary dragon is reincarnated as a human. Now living a peaceful life in a quiet village, he must protect his new home when dark forces threaten to destroy everything he loves.",
        "episodes": 12,
        "image_url": "https://raw.githubusercontent.com/princehamzaytprogramming/princetoons/main/static/good-bye-dragon-life.png",
        "download_links": [
            {"name": "MEGA", "url": "https://mega.nz/#!h1wDWYxA!Yj_afbtSgupRLew0DItEHejWP37apCaF4tZFm2YwqXw"}
        ],
        "anime-type-tags": "season,series,fantasy,adventure",
        "search-alternatives": "Good Bye Dragon Life,good bye dragon life,Goodbye Dragon Life"
    },
    {
        "id": 10,
        "title": "GOAT",
        "season": "MOVIE",
        "year": "2024",
        "description": "A heartwarming story about an unlikely hero who must overcome his fears to save his friends. When a massive flood threatens his village, a young goat must prove that even the smallest creature can be a hero.",
        "episodes": 1,
        "image_url": "https://raw.githubusercontent.com/princehamzaytprogramming/princetoons/main/static/goat.png",
        "download_links": [
            {"name": "MEGA", "url": "https://mega.nz/file/G0QwQazC#CDYSkkK5AI-dxOiG--HH3vV6VggGRwFqFo2X9WXv0VM"}
        ],
        "anime-type-tags": "movie,comedy,funny",
        "search-alternatives": "GOAT,goat,Goat movie"
    },
    {
        "id": 11,
        "title": "Turning Red",
        "season": "MOVIE",
        "year": "2022",
        "description": "A confident 13-year-old girl struggles to balance her life as a teenager with her overprotective mother. When she gets too excited, she turns into a giant red panda. A hilarious and heartwarming coming-of-age story.",
        "episodes": 1,
        "image_url": "https://raw.githubusercontent.com/princehamzaytprogramming/princetoons/main/static/turning-red.png",
        "download_links": [
            {"name": "MEGA", "url": "https://mega.nz/file/kmRnwI6I#KbKqtMd7unCX26ajyTuk6NIbenPgGYUrftJSj5BUeLY"}
        ],
        "anime-type-tags": "movie,comedy,funny",
        "search-alternatives": "Turning Red,turning red,Disney Turning Red"
    },
    {
        "id": 12,
        "title": "NE ZHA 2",
        "season": "MOVIE",
        "year": "2025",
        "description": "The legendary demon child returns in this epic sequel! Ne Zha must face new challenges and powerful enemies while trying to protect his loved ones. With stunning animation and an emotional story, this is a must-watch.",
        "episodes": 1,
        "image_url": "https://raw.githubusercontent.com/princehamzaytprogramming/princetoons/main/static/ne-zha-2.png",
        "download_links": [
            {"name": "MEGA", "url": "https://mega.nz/file/LGphDKrT#97gjsLYzLsUlnem33FI3pPuw2PyLH1PD-kkgoZgTpI0"}
        ],
        "anime-type-tags": "movie,action,fantasy",
        "search-alternatives": "NE ZHA 2,ne zha 2,Ne Zha 2 movie"
    },
    {
        "id": 13,
        "title": "I Parry Everything",
        "season": "SEASON 1",
        "year": "2024",
        "description": "No matter what attack comes his way, this protagonist will parry it! Follow his journey as he uses his incredible defensive skills to survive in a world full of powerful enemies. Action-packed and hilarious.",
        "episodes": 12,
        "image_url": "https://raw.githubusercontent.com/princehamzaytprogramming/princetoons/main/static/i-parry-everything.png",
        "download_links": [
            {"name": "MEGA", "url": "https://mega.nz/file/rFkjnLjS#7VRAlIR9jfwUPbBQUv7uykyfVp1tuGBfafmlbud8tnA"}
        ],
        "anime-type-tags": "season,series,fantasy,action",
        "search-alternatives": "I Parry Everything,i parry everything,I Parry Everything anime"
    },
    {
        "id": 14,
        "title": "Trillion Game",
        "season": "SEASON 1",
        "year": "2024",
        "description": "Two friends with big dreams set out to make a trillion dollars. With their unique skills and unwavering determination, they navigate the cutthroat world of business and technology. A thrilling anime about ambition and friendship.",
        "episodes": 12,
        "image_url": "https://raw.githubusercontent.com/princehamzaytprogramming/princetoons/main/static/trillion-game.png",
        "download_links": [
            {"name": "MEGA", "url": "https://mega.nz/#!HIhHjZbR!Dc1ItOV7VZ3148mw43nmdOlV7uRv1QAV4zzZ3xgWfQk"}
        ],
        "anime-type-tags": "season,series,thriller,psychological",
        "search-alternatives": "Trillion Game,trillion game,Trillion Game anime"
    },
    {
        "id": 15,
        "title": "Sword Art Online",
        "season": "SEASON 1",
        "year": "2012",
        "description": "In the year 2022, thousands of players are trapped in the virtual reality game Sword Art Online. To escape, they must clear all 100 floors and defeat the final boss. But death in the game means death in real life.",
        "episodes": 25,
        "image_url": "https://raw.githubusercontent.com/princehamzaytprogramming/princetoons/main/static/sword-art-online.png",
        "download_links": [
            {"name": "MEGA", "url": "https://mega.nz/#!DUllGSia!IloFZHZkRF5qRgXEriHcVX85rqpcp5b0WeOiCEiexCU"}
        ],
        "anime-type-tags": "season,series,action,fantasy",
        "search-alternatives": "Sword Art Online,sword art online,SAO"
    },
    {
        "id": 16,
        "title": "MINIONS [2015]",
        "season": "MOVIE",
        "year": "2015",
        "description": "Before Gru, the Minions were on a quest to find the most evil master. Journey through time with Kevin, Stuart, and Bob as they search for their new boss. Hilarious adventures from the yellow creatures we all love.",
        "episodes": 1,
        "image_url": "https://raw.githubusercontent.com/princehamzaytprogramming/princetoons/main/static/minions.png",
        "download_links": [
            {"name": "MEGA", "url": "https://mega.nz/file/tQpyjRRT#b92Ur3vyZXaONTk_4ifcWG2sA29Yc3AsnbvmwoqcCGw"}
        ],
        "anime-type-tags": "movie,comedy,funny",
        "search-alternatives": "MINIONS 2015,minions 2015,Minions movie"
    },
    {
        "id": 17,
        "title": "That Time I Got Reincarnated As a Slime The Tears of The Azure Sea",
        "season": "MOVIE",
        "year": "2023",
        "description": "A special movie adventure! Rimuru Tempest and his friends travel to a mysterious land where they uncover ancient secrets. When danger threatens the Azure Sea, they must come together to protect their new allies.",
        "episodes": 1,
        "image_url": "https://raw.githubusercontent.com/princehamzaytprogramming/princetoons/main/static/that-time-i-got-reincarnated-as-a-slime-the-tears-of-the-azure-sea.png",
        "download_links": [
            {"name": "MEGA", "url": "https://mega.nz/file/0NBSzIZJ#sTnTs8_HmEGH0ERJUigNG1h1E48g2vvQ4N60_REb1-w"}
        ],
        "anime-type-tags": "movie,fantasy,adventure,reincarnation",
        "search-alternatives": "That Time I Got Reincarnated As a Slime The Tears of The Azure Sea,slime movie,reincarnated as slime movie"
    },
    {
        "id": 18,
        "title": "Demon Slayer Kimetsu no Yaiba Infinity Castle",
        "season": "MOVIE",
        "year": "2024",
        "description": "The epic conclusion of the Demon Slayer arc! Tanjiro and his allies face their greatest challenge as they enter the Infinity Castle to confront Muzan Kibutsuji. An emotional and action-packed finale to the series.",
        "episodes": 1,
        "image_url": "https://raw.githubusercontent.com/princehamzaytprogramming/princetoons/main/static/demon-slayer-kimetsu-no-yaiba-infinity-castle.png",
        "download_links": [
            {"name": "MEGA", "url": "https://mega.nz/file/jLInRBCY#XDYWCOCBi_Yqj31Eoa48Z8wOtGc8rq8351XBez5k6bE"}
        ],
        "anime-type-tags": "movie,action,fantasy,dark",
        "search-alternatives": "Demon Slayer Kimetsu no Yaiba Infinity Castle,demon slayer infinity castle,Kimetsu no Yaiba movie"
    },
    {
        "id": 19,
        "title": "Avatar Aang The Last Airbender",
        "season": "MOVIE",
        "year": "2026",
        "description": "Join Aang and his friends in this new animated adventure! Set in the world of Avatar, this movie explores the early days of Team Avatar as they face new threats and learn the true meaning of balance and harmony.",
        "episodes": 1,
        "image_url": "https://raw.githubusercontent.com/princehamzaytprogramming/princetoons/main/static/avatar-aang-the-last-airbender.png",
        "download_links": [
            {"name": "MEGA", "url": "https://mega.nz/file/zXJziSJA#_ANd8oUDoszSfnU9UhYTKxEXYjSR3JWfpz-rj96ItdE"}
        ],
        "anime-type-tags": "movie,adventure,action,fantasy",
        "search-alternatives": "Avatar Aang The Last Airbender,avatar the last airbender,Aang movie"
    },
    {
        "id": 20,
        "title": "ENCANTO",
        "season": "MOVIE",
        "year": "2021",
        "description": "The magical Madrigal family lives in the mountains of Colombia. Each member has a unique gift, except for Mirabel. When the family's magic begins to fade, she must discover what makes her special and save her home.",
        "episodes": 1,
        "image_url": "https://raw.githubusercontent.com/princehamzaytprogramming/princetoons/main/static/encanto.png",
        "download_links": [
            {"name": "MEGA", "url": "https://mega.nz/file/cu4SXSoB#eJI5yN5Urg5PJT6p72BLgzHYpy2diQ4hDeBUopaFS1E"}
        ],
        "anime-type-tags": "movie,comedy,musical,fantasy",
        "search-alternatives": "ENCANTO,encanto,Disney Encanto"
    },
    {
        "id": 21,
        "title": "LUCA",
        "season": "MOVIE",
        "year": "2021",
        "description": "Set on the beautiful Italian Riviera, this is a heartwarming coming-of-age story about a young sea monster who discovers a magical world above the surface. Friendship, adventure, and pasta-filled fun!",
        "episodes": 1,
        "image_url": "https://raw.githubusercontent.com/princehamzaytprogramming/princetoons/main/static/luca.png",
        "download_links": [
            {"name": "MEGA", "url": "https://mega.nz/file/9rwVCSyZ#cMreg3rk_rFNeOSaNRF4kYMDNkuWI8rYD16cfa4XjWo"}
        ],
        "anime-type-tags": "movie,comedy,adventure,family",
        "search-alternatives": "LUCA,luca,Pixar Luca"
    },
    {
        "id": 22,
        "title": "The Boss Baby Family Business",
        "season": "MOVIE",
        "year": "2021",
        "description": "The Templeton brothers have grown up, but they're drawn back together when the Boss Baby returns with a new mission. Team up with Tim and his brother as they navigate family and business in this hilarious sequel.",
        "episodes": 1,
        "image_url": "https://raw.githubusercontent.com/princehamzaytprogramming/princetoons/main/static/the-boss-baby-family-business.png",
        "download_links": [
            {"name": "MEGA", "url": "https://mega.nz/file/MV0DjYLL#AgtV5KElpyhePPPU-IJ5pXsq02C1veTSpDp2lspOSQc"}
        ],
        "anime-type-tags": "movie,comedy,family,funny",
        "search-alternatives": "The Boss Baby Family Business,boss baby 2,boss baby family business"
    },
    {
        "id": 23,
        "title": "INCREDIBLES 2",
        "season": "MOVIE",
        "year": "2018",
        "description": "The Parr family is back! Elastigirl takes on the spotlight while Mr. Incredible stays home to care for the kids. When a new villain emerges, the entire family must work together to save the world once again.",
        "episodes": 1,
        "image_url": "https://raw.githubusercontent.com/princehamzaytprogramming/princetoons/main/static/incredibles-2.png",
        "download_links": [
            {"name": "MEGA", "url": "https://mega.nz/file/9roiVAwD#jxbKzmSEiLW-uoxiuMUdIihKCLXTZsDO5NHCvqrvR_8"}
        ],
        "anime-type-tags": "movie,action,comedy,family",
        "search-alternatives": "INCREDIBLES 2,incredibles 2,Disney Incredibles 2"
    },
    {
        "id": 24,
        "title": "THE INCREDIBLES",
        "season": "MOVIE",
        "year": "2004",
        "description": "In a world where superheroes have been banned, a family of former heroes must come out of retirement to save the world. This action-packed animated film is a classic tale of family, courage, and doing what's right.",
        "episodes": 1,
        "image_url": "https://raw.githubusercontent.com/princehamzaytprogramming/princetoons/main/static/the-incredibles.png",
        "download_links": [
            {"name": "MEGA", "url": "https://mega.nz/file/t75WyJ7C#BT8gn-GnuqtEnaK1_--7665Q20b5yj0Zr-V88A0586Y"}
        ],
        "anime-type-tags": "movie,action,comedy,family",
        "search-alternatives": "THE INCREDIBLES,the incredibles,Disney Incredibles"
    },
    {
        "id": 25,
        "title": "HOPPERS",
        "season": "MOVIE",
        "year": "2022",
        "description": "A young boy discovers a magical world of talking grasshoppers who need his help. With his new friends, he goes on an adventure to save their home from destruction. A heartwarming tale of friendship and courage.",
        "episodes": 1,
        "image_url": "https://raw.githubusercontent.com/princehamzaytprogramming/princetoons/main/static/hoppers.png",
        "download_links": [
            {"name": "MEGA", "url": "https://mega.nz/file/DmZ3ASaB#ZZO_9d2BSyvk0nvs1bSVeLvmGma8HR4Hz9tyawzQntU"}
        ],
        "anime-type-tags": "movie,comedy,family",
        "search-alternatives": "HOPPERS,hoppers,Hopper movie"
    },
    {
        "id": 26,
        "title": "Spider Man Into the Spider Verse",
        "season": "MOVIE",
        "year": "2018",
        "description": "Teenager Miles Morales becomes the Spider-Man of his dimension. When a multiverse threat emerges, he must team up with Spider-Men from other dimensions to save reality. A visually stunning and emotional masterpiece.",
        "episodes": 1,
        "image_url": "https://raw.githubusercontent.com/princehamzaytprogramming/princetoons/main/static/spider-man-into-the-spider-verse.png",
        "download_links": [
            {"name": "MEGA", "url": "https://mega.nz/file/4QliRCCK#sMx7AhVXMHmCPP6cWDg2_DgZLGFVQxD_gxM4JPr_E9s"}
        ],
        "anime-type-tags": "movie,action,adventure,fantasy",
        "search-alternatives": "Spider Man Into the Spider Verse,spider man into the spider verse,spiderverse"
    },
    {
        "id": 27,
        "title": "Attack on Titan",
        "season": "SEASON 1",
        "year": "2013",
        "description": "In a world where humanity lives inside walls to survive from giant humanoid creatures called Titans, Eren Yeager swears to exterminate them after his mother is killed. An epic tale of survival, revenge, and the dark secrets of the world.",
        "episodes": 25,
        "image_url": "https://raw.githubusercontent.com/princehamzaytprogramming/princetoons/main/static/aot-s1.png",
        "download_links": [
            {"name": "MEGA", "url": "https://mega.nz/#!B94kDRaQ!RsAOoDmCLB48aR1bTzd7hWwQM0kXgo8MjJsWqqnGgaI"}
        ],
        "anime-type-tags": "season,series,action,dark,psychological",
        "search-alternatives": "Attack on Titan,attack on titan,AOT season 1"
    },
    {
        "id": 28,
        "title": "Attack on Titan",
        "season": "SEASON 2",
        "year": "2017",
        "description": "The mystery deepens as Eren and his friends discover more about the Titans and their own abilities. With new enemies appearing and old allies becoming suspicious, the fight for survival becomes more complicated.",
        "episodes": 12,
        "image_url": "https://raw.githubusercontent.com/princehamzaytprogramming/princetoons/main/static/aot-s2.png",
        "download_links": [
            {"name": "MEGA", "url": "https://mega.nz/file/XUBBARyA#Yv7yH_KwiQZIEpCHUoLcMzcp7D5_uq7anLa1gZuzTd8"}
        ],
        "anime-type-tags": "season,series,action,dark,psychological",
        "search-alternatives": "Attack on Titan,attack on titan,AOT season 2"
    },
    {
        "id": 29,
        "title": "Attack on Titan",
        "season": "SEASON 3",
        "year": "2018",
        "description": "The fight against the Titans intensifies as Eren and his friends uncover the truth about the world outside the walls. With political conspiracies and huge revelations, this season changes everything we thought we knew.",
        "episodes": 22,
        "image_url": "https://raw.githubusercontent.com/princehamzaytprogramming/princetoons/main/static/aot-s3.png",
        "download_links": [
            {"name": "MEGA", "url": "https://mega.nz/#!EtxyiKaa!Ft4fXpotFNFF-gSFzErVO9tAzEUzacjwyuh3dL_DRsw"}
        ],
        "anime-type-tags": "season,series,action,dark,psychological",
        "search-alternatives": "Attack on Titan,attack on titan,AOT season 3"
    },
    {
        "id": 30,
        "title": "Attack on Titan",
        "season": "SEASON 4",
        "year": "2020",
        "description": "The final season! Eren leads the fight against the world as the truth about the Titans is finally revealed. A dark, emotional, and breathtaking conclusion to one of the greatest anime of all time.",
        "episodes": 28,
        "image_url": "https://raw.githubusercontent.com/princehamzaytprogramming/princetoons/main/static/aot-s4.png",
        "download_links": [
            {"name": "MEGA", "url": "https://mega.nz/#!OxAzHLzS!w37T8e5YkUiTfxJpBnWSEhu132WVVmvVEAEYi4sjJ9Y"}
        ],
        "anime-type-tags": "season,series,action,dark,psychological",
        "search-alternatives": "Attack on Titan,attack on titan,AOT season 4"
    },
    {
        "id": 31,
        "title": "The Super Mario Galaxy",
        "season": "MOVIE",
        "year": "2023",
        "description": "Mario and Luigi embark on a cosmic adventure to save Princess Peach from Bowser's latest scheme. Journey through space, discover new planets, and experience the magic of the Mushroom Kingdom like never before.",
        "episodes": 1,
        "image_url": "https://raw.githubusercontent.com/princehamzaytprogramming/princetoons/main/static/the-super-mario-galaxy.png",
        "download_links": [
            {"name": "MEGA", "url": "https://mega.nz/file/fjAW0AQa#6NUEiPlOrSEwtO7ZkmArrABbt7TCPmlS8ObMZWC1IRU"}
        ],
        "anime-type-tags": "movie,adventure,comedy,family",
        "search-alternatives": "The Super Mario Galaxy,super mario galaxy,mario movie"
    },
    {
        "id": 32,
        "title": "SCARLET",
        "season": "MOVIE",
        "year": "2023",
        "description": "A mysterious woman with incredible powers is hunted by a secret organization. As she uncovers the truth about her past, she must decide whether to run or fight back. An action-packed thriller with heart.",
        "episodes": 1,
        "image_url": "https://raw.githubusercontent.com/princehamzaytprogramming/princetoons/main/static/scarlet.png",
        "download_links": [
            {"name": "MEGA", "url": "https://mega.nz/file/78QnEaBK#eEIeVeHCMpXJHI-FGad97B0QvTOa6_r35B8wc-0R9kE"}
        ],
        "anime-type-tags": "movie,drama,action",
        "search-alternatives": "SCARLET,scarlet,Scarlet movie"
    },
    {
        "id": 33,
        "title": "ZOOTOPIA",
        "season": "MOVIE",
        "year": "2016",
        "description": "In a world where animals live together in harmony, a rabbit police officer must team up with a con-artist fox to solve a mysterious case. A brilliant film about prejudice, dreams, and working together.",
        "episodes": 1,
        "image_url": "https://raw.githubusercontent.com/princehamzaytprogramming/princetoons/main/static/zootopia-2.png",
        "download_links": [
            {"name": "MEGA", "url": "https://mega.nz/file/qlJCXBaR#cYzI-qNIUPKyEPk2YvMZttbLD-e3oz5laWTKgvYU4vk"}
        ],
        "anime-type-tags": "movie,comedy,adventure,family",
        "search-alternatives": "ZOOTOPIA,zootopia,Disney Zootopia"
    },
    {
        "id": 34,
        "title": "Lupin The 3Rd Vs Cats Eye",
        "season": "MOVIE",
        "year": "2023",
        "description": "The legendary thief Lupin III faces off against the famous Cats Eye team! In this crossover, both groups compete for the same treasure. Filled with heists, comedy, and stunning animation.",
        "episodes": 1,
        "image_url": "https://raw.githubusercontent.com/princehamzaytprogramming/princetoons/main/static/lupin-the-3rd-vs-cats-eye.png",
        "download_links": [
            {"name": "MEGA", "url": "https://mega.nz/file/e8QkAbxL#Sj9aNRJzpM5ah9u7cO0U-JJTyq8XUaKqyIcFYUgfI2M"}
        ],
        "anime-type-tags": "movie,action,adventure,mystery",
        "search-alternatives": "Lupin The 3Rd Vs Cats Eye,lupin vs cat's eye,Lupin III"
    },
    {
        "id": 35,
        "title": "To Be Hero X",
        "season": "SEASON 1",
        "year": "2025",
        "description": "A brand new hero rises in a world where superheroes are the new celebrities. Follow his journey as he discovers his powers, makes allies, and fights against a villain who threatens everything he holds dear.",
        "episodes": 12,
        "image_url": "https://raw.githubusercontent.com/princehamzaytprogramming/princetoons/main/static/to-be-hero-x.png",
        "download_links": [
            {"name": "PIXELDRAIN", "url": "https://pixeldrain.net/u/JHeYtejf?download"}
        ],
        "anime-type-tags": "season,series,action,fantasy,superhero",
        "search-alternatives": "To Be Hero X,to be hero x,ToBeHeroX"
    },
    {
        "id": 36,
        "title": "Spy X Family",
        "season": "SEASON 3",
        "year": "2025",
        "description": "The Forger family is back for more spy missions! Loid, Yor, and Anya navigate their double lives with hilarious results. A perfect blend of action, comedy, and heartwarming family moments.",
        "episodes": 12,
        "image_url": "https://raw.githubusercontent.com/princehamzaytprogramming/princetoons/main/static/spy-x-family-season-3.png",
        "download_links": [
            {"name": "PIXELDRAIN", "url": "https://pixeldrain.net/u/nZipGSvb?download"}
        ],
        "anime-type-tags": "season,series,comedy,action,family",
        "search-alternatives": "Spy X Family,spy x family,SpyXFamily season 3"
    },
    {
        "id": 37,
        "title": "BLUE LOCK",
        "season": "SEASON 1",
        "year": "2022",
        "description": "A controversial project aims to create the world's best striker. 300 young players compete in a brutal survival program where only the best will succeed. A thrilling sports anime with intense psychological battles.",
        "episodes": 24,
        "image_url": "https://raw.githubusercontent.com/princehamzaytprogramming/princetoons/main/static/blue-lock-season-1.png",
        "download_links": [
            {"name": "CLOUD HUB", "url": "https://hubcloud.cx/drive/vs91pzg73ziguin"}
        ],
        "anime-type-tags": "season,series,sports,action,psychological",
        "search-alternatives": "BLUE LOCK,blue lock,Blue Lock season 1"
    },
    {
        "id": 38,
        "title": "Blue Lock Episode Nagi",
        "season": "MOVIE",
        "year": "2024",
        "description": "A movie focusing on Nagi Seishiro, one of the most talented players in Blue Lock. Follow his journey from a lazy genius to a passionate striker who discovers the true meaning of football.",
        "episodes": 1,
        "image_url": "https://raw.githubusercontent.com/princehamzaytprogramming/princetoons/main/static/blue-lock-episode-nagi.png",
        "download_links": [
            {"name": "MEGA", "url": "https://mega.nz/#!HwIlTRaB!zRgBy_aT1uutqnmDFPAjfAkjiH4pc-tLUAKjUZ9C1nk"}
        ],
        "anime-type-tags": "movie,sports,action,psychological",
        "search-alternatives": "Blue Lock Episode Nagi,blue lock movie,episode nagi"
    },
    {
        "id": 39,
        "title": "BLUE LOCK",
        "season": "SEASON 2",
        "year": "2024",
        "description": "The Blue Lock project continues as the competition becomes more intense. New players, new challenges, and even higher stakes. Who will emerge as the world's greatest striker?",
        "episodes": 14,
        "image_url": "https://raw.githubusercontent.com/princehamzaytprogramming/princetoons/main/static/blue-lock-season-2.png",
        "download_links": [
            {"name": "MEGA", "url": "https://mega.nz/#!2QZk0RbY!Ut02y0WckrhmUzCfaXPpzdRnvDAxbRS8lewb_qHM7qA"}
        ],
        "anime-type-tags": "season,series,sports,action,psychological",
        "search-alternatives": "BLUE LOCK,blue lock,Blue Lock season 2"
    },
    {
        "id": 40,
        "title": "Lord Of Mysteries",
        "season": "SEASON 1",
        "year": "2025",
        "description": "In a world of mysteries and supernatural powers, a young man awakens as a Beyonder. Follow his journey as he uncovers the secrets of the world and climbs the ranks of the mysterious organizations.",
        "episodes": 12,
        "image_url": "https://raw.githubusercontent.com/princehamzaytprogramming/princetoons/main/static/lord-of-mysteries-season-1.png",
        "download_links": [
            {"name": "PIXELDRAIN", "url": "https://pixeldrain.net/u/VfmJsKh1?download"}
        ],
        "anime-type-tags": "season,series,mystery,fantasy,psychological",
        "search-alternatives": "Lord Of Mysteries,lord of mysteries,LordOfMysteries"
    },
    {
        "id": 41,
        "title": "The Rising Of The Shield Hero",
        "season": "SEASON 1",
        "year": "2019",
        "description": "A young man is summoned to another world as the Shield Hero, only to be betrayed and framed. Alone and despised, he must rise from the ashes and become the hero the world needs. A powerful story of redemption.",
        "episodes": 25,
        "image_url": "https://raw.githubusercontent.com/princehamzaytprogramming/princetoons/main/static/the-rising-of-the-shield-hero-season-1.png",
        "download_links": [
            {"name": "PIXELDRAIN", "url": "https://pixeldrain.net/u/q1LBqDfQ?download"},
            {"name": "CLOUD HUB", "url": "https://hubcloud.cx/drive/8k0nv89kppdk409"}
        ],
        "anime-type-tags": "season,series,action,adventure,reincarnation",
        "search-alternatives": "The Rising Of The Shield Hero,shield hero,shield hero season 1"
    },
    {
        "id": 42,
        "title": "The Rising Of The Shield Hero",
        "season": "SEASON 2",
        "year": "2022",
        "description": "Naofumi continues his journey as the Shield Hero. With new allies and enemies, he must face even greater challenges. This season expands the world and introduces new threats that push him to his limits.",
        "episodes": 13,
        "image_url": "https://raw.githubusercontent.com/princehamzaytprogramming/princetoons/main/static/the-rising-of-the-shield-hero-season-2.png",
        "download_links": [
            {"name": "PIXELDRAIN", "url": "https://pixeldrain.net/u/ao52VMFU?download"},
            {"name": "CLOUD HUB", "url": "https://hubcloud.cx/drive/gvwygqyxzhvbese"}
        ],
        "anime-type-tags": "season,series,action,adventure,reincarnation",
        "search-alternatives": "The Rising Of The Shield Hero,shield hero,shield hero season 2"
    },
    {
        "id": 43,
        "title": "The Rising Of The Shield Hero",
        "season": "SEASON 3",
        "year": "2023",
        "description": "The battle intensifies as Naofumi faces his greatest enemy yet. With the world hanging in the balance, he must unite the other heroes and fight for the survival of all. An epic continuation of the Shield Hero saga.",
        "episodes": 12,
        "image_url": "https://raw.githubusercontent.com/princehamzaytprogramming/princetoons/main/static/the-rising-of-the-shield-hero-season-3.png",
        "download_links": [
            {"name": "PIXELDRAIN", "url": "https://pixeldrain.net/u/RPuJwvYa?download"}
        ],
        "anime-type-tags": "season,series,action,adventure,reincarnation",
        "search-alternatives": "The Rising Of The Shield Hero,shield hero,shield hero season 3"
    },
    {
        "id": 44,
        "title": "The Rising Of The Shield Hero",
        "season": "SEASON 4",
        "year": "2025",
        "description": "The final season! Naofumi and his friends face the ultimate challenge as they confront the true enemy behind all their struggles. A satisfying conclusion to one of the most popular isekai anime.",
        "episodes": 12,
        "image_url": "https://raw.githubusercontent.com/princehamzaytprogramming/princetoons/main/static/the-rising-of-the-shield-hero-season-4.png",
        "download_links": [
            {"name": "PIXELDRAIN", "url": "https://pixeldrain.net/u/DtwFeGGV?download"}
        ],
        "anime-type-tags": "season,series,action,adventure,reincarnation",
        "search-alternatives": "The Rising Of The Shield Hero,shield hero,shield hero season 4"
    },
    {
        "id": 45,
        "title": "Wistoria Wand And Sword",
        "season": "SEASON 1",
        "year": "2024",
        "description": "In a world where magic and swordplay coexist, a young man with no magical talent must rely on his sword skills to survive. His journey to become the legendary Wistoria is filled with danger and discovery.",
        "episodes": 12,
        "image_url": "https://raw.githubusercontent.com/princehamzaytprogramming/princetoons/main/static/wistoria-wand-and-sword-season-1.png",
        "download_links": [
            {"name": "PIXELDRAIN", "url": "https://pixeldrain.net/u/y3q1JK2f?download"}
        ],
        "anime-type-tags": "season,series,fantasy,action,adventure",
        "search-alternatives": "Wistoria Wand And Sword,wistoria wand and sword,Wistoria season 1"
    },
    {
        "id": 46,
        "title": "Wistoria Wand And Sword",
        "season": "SEASON 2",
        "year": "2025",
        "description": "The adventures continue as our hero faces new challenges in his quest to master both wand and sword. With new allies and powerful enemies, the path to becoming Wistoria becomes even more dangerous.",
        "episodes": 12,
        "image_url": "https://raw.githubusercontent.com/princehamzaytprogramming/princetoons/main/static/wistoria-wand-and-sword-season-2.png",
        "download_links": [
            {"name": "PIXELDRAIN", "url": "https://pixeldrain.net/u/nGPiJN4w?download"}
        ],
        "anime-type-tags": "season,series,fantasy,action,adventure",
        "search-alternatives": "Wistoria Wand And Sword,wistoria wand and sword,Wistoria season 2"
    },
    {
        "id": 47,
        "title": "Vinland Saga",
        "season": "SEASON 1",
        "year": "2019",
        "description": "A young Viking named Thorfinn seeks revenge against the man who killed his father. As he navigates the brutal world of Vikings and warriors, he learns that true strength comes not from revenge but from understanding.",
        "episodes": 24,
        "image_url": "https://raw.githubusercontent.com/princehamzaytprogramming/princetoons/main/static/vinland-saga-season-1.png",
        "download_links": [
            {"name": "PIXELDRAIN", "url": "https://pixeldrain.net/u/4UHEaXzR?download"},
            {"name": "MEGA", "url": "https://mega.nz/#!RSd2DRhI!4wx9wqTdg67I4KCY8g5yaXZlLAEoSk3HQAfDGgeG5jo"}
        ],
        "anime-type-tags": "season,series,action,adventure,historical",
        "search-alternatives": "Vinland Saga,vinland saga,VinlandSaga season 1"
    },
    {
        "id": 48,
        "title": "Vinland Saga",
        "season": "SEASON 2",
        "year": "2023",
        "description": "Thorfinn's journey continues as he seeks a new purpose beyond revenge. A story about redemption, peace, and finding meaning in a world torn apart by violence. A masterpiece of storytelling.",
        "episodes": 24,
        "image_url": "https://raw.githubusercontent.com/princehamzaytprogramming/princetoons/main/static/vinland-saga-season-2.png",
        "download_links": [
            {"name": "PIXELDRAIN", "url": "https://pixeldrain.net/u/iHYoUykv?download"},
            {"name": "MEGA", "url": "https://mega.nz/#!IW8jnKCT!Uo6JsqG-8jbGW14nKIZZ2fXyUSoj_8upArQzlQuqzhU"}
        ],
        "anime-type-tags": "season,series,action,adventure,historical",
        "search-alternatives": "Vinland Saga,vinland saga,VinlandSaga season 2"
    },
    {
        "id": 49,
        "title": "Mob Psycho 100",
        "season": "SEASON 1",
        "year": "2016",
        "description": "A young boy with immense psychic powers just wants to live a normal life. But when his emotions reach 100%, his power goes out of control. A hilarious and heartwarming story about self-acceptance and friendship.",
        "episodes": 12,
        "image_url": "https://raw.githubusercontent.com/princehamzaytprogramming/princetoons/main/static/mob-psycho-100-season-1.png",
        "download_links": [
            {"name": "PIXELDRAIN", "url": "https://pixeldrain.net/u/isjpVipf?download"},
            {"name": "CLOUD HUB", "url": "https://hubcloud.cx/drive/xbwmtl5w0avm1j5"}
        ],
        "anime-type-tags": "season,series,action,comedy,supernatural",
        "search-alternatives": "Mob Psycho 100,mob psycho 100,MobPsycho100 season 1"
    },
    {
        "id": 50,
        "title": "Mob Psycho 100",
        "season": "SEASON 2",
        "year": "2019",
        "description": "Mob's journey continues as he faces new challenges and learns more about himself. With incredible animation and deep emotional moments, this season takes the story to new heights.",
        "episodes": 13,
        "image_url": "https://raw.githubusercontent.com/princehamzaytprogramming/princetoons/main/static/mob-psycho-100-season-2.png",
        "download_links": [
            {"name": "PIXELDRAIN", "url": "https://pixeldrain.net/u/jeCxP7vF?download"},
            {"name": "CLOUD HUB", "url": "https://hubcloud.cx/drive/wbdt7ixtj8oebcu"}
        ],
        "anime-type-tags": "season,series,action,comedy,supernatural",
        "search-alternatives": "Mob Psycho 100,mob psycho 100,MobPsycho100 season 2"
    },
    {
        "id": 51,
        "title": "Akudama Drive",
        "season": "SEASON 1",
        "year": "2020",
        "description": "A group of dangerous criminals are forced to work together on a suicide mission. Filled with cyberpunk aesthetics, intense action, and shocking twists, this anime is a wild ride from start to finish.",
        "episodes": 12,
        "image_url": "https://raw.githubusercontent.com/princehamzaytprogramming/princetoons/main/static/akudama-drive-season-1.png",
        "download_links": [
            {"name": "PIXELDRAIN", "url": "https://pixeldrain.net/u/rkYebPUL?download"},
            {"name": "CLOUD HUB", "url": "https://hubcloud.cx/drive/ctzi1s98f9l2fvi"}
        ],
        "anime-type-tags": "season,series,action,sci-fi,cyberpunk",
        "search-alternatives": "Akudama Drive,akudama drive,AkudamaDrive"
    },
    {
        "id": 52,
        "title": "Liar Game",
        "season": "SEASON 1 EP 1-12",
        "year": "2007",
        "description": "A naive college student gets caught up in a deadly game where players must deceive each other to win. With her wits and the help of a genius con artist, she must survive the Liar Game and its psychological challenges.",
        "episodes": 12,
        "image_url": "https://raw.githubusercontent.com/princehamzaytprogramming/princetoons/main/static/liar-game-season-1.png",
        "download_links": [
            {"name": "PIXELDRAIN", "url": "https://pixeldrain.net/u/UEDMXbK4?download"},
            {"name": "CLOUD HUB", "url": "https://hubcloud.cx/drive/zpuzuua6ctuzu0p"}
        ],
        "anime-type-tags": "season,series,psychological,thriller,game",
        "search-alternatives": "Liar Game,liar game,LiarGame"
    },
    {
        "id": 53,
        "title": "Mushoku Tensei: Jobless Reincarnation",
        "season": "SEASON 1",
        "year": "2021",
        "description": "A 34-year-old NEET dies and is reincarnated as a baby in a magical world. With memories of his past life intact, he vows to live this new life to the fullest. A deep, emotional, and beautifully animated story.",
        "episodes": 23,
        "image_url": "https://raw.githubusercontent.com/princehamzaytprogramming/princetoons/main/static/mushoku-tensei-jobless-reincarnation-season-1.png",
        "download_links": [
            {"name": "PIXELDRAIN", "url": "https://pixeldrain.net/u/S2Qzhsds?download"},
            {"name": "MEGA", "url": "https://mega.nz/#!cOFThJob!7kdMxSvF8W78l-LoYmbJmiqRfSTWDeJEkM_D5Re7hW0"}
        ],
        "anime-type-tags": "season,series,fantasy,reincarnation,adventure",
        "search-alternatives": "Mushoku Tensei Jobless Reincarnation,mushoku tensei,Jobless Reincarnation season 1"
    },
    {
        "id": 54,
        "title": "Mushoku Tensei: Jobless Reincarnation",
        "season": "SEASON 2",
        "year": "2023",
        "description": "Rudeus continues his journey in the magical world. With new challenges and deeper emotional moments, this season explores his relationships and his growth as a person. A must-watch for fans of the series.",
        "episodes": 24,
        "image_url": "https://raw.githubusercontent.com/princehamzaytprogramming/princetoons/main/static/mushoku-tensei-jobless-reincarnation-season-2.png",
        "download_links": [
            {"name": "PIXELDRAIN", "url": "https://pixeldrain.net/u/DVgQpMBU?download"},
            {"name": "GO FILE", "url": "https://gofile.io/d/43PAIj"}
        ],
        "anime-type-tags": "season,series,fantasy,reincarnation,adventure",
        "search-alternatives": "Mushoku Tensei Jobless Reincarnation,mushoku tensei,Jobless Reincarnation season 2"
    },
    {
        "id": 55,
        "title": "Sword Art Online",
        "season": "SEASON 2",
        "year": "2014",
        "description": "Kirito is back in a new virtual world! This season explores new game worlds, new challenges, and deeper emotional moments. A continuation of the beloved SAO series with even more action and romance.",
        "episodes": 24,
        "image_url": "https://raw.githubusercontent.com/princehamzaytprogramming/princetoons/main/static/sword-art-online-season-2.png",
        "download_links": [
            {"name": "MEGA", "url": "https://mega.nz/file/qdZ2wDSA#AxS__hQvk-fCocuS-OshFpBTOHdPIGXLKuAB7z6eiIQ"},
            {"name": "MEDIA FIRE", "url": "https://www.mediafire.com/file/htg36o3se7ykb4k/S2_-_SAO_in_Hindi_%255BRare_Animes%255D.zip/file"}
        ],
        "anime-type-tags": "season,series,action,fantasy,sci-fi",
        "search-alternatives": "Sword Art Online,sword art online,SAO season 2"
    },
    {
        "id": 56,
        "title": "Jack of All Trades, Party of None",
        "season": "SEASON 1",
        "year": "2024",
        "description": "A young man with no special talents is branded as useless. But when he discovers the power of versatility, he proves that being a jack of all trades can actually be the greatest strength of all.",
        "episodes": 12,
        "image_url": "https://raw.githubusercontent.com/princehamzaytprogramming/princetoons/main/static/jack-of-all-trades-party-of-none-season-1.png",
        "download_links": [
            {"name": "PIXELDRAIN", "url": "https://pixeldrain.net/u/RXo5MRLW?download"},
            {"name": "CLOUD HUB", "url": "https://hubcloud.cx/drive/wg44coa1paimfwi"}
        ],
        "anime-type-tags": "season,series,fantasy,adventure,comedy",
        "search-alternatives": "Jack of All Trades Party of None,jack of all trades,Party of None"
    },
    {
        "id": 57,
        "title": "Re:ZERO -Starting Life in Another World",
        "season": "SEASON 1",
        "year": "2016",
        "description": "A young man is summoned to a fantasy world and discovers he has the power to return from death. He uses this power to save the people he loves, but every death leaves emotional scars. A masterpiece of psychological storytelling.",
        "episodes": 25,
        "image_url": "https://raw.githubusercontent.com/princehamzaytprogramming/princetoons/main/static/re-zero-season-1.png",
        "download_links": [
            {"name": "MEGA", "url": "https://mega.nz/file/6B5RhKYS#ukqJtj1T-ZDY6xS2ZRf0d8MEDKLrYimLbWMzmu6Q8Co"},
            {"name": "PIXELDRAIN", "url": "https://pixeldrain.net/u/92vLJpcb?download"},
            {"name": "MEDIA FIRE", "url": "https://www.mediafire.com/file/eg77kbqpvezxc5i/Re+ZERO+Starting+Life+in+Another+World+S01+[RareToonsIndia].zip/file"}
        ],
        "anime-type-tags": "season,series,psychological,fantasy,reincarnation",
        "search-alternatives": "Re ZERO Starting Life in Another World,re zero,ReZero season 1"
    },
    {
        "id": 58,
        "title": "Re:ZERO -Starting Life in Another World",
        "season": "SEASON 2",
        "year": "2020",
        "description": "Subaru's struggles continue as he faces new challenges and even greater emotional pain. This season explores the depths of his character and the true cost of his ability. A powerful and heartbreaking continuation.",
        "episodes": 25,
        "image_url": "https://raw.githubusercontent.com/princehamzaytprogramming/princetoons/main/static/re-zero-season-2.png",
        "download_links": [
            {"name": "MEGA", "url": "https://mega.nz/#!2A8GmS6L!RXk7SoT5UhSADf6NJPjpyBdufnXSxMdRT6drAc_MUhE"},
            {"name": "PIXELDRAIN", "url": "https://pixeldrain.net/u/TGYf1sk9?download"},
            {"name": "MEDIA FIRE", "url": "https://www.mediafire.com/file/09m5y87dzsfi0eh/Re+ZERO+Starting+Life+in+Another+World+S02+[RareToonsIndia].zip/file"}
        ],
        "anime-type-tags": "season,series,psychological,fantasy,reincarnation",
        "search-alternatives": "Re ZERO Starting Life in Another World,re zero,ReZero season 2"
    },
    {
        "id": 59,
        "title": "Re:ZERO -Starting Life in Another World",
        "season": "SEASON 3",
        "year": "2024",
        "description": "The stakes are higher than ever as Subaru faces his most dangerous challenges yet. With new allies and terrible enemies, he must find a way to save everyone without losing himself. An epic season of the acclaimed series.",
        "episodes": 16,
        "image_url": "https://raw.githubusercontent.com/princehamzaytprogramming/princetoons/main/static/re-zero-season-3.png",
        "download_links": [
            {"name": "MEGA", "url": "https://mega.nz/#!PRYn1R5A!QU5Jhp5oivdUMd-m8BwF9ZCfajWH0DAky0nbfps7F0Y"},
            {"name": "PIXELDRAIN", "url": "https://pixeldrain.net/u/xE8u2x32?download"},
            {"name": "MEDIA FIRE", "url": "https://www.mediafire.com/file/em7cz7toq2ldlvs/Re+ZERO+Starting+Life+in+Another+World+S03+[RareToonsIndia].zip/file"}
        ],
        "anime-type-tags": "season,series,psychological,fantasy,reincarnation",
        "search-alternatives": "Re ZERO Starting Life in Another World,re zero,ReZero season 3"
    },
    {
        "id": 60,
        "title": "Re:ZERO -Starting Life in Another World",
        "season": "SEASON 4 PART-1 EP-1-11",
        "year": "2025",
        "description": "The next chapter of Subaru's epic journey begins! New mysteries, new challenges, and the same heartbreaking choices that made Re:ZERO a masterpiece. A must-watch for all fans of the series.",
        "episodes": 11,
        "image_url": "https://raw.githubusercontent.com/princehamzaytprogramming/princetoons/main/static/re-zero-season-4.png",
        "download_links": [
            {"name": "CLOUD HUB", "url": "https://hubcloud.cx/drive/owqmgq42q24m4y3"},
            {"name": "PIXELDRAIN", "url": "https://pixeldrain.net/u/BGWUjJaE?download"}
        ],
        "anime-type-tags": "season,series,psychological,fantasy,reincarnation",
        "search-alternatives": "Re ZERO Starting Life in Another World,re zero,ReZero season 4"
    },
    {
        "id": 61,
        "title": "That Time I Got Reincarnated as a Slime",
        "season": "SEASON 1",
        "year": "2018",
        "description": "A salaryman is reincarnated as a slime in a fantasy world. With his unique abilities and a helpful dragon friend, he builds a nation where all races can live together in harmony. A feel-good anime about friendship and unity.",
        "episodes": 24,
        "image_url": "https://raw.githubusercontent.com/princehamzaytprogramming/princetoons/main/static/slim-season-1.png",
        "download_links": [
            {"name": "MEGA", "url": "https://mega.nz/#!ZbcBTYKa!nzi_TLbgK9R02o5g9ASTk2icNCd0J9Q_Iw4jiHrkpyQ"},
            {"name": "PIXELDRAIN", "url": "https://pixeldrain.net/u/mpq6WAwT?download"},
            {"name": "GO FILE", "url": "https://gofile.io/d/OIU85P"}
        ],
        "anime-type-tags": "season,series,fantasy,reincarnation,adventure",
        "search-alternatives": "That Time I Got Reincarnated as a Slime,tensei slime,Slime season 1"
    },
    {
        "id": 62,
        "title": "That Time I Got Reincarnated as a Slime",
        "season": "SEASON 2",
        "year": "2021",
        "description": "Rimuru's nation grows as new allies join his cause. But with growth comes new enemies and challenges. This season explores the politics of the fantasy world and Rimuru's growth as a leader.",
        "episodes": 24,
        "image_url": "https://raw.githubusercontent.com/princehamzaytprogramming/princetoons/main/static/slim-season-2.png",
        "download_links": [
            {"name": "MEGA", "url": "https://mega.nz/#!tSszxQwJ!gHvTdRv2vPxuCkxCFp80wtlzVjlK5RNS9RQzBUPeGJo"},
            {"name": "PIXELDRAIN", "url": "https://pixeldrain.net/u/XZBmM6eE?download"},
            {"name": "GO FILE", "url": "https://gofile.io/d/0dRx1z"}
        ],
        "anime-type-tags": "season,series,fantasy,reincarnation,adventure",
        "search-alternatives": "That Time I Got Reincarnated as a Slime,tensei slime,Slime season 2"
    },
    {
        "id": 63,
        "title": "That Time I Got Reincarnated as a Slime",
        "season": "SEASON 3",
        "year": "2024",
        "description": "The nation of Tempest continues to grow and face new challenges. With epic battles, political intrigue, and heartwarming moments, this season proves why Slime is one of the most beloved isekai anime.",
        "episodes": 24,
        "image_url": "https://raw.githubusercontent.com/princehamzaytprogramming/princetoons/main/static/slim-season-3.png",
        "download_links": [
            {"name": "PIXELDRAIN", "url": "https://pixeldrain.net/u/NGAacMva?download"},
            {"name": "CLOUD HUB", "url": "https://hubcloud.cx/drive/4gffx41o7hkkz4w"}
        ],
        "anime-type-tags": "season,series,fantasy,reincarnation,adventure",
        "search-alternatives": "That Time I Got Reincarnated as a Slime,tensei slime,Slime season 3"
    },
    {
        "id": 64,
        "title": "That Time I Got Reincarnated as a Slime",
        "season": "SEASON 4 EP-1-12",
        "year": "2025",
        "description": "The adventure continues! Rimuru faces his biggest challenge yet as enemies from all sides threaten his peaceful nation. A thrilling continuation of the beloved Slime series.",
        "episodes": 12,
        "image_url": "https://raw.githubusercontent.com/princehamzaytprogramming/princetoons/main/static/slim-season-4.png",
        "download_links": [
            {"name": "PIXELDRAIN", "url": "https://pixeldrain.net/u/zVDt2niU?download"},
            {"name": "CLOUD HUB", "url": "https://hubcloud.cx/drive/txshlx2jdyx6jjz"}
        ],
        "anime-type-tags": "season,series,fantasy,reincarnation,adventure",
        "search-alternatives": "That Time I Got Reincarnated as a Slime,tensei slime,Slime season 4"
    },
    {
        "id": 65,
        "title": "I Got a Cheat Skill in Another World and Became Unrivaled in the Real World, Too",
        "season": "SEASON 1",
        "year": "2023",
        "description": "A bullied teenager discovers a door to another world where he gains incredible powers. These powers also work in the real world, and he uses them to transform his life. A satisfying power fantasy anime.",
        "episodes": 13,
        "image_url": "https://raw.githubusercontent.com/princehamzaytprogramming/princetoons/main/static/i-got-cheat-skill-in-another-world.png",
        "download_links": [
            {"name": "MEGA", "url": "https://mega.nz/#!0bM3yTCI!010Z3Xn5PG0jhgLtRoKGnBugDfS1FchY5gqrsac4Se0"},
            {"name": "PIXELDRAIN", "url": "https://pixeldrain.net/u/NVupSh4e?download"}
        ],
        "anime-type-tags": "season,series,fantasy,reincarnation,action",
        "search-alternatives": "I Got a Cheat Skill in Another World,cheat skill in another world,I Got a Cheat Skill"
    },
    {
        "id": 66,
        "title": "I Was Reincarnated as the 7th Prince So I Can Take My Time Perfecting My Magical Ability",
        "season": "SEASON 1",
        "year": "2024",
        "description": "A powerful mage is reincarnated as the 7th prince of a kingdom. With his past knowledge, he pursues his passion for magic while navigating the politics of royal life. A lighthearted and fun isekai comedy.",
        "episodes": 12,
        "image_url": "https://raw.githubusercontent.com/princehamzaytprogramming/princetoons/main/static/recarnation-7th-prince-season-1.png",
        "download_links": [
            {"name": "CLOUD HUB", "url": "https://hubcloud.cx/drive/krpxlcggkl5dnch"},
            {"name": "PIXELDRAIN", "url": "https://pixeldrain.net/u/cUUpmnDm?download"}
        ],
        "anime-type-tags": "season,series,fantasy,reincarnation,comedy",
        "search-alternatives": "I Was Reincarnated as the 7th Prince,7th prince,7th Prince season 1"
    },
    {
        "id": 67,
        "title": "I Was Reincarnated as the 7th Prince So I Can Take My Time Perfecting My Magical Ability",
        "season": "SEASON 2",
        "year": "2025",
        "description": "The 7th prince continues his magical studies while dealing with new royal intrigues. More magic, more comedy, and more heartwarming moments in this delightful isekai anime.",
        "episodes": 12,
        "image_url": "https://raw.githubusercontent.com/princehamzaytprogramming/princetoons/main/static/recarnation-7th-prince-season-2.png",
        "download_links": [
            {"name": "CLOUD HUB", "url": "https://hubcloud.cx/drive/xcnaxss335bv4k6"},
            {"name": "PIXELDRAIN", "url": "https://pixeldrain.net/u/NC3TwnUT?download"}
        ],
        "anime-type-tags": "season,series,fantasy,reincarnation,comedy",
        "search-alternatives": "I Was Reincarnated as the 7th Prince,7th prince,7th Prince season 2"
    },
    {
        "id": 68,
        "title": "KONOSUBA God's blessing on this wonderful world",
        "season": "SEASON 1",
        "year": "2016",
        "description": "A young man dies and is reincarnated into a fantasy world. But instead of a grand adventure, he gets stuck with a useless goddess and a group of misfits. One of the funniest isekai anime ever made.",
        "episodes": 10,
        "image_url": "https://raw.githubusercontent.com/princehamzaytprogramming/princetoons/main/static/konosuba-gods-blessing-on-this-wonderful-world-season-1.png",
        "download_links": [
            {"name": "CLOUD HUB", "url": "https://hubcloud.cx/drive/a6vaid4utuglwds"},
            {"name": "PIXELDRAIN", "url": "https://pixeldrain.net/u/rTZ8LwV4?download"}
        ],
        "anime-type-tags": "season,series,comedy,fantasy,isekai",
        "search-alternatives": "KONOSUBA God's blessing on this wonderful world,konosuba,Konosuba season 1"
    },
    {
        "id": 69,
        "title": "Witch Hat Atelier",
        "season": "SEASON 1",
        "year": "2025",
        "description": "In a world where magic is a privilege only the elite can use, a young girl discovers a way to learn magic through drawing. A beautiful and enchanting story about creativity, determination, and breaking barriers.",
        "episodes": 12,
        "image_url": "https://raw.githubusercontent.com/princehamzaytprogramming/princetoons/main/static/witch-hat-atelier-season-1.png",
        "download_links": [
            {"name": "PIXELDRAIN", "url": "https://pixeldrain.net/u/JummdkeS?download"},
            {"name": "CLOUD HUB", "url": "https://hubcloud.cx/drive/gpmap9x93isk7m9"}
        ],
        "anime-type-tags": "season,series,fantasy,adventure,magic",
        "search-alternatives": "Witch Hat Atelier,witch hat atelier,WitchHatAtelier"
    },
    {
        "id": 70,
        "title": "Classroom of The Elite",
        "season": "SEASON 1",
        "year": "2017",
        "description": "At a prestigious high school where only the best can succeed, a mysterious student with a hidden past navigates the cutthroat world of academic competition. A psychological thriller with incredible twists.",
        "episodes": 12,
        "image_url": "https://raw.githubusercontent.com/princehamzaytprogramming/princetoons/main/static/classroom-of-the-elite-season-1.png",
        "download_links": [
            {"name": "CLOUD HUB", "url": "https://hubcloud.cx/drive/wa4wddccxdccfdx"},
            {"name": "PIXELDRAIN", "url": "https://pixeldrain.net/u/nnURpy6v?download"}
        ],
        "anime-type-tags": "season,series,psychological,school,thriller",
        "search-alternatives": "Classroom of The Elite,classroom of the elite,COTE season 1"
    },
    {
        "id": 71,
        "title": "Classroom of The Elite",
        "season": "SEASON 2",
        "year": "2022",
        "description": "The psychological battles continue as Kiyotaka and his classmates face even more challenging tests. Secrets are revealed, alliances are formed, and the true nature of the school is slowly uncovered.",
        "episodes": 13,
        "image_url": "https://raw.githubusercontent.com/princehamzaytprogramming/princetoons/main/static/classroom-of-the-elite-season-2.png",
        "download_links": [
            {"name": "CLOUD HUB", "url": "https://hubcloud.cx/drive/fxobhqtyhvhlxoe"},
            {"name": "PIXELDRAIN", "url": "https://pixeldrain.net/u/XqCn3Sj8?download"}
        ],
        "anime-type-tags": "season,series,psychological,school,thriller",
        "search-alternatives": "Classroom of The Elite,classroom of the elite,COTE season 2"
    },
    {
        "id": 72,
        "title": "Classroom of The Elite",
        "season": "SEASON 3",
        "year": "2024",
        "description": "The final season! The mysteries of the school are finally revealed as Kiyotaka faces his toughest challenge yet. A thrilling conclusion to one of the best psychological anime of all time.",
        "episodes": 13,
        "image_url": "https://raw.githubusercontent.com/princehamzaytprogramming/princetoons/main/static/classroom-of-the-elite-season-3.png",
        "download_links": [
            {"name": "CLOUD HUB", "url": "https://hubcloud.cx/drive/oqzkrkeqq1suit8"},
            {"name": "PIXELDRAIN", "url": "https://pixeldrain.net/u/Wv5M3mTU?download"}
        ],
        "anime-type-tags": "season,series,psychological,school,thriller",
        "search-alternatives": "Classroom of The Elite,classroom of the elite,COTE season 3"
    },
    {
        "id": 73,
        "title": "Assassination Classroom",
        "season": "SEASON 1",
        "year": "2015",
        "description": "A class of misfit students must kill their alien teacher before he destroys the Earth. But he's the best teacher they've ever had. A hilarious, heartwarming, and action-packed anime about growing up.",
        "episodes": 22,
        "image_url": "https://raw.githubusercontent.com/princehamzaytprogramming/princetoons/main/static/assassination-classroom-season-1.png",
        "download_links": [
            {"name": "GO FILE", "url": "https://gofile.io/d/ZScKs2"},
            {"name": "PIXELDRAIN", "url": "https://pixeldrain.net/u/2XkjmEav?download"}
        ],
        "anime-type-tags": "season,series,comedy,school,action",
        "search-alternatives": "Assassination Classroom,assassination classroom,Ansatsu Kyoshitsu season 1"
    },
    {
        "id": 74,
        "title": "Assassination Classroom",
        "season": "SEASON 2",
        "year": "2016",
        "description": "The students of Class 3-E continue their mission to kill their teacher. But as the deadline approaches, they realize what they'll lose. An emotional and satisfying conclusion to this beloved series.",
        "episodes": 25,
        "image_url": "https://raw.githubusercontent.com/princehamzaytprogramming/princetoons/main/static/assassination-classroom-season-2.png",
        "download_links": [
            {"name": "MEGA", "url": "https://mega.nz/#!WvRn0TJB!t7sfoVEhNQCy7MEnbfCRmokHmXv05QmjYmpY1vK48t8"},
            {"name": "GO FILE", "url": "https://gofile.io/d/T5KFnk"},
            {"name": "PIXELDRAIN", "url": "https://pixeldrain.net/u/gcTQEwue?download"}
        ],
        "anime-type-tags": "season,series,comedy,school,action",
        "search-alternatives": "Assassination Classroom,assassination classroom,Ansatsu Kyoshitsu season 2"
    },
    {
        "id": 75,
        "title": "Jujutsu Kaisen",
        "season": "SEASON 1",
        "year": "2020",
        "description": "A high school student swallows a cursed finger to save his friends and becomes the vessel of a powerful curse. Now he must train as a Jujutsu Sorcerer to fight evil curses. A modern masterpiece of action and horror.",
        "episodes": 24,
        "image_url": "https://raw.githubusercontent.com/princehamzaytprogramming/princetoons/main/static/jjk-season-1.png",
        "download_links": [
            {"name": "PIXELDRAIN", "url": "https://pixeldrain.net/u/w8fQXzW5?download"},
            {"name": "CLOUD HUB", "url": "https://hubcloud.cx/drive/u5jn2xa6jn25ejz#!/ZSLUQFbH3wvDSqv"}
        ],
        "anime-type-tags": "season,series,action,supernatural,horror",
        "search-alternatives": "jjk,jjks1,Jujutsu Kaisen,Jujutsu Kaisen,jujutsu kaisen,JujutsuKaisen,Jujutsu Kaisen Season 1"
    },
    {
        "id": 76,
        "title": "Jujutsu Kaisen",
        "season": "SEASON 2",
        "year": "2023",
        "description": "The story continues with the Hidden Inventory and Shibuya Incident arcs. Darker, more intense, and more emotional than season one, this is where Jujutsu Kaisen truly becomes a masterpiece.",
        "episodes": 23,
        "image_url": "https://raw.githubusercontent.com/princehamzaytprogramming/princetoons/main/static/jjk-season-2.png",
        "download_links": [
            {"name": "PIXELDRAIN", "url": "https://pixeldrain.net/u/mxnvtEMn?download"},
            {"name": "CLOUD HUB", "url": "https://hubcloud.cx/drive/riuigt6gie1ogx6"}
        ],
        "anime-type-tags": "season,series,action,supernatural,horror",
        "search-alternatives": "jjk,jjks2,Jujutsu Kaisen,Jujutsu Kaisen,jujutsu kaisen,JujutsuKaisen,Jujutsu Kaisen Season 2"
    },
    {
        "id": 77,
        "title": "Jujutsu Kaisen",
        "season": "SEASON 3",
        "year": "2025",
        "description": "The highly anticipated continuation of the Jujutsu Kaisen saga! With the Shibuya incident behind them, the surviving sorcerers must face even greater threats. The battle against curses reaches its peak.",
        "episodes": 12,
        "image_url": "https://raw.githubusercontent.com/princehamzaytprogramming/princetoons/main/static/jjk-season-3.png",
        "download_links": [
            {"name": "PIXELDRAIN", "url": "https://pixeldrain.net/u/sJJVP9JP?download"},
            {"name": "CLOUD HUB", "url": "https://hubcloud.cx/drive/syopddwx0uyafcu"}
        ],
        "anime-type-tags": "season,series,action,supernatural,horror",
        "search-alternatives": "jjk,jjks3,Jujutsu Kaisen,Jujutsu Kaisen,jujutsu kaisen,JujutsuKaisen,Jujutsu Kaisen Season 3"
    },
    {
        "id": 78,
        "title": "Jujutsu Kaisen 0",
        "season": "MOVIE",
        "year": "2021",
        "description": "The prequel to the Jujutsu Kaisen series! Follow Yuta Okkotsu, a young man cursed by the spirit of his childhood friend. A powerful story about love, loss, and finding the strength to protect others.",
        "episodes": 1,
        "image_url": "https://raw.githubusercontent.com/princehamzaytprogramming/princetoons/main/static/jjk-0-movie.png",
        "download_links": [
            {"name": "MEGA", "url": "https://mega.nz/file/v0AgQahC#CclQ2UOcfuRKmmD7FL9EENF1xp5rqC6AOWZQKjvPFXI"},
            {"name": "MEDIA FIRE", "url": "https://www.mediafire.com/file/my19le1bdkedx0k/[RAI]+Jujutsu+Kaisen+0+Movie+-+Hindi.mp4/file"}
        ],
        "anime-type-tags": "movie,action,supernatural,horror",
        "search-alternatives": "jjk,jjkm,jjkmovie,Jujutsu Kaisen,Jujutsu Kaisen,jujutsu kaisen,JujutsuKaisen,Jujutsu Kaisen Movie,jujutsu kaisen movie,jujutsu kaisen zero,jujutsu kaisen 0"
    },
    {
        "id": 79,
        "title": "Ao Ashi",
        "season": "SEASON 1",
        "year": "2022",
        "description": "A young soccer player with incredible potential is scouted to join a prestigious club's youth academy. Through hard work and determination, he discovers his true potential. A thrilling sports anime for football fans.",
        "episodes": 24,
        "image_url": "https://raw.githubusercontent.com/princehamzaytprogramming/princetoons/main/static/ao-ashi-season-1.png",
        "download_links": [
            {"name": "CLOUD HUB", "url": "https://hubcloud.cx/drive/mws5mizbmo13ho3"}
        ],
        "anime-type-tags": "season,series,sport,sports,football",
        "search-alternatives": "aoashi,ao ashi,Ao Ashi,AoAshi,ao ashi season1"
    },
    {
        "id": 80,
        "title": "Haikyu",
        "season": "SEASON 2",
        "year": "2015",
        "description": "The volleyball competition intensifies as Karasuno faces stronger opponents. With new skills and strategies, the team works together to reach the nationals. An inspiring anime about teamwork and perseverance.",
        "episodes": 25,
        "image_url": "https://raw.githubusercontent.com/princehamzaytprogramming/princetoons/main/static/haikyu-season-2.png",
        "download_links": [
            {"name": "CLOUD HUB", "url": "https://hubcloud.cx/drive/pve44r4e587b95b"}
        ],
        "anime-type-tags": "season,series,sport,sports,volleyball",
        "search-alternatives": "haikyu,haiku,Haikyu,haikyu season 2,haikyu season2"
    },
    {
        "id": 81,
        "title": "Haikyu",
        "season": "SEASON 3",
        "year": "2016",
        "description": "Karasuno faces their toughest challenge yet in the spring nationals qualifiers. Against the powerful Shiratorizawa Academy, they must give everything they have. A spectacular season of high-stakes volleyball.",
        "episodes": 10,
        "image_url": "https://raw.githubusercontent.com/princehamzaytprogramming/princetoons/main/static/haikyu-season-3.png",
        "download_links": [
            {"name": "CLOUD HUB", "url": "https://hubcloud.cx/drive/ux1pewexsqv1wlu"}
        ],
        "anime-type-tags": "season,series,sport,sports,volleyball",
        "search-alternatives": "haikyu,haiku,Haikyu,haikyu season 3,haikyu season3"
    },
    {
        "id": 82,
        "title": "Haikyu",
        "season": "SEASON 4",
        "year": "2020",
        "description": "Karasuno finally reaches the nationals! Against the best teams in Japan, the team faces their greatest challenge. This season explores the growth of each character and the true meaning of competition.",
        "episodes": 25,
        "image_url": "https://raw.githubusercontent.com/princehamzaytprogramming/princetoons/main/static/haikyu-season-4.png",
        "download_links": [
            {"name": "PIXELDRAIN", "url": "https://pixeldrain.net/u/vjs8W6Mf?download"},
            {"name": "CLOUD HUB", "url": "https://hubcloud.cx/drive/lgh8v1qalrac1ke"}
        ],
        "anime-type-tags": "season,series,sport,sports,volleyball",
        "search-alternatives": "haikyu,haiku,Haikyu,haikyu season 4,haikyu season4"
    },
    {
        "id": 83,
        "title": "Haikyu The Dumpster Battle",
        "season": "MOVIE",
        "year": "2024",
        "description": "The long-awaited match between Karasuno and Nekoma! This movie captures the intense rivalry and friendship between the two teams. A must-watch for every Haikyu fan.",
        "episodes": 1,
        "image_url": "https://raw.githubusercontent.com/princehamzaytprogramming/princetoons/main/static/haikyu-the-dumpster-battle-movie.png",
        "download_links": [
            {"name": "MEGA", "url": "https://mega.nz/file/PZMgASqY#yM90QVNs7ygVtBkAuIsSyoPivbuB0CjixMLTpMmG6S0"},
            {"name": "PIXEL DRAIN", "url": "https://pixeldrain.net/u/okCyrXYn?download"}
        ],
        "anime-type-tags": "movie,movies,sport,sports,volleyball",
        "search-alternatives": "haikyu,haiku,Haikyu,haikyu movie,Haikyu Movie,HAIKYU The Dumpster Battle"
    },
    {
        "id": 84,
        "title": "SpiderMan Across the Spider Verse",
        "season": "MOVIE",
        "year": "2023",
        "description": "Miles Morales returns for an epic multiverse adventure! When a new threat emerges, he must team up with Spider-People from across dimensions. Visually stunning and emotionally powerful, this is a masterpiece.",
        "episodes": 1,
        "image_url": "https://raw.githubusercontent.com/princehamzaytprogramming/princetoons/main/static/spider-man-across-the-spider-verse-movie.png",
        "download_links": [
            {"name": "MEGA", "url": "https://mega.nz/file/Uyl2BJYI#s2JeXiVXbIQOOqZT3rt_mUvqBRZuA95pWWEBKwmi3w0"}
        ],
        "anime-type-tags": "movie,marvel,hero,spider,spiderman",
        "search-alternatives": "SpiderMan Across the Spider Verse,spiderman across the spider verse,spidermanacrossthespiderverse"
    }
]
'''

# Convert JSON string to Python list of dictionaries
anime_list = json.loads(jsons)
titles_list = [item['title'] for item in anime_list]

# Join all titles with commas and print
name_keywords = ','.join(titles_list)


# ============================================
# Add slug (image name) to each anime
# ============================================
for anime in anime_list:
    # Extract the image filename from the URL
    image_url = anime.get('image_url', '')
    if image_url:
        # Get the filename from the URL
        filename = os.path.basename(image_url)
        # Remove the .png extension
        slug = filename.replace('.png', '')
        anime['slug'] = slug

# ============================================
# REVERSE THE ANIME LIST - Show highest ID first
# ============================================
anime_list_reversed = anime_list[::-1]

# ============================================
# HELPER FUNCTION - Generate page titles
# ============================================

def get_page_title(page_type, anime=None, query=None, page_num=None):
    """
    Generate unique, SEO-friendly page titles for each page
    """
    if page_type == 'home':
        return "PRINCE TOONS - Download Hindi Dubbed Anime & Movies Free"
    elif page_type == 'page1':
        if page_num and page_num > 1:
            return f"Hindi Dubbed Anime Page {page_num} - Watch Online Free | PRINCE TOONS"
        return "All Hindi Dubbed Anime - Watch Online Free | PRINCE TOONS"
    elif page_type == 'detail' and anime:
        title = anime.get('title', '')
        season = anime.get('season', '')
        return f"{title} {season} Hindi Dubbed - Download & Watch | PRINCE TOONS"
    elif page_type == 'search':
        if query:
            return f"Search Results for '{query}' - PRINCE TOONS"
        return "Search Anime - PRINCE TOONS"
    elif page_type == 'about':
        return "About PRINCE TOONS - DMCA Policy, Terms & Disclaimer"
    elif page_type == 'sitemap':
        return "Sitemap - PRINCE TOONS"
    else:
        return "PRINCE TOONS - Hindi Dubbed Anime & Movies"

def get_meta_description(page_type, anime=None, query=None):
    """
    Generate unique meta descriptions for each page
    """
    if page_type == 'home':
        return "Download and watch Hindi dubbed anime and movies for free at PRINCE TOONS. Full seasons of Attack on Titan, Jujutsu Kaisen, Re:Zero, Sword Art Online, Blue Lock, and more in HD quality."
    elif page_type == 'page1':
        return "Browse all Hindi dubbed anime and movies at PRINCE TOONS. Watch Attack on Titan, Jujutsu Kaisen, Re:Zero, Sword Art Online, Blue Lock, and more in HD quality."
    elif page_type == 'detail' and anime:
        desc = anime.get('description', '')
        title = anime.get('title', '')
        season = anime.get('season', '')
        return f"Download {title} {season} Hindi Dubbed for free. {desc[:140]} Watch online in HD quality at PRINCE TOONS."
    elif page_type == 'search':
        if query:
            return f"Search results for '{query}' at PRINCE TOONS. Find your favorite Hindi dubbed anime and movies."
        return "Search for Hindi dubbed anime and movies at PRINCE TOONS. Find Attack on Titan, Jujutsu Kaisen, and more."
    elif page_type == 'about':
        return "About PRINCE TOONS - Your source for Hindi dubbed anime and movies. Learn about our platform, DMCA policy, terms of use, and how we provide free anime streaming."
    else:
        return "PRINCE TOONS - Hindi Dubbed Anime & Movies Free Download"

# ============================================
# HTML TEMPLATES - Website Pages (SEO Enhanced)
# ============================================

# [HOME PAGE - Kept same as before with minor SEO improvements]
home = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    
    
    <meta name="google-site-verification" content="0nVOqCF33huAKgNcWE-zEjGHLpQj_FRtPjPPkdt5Gu0" />
    <title>{{ page_title }}</title>
    <meta name="description" content="{{ meta_description }}" />
    
    <link rel="canonical" href="https://princetoons.pythonanywhere.com/" />
    
    <meta property="og:title" content="PRINCE TOONS - Download Hindi Dubbed Anime & Movies Free" />
    <meta property="og:description" content="Download and watch Hindi dubbed anime and movies for free. Full seasons available in HD quality." />
    <meta property="og:image" content="https://raw.githubusercontent.com/princehamzaytprogramming/princetoons/main/static/princetoons.png" />
    <meta name="keywords" content="anime,cartoon,toon,toons,movie,movies,animes,hindi,Hindi,HINDI,urdu,Urdu,URDU,english,English,ENGLISH,sub,dub,subbed,dubbed,Sub,Dub,SUBBED,DUBBED,english sub,english dub,urdu sub,urdu dub,hindi sub,hindi dub,english subbed,english dubbed,urdu subbed,urdu dubbed,hindi subbed,hindi dubbed,HINDI SUB,HINDI DUB,HINDI SUBBED,HINDI DUBBED,2d,3d,2dcartoon,3dcartoon,2danime,3danime,prince,Prince,PRINCE,toon,toons,Toon,Toons,TOONS,princetoon,princetoons,PrinceToon,PrinceToons,PRINCETOON,PRINCETOONS,prince toon,prince toons,Prince Toon,Prince Toons,PRINCE TOON,PRINCE TOONS,princeanime,prince anime,PrinceAnime,Prince Anime,PRINCEANIME,PRINCE ANIME,Cartoon,cartoon,cartoons,CARTOON,CARTOONS,animename,anime name,AnimeName,Anime Name,new,old,80s,90s,20s,newanime,New Anime,new anime,oldanime,Old Anime,old anime,newtoon,oldtoon,newtoons,oldtoons,new toons,old toons,princetoonswebsite,princetoonsweb,prince toons web,prince toons website,princetoonanime,princetoonsanime,prince toon anime,prince toons anime,PrinceToonAnime,PrinceToonsAnime,princetoonreview,princetoonsreview,prince toons review,good,verygood,normal,average,exelent,characters,goku,kakarot,vegeta,gon,boboiboy,naruto,saska,kakashi,itachi,madara,bleach,gojo,sakuna,yuji,isagi,nagi,barou,bachira,rin,sae,chigiri,spider,spiderman,miles,peter,peter parker,gopal,yaya,krillen,yamcha,picollo,frieza,gohan,kiluha,pakistan,india,usa,united,unitedstate,unitedstates,united states,america,Pakistan,PAKISTAN,pak,ind,INDIA,{{name_keywords}}" />
    <meta property="og:url" content="https://princetoons.pythonanywhere.com/" />
    <meta property="og:type" content="website" />
    <meta property="og:site_name" content="PRINCE TOONS" />
    <meta property="og:updated_time" content="{{ current_date }}" />
    
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:title" content="PRINCE TOONS - Download Hindi Dubbed Anime & Movies Free" />
    <meta name="twitter:description" content="Download and watch Hindi dubbed anime and movies for free." />
    <meta name="twitter:image" content="https://raw.githubusercontent.com/princehamzaytprogramming/princetoons/main/static/princetoons.png" />
    
    <link rel="alternate" hreflang="en" href="https://princetoons.pythonanywhere.com/" />
    <link rel="alternate" hreflang="hi" href="https://princetoons.pythonanywhere.com/" />
    <link rel="alternate" hreflang="x-default" href="https://princetoons.pythonanywhere.com/" />
    
    <!-- Organization Schema -->
    
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "Organization",
      "name": "PRINCE TOONS",
      "url": "https://princetoons.pythonanywhere.com/",
      "thumbnailUrl": "https://raw.githubusercontent.com/princehamzaytprogramming/princetoons/main/static/princetoons.png",
      "logo": "https://raw.githubusercontent.com/princehamzaytprogramming/princetoons/main/static/princetoons.png",
      "description": "Free Hindi Dubbed Anime and Movies Download Website",
      "sameAs": [
        "https://youtube.com/@princehamzayt6210",
        "https://www.instagram.com/princehmzayt",
        "https://www.tiktok.com/@princehamza.yt"
      ]
    }
    </script>
    
    <!-- WebSite Schema -->
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "WebSite",
      "thumbnailUrl": "https://raw.githubusercontent.com/princehamzaytprogramming/princetoons/main/static/princetoons.png",
      "url": "https://princetoons.pythonanywhere.com/",
      "name": "PRINCE TOONS",
      "description": "Free Hindi Dubbed Anime and Movies Download Website",
      "potentialAction": {
        "@type": "SearchAction",
        "target": "https://princetoons.pythonanywhere.com/search?q={search_term_string}",
        "query-input": "required name=search_term_string"
      }
    }
    </script>
    
    <style>
        /* Reset default margins and padding */
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        /* Main body styling */
        body { 
            background-color: black;
            color: white;
            font-family: Arial, sans-serif;
        }
        
        /* Remove underline and blue color from links */
        a, a:focus, a:active, a:visited {
            -webkit-tap-highlight-color: transparent;
            color: white;
            text-decoration: none;
        }
        
        /* Logo image styling with alt */
        .toonimage {
            width: 75px;
            height: auto;
        }
        
        /* Header table styling */
        .header-table {
            margin: 0 auto;
            text-align: center;
            border-collapse: collapse;
            width: 100%;
            max-width: 600px;
        }
        
        .header-table td {
            padding: 10px 15px;
            vertical-align: middle;
        }
        
        /* Header title styling */
        .header-title {
            color: white;
            font-size: 30px;
        }
        
        .header-title:hover {
            color: #ffcc00;
            transition: 0.3s;
        }
        
        /* Welcome box styling */
        .welcome-box {
            border-top: 2px solid;
            border-bottom: 2px solid;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100px;
            border-color: white;
            margin: 10px 0;
        }
        
        .welcome-inner {
            border: 2px solid;
            border-radius: 20px;
            width: 330px;
            height: 70px;
            display: flex;
            justify-content: center;
            align-items: center;
            border-color: white;
        }
        
        .welcome-text {
            margin: 0;
            font-size: 30px;
            font-weight: bold;
            color: white;
        }
        
        /* Main container styling */
        .main-container {
            border: 2px solid;
            border-radius: 90px;
            border-color: white;
            margin: 20px;
            padding: 20px;
            text-align: center;
        }
        
        .main-title {
            font-size: 33px;
            font-weight: bold;
            color: white;
        }
        
        .sub-title {
            font-size: 23px;
            font-weight: bold;
            color: white;
            margin: 10px 0;
        }
        
        .gold-text {
            color: gold;
            font-size: 33px;
            font-weight: bold;
            margin: 10px 0;
        }
        
        /* Pokeball styling */
        .pokeball {
            position: relative;
            margin: 10px auto;
            width: 145px;
            height: 145px;
            background: linear-gradient(to bottom, #ff1c1c 45%, #111111 45%, skyblue 55%, #ffffff 55%);
            border: 3px solid #111111;
            border-radius: 50%;
            overflow: hidden;
            cursor: pointer;
            display: flex;
            justify-content: center;
            align-items: center;
            -webkit-tap-highlight-color: transparent;
            user-select: none;
            -webkit-user-select: none;
            outline: none;
            -webkit-touch-callout: none;
            animation: shake 4s alternate infinite;
            
        }
        
        .pokeball-button {
            position: absolute;
            width: 55px;
            height: 55px;
            background-color: #ffffff;
            border: 7px solid #111111;
            border-radius: 50%;
            z-index: 10;
            transition: background-color 0.2s ease;
            -webkit-tap-highlight-color: transparent;
            outline: none;
            animation: flash 1.5s ease-in-out infinite;
        }
        
        .pokeball-button::after {
            content: "";
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            width: 15px;
            height: 15px;
            border: 4px solid #111111;
            border-radius: 50%;
            background-color: #ebc82f;
        }
        
        @keyframes shake {
            0% { transform: translate(0, 0); }
            50% { transform: translate(-10px, 0); }
            100% { transform: translate(15px, 0); }
        }
        
        @keyframes flash {
            0%, 100% { background-color: #ffffff; }
            50% { background-color: skyblue; }
            80% { background-color: #ff3838; }
        }
        
        .pokeball, .pokeball-button, .pokeball * {
            -webkit-tap-highlight-color: transparent !important;
            outline: none !important;
            -webkit-touch-callout: none !important;
            -webkit-user-select: none !important;
            user-select: none !important;
        }
        
        /* Search Button */
        .search-button-container {
            display: flex;
            justify-content: center;
            margin: 15px 0;
        }
        
        .search-button {
            display: inline-block;
            border: 2px solid gold;
            border-radius: 30px;
            padding: 12px 30px;
            color: gold;
            font-size: 20px;
            font-weight: bold;
            text-decoration: none;
            transition: background-color 0.3s, transform 0.2s;
            cursor: pointer;
        }
        
        .search-button:hover {
            background-color: gold;
            color: black;
            transform: scale(1.05);
        }
        
        /* Social section */
        .social-row {
            display: flex;
            flex-wrap: nowrap;
            justify-content: center;
            align-items: center;
            gap: 0.8rem;
            padding: 0.8rem 1.2rem;
            background: rgba(255,255,255,0.05);
            backdrop-filter: blur(8px);
            border-radius: 50px;
            box-shadow: 0 15px 30px rgba(0,0,0,0.5);
            border: 1px solid rgba(255,255,255,0.08);
            width: fit-content;
            max-width: 100%;
            overflow: hidden;
            margin: 0 auto;
        }
        
        .social-row a {
            display: flex;
            align-items: center;
            justify-content: center;
            width: 60px;
            height: 60px;
            flex-shrink: 0;
            background: rgba(255,255,255,0.05);
            border-radius: 50%;
            border: 1px solid rgba(255,255,255,0.06);
            transition: all 0.3s ease;
            text-decoration: none;
            animation: float 3s ease-in-out infinite;
        }
        
        .social-row a:nth-child(1) { animation-delay: 0s; }
        .social-row a:nth-child(2) { animation-delay: 0.4s; }
        .social-row a:nth-child(3) { animation-delay: 0.8s; }
        .social-row a:nth-child(4) { animation-delay: 1.2s; }
        
        .social-row img {
            width: 38px;
            height: 38px;
            object-fit: contain;
            display: block;
            filter: drop-shadow(0 3px 6px rgba(0,0,0,0.3));
            border-radius: 6px;
            transition: transform 0.3s ease;
        }
        
        @keyframes float {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(-6px); }
        }
        
        .social-row a:hover {
            transform: scale(1.12) !important;
            background: rgba(255, 255, 255, 0.12);
            border-color: rgba(255, 255, 255, 0.18);
            box-shadow: 0 6px 20px rgba(0, 0, 0, 0.4);
            animation-play-state: paused;
        }
        
        .social-row a:hover img {
            transform: scale(1.05);
            filter: drop-shadow(0 4px 10px rgba(255, 255, 255, 0.12));
        }
        
        .social-row a:active {
            transform: scale(0.92) !important;
            transition-duration: 0.08s;
        }
        
        /* Mobile responsive design */
        @media (max-width: 768px) {
            .header-title { font-size: 25px; }
            .header-table td { padding: 5px 10px; }
            .main-container { margin: 10px; padding: 15px; }
            .main-title { font-size: 28px; }
            .gold-text { font-size: 28px; }
            .social-row { gap: 0.5rem; padding: 0.6rem 1rem; }
            .social-row a { width: 50px; height: 50px; }
            .social-row img { width: 30px; height: 30px; }
            .search-button { padding: 10px 20px; font-size: 16px; }
            .welcome-inner { width: 280px; }
            .welcome-text { font-size: 24px; }
            .pokeball { width: 120px; height: 120px; }
            .pokeball-button { width: 45px; height: 45px; border-width: 5px; }
            .pokeball-button::after { width: 12px; height: 12px; border-width: 3px; }
        }
        
        @media (max-width: 480px) {
            .header-title { font-size: 20px; }
            .header-table td { padding: 3px 6px; }
            .main-title { font-size: 22px; }
            .sub-title { font-size: 18px; }
            .gold-text { font-size: 22px; }
            .search-button { padding: 8px 15px; font-size: 14px; }
            .welcome-inner { width: 220px; height: 32px; }
            .welcome-text { font-size: 18px; }
            .social-row a { width: 42px; height: 42px; }
            .social-row img { width: 24px; height: 24px; }
            .social-row { gap: 0.4rem; padding: 0.5rem 0.8rem; }
            .pokeball { width: 100px; height: 100px; }
            .pokeball-button { width: 38px; height: 38px; border-width: 4px; }
            .pokeball-button::after { width: 10px; height: 10px; border-width: 3px; }
        }
    </style>
</head>
<body>
    <header>
    <!-- Header with navigation links -->
    <table class="header-table">
        <tr>
            <td>
                <a href='/home' aria-label="Home Page">
                    <h1 class="header-title">HOME</h1>
                </a>
            </td>
            <td>
                <img class='toonimage logo-image' src="https://raw.githubusercontent.com/princehamzaytprogramming/princetoons/main/static/princetoons.png" alt='PRINCE TOONS Logo - Free Hindi Dubbed Anime Download Website' width="75" height="auto" loading="lazy">
            </td>
            <td>
                <a href='/about' aria-label="About Page">
                    <h1 class="header-title">ABOUT</h1>
                </a>
            </td>
        </tr>
    </table>
    
    <!-- Welcome section -->
    <div class="welcome-box">
        <div class="welcome-inner">
            <p style='font-size:27px;' class="welcome-text">• HOME •</p>
        </div>
    </div>
    <br>
    </header>
    <main>
    <!-- Main content -->
    <div class="main-container">
        <p class="main-title">• ANIME & MOVIES •</p>
        <h2 class="sub-title">WELCOME TO PRINCE TOONS</h2>
        <p style='margin-bottom:0px;' class="gold-text">• CLICK ON BALL •</p>
        
        <!-- Pokeball link -->
        <a style='margin:0px;' href='/page1' class="ball-link" aria-label="Enter PRINCE TOONS anime list">
            <div class="pokeball" role="button" tabindex="0" aria-label="Click to enter PRINCE TOONS">
                <div class="pokeball-button"></div>
            </div>
        </a>
        
        <!-- Search Button -->
        <div class="search-button-container">
            <a href='/search' class="search-button" aria-label="Search for anime">🔍 SEARCH ANIME</a>
        </div>
    </div>
    </main>
    <footer>
    	<ul style='text-align:center;' >
    	    <li style='font-weight:bold;font-size:27px;' >Prince Anime Toons</li>
            <li style='font-weight:bold;font-size:28px;' >Prince Toons</li>
            <li style='font-weight:bold;font-size:23px;' >Prince Anime</li>
            
        </ul>
        <br>
        <hr>
        <br>
        <!--INFORMATION ABOUT WEBSITE-->
        <h2 style="text-align:center;font-size:20px;">The Best Site to Watch/Download Anime CartoonsMovies in Hindi & Other Languages for Free</h2>
        <br>
        <p style='font-size:14px;color:gray;text-align:center;' >
          Since 2020, the anime industry has grown tremendously, with shows now available in multiple languages including English, Hindi, Urdu, Tamil, and Telugu — both subbed and dubbed. 
          This is why we created <strong>PrinceToons</strong> — a dedicated platform where anime and cartoon lovers can watch or download their favorite content in their preferred language, completely free of cost.
          <br> 	
          <strong>Important Note:</strong> PrinceToons does not host or store any content on its own servers. All content displayed on our website is sourced from third-party providers and is already freely available across the internet as open-source or publicly accessible media. We only organize and present this content to make it easier for our audience to discover and enjoy.
          <br>
          Our mission is simple: to revolutionize the anime streaming experience by offering a user-friendly, language-friendly, and completely free platform for fans around the world.
        </p>
        <br><br>
        <h2 style="text-align:center;">• What’s Prince Toons? •</h2>
        <br>
        <p style="font-size:14px;color:gray;text-align:center;max-width:800px;margin:0 auto;line-height:1.6;">
        <strong>PrinceToons</strong> (also known as <strong>Prince Toons</strong> or <strong>Prince Anime Toons</strong>) is a brand-new, free anime streaming platform designed for anime and cartoon lovers worldwide. 
        On <strong>PrinceToons</strong>, users can easily <strong>watch anime online</strong> or <strong>download anime for free</strong> in multiple languages including Hindi, English, Urdu, Tamil, and Telugu. 
        Whether you're looking for <strong>dubbed anime</strong>, <strong>subbed anime</strong>, or classic cartoons, our platform brings everything together in one place. 
        Best of all, it's completely <strong>free to watch and download anime</strong> — no hidden costs, no subscriptions, just pure entertainment. 
        Share your favorite shows with friends and family and enjoy the ultimate <strong>anime streaming experience</strong> at <strong>PrinceToons</strong>!
       </p>
       <br><br>
        <h2 style="text-align:center;">• Is Prince Toons Safe? •</h2>
        <br>
        <p style="font-size:14px;color:gray;text-align:center;max-width:800px;margin:0 auto;line-height:1.6;">
          Yes, <strong>PrinceToons</strong> is completely safe to use. Unlike many other anime streaming websites, <strong>PrinceToons</strong> does not host any content on its own servers — all content is sourced from third-party providers and is already publicly available on the internet. We simply organize and present this content for easy access. However, we always recommend using a reliable <strong>ad blocker</strong> and <strong>antivirus software</strong> while browsing any free streaming site, as third-party ads may appear. Your privacy and security matter to us, and we strive to provide a clean, user-friendly experience for all anime lovers.
        </p>
        <br><br>
        <h2 style="text-align:center;font-size:20px;">• Is PrinceToons User-Friendly? •</h2>
        <br>
        <p style="font-size:14px;color:gray;text-align:center;max-width:800px;margin:0 auto;line-height:1.6;">
          Yes! <strong>PrinceToons</strong> is built with a <strong>user-friendly interface</strong> that makes watching and downloading anime a breeze. All pages are designed for <strong>smooth navigation</strong>, with clear menus, fast search, and quick access to your favorite shows. Whether you're on mobile or desktop, our responsive design ensures a seamless experience. No clutter, no confusion — just easy access to the best anime content!
        </p>
        <br><br>
        <h1 style='color:#5b1eb0;font-size:25px;text-align:center;'>Prince Anime Toons does not store any files on own server, We only index links from internet which are hosted on third-party services. We Index Links Just Like Google</h1>
        <br><br>
        <p style='font-weight:bold;text-align:center;font-size:20px;'>OWNER</p>
        <p style='font-weight:bold;text-align:center;font-size:20px;'>SOCIAL MEDIA</p>
        
        
        <!-- Social media links with nofollow -->
        <div style="margin-top:0px;display:flex;justify-content:center;align-items:center;min-height:10vh;padding:1rem;">
            <div class="social-row">
                <a href='https://youtube.com/@princehamzayt6210' target="_blank" rel="noopener noreferrer nofollow" aria-label="YouTube Channel">
                    <img src="https://raw.githubusercontent.com/princehamzaytprogramming/princetoons/main/static/youtube.png" alt='Subscribe on YouTube' width="38" height="38" loading="lazy">
                </a>
                <a href='https://www.tiktok.com/@princehamza.yt' target="_blank" rel="noopener noreferrer nofollow" aria-label="TikTok Profile">
                    <img src="https://raw.githubusercontent.com/princehamzaytprogramming/princetoons/main/static/tiktok.png" alt='Follow on TikTok' width="38" height="38" loading="lazy">
                </a>
                <a href='https://www.instagram.com/princehmzayt' target="_blank" rel="noopener noreferrer nofollow" aria-label="Instagram Profile">
                    <img src="https://raw.githubusercontent.com/princehamzaytprogramming/princetoons/main/static/instagram.png" alt='Follow on Instagram' width="38" height="38" loading="lazy">
                </a>
                <a href='https://chat.whatsapp.com/HwvR3IcDg3gIgMUsnB90ss?s=cl&p=a&ilr=4' target="_blank" rel="noopener noreferrer nofollow" aria-label="WhatsApp Group">
                    <img src="https://raw.githubusercontent.com/princehamzaytprogramming/princetoons/main/static/whatsapp.png" alt='Join WhatsApp Group' width="38" height="38" loading="lazy">
                </a>
            </div>
        </div>
    </footer>
</body>
</html>
'''

# ============================================
# [PAGE1 TEMPLATE - SEO Enhanced with H1, breadcrumbs, related content]
# ============================================

page_template = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    
    <meta name="google-site-verification" content="0nVOqCF33huAKgNcWE-zEjGHLpQj_FRtPjPPkdt5Gu0" />
    
    <title>{{ page_title }}</title>
    <meta name="description" content="{{ meta_description }}" />
    
    <link rel="canonical" href="https://princetoons.pythonanywhere.com/page1{% if current_page > 1 %}?page={{ current_page }}{% endif %}" />
    {% if current_page > 1 %}
    <link rel="prev" href="https://princetoons.pythonanywhere.com/page1?page={{ current_page - 1 }}" />
    {% endif %}
    {% if current_page < total_pages %}
    <link rel="next" href="https://princetoons.pythonanywhere.com/page1?page={{ current_page + 1 }}" />
    {% endif %}
    
    <meta property="og:title" content="{{ page_title }}" />
    <meta property="og:description" content="{{ meta_description }}" />
    <meta property="og:image" content="https://raw.githubusercontent.com/princehamzaytprogramming/princetoons/main/static/princetoons.png" />
    <meta name="keywords" content="anime,cartoon,toon,toons,movie,movies,animes,hindi,Hindi,HINDI,urdu,Urdu,URDU,english,English,ENGLISH,sub,dub,subbed,dubbed,Sub,Dub,SUBBED,DUBBED,english sub,english dub,urdu sub,urdu dub,hindi sub,hindi dub,english subbed,english dubbed,urdu subbed,urdu dubbed,hindi subbed,hindi dubbed,HINDI SUB,HINDI DUB,HINDI SUBBED,HINDI DUBBED,2d,3d,2dcartoon,3dcartoon,2danime,3danime,prince,Prince,PRINCE,toon,toons,Toon,Toons,TOONS,princetoon,princetoons,PrinceToon,PrinceToons,PRINCETOON,PRINCETOONS,prince toon,prince toons,Prince Toon,Prince Toons,PRINCE TOON,PRINCE TOONS,princeanime,prince anime,PrinceAnime,Prince Anime,PRINCEANIME,PRINCE ANIME,Cartoon,cartoon,cartoons,CARTOON,CARTOONS,animename,anime name,AnimeName,Anime Name,new,old,80s,90s,20s,newanime,New Anime,new anime,oldanime,Old Anime,old anime,newtoon,oldtoon,newtoons,oldtoons,new toons,old toons,princetoonswebsite,princetoonsweb,prince toons web,prince toons website,princetoonanime,princetoonsanime,prince toon anime,prince toons anime,PrinceToonAnime,PrinceToonsAnime,princetoonreview,princetoonsreview,prince toons review,good,verygood,normal,average,exelent,characters,goku,kakarot,vegeta,gon,boboiboy,naruto,saska,kakashi,itachi,madara,bleach,gojo,sakuna,yuji,isagi,nagi,barou,bachira,rin,sae,chigiri,spider,spiderman,miles,peter,peter parker,gopal,yaya,krillen,yamcha,picollo,frieza,gohan,kiluha,pakistan,india,usa,united,unitedstate,unitedstates,united states,america,Pakistan,PAKISTAN,pak,ind,INDIA,{{name_keywords}}" />
    <meta property="og:url" content="https://princetoons.pythonanywhere.com/page1{% if current_page > 1 %}?page={{ current_page }}{% endif %}" />
    <meta property="og:type" content="website" />
    <meta name="twitter:card" content="summary_large_image" />
    
    <link rel="alternate" hreflang="en" href="https://princetoons.pythonanywhere.com/page1" />
    <link rel="alternate" hreflang="hi" href="https://princetoons.pythonanywhere.com/page1" />
    
    <!-- Breadcrumb Schema -->
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "BreadcrumbList",
      "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://princetoons.pythonanywhere.com/"},
        {"@type": "ListItem", "position": 2, "name": "Anime List", "item": "https://princetoons.pythonanywhere.com/page1"}
      ]
    }
    </script>
    
    <!-- CollectionPage Schema -->
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "CollectionPage",
      "name": "Hindi Dubbed Anime List",
      "description": "Browse all Hindi dubbed anime and movies at PRINCE TOONS.",
      "url": "https://princetoons.pythonanywhere.com/page1",
      "about": {
        "@type": "Thing",
        "name": "Anime"
      }
    }
    </script>
    
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { background-color: black; color: white; font-family: Arial, sans-serif; }
        
        a {
            text-decoration: none !important;
            color: inherit;
            -webkit-tap-highlight-color: transparent;
        }
        
        .header-table {
            margin: 0 auto;
            text-align: center;
            border-collapse: collapse;
            width: 100%;
            max-width: 600px;
        }
        
        .header-table td {
            padding: 10px 15px;
            vertical-align: middle;
        }
        
        .header-title {
            color: white;
            font-size: 30px;
        }
        
        .header-title:hover {
            color: #ffcc00;
            transition: 0.3s;
        }
        
        .toonimage {
            width: 75px;
            height: auto;
        }
        
        .logo-image {
            height: 80px;
            width: 90px;
        }
        
        .welcome-box {
            border-top: 2px solid;
            border-bottom: 2px solid;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100px;
            border-color: white;
            margin: 10px 0;
        }
        
        .welcome-inner {
            border: 2px solid;
            border-radius: 20px;
            width: 330px;
            height: 40px;
            display: flex;
            justify-content: center;
            align-items: center;
            border-color: white;
        }
        
        .welcome-text {
            margin: 0;
            font-size: 30px;
            color: white;
            font-weight: bold;
        }
        
        .search-button-container {
            display: flex;
            justify-content: center;
            margin: 15px 0;
        }
        
        .search-button {
            display: inline-block;
            border: 2px solid gold;
            border-radius: 30px;
            padding: 12px 30px;
            color: gold;
            font-size: 20px;
            font-weight: bold;
            text-decoration: none;
            transition: background-color 0.3s, transform 0.2s;
            cursor: pointer;
        }
        
        .search-button:hover {
            background-color: gold;
            color: black;
            transform: scale(1.05);
        }
        
        .anime-container {
            min-height: 220px;
            margin: 20px;
            padding: 10px;
            text-align: center;
        }
        
        .anime-image {
            background-position: center;
            background-size: cover;
            background-repeat: no-repeat;
            border-radius: 15px;
            width: 100%;
            max-width: 386px;
            height: 200px;
            margin: 0 auto;
        }
        
        .anime-title {
            font-size: 25px;
            color: white;
            margin-top: 10px;
        }
        
        .anime-meta {
            color: #aaa;
            font-size: 16px;
            margin-top: 5px;
        }
        
        .watch-button {
            display: flex;
            justify-content: center;
            border: 2px solid;
            border-radius: 65px;
            width: 100%;
            max-width: 386px;
            height: 35px;
            border-color: white;
            margin: 10px auto;
            cursor: pointer;
            transition: background-color 0.3s;
        }
        
        .watch-button:hover {
            background-color: #333;
        }
        
        .watch-text {
            font-size: 20px;
            text-align: center;
            position: relative;
            top: 5px;
            color: white;
        }
        
        .pagination {
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 15px;
            margin: 30px 0;
            padding: 10px;
            flex-wrap: wrap;
        }
        
        .pagination a {
            color: white;
            border: 2px solid white;
            border-radius: 10px;
            padding: 10px 20px;
            font-size: 20px;
            transition: background-color 0.3s;
        }
        
        .pagination a:hover {
            background-color: #333;
        }
        
        .pagination .current {
            color: gold;
            border-color: gold;
            padding: 10px 20px;
            font-size: 20px;
        }
        
        .page-info {
            text-align: center;
            color: gold;
            font-size: 18px;
            margin: 10px 0;
        }
        
        .breadcrumb {
            text-align: center;
            color: #888;
            font-size: 14px;
            padding: 10px;
        }
        
        .breadcrumb a {
            color: #aaa;
            text-decoration: none;
        }
        
        .breadcrumb a:hover {
            color: gold;
        }
        
        /* Social section */
        .social-row {
            display: flex;
            flex-wrap: nowrap;
            justify-content: center;
            align-items: center;
            gap: 0.8rem;
            padding: 0.8rem 1.2rem;
            background: rgba(255,255,255,0.05);
            backdrop-filter: blur(8px);
            border-radius: 50px;
            box-shadow: 0 15px 30px rgba(0,0,0,0.5);
            border: 1px solid rgba(255,255,255,0.08);
            width: fit-content;
            max-width: 100%;
            overflow: hidden;
            margin: 0 auto;
        }
        
        .social-row a {
            display: flex;
            align-items: center;
            justify-content: center;
            width: 60px;
            height: 60px;
            flex-shrink: 0;
            background: rgba(255,255,255,0.05);
            border-radius: 50%;
            border: 1px solid rgba(255,255,255,0.06);
            transition: all 0.3s ease;
            text-decoration: none;
            animation: float 3s ease-in-out infinite;
        }
        
        .social-row a:nth-child(1) { animation-delay: 0s; }
        .social-row a:nth-child(2) { animation-delay: 0.4s; }
        .social-row a:nth-child(3) { animation-delay: 0.8s; }
        .social-row a:nth-child(4) { animation-delay: 1.2s; }
        
        .social-row img {
            width: 38px;
            height: 38px;
            object-fit: contain;
            display: block;
            filter: drop-shadow(0 3px 6px rgba(0,0,0,0.3));
            border-radius: 6px;
            transition: transform 0.3s ease;
        }
        
        @keyframes float {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(-6px); }
        }
        
        .social-row a:hover {
            transform: scale(1.12) !important;
            background: rgba(255, 255, 255, 0.12);
            border-color: rgba(255, 255, 255, 0.18);
            box-shadow: 0 6px 20px rgba(0, 0, 0, 0.4);
            animation-play-state: paused;
        }
        
        .social-row a:hover img {
            transform: scale(1.05);
            filter: drop-shadow(0 4px 10px rgba(255, 255, 255, 0.12));
        }
        
        .social-row a:active {
            transform: scale(0.92) !important;
            transition-duration: 0.08s;
        }
        
        .back-to-top {
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: gold;
            color: black;
            padding: 10px 15px;
            border-radius: 50%;
            font-size: 20px;
            cursor: pointer;
            display: none;
            z-index: 999;
            transition: opacity 0.3s;
        }
        
        .back-to-top:hover {
            opacity: 0.8;
        }
        
        @media (max-width: 768px) {
            .header-title { font-size: 25px; }
            .header-table td { padding: 5px 10px; }
            .anime-image { max-width: 100%; }
            .watch-button { max-width: 100%; }
            .pagination a { padding: 8px 15px; font-size: 16px; }
            .pagination .current { padding: 8px 15px; font-size: 16px; }
            .search-button { padding: 10px 20px; font-size: 16px; }
            .welcome-inner { width: 280px; }
            .welcome-text { font-size: 24px; }
            .anime-title { font-size: 20px; }
            .social-row a { width: 50px; height: 50px; }
            .social-row img { width: 30px; height: 30px; }
            .social-row { gap: 0.5rem; padding: 0.6rem 1rem; }
        }
        
        @media (max-width: 480px) {
            .header-title { font-size: 20px; }
            .header-table td { padding: 3px 6px; }
            .anime-title { font-size: 17px; }
            .watch-text { font-size: 16px; }
            .pagination a { padding: 6px 12px; font-size: 14px; }
            .pagination .current { padding: 6px 12px; font-size: 14px; }
            .search-button { padding: 8px 15px; font-size: 14px; }
            .welcome-inner { width: 220px; height: 32px; }
            .welcome-text { font-size: 18px; }
            .social-row a { width: 42px; height: 42px; }
            .social-row img { width: 24px; height: 24px; }
            .social-row { gap: 0.4rem; padding: 0.5rem 0.8rem; }
            .page-info { font-size: 14px; }
        }
    </style>
</head>
<body>
    <header>
    <table class="header-table">
        <tr>
            <td>
                <a href='/page1' aria-label="Home Page">
                    <h1 class="header-title">HOME</h1>
                </a>
            </td>
            <td>
                <a href='/'>
                    <img class='toonimage logo-image' src="https://raw.githubusercontent.com/princehamzaytprogramming/princetoons/main/static/princetoons.png" alt='PRINCE TOONS Logo - Free Hindi Dubbed Anime Download Website' width="75" height="auto" loading="lazy">
                </a>
            </td>
            <td>
                <a href='/about' aria-label="About Page">
                    <h1 class="header-title">ABOUT</h1>
                </a>
            </td>
        </tr>
    </table>

    <div class="welcome-box">
        <div class="welcome-inner">
            <p class="welcome-text">• ANIME & MOVIES •</p>
        </div>
    </div>
    <br>
    </header>
    <main>
    <div class="breadcrumb">
        <a href="/">Home</a> › Anime List
    </div>
    
    <div class="search-button-container">
        <a href='/search' class="search-button" aria-label="Search for anime">🔍 SEARCH ANIME</a>
    </div>
    
    <h2 style="text-align:center;color:gold;font-size:22px;margin:20px 0;">All Hindi Dubbed Anime & Movies</h2>
    
    <div class="page-info">
        Page {{ current_page }} of {{ total_pages }} ({{ anime_list_reversed|length }} total anime)
    </div>
    
    {% for anime in page_anime %}
    <a href='/detail/{{ anime.slug }}' aria-label="{{ anime.title }} {{ anime.season }} details">
        <div style='margin-top:8px;margin-bottom:8px;' class="anime-container" itemscope itemtype="https://schema.org/VideoObject">
            <div class="anime-image" style="background-image: url('{{ anime.image_url }}');" role="img" aria-label="{{ anime.title }} poster image" loading="lazy"></div>
            <h2 class="anime-title" itemprop="name">{{ anime.title }} {{ anime.season }} Hindi</h2>
            <meta itemprop="description" content="{{ anime.description[:200] }}" />
            <meta itemprop="thumbnailUrl" content="{{ anime.image_url }}" />
            <meta itemprop="uploadDate" content="{{ anime.year }}" />
            
            <div class="watch-button">
                <p class="watch-text">WATCH/DOWNLOAD</p>
            </div>
        </div>
    </a>
    <br>
    {% endfor %}
    
    <div class="pagination">
        {% if current_page > 1 %}
            <a href="/page1?page={{ current_page - 1 }}" aria-label="Previous page" rel="prev">◀ PREV</a>
        {% endif %}
        
        <span class="current">{{ current_page }}</span>
        
        {% if current_page < total_pages %}
            <a href="/page1?page={{ current_page + 1 }}" aria-label="Next page" rel="next">NEXT ▶</a>
        {% endif %}
    </div>
    </main>
    <footer>
        <p style='font-weight:bold;text-align:center;font-size:20px;'>OWNER</p>
        <p style='font-weight:bold;text-align:center;font-size:20px;'>SOCIAL MEDIA</p>
        
        <div style="margin-top:0px;display:flex;justify-content:center;align-items:center;min-height:10vh;padding:1rem;">
            <div class="social-row">
                <a href='https://youtube.com/@princehamzayt6210' target="_blank" rel="noopener noreferrer nofollow" aria-label="YouTube Channel">
                    <img src="https://raw.githubusercontent.com/princehamzaytprogramming/princetoons/main/static/youtube.png" alt='Subscribe on YouTube' width="38" height="38" loading="lazy">
                </a>
                <a href='https://www.tiktok.com/@princehamza.yt' target="_blank" rel="noopener noreferrer nofollow" aria-label="TikTok Profile">
                    <img src="https://raw.githubusercontent.com/princehamzaytprogramming/princetoons/main/static/tiktok.png" alt='Follow on TikTok' width="38" height="38" loading="lazy">
                </a>
                <a href='https://www.instagram.com/princehmzayt' target="_blank" rel="noopener noreferrer nofollow" aria-label="Instagram Profile">
                    <img src="https://raw.githubusercontent.com/princehamzaytprogramming/princetoons/main/static/instagram.png" alt='Follow on Instagram' width="38" height="38" loading="lazy">
                </a>
                <a href='https://chat.whatsapp.com/HwvR3IcDg3gIgMUsnB90ss?s=cl&p=a&ilr=4' target="_blank" rel="noopener noreferrer nofollow" aria-label="WhatsApp Group">
                    <img src="https://raw.githubusercontent.com/princehamzaytprogramming/princetoons/main/static/whatsapp.png" alt='Join WhatsApp Group' width="38" height="38" loading="lazy">
                </a>
            </div>
        </div>
    </footer>
    
    <button onclick="topFunction()" id="backToTop" class="back-to-top" title="Back to top">↑</button>
    
    <script>
        // Back to top button
        var mybutton = document.getElementById("backToTop");
        window.onscroll = function() {scrollFunction()};
        function scrollFunction() {
            if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
                mybutton.style.display = "block";
            } else {
                mybutton.style.display = "none";
            }
        }
        function topFunction() {
            document.body.scrollTop = 0;
            document.documentElement.scrollTop = 0;
        }
    </script>
</body>
</html>
'''

# ============================================
# [DETAIL PAGE - SEO Enhanced with H1, breadcrumbs, schema, related anime]
# ============================================

detail_template = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    
    <meta name="google-site-verification" content="0nVOqCF33huAKgNcWE-zEjGHLpQj_FRtPjPPkdt5Gu0" />
    <meta name="author" content="PRINCE TOONS" />
    <meta name="robots" content="index, follow" />
    
    <title>{{ page_title }}</title>
    <meta name="description" content="{{ meta_description }}" />
    
    <link rel="canonical" href="https://princetoons.pythonanywhere.com/detail/{{ anime.slug }}" />
    
    <meta property="og:title" content="{{ anime.title }} {{ anime.season }} Hindi Dubbed - PRINCE TOONS" />
    <meta property="og:description" content="{{ anime.description[:160] }}" />
    <meta property="og:image" content="{{ anime.image_url }}" />
    <meta name="keywords" content="anime,cartoon,toon,toons,movie,movies,animes,hindi,Hindi,HINDI,urdu,Urdu,URDU,english,English,ENGLISH,sub,dub,subbed,dubbed,Sub,Dub,SUBBED,DUBBED,english sub,english dub,urdu sub,urdu dub,hindi sub,hindi dub,english subbed,english dubbed,urdu subbed,urdu dubbed,hindi subbed,hindi dubbed,HINDI SUB,HINDI DUB,HINDI SUBBED,HINDI DUBBED,2d,3d,2dcartoon,3dcartoon,2danime,3danime,prince,Prince,PRINCE,toon,toons,Toon,Toons,TOONS,princetoon,princetoons,PrinceToon,PrinceToons,PRINCETOON,PRINCETOONS,prince toon,prince toons,Prince Toon,Prince Toons,PRINCE TOON,PRINCE TOONS,princeanime,prince anime,PrinceAnime,Prince Anime,PRINCEANIME,PRINCE ANIME,Cartoon,cartoon,cartoons,CARTOON,CARTOONS,animename,anime name,AnimeName,Anime Name,new,old,80s,90s,20s,newanime,New Anime,new anime,oldanime,Old Anime,old anime,newtoon,oldtoon,newtoons,oldtoons,new toons,old toons,princetoonswebsite,princetoonsweb,prince toons web,prince toons website,princetoonanime,princetoonsanime,prince toon anime,prince toons anime,PrinceToonAnime,PrinceToonsAnime,princetoonreview,princetoonsreview,prince toons review,good,verygood,normal,average,exelent,characters,goku,kakarot,vegeta,gon,boboiboy,naruto,saska,kakashi,itachi,madara,bleach,gojo,sakuna,yuji,isagi,nagi,barou,bachira,rin,sae,chigiri,spider,spiderman,miles,peter,peter parker,gopal,yaya,krillen,yamcha,picollo,frieza,gohan,kiluha,pakistan,india,usa,united,unitedstate,unitedstates,united states,america,Pakistan,PAKISTAN,pak,ind,INDIA,{{name_keywords}}" />
    <meta property="og:url" content="https://princetoons.pythonanywhere.com/detail/{{ anime.slug }}" />
    <meta property="og:type" content="video.episode" />
    <meta property="og:site_name" content="PRINCE TOONS" />
    <meta property="og:updated_time" content="{{ current_date }}" />
    
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:title" content="{{ anime.title }} {{ anime.season }} Hindi Dubbed" />
    <meta name="twitter:description" content="{{ anime.description[:160] }}" />
    <meta name="twitter:image" content="{{ anime.image_url }}" />
    
    <link rel="alternate" hreflang="en" href="https://princetoons.pythonanywhere.com/detail/{{ anime.slug }}" />
    <link rel="alternate" hreflang="hi" href="https://princetoons.pythonanywhere.com/detail/{{ anime.slug }}" />
    
    <!-- Breadcrumb Schema -->
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "BreadcrumbList",
      "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://princetoons.pythonanywhere.com/"},
        {"@type": "ListItem", "position": 2, "name": "Anime List", "item": "https://princetoons.pythonanywhere.com/page1"},
        {"@type": "ListItem", "position": 3, "name": "{{ anime.title }}", "item": "https://princetoons.pythonanywhere.com/detail/{{ anime.slug }}"}
      ]
    }
    </script>
    
    <!-- VideoObject Schema -->
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "VideoObject",
      "name": "{{ anime.title }} {{ anime.season }} Hindi Dubbed",
      "description": "{{ anime.description[:200] }}",
      "thumbnailUrl": "{{ anime.image_url }}",
      "uploadDate": "{{ anime.year }}",
      "duration": "PT{{ anime.episodes * 24 }}M",
      "contentUrl": "{% if anime.download_links %}{{ anime.download_links[0].url }}{% endif %}",
      "embedUrl": "https://princetoons.pythonanywhere.com/detail/{{ anime.slug }}",
      "publisher": {
        "@type": "Organization",
        "name": "PRINCE TOONS"
      },
      "interactionStatistic": {
        "@type": "InteractionCounter",
        "interactionType": "https://schema.org/WatchAction"
      }
    }
    </script>
    
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { background-color: black; color: white; font-family: Arial, sans-serif; }
        
        a {
            text-decoration: none !important;
            color: inherit;
            -webkit-tap-highlight-color: transparent;
        }
        
        .header-table {
            margin: 0 auto;
            text-align: center;
            border-collapse: collapse;
            width: 100%;
            max-width: 600px;
        }
        
        .header-table td {
            padding: 10px 15px;
            vertical-align: middle;
        }
        
        .header-title {
            color: white;
            font-size: 30px;
        }
        
        .header-title:hover {
            color: #ffcc00;
            transition: 0.3s;
        }
        
        .toonimage {
            width: 75px;
            height: auto;
        }
        
        .logo-image {
            height: 80px;
            width: 90px;
        }
        
        .welcome-box {
            border-top: 2px solid;
            border-bottom: 2px solid;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100px;
            border-color: white;
            margin: 10px 0;
        }
        
        .welcome-inner {
            border: 2px solid;
            border-radius: 20px;
            width: 330px;
            height: 40px;
            display: flex;
            justify-content: center;
            align-items: center;
            border-color: white;
        }
        
        .welcome-text {
            margin: 0;
            font-size: 40px;
            color: white;
        }
        
        .search-button-container {
            display: flex;
            justify-content: center;
            margin: 15px 0;
        }
        
        .search-button {
            display: inline-block;
            border: 2px solid gold;
            border-radius: 30px;
            padding: 12px 30px;
            color: gold;
            font-size: 20px;
            font-weight: bold;
            text-decoration: none;
            transition: background-color 0.3s, transform 0.2s;
            cursor: pointer;
        }
        
        .search-button:hover {
            background-color: gold;
            color: black;
            transform: scale(1.05);
        }
        
        .breadcrumb {
            text-align: center;
            color: #888;
            font-size: 14px;
            padding: 10px;
        }
        
        .breadcrumb a {
            color: #aaa;
            text-decoration: none;
        }
        
        .breadcrumb a:hover {
            color: gold;
        }
        
        .detail-container {
            text-align: center;
            border: 2px solid;
            border-radius: 60px;
            margin: 20px;
            padding: 20px;
            border-color: white;
        }
        
        .detail-title {
            font-size: 17px;
            font-weight: 700;
            color: gold;
        }
        
        .anime-name {
            font-size: 25px;
            color: white;
            margin: 20px 0 10px 0;
        }
        
        .anime-season {
            font-size: 30px;
            color: white;
            margin: 10px 0;
        }
        
        .anime-dub {
            font-size: 30px;
            color: white;
            margin: 10px 0;
        }
        
        .anime-year {
            font-size: 18px;
            color: #aaa;
            margin: 5px 0;
        }
        
        .anime-episodes {
            font-size: 18px;
            color: #aaa;
            margin: 5px 0;
        }
        
        .anime-description {
            font-size: 16px;
            color: #ddd;
            margin: 15px 20px;
            line-height: 1.6;
            text-align: left;
            max-width: 600px;
            margin-left: auto;
            margin-right: auto;
        }
        
        .anime-image-detail {
            background-position: center;
            background-size: cover;
            background-repeat: no-repeat;
            border-radius: 15px;
            width: 100%;
            max-width: 389px;
            height: 200px;
            margin: 20px auto;
        }
        
        .download-links {
            color: gold;
            font-weight: bold;
            margin: 20px 0;
        }
        
        .download-buttons {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 15px;
            margin: 20px 0;
            outline: none;
            -webkit-tap-highlight-color: transparent;
        }
        
        .download-button {
            display: flex;
            justify-content: center;
            align-items: center;
            border: 2px solid;
            border-radius: 40px;
            height: 50px;
            width: 200px;
            border-color: white;
            transition: background-color 0.3s, transform 0.2s;
            cursor: pointer;
            outline: none;
            -webkit-tap-highlight-color: transparent;
        }
        
        .download-button:hover {
            transform: scale(1.05);
        }
        
        .download-button a {
            color: white;
            text-decoration: none;
            font-size: 18px;
            font-weight: bold;
            width: 100%;
            height: 100%;
            display: flex;
            justify-content: center;
            align-items: center;
            outline: none;
            -webkit-tap-highlight-color: transparent;
        }
        
        .download-mega { border-color: #ff0066; }
        .download-mega a { color: #ff0066; }
        .download-mega:hover { background-color: #ff006622; }
        
        .download-pixeldrain { border-color: #00ccff; }
        .download-pixeldrain a { color: #00ccff; }
        .download-pixeldrain:hover { background-color: #00ccff22; }
        
        .download-mediafire { border-color: #ff9900; }
        .download-mediafire a { color: #ff9900; }
        .download-mediafire:hover { background-color: #ff990022; }
        
        .download-googledrive { border-color: #00ff00; }
        .download-googledrive a { color: #00ff00; }
        .download-googledrive:hover { background-color: #00ff0022; }
        
        .download-hub { border-color: #ff00ff; }
        .download-hub a { color: #ff00ff; }
        .download-hub:hover { background-color: #ff00ff22; }
        
        .download-zippyfire { border-color: #ff6600; }
        .download-zippyfire a { color: #ff6600; }
        .download-zippyfire:hover { background-color: #ff660022; }
        
        .download-default { border-color: #ffffff; }
        .download-default a { color: #ffffff; }
        .download-default:hover { background-color: #ffffff22; }
        
        .no-links {
            color: #666;
            font-size: 18px;
            margin: 15px 0;
        }
        
        .back-link {
            display: inline-block;
            border: 2px solid white;
            border-radius: 30px;
            padding: 10px 30px;
            color: white;
            font-size: 18px;
            transition: all 0.3s;
            margin: 20px 0;
        }
        
        .back-link:hover {
            background-color: white;
            color: black;
        }
        
        .related-anime {
            margin: 30px 20px;
            padding: 20px;
            border-top: 2px solid #333;
        }
        
        .related-anime h3 {
            color: gold;
            text-align: center;
            font-size: 24px;
            margin-bottom: 20px;
        }
        
        .related-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
            max-width: 600px;
            margin: 0 auto;
        }
        
        .related-item {
            background: #1a1a1a;
            border-radius: 10px;
            padding: 10px;
            text-align: center;
            transition: transform 0.3s;
        }
        
        .related-item:hover {
            transform: scale(1.05);
            background: #2a2a2a;
        }
        
        .related-item img {
            width: 100%;
            height: 100px;
            object-fit: cover;
            border-radius: 8px;
        }
        
        .related-item p {
            color: #aaa;
            font-size: 12px;
            margin-top: 5px;
        }
        
        .social-row {
            display: flex;
            flex-wrap: nowrap;
            justify-content: center;
            align-items: center;
            gap: 0.8rem;
            padding: 0.8rem 1.2rem;
            background: rgba(255,255,255,0.05);
            backdrop-filter: blur(8px);
            border-radius: 50px;
            box-shadow: 0 15px 30px rgba(0,0,0,0.5);
            border: 1px solid rgba(255,255,255,0.08);
            width: fit-content;
            max-width: 100%;
            overflow: hidden;
            margin: 0 auto;
        }
        
        .social-row a {
            display: flex;
            align-items: center;
            justify-content: center;
            width: 60px;
            height: 60px;
            flex-shrink: 0;
            background: rgba(255,255,255,0.05);
            border-radius: 50%;
            border: 1px solid rgba(255,255,255,0.06);
            transition: all 0.3s ease;
            text-decoration: none;
            animation: float 3s ease-in-out infinite;
        }
        
        .social-row a:nth-child(1) { animation-delay: 0s; }
        .social-row a:nth-child(2) { animation-delay: 0.4s; }
        .social-row a:nth-child(3) { animation-delay: 0.8s; }
        .social-row a:nth-child(4) { animation-delay: 1.2s; }
        
        .social-row img {
            width: 38px;
            height: 38px;
            object-fit: contain;
            display: block;
            filter: drop-shadow(0 3px 6px rgba(0,0,0,0.3));
            border-radius: 6px;
            transition: transform 0.3s ease;
        }
        
        @keyframes float {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(-6px); }
        }
        
        .social-row a:hover {
            transform: scale(1.12) !important;
            background: rgba(255, 255, 255, 0.12);
            border-color: rgba(255, 255, 255, 0.18);
            box-shadow: 0 6px 20px rgba(0, 0, 0, 0.4);
            animation-play-state: paused;
        }
        
        .social-row a:hover img {
            transform: scale(1.05);
            filter: drop-shadow(0 4px 10px rgba(255, 255, 255, 0.12));
        }
        
        .social-row a:active {
            transform: scale(0.92) !important;
            transition-duration: 0.08s;
        }
        
        .back-to-top {
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: gold;
            color: black;
            padding: 10px 15px;
            border-radius: 50%;
            font-size: 20px;
            cursor: pointer;
            display: none;
            z-index: 999;
            transition: opacity 0.3s;
        }
        
        .back-to-top:hover {
            opacity: 0.8;
        }
        
        @media (max-width: 768px) {
            .header-title { font-size: 25px; }
            .header-table td { padding: 5px 10px; }
            .anime-image-detail { max-width: 100%; }
            .anime-description { font-size: 14px; margin: 10px; }
            .detail-container { margin: 10px; padding: 15px; }
            .download-button { width: 160px; height: 45px; }
            .download-button a { font-size: 16px; }
            .search-button { padding: 10px 20px; font-size: 16px; }
            .welcome-inner { width: 280px; }
            .welcome-text { font-size: 30px; }
            .social-row a { width: 50px; height: 50px; }
            .social-row img { width: 30px; height: 30px; }
            .social-row { gap: 0.5rem; padding: 0.6rem 1rem; }
            .related-grid { grid-template-columns: repeat(auto-fit, minmax(120px, 1fr)); }
        }
        
        @media (max-width: 480px) {
            .header-title { font-size: 20px; }
            .header-table td { padding: 3px 6px; }
            .anime-name { font-size: 20px; }
            .anime-season { font-size: 22px; }
            .anime-dub { font-size: 22px; }
            .anime-description { font-size: 13px; margin: 8px; }
            .detail-container { margin: 8px; padding: 12px; border-radius: 30px; }
            .download-button { width: 140px; height: 40px; }
            .download-button a { font-size: 14px; }
            .search-button { padding: 8px 15px; font-size: 14px; }
            .welcome-inner { width: 220px; height: 32px; }
            .welcome-text { font-size: 22px; }
            .social-row a { width: 42px; height: 42px; }
            .social-row img { width: 24px; height: 24px; }
            .social-row { gap: 0.4rem; padding: 0.5rem 0.8rem; }
            .back-link { padding: 8px 20px; font-size: 14px; }
            .related-grid { grid-template-columns: repeat(auto-fit, minmax(100px, 1fr)); }
        }
    </style>
</head>
<body>
    <header>
    <table class="header-table">
        <tr>
            <td>
                <a href='/page1' aria-label="Home Page">
                    <h1 class="header-title">HOME</h1>
                </a>
            </td>
            <td>
                <a href='/'>
                    <img class='toonimage logo-image' src="https://raw.githubusercontent.com/princehamzaytprogramming/princetoons/main/static/princetoons.png" alt='PRINCE TOONS Logo - Free Hindi Dubbed Anime Download Website' width="75" height="auto" loading="lazy">
                </a>
            </td>
            <td>
                <a href='/about' aria-label="About Page">
                    <h1 class="header-title">ABOUT</h1>
                </a>
            </td>
        </tr>
    </table>

    <div class="welcome-box">
        <div class="welcome-inner">
            <h1 class="welcome-text">• ANIME •</h1>
        </div>
    </div>
    <br>
    </header>
    <main>
    <div class="breadcrumb">
        <a href="/">Home</a> › <a href="/page1">Anime List</a> › <span style="color:gold;">{{ anime.title }}</span>
    </div>
    
    <div class="search-button-container">
        <a href='/search' class="search-button" aria-label="Search for anime">🔍 SEARCH ANIME</a>
    </div>
    
    <div class="detail-container" itemscope itemtype="https://schema.org/VideoObject">
        <u class="detail-title">• ANIME DETAILS •</u>
        
        <h1 class="anime-name" itemprop="name">
            {{ anime.title }}
        </h1>
        
        <div class="anime-season">
            <p><u>{{ anime.season }}</u></p>
        </div>
        
        <div class="anime-dub">
            <p><u>HINDI DUBBED</u></p>
        </div>
        
        <div class="anime-image-detail" style="background-image: url('{{ anime.image_url }}');" role="img" aria-label="{{ anime.title }} poster image" loading="lazy" itemprop="thumbnailUrl"></div>
        
        <div class="anime-description" itemprop="description">
            <p>{{ anime.description }}</p>
        </div>
        
        
        
        <div class="download-links">
            <u>⬇️ DOWNLOAD LINKS ⬇️</u>
        </div>
        
        <div class="download-buttons">
            {% if anime.download_links %}
                {% for link in anime.download_links %}
                    {% if link.url and link.url.strip() %}
                        {% set link_name = link.name|lower %}
                        {% if 'mega' in link_name %}
                            {% set button_class = 'download-mega' %}
                        {% elif 'pixel' in link_name or 'pixeldrain' in link_name %}
                            {% set button_class = 'download-pixeldrain' %}
                        {% elif 'mediafire' in link_name %}
                            {% set button_class = 'download-mediafire' %}
                        {% elif 'google' in link_name or 'drive' in link_name %}
                            {% set button_class = 'download-googledrive' %}
                        {% elif 'hub' in link_name %}
                            {% set button_class = 'download-hub' %}
                        {% elif 'zippy' in link_name %}
                            {% set button_class = 'download-zippyfire' %}
                        {% else %}
                            {% set button_class = 'download-default' %}
                        {% endif %}
                        
                        <div class="download-button {{ button_class }}">
                            <a href="{{ link.url }}" target="_blank" rel="noopener noreferrer nofollow" itemprop="contentUrl">
                                {{ link.name|upper }}
                            </a>
                        </div>
                    {% endif %}
                {% endfor %}
            {% else %}
                <p class="no-links">No download links available</p>
            {% endif %}
        </div>
        
        <a href="/page1" class="back-link" aria-label="Back to anime list">← BACK TO ANIME</a>
    </div>
    
    </main>
    
    <footer>
        <p style='font-weight:bold;text-align:center;font-size:20px;'>OWNER</p>
        <p style='font-weight:bold;text-align:center;font-size:20px;'>SOCIAL MEDIA</p>
        
        <div style="margin-top:0px;display:flex;justify-content:center;align-items:center;min-height:10vh;padding:1rem;">
            <div class="social-row">
                <a href='https://youtube.com/@princehamzayt6210' target="_blank" rel="noopener noreferrer nofollow" aria-label="YouTube Channel">
                    <img src="https://raw.githubusercontent.com/princehamzaytprogramming/princetoons/main/static/youtube.png" alt='Subscribe on YouTube' width="38" height="38" loading="lazy">
                </a>
                <a href='https://www.tiktok.com/@princehamza.yt' target="_blank" rel="noopener noreferrer nofollow" aria-label="TikTok Profile">
                    <img src="https://raw.githubusercontent.com/princehamzaytprogramming/princetoons/main/static/tiktok.png" alt='Follow on TikTok' width="38" height="38" loading="lazy">
                </a>
                <a href='https://www.instagram.com/princehmzayt' target="_blank" rel="noopener noreferrer nofollow" aria-label="Instagram Profile">
                    <img src="https://raw.githubusercontent.com/princehamzaytprogramming/princetoons/main/static/instagram.png" alt='Follow on Instagram' width="38" height="38" loading="lazy">
                </a>
                <a href='https://chat.whatsapp.com/HwvR3IcDg3gIgMUsnB90ss?s=cl&p=a&ilr=4' target="_blank" rel="noopener noreferrer nofollow" aria-label="WhatsApp Group">
                    <img src="https://raw.githubusercontent.com/princehamzaytprogramming/princetoons/main/static/whatsapp.png" alt='Join WhatsApp Group' width="38" height="38" loading="lazy">
                </a>
            </div>
        </div>
    </footer>
    
    <button onclick="topFunction()" id="backToTop" class="back-to-top" title="Back to top">↑</button>
    
    <script>
        // Back to top button
        var mybutton = document.getElementById("backToTop");
        window.onscroll = function() {scrollFunction()};
        function scrollFunction() {
            if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
                mybutton.style.display = "block";
            } else {
                mybutton.style.display = "none";
            }
        }
        function topFunction() {
            document.body.scrollTop = 0;
            document.documentElement.scrollTop = 0;
        }
    </script>
</body>
</html>
'''

# ============================================
# SEARCH PAGE - SEO Enhanced
# ============================================

search_template = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    
    <meta name="google-site-verification" content="0nVOqCF33huAKgNcWE-zEjGHLpQj_FRtPjPPkdt5Gu0" />
    <meta name="robots" content="index, follow" />
    
    <title>{{ page_title }}</title>
    <meta name="description" content="{{ meta_description }}" />
    
    <link rel="canonical" href="https://princetoons.pythonanywhere.com/search" />
    
    <meta property="og:title" content="{{ page_title }}" />
    <meta property="og:description" content="{{ meta_description }}" />
    <meta property="og:image" content="https://raw.githubusercontent.com/princehamzaytprogramming/princetoons/main/static/princetoons.png" />
    <meta name="keywords" content="anime,cartoon,toon,toons,movie,movies,animes,hindi,Hindi,HINDI,urdu,Urdu,URDU,english,English,ENGLISH,sub,dub,subbed,dubbed,Sub,Dub,SUBBED,DUBBED,english sub,english dub,urdu sub,urdu dub,hindi sub,hindi dub,english subbed,english dubbed,urdu subbed,urdu dubbed,hindi subbed,hindi dubbed,HINDI SUB,HINDI DUB,HINDI SUBBED,HINDI DUBBED,2d,3d,2dcartoon,3dcartoon,2danime,3danime,prince,Prince,PRINCE,toon,toons,Toon,Toons,TOONS,princetoon,princetoons,PrinceToon,PrinceToons,PRINCETOON,PRINCETOONS,prince toon,prince toons,Prince Toon,Prince Toons,PRINCE TOON,PRINCE TOONS,princeanime,prince anime,PrinceAnime,Prince Anime,PRINCEANIME,PRINCE ANIME,Cartoon,cartoon,cartoons,CARTOON,CARTOONS,animename,anime name,AnimeName,Anime Name,new,old,80s,90s,20s,newanime,New Anime,new anime,oldanime,Old Anime,old anime,newtoon,oldtoon,newtoons,oldtoons,new toons,old toons,princetoonswebsite,princetoonsweb,prince toons web,prince toons website,princetoonanime,princetoonsanime,prince toon anime,prince toons anime,PrinceToonAnime,PrinceToonsAnime,princetoonreview,princetoonsreview,prince toons review,good,verygood,normal,average,exelent,characters,goku,kakarot,vegeta,gon,boboiboy,naruto,saska,kakashi,itachi,madara,bleach,gojo,sakuna,yuji,isagi,nagi,barou,bachira,rin,sae,chigiri,spider,spiderman,miles,peter,peter parker,gopal,yaya,krillen,yamcha,picollo,frieza,gohan,kiluha,pakistan,india,usa,united,unitedstate,unitedstates,united states,america,Pakistan,PAKISTAN,pak,ind,INDIA,{{name_keywords}}" />
    
    <meta property="og:url" content="https://princetoons.pythonanywhere.com/search" />
    <meta property="og:type" content="website" />
    <meta name="twitter:card" content="summary_large_image" />
    
    <!-- SearchAction Schema -->
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "WebSite",
      "url": "https://princetoons.pythonanywhere.com/",
      "potentialAction": {
        "@type": "SearchAction",
        "target": "https://princetoons.pythonanywhere.com/search?q={search_term_string}",
        "query-input": "required name=search_term_string"
      }
    }
    </script>
    
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { background-color: black; color: white; font-family: Arial, sans-serif; }
        a { text-decoration: none; color: inherit; }
        
        .header-table {
            margin: 0 auto;
            text-align: center;
            border-collapse: collapse;
            width: 100%;
            max-width: 600px;
        }
        .header-table td { padding: 10px 15px; vertical-align: middle; }
        .header-title { color: white; font-size: 30px; }
        .header-title:hover { color: #ffcc00; transition: 0.3s; }
        .toonimage { width: 75px; height: auto; }
        .logo-image { height: 80px; width: 90px; }
        
        .welcome-box {
            border-top: 2px solid;
            border-bottom: 2px solid;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100px;
            border-color: white;
            margin: 10px 0;
        }
        .welcome-inner {
            border: 2px solid;
            border-radius: 20px;
            width: 330px;
            height: 40px;
            display: flex;
            justify-content: center;
            align-items: center;
            border-color: white;
        }
        .welcome-text { margin: 0; font-size: 30px; color: white; font-weight: bold; }
        
        .search-container {
            max-width: 600px;
            margin: 30px auto;
            padding: 20px;
            text-align: center;
        }
        
        .search-box {
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            gap: 10px;
            margin: 20px 0;
        }
        
        .search-input {
            padding: 12px 20px;
            border-radius: 30px;
            border: 2px solid gold;
            background-color: #1a1a1a;
            color: white;
            font-size: 18px;
            width: 70%;
            max-width: 400px;
            outline: none;
        }
        
        .search-input:focus {
            border-color: #ffd700;
            box-shadow: 0 0 15px rgba(255, 215, 0, 0.3);
        }
        
        .search-submit {
            padding: 12px 30px;
            border-radius: 30px;
            border: 2px solid gold;
            background-color: gold;
            color: black;
            font-size: 18px;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s;
        }
        
        .search-submit:hover {
            background-color: transparent;
            color: gold;
            transform: scale(1.05);
        }
        
        .results-container {
            max-width: 600px;
            margin: 20px auto;
            padding: 0 20px;
        }
        
        .result-item {
            border: 2px solid #333;
            border-radius: 15px;
            padding: 15px;
            margin: 15px 0;
            transition: border-color 0.3s;
            cursor: pointer;
        }
        
        .result-item:hover {
            border-color: gold;
        }
        
        .result-title {
            font-size: 20px;
            color: gold;
        }
        
        .result-season {
            color: #aaa;
            font-size: 16px;
        }
        
        .result-meta {
            color: #666;
            font-size: 14px;
            margin-top: 5px;
        }
        
        .no-results {
            color: #666;
            font-size: 20px;
            margin: 40px 0;
        }
        
        .back-button {
            display: inline-block;
            border: 2px solid white;
            border-radius: 30px;
            padding: 10px 30px;
            color: white;
            font-size: 18px;
            transition: all 0.3s;
            margin: 20px 0;
        }
        
        .back-button:hover {
            background-color: white;
            color: black;
        }
        
        .breadcrumb {
            text-align: center;
            color: #888;
            font-size: 14px;
            padding: 10px;
        }
        
        .breadcrumb a {
            color: #aaa;
            text-decoration: none;
        }
        
        .breadcrumb a:hover {
            color: gold;
        }
        
        .popular-tags {
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            gap: 10px;
            margin: 20px 0;
        }
        
        .popular-tags a {
            background: #1a1a1a;
            padding: 8px 15px;
            border-radius: 20px;
            color: #aaa;
            font-size: 14px;
            transition: all 0.3s;
            border: 1px solid #333;
        }
        
        .popular-tags a:hover {
            background: gold;
            color: black;
            border-color: gold;
        }
        
        @media (max-width: 768px) {
            .header-title { font-size: 25px; }
            .search-input { width: 100%; font-size: 16px; }
            .search-submit { width: 100%; }
            .result-title { font-size: 17px; }
            .welcome-inner { width: 280px; }
            .welcome-text { font-size: 24px; }
        }
        
        @media (max-width: 480px) {
            .header-title { font-size: 20px; }
            .header-table td { padding: 3px 6px; }
            .welcome-inner { width: 220px; height: 32px; }
            .welcome-text { font-size: 18px; }
            .search-input { font-size: 14px; padding: 10px 15px; }
            .search-submit { font-size: 14px; padding: 10px 20px; }
            .result-title { font-size: 15px; }
            .result-season { font-size: 13px; }
        }
    </style>
</head>
<body>
    <header>
    <table class="header-table">
        <tr>
            <td><a href='/page1' aria-label="Home Page"><h1 class="header-title">HOME</h1></a></td>
            <td><a href='/'><img class='toonimage logo-image' src="https://raw.githubusercontent.com/princehamzaytprogramming/princetoons/main/static/princetoons.png" alt='PRINCE TOONS Logo - Free Hindi Dubbed Anime Download Website' width="75" height="auto" loading="lazy"></a></td>
            <td><a href='/about' aria-label="About Page"><h1 class="header-title">ABOUT</h1></a></td>
        </tr>
    </table>
    
    <div class="welcome-box">
        <div class="welcome-inner">
            <p class="welcome-text">• SEARCH ANIME •</p>
        </div>
    </div>
    </header>
    <main>
    <div class="breadcrumb">
        <a href="/">Home</a> › Search
    </div>
    
    <div class="search-container">
        <form method="GET" action="/search" class="search-box" role="search">
            <input type="text" name="q" class="search-input" placeholder="Search anime title, genre, or keyword..." value="{{ query|default('') }}" aria-label="Search for anime">
            <button type="submit" class="search-submit" aria-label="Submit search">🔍 SEARCH</button>
        </form>
        
        <div class="popular-tags">
            <strong style="color:#888;margin-right:10px;">Popular:</strong>
            <a href="/search?q=action">Action</a>
            <a href="/search?q=comedy">Comedy</a>
            <a href="/search?q=fantasy">Fantasy</a>
            <a href="/search?q=sports">Sports</a>
            <a href="/search?q=reincarnation">Reincarnation</a>
            <a href="/search?q=movie">Movies</a>
            <a href="/search?q=season">Series</a>
        </div>
    </div>
    
    <div class="results-container">
        {% if query %}
            {% if results %}
                <p style="color: #aaa; text-align: center; margin-bottom: 20px;">Found {{ results|length }} result(s) for "{{ query }}"</p>
                {% for anime in results %}
                    <a href="/detail/{{ anime.slug }}" aria-label="{{ anime.title }} details">
                        <div class="result-item" itemscope itemtype="https://schema.org/VideoObject">
                            <div class="result-title" itemprop="name">{{ anime.title }}</div>
                            <div class="result-season">{{ anime.season }} • Hindi Dubbed</div>
                            <div class="result-meta">{{ anime.year }} • {{ anime.episodes }} Episodes</div>
                            <meta itemprop="description" content="{{ anime.description[:200] }}" />
                            <meta itemprop="thumbnailUrl" content="{{ anime.image_url }}" />
                        </div>
                    </a>
                {% endfor %}
            {% else %}
                <p class="no-results">😕 No results found for "{{ query }}"</p>
                <p style="color: #666; text-align: center;">Try searching for anime like "Attack on Titan", "Jujutsu Kaisen", or "Re:Zero"</p>
            {% endif %}
            <div style="text-align: center;">
                <a href="/search" class="back-button" aria-label="Clear search">← CLEAR SEARCH</a>
            </div>
        {% else %}
            <p style="color: #666; text-align: center; font-size: 18px;">🔍 Enter an anime title, genre, or keyword to search</p>
            <p style="color: #444; text-align: center; font-size: 14px; margin-top: 10px;">Popular searches: Action, Comedy, Fantasy, Sports, Reincarnation</p>
        {% endif %}
    </div>
    </main>
</body>
</html>
'''

# ============================================
# ABOUT PAGE - SEO Enhanced
# ============================================

about_page = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    
    <meta name="google-site-verification" content="0nVOqCF33huAKgNcWE-zEjGHLpQj_FRtPjPPkdt5Gu0" />
    <meta name="robots" content="index, follow" />
    <meta name="author" content="PRINCE TOONS" />
    
    <title>{{ page_title }}</title>
    <meta name="description" content="{{ meta_description }}" />
    
    <link rel="canonical" href="https://princetoons.pythonanywhere.com/about" />
    
    <meta property="og:title" content="About PRINCE TOONS - DMCA Policy & Terms" />
    <meta property="og:description" content="{{ meta_description }}" />
    <meta property="og:image" content="https://raw.githubusercontent.com/princehamzaytprogramming/princetoons/main/static/princetoons.png" />
    <meta name="keywords" content="anime,cartoon,toon,toons,movie,movies,animes,hindi,Hindi,HINDI,urdu,Urdu,URDU,english,English,ENGLISH,sub,dub,subbed,dubbed,Sub,Dub,SUBBED,DUBBED,english sub,english dub,urdu sub,urdu dub,hindi sub,hindi dub,english subbed,english dubbed,urdu subbed,urdu dubbed,hindi subbed,hindi dubbed,HINDI SUB,HINDI DUB,HINDI SUBBED,HINDI DUBBED,2d,3d,2dcartoon,3dcartoon,2danime,3danime,prince,Prince,PRINCE,toon,toons,Toon,Toons,TOONS,princetoon,princetoons,PrinceToon,PrinceToons,PRINCETOON,PRINCETOONS,prince toon,prince toons,Prince Toon,Prince Toons,PRINCE TOON,PRINCE TOONS,princeanime,prince anime,PrinceAnime,Prince Anime,PRINCEANIME,PRINCE ANIME,Cartoon,cartoon,cartoons,CARTOON,CARTOONS,animename,anime name,AnimeName,Anime Name,new,old,80s,90s,20s,newanime,New Anime,new anime,oldanime,Old Anime,old anime,newtoon,oldtoon,newtoons,oldtoons,new toons,old toons,princetoonswebsite,princetoonsweb,prince toons web,prince toons website,princetoonanime,princetoonsanime,prince toon anime,prince toons anime,PrinceToonAnime,PrinceToonsAnime,princetoonreview,princetoonsreview,prince toons review,good,verygood,normal,average,exelent,characters,goku,kakarot,vegeta,gon,boboiboy,naruto,saska,kakashi,itachi,madara,bleach,gojo,sakuna,yuji,isagi,nagi,barou,bachira,rin,sae,chigiri,spider,spiderman,miles,peter,peter parker,gopal,yaya,krillen,yamcha,picollo,frieza,gohan,kiluha,pakistan,india,usa,united,unitedstate,unitedstates,united states,america,Pakistan,PAKISTAN,pak,ind,INDIA,{{name_keywords}}" />
    
    <meta property="og:url" content="https://princetoons.pythonanywhere.com/about" />
    <meta property="og:type" content="website" />
    <meta name="twitter:card" content="summary_large_image" />
    
    <!-- AboutPage Schema -->
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "AboutPage",
      "name": "About PRINCE TOONS",
      "description": "Learn about PRINCE TOONS - Your source for Hindi dubbed anime and movies.",
      "url": "https://princetoons.pythonanywhere.com/about",
      "mainEntity": {
        "@type": "Organization",
        "name": "PRINCE TOONS",
        "description": "Free Hindi Dubbed Anime Download Website"
      }
    }
    </script>
    
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { background-color: black; color: white; font-family: Arial, sans-serif; }
        
        a, a:focus, a:active, a:visited {
            -webkit-tap-highlight-color: transparent;
            color: white;
            text-decoration: none;
        }
        
        .toonimage { width: 75px; height: auto; }
        
        .header-table {
            margin: 0 auto;
            text-align: center;
            border-collapse: collapse;
            width: 100%;
            max-width: 600px;
        }
        
        .header-table td { padding: 10px 15px; vertical-align: middle; }
        
        .header-title { color: white; font-size: 30px; }
        .header-title:hover { color: #ffcc00; transition: 0.3s; }
        
        .welcome-box {
            border-top: 2px solid;
            border-bottom: 2px solid;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100px;
            border-color: white;
            margin: 10px 0;
        }
        
        .welcome-inner {
            border: 2px solid;
            border-radius: 20px;
            width: 330px;
            height: 40px;
            display: flex;
            justify-content: center;
            align-items: center;
            border-color: white;
        }
        
        .welcome-text {
            margin: 0;
            font-size: 30px;
            font-weight: bold;
            color: white;
        }

        .logo-image {
            height: 80px;
            width: 90px;
        }
        
        .breadcrumb {
            text-align: center;
            color: #888;
            font-size: 14px;
            padding: 10px;
        }
        
        .breadcrumb a {
            color: #aaa;
            text-decoration: none;
        }
        
        .breadcrumb a:hover {
            color: gold;
        }

        .about-content {
            max-width: 900px;
            margin: 0 auto;
            padding: 20px 30px;
            text-align: left;
            line-height: 1.8;
        }
        
        .about-content h1 {
            text-align: center;
            margin-bottom: 30px;
            font-size: 32px;
            color: #ffcc00;
            border-bottom: 2px solid #ffcc00;
            padding-bottom: 15px;
        }
        
        .about-content h2 {
            margin-top: 30px;
            margin-bottom: 12px;
            color: #ffcc00;
            font-size: 20px;
            border-left: 4px solid #ffcc00;
            padding-left: 12px;
        }
        
        .about-content h3 {
            margin-top: 20px;
            margin-bottom: 10px;
            color: #ffcc00;
            font-size: 18px;
        }
        
        .about-content p, .about-content li {
            margin-bottom: 12px;
            font-size: 16px;
        }
        
        .about-content ul {
            padding-left: 25px;
            list-style-type: disc;
        }
        
        .about-content ul li { margin-bottom: 8px; }
        .about-content a { color: #66ccff; text-decoration: underline; }
        .about-content a:hover { color: #ffcc00; }
        .about-content strong { color: #ffcc00; }
        
        .about-content .highlight-box {
            background: rgba(255, 204, 0, 0.1);
            border: 1px solid #ffcc00;
            border-radius: 10px;
            padding: 20px;
            margin: 20px 0;
        }
        
        .about-content .info-box {
            background: rgba(102, 204, 255, 0.1);
            border: 1px solid #66ccff;
            border-radius: 10px;
            padding: 20px;
            margin: 20px 0;
        }
        
        .faq-section {
            margin: 30px 0;
        }
        
        .faq-item {
            background: #1a1a1a;
            border-radius: 10px;
            padding: 15px 20px;
            margin: 10px 0;
            border-left: 3px solid #ffcc00;
        }
        
        .faq-item h4 {
            color: gold;
            margin-bottom: 5px;
        }
        
        .faq-item p {
            color: #ccc;
            font-size: 15px;
            margin-bottom: 0;
        }

        @media (max-width: 768px) {
            .about-content { padding: 15px; }
            .about-content h1 { font-size: 24px; }
            .about-content h2 { font-size: 18px; }
            .header-title { font-size: 25px; }
            .welcome-inner { width: 280px; }
            .welcome-text { font-size: 24px; }
        }
        
        @media (max-width: 480px) {
            .header-title { font-size: 20px; }
            .header-table td { padding: 3px 6px; }
            .about-content h1 { font-size: 20px; }
            .about-content h2 { font-size: 16px; }
            .about-content p, .about-content li { font-size: 14px; }
            .welcome-inner { width: 220px; height: 32px; }
            .welcome-text { font-size: 18px; }
        }
    </style>
</head>
<body>
    <header>
        <table class="header-table">
            <tr>
                <td>
                    <a href='/'>
                        <h1 class="header-title">🏠 HOME</h1>
                    </a>
                </td>
                <td>
                    <img class='toonimage logo-image' src="https://raw.githubusercontent.com/princehamzaytprogramming/princetoons/main/static/princetoons.png" alt='PRINCE TOONS Logo - Free Hindi Dubbed Anime Download Website' width="75" height="auto" loading="lazy">
                </td>
                <td>
                    <a href='/about'>
                        <h1 class="header-title">📖 ABOUT</h1>
                    </a>
                </td>
            </tr>
        </table>
        
        <div class="welcome-box">
            <div class="welcome-inner">
                <p class="welcome-text">📖 ABOUT US</p>
            </div>
        </div>
        <br>
    </header>

    <main>
        <div class="breadcrumb">
            <a href="/">Home</a> › About
        </div>
        
        <div class="about-content">
            <h1>🌟 ABOUT PRINCE TOONS</h1>
            
            <div class="highlight-box">
                <p style="text-align: center; font-size: 18px; color: #ffcc00;">
                    <strong>🎬 Your #1 Source for Hindi Dubbed Anime &amp; Movies</strong>
                </p>
                <p style="text-align: center;">
                    Welcome to <strong>PRINCE TOONS</strong> – a private platform dedicated to bringing you the best Hindi dubbed anime and movies. 
                    This site is managed and operated by a single passionate admin who loves anime and wants to share it with the world.
                </p>
            </div>

            <h2>👑 About PRINCE TOONS</h2>
            <p>
                <strong>PRINCE TOONS</strong> is a <strong>private anime streaming website</strong> created by an anime enthusiast. 
                The site features a carefully curated collection of Hindi dubbed anime series, movies, and more. 
                All content is handpicked and uploaded by the site administrator to ensure quality and entertainment.
            </p>

            <h2>📤 Content Upload Information</h2>
            <div class="info-box">
                <p><strong>📌 How Content is Added to This Site:</strong></p>
                <ul>
                    <li><strong>Open-Source Anime:</strong> The admin uploads <strong>open-source / public domain</strong> anime content that is freely available.</li>
                    <li><strong>Multi-Page Uploads:</strong> Content is organized and uploaded across <strong>different pages</strong> for easy browsing.</li>
                    <li><strong>Embedded Content:</strong> All videos are <strong>embedded from third-party platforms</strong> like MEGA, Pixeldrain, and Cloud Hub.</li>
                    <li><strong>Admin Curated:</strong> Every anime is carefully selected by the admin and uploaded to the appropriate category.</li>
                    <li><strong>No Direct Hosting:</strong> We do not host any files on our servers – we only provide <strong>links to publicly available content</strong>.</li>
                </ul>
            </div>

            <h2>📺 What We Offer</h2>
            <ul>
                <li>🎌 <strong>Hindi Dubbed Anime</strong> – Popular and trending series</li>
                <li>🎬 <strong>Anime Movies</strong> – Full-length feature films</li>
                <li>🔥 <strong>HD Quality</strong> – High-definition streaming experience</li>
                <li>🌍 <strong>Multiple Genres</strong> – Action, adventure, comedy, fantasy, sports, and more</li>
                <li>🔄 <strong>Regular Updates</strong> – New episodes and series added often</li>
                <li>📂 <strong>Organized Categories</strong> – Easy to find your favorite anime</li>
            </ul>

            <h2>⚠️ DISCLAIMER &amp; TERMS OF USE</h2>
            
            <h3>1. GENERAL</h3>
            <p>This website ("Site") is operated by <strong>PRINCE TOONS</strong> ("we", "us", "our"). By accessing or using this Site, you agree to be bound by these terms.</p>
            
            <h3>2. ADMIN-ONLY ACCESS</h3>
            <p>This Site is a <strong>private streaming platform</strong>. Only the site administrator (PRINCE TOONS) has access to upload, add, or modify any content. Regular users <strong>cannot upload, post, or share</strong> any content on this Site.</p>
            
            <h3>3. COPYRIGHT &amp; DMCA POLICY</h3>
            <p>We respect intellectual property rights. If you are a copyright owner and believe that any content on this Site infringes your copyright, please contact us at:</p>
            <p><strong>📧 princehamzayt@gmail.com</strong></p>
            <p>with the following information:
                <ul>
                    <li>Identification of the copyrighted work claimed to be infringed.</li>
                    <li>Identification of the infringing material and its URL on our Site.</li>
                    <li>Your contact information (name, address, phone, email).</li>
                    <li>A statement that you have a good faith belief that use is unauthorized.</li>
                    <li>A statement, under penalty of perjury, that the information is accurate.</li>
                </ul>
                We will respond to valid takedown requests within <strong>24-72 hours</strong>.
            </p>
            
            <h3>4. NO WARRANTY</h3>
            <p>THIS SITE IS PROVIDED "AS IS" AND "AS AVAILABLE" WITHOUT ANY WARRANTIES OF ANY KIND, EXPRESS OR IMPLIED.</p>
            
            <h3>5. LIMITATION OF LIABILITY</h3>
            <p>TO THE MAXIMUM EXTENT PERMITTED BY LAW, WE SHALL NOT BE LIABLE FOR ANY DAMAGES ARISING FROM YOUR USE OF THIS SITE.</p>
            
            <h3>6. EXTERNAL LINKS</h3>
            <p>Our Site may contain links to external websites. We are not responsible for the content, privacy policies, or availability of any third-party sites.</p>
            
            <h3>7. USER RESPONSIBILITY</h3>
            <p>Users are solely responsible for ensuring their use of this Site complies with all applicable <strong>local, national, and international laws</strong>.</p>

            <h2>📞 CONTACT INFORMATION</h2>
            <div class="highlight-box">
                <p>For any questions, concerns, feedback, or takedown requests, please contact us at:</p>
                <p><strong>📧 Email:</strong> <a href="mailto:princehamzayt@gmail.com" style="color: #ffcc00;">princehamzayt@gmail.com</a></p>
                <p><strong>🕐 Response Time:</strong> We aim to respond to all inquiries within 24-48 hours.</p>
            </div>
            
            <div class="faq-section">
                <h2>❓ Frequently Asked Questions</h2>
                
                <div class="faq-item">
                    <h4>Is PRINCE TOONS free?</h4>
                    <p>Yes, PRINCE TOONS is completely free to use. All content is available without any subscription or payment.</p>
                </div>
                
                <div class="faq-item">
                    <h4>Do I need to create an account?</h4>
                    <p>No account is required to watch or download any anime from PRINCE TOONS.</p>
                </div>
                
                <div class="faq-item">
                    <h4>How often is new content added?</h4>
                    <p>New anime and movies are added regularly. The site is updated whenever new Hindi dubbed content becomes available.</p>
                </div>
                
                <div class="faq-item">
                    <h4>What quality are the videos?</h4>
                    <p>Most videos are available in HD quality (720p or 1080p), depending on the source.</p>
                </div>
            </div>

            <br>
            <hr style="border-color: #ffcc00; margin: 30px 0;">
            <p style="text-align: center; color: #888; font-size: 14px;">
                <strong>Last Updated:</strong> {{ current_date }}<br>
                &copy; 2026 <strong style="color: #ffcc00;">PRINCE TOONS</strong>. All rights reserved.
            </p>
        </div>
    </main>
</body>
</html>
'''

# ============================================
# SITEMAP XML TEMPLATE - Updated with dynamic dates
# ============================================

sitemap_xml_template = '''<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet type="text/css" href="https://www.xml-sitemaps.com/css/sitemap.css"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml" xmlns:video="http://www.google.com/schemas/sitemap-video/1.1">
  <url>
       <loc>https://princetoons.pythonanywhere.com/</loc>
       <lastmod>{{ current_date }}</lastmod>
       <changefreq>daily</changefreq>
       <priority>1.0000</priority>
  </url>
  <url>
       <loc>https://princetoons.pythonanywhere.com/page1</loc>
       <lastmod>{{ current_date }}</lastmod>
       <changefreq>daily</changefreq>
       <priority>0.8000</priority>
  </url>
  <url>
       <loc>https://princetoons.pythonanywhere.com/about</loc>
       <lastmod>{{ current_date }}</lastmod>
       <changefreq>monthly</changefreq>
       <priority>0.6000</priority>
  </url>
  {% for anime in anime_list %}
  <url>
       <loc>https://princetoons.pythonanywhere.com/detail/{{ anime.slug }}</loc>
       <lastmod>{{ current_date }}</lastmod>
       <changefreq>weekly</changefreq>
       <priority>0.6400</priority>
       <video:video>
            <video:thumbnail_loc>{{ anime.image_url }}</video:thumbnail_loc>
            <video:title>{{ anime.title }} {{ anime.season }} Hindi Dubbed</video:title>
            <video:description>{{ anime.description[:200] }}</video:description>
            <video:publication_date>{{ anime.year }}</video:publication_date>
            <video:family_friendly>yes</video:family_friendly>
            <video:duration>{{ anime.episodes * 24 }}</video:duration>
       </video:video>
  </url>
  {% endfor %}
  <url>
       <loc>https://princetoons.pythonanywhere.com/sitemap.xml</loc>
       <lastmod>{{ current_date }}</lastmod>
       <changefreq>monthly</changefreq>
       <priority>0.5000</priority>
  </url>
  <url>
       <loc>https://princetoons.pythonanywhere.com/robots.txt</loc>
       <lastmod>{{ current_date }}</lastmod>
       <changefreq>monthly</changefreq>
       <priority>0.3000</priority>
  </url>
  <url>
       <loc>https://princetoons.pythonanywhere.com/search</loc>
       <lastmod>{{ current_date }}</lastmod>
       <changefreq>daily</changefreq>
       <priority>0.7000</priority>
  </url>
</urlset>'''

# ============================================
# ROUTES - URL Endpoints
# ============================================

@app.route('/static/<path:filename>')
def serve_static(filename):
    try:
        return send_from_directory('static', filename)
    except Exception as e:
        return f"File not found: {filename}", 404

# ============================================
# GOOGLE VERIFICATION ROUTE
# ============================================

@app.route('/google01e00ac114a683b1.html')
def google_verify():
    try:
        return send_from_directory('static', 'google4050f0df3b808492.html')
    except Exception as e:
        return f"Verification file not found", 404

# ============================================
# SITEMAP ROUTE - With dynamic date
# ============================================

@app.route('/sitemap.xml')
def sitemap():
    current_date = datetime.now().strftime('%Y-%m-%dT%H:%M:%S+00:00')
    sitemap_xml = render_template_string(sitemap_xml_template, anime_list=anime_list, current_date=current_date)
    return Response(sitemap_xml, mimetype='application/xml')

# ============================================
# ROBOTS.TXT ROUTE
# ============================================

@app.route('/robots.txt')
def robots():
    robots_txt = '''User-agent: *
Allow: /
Allow: /page1
Allow: /detail/
Allow: /search
Allow: /about
Disallow: /static/
Disallow: /admin/
Sitemap: https://princetoons.pythonanywhere.com/sitemap.xml
'''
    return Response(robots_txt, mimetype='text/plain')

# ============================================
# SEARCH ROUTE - With unique title
# ============================================

@app.route('/search', methods=['GET'])
def search_route():
    query = request.args.get('q', '').strip()
    results = []
    
    if query:
        query_lower = query.lower()
        for anime in anime_list:
            if query_lower in anime['title'].lower():
                results.append(anime)
                continue
            if 'anime-type-tags' in anime and anime['anime-type-tags']:
                if query_lower in anime['anime-type-tags'].lower():
                    results.append(anime)
                    continue
            if 'search-alternatives' in anime and anime['search-alternatives']:
                if query_lower in anime['search-alternatives'].lower():
                    results.append(anime)
                    continue
        
        results.sort(key=lambda x: x['id'], reverse=True)
    
    page_title = get_page_title('search', query=query)
    meta_description = get_meta_description('search', query=query)
    return render_template_string(search_template, query=query, results=results, page_title=page_title, meta_description=meta_description,name_keywords=name_keywords)

# ============================================
# MAIN ROUTES
# ============================================

@app.route('/', methods=['GET', 'POST'])
def home_route():
    page_title = get_page_title('home')
    meta_description = get_meta_description('home')
    current_date = datetime.now().strftime('%Y-%m-%dT%H:%M:%S+00:00')
    return render_template_string(home, page_title=page_title, meta_description=meta_description, current_date=current_date,name_keywords=name_keywords)

@app.route('/page1', methods=['GET', 'POST'])
def page1_route():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    total_anime = len(anime_list_reversed)
    total_pages = (total_anime + per_page - 1) // per_page
    
    if page < 1:
        page = 1
    elif page > total_pages:
        page = total_pages
    
    start = (page - 1) * per_page
    end = start + per_page
    page_anime = anime_list_reversed[start:end]
    
    page_title = get_page_title('page1', page_num=page)
    meta_description = get_meta_description('page1')
    return render_template_string(
        page_template, 
        anime_list_reversed=anime_list_reversed,
        page_anime=page_anime,
        current_page=page,
        total_pages=total_pages,
        page_title=page_title,
        meta_description=meta_description,
        name_keywords=name_keywords
    )

@app.route('/detail/<slug>', methods=['GET', 'POST'])
def detail_route(slug):
    # First try to find by slug (image name)
    anime = next((a for a in anime_list if a.get('slug') == slug), None)
    
    # If not found by slug, try to find by ID (for backward compatibility)
    if anime is None and slug.isdigit():
        anime = next((a for a in anime_list if a['id'] == int(slug)), None)
        # If found by ID, redirect to the slug URL for SEO
        if anime:
            return redirect(f"/detail/{anime['slug']}", 301)
    
    if anime is None:
        return "Anime not found", 404
    
    page_title = get_page_title('detail', anime=anime)
    meta_description = get_meta_description('detail', anime=anime)
    current_date = datetime.now().strftime('%Y-%m-%dT%H:%M:%S+00:00')
    
    # Shuffle anime list for related section
    import random
    random.shuffle(anime_list)
    
    return render_template_string(
        detail_template, 
        anime=anime, 
        page_title=page_title, 
        meta_description=meta_description,
        current_date=current_date,
        anime_list=anime_list,
        name_keywords=name_keywords
    )

@app.route('/about')
def about():
    page_title = get_page_title('about')
    meta_description = get_meta_description('about')
    current_date = datetime.now().strftime('%Y-%m-%dT%H:%M:%S+00:00')
    return render_template_string(about_page, page_title=page_title, meta_description=meta_description, current_date=current_date,name_keywords=name_keywords)

# ============================================
# ADD JINJA2 FILTERS
# ============================================

@app.template_filter('shuffle')
def shuffle_filter(sequence):
    import random
    shuffled = list(sequence)
    random.shuffle(shuffled)
    return shuffled

@app.template_filter('truncate')
def truncate_filter(text, length=30):
    if len(text) > length:
        return text[:length] + '...'
    return text

# ============================================
# 404 ERROR HANDLER
# ============================================

@app.errorhandler(404)
def page_not_found(e):
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Page Not Found - PRINCE TOONS</title>
        <meta name="robots" content="noindex, follow" />
        <style>
            body { background-color: black; color: white; font-family: Arial, sans-serif; text-align: center; padding: 50px; }
            h1 { font-size: 72px; color: gold; }
            p { font-size: 24px; }
            a { color: gold; text-decoration: none; border: 2px solid gold; padding: 10px 30px; border-radius: 30px; display: inline-block; margin-top: 20px; }
            a:hover { background-color: gold; color: black; }
        </style>
    </head>
    <body>
        <h1>404</h1>
        <p>Oops! The page you're looking for doesn't exist.</p>
        <a href="/">← Go Back Home</a>
    </body>
    </html>
    ''', 404

# ============================================
# MAIN - Run the Application
# ============================================

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)