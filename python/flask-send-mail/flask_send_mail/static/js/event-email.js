/*
 * JavaScript file for the application to demonstrate
 * using the API for the Recipient
 */

// Create the namespace instance
let ns = {};

// Create the model instance
ns.model = (function () {
    'use strict';

    // Return the API
    return {
        read_one: function (event_email_id) {
            let ajax_options = {
                type: 'GET',
                url: `/api/event_emails/${event_email_id}`,
                accepts: 'application/json',
                dataType: 'json'
            };
            return $.ajax(ajax_options);
        },
        read: function () {
            let ajax_options = {
                type: 'GET',
                url: '/api/event_emails',
                accepts: 'application/json',
                dataType: 'json'
            };
            return $.ajax(ajax_options);
        },
        create: function (data) {
            let ajax_options = {
                type: 'POST',
                url: '/api/save_emails',
                accepts: 'application/json',
                contentType: 'application/json',
                dataType: 'json',
                data: JSON.stringify(data)
            };
            return $.ajax(ajax_options);
        },
        update: function (data) {
            let ajax_options = {
                type: 'PATCH',
                url: `/api/event_emails/${data.id}`,
                accepts: 'application/json',
                contentType: 'application/json',
                dataType: 'json',
                data: JSON.stringify(data)
            };
            return $.ajax(ajax_options);
        },
        'delete': function (event_email_id) {
            let ajax_options = {
                type: 'DELETE',
                url: `/api/event_emails/${event_email_id}`,
                accepts: 'application/json',
                contentType: 'plain/text'
            };
            return $.ajax(ajax_options);
        }
    };
}());

// Create the view instance
ns.view = (function () {
    'use strict';

    const NEW_NOTE = 0,
        EXISTING_NOTE = 1;

    let $event_email_id = $('#event_email_id'),
        $event_id = $('#event-id'),
        $email_subject = $('#email-subject'),
        $email_content = $('#email-content'),
        $timestamp = $('#timestamp'),
        $recipients = $('#recipients'),
        $create = $('#create'),
        $update = $('#update'),
        $delete = $('#delete'),
        $reset = $('#reset');

    // return the API
    return {
        NEW_NOTE: NEW_NOTE,
        EXISTING_NOTE: EXISTING_NOTE,
        reset: function () {
            $event_email_id.text('');
            $event_id.val('').focus();
            $email_subject.val('');
            $email_content.val('');
            $timestamp.val('');
            $recipients.val('');
        },
        update_editor: function (data) {
            $event_email_id.text(data.id);
            $event_id.val(data.event_id).focus();
            $email_subject.val(data.email_subject);
            $email_content.val(data.email_content);
            $timestamp.val(data.timestamp);
            $recipients.val(data.recipients);
        },
        set_button_state: function (state) {
            if (state === NEW_NOTE) {
                $create.prop('disabled', false);
                $update.prop('disabled', true);
                $delete.prop('disabled', true);
            } else if (state === EXISTING_NOTE) {
                $create.prop('disabled', true);
                $update.prop('disabled', false);
                $delete.prop('disabled', false);
            }
        },
        build_table: function (people) {
            let source = $('#people-table-template').html(),
                template = Handlebars.compile(source),
                html;

            // clear the table
            $('.people table > tbody').empty();

            if (people) {

                // Create the HTML from the template and event email
                html = template({event_email: people})

                // Append the html to the table
                $('table').append(html);
            }
        },
        error: function (error_msg) {
            $('.error')
                .text(error_msg)
                .css('visibility', 'visible');
            setTimeout(function () {
                $('.error').fadeOut();
            }, 2000)
        }
    };
}());

