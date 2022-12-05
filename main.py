#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Author       : BobAnkh
# @Github       : https://github.com/BobAnkh
# @Date         : 2020-07-29 00:12:39
# @LastEditors  : Vithano
# @LastEditTime : 2022-11-29 16:28:29
# @Maintainer   : https://github.com/vithano
# @FilePath     : /add-dev-stack/main.py
# @Description  : Main script of Github Action
# @Copyright 2020 BobAnkh

import argparse
import base64
import os
import re
import requests
import github
import yaml
head = '''<table>
<tr>'''
tail = '''
</tr>
</table>'''


def argument_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-m',
        '--mode',
        help=
        'choose to use local-dev mode or on github action mode. Valid values are \'local\' or \'github\'',
        default='github')
    parser.add_argument(
        '-f',
        '--file',
        help='configuration file to read from when running local-dev mode',
        default='.github/workflows/dev-stack.yml')
    parser.add_argument('-o',
                        '--output',
                        help='output file when running local-dev mode',
                        default='local-dev.md')
    parser.add_argument('-t', '--token', help='Github Access Token')
    args = parser.parse_args()
    return args

class GithubWrite:
    '''
    Class for data interface of Github

    Use it to get dev stack data and file content from Github and write new file content to Github
    '''
    def __init__(self, ACCESS_TOKEN, REPO_NAME, PATH, BRANCH, PULL_REQUEST, COMMIT_MESSAGE,PACKAGES_TO_SHOW,TYPES_TO_SHOW):
        '''
        Initial GithubWrite

        Args:
            ACCESS_TOKEN (str): Personal Access Token for Github
            REPO_NAME (str): The name of the repository
            PATH (str): The path to the file
            BRANCH (str): The branch of the file
            PULL_REQUEST (str): Pull request target branch, none means do not open a pull request
            COMMIT_MESSAGE (str): Commit message you want to use
        '''
        self.COMMIT_MESSAGE = COMMIT_MESSAGE
        self.PATH = PATH
        self.BRANCH = BRANCH
        self.PULL_REQUEST = PULL_REQUEST
        self.SHA = ''
        self.dev_stack_data = []
        self.file_content = ''
        self.PACKAGES_TO_SHOW = PACKAGES_TO_SHOW
        self.TYPES_TO_SHOW = TYPES_TO_SHOW
        # Use PyGithub to login to the repository
        # References: https://pygithub.readthedocs.io/en/latest/github_objects/Repository.html#github.Repository.Repository
        g = github.Github(ACCESS_TOKEN)
        self.repo = g.get_repo(REPO_NAME)

    def find_deps(self,packageJson):
        # find all dependencies and devDependencies in package.json file
        all_deps = []
        list_of_chars = ['<', '=', '>', '\-', '*', 'x', 'X', '~', '^', 'v', 'V', '@', "'",'"']
        pattern = '[' +  ''.join(list_of_chars) +  ']'
        # get packageManager version
        decoded_string = packageJson.decoded_content.decode('utf-8')
        package_manager = decoded_string.split('packageManager')[1].split(':')[1].split('"')[1]
        package_manager_version = package_manager.split('@')[1]
        package_manager_name = package_manager.split('@')[0]
        if self.PACKAGES_TO_SHOW == 'all' or package_manager_name in self.PACKAGES_TO_SHOW:
            obj = map_package_to_framework_type(package_manager_name)
            all_deps.append({
                'name': package_manager_name,
                'version': re.sub(pattern, '', package_manager_version),
                'type': obj.get('type',''),
                'dev': obj.get('dev',''),
                'logo': obj.get('logo','')
                
            })
        dependency_types = ['dependencies', 'devDependencies']
        # get all dependencies and devDependencies from package.json file
        for dependency_type in dependency_types:
            deps = decoded_string.split(f'"{dependency_type}": {{')
            if len(deps) == 1:
                deps = decoded_string.split(f'"{dependency_type}" : {{')
            if len(deps) == 1:
                deps = decoded_string.split(f'"{dependency_type}":{{')
            if len(deps) == 1:
                deps = decoded_string.split(f'"{dependency_type}" :{{')
            if len(deps) > 1:
                deps = deps[1].split('}')[0].split(',')
            for dep in deps:
                dep = dep.strip()
                if dep != '':
                    version = dep.split(':')[1].strip()
                    name = dep.split(':')[0].strip().replace('"', '').replace("'", '')
                    version = re.sub(pattern, '', version)
                    if(self.PACKAGES_TO_SHOW == 'all'):
                        obj = map_package_to_framework_type(name)
                        all_deps.append({
                            'name': name,
                            'version': version,
                            'type': obj.get('type',''),
                            'dev': obj.get('dev',''),
                            'logo': obj.get('logo','')
                        })
                    else:
                        if name in self.PACKAGES_TO_SHOW:
                            obj = map_package_to_framework_type(name)
                            all_deps.append({
                                'name': name,
                                'version': version,
                                'type': obj.get('type',''),
                                'dev': obj.get('dev',''),
                                'logo': obj.get('logo','')
                            })
        return all_deps
    def order_dev_stack_data(self,dev_stack_data):
        # order dev stack data by package name and PACKAGES_TO_SHOW
        ordered_dev_stack_data = dev_stack_data
        if self.PACKAGES_TO_SHOW != 'all':
            ordered_dev_stack_data = []
            for package in self.PACKAGES_TO_SHOW.split(','):
                for dev_stack in dev_stack_data:
                    if dev_stack.get('name','') == package.strip():
                        ordered_dev_stack_data.append(dev_stack)
        ordered_dev_stack_data_typed = ordered_dev_stack_data
        if self.TYPES_TO_SHOW != 'all':
            ordered_dev_stack_data_typed = []
            for type_to_show in self.TYPES_TO_SHOW.split(','):
                for dev_stack in ordered_dev_stack_data:
                    if dev_stack.get('type','') == type_to_show.strip():
                        ordered_dev_stack_data_typed.append(dev_stack)
        print(ordered_dev_stack_data_typed)
        return ordered_dev_stack_data_typed

    def get_data(self):
        # get dev stack data
        packageJson = self.repo.get_contents('package.json')
        print('[DEBUG]All dev stack\' names:')
        
        my_dev_stack = self.find_deps(packageJson)
        my_dev_stack = self.order_dev_stack_data(my_dev_stack)
        for package in my_dev_stack:
            name = package.get('name','')
            version = package.get('version')
            package_type = package.get('type', '')
            package_logo = package.get('logo', '')
            package_dev = package.get('dev', '')
            print(f'[DEBUG]{name}:{version}')
            if re.match('apps/', name):
                continue
            self.dev_stack_data.append({
                'name': name,
                'version': version,
                'type': package_type,
                'logo': package_logo,
                'dev': package_dev
            })
        # get file content
        contents = self.repo.get_contents(self.PATH, self.BRANCH)
        self.PATH = contents.path
        self.SHA = contents.sha
        base = contents.content
        base = base.replace('\n', '')
        self.file_content = base64.b64decode(base).decode('utf-8')

    def write_data(self, content):
        if content == self.file_content:
            pass
        else:
            self.repo.update_file(self.PATH, self.COMMIT_MESSAGE, content,
                                  self.SHA, self.BRANCH)
            print(f'[DEBUG] BRANCH: {self.BRANCH}, PULL_REQUEST: {self.PULL_REQUEST}')
            if self.PULL_REQUEST != '' and self.PULL_REQUEST != self.BRANCH:
                self.repo.create_pull(title=self.COMMIT_MESSAGE, body=self.COMMIT_MESSAGE, base=self.PULL_REQUEST, head=self.BRANCH, draft=False, maintainer_can_modify=True)

    def read_dev_stack(self):
        return self.dev_stack_data

    def read_file_content(self):
        return self.file_content


