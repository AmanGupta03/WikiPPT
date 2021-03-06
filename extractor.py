"""
return dictionary object 'data' as follows -:
{
    'topic': 'Main Heading'
    'no_of_head': 'No. of Sub Headings'
    'introduction': 'One line description along with heading'
    #list of subheadings
    'section': [ 
        {
            'heading':  'sub Heading title'
            #list of points 
            'content': [ 
                {
                    'title': 'name of sub-sub heading, can be empty'
                    'desc': 'list of points from sub-sub-heading'
                }
            ]
        }
    ]
}
"""

import summarizer
import wikipediaapi
import json

def data_for_ppt(content, slide_per_head=1):
    data = []
    for head in content.sections:
        sec_info = {}
        head_content = []
        sec_info['heading'] = head.title
        point = {}
        point['title'] = ''
        point['desc'] = head.text
        head_content.append(point)
        for sub_head in head.sections:
            point = {}
            point['title'] = sub_head.title
            point['desc'] = sub_head.text
            head_content.append(point)
        sec_info['content'] = summarizer.bullets(head_content, slide_per_head)
        data.append(sec_info)
    return data

data = {}
topic = 'Operating System'  # to be input

print('Fetching Content...')
wiki = wikipediaapi.Wikipedia(language='en', extract_format=wikipediaapi.ExtractFormat.WIKI)
#Exception Handling Pending..
content = wiki.page(topic)

print('Modifying data...')

data['topic'] = topic
data['no_of_head'] = len(content.sections)
data['introduction'] = summarizer.extract_intro(content.text)
data['sections'] = data_for_ppt(content)

print(json.dumps(data, indent=4)) #json to pretiffy
