import argparse
import requests
import re
from bs4 import BeautifulSoup
import os
import time
from openpyxl import Workbook


def create_parser(*args):
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--output', help='output path', type=str)
    parser.add_argument('-n', '--number', help='number of courses', type=int)
    return parser.parse_args()


def get_courses_page(url):
    return requests.get(url)


def get_courses_list(courses_page):
    soup = BeautifulSoup(courses_page.content, 'xml')
    return [x.text for x in soup.find_all('loc')]


def get_course_info(courses_url_list, count_courses):
    if not count_courses:
        count_courses = 20
    course_info = {}
    for course_url in courses_url_list[:count_courses]:
        course_page = get_courses_page(course_url)
        souped_url = BeautifulSoup(course_page.content, 'lxml')
        course_name = souped_url.find(class_='title display-3-text').text
        language = souped_url.find(class_='rc-Language').text
        start_date = souped_url.\
            find(class_='startdate rc-StartDateString caption-text').text
        start_date = ' '.join(start_date.split(' ')[1:])
        rating = souped_url.find(class_='ratings-text bt3-hidden-xs')
        number_of_weeks = len(souped_url.find_all(class_='week'))
        if rating:
            rating = re.sub('[^0-9.]', '', rating.text)
        course_info[course_name] = {
            'language': language,
            'start_date': start_date,
            'rating': rating,
            'number_of_weeks': number_of_weeks
        }
    return course_info


def dict_to_xlsx(courses_dict):
    wb = Workbook()
    sheet = wb.active
    sheet.title = 'Coursera courses'
    sheet.cell(row=1, column=1, value='Courses:')
    sheet.cell(row=2, column=1, value='Name')
    sheet.cell(row=2, column=2, value='Language')
    sheet.cell(row=2, column=3, value='Weeks')
    sheet.cell(row=2, column=4, value='Start date')
    sheet.cell(row=2, column=5, value='Rating')
    actual_row = 3
    for course, value in courses_dict.items():
        sheet.cell(row=actual_row, column=1, value=course)
        sheet.cell(row=actual_row, column=2, value=value['language'])
        sheet.cell(row=actual_row, column=3, value=value['number_of_weeks'])
        sheet.cell(row=actual_row, column=4, value=value['start_date'])
        sheet.cell(row=actual_row, column=5, value=value['rating'])
        actual_row += 1
    return wb


def output_courses_info_to_xlsx(wb, filepath):
    wb.save(filepath)


if __name__ == '__main__':
    args = create_parser()

    if args.output:
        output_path = args.output
    else:
        output_path = (
            '{}{}{}{}'.format(os.getcwd(), os.sep, int(time.time()), '.xlsx')
        )

    sitemap_courses = 'https://www.coursera.org/sitemap~www~courses.xml'
    courses_page_requests = get_courses_page(sitemap_courses)
    courses_url_list = get_courses_list(courses_page_requests)
    courses_dict = get_course_info(courses_url_list, args.number)
    xlsx_workbook = dict_to_xlsx(courses_dict)

    if os.path.exists(output_path):
        print('Output path exists. The file will be overriden')
        os.remove(output_path)

    output_courses_info_to_xlsx(xlsx_workbook, output_path)
    print('The file has been created:{}'.format(output_path))
