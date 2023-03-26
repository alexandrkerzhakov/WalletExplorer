import asyncio
import csv
import random
import aiohttp
import aiosocksy
from aiosocksy.connector import ProxyConnector, ProxyClientRequest
from bs4 import BeautifulSoup
from config import BTC, SHARE
from function import get_headers_from_fake, get_tor_process, get_count_page_on_wallet, renew_connection_tor, \
    get_list_with_port, remove_and_create_folder, get_list_txid, execute_txid, get_res_csv_with_com


class RECEIVE_TXID_BY_WALLET:

    async def get_page_data(self, session, page, port):
        url = f'https://www.walletexplorer.com/address/{BTC}?page={page}'
        async with session.get(url=url, headers=get_headers_from_fake(),
                               proxy=f'socks5://127.0.0.1:{port}') as r:
            soup = BeautifulSoup(await r.text(), "html.parser")
            TRANSACTION_ALL_TAG = soup.findAll('tr', class_=['sent', 'received'])
            for tag in TRANSACTION_ALL_TAG:
                # SENT or RECEIVED
                TYPE = str(tag.attrs['class'][0]).upper()
                print(TYPE)

                # DATE
                DATE = tag.find('td', class_='date').text
                print("DATE : " + DATE)

                # WALLET ID
                WALLET_ID = []  # Список ID по транзакции
                for wallet_line in tag.find_all('td', class_='walletid'):
                    if wallet_line.find('a') is not None:
                        wal_id = wallet_line.find('a').get('href').split('/')[2]
                        WALLET_ID.append(wal_id.strip())
                        print("WALLET ID : " + wal_id)

                # SUM
                SUM = []  # Список сумм по транзакции
                for sum in tag.find_all('td', class_='amount diff'):
                    if sum.text is not None:
                        if sum.find('em'):
                            # print('fee')
                            WALLET_ID.append('fee')
                        sum = sum.text
                        SUM.append(sum.strip())
                        print("SUM : " + sum)

                # BALANCE
                BALANCE = ''  # Столбец BALANCE
                for bal in tag.find_all('td', class_='amount'):
                    if len(bal.attrs['class']) == 1:
                        BALANCE = bal.text
                        print("BALANCE : " + BALANCE)

                # TXID
                TXID = tag.find('td', class_='txid').find('a').get('href').split('/')[2]
                print("TXID : " + TXID)

                with open(f"{BTC}.csv", "a") as file: # формирование файла f"{BTC}_page.csv" с полным списком транзакций
                    writer = csv.writer(file)
                    writer.writerow(
                        (
                            DATE.strip(),
                            TYPE.strip(),
                            SUM,
                            WALLET_ID,
                            BALANCE.strip(),
                            TXID.strip(),
                        )
                    )

                print('--------------------------------' + str(page) + '--------------------------------------------')

        with open(f"{BTC}_page.csv", "a") as file2: # формирование файла со списком обработанных страниц (необязательно)
            writer = csv.writer(file2)
            writer.writerow(
                (
                    str(page)
                )
            )
        renew_connection_tor(port + 1) # переподключение к сети Tor

    async def gather_data(self):
        try:
            async with asyncio.Semaphore(100):
                connector = ProxyConnector()
                async with aiohttp.ClientSession(connector=connector, request_class=ProxyClientRequest) as session:
                    tasks = []
                    PAGE = []
                    for page in range(1, int(get_count_page_on_wallet())):
                        port = get_list_with_port()[random.randint(0, 20)]
                        await asyncio.sleep(0.1)  # нужно тестировать, иногда требуется увеличение времени задержки до 0.5-1
                        task = asyncio.create_task(self.get_page_data(session, page, port))
                        print(task)
                        tasks.append(task)
                        PAGE.append(page)
                    await asyncio.gather(*tasks)
        except aiosocksy.errors.SocksError:
            print("Can not connect to site")  # for last page (task for last page)

        except aiohttp.ClientConnectionError:
            print("Oops, the connection was dropped before we finished")  # for last page (task for last page)

class RECEIVE_COM_BY_TXID:

    async def get_page_data(self, session, txid, port):
        url = f'https://www.walletexplorer.com/txid/{txid}'
        async with session.get(url=url, headers=get_headers_from_fake(), proxy=f'socks5://127.0.0.1:{port}') as r:
            soup = BeautifulSoup(await r.text(), "html.parser")
            ALL_TAG_TR = soup.findAll('tr')

            INPUTS_WALLET = []
            OUTPUTS_WALLET = []

            # TXID
            try:
                TXID = ALL_TAG_TR[0].find('td').text
                print(TXID)
            except:
                IXID = 'None'

            # INCLUDED_IN_BLOCK
            try:
                INCLUDED_IN_BLOCK = ALL_TAG_TR[1].find('td').text
                print(INCLUDED_IN_BLOCK)
            except:
                INCLUDED_IN_BLOCK = 'None'

            # TIME
            try:
                TIME = ALL_TAG_TR[2].find('td').text
                print(TIME)
            except:
                TIME = 'None'

            # SENDER
            try:
                SENDER = ALL_TAG_TR[3].find('td').text
                print(SENDER)
            except:
                SENDER = 'None'

            # FEE
            try:
                FEE = ALL_TAG_TR[4].find('td').text
                print(FEE)
            except:
                FEE = 'None'

            # SIZE
            try:
                SIZE = ALL_TAG_TR[5].find('td').text
                print(SIZE)
            except:
                SIZE = 'None'

            # INPUTS WALLET AND OUTPUTS WALLET
            try:
                for t in ALL_TAG_TR:
                    if t.find('table', class_='empty'):
                        for tag_inp_wal in t.find_all_next('table', class_='empty')[0].find_all('a'):
                            inp_wallet = tag_inp_wal.get('href').strip()
                            INPUTS_WALLET.append(inp_wallet)
                            print(inp_wallet)
                        for tag_out_wal in t.find_all_next('table', class_='empty')[1].find_all('a'):
                            out_wallet = tag_out_wal.get('href').strip()
                            OUTPUTS_WALLET.append(out_wallet)
                            print(out_wallet)
            except:
                INPUTS_WALLET = None
                OUTPUTS_WALLET = None

            with open(f"{BTC}_with_com.csv", "a") as file: # формирование файла {BTC}_with_com.csv
                writer = csv.writer(file)
                writer.writerow(
                    (
                        TXID,
                        INCLUDED_IN_BLOCK,
                        TIME,
                        SENDER,
                        FEE,
                        SIZE,
                        INPUTS_WALLET,
                        OUTPUTS_WALLET
                    )
                )
            print('--------------------------------' + txid + '--------------------------------------------')
        renew_connection_tor(port + 1)

    async def gather_data(self):
        async with asyncio.Semaphore(100):
            connector = ProxyConnector()
            async with aiohttp.ClientSession(connector=connector, request_class=ProxyClientRequest) as session:
                tasks = []
                for txid in get_list_txid():
                    port = get_list_with_port()[random.randint(0, 20)]
                    await asyncio.sleep(0.1)
                    task = asyncio.create_task(self.get_page_data(session, txid, port))
                    # print(task)
                    tasks.append(task)
                await asyncio.gather(*tasks)


if __name__ == '__main__':
    remove_and_create_folder(SHARE)
    get_tor_process()

    c = RECEIVE_TXID_BY_WALLET()
    asyncio.get_event_loop().run_until_complete(c.gather_data())

    execute_txid()

    c2 = RECEIVE_COM_BY_TXID()
    asyncio.get_event_loop().run_until_complete(c2.gather_data())

    get_res_csv_with_com()
