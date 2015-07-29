from setuptools import setup
import py2exe

setup(
	name='NaOH',
	description='PocketMine-MP 서버 구동기',
	version='0.1b',
	windows=[{'script': 'main.py', 'icon_resources': [(1, 'icon.ico')]}],
	data_files=[('', [r'icon.ico'])],
	options={
		'py2exe': {
			'bundle_files': 2,
			'includes': [
				'tkinter',
				'os',
				'json',
				'threading',
				'sys',
				'signal',
				'time'
			]
		}
	},
	zipfile=None
)
