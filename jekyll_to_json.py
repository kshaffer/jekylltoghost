import yaml
import json
import os


"""
Specify the Jekyll post directory (relative to this file's location)
and the output file name.
"""

post_directory = '../_posts/'
new_filename = 'jekyll_to_ghost.json'


"""
Get list of .md or .markdown files from that directory.
(Modify if source files have different extensions.)
"""

file_list = []
for f in os.listdir(post_directory):
    if '.md' in f or '.markdown' in f:
        file_list.append(f)


"""
Build an empty dictionary structure for the output file.
"""

json_object = {}
json_object['db'] = []
posts_object = {}
posts_object['data'] = {}
posts_object['data']['posts'] = []


"""
Create a JSON object for each markdown file in the posts directory.
This section assumes certain names for YAML parameters.
Edit as necessary to fit YAML parameters used by your blog/theme.
"""

for filename in file_list:
    original = open(post_directory + filename, 'r', encoding='utf-8')
    parsed = ''

    for line in original:
        parsed += line

    parsed = parsed.split('---\n')
    header = yaml.load(parsed[1])
    header['content'] = parsed[2].replace('/assets/images/', '/content/images/')

    post_object = {
    "id": 0,
    "title": "",
    "slug": "",
    "markdown": "",
    "html": "",
    "image": "",
    "featured": 0,
    "page": 0,
    "status": "published",
    "language": "en_US",
    "meta_title": "",
    "meta_description": "",
    "author_id": 1,
    "created_at": "",
    "created_by": 1,
    "updated_at": "",
    "updated_by": 1,
    "published_at": "",
    "published_by": 1
    }

    post_object['title'] = post_object['og_title'] = post_object['twitter_title'] = header['title']
    post_object['meta_title'] = header['title']
    post_object['slug'] = filename[11:].split('.')[0]
    try:
        post_object['meta_description'] = post_object['og_description'] = post_object['twitter_description'] = header['short_description']
    except:
        post_object['meta_description'] = post_object['og_description'] = post_object['twitter_description'] = ''
    try:
        post_object['created_at'] = post_object['updated_at'] = post_object['published_at'] = str(header['modified'])
    except:
        post_object['created_at'] = post_object['updated_at'] = post_object['published_at'] = str(header['date'])
    post_object['markdown'] = header['content']
    try:
        post_object['image'] = post_object['og_image'] = post_object['twitter_image'] = '/content/images/' + header['image']['feature']
    except:
        post_object['image'] = post_object['og_image'] = post_object['twitter_image'] = ''

    posts_object['data']['posts'].append(post_object)


"""
Insert all post objects into the blank database created above, following
the structure expected by Ghost. Write to file (name provided above).
"""

json_object['db'].append(posts_object)

with open(new_filename, 'w') as new_file:
    # new_file.write(str(header))
    json.dump(json_object, new_file, indent = 4)
