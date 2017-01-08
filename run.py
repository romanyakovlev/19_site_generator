from jinja2 import Environment, FileSystemLoader
import markdown
import json
import os


def make_environment(root_folder_path):
  loader = FileSystemLoader(root_folder_path)
  template_environment = Environment(loader=loader)
  return template_environment


def render_static_to_html(template_environment, root_folder_path):
  path_to_static = os.path.join('rendered_pages', 'static.html')
  relative_path_static = os.path.join('templates','static_template.html')
  static_template = template_environment.get_template(relative_path_static)
  static_template.stream(path_to_dir='/19_site_generator').dump(path_to_static)


def get_json_config():
  with open('config.json') as json_data:
    json_dict = json.load(json_data)
  return json_dict


def get_rendered_markdown_text_from_file(path_to_file):
  markdown_text = open(path_to_file).read()
  rendered_text = markdown.Markdown().convert(markdown_text)
  return rendered_text


def create_folder_for_topic_if_it_does_not(file_name_with_html_format):
  only_folders_path = os.path.split(file_name_with_html_format)[0]
  if not os.path.exists(only_folders_path):
    os.makedirs(only_folders_path)


def create_full_file_path(article_path, root_folder_path):
  file_name_without_md_format = os.path.splitext(article_path)[0]
  file_name_with_html_format = '.'.join([file_name_without_md_format, 'html'])
  full_path = os.path.join(root_folder_path, 'rendered_pages',
                           'articles', file_name_with_html_format)
  return full_path

def create_relative_file_path(article_path):
  file_name_without_md_format = os.path.splitext(article_path)[0]
  file_name_with_html_format = '.'.join([file_name_without_md_format, 'html'])
  relative_path = os.path.join('19_site_generator', 'rendered_pages',
                                                     'articles', file_name_with_html_format)
  return relative_path


def create_file(file_path):
  open(file_path, 'w').close()


def render_markdown_to_html(template_environment, article_dict,
                            path_to_index, root_folder_path):
  relative_path_markdown = os.path.join('templates','md_template.html')
  markdown_template = template_environment.get_template(relative_path_markdown)
  article_path = article_dict['source']
  path_to_markdown = os.path.join('articles', article_path)
  article_dict['html_text'] = get_rendered_markdown_text_from_file(path_to_markdown)
  full_file_path = create_full_file_path(article_path, root_folder_path)
  create_folder_for_topic_if_it_does_not(full_file_path)
  create_file(full_file_path)
  markdown_template.stream(article=article_dict,
                           index_link='/19_site_generator/rendered_pages/index.html').dump(full_file_path)


def render_all_markdowns_to_html(template_environment, json_dict, root_folder_path, path_to_index):
  for article_dict in json_dict['articles']:
    render_markdown_to_html(template_environment, article_dict,
                            path_to_index, root_folder_path)


def make_topic_dict_with_articles_inside(json_dict, root_folder_path):
  articles_by_topic = {x['slug']: list() for x in json_dict['topics']}
  for article in json_dict['articles']:
    for article_key in articles_by_topic.keys():
      if article_key == article['topic']:
        article.update({'href': os.sep+create_relative_file_path(article['source'])})
        articles_by_topic[article_key].append(article)
  return articles_by_topic


def render_index_to_html(template_environment, json_dict, root_folder_path, path_to_index):
  articles_by_topic = make_topic_dict_with_articles_inside(json_dict, root_folder_path)
  relative_path_index = os.path.join('templates', 'index_template.html')
  static_template = template_environment.get_template(relative_path_index)
  static_template.stream(topics=json_dict['topics'], articles=articles_by_topic,
                         index_link=path_to_index).dump(path_to_index)


def make_all_data():
  root_folder_path = os.getcwd()
  template_environment = make_environment(root_folder_path)
  json_dict = get_json_config()
  path_to_index = os.path.join('', 'rendered_pages', 'index.html')
  return root_folder_path, template_environment, json_dict, path_to_index


def render_templates(template_environment, json_dict, root_folder_path, path_to_index):
  render_static_to_html(template_environment, root_folder_path)
  render_all_markdowns_to_html(template_environment, json_dict, root_folder_path, path_to_index)
  render_index_to_html(template_environment, json_dict, root_folder_path, path_to_index)


if __name__ == '__main__':
  root_folder_path, template_environment, json_dict, path_to_index = make_all_data()
  render_templates(template_environment, json_dict, root_folder_path, path_to_index)
