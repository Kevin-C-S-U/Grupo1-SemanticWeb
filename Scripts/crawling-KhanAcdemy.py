from bs4 import BeautifulSoup
import urllib.request
import requests
import pandas as pd

url = "https://en.khanacademy.org/"
response = requests.get(url)

soup = BeautifulSoup(response.content, 'html.parser')

links = soup.find_all('a',{'class':"_pt9he7" })

categories = {'name':[],
              'link':[]}

courses = {'name':[],
          'link':[],
          'category':[],
           'categoryLink':[],
           'language':[]}

for link in links:
    if len(link.get('href').split("/")[1:]) == 1:
        category = link.get('href').split("/")[1:][0]
        categories['name'].append(category)
        categories['link'].append(link.get('href'))
    else:
        category = link.get('href').split("/")[1:][0]
        course = link.get('href').split("/")[1:][1]
        courses['name'].append(course)
        courses['link'].append(link.get('href'))
        courses['category'].append(category)
        courses['categoryLink'].append('/'+category)


course_links = []
for value in courses['link']:
    course_links.append(url+value[1:])

units = {'name':[],
         'link':[],
         'course':[],
         'courseLink':[],
         'description':[]}

lessons = {'name':[],
           'link':[]}

num = 0
for link in course_links:
    urllink = link
    response = requests.get(urllink)
    print(urllink)
    soupCourse = BeautifulSoup(response.content, 'html.parser')
    links = soupCourse.find('h1',{'class':"_1eqoe4n8" })
    name = ""
    if links is None:
        courses['name'][num] = ''
    else:
        courses['name'][num] = links.text
    courses['language'] = url[8:10]
    unit_links = soupCourse.findAll('a',{'class':"_dwmetq", 'data-test-id':"unit-header"})
    for unit_link in unit_links:
        units['name'].append(unit_link.text)
        units['link'].append(unit_link.get('href'))
        units['course'].append(links.text)
        units['courseLink'].append(link)
    num +=1

num = 0
for link in units['link']:
    urllink = url + link[1:]
    response = requests.get(urllink)
    print(urllink)
    soupUnit = BeautifulSoup(response.content, 'html.parser')
    lesson_links = soupUnit.find("span",{"class":'_1djt3vmr'})
    if lesson_links:
        units['description'].append(lesson_links.text)
    else:
        units['description'].append('')
    num +=1
    print(num)


lessons = {
    'name':[],
    'link':[],
    'unit':[],
    'unitLink':[],
    'content':[]
}

num = 0
for unitLink in units['link']:
    response = requests.get(url + unitLink[1:])
    soupUnit = BeautifulSoup(response.content, 'html.parser')
    lessons_list = soupUnit.findAll('a',{"class":'_dwmetq',"data-test-id":"lesson-card-link"})
    for i in lessons_list:
        if i.get('href')[:4]!='http':
            lessons['name'].append(i.text)
            lessons['link'].append(i.get('href'))
            lessons['unit'].append(units['name'][num])
            lessons['unitLink'].append(unitLink)
    num += 1
    print(num)

num = 0
for lesson_link in lessons['link']:
    response = requests.get(url + lesson_link[:1])
    soupUnit = BeautifulSoup(response.content, 'html.parser')
    lessons_list = soupUnit.findAll("a")
    text = ''
    for i in lessons_list:
        text += i.text
    lessons['content'].append(text)
    num += 1
    print(num)

category_df = pd.DataFrame(categories)
course_df = pd.DataFrame(courses) 
units_df = pd.DataFrame(units) 
lessons_df = pd.DataFrame(lessons) 

category_df.to_csv('category1.csv', index=False)
course_df.to_csv('course1.csv', index=False)
units_df.to_csv('units1.csv', index=False)
lessons_df.to_csv('lessons1.csv', index=False)