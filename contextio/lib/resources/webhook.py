from __future__ import absolute_import
import logging

from .base_resource import BaseResource

class WebHook(BaseResource):
    """Class to represent the WebHook resource.

    Properties:
        callback_url: string - Your callback URL to which we'll POST
            message data
        failure_notif_url: string - Your callback URL for failure
            notifications
        active: bool - Whether this webhook is currently applied to
            new messages we find in the account or not
        failure: bool - true means we're having issues connecting to
            the account and gave up after a couple retries. The
            failure_notif_url is called when a webhook's failure
            property becomes true.
        webhook_id: string - Id of the webhook
        filter_to: string - Check for new messages sent to a given name or
            email address.
        filter_from: string - Check for new messages received from a given
            name or email address.
        filter_cc: string - Check for new messages where a given name or
            email address is cc'ed
        filter_subject: string - Check for new messages with a subject
            matching a given string or regular expresion
        filter_thread: string - Check for new messages in a given thread.
            Value can be a gmail_thread_id or the email_message_id or
            message_id of an existing message currently in the thread.
        filter_new_important: string - Check for new messages
            automatically tagged as important by the Gmail Priority Inbox
            algorithm. To trace all messages marked as important
            (including those manually set by the user), use
            filter_folder_added with value Important. Note the leading
            back-slash character in the value, it is required to keep this
            specific to Gmail Priority Inbox. Otherwise any message placed
            in a folder called "Important" would trigger the WebHook.
        filter_file_name: string - Check for new messages where a file
            whose name matches the given string is attached. Supports
            wildcards and regular expressions like the file_name parameter
            of the files list call.
        filter_folder_added: string - Check for messages filed in a given
            folder. On Gmail, this is equivalent to having a label applied
            to a message. The value should be the complete name (including
            parents if applicable) of the folder you want to track.
        filter_folder_removed: string - Check for messages removed from a
            given folder. On Gmail, this is equivalent to having a label
            removed from a message. The value should be the complete name
            (including parents if applicable) of the folder you want to
            track.
        filter_to_domain: string - Check for new messages sent to a given
            domain. Also accepts a comma delimited list of domains.
        filter_from_domain: string - Check for new messages sent from a given
            domain. Also accepts a comma delimited list of domains.
    """
    resource_id = "webhook_id"
    keys = [
        "callback_url", "failure_notif_url", "active", "failure",
        "webhook_id", "filter_to", "filter_from", "filter_cc",
        "filter_subject", "filter_thread", "filter_new_important",
        "filter_file_name", "filter_folder_added", "filter_folder_removed",
        "filter_to_domain", "filter_from_domain", "version", "receive_historical", "receive_all_changes", "include_body", "body_type", "include_header"
    ]

    def __init__(self, parent, defn):
        """Constructor.

        Required Arguments:
            parent: Account object - parent is an Account object.
            defn: a dictionary of parameters. The 'webhook_id' parameter
                is required to make method calls.
        """
        super(WebHook, self).__init__(parent, 'webhooks/{webhook_id}', defn)

    def get(self):
        """Get properties of a given webhook.

        Documentation: http://context.io/docs/2.0/accounts/webhooks#id-get

        Arguments:
            None

        Returns:
            True if self is updated, else will throw a request error
        """
        return super(WebHook, self).get()

    def put(self):
        logging.info("This method is not implemented")

    def post(self, **params):
        """Change properties of a given WebHook.

        Returns:
            Bool
        """
        all_args = ["callback_url", "failure_notif_url", "active",
        "filter_to", "filter_from", "filter_cc",
        "filter_subject", "filter_thread", "filter_new_important",
        "filter_file_name", "filter_folder_added", "filter_folder_removed",
        "filter_to_domain", "filter_from_domain", "receive_historical", "receive_all_changes", "include_body", "body_type", "include_header"]

        return super(WebHook, self).post(params=params, all_args=all_args)

    def delete(self):
        """Delete a webhook.

        Documentation: http://context.io/docs/2.0/accounts/webhooks#id-delete

        Arguments:
            None

        Returns:
            Bool
        """
        return super(WebHook, self).delete()
