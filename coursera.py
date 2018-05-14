import argparse
import requests
import re
from bs4 import BeautifulSoup
import os
import sys
import time
from openpyxl import Workbook


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-o',
        '--output',
        help='output path',
        default=get_default_path(),
        type=str
    )
    parser.add_argument(
        '-n', '--number', help='number of courses', default=20, type=int
    )
    return parser.parse_args()


def get_course_response(url):
    return requests.get(url).content


def get_default_path():
    return '{}{}{}{}'.format(os.getcwd(), os.sep, int(time.time()), '.xlsx')


def get_courses_list(courses_page):
    soup = BeautifulSoup(courses_page, 'xml')
    return [x.text for x in soup.find_all('loc')]


def parse_course_response(course_response):
    course_dict = {}
    soup = BeautifulSoup(course_response, 'html.parser')
    course_dict['name'] = soup.find(class_='title display-3-text').text
    course_dict['language'] = soup.find(class_='rc-Language').text
    start_date = soup.find(
        class_='startdate rc-StartDateString caption-text'
    ).text
    course_dict['start_date'] = ' '.join(start_date.split(' ')[1:])
    rating = soup.find(class_='ratings-text bt3-hidden-xs')
    if rating:
        rating = re.sub('[^0-9.]', '', rating.text)
    course_dict['rating'] = rating
    course_dict['weeks'] = len(soup.find_all(class_='week'))
    return course_dict


def get_courses_info(courses_url_list, count_courses):
    courses_info = []
    for course_url in courses_url_list[:count_courses]:
        course_response = get_course_response(course_url)
        course_dict = parse_course_response(course_response)
        courses_info.append(course_dict)
    return courses_info


def courses_info_to_xlsx(courses_list):
    header = ['Name', 'Language', 'Start date', 'Rating', 'Weeks', ]
    wb = Workbook()
    sheet = wb.active
    sheet.title = 'Coursera courses'
    sheet.append(header)
    for course in courses_list:
        sheet.append(
            {1: course['name'],
             2: course['language'],
             3: course['start_date'],
             4: course['rating'],
             5: course['weeks']}
        )
    return wb


def output_courses_info_to_xlsx(wb, filepath):
    wb.save(filepath)


if __name__ == '__main__':
    args = create_parser()

    output_path = args.output
    sitemap_url = 'https://www.coursera.org/sitemap~www~courses.xml'

    courses_page_requests = get_course_response(sitemap_url)
    courses_url_list = get_courses_list(courses_page_requests)
    courses_dict = get_courses_info(courses_url_list, args.number)
    xlsx_workbook = courses_info_to_xlsx(courses_dict)

    if os.path.exists(output_path):
        sys.exit('File exists. Program will exit')

    output_courses_info_to_xlsx(xlsx_workbook, output_path)
    print('The file has been created:{}'.format(output_path))
