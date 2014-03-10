try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(name = "context",
            description="context implmentation",
            long_description = """Long description""",
            license="""BSD""",
            version = "0.1",
            author = "Sungmin Cho",
            author_email = "sm.cho@mac.com",
            maintainer = "Sungmin Cho",
            maintainer_email = "sm.cho@mac.com",
            url = "http://www.prosseek.com",
            packages = ['context'],
            classifiers = [
              'Programming Language :: Python :: 2',
              ]
            )
