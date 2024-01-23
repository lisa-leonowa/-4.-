# Написать программу, которая скачивает изображения с заданных URL-адресов и сохраняет их на диск. Каждое изображение
# должно сохраняться в отдельном файле, название которого соответствует названию изображения в URL-адресе.
# Например, URL-адрес: https://example/images/image1.jpg -> файл на диске: image1.jpg
# — Программа должна использовать многопоточный, многопроцессорный и асинхронный подходы.
# — Программа должна иметь возможность задавать список URL-адресов через аргументы командной строки.
# — Программа должна выводить в консоль информацию о времени скачивания каждого изображения и общем времени выполнения
#   программы.

import requests
import os
import time
import argparse
from multiprocessing.pool import ThreadPool
from concurrent.futures import ThreadPoolExecutor
import aiohttp
import asyncio


def download_image(url):
    folder_save = 'data_homework'
    if not os.path.exists(folder_save):
        os.mkdir(folder_save)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            filename = os.path.basename(url)
            with open(f'{folder_save}/{filename}', 'wb') as file:
                file.write(response.content)
            # print(f"Изображение {filename} успешно скачано.")
        else:
            print(f"Не удалось скачать изображение по адресу: {url}")
    except Exception as e:
        print(f"Ошибка при скачивании изображения: {e}")


# Многопоточный подход
def download_images_multithread(urls):
    start_time = time.time()
    pool = ThreadPool()
    pool.map(download_image, urls)
    pool.terminate()
    pool.join()
    end_time = time.time()
    total_time = end_time - start_time
    print(f"Общее время выполнения (многопоточный подход): {total_time} сек.")


# Многопроцессный подход:
def download_images_multiprocess(urls):
    start_time = time.time()
    with ThreadPoolExecutor() as executor:
        executor.map(download_image, urls)
    end_time = time.time()
    total_time = end_time - start_time
    print(f"Общее время выполнения (многопроцессный подход): {total_time} сек.")


# Асинхронный подход
async def download_image_async(url, session):
    try:
        async with session.get(url) as response:
            if response.status == 200:
                filename = os.path.basename(url)

                folder_save = 'data_homework'
                if not os.path.exists(folder_save):
                    os.mkdir(folder_save)

                with open(f'{folder_save}/{filename}', 'wb') as file:
                    file.write(await response.read())
                # print(f"Изображение {filename} успешно скачано.")
            else:
                print(f"Не удалось скачать изображение по адресу: {url}")
    except Exception as e:
        print(f"Ошибка при асинхронном скачивании изображения: {e}")


# Асинхронный подход
async def download_images_async(urls):
    start_time = time.time()
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in urls:
            task = asyncio.create_task(download_image_async(url, session))
            tasks.append(task)
        await asyncio.gather(*tasks)
    end_time = time.time()
    total_time = end_time - start_time
    print(f"Общее время выполнения (асинхронный подход): {total_time} сек.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("urls", nargs="+", help="Список URL-адресов для скачивания изображений")
    args = parser.parse_args()

    urls = args.urls

    # urls = ['https://klike.net/uploads/posts/2020-05/1588749677_1.jpg',
    #         'https://cdn.trinixy.ru/pics6/20230526/238923_1_trinixy_ru.jpg',
    #         'https://kartin.papik.pro/uploads/posts/2023-06/1686736061_kartin-papik-pro-p-kartinki-krasivie-na-avatarku-priroda-zima-62.jpg']

    # Многопоточный подход:
    download_images_multithread(urls)

    # Многопроцессный подход:
    download_images_multiprocess(urls)

    # Асинхронный подход:
    asyncio.run(download_images_async(urls))
