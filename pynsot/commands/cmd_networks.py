# -*- coding: utf-8 -*-

"""
Sub-command for Networks.

In all cases ``data = ctx.params`` when calling the appropriate action method
on ``ctx.obj``. (e.g. ``ctx.obj.add(ctx.params)``)

Also, ``action = ctx.info_name`` *might* reliably contain the name of the
action function, but still not sure about that. If so, every function could be
fundamentally simplified to this::

    getattr(ctx.obj, ctx.info_name)(ctx.params)
"""

__author__ = 'Jathan McCollum'
__maintainer__ = 'Jathan McCollum'
__email__ = 'jathan@dropbox.com'
__copyright__ = 'Copyright (c) 2015 Dropbox, Inc.'


import click


# Ordered list of 2-tuples of (field, display_name) used to translate object
# field names oto their human-readable form when calling .print_list().
DISPLAY_FIELDS = (
    ('id', 'ID'),
    ('network_address', 'Network'),
    ('prefix_length', 'Prefix'),
    # ('site_id': 'Site ID'),
    ('is_ip', 'Is IP?'),
    ('ip_version', 'IP Ver.'),
    ('parent_id', 'Parent ID'),
    ('attributes', 'Attributes'),
)


# Main group
@click.group()
@click.pass_context
def cli(ctx):
    """Network objects."""


def transform_attributes(ctx, param, value):
    """Callback to turn attributes arguments into a dict."""
    attrs = {}
    for attr in value:
        key, _, val = attr.partition('=')
        if not all([key, val]):
            msg = 'Invalid attribute: %s; format should be key=value' % (attr,)
            raise click.UsageError(msg)
        attrs[key] = val
    return attrs


# Add
@cli.command()
@click.option(
    '-a',
    '--attributes',
    metavar='ATTRS',
    help='A key/value pair attached to this Network (format: key=value).',
    multiple=True,
    callback=transform_attributes,
)
@click.option(
    '-c',
    '--cidr',
    metavar='CIDR',
    help='A network or IP address in CIDR notation.',
    required=True,
)
@click.option(
    '-s',
    '--site-id',
    metavar='SITE_ID',
    help='Unique ID of the Site this Network is under.',
    required=True,
)
@click.pass_context
def add(ctx, cidr, attributes, site_id):
    """
    Add a new Network.

    You must provide a Site ID using the -s/--site-id option.

    When adding a new Network, you must provide a value for the -c/--cidr
    option.

    If you wish to add attributes, you may specify the -a/--attributes
    option once for each key/value pair.
    """
    data = ctx.params
    ctx.obj.add(data)


# List
@cli.command()
@click.option(
    '-i',
    '--id',
    metavar='ID',
    help='Unique ID of the Network being retrieved.',
)
@click.option(
    '-l',
    '--limit',
    metavar='LIMIT',
    help='Limit result to N resources.',
)
@click.option(
    '-o',
    '--offset',
    metavar='OFFSET',
    help='Skip the first N resources.',
)
@click.option(
    '-s',
    '--site-id',
    metavar='SITE_ID',
    help='Unique ID of the Site this Network is under.',
    required=True,
)
@click.pass_context
def list(ctx, id, limit, offset, site_id):
    """
    List existing Networks for a Site.

    You must provide a Site ID using the -s/--site-id option.

    When listing Networks, all objects are displayed by default. You optionally
    may lookup a single Network by ID using the -i/--id option.

    You may limit the number of results using the -l/--limit option.
    """
    data = ctx.params
    ctx.obj.list(data, display_fields=DISPLAY_FIELDS)


# Remove
@cli.command()
@click.option(
    '-i',
    '--id',
    metavar='ID',
    help='Unique ID of the Network being deleted.',
    required=True,
)
@click.option(
    '-s',
    '--site-id',
    metavar='SITE_ID',
    help='Unique ID of the Site this Network is under.',
    required=True,
)
@click.pass_context
def remove(ctx, id, site_id):
    """
    Remove a Network.

    You must provide a Site ID using the -s/--site-id option.

    When removing a Network, you must provide the unique ID using -i/--id. You
    may retrieve the ID for a Network by parsing it from the list of Networks
    for a given Site:

        nsot networks list --site <site_id> | grep <network>
    """
    data = ctx.params
    ctx.obj.remove(**data)


# Update
@cli.command()
@click.option(
    '-a',
    '--attributes',
    metavar='ATTRS',
    help='A key/value pair attached to this Network (format: key=value).',
    multiple=True,
    callback=transform_attributes,
)
@click.option(
    '-i',
    '--id',
    metavar='ID',
    help='Unique ID of the Network being updated.',
    required=True,
)
@click.option(
    '-s',
    '--site-id',
    metavar='SITE_ID',
    help='Unique ID of the Site this Network is under.',
    required=True,
)
@click.pass_context
def update(ctx, attributes, id, site_id):
    """
    Update a Network.

    You must provide a Site ID using the -s/--site-id option.

    When updating a Network you must provide the unique ID (-i/--id) and at
    least one of the optional arguments.
    """
    if not any([attributes]):
        msg = 'You must supply at least one of the optional arguments.'
        raise click.UsageError(msg)

    data = ctx.params
    ctx.obj.update(data)