def set_local_env(env_name: str, env_value: str, prefix='INPUT'):
    '''
    set local env for dev

    Args:
        env_name (str): local env name.
        env_value (str): value of local env name.
        prefix (str, optional): prefix of env variable. Defaults to 'INPUT'.
    '''
    os.environ[prefix + '_{}'.format(env_name).upper()] = env_value


def get_inputs(input_name: str, prefix='INPUT') -> str:
    '''
    Get a Github actions input by name

    Args:
        input_name (str): input_name in workflow file.
        prefix (str, optional): prefix of input variable. Defaults to 'INPUT'.

    Returns:
        str: action_input

    References
    ----------
    [1] https://help.github.com/en/actions/automating-your-workflow-with-github-actions/metadata-syntax-for-github-actions#example
    '''
    return os.getenv(prefix + '_{}'.format(input_name).upper())

def map_package_to_framework_type(package_name):
    packages_map = {
        'pnpm': {
            'type': 'Package manager',
            'logo': 'https://avatars.githubusercontent.com/u/21320719?s=200&v=4',
            'dev': 'https://pnpm.io'
        },
        'npm': {
            'type': 'Package manager',
            'logo': 'https://avatars.githubusercontent.com/u/6078720?s=200&v=4',
            'dev': 'https://www.npmjs.com/'
        },
        'yarn': {
            'type': 'Package manager',
            'logo': 'https://avatars.githubusercontent.com/u/22247014?s=200&v=4',
            'dev': 'https://yarnpkg.com/'
        },
        'webpack': {
            'type': 'Bundler',
            'logo': 'https://avatars.githubusercontent.com/u/2105791?s=200&v=4',
            'dev': 'https://webpack.js.org/'
        },
        'babel': {
            'type': 'Bundler',
            'logo': 'https://avatars.githubusercontent.com/u/9637642?s=200&v=4',
            'dev': 'https://babeljs.io/'
        },
        'gulp': {
            'type': 'Bundler',
            'logo': 'https://avatars.githubusercontent.com/u/6200624?s=200&v=4',
            'dev': 'https://gulpjs.com/'
        },
        'grunt': {
            'type': 'Bundler',
            'logo': 'https://avatars.githubusercontent.com/u/1630826?s=200&v=4',
            'dev': 'https://gruntjs.com/'
        },
        'rollup': {
            'type': 'Bundler',
            'logo': 'https://avatars.githubusercontent.com/u/12554859?s=200&v=4',
            'dev': 'https://rollupjs.org/'
        },
        'parcel': {
            'type': 'Bundler',
            'logo': 'https://avatars.githubusercontent.com/u/32607881?s=200&v=4',
            'dev': 'https://parceljs.org/'
        },
        'jest': {
            'type': 'Test runner',
            'logo': 'https://cdn.freebiesupply.com/logos/large/2x/jest-logo-png-transparent.png',
            'dev': 'https://jestjs.io/'
        },
        'mocha': {
            'type': 'Test runner',
            'logo': 'https://avatars.githubusercontent.com/u/8770005?s=200&v=4',
            'dev': 'https://mochajs.org/'
        },
        'jasmine': {
            'type': 'Test runner',
            'logo': 'https://avatars.githubusercontent.com/u/4624349?s=200&v=4',
            'dev': 'https://jasmine.github.io/'
        },
        'karma': {
            'type': 'Test runner',
            'logo': 'https://avatars.githubusercontent.com/u/3284117?s=200&v=4',
            'dev': 'https://karma-runner.github.io/latest/index.html'
        },
        'nightwatch': {
            'type': 'Test runner',
            'logo': 'https://avatars.githubusercontent.com/u/12559275?s=200&v=4',
            'dev': 'https://nightwatchjs.org/'
        },
        'react': {
            'type': 'UI Library',
            'logo': 'https://upload.wikimedia.org/wikipedia/commons/thumb/a/a7/React-icon.svg/768px-React-icon.svg.png',
            'dev': 'https://reactjs.org/'
        },
        'vue': {
            'type': 'Frontend Framework',
            'logo': 'https://avatars.githubusercontent.com/u/6128107?s=200&v=4',
            'dev': 'https://vuejs.org/'
        },
        '@angular/core': {
            'type': 'Frontend Framework',
            'logo': 'https://avatars.githubusercontent.com/u/139426?s=200&v=4',
            'dev': 'https://angular.io/'
        },
        'emberjs': {
            'type': 'Frontend Framework',
            'logo': 'https://avatars.githubusercontent.com/u/1253363?s=200&v=4',
            'dev': 'https://emberjs.com/'
        },
        'svelte': {
            'type': 'Frontend Framework',
            'logo': 'https://avatars.githubusercontent.com/u/23617963?s=200&v=4',
            'dev': 'https://svelte.dev/'
        },
        'lit-element': {
            'type': 'UI Library',
            'logo': 'https://avatars.githubusercontent.com/u/18489846?s=200&v=4',
            'dev': 'https://lit-element.polymer-project.org/'
        },
        'lit-html': {
            'type': 'UI Library',
            'logo': 'https://avatars.githubusercontent.com/u/18489846?s=200&v=4',
            'dev': 'https://lit-html.polymer-project.org/'
        },
        'preact': {
            'type': 'UI Library',
            'logo': 'https://avatars.githubusercontent.com/u/26872990?s=200&v=4',
            'dev': 'https://preactjs.com/'
        },
        'riot': {
            'type': 'UI Library',
            'logo': 'https://avatars.githubusercontent.com/u/12729373?s=200&v=4',
            'dev': 'https://riot.js.org/'
        },
        'marko': {
            'type': 'Frontend Language',
            'logo': 'https://avatars.githubusercontent.com/u/11873696?s=200&v=4',
            'dev': 'https://markojs.com/'
        },
        'hyperapp': {
            'type': 'Frontend Framework',
            'logo': 'https://miro.medium.com/max/828/1*o1Lyd3SKXAn6y3hHKB7jCg.webp',
            'dev': 'https://hyperapp.dev/'
        },
        'mithril': {
            'type': 'Frontend Framework',
            'logo': 'https://avatars.githubusercontent.com/u/19475707?s=200&v=4',
            'dev': 'https://mithril.js.org/'
        },
        '@polymer/polymer': {
            'type': 'UI Library',
            'logo': 'https://avatars.githubusercontent.com/u/2159051?s=200&v=4',
            'dev': 'https://www.polymer-project.org/'
        },
        '@apollo/client': {
            'type': 'GraphQL',
            'logo': 'https://avatars.githubusercontent.com/u/17189275?s=200&v=4',
            'dev': 'https://www.apollographql.com/docs/react/'
        },
        'graphql': {
            'type': 'GraphQL',
            'logo': 'https://avatars.githubusercontent.com/u/12972006?s=200&v=4',
            'dev': 'https://graphql.org/'
        },
        'relay-runtime': {
            'type': 'GraphQL',
            'logo': 'https://relay.dev/img/relay.svg',
            'dev': 'https://relay.dev/'
        },
        'turbo': {
            'type': 'Monorepo manager',
            'logo': 'https://user-images.githubusercontent.com/4060187/196936104-5797972c-ab10-4834-bd61-0d1e5f442c9c.png',
            'dev': 'https://turborepo.org/docs'
        },
        'lerna': {
            'type': 'Monorepo manager',
            'logo': 'https://avatars.githubusercontent.com/u/19333396?s=200&v=4',
            'dev': 'https://lerna.js.org/'
        },
        'nx': {
            'type': 'Monorepo manager',
            'logo': 'https://avatars.githubusercontent.com/u/23692104?s=200&v=4',
            'dev': 'https://nx.dev/'
        },
        '@microsoft/rush': {
            'type': 'Monorepo manager',
            'logo': 'https://github.com/microsoft/rushstack/raw/main/common/wiki-images/rush-logo.png?raw=true',
            'dev': 'https://rushjs.io/pages/intro/welcome/'
        },
        'tailwindcss': {
            'type': 'CSS Framework',
            'logo': 'https://avatars.githubusercontent.com/u/67109815?s=200&v=4',
            'dev':'https://tailwindcss.com/docs/installation'
        },
        'bootstrap': {
            'type': 'CSS Framework',
            'logo': 'https://avatars.githubusercontent.com/u/2918581?s=200&v=4',
            'dev': 'https://getbootstrap.com/docs/5.0/getting-started/introduction/'
        },
        'bulma': {
            'type': 'CSS Framework',
            'logo': 'https://raw.githubusercontent.com/github/explore/ad9cd7e959a88047c830c3a9cc4e9ffcf5e644f7/topics/bulma/bulma.png',
            'dev': 'https://bulma.io/documentation/'
        },
        '@mui/material': {
            'type': 'UI Library',
            'logo': 'https://avatars.githubusercontent.com/u/33663932?s=200&v=4',
            'dev': 'https://mui.com/getting-started/usage/'
        },
        'antd': {
            'type': 'UI Library',
            'logo': 'https://avatars.githubusercontent.com/u/12101536?s=200&v=4',
            'dev': 'https://ant.design/docs/react/introduce'
        },
        'element-ui': {
            'type': 'UI Library',
            'logo': 'https://avatars.githubusercontent.com/u/12810740?s=200&v=4',
            'dev': 'https://element.eleme.io/#/en-US'
        },
        'vuetify': {
            'type': 'CSS Framework',
            'logo': 'https://avatars.githubusercontent.com/u/22138497?s=200&v=4',
            'dev': 'https://vuetifyjs.com/en/getting-started/installation/'
        },
        '@trpc/server': {
            'type': 'Server-client communication',
            'logo': 'https://avatars.githubusercontent.com/u/78011399?s=200&v=4',
            'dev': 'https://trpc.io/docs'
        },
        'next': {
            'type': 'Frontend Framework',
            'logo': 'https://camo.githubusercontent.com/f21f1fa29dfe5e1d0772b0efe2f43eca2f6dc14f2fede8d9cbef4a3a8210c91d/68747470733a2f2f6173736574732e76657263656c2e636f6d2f696d6167652f75706c6f61642f76313636323133303535392f6e6578746a732f49636f6e5f6c696768745f6261636b67726f756e642e706e67',
            'dev': 'https://nextjs.org/docs/getting-started'
        },
        'express': {
            'type': 'Backend Framework',
            'logo': 'https://avatars.githubusercontent.com/u/5658226?s=200&v=4',
            'dev': 'https://expressjs.com/'
        },
        'koa': {
            'type': 'Backend Framework',
            'logo': 'https://avatars.githubusercontent.com/u/5055057?s=200&v=4',
            'dev': 'https://koajs.com/'
        },
        'hapi': {
            'type': 'Backend Framework',
            'logo': 'https://avatars.githubusercontent.com/u/3774533?s=200&v=4',
            'dev': 'https://hapi.dev/'
        },
        'fastify': {
            'type': 'Backend Framework',
            'logo': 'https://avatars.githubusercontent.com/u/24939410?s=200&v=4',
            'dev': 'https://www.fastify.io/'
        },
        '@nestjs/core': {
            'type': 'Backend Framework',
            'logo': 'https://avatars.githubusercontent.com/u/28507035?s=200&v=4',
            'dev': 'https://docs.nestjs.com/'
        },
        'sapper': {
            'type': 'Frontend Framework',
            'logo': 'https://avatars.githubusercontent.com/u/23617963?s=200&v=4',
            'dev': 'https://sapper.svelte.dev/docs'
        },
        '@sveltejs/kit': {
            'type': 'Frontend Framework',
            'logo': 'https://avatars.githubusercontent.com/u/23617963?s=200&v=4',
            'dev': 'https://kit.svelte.dev/docs'
        },
        'strapi': {
            'type': 'Backend Framework',
            'logo': 'https://avatars.githubusercontent.com/u/19872173?s=200&v=4',
            'dev': 'https://strapi.io/documentation/developer-docs/latest/getting-started/introduction.html'
        },
        'nuxt': {
            'type': 'Frontend Framework',
            'logo': 'https://avatars.githubusercontent.com/u/23360933?s=200&v=4',
            'dev': 'https://nuxtjs.org/docs/2.x/get-started/installation'
        },
        'gatsby': {
            'type': 'Frontend Framework',
            'logo': 'https://avatars.githubusercontent.com/u/12551863?s=200&v=4',
            'dev': 'https://www.gatsbyjs.com/docs/'
        },
        'react-native': {
            'type': 'Mobile Framework',
            'logo': 'https://upload.wikimedia.org/wikipedia/commons/thumb/a/a7/React-icon.svg/768px-React-icon.svg.png',
            'dev': 'https://reactnative.dev/docs/getting-started'
        },
        'ionic': {
            'type': 'Mobile Framework',
            'logo': 'https://avatars.githubusercontent.com/u/3171503?s=200&v=4',
            'dev': 'https://ionicframework.com/docs'
        },
        '@ionic/cli': {
            'type': 'Mobile Framework',
            'logo': 'https://avatars.githubusercontent.com/u/3171503?s=200&v=4',
            'dev': 'https://ionicframework.com/docs/cli'
        },
        'cordova': {
            'type': 'Mobile Framework',
            'logo': 'https://avatars.githubusercontent.com/u/47359?s=200&v=4',
            'dev': 'https://cordova.apache.org/docs/en/latest/'
        },
        'expo': {
            'type': 'Mobile Framework',
            'logo': 'https://avatars.githubusercontent.com/u/12504344?s=200&v=4',
            'dev': 'https://docs.expo.io/'
        },
        'nativescript': {
            'type': 'Mobile Framework',
            'logo': 'https://avatars.githubusercontent.com/u/7392261?s=200&v=4',
            'dev': 'https://docs.nativescript.org/'
        },
        'react-native-web': {
            'type': 'Mobile Framework',
            'logo': 'https://upload.wikimedia.org/wikipedia/commons/thumb/a/a7/React-icon.svg/768px-React-icon.svg.png',
            'dev': 'https://necolas.github.io/react-native-web/docs/'
        },
        'prisma': {
            'type': 'ORM',
            'logo': 'https://avatars.githubusercontent.com/u/17219288?s=200&v=4',
            'dev': 'https://prisma.io/',
        },
        'typeorm': {
            'type': 'ORM',
            'logo': 'https://avatars.githubusercontent.com/u/20165699?s=200&v=4',
            'dev': 'https://typeorm.io/'
        },
        'sequelize': {
            'type': 'ORM',
            'logo': 'https://avatars.githubusercontent.com/u/3591786?s=200&v=4',
            'dev': 'https://sequelize.org/'
        },
        'mongoose': {
            'type': 'ORM',
            'logo': 'https://raw.githubusercontent.com/github/explore/80688e429a7d4ef2fca1e82350fe8e3517d3494d/topics/mongoose/mongoose.png',
            'dev': 'https://mongoosejs.com/'
        },
        'vitest': {
            'type': 'Test runner',
            'logo': 'https://avatars.githubusercontent.com/u/95747107?s=200&v=4',
            'dev': 'https://vitest.dev/'
        },
        'jest-circus': {
            'type': 'Test runner',
            'logo': 'https://camo.githubusercontent.com/4ce8c09d94ba2fd16f82fbc8783b3c2738e07b670b1acdd2f6f6ce86ace36297/68747470733a2f2f6a6573746a732e696f2f696d672f6369726375732e706e67',
            'dev': 'https://jestjs.io/docs/en/configuration#testrunner-string'
        },
        'jest-jasmine2': {
            'type': 'Test runner',
            'logo': 'https://cdn.freebiesupply.com/logos/large/2x/jest-logo-png-transparent.png',
            'dev': 'https://jestjs.io/docs/en/configuration#testrunner-string'
        },
        'jest-mocha': {
            'type': 'Test runner',
            'logo': 'https://cdn.freebiesupply.com/logos/large/2x/jest-logo-png-transparent.png',
            'dev': 'https://jestjs.io/docs/en/configuration#testrunner-string'
        },
        'protractor': {
            'type': 'Test runner',
            'logo': 'https://res.cloudinary.com/practicaldev/image/fetch/s--2j6Ao4pq--/c_imagga_scale,f_auto,fl_progressive,h_420,q_auto,w_1000/https://thepracticaldev.s3.amazonaws.com/i/9tp05j5fpbghqa3f9whz.png',
            'dev': 'https://www.protractortest.org/#/'
        },
        'cypress': {
            'type': 'Test runner',
            'logo': 'https://avatars.githubusercontent.com/u/8908513?s=200&v=4',
            'dev': 'https://docs.cypress.io/guides/overview/why-cypress'
        },
        'ava': {
            'type': 'Test runner',
            'logo': 'https://avatars.githubusercontent.com/u/8527916?s=200&v=4',
            'dev': 'https://github.com/avajs/ava'
        },
        '@testing-library/react': {
            'type': 'Testing components',
            'logo': 'https://avatars.githubusercontent.com/u/49996085?s=200&v=4',
            'dev': 'https://testing-library.com/docs/react-testing-library/intro/'
        },
        'enzyme': {
            'type': 'Testing components',
            'logo': 'https://avatars.githubusercontent.com/u/698437?s=200&v=4',
            'dev': 'https://enzymejs.github.io/enzyme/'
        },
        'storybook': {
            'type': 'Component library',
            'logo': 'https://avatars.githubusercontent.com/u/22632046?s=200&v=4',
            'dev': 'https://storybook.js.org/docs/react/get-started/introduction'
        },
        'react-styleguidist': {
            'type': 'Component library',
            'logo': 'https://avatars.githubusercontent.com/u/23550189?s=200&v=4',
            'dev': 'https://react-styleguidist.js.org/'
        },
        'docz': {
            'type': 'Documentation',
            'logo': 'https://avatars.githubusercontent.com/u/39714731?s=200&v=4',
            'dev': 'https://www.docz.site/'
        },
        '@teambit/bit': {
            'type': 'Component library',
            'logo': 'https://avatars.githubusercontent.com/u/24789812?s=200&v=4',
            'dev': 'https://bit.dev/'
        },
        'msw': {
            'type': 'Mocking',
            'logo': 'https://avatars.githubusercontent.com/u/64637271?s=200&v=4',
            'dev': 'https://mswjs.io/docs/'
        },
        'nock': {
            'type': 'Mocking',
            'logo': 'https://avatars.githubusercontent.com/u/17545810?s=200&v=4',
            'dev': 'https://github.com/nock/nock#readme'
        },
        'sinon': {
            'type': 'Mocking',
            'logo': 'https://avatars.githubusercontent.com/u/6570253?s=200&v=4',
            'dev': 'https://sinonjs.org/'
        },
        'eslint': {
            'type': 'Lint',
            'logo': 'https://avatars.githubusercontent.com/u/6019716?s=200&v=4',
            'dev': 'https://eslint.org/docs/user-guide/getting-started'
        },
        'prettier': {
            'type': 'Lint',
            'logo': 'https://avatars.githubusercontent.com/u/25822731?s=200&v=4',
            'dev': 'https://prettier.io/docs/en/index.html'
        },
        'stylelint': {
            'type': 'Lint',
            'logo': 'https://avatars.githubusercontent.com/u/10076935?s=200&v=4',
            'dev': 'https://stylelint.io/user-guide/get-started'
        },
        'tslint': {
            'type': 'Lint',
            'logo': '',
            'dev': 'https://palantir.github.io/tslint/'
        },
        'husky': {
            'type': 'Lint',
            'logo': 'https://res.cloudinary.com/practicaldev/image/fetch/s--3HkALzIp--/c_imagga_scale,f_auto,fl_progressive,h_420,q_auto,w_1000/https://dev-to-uploads.s3.amazonaws.com/uploads/articles/v67mrvpgrqg19k3ifgll.png',
            'dev': 'https://typicode.github.io/husky/'
        },
        'lint-staged': {
            'type': 'Lint',
            'logo': '',
            'dev': 'https://github.com/okonet/lint-staged'
        },
        '@ladle/react': {
            'type': 'Testing Components',
            'logo': 'https://raw.githubusercontent.com/tajo/ladle/main/packages/website/static/img/logo-gray.svg',
            'dev': 'https://github.com/tajo/ladle#readme'
        }
    }
    return packages_map.get(package_name, {})

