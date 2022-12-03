import csv
import itertools
import multiprocessing
import os
import random
import shutil
import time
from os.path import exists
import lxml.html
from lxml import etree

import requests
from bs4 import BeautifulSoup

headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '3600',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
}


# check if url is reachable≠
def url_checker(url):
    try:
        # Get Url
        get = requests.get(url)
        # if the request succeeds
        if get.status_code == 200:
            print(f"{url}: is reachable")
        else:
            return f"{url}: is Not reachable, status_code: {get.status_code}"

    # Exception
    except requests.exceptions.RequestException as e:
        # print URL with Errs
        raise SystemExit(f"{url}: is Not reachable \nErr: {e}")


# get the object listing pages of each type
def get_start_urls(num_of_pages_per_media):  # num of pages <= 100
    media_list = ['painting', 'prints', 'photography', 'sculpture', 'works-on-paper', 'mixed-media', 'design']
    prefix = 'https://www.artsy.net/collection/'
    # postfix example: '?page=1&metric=in'
    postfix1 = '?page='
    postfix2 = '&metric=in'
    start_urls = []
    start_urls_map = {}
    for media in media_list:
        start_urls_map[media] = []
        for page in range(1, num_of_pages_per_media + 1):
            # start_urls.append(prefix + media + postfix1 + str(page) + postfix2)
            start_urls_map[media].append(prefix + media + postfix1 + str(page) + postfix2)
    return start_urls_map


def get_work_url(start_url_list):  # input: list of url string
    time.sleep(3.0 * random.random())
    res = []
    for url in start_url_list:
        req = requests.get(url, headers)
        soup = BeautifulSoup(req.content, 'html.parser')
        a_item = soup.find_all('a', attrs={"data-testid": "metadata-artwork-link"})
        link = []
        for a in a_item:
            link.append("https://www.artsy.net" + a['href'])
        # 去重
        link = set(link)
        res += list(link)
    return res


def get_work_data(work_url, media, id):
    info_map = {}
    info_list = []

    try:

        url = work_url
        req = requests.get(url, headers)
        soup = BeautifulSoup(req.content, 'html.parser')
        # get artist_name, artist_url, work_name, work_year,
        artist_a = soup.find('a', attrs={
            "class": "RouterLink__RouterAwareLink-sc-1nwbtp5-0 ekDWRq ArtworkSidebar2Artists__StyledArtistLink-gyavil-0 iKbnpN"})
        artist_name = artist_a.text
        artist_url = "https://www.artsy.net" + artist_a['href']
        work_name_year = soup.find('h1',
                                   attrs={"class": "Box-sc-15se88d-0 Text-sc-18gcpao-0 caIGcn fiPLKL"}).text.strip()
        if work_name_year[-4:].isnumeric():
            work_name, work_year = ",".join(work_name_year.split(',')[:-1]), work_name_year.split(',')[-1].strip(' ')
        else:
            work_name= work_name_year
            work_year = None
        # dimension and media
        info_box = soup.find('div', attrs={"class": "Box-sc-15se88d-0 caIGcn"})
        info_box_divs = info_box.find_all('div')
        media_long, dimension = info_box_divs[0].text.strip(), info_box_divs[1].text.strip()

        # gallery 没爬
        '''# 可能问题： about the work/exhibition history
        potential_gallery = soup.find_all('a', attrs={
            "class": "RouterLink__RouterAwareLink-sc-1nwbtp5-0 guyBXx Box-sc-15se88d-0 Flex-cw39ct-0 cCmCIs"})
        temp = soup.find_all('a')'''

        gallery_a = soup.find('a', attrs={"class":"RouterLink__RouterAwareLink-sc-1nwbtp5-0 ekDWRq ArtworkSidebar2PartnerInfo__StyledPartnerLink-sc-1s2jic8-1 ERKdk"})
        gallery_url = "https://www.artsy.net" +gallery_a['href']
        gallery_name =  gallery_a.text.strip()
        

        # price  (bid == False) / estimated price (bid == True)
        estimated_price_div = soup.find('div', attrs={"class": "Box-sc-15se88d-0 Text-sc-18gcpao-0 eXbAnU caKFjP"})
        if estimated_price_div:
            bid = True
            price = estimated_price_div.text.strip()
        else:
            bid = False
            price = soup.find('div', attrs={"class": "Box-sc-15se88d-0 Text-sc-18gcpao-0 eXbAnU lcTzuI"}).text.strip()

        # img
        img_url = soup.find('img', attrs={"data-testid": "artwork-lightbox-image"})['src']

        # write dictionary
        info_list = [media + str(id), media, work_url, artist_name, artist_url, work_name,
                     work_year, media_long, dimension, gallery_name, gallery_url, bid, price, img_url]
        return info_list
    except Exception as e:
        print('failed to scrape %s' % url, e)
    '''info_map['id'] = media+str(id)
    info_map['media'] = media
    info_map['url'] = work_url
    info_map['artist_name'] = artist_name
    info_map['artist_url'] = artist_url
    info_map['work_name'] = work_name
    info_map['work_year'] = work_year
    info_map['media_long'] = media_long
    info_map['dimension'] = dimension
    info_map['bid'] = bid
    info_map['price'] = price
    info_map['img_url'] = img_url'''
    # info_map['path_to_img'] = 'images/%s/%s' % (str(media), str(media) + "_" + str(id) + ".png")


