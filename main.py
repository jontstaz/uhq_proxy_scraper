import asyncio
from proxybroker import Broker
import warnings

warnings.filterwarnings('ignore');

async def save(proxies, filename):
    """Save proxies to a file."""
    with open(filename, 'w') as f:
        while True:
            proxy = await proxies.get()
            if proxy is None:
                break
            proto = 'https' if 'HTTPS' in proxy.types else 'http'
            row = '%s:%d\n' % (proxy.host, proxy.port)
            f.write(row)

async def show(proxies):
    while True:
        proxy = await proxies.get()
        if proxy is None: break
        print('%s:%d' % (proxy.host, proxy.port))


def get_user_proxy_choices():
    proxy_options = ['HTTP', 'HTTPS', 'SOCKS4', 'SOCKS5']
    while True:
        print("Proxy types: ")
        for index, option in enumerate(proxy_options, start=1):
            print(f"{index}. {option}")

        user_input = input("Enter the proxy types you want separated by ',' or space: ")

        if not user_input.strip():
            print("Input cannot be empty. Please provide a valid input.")
            continue

        chosen_proxy_indices = [int(x.strip()) - 1 for x in user_input.replace(',', ' ').split()]
        
        if all(x in range(len(proxy_options)) for x in chosen_proxy_indices):
            chosen_proxies = [proxy_options[x] for x in chosen_proxy_indices]
            return chosen_proxies
        else:
            print("Invalid format. Please provide a valid input.")

def get_user_proxy_countries():
    while True:
        country_choice = input("Do you wish to choose specific countries for proxies (1 = Yes, 0 = No)? ")

        if country_choice == '1':
            user_input = input("Enter the 2-character country codes separated by ',' or space: ")
            chosen_countries = [x.strip().upper() for x in user_input.replace(',', ' ').split()]

            if all(len(x) == 2 and x.isalpha() for x in chosen_countries):
                return chosen_countries
            else:
                print("Invalid format. Please provide a valid input.")
                continue

        elif country_choice == '0':
            return None
        else:
            print("Invalid choice. Please enter 1 or 0.")


def main():
    numProxies = int(input("How many proxies do you want to fetch? "))
    proxyType = get_user_proxy_choices()
    proxyCountries = get_user_proxy_countries()
    saveOutput = int(input("Do you want to output proxies to terminal or save to file (1 = Save to File, 0 = Output to Terminal)? "))
    if saveOutput == 1:
        fileOutput = str(input("Where to save the proxies? Eg. 'http-proxies.txt' "))
        while fileOutput == "":
            print("Error. You must enter a .txt file output.")
            fileOutput = str(input("Where to save the proxies? Eg. 'http-proxies.txt' "))
    proxies = asyncio.Queue()
    broker = Broker(proxies)
    if proxyCountries is None:
        if saveOutput == 1:
            print("Processing... Please note: if you've selected a large amount of proxies this may take some time...")
            tasks = asyncio.gather(broker.find(types=proxyType, limit=numProxies),
                                save(proxies, filename=fileOutput))
        else:
            tasks = asyncio.gather(broker.find(types=proxyType, limit=numProxies),
                                show(proxies))
            
    else:
        if saveOutput == 1:
            print("Processing... Please note: if you've selected a large amount of proxies this may take some time...")
            tasks = asyncio.gather(broker.find(types=proxyType, countries=proxyCountries, limit=numProxies),
                                save(proxies, filename=fileOutput))
        else:
            tasks = asyncio.gather(broker.find(types=proxyType, limit=numProxies),
                                show(proxies))
    loop = asyncio.get_event_loop()
    loop.run_until_complete(tasks)


if __name__ == '__main__':
    main()
