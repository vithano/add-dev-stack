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
            all_deps.append({
                'name': package_manager_name,
                'version': re.sub(pattern, '', package_manager_version)
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
                        all_deps.append({
                            'name': name,
                            'version': version
                        })
                    else:
                        if name in self.PACKAGES_TO_SHOW:
                            all_deps.append({
                                'name': name,
                                'version': version
                            })
        return all_deps
    def order_dev_stack_data(self,dev_stack_data):
        # order dev stack data by package name and PACKAGES_TO_SHOW
        ordered_dev_stack_data = dev_stack_data
        if self.PACKAGES_TO_SHOW != 'all':
            ordered_dev_stack_data = []
            for package in self.PACKAGES_TO_SHOW.split(',').strip():
                for dev_stack in dev_stack_data:
                    if dev_stack.get('name','') == package:
                        ordered_dev_stack_data.append(dev_stack)
        ordered_dev_stack_data_typed = ordered_dev_stack_data
        if self.TYPES_TO_SHOW != 'all':
            ordered_dev_stack_data_typed = []
            for type_to_show in self.TYPES_TO_SHOW.split(',').strip():
                for dev_stack in ordered_dev_stack_data:
                    if dev_stack.get('type','') == type_to_show:
                        ordered_dev_stack_data_typed.append(dev_stack)
        return ordered_dev_stack_data_typed

    def get_data(self):
        # get dev stack data
        packageJson = self.repo.get_contents('package.json')
        print('[DEBUG]All dev stack\' names:')
        
        my_dev_stack = self.find_deps(packageJson)
        my_dev_stack = self.order_dev_stack_data(my_dev_stack)
        for package in my_dev_stack:
            name = package["name"]
            version = package["version"]
            print(f'[DEBUG]{name}:{version}')
            if re.match('apps/', name):
                continue
            self.dev_stack_data.append({
                'name': name,
                'version': version,
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
            'logo': 'https://user-images.githubusercontent.com/4253088/196271039-0b998d0d-5867-47bf-a627-e36825175aeb.png',
            'dev': 'https://pnpm.io'
        },
        'npm': {
            'type': 'Package manager',
            'logo': ''
        },
        'yarn': {
            'type': 'Package manager',
            'logo': ''
        },
        'webpack': {
            'type': 'Bundler',
            'logo': ''
        },
        'babel': {
            'type': 'Bundler',
            'logo': ''
        },
        'gulp': {
            'type': 'Bundler',
            'logo': ''
        },
        'grunt': {
            'type': 'Bundler',
            'logo': ''
        },
        'rollup': {
            'type': 'Bundler',
            'logo': ''
        },
        'parcel': {
            'type': 'Bundler',
            'logo': ''
        },
        'jest': {
            'type': 'Test runner',
            'logo': ''
        },
        'mocha': {
            'type': 'Test runner',
            'logo': ''
        },
        'jasmine': {
            'type': 'Test runner',
            'logo': ''
        },
        'karma': {
            'type': 'Test runner',
            'logo': ''
        },
        'nightwatch': {
            'type': 'Test runner',
            'logo': ''
        },
        'react': {
            'type': 'Frontend Framework',
            'logo': ''
        },
        'vue': {
            'type': 'Frontend Framework',
            'logo': ''
        },
        'angular': {
            'type': 'Frontend Framework',
            'logo': ''
        },
        'ember': {
            'type': 'Frontend Framework',
            'logo': ''
        },
        'svelte': {
            'type': 'Frontend Framework',
            'logo': ''
        },
        'lit-element': {
            'type': 'Frontend Framework',
            'logo': ''
        },
        'lit-html': {
            'type': 'Frontend Framework',
            'logo': ''
        },
        'preact': {
            'type': 'Frontend Framework',
            'logo': ''
        },
        'riot': {
            'type': 'Frontend Framework',
            'logo': ''
        },
        'marko': {
            'type': 'Frontend Framework',
            'logo': ''
        },
        'hyperapp': {
            'type': 'Frontend Framework',
            'logo': ''
        },
        'mithril': {
            'type': 'Frontend Framework',
            'logo': ''
        },
        'polymer': {
            'type': 'Frontend Framework',
            'logo': ''
        },
        'apollo': {
            'type': 'GraphQL',
            'logo': ''
        },
        'graphql': {
            'type': 'GraphQL',
            'logo': ''
        },
        'relay': {
            'type': 'GraphQL',
            'logo': ''
        },
        'turbo': {
            'type': 'Monorepo manager',
            'logo': 'https://user-images.githubusercontent.com/4253088/196269627-8da367d0-5e1a-40a6-b261-d0f4e00498c1.png',
            'dev': 'https://turborepo.org/docs'
        },
        'lerna': {
            'type': 'Monorepo manager',
            'logo': ''
        },
        'nx': {
            'type': 'Monorepo manager',
            'logo': ''
        },
        'rush': {
            'type': 'Monorepo manager',
            'logo': ''
        },
        'pnpm-workspace': {
            'type': 'Monorepo manager',
            'logo': ''
        },
        'tailwindcss': {
            'type': 'CSS Framework',
            'logo': 'https://user-images.githubusercontent.com/4253088/196271439-de4d436c-fb47-4a7e-84a6-fcc01d86026b.png',
            'dev':'https://tailwindcss.com/docs/installation'
        },
        'bootstrap': {
            'type': 'CSS Framework',
            'logo': ''
        },
        'bulma': {
            'type': 'CSS Framework',
            'logo': ''
        },
        'material-ui': {
            'type': 'CSS Framework',
            'logo': ''
        },
        'ant-design': {
            'type': 'CSS Framework',
            'logo': ''
        },
        'element-ui': {
            'type': 'CSS Framework',
            'logo': ''
        },
        'vuetify': {
            'type': 'CSS Framework',
            'logo': ''
        },
        '@trpc/server': {
            'type': 'Server-client communication',
            'logo': 'https://trpc.io/img/logo-text-black.svg',
            'dev': 'https://trpc.io/docs'
        },
        'next': {
            'type': 'Frontend Framework',
            'logo': 'https://user-images.githubusercontent.com/4253088/196269841-32444c2d-7798-471d-8c7d-455323680297.png',
            'dev': 'https://nextjs.org/docs/getting-started'
        },
        'express': {
            'type': 'Backend Framework',
            'logo': 'https://camo.githubusercontent.com/0566752248b4b31b2c4bdc583404e41066bd0b6726f310b73e1140deefcc31ac/68747470733a2f2f692e636c6f756475702e636f6d2f7a6659366c4c376546612d3330303078333030302e706e67',
            'dev': 'https://expressjs.com/'
        },
        'koa': {
            'type': 'Backend Framework',
            'logo': ''
        },
        'hapi': {
            'type': 'Backend Framework',
            'logo': ''
        },
        'fastify': {
            'type': 'Backend Framework',
            'logo': ''
        },
        'nest': {
            'type': 'Backend Framework',
            'logo': ''
        },
        'sapper': {
            'type': 'Frontend Framework',
            'logo': ''
        },
        'svelte-kit': {
            'type': 'Frontend Framework',
            'logo': ''
        },
        'strapi': {
            'type': 'Backend Framework',
            'logo': ''
        },
        'nuxt': {
            'type': 'Frontend Framework',
            'logo': ''
        },
        'gatsby': {
            'type': 'Frontend Framework',
            'logo': ''
        },
        'react-native': {
            'type': 'Mobile Framework',
            'logo': ''
        },
        'flutter': {
            'type': 'Mobile Framework',
            'logo': ''
        },
        'ionic': {
            'type': 'Mobile Framework',
            'logo': ''
        },
        'cordova': {
            'type': 'Mobile Framework',
            'logo': ''
        },
        'expo': {
            'type': 'Mobile Framework',
            'logo': ''
        },
        'native-script': {
            'type': 'Mobile Framework',
            'logo': ''
        },
        'react-native-web': {
            'type': 'Mobile Framework',
            'logo': ''
        },
        'prisma': {
            'type': 'ORM',
            'logo': 'https://website-v9.vercel.app/logo-dark.svg',
            'dev': 'https://prisma.io/'
        },
        'typeorm': {
            'type': 'ORM',
            'logo': ''
        },
        'sequelize': {
            'type': 'ORM',
            'logo': ''
        },
        'mongoose': {
            'type': 'ORM',
            'logo': ''
        },
        'vitest': {
            'type': 'Test runner',
            'logo': 'https://user-images.githubusercontent.com/4253088/196270525-cea1d088-d329-4dba-879d-5e48ef779544.png',
            'dev': 'https://vitest.dev/'
        },
        'react-testing-library': {
            'type': 'Test runner',
            'logo': ''
        },
        'jest-circus': {
            'type': 'Test runner',
            'logo': ''
        },
        'jest-jasmine2': {
            'type': 'Test runner',
            'logo': ''
        },
        'jest-mocha': {
            'type': 'Test runner',
            'logo': ''
        },
        'protractor': {
            'type': 'Test runner',
            'logo': ''
        },
        'cypress': {
            'type': 'Test runner',
            'logo': ''
        },
        'ava': {
            'type': 'Test runner',
            'logo': ''
        },
        '@testing-library/react': {
            'type': 'Testing components',
            'logo': 'https://user-images.githubusercontent.com/4253088/196271647-0265eca3-61e4-44c2-8641-fabdb07e875f.png',
            'dev': 'https://testing-library.com/docs/react-testing-library/intro/'
        },
        'enzyme': {
            'type': 'Testing components',
            'logo': ''
        },
        'storybook': {
            'type': 'Component library',
            'logo': 'https://user-images.githubusercontent.com/321738/63501763-88dbf600-c4cc-11e9-96cd-94adadc2fd72.png',
            'dev': 'https://storybook.js.org/docs/react/get-started/introduction'
        },
        '@storybook/react': {
            'type': 'Component library',
            'logo': 'https://user-images.githubusercontent.com/321738/63501763-88dbf600-c4cc-11e9-96cd-94adadc2fd72.png',
            'dev': 'https://storybook.js.org/docs/react/get-started/introduction'
        },
        '@storybook/vue': {
            'type': 'Component library',
            'logo': 'https://user-images.githubusercontent.com/321738/63501763-88dbf600-c4cc-11e9-96cd-94adadc2fd72.png',
            'dev': 'https://storybook.js.org/docs/vue/get-started/introduction'
        },
        '@storybook/angular': {
            'type': 'Component library',
            'logo': 'https://user-images.githubusercontent.com/321738/63501763-88dbf600-c4cc-11e9-96cd-94adadc2fd72.png',
            'dev': 'https://storybook.js.org/docs/angular/get-started/introduction'
        },
        '@storybook/svelte': {
            'type': 'Component library',
            'logo': 'https://user-images.githubusercontent.com/321738/63501763-88dbf600-c4cc-11e9-96cd-94adadc2fd72.png',
            'dev': 'https://storybook.js.org/docs/svelte/get-started/introduction'
        },
        '@storybook/html': {
            'type': 'Component library',
            'logo': 'https://user-images.githubusercontent.com/321738/63501763-88dbf600-c4cc-11e9-96cd-94adadc2fd72.png',
            'dev': 'https://storybook.js.org/docs/html/get-started/introduction'
        },
        '@storybook/addon-docs': {
            'type': 'Component library',
            'logo': 'https://user-images.githubusercontent.com/321738/63501763-88dbf600-c4cc-11e9-96cd-94adadc2fd72.png',
            'dev': 'https://storybook.js.org/docs/react/writing-docs/introduction'
        },
        '@storybook/addon-controls': {
            'type': 'Component library',
            'logo': 'https://user-images.githubusercontent.com/321738/63501763-88dbf600-c4cc-',
            'dev': 'https://storybook.js.org/docs/react/essentials/controls'
        },
        'react-styleguidist': {
            'type': 'Component library',
            'logo': ''
        },
        'docz': {
            'type': 'Component library',
            'logo': ''
        },
        'bit': {
            'type': 'Component library',
            'logo': ''
        },
        'msw': {
            'type': 'Mocking',
            'logo': 'https://user-images.githubusercontent.com/11342649/204375767-0075e85e-3602-41d7-a9e7-03c4f8c36f32.png',
            'dev': 'https://mswjs.io/docs/'
        },
        'nock': {
            'type': 'Mocking',
            'logo': ''
        },
        'sinon': {
            'type': 'Mocking',
            'logo': ''
        },
        'eslint': {
            'type': 'Lint',
            'logo': '',
            'dev': 'https://eslint.org/docs/user-guide/getting-started'
        },
        'prettier': {
            'type': 'Lint',
            'logo': ''
        },
        'stylelint': {
            'type': 'Lint',
            'logo': ''
        },
        'tslint': {
            'type': 'Lint',
            'logo': ''
        },
        'husky': {
            'type': 'Lint',
            'logo': ''
        },
        'lint-staged': {
            'type': 'Lint',
            'logo': ''
        },
        '@ladle/react': {
            'type': 'Testing Components',
            'logo': 'https://user-images.githubusercontent.com/4253088/196270689-6216be78-82a5-4800-b3ee-81fe47792360.png',
            'dev': ''
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
    <th>{columns[0]}</th>
    <th>{columns[1]}</th>
    <th>{columns[2]}</th>
'''
    TAIL = tail_format
    cell_width = 1.5 * img_width
    cell_height = 1.5 * img_width
    for package in dev_stack_data:
        name = package['name']
        version = package['version']
        package_obj = map_package_to_framework_type(name)
        package_type = package_obj.get('type', '')
        package_logo = package_obj.get('logo', '')
        package_dev = package_obj.get('dev', '')
        if package_type == '':
            continue
        # fetch latest version from unpkg
        try:
            response = requests.get(f'https://unpkg.com/{name}/package.json')
            response.raise_for_status()
            print(f'Fetching latest version of {name} from unpkg')
            print(response)
            if response.status_code != 204:
                json = response.json()
            if 'version' in json:
                latest_version = json['version']
            else:
                latest_version = version
            if version == 'latest':
                version = latest_version
            if version[0] == latest_version[0]:
                version = f'https://img.shields.io/badge/{version}-brightgreen'
            elif version[0] - latest_version[0] == 1:
                version = f'https://img.shields.io/badge/{version}-yellow'
            elif version[0] - latest_version[0] > 1:
                version = f'https://img.shields.io/badge/{version}-red'
        except:
            version = f'https://img.shields.io/badge/{version}-brightgreen'
        new_tr = '''\n</tr>\n<tr>'''
        HEAD = HEAD + new_tr
        if shape == 'round':
            img_style = ' style="border-radius:50%;align-items:center;justify-content:center;overflow:hidden;padding-top:10px"'
        else:
            img_style = ''
        logo = name.capitalize()
        package_src = ''
        package_dev_ref = ''
        if package_logo != '':
            logo = f'''<img style="width:width:{img_width};" src="{package_logo}" {img_style} alt="{name}"/>'''
        if package_dev != '':
            package_dev_ref = f'href="{package_dev}"'
        td = f'''
    <td align="center" style="word-wrap: break-word; width: {cell_width}; height: {cell_height}">
        {package_obj.get("type","")}
    </td>
    <td align="center" style="word-wrap: break-word; width: {cell_width}; height: {cell_height}">
        <a aria-label="{name}" {package_dev_ref}>
            {logo}
        </a>
    </td>
    <td align="center" style="word-wrap: break-word; width: {cell_width}; height: {cell_height}">
        <a aria-label="NPM Version" href="https://www.npmjs.com/package/{name}">
            <img src="{version}" {img_style} alt="{name}"/>
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
        'IMG_WIDTH', 'FONT_SIZE', 'PATH', 'COMMIT_MESSAGE', 'AVATAR_SHAPE'
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