def img_downloader(link, img_folder_dir, media, img_id):
    time.sleep(0.2)
    r = requests.get(link, stream=True)
    path = os.path.join(img_folder_dir, media, media + str(img_id) + '.png')
    with open(path, 'wb') as f:
        r.raw.decode_content = True
        shutil.copyfileobj(r.raw, f)


def csv_writer(artwork_data, path_to_file):
    with open(path_to_file, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(artwork_data)


def main(pages):
    if exists("ArtsyResult"):
        shutil.rmtree("ArtsyResult")
        print("ArtsyResult has been deleted")
    media_list = ['painting', 'prints', 'photography', 'sculpture', 'works-on-paper', 'mixed-media', 'design']
    # create folder for each media
    mode = 0o777
    parent_dir = os.getcwd()
    ArtsyResult = "ArtsyResult"
    os.mkdir(os.path.join(parent_dir, ArtsyResult), mode)
    for media in media_list:
        path = os.path.join(parent_dir, ArtsyResult, media)
        os.mkdir(path, mode)
    print('result directory has been created')
    print(path)

    # initialize urls to all works
    work_url_map = {}
    for media in media_list:
        work_url_map[media] = []
    # add urls to work_url_map
    '''threadpool = Pool(multiprocessing.cpu_count() - 1)
    numbers = list(range(1, num_pages))
    wikiart_pages = threadpool.starmap(get_painting_list,
                                       zip(numbers, itertools.repeat(typep), itertools.repeat(searchword)))
    threadpool.close()
    threadpool.join()'''
    threadpool = multiprocessing.Pool(multiprocessing.cpu_count() - 1)
    start_urls_map = get_start_urls(pages)
    for m, links in start_urls_map.items():
        work_url_map[m] += get_work_url(links)

        print('media %s urls has been collected' % m)
    print('All url has been collected \n start to collect data ---')

    # create csv file
    csv_file = "ArtsyData.csv"
    csv_path = os.path.join(parent_dir, ArtsyResult, csv_file)
    print(csv_path)
    csv_header = ['id', 'media', 'url', 'artist_name', 'artist_url', 'work_name', 'work_year', 'media_long'
                ,'dimension', 'gallery_name', 'gallery_url', 'bid', 'price', 'img_url']
    with open(csv_path, 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(csv_header)
    # get art work data and write csv file
    for media, urls in work_url_map.items():
        count = 1
        for url in urls:
            try:
                data = get_work_data(url, media, count)
                csv_writer(data, csv_path)
                # print(data)
                img_downloader(data[-1], "ArtsyResult", media, count)
                count += 1

            except:
                continue
        print('%s data collecting is done' % (media))


if __name__ == '__main__':

    main(50)
