define([
    'jquery',
    'base/js/dialog',
    'base/js/events',
    'base/js/namespace',
    //'notebook/js/celltoolbar',
    'notebook/js/codecell',
    'typeahead'
], function (
    $,
    dialog,
    events,
    Jupyter,
    // celltoolbar,
    codecell ,  typeahead
) {
    "use strict";

    var mod_name = 'schemaindex_nbext_run';
    var log_prefix = '[' + mod_name + ']';
    var options = { // updated from server's config & nb metadata
        run_on_kernel_ready: true,
    };

    var toolbar_preset_name = 'Schemaindex Cell';

    function init_schemaindex_extension () {
        console.log(log_prefix, 'Loading schemaindex search extension ...');
        //var num = 0;
        dialog.modal({
                    title : 'Search for data and generate snippets ...',
                    body : build_schemaindex_search_modal(),
                    notebook: Jupyter.notebook,
                    keyboard_manager: Jupyter.keyboard_manager,
                    buttons: {
                        'Manage Data Sources': {
                            class : 'btn-primary',
                            click: function(event) {
                                event.preventDefault();
                                window.open(window.location.protocol+ '//' + window.location.hostname + ':8088/overview');
                                }
                        },
                        Cancel: {class : 'btn-primary'},

                    },
                });
        // $('#schemaindex_search_term').focus();

    }

    var load_ipython_extension = function() {
        // register action
        var prefix = 'auto';
        var action_name = 'run-schemaindex';
        var action = {
            icon: 'fa-database',
            help: 'Schemaindex Snippets',
            help_index : 'sizzxx',
            handler : init_schemaindex_extension
        };
        var action_full_name = Jupyter.notebook.keyboard_manager.actions.register(action, action_name, prefix);

        // add toolbar button
        Jupyter.toolbar.add_buttons_group([action_full_name]);

        // setup things to run on loading config/notebook
        Jupyter.notebook.config.loaded
            .then(function update_options_from_config () {
                $.extend(true, options, Jupyter.notebook.config.data[mod_name]);
            }, function (reason) {
                console.warn(log_prefix, 'error loading config:', reason);
            })
            .then(function () {
                if (Jupyter.notebook._fully_loaded) {
                    callback_notebook_loaded();
                }
                events.on('notebook_loaded.Notebook', callback_notebook_loaded);
            }).catch(function (reason) {
                console.error(log_prefix, 'unhandled error:', reason);
            });
    };

    function callback_notebook_loaded () {
        // update from metadata
        var md_opts = Jupyter.notebook.metadata[mod_name];
        if (md_opts !== undefined) {
            //console.log(log_prefix, 'after notebook loaded, schemaindex start its initial work. updating options from notebook metadata:', md_opts);
            $.extend(true, options, md_opts);
        }

    }
/*
    function html_table_from_result_json() {
        var search_result_table_html = '<br> <div ><table class=\"table table-bordered table-hover\"> \
                        <thead><tr><th>Data ID</th> <th>Data Source</th> <th>Details</th> <th>Snippets</th></tr></thead> \
                        <tbody  id="the_search_result_table_to_append"></tbody></table></div>';

        var full_table = beg_table ;
        return full_table
    }
*/

    function build_schemaindex_search_modal () {
        var schemaindex_modal = $('#schemaindex_modal');
        if (schemaindex_modal.length > 0) return schemaindex_modal;

        schemaindex_modal = $('<div/>').attr('id', 'schemaindex_modal') ;
        // for typeahead, following http://www.runningcoder.org/jquerytypeahead/demo/
        // Those pages explained typeahead well.
        // https://github.com/running-coder/jquery-typeahead/issues/48
        // https://github.com/running-coder/jquery-typeahead/issues/42
        // also refer to : /static/notebook/js/commandpalette.js

        var typeahead_form   = $('<form/>');
        var container = $('<div/>').addClass('typeahead-container');
        var field = $('<div/>').addClass('typeahead-field');
        var input = $('<input />').attr('type', 'search').attr('placeholder', 'search').attr('id', 'schemaindex_search_term');


        field
          .append(
            $('<span>').addClass('typeahead-query').append(
              input
            )
          )
          .append(
            $('<span/>').addClass('typeahead-button').append(
              $('<button/>').attr('type', 'submit').attr(  'id','the_search_button').append(
                $('<span/>').addClass('typeahead-search-icon')
              )
            )
          );

        container.append(field);
        typeahead_form.append(container);


        input.typeahead({
            emptyTemplate: "No results found for <pre>{{query}}</pre>",
            minLength: 1,
            dynamic: true,
            delay: 0,
            display: ["table_id", "table_freq"],
            template: '{{table_id}}  <div class="pull-right ">{{table_freq}}</div>',
            order: "asc",
            source:  {
                        results: {
                            url: {

                                type: "GET",
                                url: "/schemaindex/search_suggestion_json",
                                data: {
                                    query: "{{query}}"
                                },
                                callback: {
                                    // You do not need done callback if you are not doing post-request operation
                                    done: function (data) {
                                        //console.log("i got data:", data);
                                        return data;
                                    }
                                }
                            } }
                    }  ,
              debug: false,
            });

        $('<div/>')
            .addClass('row')
            .appendTo(schemaindex_modal)
            .append( typeahead_form  );


                $.ajax({
                    url: '/schemaindex/get_schemaindex_statistics'  ,
                    type: 'GET',
                    async:false,
                    success: function (response, textStatus, jqXHR) {
                        //console.log('success, got code: ',response);
                        var resDict = JSON.parse(String(response));
                        var actionMessage = 'Please type in search terms and click Search Button...';
                        if (resDict['ds_count'] < 1 ){
                            actionMessage = 'Please click "Manage Data Source" to add data sources...'
                        }


                        $('<div/>')
                            .addClass('row')
                            .appendTo(schemaindex_modal)
                            .append(
                                $('<div/>')
                                    .attr('id', 'schemaindex_search_result_tbody')
                                    .append(
                                        $('<br><label>')
                                            .text(resDict['ds_count']+' Data Sources, '
                                                + resDict['table_count']+' Entities available. '
                                                + actionMessage)
                                    )
                            );


                    },
                    error: function (jqXHR, textStatus, errorThrown) {console.log('eerrrrrr, duanqiyang', errorThrown)},
                    complete: function (jqXHR, textStatus) {
                        //console.log('completeee ajax get_schemaindex_statistics: ', textStatus)
                    }
                });





        var insert_snippets_func = function(table_id, ds_name) {
                // get the code snippet from server extension
                $.ajax({
                    url: '/schemaindex/generate_snippet?ds_name=' + ds_name + '&table_id=' + table_id  ,
                    type: 'GET',
                    data: { table_id:table_id , time: "2pm" },
                    success: function (response, textStatus, jqXHR) {
                        //console.log('success, got code: ',response);
                        var code = response;
                        var new_cell = Jupyter.notebook.insert_cell_above('code');
                        new_cell.set_text(code);
                        new_cell.focus_cell();

                    },
                    error: function (jqXHR, textStatus, errorThrown) {console.log('eerrrrrr, duanqiyang', errorThrown)},
                    complete: function (jqXHR, textStatus) {
                        //console.log('completeee ajax: ', textStatus)
                    }
                });



        };

        schemaindex_modal.find('#the_search_button').bind("click", function(event) {
                event.preventDefault()
                //console.log('i will searcj fpr, duanqiyang:', id_input.data('oldVal'), ', new value:' , id_input.val());

                // get the search result
                $.ajax({
                    url: '/schemaindex/global_search_formatted', // ?q=' +  $('#schemaindex_search_term').val() , //id_input.val() ,
                    type: 'GET',
                    data: { q: $('#schemaindex_search_term').val() , time: "2pm" },
                    success: function (response, textStatus, jqXHR) {
                        //console.log('success, duanqiyang',response);
                        var resDict = JSON.parse(String(response));
                        schemaindex_modal.find('#schemaindex_search_result_tbody').html('');

                        if (resDict.hasOwnProperty('table')) {
                            var varList = resDict['table'];

                            var search_result_table_html = '<br> <div ><table class=\"table table-bordered table-hover\"> \
                                            <thead><tr><th>Table Name</th> <th>Data Source</th> <th>Column List</th> <th>Snippets</th></tr></thead> \
                                            <tbody  id="schemaindex_search_result_table_to_append_table"></tbody></table></div>';

                            schemaindex_modal.find('#schemaindex_search_result_tbody').append(search_result_table_html);

                            var the_search_result_tbody = schemaindex_modal.find('#schemaindex_search_result_table_to_append_table');

                            for (var i = 0; i < varList.length; i++) {
                                    var columnInfoJSON = JSON.parse(varList[i].table_info)['column_info'];
                                    var columnString = '';
                                    for ( var ij = 0; ij< columnInfoJSON.length; ij++){
                                        columnString = columnString + columnInfoJSON[ij][0] + ', '
                                    }

                                    var tr = '<tr>';
                                    tr += '<td>' + varList[i].table_id + '</td>';
                                    tr += '<td>' + varList[i].ds_name + '</td>';
                                    tr += '<td>' + columnString + '</td>';
                                    tr += '<td><button class="addsnippets" data-key="'+ varList[i].table_id +'"><i class="fa fa-file-code-o">Insert</i></button></td>';
                                    tr += '</tr>';
                                    the_search_result_tbody.append(tr);
                            }
                        }

                        if (resDict.hasOwnProperty('file')) {
                            var varList = resDict['file'];

                            var search_result_table_html = '<br> <div ><table class=\"table table-bordered table-hover\"> \
                                            <thead><tr><th>File Path</th> <th>Data Source</th> <th>Changed At</th> <th>Snippets</th></tr></thead> \
                                            <tbody  id="schemaindex_search_result_table_to_append_file"></tbody></table></div>';

                            schemaindex_modal.find('#schemaindex_search_result_tbody').append(search_result_table_html);

                            var the_search_result_tbody = schemaindex_modal.find('#schemaindex_search_result_table_to_append_file');

                            for (var i = 0; i < varList.length; i++) {
                                    var modificationTime = JSON.parse(varList[i].table_info)['modificationTime'];


                                    var tr = '<tr>';
                                    tr += '<td>' + varList[i].table_id + '</td>';
                                    tr += '<td>' + varList[i].ds_name + '</td>';
                                    tr += '<td>' + modificationTime + '</td>';
                                    tr += '<td><button class="addsnippets" data-key="'+ varList[i].table_id +'"><i class="fa fa-file-code-o">Insert</i></button></td>';
                                    tr += '</tr>';
                                    the_search_result_tbody.append(tr);
                            }
                        }
                    },
                    error: function (jqXHR, textStatus, errorThrown) {console.log('eerrrrrr, duanqiyang', errorThrown)},
                    complete: function (jqXHR, textStatus) {
                        //console.log('completeee ajax: ', textStatus)
                        $('button.addsnippets').unbind().bind('click', function() {
                            var ds_name =  $('td:nth-child(2)', $(this).parents('tr')).text();
                            // console.log('adding snippet ajax: ', $(this).data('key'),     ds_name);
                            insert_snippets_func($(this).data('key'),   ds_name  );
                          });

                        
                    }  
                });
            

        });

        //TODO: This does not work yet.
        schemaindex_modal.on('shown', function () {
                schemaindex_modal.find('#schemaindex_search_term').focus();
                setTimeout(function (){
                    $('#schemaindex_search_term').focus();
                }, 1000);

            })

        
        return schemaindex_modal;
    }


    return {
        load_ipython_extension : load_ipython_extension
    };
});
