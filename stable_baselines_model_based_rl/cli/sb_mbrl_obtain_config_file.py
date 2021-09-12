import os
import shutil

import click


@click.command(
    help="Obtain the base/default configuration file. It'll be copied into the current working"
         "directory, unless you specify a custom DESTINATION path.")
@click.argument('destination', default='./config.yaml')
def obtain_config_file(destination):
    file_path = os.path.dirname(os.path.abspath(__file__))
    sample_config_path = os.path.join(file_path, '../../example_usage/sample_config.yaml')
    sample_config_path = os.path.abspath(sample_config_path)
    dest_path = os.path.abspath(destination)
    shutil.copyfile(sample_config_path, dest_path)
    click.echo(f'Config available under: {dest_path}')
