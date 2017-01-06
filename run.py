from jinja2 import Environment, FileSystemLoader
import json, os
import markdown

def make_environment():
	loader = FileSystemLoader(os.getcwd())
	env = Environment(loader=loader)
	return env

env = make_environment()

def render_static_to_html(env):
	abs_path = os.getcwd()
	static_template = env.get_template('static_template.html')
	static_template.stream(path_to_dir=abs_path).dump('static.html')

render_static_to_html(env)

template = env.get_template('md_template.html')


def get_json_config():
	with open('config.json') as f:
		data = json.load(f)
	return data

json = get_json_config()
articles = [x['source'] for x in json['articles']]

def get_rendered_markdown_text_from_file(path_to_file):
	markdown_text = open(path_to_file).read()
	rendered_text = markdown.Markdown().convert(markdown_text)
	return rendered_text

abs_path = os.getcwd()
path_to_index = abs_path + '/rendered_pages/index.html'

def render_markdown_to_html(article_dict, path_to_index):
	article = article_dict['source']
	article_dict['html_text'] = get_rendered_markdown_text_from_file('articles/'+article)
	open('rendered_pages/articles/'+article.split('.')[0]+'.html', 'w').close()
	template.stream(article=article_dict, index=path_to_index).dump('rendered_pages/articles/'+
											  article.split('.')[0]+'.html')

for x in json['articles']:
	render_markdown_to_html(x, path_to_index)

def make_topic_dict_with_articles_inside(json):
	articles_by_topic = {x['slug']: list() for x in json['topics']}
	for x in json['articles']:
		for y in articles_by_topic.keys():
			if y == x['topic']:
				x.update({'href': 'articles/'+x['source'].split('.')[0]+'.html'})
				articles_by_topic[y].append(x)
	return articles_by_topic


def render_index_to_html(json):
	abs_path = os.getcwd()
	articles_by_topic = make_topic_dict_with_articles_inside(json)
	static_template = env.get_template('index_template.html')
	static_template.stream(topics=json['topics'],articles=articles_by_topic, index=path_to_index).dump('rendered_pages/index.html')

render_index_to_html(json)
