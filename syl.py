#!/usr/bin/env python

import argparse
import os
import subprocess
import tempfile
from distutils import dir_util

parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(dest='command')

parser_create = subparsers.add_parser('create')
parser_create.add_argument('template', choices=[
    'sls/fn',
    'react'
])
parser_create.add_argument('--name', default='file')

args = parser.parse_args()

if args.command == 'create':
    template_path = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        'templates',
        *args.template.split('/'))

    template_command_path = os.path.join(template_path, '__command__')
    if os.path.isfile(template_command_path):
        subprocess.run([template_command_path])
    else:
        with tempfile.TemporaryDirectory() as tmp_path:
            dir_util.copy_tree(template_path, tmp_path)
            for root, dirs, files in os.walk(tmp_path):
                for file in files:
                    if '__NAME__' not in file:
                        continue
                    file_path = os.path.join(root, file)
                    file_renamed_path = os.path.join(
                        root, file.replace('__NAME__', args.name))
                    os.rename(file_path, file_renamed_path)
            dir_util.copy_tree(tmp_path, os.getcwd())