def generate_dev_stack_table(dev_stack_data, img_width,
                                font_size, head_format, tail_format, shape, columns):
    '''
    Generate the dev stack table in html format using a given template

    Args:
        dev_stack_data (list): a list of dict which contains the dev stack' name, version and type

        img_width (int): width of img
        font_size (int): font size of name
        head_format (str): html_format for table head
        tail_format (str): html_format for table tail
        shape (str): round for round avatar and square for square avatar

    Returns:
        str: dev stack table in html format
    '''
    HEAD = head_format
    if columns == '':
        columns = ['Type','Package','Version']
    else:
        columns = columns.split(',')
    HEAD = f'''<table>
<tr>
    <th style="text-align:center;">{columns[0]}</th>
    <th style="text-align:center;">{columns[1]}</th>
    <th style="text-align:center;">{columns[2]}</th>
'''
    TAIL = tail_format
    cell_width = str(1.5 * img_width) + 'px'
    cell_height = str(1.5 * img_width) + 'px'
    for package in dev_stack_data:
        name = package.get('name','')
        version = package.get('version','')
        package_type = package.get('type', '')
        package_logo = package.get('logo', '')
        package_dev = package.get('dev', '')
        if package_type == '':
            continue
        # fetch latest version from unpkg
        try:
            response = requests.get(f'https://unpkg.com/{name}/package.json')
            response.raise_for_status()
            print(f'Fetching latest version of {name} from unpkg')
            
            if response.status_code != 204:
                json = response.json()
                latest_version = json.get('version','')
            else:
                latest_version = version
            if version == 'latest':
                version = latest_version
            major_version = version.split('.')[0]
            latest_major_version = latest_version.split('.')[0]
            if int(latest_major_version) == int(major_version):
                version = f'https://img.shields.io/badge/{version}-brightgreen'
            elif int(latest_major_version) - int(major_version) == 1:
                version = f'https://img.shields.io/badge/{version}-yellow'
            elif int(latest_major_version) - int(major_version) > 1:
                version = f'https://img.shields.io/badge/{version}-red'
            else:
                version = f'https://img.shields.io/badge/{version}-brightgreen'

        except:
            version = f'https://img.shields.io/badge/{version}-brightgreen'
        new_tr = '''\n</tr>\n<tr style="padding-top:10px;">'''
        HEAD = HEAD + new_tr
        if shape == 'round':
            img_style = f'border-radius:50%;align-items:center;justify-content:center;overflow:hidden;'
        else:
            img_style = ''
        logo = name.capitalize()
        font_style = f'''style="display: inline-flex;align-items: center;padding-top:10px;
    flex-direction: column; font-size:{str(font_size) + 'px'}"'''
        package_dev_ref = ''
        if package_logo != '':
            logo = f'''<img style="border-radius:6px;width:{img_width}px;height:{img_width}px; {img_style}" src="{package_logo}" alt="{name}"/>
                {name}'''
        cell_style = f'''text-align:center;white-space: nowrap; width: {cell_width}; height: {cell_height}'''
        if package_dev != '':
            package_dev_ref = f'href="{package_dev}"'
        td = f'''
    <td style="{cell_style}">
        {package_type}
    </td>
    <td style="{cell_style}">
        <a {font_style} aria-label="{name}" {package_dev_ref}>
            {logo}
        </a>
    </td>
    <td style="{cell_style}">
        <a aria-label="NPM Version" href="https://www.npmjs.com/package/{name}">
            <img src="{version}" alt="{name}"/>
        </a>
    </td>

    '''
        HEAD = HEAD + td
        
    HEAD = HEAD + TAIL
    return HEAD


