#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" stanmoctl.py
    
    Usage:
        schemaindex -h
        schemaindex runserver [--port=<port> ] [--instance=<id> ]
        schemaindex list ( data_source | plugin )
        schemaindex add <data_source_name> --plugin=<spec_name> --ds_param=<ds_param_string>
        schemaindex reload plugin
        schemaindex reflect <data_source_name>
        schemaindex search <search_key_word>...
        schemaindex show <data_source_name>

    Options:
        -h,--help             : show this help message
        data_source_name      : name of data source given when it was created
        spec_name             : The name of model specification
        --input_file=<path>   : Path of input files to the model
        --output_file=<path>  : Path to write the model output file.
        --instance=<id>       : The model instance ID.
        --port=<port>         : The OS port where server will be listening on. It uses 5000 if omitted..
"""
# This command push will be implemented later.
#        schemaindex push [specs]
#        schemaindex pull [specs]  # To download a plugin from central repository
#        schemaindex search [specs]
# following: https://github.com/docopt/docopt

import os
from docopt import docopt
from app.schemaindexapp import si_app #
from app.webserver import run_webserver


def list_plugs():
    plist = si_app.get_plugin_list()

    # {"name":spec_name, "path":os.path.join(model_spec_path,item)} )
    if len(plist) > 0:
        print('{0:40} {1:35} '.format('Reflect Plugin Name:', 'Path:  '))
        for spec in plist:
            print('{0:40} {1:55}'.format(spec.plugin_name, os.path.join(spec.plugin_spec_path, spec.module_name)))
    else:
        print('No plugins are found!')



def main():
    """ main-entry point for schemaindex program, parse the commands and build the si_app platform """
    docopt_args = docopt(__doc__)

    # Parse the User command and the required arguments
    if docopt_args["list"]:
        if docopt_args["data_source"] == True:
            # print(json.dumps(si_app.list_models()))
            si_app.list_data_sources()
        elif docopt_args["plugin"] == True:
            list_plugs()


    # Parse the User command and the required arguments
    # create <model_name> --plugin=<spec_name>
    if docopt_args["add"]:
        model_name = docopt_args["<model_name>"]
        spec_name = docopt_args["--plugin"]
        if spec_name is None:
            print("Please specify the <model_name> and <spec_name>")
        si_app.create_model(model_name=model_name, spec_name=spec_name)
        print("Model is created successfully.")


    elif docopt_args["reflect"]:
        # to reflect the specified data source.
        data_source_name = docopt_args["<data_source_name>"]
        the_model = si_app.reflect_db(data_source_name=data_source_name)

    elif docopt_args["search"]:
        # to search by a keyword
        q = docopt_args["<search_key_word>"]
        print(q)
        the_tables = si_app.global_whoosh_search(q=' '.join(q))



    elif docopt_args["runserver"]:
        # to run a HTTP server to provide restful api services..

        if docopt_args["--port"] is not None:
            si_app.config['web']['port'] =  docopt_args["--port"]
        run_webserver(port = si_app.config['web']['port'])

    elif docopt_args["reload"]:
        # to reload from plugin folder
        if docopt_args["plugin"] == True:
            si_app.scan_reflect_plugins()
            print("Plugins are reloaded.")
            list_plugs()


    elif docopt_args["show"]:
        # to predict according to trained a model, given the input file.
        port = 5011
        if docopt_args["--port"] is not None:
            port =  docopt_args["--port"]

        model_name = docopt_args["<model_name>"]
        the_model = si_app.load_model(model_name=model_name)
        try:
            the_model.show(port=port)
        except :
            print('Failed to show the model: {0}'.format(e.strerror))


# START OF SCRIPT
if __name__ == "__main__":
    main()


