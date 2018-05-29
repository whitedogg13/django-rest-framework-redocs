from setuptools import find_packages, setup

setup(
    name="django_rest_framework_redocs",
    version=__import__('redocs').__version__,
    author="Richie Hsieh",
    author_email="whitedogg13@gmail.com",
    packages=find_packages(),
    include_package_data=True,
    url="https://github.com/whitedogg13/django-rest-framework-redocs",
    license='MIT',
    description="Live API endpoints for django rest framework 1.x & 2.x",
    long_description=open("README.md").read(),
    install_requires=[
        'django>=1.8',
        'djangorestframework>=3'
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
    ],
)

