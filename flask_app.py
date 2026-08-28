"""
PRINCE TOONS - Anime Streaming Website
A simple Flask web application that displays anime information and provides download links.
"""

# Import necessary modules
from flask import Flask, request, render_template_string, json, send_from_directory

# Create Flask application instance
app = Flask(__name__)

# ============================================
# DATA SECTION - Anime Information
# ============================================

# JSON data containing all anime information
# This is stored as a string and will be converted to Python dictionary
jsons = '''
[
    {
        "id": 1,
        "title": "As a Reincarnated Aristocrat, I'll Use My Appraisal Skill",
        "season": "SEASON 2",
        "year": "YEAR",
        "description": "DESCRIPTION",
        "image_url": "/static/as-a-reincarnated-aristocrat-ill-use-my-appraisal-skill.png",
        "download_links": [
            {"name": "MEGA", "url": "https://mega.nz/file/uU5VnLyK#JbDXnXHdeNYjQBpSVTObno-OACeGqCrD7W88l6nj_YM"}
            
        ],
        "episodes": 0
    },
    {
        "id": 2,
        "title": "The Unaware Atelier Meister",
        "season": "SEASON 1",
        "year": "YEAR",
        "description": "DESCRIPTION",
        "image_url": "/static/the-unaware-atelier-meister.png",
        "download_links": [
            {"name": "MEGA", "url": "https://mega.nz/file/EMJkACjY#zDw-rwAApCv3wM-OexhqYoyHynYm-T8esQI6HqaSfIk"}
            
        ],
        "episodes": 0
    },
    {
        "id": 3,
        "title": "How To Train Your Dragon",
        "season": "SEASON 1",
        "year": "YEAR",
        "description": "DESCRIPTION",
        "image_url": "/static/how-to-train-your-dragon.png",
        "download_links": [
            {"name": "MEGA", "url": "https://mega.nz/#!px532BZB!JCIJ6JDZKJ52Zc-Zz9YXTohpy84_-i-mM--bmVLsA_8"}
            
        ],
        "episodes": 0
    },
    {
        "id": 4,
        "title": "Boonie Bears The Hidden Protector",
        "season": "MOVIE",
        "year": "YEAR",
        "description": "DESCRIPTION",
        "image_url": "/static/boonie-bears-the-hidden-protector.png",
        "download_links": [
            {"name": "MEGA", "url": "https://mega.nz/file/OPBy0IYK#LDuffJ503peOvsRDYtY-RJ4ROkWywJZm2mtzko_qfi8"}
        ],
        "episodes": 0
    },
    {
        "id": 5,
        "title": "Raya and the Last Dragon",
        "season": "MOVIE",
        "year": "YEAR",
        "description": "DESCRIPTION",
        "image_url": "/static/raya-and-the-last-Dragon.png",
        "download_links": [
            {"name": "MEGA", "url": "https://mega.nz/file/hV9Fnb5b#GzdEooG0zYAmYMVR1PP50kauTP8GcdELFoBPZHL8tU0"}
            
        ],
        "episodes": 0
    },
    {
        "id": 6,
        "title": "Minions & Monsters",
        "season": "MOVIE",
        "year": "YEAR",
        "description": "DESCRIPTION",
        "image_url": "/static/minions-monsters.png",
        "download_links": [
            {"name": "MEGA", "url": "https://mega.nz/file/lEgy2ZoD#JpcyaR8F6yOAY9YwkpNs67gmhbimUXIkJirjX-WcRFU"}
        ],
        "episodes": 0
    },
    {
        "id": 7,
        "title": "Dragon Ball Daima",
        "season": "SEASON 1",
        "year": "YEAR",
        "description": "DESCRIPTION",
        "image_url": "/static/dragon-ball-daima-s1.png",
        "download_links": [
            {"name": "MEGA", "url": "https://mega.nz/#!DoBlkTBK!5aYy1YVP57TN7xLoliEFFoopwCiGxl1Q40hgNbJKW3c"}
        ],
        "episodes": 0
    },
    {
        "id": 8,
        "title": "Wish Dragon",
        "season": "MOVIE",
        "year": "YEAR",
        "description": "DESCRIPTION",
        "image_url": "/static/wish-dragon.png",
        "download_links": [
            {"name": "MEGA", "url": "https://mega.nz/file/F3oCDABa#67jogzWr8DvYsRZoRCXvwve2l92xuv2K1XMXMw-rlM4"}
        ],
        "episodes": 0
    },
    {
        "id": 9,
        "title": "Good Bye Dragon Life",
        "season": "SEASON 1",
        "year": "YEAR",
        "description": "DESCRIPTION",
        "image_url": "/static/good-bye-dragon-life.png",
        "download_links": [
            {"name": "MEGA", "url": "https://mega.nz/#!h1wDWYxA!Yj_afbtSgupRLew0DItEHejWP37apCaF4tZFm2YwqXw"}
        ],
        "episodes": 0
    },
    {
        "id": 10,
        "title": "GOAT",
        "season": "MOVIE",
        "year": "YEAR",
        "description": "DESCRIPTION",
        "image_url": "/static/goat.png",
        "download_links": [
            {"name": "MEGA", "url": "https://mega.nz/file/G0QwQazC#CDYSkkK5AI-dxOiG--HH3vV6VggGRwFqFo2X9WXv0VM"}
        ],
        "episodes": 0
    },
    {
        "id": 11,
        "title": "Turning Red",
        "season": "MOVIE",
        "year": "YEAR",
        "description": "DESCRIPTION",
        "image_url": "/static/turning-red.png",
        "download_links": [
            {"name": "MEGA", "url": "https://mega.nz/file/kmRnwI6I#KbKqtMd7unCX26ajyTuk6NIbenPgGYUrftJSj5BUeLY"}
        ],
        "episodes": 0
    },
    {
        "id": 12,
        "title": "NE ZHA 2",
        "season": "MOVIE",
        "year": "YEAR",
        "description": "DESCRIPTION",
        "image_url": "/static/ne-zha-2.png",
        "download_links": [
            {"name": "MEGA", "url": "https://mega.nz/file/LGphDKrT#97gjsLYzLsUlnem33FI3pPuw2PyLH1PD-kkgoZgTpI0"}
        ],
        "episodes": 0
    },
    {
        "id": 13,
        "title": "I Parry Everything",
        "season": "SEASON 1",
        "year": "YEAR",
        "description": "DESCRIPTION",
        "image_url": "/static/i-parry-everything.png",
        "download_links": [
            {"name": "MEGA", "url": "https://mega.nz/file/rFkjnLjS#7VRAlIR9jfwUPbBQUv7uykyfVp1tuGBfafmlbud8tnA"}
        ],
        "episodes": 0
    },
    {
        "id": 14,
        "title": "Trillion Game",
        "season": "SEASON 1",
        "year": "YEAR",
        "description": "DESCRIPTION",
        "image_url": "/static/trillion-game.png",
        "download_links": [
            {"name": "MEGA", "url": "https://mega.nz/#!HIhHjZbR!Dc1ItOV7VZ3148mw43nmdOlV7uRv1QAV4zzZ3xgWfQk"}
        ],
        "episodes": 0
    },
    {
        "id": 15,
        "title": "Sword Art Online",
        "season": "SEASON 1",
        "year": "YEAR",
        "description": "DESCRIPTION",
        "image_url": "/static/sword-art-online.png",
        "download_links": [
            {"name": "MEGA", "url": "https://mega.nz/#!DUllGSia!IloFZHZkRF5qRgXEriHcVX85rqpcp5b0WeOiCEiexCU"}
        ],
        "episodes": 0
    },
    {
        "id": 16,
        "title": "MINIONS [2015]",
        "season": "MOVIE",
        "year": "YEAR",
        "description": "DESCRIPTION",
        "image_url": "/static/minions.png",
        "download_links": [
            {"name": "MEGA", "url": "https://mega.nz/file/tQpyjRRT#b92Ur3vyZXaONTk_4ifcWG2sA29Yc3AsnbvmwoqcCGw"}
        ],
        "episodes": 0
    },
    {
        "id": 17,
        "title": "That Time I Got Reincarnated As a Slime The Tears of The Azure Sea",
        "season": "MOVIE",
        "year": "YEAR",
        "description": "DESCRIPTION",
        "image_url": "/static/that-time-i-got-reincarnated-as-a-slime-the-tears-of-the-azure-sea.png",
        "download_links": [
            {"name": "MEGA", "url": "https://mega.nz/file/0NBSzIZJ#sTnTs8_HmEGH0ERJUigNG1h1E48g2vvQ4N60_REb1-w"}
        ],
        "episodes": 0
    },
    {
        "id": 18,
        "title": "Demon Slayer Kimetsu no Yaiba Infinity Castle",
        "season": "MOVIE",
        "year": "YEAR",
        "description": "DESCRIPTION",
        "image_url": "/static/demon-slayer-kimetsu-no-yaiba-infinity-castle.png",
        "download_links": [
            {"name": "MEGA", "url": "https://mega.nz/file/jLInRBCY#XDYWCOCBi_Yqj31Eoa48Z8wOtGc8rq8351XBez5k6bE"}
        ],
        "episodes": 0
    },
    {
        "id": 19,
        "title": "Avatar Aang The Last Airbender",
        "season": "MOVIE",
        "year": "YEAR",
        "description": "DESCRIPTION",
        "image_url": "/static/avatar-aang-the-last-airbender.png",
        "download_links": [
            {"name": "MEGA", "url": "https://mega.nz/file/zXJziSJA#_ANd8oUDoszSfnU9UhYTKxEXYjSR3JWfpz-rj96ItdE"}
        ],
        "episodes": 0
    },
    {
        "id": 20,
        "title": "ENCANTO",
        "season": "MOVIE",
        "year": "YEAR",
        "description": "DESCRIPTION",
        "image_url": "/static/encanto.png",
        "download_links": [
            {"name": "MEGA", "url": "https://mega.nz/file/cu4SXSoB#eJI5yN5Urg5PJT6p72BLgzHYpy2diQ4hDeBUopaFS1E"}
        ],
        "episodes": 0
    },
    {
        "id": 21,
        "title": "LUCA",
        "season": "MOVIE",
        "year": "YEAR",
        "description": "DESCRIPTION",
        "image_url": "/static/luca.png",
        "download_links": [
            {"name": "MEGA", "url": "https://mega.nz/file/9rwVCSyZ#cMreg3rk_rFNeOSaNRF4kYMDNkuWI8rYD16cfa4XjWo"}
        ],
        "episodes": 0
    },
    {
        "id": 22,
        "title": "The Boss Baby Family Business",
        "season": "MOVIE",
        "year": "YEAR",
        "description": "DESCRIPTION",
        "image_url": "/static/the-boss-baby-family-business.png",
        "download_links": [
            {"name": "MEGA", "url": "https://mega.nz/file/MV0DjYLL#AgtV5KElpyhePPPU-IJ5pXsq02C1veTSpDp2lspOSQc"}
        ],
        "episodes": 0
    },
    {
        "id": 23,
        "title": "INCREDIBLES 2",
        "season": "MOVIE",
        "year": "YEAR",
        "description": "DESCRIPTION",
        "image_url": "/static/incredibles-2.png",
        "download_links": [
            {"name": "MEGA", "url": "https://mega.nz/file/9roiVAwD#jxbKzmSEiLW-uoxiuMUdIihKCLXTZsDO5NHCvqrvR_8"}
        ],
        "episodes": 0
    },
    {
        "id": 24,
        "title": "THE INCREDIBLES",
        "season": "MOVIE",
        "year": "YEAR",
        "description": "DESCRIPTION",
        "image_url": "/static/the-incredibles.png",
        "download_links": [
            {"name": "MEGA", "url": "https://mega.nz/file/t75WyJ7C#BT8gn-GnuqtEnaK1_--7665Q20b5yj0Zr-V88A0586Y"}
        ],
        "episodes": 0
    },
    {
        "id": 25,
        "title": "HOPPERS",
        "season": "MOVIE",
        "year": "YEAR",
        "description": "DESCRIPTION",
        "image_url": "/static/hoppers.png",
        "download_links": [
            {"name": "MEGA", "url": "https://mega.nz/file/DmZ3ASaB#ZZO_9d2BSyvk0nvs1bSVeLvmGma8HR4Hz9tyawzQntU"}
        ],
        "episodes": 0
    },
    {
        "id": 26,
        "title": "Spider Man Into the Spider Verse",
        "season": "MOVIE",
        "year": "YEAR",
        "description": "DESCRIPTION",
        "image_url": "/static/spider-man-into-the-spider-verse.png",
        "download_links": [
            {"name": "MEGA", "url": "https://mega.nz/file/4QliRCCK#sMx7AhVXMHmCPP6cWDg2_DgZLGFVQxD_gxM4JPr_E9s"}
        ],
        "episodes": 0
    },
    {
        "id": 27,
        "title": "Attack on Titan",
        "season": "SEASON 1",
        "year": "YEAR",
        "description": "DESCRIPTION",
        "image_url": "/static/aot-s1.png",
        "download_links": [
            {"name": "MEGA", "url": "https://mega.nz/#!B94kDRaQ!RsAOoDmCLB48aR1bTzd7hWwQM0kXgo8MjJsWqqnGgaI"}
        ],
        "episodes": 0
    },
    {
        "id": 28,
        "title": "Attack on Titan",
        "season": "SEASON 2",
        "year": "YEAR",
        "description": "DESCRIPTION",
        "image_url": "/static/aot-s2.png",
        "download_links": [
            {"name": "MEGA", "url": "https://mega.nz/file/XUBBARyA#Yv7yH_KwiQZIEpCHUoLcMzcp7D5_uq7anLa1gZuzTd8"}
        ],
        "episodes": 0
    },
    {
        "id": 29,
        "title": "Attack on Titan",
        "season": "SEASON 3",
        "year": "YEAR",
        "description": "DESCRIPTION",
        "image_url": "/static/aot-s3.png",
        "download_links": [
            {"name": "MEGA", "url": "https://mega.nz/#!EtxyiKaa!Ft4fXpotFNFF-gSFzErVO9tAzEUzacjwyuh3dL_DRsw"}
        ],
        "episodes": 0
    },
    {
        "id": 30,
        "title": "Attack on Titan",
        "season": "SEASON 4",
        "year": "YEAR",
        "description": "DESCRIPTION",
        "image_url": "/static/aot-s4.png",
        "download_links": [
            {"name": "MEGA", "url": "https://mega.nz/#!OxAzHLzS!w37T8e5YkUiTfxJpBnWSEhu132WVVmvVEAEYi4sjJ9Y"}
        ],
        "episodes": 0
    },
    {
        "id": 31,
        "title": "The Super Mario Galaxy",
        "season": "MOVIE",
        "year": "YEAR",
        "description": "DESCRIPTION",
        "image_url": "/static/the-super-mario-galaxy.png",
        "download_links": [
            {"name": "MEGA", "url": "https://mega.nz/file/fjAW0AQa#6NUEiPlOrSEwtO7ZkmArrABbt7TCPmlS8ObMZWC1IRU"}
        ],
        "episodes": 0
    },
    {
        "id": 32,
        "title": "SCARLET",
        "season": "MOVIE",
        "year": "YEAR",
        "description": "DESCRIPTION",
        "image_url": "/static/scarlet.png",
        "download_links": [
            {"name": "MEGA", "url": "https://mega.nz/file/78QnEaBK#eEIeVeHCMpXJHI-FGad97B0QvTOa6_r35B8wc-0R9kE"}
        ],
        "episodes": 0
    },
    {
        "id": 33,
        "title": "ZOOTOPIA",
        "season": "MOVIE",
        "year": "YEAR",
        "description": "DESCRIPTION",
        "image_url": "/static/zootopia-2.png",
        "download_links": [
            {"name": "MEGA", "url": "https://mega.nz/file/qlJCXBaR#cYzI-qNIUPKyEPk2YvMZttbLD-e3oz5laWTKgvYU4vk"}
        ],
        "episodes": 0
    },
    {
        "id": 34,
        "title": "Lupin The 3Rd Vs Cats Eye",
        "season": "MOVIE",
        "year": "YEAR",
        "description": "DESCRIPTION",
        "image_url": "/static/lupin-the-3rd-vs-cats-eye.png",
        "download_links": [
            {"name": "MEGA", "url": "https://mega.nz/file/e8QkAbxL#Sj9aNRJzpM5ah9u7cO0U-JJTyq8XUaKqyIcFYUgfI2M"}
        ],
        "episodes": 0
    },
    {
        "id": 35,
        "title": "To Be Hero X",
        "season": "SEASON 1",
        "year": "YEAR",
        "description": "DESCRIPTION",
        "image_url": "/static/to-be-hero-x.png",
        "download_links": [
            {"name": "PIXELDRAIN", "url": "https://pixeldrain.net/u/JHeYtejf?download"}
        ],
        "episodes": 0
    },
    {
        "id": 36,
        "title": "Spy X Family",
        "season": "SEASON 3",
        "year": "YEAR",
        "description": "DESCRIPTION",
        "image_url": "/static/spy-x-family-season-3.png",
        "download_links": [
            {"name": "PIXELDRAIN", "url": "https://pixeldrain.net/u/nZipGSvb?download"}
        ],
        "episodes": 0
    },
    {
        "id": 37,
        "title": "BLUE LOCK",
        "season": "SEASON 1",
        "year": "YEAR",
        "description": "DESCRIPTION",
        "image_url": "/static/blue-lock-season-1.png",
        "download_links": [
            {"name": "CLOUD HUB", "url": "https://hubcloud.cx/drive/vs91pzg73ziguin"}
        ],
        "episodes": 0
    },
    {
        "id": 38,
        "title": "Blue Lock Episode Nagi",
        "season": "MOVIE",
        "year": "YEAR",
        "description": "DESCRIPTION",
        "image_url": "/static/blue-lock-episode-nagi.png",
        "download_links": [
            {"name": "MEGA", "url": "https://mega.nz/#!HwIlTRaB!zRgBy_aT1uutqnmDFPAjfAkjiH4pc-tLUAKjUZ9C1nk"}
        ],
        "episodes": 0
    },
    {
        "id": 39,
        "title": "BLUE LOCK",
        "season": "SEASON 2",
        "year": "YEAR",
        "description": "DESCRIPTION",
        "image_url": "/static/blue-lock-season-2.png",
        "download_links": [
            {"name": "MEGA", "url": "https://mega.nz/#!2QZk0RbY!Ut02y0WckrhmUzCfaXPpzdRnvDAxbRS8lewb_qHM7qA"}
        ],
        "episodes": 0
    },
    {
        "id": 40,
        "title": "Lord Of Mysteries",
        "season": "SEASON 1",
        "year": "YEAR",
        "description": "DESCRIPTION",
        "image_url": "/static/lord-of-mysteries-season-1.png",
        "download_links": [
            {"name": "PIXELDRAIN", "url": "https://pixeldrain.net/u/VfmJsKh1?download"}
        ],
        "episodes": 0
    },
    {
        "id": 41,
        "title": "The Rising Of The Shield Hero",
        "season": "SEASON 1",
        "year": "YEAR",
        "description": "DESCRIPTION",
        "image_url": "/static/the-rising-of-the-shield-hero-season-1.png",
        "download_links": [
            {"name": "PIXELDRAIN", "url": "https://pixeldrain.net/u/q1LBqDfQ?download"},
            {"name": "CLOUD HUB", "url": "https://hubcloud.cx/drive/8k0nv89kppdk409"}
        ],
        "episodes": 0
    },
    {
        "id": 42,
        "title": "The Rising Of The Shield Hero",
        "season": "SEASON 2",
        "year": "YEAR",
        "description": "DESCRIPTION",
        "image_url": "/static/the-rising-of-the-shield-hero-season-2.png",
        "download_links": [
            {"name": "PIXELDRAIN", "url": "https://pixeldrain.net/u/ao52VMFU?download"},
            {"name": "CLOUD HUB", "url": "https://hubcloud.cx/drive/gvwygqyxzhvbese"}
        ],
        "episodes": 0
    },
    {
        "id": 43,
        "title": "The Rising Of The Shield Hero",
        "season": "SEASON 3",
        "year": "YEAR",
        "description": "DESCRIPTION",
        "image_url": "/static/the-rising-of-the-shield-hero-season-3.png",
        "download_links": [
            {"name": "PIXELDRAIN", "url": "https://pixeldrain.net/u/RPuJwvYa?download"}
        ],
        "episodes": 0
    },
    {
        "id": 44,
        "title": "The Rising Of The Shield Hero",
        "season": "SEASON 4",
        "year": "YEAR",
        "description": "DESCRIPTION",
        "image_url": "/static/the-rising-of-the-shield-hero-season-4.png",
        "download_links": [
            {"name": "PIXELDRAIN", "url": "https://pixeldrain.net/u/DtwFeGGV?download"}
        ],
        "episodes": 0
    },
    {
        "id": 45,
        "title": "Wistoria Wand And Sword",
        "season": "SEASON 1",
        "year": "YEAR",
        "description": "DESCRIPTION",
        "image_url": "/static/wistoria-wand-and-sword-season-1.png",
        "download_links": [
            {"name": "PIXELDRAIN", "url": "https://pixeldrain.net/u/y3q1JK2f?download"}
        ],
        "episodes": 0
    },
    {
        "id": 46,
        "title": "Wistoria Wand And Sword",
        "season": "SEASON 2",
        "year": "YEAR",
        "description": "DESCRIPTION",
        "image_url": "/static/wistoria-wand-and-sword-season-2.png",
        "download_links": [
            {"name": "PIXELDRAIN", "url": "https://pixeldrain.net/u/nGPiJN4w?download"}
        ],
        "episodes": 0
    },
    {
        "id": 47,
        "title": "Vinland Saga",
        "season": "SEASON 1",
        "year": "YEAR",
        "description": "DESCRIPTION",
        "image_url": "/static/vinland-saga-season-1.png",
        "download_links": [
            {"name": "PIXELDRAIN", "url": "https://pixeldrain.net/u/4UHEaXzR?download"},
            {"name": "MEGA", "url": "https://mega.nz/#!RSd2DRhI!4wx9wqTdg67I4KCY8g5yaXZlLAEoSk3HQAfDGgeG5jo"}
        ],
        "episodes": 0
    },
    {
        "id": 48,
        "title": "Vinland Saga",
        "season": "SEASON 2",
        "year": "YEAR",
        "description": "DESCRIPTION",
        "image_url": "/static/vinland-saga-season-2.png",
        "download_links": [
            {"name": "PIXELDRAIN", "url": "https://pixeldrain.net/u/iHYoUykv?download"},
            {"name": "MEGA", "url": "https://mega.nz/#!IW8jnKCT!Uo6JsqG-8jbGW14nKIZZ2fXyUSoj_8upArQzlQuqzhU"}
        ],
        "episodes": 0
    },
    {
        "id": 49,
        "title": "Mob Psycho 100",
        "season": "SEASON 1",
        "year": "YEAR",
        "description": "DESCRIPTION",
        "image_url": "/static/mob-psycho-100-season-1.png",
        "download_links": [
            {"name": "PIXELDRAIN", "url": "https://pixeldrain.net/u/isjpVipf?download"},
            {"name": "CLOUD HUB", "url": "https://hubcloud.cx/drive/xbwmtl5w0avm1j5"}
        ],
        "episodes": 0
    },
    {
        "id": 50,
        "title": "Mob Psycho 100",
        "season": "SEASON 2",
        "year": "YEAR",
        "description": "DESCRIPTION",
        "image_url": "/static/mob-psycho-100-season-2.png",
        "download_links": [
            {"name": "PIXELDRAIN", "url": "https://pixeldrain.net/u/jeCxP7vF?download"},
            {"name": "CLOUD HUB", "url": "https://hubcloud.cx/drive/wbdt7ixtj8oebcu"}
        ],
        "episodes": 0
    },
    {
        "id": 51,
        "title": "Akudama Drive",
        "season": "SEASON 1",
        "year": "YEAR",
        "description": "DESCRIPTION",
        "image_url": "/static/akudama-drive-season-1.png",
        "download_links": [
            {"name": "PIXELDRAIN", "url": "https://pixeldrain.net/u/rkYebPUL?download"},
            {"name": "CLOUD HUB", "url": "https://hubcloud.cx/drive/ctzi1s98f9l2fvi"}
        ],
        "episodes": 0
    },
    {
        "id": 52,
        "title": "Liar Game",
        "season": "SEASON 1 EP 1-12",
        "year": "YEAR",
        "description": "DESCRIPTION",
        "image_url": "/static/liar-game-season-1.png",
        "download_links": [
            {"name": "PIXELDRAIN", "url": "https://pixeldrain.net/u/UEDMXbK4?download"},
            {"name": "CLOUD HUB", "url": "https://hubcloud.cx/drive/zpuzuua6ctuzu0p"}
        ],
        "episodes": 0
    },
    {
        "id": 53,
        "title": "Mushoku Tensei: Jobless Reincarnation",
        "season": "SEASON 1",
        "year": "YEAR",
        "description": "DESCRIPTION",
        "image_url": "/static/mushoku-tensei-jobless-reincarnation-season-1.png",
        "download_links": [
            {"name": "PIXELDRAIN", "url": "https://pixeldrain.net/u/S2Qzhsds?download"},
            {"name": "MEGA", "url": "https://mega.nz/#!cOFThJob!7kdMxSvF8W78l-LoYmbJmiqRfSTWDeJEkM_D5Re7hW0"}
        ],
        "episodes": 0
    },
    
    {
        "id": 54,
        "title": "Mushoku Tensei: Jobless Reincarnation",
        "season": "SEASON 2",
        "year": "YEAR",
        "description": "DESCRIPTION",
        "image_url": "/static/mushoku-tensei-jobless-reincarnation-season-2.png",
        "download_links": [
            {"name": "PIXELDRAIN", "url": "https://pixeldrain.net/u/DVgQpMBU?download"},
            {"name": "GO FILE", "url": "https://gofile.io/d/43PAIj"}
        ],
        "episodes": 0
    },
    {
        "id": 55,
        "title": "Sword Art Online",
        "season": "SEASON 2",
        "year": "YEAR",
        "description": "DESCRIPTION",
        "image_url": "/static/sword-art-online-season-2.png",
        "download_links": [
            {"name": "MEGA", "url": "https://mega.nz/file/qdZ2wDSA#AxS__hQvk-fCocuS-OshFpBTOHdPIGXLKuAB7z6eiIQ"},
            {"name": "MEDIA FIRE", "url": "https://www.mediafire.com/file/htg36o3se7ykb4k/S2_-_SAO_in_Hindi_%255BRare_Animes%255D.zip/file"}
        ],
        "episodes": 0
    },
    {
        "id": 56,
        "title": "Jack of All Trades, Party of None",
        "season": "SEASON 1",
        "year": "YEAR",
        "description": "DESCRIPTION",
        "image_url": "/static/jack-of-all-trades-party-of-none-season-1.png",
        "download_links": [
            {"name": "PIXELDRAIN", "url": "https://pixeldrain.net/u/RXo5MRLW?download"},
            {"name": "CLOUD HUB", "url": "https://hubcloud.cx/drive/wg44coa1paimfwi"}
        ],
        "episodes": 0
    },
    {
        "id": 57,
        "title": "Re:ZERO -Starting Life in Another World",
        "season": "SEASON 1",
        "year": "YEAR",
        "description": "DESCRIPTION",
        "image_url": "/static/re-zero-season-1.png",
        "download_links": [
            {"name": "MEGA", "url": "https://mega.nz/file/6B5RhKYS#ukqJtj1T-ZDY6xS2ZRf0d8MEDKLrYimLbWMzmu6Q8Co"},
            {"name": "PIXELDRAIN", "url": "https://pixeldrain.net/u/92vLJpcb?download"},
            {"name": "MEDIA FIRE", "url": "https://www.mediafire.com/file/eg77kbqpvezxc5i/Re+ZERO+Starting+Life+in+Another+World+S01+[RareToonsIndia].zip/file"}
        ],
        "episodes": 0
    },
    {
        "id": 58,
        "title": "Re:ZERO -Starting Life in Another World",
        "season": "SEASON 2",
        "year": "YEAR",
        "description": "DESCRIPTION",
        "image_url": "/static/re-zero-season-2.png",
        "download_links": [
            {"name": "MEGA", "url": "https://mega.nz/#!2A8GmS6L!RXk7SoT5UhSADf6NJPjpyBdufnXSxMdRT6drAc_MUhE"},
            {"name": "PIXELDRAIN", "url": "https://pixeldrain.net/u/TGYf1sk9?download"},
            {"name": "MEDIA FIRE", "url": "https://www.mediafire.com/file/09m5y87dzsfi0eh/Re+ZERO+Starting+Life+in+Another+World+S02+[RareToonsIndia].zip/file"}
        ],
        "episodes": 0
    },
    {
        "id": 59,
        "title": "Re:ZERO -Starting Life in Another World",
        "season": "SEASON 3",
        "year": "YEAR",
        "description": "DESCRIPTION",
        "image_url": "/static/re-zero-season-3.png",
        "download_links": [
            {"name": "MEGA", "url": "https://mega.nz/#!PRYn1R5A!QU5Jhp5oivdUMd-m8BwF9ZCfajWH0DAky0nbfps7F0Y"},
            {"name": "PIXELDRAIN", "url": "https://pixeldrain.net/u/xE8u2x32?download"},
            {"name": "MEDIA FIRE", "url": "https://www.mediafire.com/file/em7cz7toq2ldlvs/Re+ZERO+Starting+Life+in+Another+World+S03+[RareToonsIndia].zip/file"}
        ],
        "episodes": 0
    },
    {
        "id": 60,
        "title": "Re:ZERO -Starting Life in Another World",
        "season": "SEASON 4 PART-1 EP-1-11",
        "year": "YEAR",
        "description": "DESCRIPTION",
        "image_url": "/static/re-zero-season-4.png",
        "download_links": [
            {"name": "CLOUD HUB", "url": "https://hubcloud.cx/drive/owqmgq42q24m4y3"},
            {"name": "PIXELDRAIN", "url": "https://pixeldrain.net/u/BGWUjJaE?download"}
        ],
        "episodes": 0
    }
]
'''