def generate_content(file_content, dev_stack_table, DEV_STACK, PATH):
    '''
    Generate the whole content with dev stack table

    Args:
        file_content (str): content of target file
        dev_stack_table (str): dev stack list
        DEV_STACK (str): where you want to write the dev stack table
        PATH (str): the file to write

    Raises:
        Exception: the target file does not have the DEV_STACK section

    Returns:
        str: the whole content with dev stack table
    '''
    text = file_content
    text_str = text.split(DEV_STACK)
    if len(text_str) == 1:
        print('[DEBUG]: ', text, '\n[DEBUG]')
        raise Exception("File '" + PATH + "' does not have '" + DEV_STACK +
                        "' section")
    if re.match(r'\n+', text_str[1]):
        lf_num = re.match(r'\n+', text_str[1]).span()[1]
        text_str[1] = text_str[1][lf_num:]
    else:
        lf_num = 0
        print('[DEBUG-lr_num]: ', text_str[1])
    if re.match(head, text_str[1]):
        end = text_str[1].split(tail)
        end[0] = end[0] + tail
    else:
        end = ['', '\n' * (lf_num + 1) + text_str[1]]
    end[0] = dev_stack_table
    text = text_str[0] + DEV_STACK + '\n' + end[0] + end[1]
    return text


def set_env_from_file(file, args, prefix='INPUT'):
    '''
    Set env when use local-dev mode

    Args:
        file (str): path to config file
        args (object): cmdline argument
        prefix (str, optional): prefix of env. Defaults to 'INPUT'.
    '''
    f = open(file, encoding='utf-8')
    y = yaml.safe_load(f)
    for job in y['jobs'].values():
        for step in job['steps']:
            if re.match(r'vithano/add-dev-stack', step['uses']):
                params = step['with']
                break
    option_params = [
        'REPO_NAME', 'DEV_STACK', 'ACCESS_TOKEN',
        'IMG_WIDTH', 'FONT_SIZE', 'PATH', 'COMMIT_MESSAGE', 'AVATAR_SHAPE','PACKAGES_TO_SHOW','TYPES_TO_SHOW','PATH','BRANCH','COLUMNS'
    ]
    for param in option_params:
        if param not in params.keys():
            if param == 'ACCESS_TOKEN' and args.token:
                tmp = args.token
            else:
                tmp = input('Please input the value of ' + param + ':')
        elif param == 'ACCESS_TOKEN':
            if re.match(r'\$\{\{secrets\.', params[param]):
                if args.token:
                    tmp = args.token
                else:
                    tmp = input('Please input the value of ' + param + ':')
            else:
                tmp = params[param]
        elif param == 'REPO_NAME' and params[param] == '':
            tmp = input('Please input the value of ' + param + ':')
        else:
            tmp = params[param]
        set_local_env(param, tmp, prefix)


