## **_Определение криптовалютных бирж, связанных с интересующим криптовалютным кошельком BTC на основе анализа ("парсинга") сайта https://www.walletexplorer.com/_**.

### *Хорошая статья по теме "Block Explorer"(<https://bytwork.com/articles/block-explorer>).
### Предварительно устанавливаем: python 3.9(<https://www.python.org/downloads/release/python-390/>), PyCharm (<https://www.jetbrains.com/ru-ru/pycharm/download/>).
### 1. Клонируем репозиторий в любую папку (в пути не использовать кириллицу).
### 2. Устанавливаем необходимые зависимости через терминал в PyCharm:
```
pip install aiohttp
pip install aiosocksy
pip install beautifulsoup4
pip install asyncio
pip install requests
pip install fake-useragent
pip install stem
```
### 3. В файле config.py задаем путь для размещения папки **_SHARE_** (в данной папке будут создаваться необходимые для анализа файлы в формате *.csv - **_{BTC}.csv_**, **_{BTC}_txid.csv_**, **_{BTC}_with_com.csv_**, **_result.csv_**) и интересующий нас адрес кошелька BTC.
### 4. Параметры, которые необходимо определить для корректной работы скрипта: **_get_tor_process()_** в **_function.py_** - путь к локальной папке с Tor(с конфигурационном файлом torrc).
Пример конфигурационного файла torrc:
```
SocksPort 127.0.0.1:9050 # SocksPort
ControlPort 9051 # Порт для переподключения к сети Tor

SocksPort 127.0.0.1:9052
ControlPort 9053

SocksPort 127.0.0.1:9054
ControlPort 9055 
# далее - по аналогии

DataDirectory "PathToTor" # путь к Tor
HashedControlPassword 16:86D9F86325796C3A607465CF77952A4A84085DEAE16F6BFBFD4DD81468 # соответствует значению passw в renew_connection_tor(port)
ClientTransportPlugin obfs4 exec "PathToTor"\obfs4proxy.exe # путь к файлу с obfs4proxy.exe
Bridge obfs4 # мосты получаете через Telegram Bot Tor или через "запрос" на мосты после установки браузера Tor (ссылки придется поискать самим, в том числе необходимо найти инструкцию по локальной установке Tor на компьютер)

UseBridges 1
EnforceDistinctSubnets 1
ConnectionPadding 1
ReducedConnectionPadding 1
CircuitPadding 0
ReducedCircuitPadding 1
NewCircuitPeriod 10
```
### *Пояснение к методам из функции **_main_**:
### 5. Информация из консоли при запуске **_get_tor_process()_**:
![tor1](Pictures\tor1.png)
![tor2](Pictures\tor2.png)
![tor3](Pictures\tor3.png)

### 5.1. Блок кода:
```
c = RECEIVE_TXID_BY_WALLET()
    asyncio.get_event_loop().run_until_complete(c.gather_data())
```
вызывает метод
```
async def get_page_data из класса RECEIVE_TXID_BY_WALLET()
```
В результате выполнения метода в папке **_SHARE_** формируется файл **_{BTC}.csv_**.
### Информация из консоли:
![item4](Pictures\item4.png)

### Информация из файла **_{BTC}.csv_**:
![item4_1](Pictures\item4_1.png)

### 5.2. Информация из консоли при запуске **_execute_txid()_** (происходит формирование файла **{BTC}_txid.csv** из **_{BTC}.csv_**):
![item5](Pictures\item5.png)

### 5.3. Блок кода:

```
c2 = RECEIVE_COM_BY_TXID()
    asyncio.get_event_loop().run_until_complete(c2.gather_data())
```
вызывает метод **_get_page_data_** из класса RECEIVE_COM_BY_TXID(), при этом происходит отправка запросов на сайт с каждым TXID из файла **{BTC}_txid.csv_**

### Информация из консоли:
![item5](Pictures\item6.png)

### 6. В резульатате формируются 2 файла: **{BTC}_with_com.csv** (из него - **_result.csv_**) с интересующим нас содержиымым:
![result](Pictures\result.png)
Здесь для примера представлена связь по 1-му TXID с другими криптовалютными кошельками и криптовалютными биржами (в итоговом файле добавлены также дата, время, а также другая информация, определяющая конкретную криптовалютную транзакцию).