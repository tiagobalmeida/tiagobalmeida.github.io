#!/usr/bin/python
from jinja2 import Environment, FileSystemLoader
import markdown
import os


class JinjaGenerator():
	def __init__(self):
		self.PATH = os.path.dirname(os.path.abspath(__file__))
		self.TEMPLATE_ENVIRONMENT = Environment(
			autoescape=False,
		loader=FileSystemLoader(
			os.path.join(self.PATH, '')),
			trim_blocks=True,
			lstrip_blocks=True)
	#
	def render(self, template_filename, context):
		return (self.TEMPLATE_ENVIRONMENT
							.get_template(template_filename)
							.render(context))

def _render_post(md_path):
	post_html = ''
	md = markdown.Markdown(
		extensions=['markdown.extensions.fenced_code', 
					'markdown.extensions.codehilite'])
	with open(md_path, 'r') as f:
		post_html = md.convert(f.read())
	context = {
		'content': post_html
	}
	generator = JinjaGenerator()
	return generator.render('post_template.html', context)


def _title(md_path):
	"""
	Given the path to a markdown file, returns the title for the 
	post. This is built by the sluggified file name
	"""
	from slugify import slugify
	file_name = os.path.splitext(os.path.basename(md_path))[0]
	return os.path.join('posts', slugify(file_name) + '.html')


def write_post(name, content):
	with open(name, 'w') as f:
		f.write(content)
	f.close()


if __name__ == "__main__":
	from sys import argv
	if len(argv) == 2:
		write_post(_title(argv[1]), _render_post(argv[1]))
	else:
		pass #todo
