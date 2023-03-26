import csv
import os
import re
import shutil
import subprocess
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from stem import Signal
from stem.control import Controller
from config import BTC, SHARE


# подмена заголовка при отправке запроса на сайт
def get_headers_from_fake():
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "accept-encoding": "gzip, deflate, br",
        "connection": "keep-alive",
        "user-agent": f"{UserAgent()}"
    }
    return headers



# получение количества страниц на www.walletexplorer.com
def get_count_page_on_wallet():
    r = requests.get(f'https://www.walletexplorer.com/address/{BTC}',
                     headers=get_headers_from_fake())
    # sleep(1)
    if r.status_code == 200:
        soup = BeautifulSoup(r.text, "html.parser")
        PAGING = soup.find('div', class_='paging').text.split('/')[1].split(' ')[1].strip()
        # print(PAGING)
        return PAGING



# локальный запуск Tor
def get_tor_process():
    subprocess.Popen('PathToTor -f torrc', cwd='PathToTor')



# отправка сигнала на переподключение к Tor
def renew_connection_tor(port):
    with Controller.from_port(port=port) as controller:
        controller.authenticate(password="passw")  # tor --hash-password password
        # отправить сигнал NEWNYM для установления нового чистого соединения через сеть Tor
        controller.signal(Signal.NEWNYM)



# получение списка портов
def get_list_with_port():
    list_with_port = [9050, 9052, 9054, 9056, 9058, 9060, 9062, 9064, 9066, 9068, 9070, 9072, 9074, 9076, 9078, 9080,
                      9082, 9084, 9086, 9088, 9090]
    return list_with_port



# создание и удаление папки
def remove_and_create_folder(folder):
    if folder:
        shutil.rmtree(folder, ignore_errors=True)
    os.makedirs(folder)
    os.chdir(folder)



# формируем файл f"{BTC}_txid.csv", который содержит TXID
def execute_txid():
    os.chdir(SHARE)
    if f'{BTC}.csv':
        with open(f'{BTC}.csv', 'r') as csvfile:
            reader = csv.reader(csvfile)
            for list_line in reader:
                for line in list_line:
                    txid_list = re.findall('[a-z0-9]{64}', line)
                    if txid_list:
                        with open(f"{BTC}_txid.csv", "a") as csvfile2:
                            writer2 = csv.writer(csvfile2)
                            writer2.writerow(txid_list)
                        break



# получаем список TXID из файла f"{BTC}_txid.csv"
def get_list_txid():
    os.chdir(SHARE)
    if f"{BTC}_txid.csv":
        LIST_TXID = []
        with open(f"{BTC}_txid.csv", 'r') as csvfile:
            for line_list in csv.reader(csvfile):
                for line in line_list:
                    LIST_TXID.append(line)
            return LIST_TXID



# получаем файл result.csv, в который добавлены доменные имена .com из {BTC}_with_com.csv
def get_res_csv_with_com():
    os.chdir(SHARE)
    if f"{BTC}_with_com.csv":
        with open(f"{BTC}_with_com.csv", 'r') as csvfile:
            reader = csv.reader(csvfile)
            for list_line in reader:
                for line in list_line:
                    if '.com' in line:
                        with open("result.csv", "a") as csvfile2:
                            writer1 = csv.writer(csvfile2)
                            writer1.writerow(list_line)
                        break