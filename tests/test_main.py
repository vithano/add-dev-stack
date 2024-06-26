#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Author       : BobAnkh
# @Github       : https://github.com/BobAnkh
# @Date         : 2021-01-09 11:53:15
# @LastEditTime : 2021-01-10 22:01:16
# @Description  : Tests for main.py

import json
import random
import string
import sys

import pytest

sys.path.append('.')
import main

case = json.load(open('tests/case.json'))


@pytest.fixture(params=case['test_env_case'])
def generate_env(request):
    output = {}
    output['env_name'] = request.param
    output['env_value'] = ''.join(
        random.sample(string.ascii_letters + string.digits, 20))
    return output


def test_env(generate_env):
    env_name = generate_env['env_name']
    env_value = generate_env['env_value']
    main.set_local_env(env_name, env_value)
    msg = "Test case %s is wrong" % (env_name)
    assert env_value == main.get_inputs(env_name), msg


@pytest.mark.parametrize(
    'dev_stack_data, row, width, font_size, head,tail, rsb, dev_stack_table',
    case['test_table_case'])
def test_table(dev_stack_data, row, width, font_size, head, tail, rsb,
               dev_stack_table):
    assert dev_stack_table == main.generate_dev_stack_table(
        dev_stack_data, row, width, font_size, head, tail, rsb)


@pytest.mark.parametrize(
    'content, dev_stack_table, DEV_STACK, PATH, text',
    case['test_content_case'])
def test_content(content, dev_stack_table, DEV_STACK, PATH, text):
    assert text == main.generate_content(content, dev_stack_table,
                                         DEV_STACK, PATH)
