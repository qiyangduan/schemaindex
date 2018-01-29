#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" stanmoctl.py
    
    Usage:
        schemaindex -h
        schemaindex runserver [--port=<port> ] [--ip=<ip> ] [--browser]
        schemaindex list ( data_source | plugin )
        schemaindex add <data_source_name> --plugin=<spec_name> --ds_param=<ds_param_string>
        schemaindex init
        schemaindex reload plugin
        schemaindex reflect <data_source_name>
        schemaindex snippet <data_source_name> <table_id>
        schemaindex search <search_key_word>...
        schemaindex show <data_source_name>

    Options:
        -h                    : show this help message
        data_source_name      : name of data source given when it was created
        spec_name             : The name of model specification
        --input_file=<path>   : Path of input files to the model
        --output_file=<path>  : Path to write the model output file.
        --ip=<ip>             : The ip address to listen on, and --ip=* indicates all interfaces.
        --port=<port>         : The OS port where server will be listening on. It uses 5000 if omitted..
        --browser             : Open the browser automatically
"""
# This command push will be implemented later.
#        schemaindex push [specs]
#        schemaindex pull [specs]  # To download a plugin from central repository
#        schemaindex search [specs]
# following: https://github.com/docopt/docopt

import os
from docopt import docopt
from schemaindex.app.schemaindexapp import si_app #
from schemaindex.app.webserver import run_webserver
from schemaindex.app.pluginmanager import si_pm

def initialize_schemaindex():
    db_file_path = si_app.config['database']['sqlite_file']
    to_init_indicator = db_file_path  # cfg['main']['init_indicator_file']
    si_app.logger.debug('Checking whether to re-initialize by file:' + to_init_indicator)

    if os.path.exists(to_init_indicator):
        si_app.logger.debug('DB file is ready, no re-init, going to normal startup.')
        return;
    print("\n\r\n\r")
    si_app.logger.debug('SchemaIndex platform will be re-initialized because there no data file yet.')
    print('SchemaIndex platform will be re-initialized because there no data file yet.')

    si_app.schemaindex_init(db_file_path = db_file_path)
    si_pm.scan_reflect_plugins()

    try:
        si_app.init_notebook_extensions()
    except Exception as e:
        print('Exceptions during notebook extension installation: {0}'.format(e.strerror))



    si_app.logger.debug('SchemaIndex platform is initialized.')


# os.remove(to_init_indicator)





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

    # First we initialize the schemaindex database and load the plugins
    initialize_schemaindex()

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

    elif docopt_args["snippet"]:
        # to reflect the specified data source.
        data_source_name = docopt_args["<data_source_name>"]
        table_id = docopt_args["<table_id>"]
        the_snippet = si_pm.generate_notebook_snippet_for_table(table_id=table_id,
                                                                ds_name=data_source_name)
        print(the_snippet)


    elif docopt_args["reflect"]:
        # to reflect the specified data source.
        data_source_name = docopt_args["<data_source_name>"]
        the_model = si_app.reflect_db(data_source_name=data_source_name)

    elif docopt_args["search"]:
        # to search by a keyword
        q = docopt_args["<search_key_word>"]
        print(q)
        tt = si_app.global_whoosh_search_formatted(q=' '.join(q))
        import json
        print(json.dumps(tt))



    elif docopt_args["runserver"]:
        # to run a HTTP server to provide restful api services..

        if docopt_args["--port"] is not None:
            port =  docopt_args["--port"]
        else:
            port = si_app.config['web']['port']

        addr_ip = 'localhost'
        url = 'http://%s:%s/' % (str(addr_ip), str(port))
        if docopt_args["--ip"] is not None:
            addr_ip =  docopt_args["--ip"]
            url = 'http://%s:%s/' % (str(addr_ip), str(port))
            if docopt_args["--ip"] == '*':
                url = 'http://%s:%s/' % ('localhost', str(port))  # 'http://localhost:' + str(port) + '/'

        si_pm.datasource_init()

        print("\n\rServer started, please visit : " + url)

        if docopt_args["--browser"] == True:
            import webbrowser
            # Open URL in new window, raising the window if possible.
            webbrowser.open_new(url)

        run_webserver(addr=addr_ip, port = port)

    elif docopt_args["reload"]:
        # to reload from plugin folder
        if docopt_args["plugin"] == True:
            si_pm.scan_reflect_plugins()
            print("Plugins are reloaded.")
            list_plugs()

    elif docopt_args["init"]:
        # to reload from plugin folder
        si_app.scan_reflect_plugins()
        if docopt_args["plugin"] == True:

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