# Convert JSON string to Python list of dictionaries
anime_list = json.loads(jsons)

# ============================================
# REVERSE THE ANIME LIST - Show highest ID first
# ============================================

# Method 1: Reverse the list using [::-1] (Slicing)
# This creates a new reversed list
anime_list_reversed = anime_list[::-1]

# ============================================
# HTML TEMPLATES - Website Pages
# ============================================

# HOME PAGE HTML - Landing page with logo and social media links
home = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name='viewport' content='width=device-width, initial-scale=1.0'>
    <title>PRINCE TOONS</title>
    <style>
        /* Reset default margins and padding */
        * { margin: 0; padding: 0; }
        
        /* Main body styling */
        body { 
            background-color: black;  /* Black background */
            color: white;            /* White text */
            font-family: Arial, sans-serif;
        }
        
        /* Remove underline and blue color from links */
        a, a:focus, a:active, a:visited {
            -webkit-tap-highlight-color: transparent;
            color: white;
            text-decoration: none;
        }
        
        /* Logo image styling */
        .toonimage {
            width: 75px;
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
        
        /* Ball image - clickable to navigate */
        .ball-image {
            width: 150px;
            cursor: pointer;
            margin: 10px 0;
        }
        
        /* Social media section */
        .social-row {
            display: flex;
            flex-direction: row;
            justify-content: center;
            align-items: center;
            gap: 10px;
            flex-wrap: wrap;
            margin: 20px 0;
        }
        
        .social-row img {
            width: 80px;
            height: auto;
        }
        
        /* Individual social media icon sizes */
        .youtube { width: 130px; }
        .tiktok { width: 100px; height: 90px; }
        .instagram { width: 70px; height: 65px; border-radius: 15px; }
        .whatsapp { width: 90px; height: 82px; }
        
        .logo-image {
            height: 80px;
            width: 90px;
        }
        
        /* Mobile responsive design */
        @media (max-width: 768px) {
            .header-title { font-size: 25px; }
            .header-table td { padding: 5px 10px; }
            .main-container { margin: 10px; padding: 15px; }
            .main-title { font-size: 28px; }
            .gold-text { font-size: 28px; }
            .social-row img { width: 60px; }
            .youtube { width: 100px; }
            .tiktok { width: 80px; height: 70px; }
            .instagram { width: 60px; height: 55px; }
            .whatsapp { width: 70px; height: 62px; }
        }
    </style>
</head>
<body>
    <!-- Header with navigation links -->
    <table class="header-table">
        <tr>
            <td>
                <a href='/page1'>
                    <h1 class="header-title">HOME</h1>
                </a>
            </td>
            <td>
                <img class='toonimage logo-image' src="/static/princetoons.png" alt='image'>
            </td>
            <td>
                <a href='/'>
                    <h1 class="header-title">ABOUT</h1>
                </a>
            </td>
        </tr>
    </table>
    
    <!-- Welcome section -->
    <div class="welcome-box">
        <div class="welcome-inner">
            <p class="welcome-text">• PRINCE TOONS •</p>
        </div>
    </div>
    <br>
    
    <!-- Main content - Click on ball to enter -->
    <div class="main-container">
        <p class="main-title">• MOVIES & ANIME •</p>
        <p class="sub-title">WELCOME TO PRINCE TOONS</p>
        <p class="gold-text">• CLICK ON BALL •</p>
        <a href='/page1'>
            <img class="ball-image" src="/static/ball.png" alt='BALL'>
        </a>
        <p class="owner-text">OWNER</p>
        <p class="social-text">SOCIAL MEDIA</p>
        
        <!-- Social media links -->
        <div class="social-row">
            <a href='https://youtube.com/@princehamzayt6210'>
                <img class="youtube" src="/static/youtube.png" alt='YOUTUBE'>
            </a>
            <a href='https://www.tiktok.com/@princehamza.yt'>
                <img class="tiktok" src="/static/tiktok.png" alt='tiktok'>
            </a>
            <a href='https://www.instagram.com/princehmzayt'>
                <img class="instagram" src="/static/instagram.png" alt='instagram'>
            </a>
            <a href='https://chat.whatsapp.com/HwvR3IcDg3gIgMUsnB90ss?s=cl&p=a&ilr=4'>
                <img class="whatsapp" src="/static/whatsapp.png" alt='whatsapp'>
            </a>
        </div>
    </div>
</body>
</html>
'''

# PAGE 1 - Anime listing page with pagination (10 per page)
page_template = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name='viewport' content='width=device-width, initial-scale=1.0'>
    <title>PRINCE TOONS PAGE</title>
    <style>
        * { margin: 0; padding: 0; }
        body { background-color: black; color: white; font-family: Arial, sans-serif; }
        
        /* Remove default link styling */
        a {
            text-decoration: none !important;
            color: inherit;
            -webkit-tap-highlight-color: transparent;
        }
        
        /* Header styling */
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
        
        .toonimage {
            width: 75px;
        }
        
        .logo-image {
            height: 80px;
            width: 90px;
        }
        
        /* Welcome box */
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
        }
        
        /* Anime card container */
        .anime-container {
            min-height: 220px;
            margin: 20px;
            padding: 10px;
            text-align: center;
        }
        
        /* Anime image styling - uses background-image for better control */
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
        
        /* Watch button styling */
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
        
        /* Pagination styling */
        .pagination {
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 15px;
            margin: 30px 0;
            padding: 10px;
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
        
        /* Mobile responsive */
        @media (max-width: 768px) {
            .header-title { font-size: 25px; }
            .header-table td { padding: 5px 10px; }
            .anime-image { max-width: 100%; }
            .watch-button { max-width: 100%; }
            .pagination a { padding: 8px 15px; font-size: 16px; }
            .pagination .current { padding: 8px 15px; font-size: 16px; }
        }
    </style>
</head>
<body>
    <!-- Header -->
    <table class="header-table">
        <tr>
            <td>
                <a href='/page1'>
                    <h1 class="header-title">HOME</h1>
                </a>
            </td>
            <td>
                <a href='/'>
                    <img class='toonimage logo-image' src="/static/princetoons.png" alt='image'>
                </a>
            </td>
            <td>
                <a href='/'>
                    <h1 class="header-title">ABOUT</h1>
                </a>
            </td>
        </tr>
    </table>

    <!-- Welcome -->
    <div class="welcome-box">
        <div class="welcome-inner">
            <p class="welcome-text">• ANIME & MOVIES •</p>
        </div>
    </div>
    <br>
    
    <!-- Page info -->
    <div class="page-info">
        Page {{ current_page }} of {{ total_pages }} ({{ anime_list_reversed|length }} total anime)
    </div>
    
    <!-- 
        ============================================
        LOOP THROUGH ANIME IN REVERSE ORDER
        Showing only 10 per page
        ============================================
    -->
    {% for anime in page_anime %}
    <a href='/detail/{{ anime.id }}'>
        <div class="anime-container">
            <!-- Anime image from static folder -->
            <div class="anime-image" style="background-image: url('{{ anime.image_url }}');"></div>
            
            <!-- Anime title and season -->
            <p class="anime-title">{{ anime.title }} {{ anime.season }} Hindi</p>
            
            <!-- Watch/Download button -->
            <div class="watch-button">
                <p class="watch-text">WATCH/DOWNLOAD</p>
            </div>
        </div>
    </a>
    <br>
    {% endfor %}
    
    <!-- Pagination links -->
    <div class="pagination">
        {% if current_page > 1 %}
            <a href="/page1?page={{ current_page - 1 }}">◀ PREV</a>
        {% endif %}
        
        <span class="current">{{ current_page }}</span>
        
        {% if current_page < total_pages %}
            <a href="/page1?page={{ current_page + 1 }}">NEXT ▶</a>
        {% endif %}
    </div>
</body>
</html>
'''

# DETAIL PAGE - Shows detailed information about selected anime with multiple download buttons
detail_template = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name='viewport' content='width=device-width, initial-scale=1.0'>
    <title>PRINCE TOONS DETAILS</title>
    <style>
        * { margin: 0; padding: 0; }
        body { background-color: black; color: white; font-family: Arial, sans-serif; }
        
        a {
            text-decoration: none !important;
            color: inherit;
            -webkit-tap-highlight-color: transparent;
        }
        
        /* Header styling */
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
        
        .toonimage {
            width: 75px;
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
        
        /* Detail container */
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
        
        /* Download buttons container */
        .download-buttons {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 15px;
            margin: 20px 0;
        }
        
        /* Individual download button */
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
        }
        
        .download-button:hover {
            background-color: #333;
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
        }
        
        /* Different colors for different download sources */
        .download-mega {
            border-color: #ff0066;
        }
        .download-mega a {
            color: #ff0066;
        }
        .download-mega:hover {
            background-color: #ff006622;
        }
        
        .download-pixeldrain {
            border-color: #00ccff;
        }
        .download-pixeldrain a {
            color: #00ccff;
        }
        .download-pixeldrain:hover {
            background-color: #00ccff22;
        }
        
        .download-mediafire {
            border-color: #ff9900;
        }
        .download-mediafire a {
            color: #ff9900;
        }
        .download-mediafire:hover {
            background-color: #ff990022;
        }
        
        .download-googledrive {
            border-color: #00ff00;
        }
        .download-googledrive a {
            color: #00ff00;
        }
        .download-googledrive:hover {
            background-color: #00ff0022;
        }
        
        .download-hub {
            border-color: #ff00ff;
        }
        .download-hub a {
            color: #ff00ff;
        }
        .download-hub:hover {
            background-color: #ff00ff22;
        }
        
        .download-zippyfire {
            border-color: #ff6600;
        }
        .download-zippyfire a {
            color: #ff6600;
        }
        .download-zippyfire:hover {
            background-color: #ff660022;
        }
        
        .download-default {
            border-color: #ffffff;
        }
        .download-default a {
            color: #ffffff;
        }
        .download-default:hover {
            background-color: #ffffff22;
        }
        
        .no-links {
            color: #666;
            font-size: 18px;
            margin: 15px 0;
        }
        
        /* Social media section */
        .social-section {
            margin: 40px 0 20px 0;
        }
        
        .social-section h1 {
            font-size: 45px;
            color: white;
            margin: 10px 0;
        }
        
        .social-icons {
            border: 2px solid;
            border-radius: 20px;
            display: flex;
            gap: 10px;
            padding: 10px;
            align-items: center;
            border-color: white;
            justify-content: center;
            flex-wrap: wrap;
        }
        
        .social-icon {
            border-radius: 50px;
            height: 60px;
            width: 90px;
            background-position: center;
            background-size: cover;
            background-repeat: no-repeat;
        }
        
        @media (max-width: 768px) {
            .header-title { font-size: 25px; }
            .header-table td { padding: 5px 10px; }
            .anime-image-detail { max-width: 100%; }
            .social-icons { height: auto; padding: 20px; }
            .social-section h1 { font-size: 35px; }
            .download-button {
                width: 160px;
                height: 45px;
            }
            .download-button a {
                font-size: 16px;
            }
        }
    </style>
</head>
<body>
    <!-- Header -->
    <table class="header-table">
        <tr>
            <td>
                <a href='/page1'>
                    <h1 class="header-title">HOME</h1>
                </a>
            </td>
            <td>
                <a href='/'>
                    <img class='toonimage logo-image' src="/static/princetoons.png" alt='image'>
                </a>
            </td>
            <td>
                <a href='/'>
                    <h1 class="header-title">ABOUT</h1>
                </a>
            </td>
        </tr>
    </table>

    <!-- Welcome -->
    <div class="welcome-box">
        <div class="welcome-inner">
            <h1 class="welcome-text">• ANIME •</h1>
        </div>
    </div>
    <br>
    
    <div class="detail-container">
        <u class="detail-title">• ANIME DETAILS •</u>
        
        <!-- Display anime information from the database -->
        <div class="anime-name">
            <p>{{ anime.title }}</p>
        </div>
        
        <div class="anime-season">
            <p><u>{{ anime.season }}</u></p>
        </div>
        
        <div class="anime-dub">
            <p><u>HINDI DUBBED</u></p>
        </div>
        
        <!-- Anime image -->
        <div class="anime-image-detail" style="background-image: url('{{ anime.image_url }}');"></div>
        
        <!-- Download section -->
        <div class="download-links">
            <u>• DOWNLOAD LINKS •</u>
        </div>
        
        <!-- Multiple download buttons -->
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
                            <a href="{{ link.url }}" target="_blank">
                                {{ link.name|upper }}
                            </a>
                        </div>
                    {% endif %}
                {% endfor %}
            {% else %}
                <p class="no-links">No download links available</p>
            {% endif %}
        </div>
        
        <!-- Social media -->
        <div class="social-section">
            <h1>OWNER</h1>
            <h1>SOCIAL MEDIA</h1>
        </div>
        
        <div class="social-icons">
            <a href='https://youtube.com/@princehamzayt6210'>
                <div class="social-icon" style="background-image:url('/static/youtube.png');"></div>
            </a>
            <a href='https://www.tiktok.com/@princehamza.yt'>
                <div class="social-icon" style="background-image:url('/static/tiktok.png');"></div>
            </a>
            <a href='https://www.instagram.com/princehmzayt'>
                <div class="social-icon" style="background-image:url('/static/instagram.png');"></div>
            </a>
            <a href='https://chat.whatsapp.com/HwvR3IcDg3gIgMUsnB90ss?s=cl&p=a&ilr=4'>
                <div class="social-icon" style="background-image:url('/static/whatsapp.png');"></div>
            </a>
        </div>
    </div>
</body>
</html>
'''

# ============================================
# ROUTES - URL Endpoints
# ============================================

@app.route('/static/<path:filename>')
def serve_static(filename):
    """
    Route to serve static files (images, CSS, etc.)
    This is needed because Flask doesn't serve static files by default in production
    
    Parameters:
    filename: The name of the file to serve
    
    Returns:
    The requested file from the 'static' folder
    """
    try:
        return send_from_directory('static', filename)
    except Exception as e:
        return f"File not found: {filename}", 404

@app.route('/', methods=['GET', 'POST'])
def home_route():
    """
    Home page route - displays the landing page
    
    This is the main entry point of the website
    Handles both GET (view) and POST (submit) requests
    
    Returns:
    The home page HTML
    """
    if request.method == 'POST':
        return home
    return home

@app.route('/page1', methods=['GET', 'POST'])
def page1_route():
    """
    Page 1 route - displays all anime in REVERSE order with pagination
    10 anime per page
    
    This page shows all available anime with their images
    Starting from the highest ID (newest first)
    Each anime is clickable and leads to its detail page
    
    Returns:
    The page1 HTML with paginated reversed anime data injected
    """
    # Get the current page number from query parameters, default to 1
    page = request.args.get('page', 1, type=int)
    
    # Number of anime per page
    per_page = 10
    
    # Total number of anime
    total_anime = len(anime_list_reversed)
    
    # Calculate total pages
    total_pages = (total_anime + per_page - 1) // per_page  # Ceiling division
    
    # Ensure page is within bounds
    if page < 1:
        page = 1
    elif page > total_pages:
        page = total_pages
    
    # Calculate start and end indices for slicing
    start = (page - 1) * per_page
    end = start + per_page
    
    # Get the anime for the current page
    page_anime = anime_list_reversed[start:end]
    
    # Render the template with pagination data
    if request.method == 'POST':
        return render_template_string(
            page_template, 
            anime_list_reversed=anime_list_reversed,
            page_anime=page_anime,
            current_page=page,
            total_pages=total_pages
        )
    return render_template_string(
        page_template, 
        anime_list_reversed=anime_list_reversed,
        page_anime=page_anime,
        current_page=page,
        total_pages=total_pages
    )

@app.route('/detail/<int:anime_id>', methods=['GET', 'POST'])
def detail_route(anime_id):
    """
    Detail page route - shows detailed information about a specific anime
    
    Parameters:
    anime_id: The ID of the anime to display (integer)
    
    This finds the anime in the list by its ID
    If found, displays its details including download links
    If not found, returns a 404 error
    
    Returns:
    The detail page HTML with specific anime data
    """
    # Find the anime with matching ID
    # next() gets the first item that matches the condition
    # If no match, returns None
    anime = next((a for a in anime_list if a['id'] == anime_id), None)
    
    # If anime not found, return 404 error
    if anime is None:
        return "Anime not found", 404
    
    # Render the detail page with the anime data
    if request.method == 'POST':
        return render_template_string(detail_template, anime=anime)
    return render_template_string(detail_template, anime=anime)

# ============================================
# MAIN - Run the Application
# ============================================

if __name__ == '__main__':
    """
    This runs the Flask application when the script is executed directly
    debug=True allows hot reloading during development
    
    On PythonAnywhere, this file is imported as a module,
    so this section won't run there
    """
    app.run(debug=True, host='0.0.0.0', port=5000)