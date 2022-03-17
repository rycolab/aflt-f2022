from setuptools import setup


install_requires = [
	"numpy",
	"frozendict",
	"frozenlist",
	"pyconll",
	"nltk"
]


setup(
	name="rayuela",
	install_requires=install_requires,
	version="0.1",
	scripts=[]
)