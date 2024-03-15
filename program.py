import os
import sys
import requests
import time
import concurrent.futures
import asyncio
import aiohttp

def download_image(url):
    filename = url.split('/')[-1]
    response = requests.get(url)
    with open(filename, 'wb') as file:
        file.write(response.content)
    return filename

async def async_download_image(session, url):
    filename = url.split('/')[-1]
    async with session.get(url) as response:
        with open(filename, 'wb') as file:
            file.write(await response.read())
    return filename

def download_images_thread_pool(urls):
    start_time = time.time()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = list(executor.map(download_image, urls))
    end_time = time.time()
    return results, end_time - start_time

def download_images_process_pool(urls):
    start_time = time.time()
    with concurrent.futures.ProcessPoolExecutor() as executor:
        results = list(executor.map(download_image, urls))
    end_time = time.time()
    return results, end_time - start_time

async def download_images_async(urls):
    start_time = time.time()
    async with aiohttp.ClientSession() as session:
        tasks = [async_download_image(session, url) for url in urls]
        results = await asyncio.gather(*tasks)
    end_time = time.time()
    return results, end_time - start_time

if __name__ == '__main__':
    urls = sys.argv[1:]

    # Скачивание изображений с использованием многопоточности
    thread_results, thread_time = download_images_thread_pool(urls)
    print("Скачивание с использованием многопоточности:")
    for image in thread_results:
        print(f"Изображение {image} загружено.")
    print(f"Общее время выполнения: {thread_time} секунд")

    # Скачивание изображений с использованием многопроцессорности
    process_results, process_time = download_images_process_pool(urls)
    print("\nСкачивание с использованием многопроцессорности:")
    for image in process_results:
        print(f"Изображение {image} загружено.")
    print(f"Общее время выполнения: {process_time} секунд")

    # Скачивание изображений с использованием асинхронности
    loop = asyncio.get_event_loop()
    async_results, async_time = loop.run_until_complete(download_images_async(urls))
    print("\nСкачивание с использованием асинхронности:")
    for image in async_results:
        print(f"Изображение {image} загружено.")
    print(f"Общее время выполнения: {async_time} секунд")