def main():
    args = argument_parser()
    if args.mode == 'local':
        set_env_from_file(args.file, args)
    elif args.mode == 'github':
        pass
    else:
        print("Illegal mode option, please type \'-h\' to read the help")
        os.exit()
    ACCESS_TOKEN = get_inputs('ACCESS_TOKEN')
    REPO_NAME = get_inputs('REPO_NAME')
    if REPO_NAME == '':
        REPO_NAME = get_inputs('REPOSITORY', 'GITHUB')
    DEV_STACK = get_inputs('DEV_STACK') + '\n'
    IMG_WIDTH = int(get_inputs('IMG_WIDTH'))
    FONT_SIZE = int(get_inputs('FONT_SIZE'))
    COLUMNS = get_inputs('COLUMNS')
    PACKAGES_TO_SHOW = get_inputs('PACKAGES_TO_SHOW')
    TYPES_TO_SHOW = get_inputs('TYPES_TO_SHOW')
    PATH = get_inputs('PATH')
    BRANCH = get_inputs('BRANCH')
    if BRANCH == '':
        BRANCH = github.GithubObject.NotSet
    PULL_REQUEST = get_inputs('PULL_REQUEST')
    COMMIT_MESSAGE = get_inputs('COMMIT_MESSAGE')
    AVATAR_SHAPE = get_inputs('AVATAR_SHAPE')
    GithubWriteData = GithubWrite(ACCESS_TOKEN, REPO_NAME, PATH, BRANCH, PULL_REQUEST,
                                      COMMIT_MESSAGE,PACKAGES_TO_SHOW,TYPES_TO_SHOW)
    GithubWriteData.get_data()
    dev_stack_table = generate_dev_stack_table(
        GithubWriteData.read_dev_stack(), IMG_WIDTH, FONT_SIZE,
        head, tail, AVATAR_SHAPE,COLUMNS)
    content = generate_content(GithubWriteData.read_file_content(),
                               dev_stack_table, DEV_STACK, PATH)
    if args.mode == 'local':
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(content)
    else:
        GithubWriteData.write_data(content)


if __name__ == '__main__':
    main()