// Create the controller
ns.controller = (function (m, v) {
    'use strict';

    let model = m,
        view = v,
        $url_event_email_id = $('#url_event_email_id'),
        $event_email_id = $('#event_email_id'),
        $event_id = $('#event-id'),
        $email_subject = $('#email-subject'),
        $email_content = $('#email-content'),
        $timestamp = $('#timestamp'),
        $recipient_ids = $('#recipients');

    // Get the data from the model after the controller is done initializing
    setTimeout(function () {
        view.reset();
        model.read()
            .done(function (data) {
                view.build_table(data);
            })
            .fail(function (xhr, textStatus, errorThrown) {
                error_handler(xhr, textStatus, errorThrown);
            })

        if ($url_event_email_id.val() !== "") {
            model.read_one(parseInt($url_event_email_id.val()))
                .done(function (data) {
                    view.update_editor(data);
                    view.set_button_state(view.EXISTING_NOTE);
                })
                .fail(function (xhr, textStatus, errorThrown) {
                    error_handler(xhr, textStatus, errorThrown);
                });
        }
    }, 100)

    // generic error handler
    function error_handler(xhr, textStatus, errorThrown) {
        let error_msg = `${textStatus}: ${errorThrown} - ${xhr.responseJSON.detail}`;

        view.error(error_msg);
        console.log(error_msg);
    }

    // initialize the button states
    view.set_button_state(view.NEW_NOTE);

    // Validate input
    function validate(event_id, email_subject, email_content, timestamp) {
        return event_id !== "" && email_subject !== "" && timestamp !== "";
    }

    // Create our event handlers
    $('#create').click(function (e) {
        let trimmed_recipient_ids = $recipient_ids.val().replace(/\s/g, '');
        let recipient_ids = trimmed_recipient_ids.split(',').map(function (item) {
            return parseInt(item, 10);
        });

        let event_id = $event_id.val(),
            email_subject = $email_subject.val(),
            email_content = $email_content.val(),
            recipients = recipient_ids,
            timestamp = $timestamp.val().replace("T", " ");

        e.preventDefault();

        if (validate(event_id, email_subject, email_content, timestamp)) {
            model.create({
                'event_id': event_id,
                'email_subject': email_subject,
                'email_content': email_content,
                'timestamp': timestamp + ':00',
                'recipients': recipients
            })
                .done(function (data) {
                    console.log(timestamp)
                    model.read()
                        .done(function (data) {
                            view.build_table(data);
                        })
                        .fail(function (xhr, textStatus, errorThrown) {
                            error_handler(xhr, textStatus, errorThrown);
                        });
                    view.set_button_state(view.NEW_NOTE);
                })
                .fail(function (xhr, textStatus, errorThrown) {
                    error_handler(xhr, textStatus, errorThrown);
                });

            view.reset();

        } else {
            alert('Problem with name or email input');
        }
    });

    $('#update').click(function (e) {
        let trimmed_recipient_ids = $recipient_ids.val().replace(/\s/g, '');
        let recipient_ids = trimmed_recipient_ids.split(',').map(function (item) {
            return parseInt(item, 10);
        });
        let event_email_id = parseInt($event_email_id.text()),
            event_id = $event_id.val(),
            email_subject = $email_subject.val(),
            email_content = $email_content.val(),
            recipients = recipient_ids,
            timestamp = $timestamp.val().replace("T", " ");

        e.preventDefault();

        if (validate(event_id, email_subject, email_content, timestamp)) {
            model.update({
                id: event_email_id,
                event_id: event_id,
                email_subject: email_subject,
                email_content: email_content,
                timestamp: timestamp.length < 17 ? timestamp + ':00' : timestamp,
                recipients: recipients
            })
                .done(function (data) {
                    model.read()
                        .done(function (data) {
                            view.build_table(data);
                        })
                        .fail(function (xhr, textStatus, errorThrown) {
                            error_handler(xhr, textStatus, errorThrown);
                        });
                    view.reset();
                    view.set_button_state(view.NEW_NOTE);
                })
                .fail(function (xhr, textStatus, errorThrown) {
                    error_handler(xhr, textStatus, errorThrown);
                })

        } else {
            alert('Problem with name or email input');
        }
        e.preventDefault();
    });

    $('#delete').click(function (e) {
        let event_email_id = parseInt($event_email_id.text());

        e.preventDefault();

        model.delete(event_email_id)
            .done(function (data) {
                model.read()
                    .done(function (data) {
                        view.build_table(data);
                    })
                    .fail(function (xhr, textStatus, errorThrown) {
                        error_handler(xhr, textStatus, errorThrown);
                    });
                view.reset();
                view.set_button_state(view.NEW_NOTE);
            })
            .fail(function (xhr, textStatus, errorThrown) {
                error_handler(xhr, textStatus, errorThrown);
            });

    });

    $('#reset').click(function () {
        view.reset();
        view.set_button_state(view.NEW_NOTE);
    })

    $('table').on('click', 'tbody tr', function (e) {
        let $target = $(e.target).parent(),
            id = $target.data('event-email-id'),
            event_id = $target.data('event-id'),
            email_subject = $target.data('email-subject'),
            email_content = $target.data('email-content'),
            timestamp = $target.data('timestamp'),
            recipients = $target.data('recipients');

        console.log($target)
        view.update_editor({
            id: id,
            event_id: event_id,
            email_subject: email_subject,
            email_content: email_content,
            timestamp: timestamp,
            recipients: recipients
        });
        view.set_button_state(view.EXISTING_NOTE);
    });
}(ns.model, ns.view));