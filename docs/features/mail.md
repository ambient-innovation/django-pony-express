# Mailing

## Class-based Emails

This package contains an approach called "class-based emails". Similar to class-based views in django (in comparison to
function-based ones), you can now implement your email as a class and use all the benefits of object-orientated
programming like fiddling around with functions and all the non-DRY repetition of code you'll usually end up with.

USPs:

* Better structure and advantages of object-orientated programming over handling multiple functions!
* Quick and fast creation of new emails - only worry about the things you have to think about!
* No code redundancy for setting up the default mail configuration - all wrapped in the class!
* The text part of the email can be automatically rendered from the HTML part - no redundant templates anymore!
* Built-in (and extendable) sanity checks as a validation for forgotten variables!
* Clean and easy solution for email attachments

There are two scenarios covered by this package:

* **Single mail**: Create a single email through a class to utilise benefits of object-orientation.
* **Similar mails**: Create a bunch of similar emails with a factory class, for example if you want to send the same
  content but with a personal salutation to a number of people.

### Create a single email

Imagine you want to send a single email to a given user or to the system admins. Instead of having to deal with how to
end an email and worry about if the ``to`` field requires a list or string of emails... look at this example:

````
from django_pony_express.services.base import BaseEmailService

class MyFancyClassBasedMail(BaseEmailService):
    """
    Send an email to my admins to inform them about something important.
    """
    subject = _('Heads up, admins!')
    template_name = 'email/my_fancy_class_based_email.html'

    def get_context_data(self):
        data = super().get_context_data()
        data['my_variable'] = ...
        return data
````

This is a simple example of how to create an email. We pass or set the recipients in the `__init__()` method and can add
more data in the `get_context_data()` - or just provide the context on creation as a parameter.

One big advantage is that you can create your own base class which handles all the context data you need to have for
your base email template. Imagine you have an unsubscribe link or a logo in the base template. In the "old world"
you have to think to pass these variables every time. Now, just wrap it up in a base class and that's it!

And that is how you would send the email:

````
from django.conf import settings

email_service = MyFancyClassBasedMail(settings.MY_ADMIN_EMAIL_ADDRESS)
email_service.process()
````

Optionally you can set the class attribute ``template_txt_name`` to define a plain text template. If not set, the HTML
part will be used to render the plain text body.

#### Configuration

You can set a subject prefix, so that all your emails look more similar when setting the constant ``SUBJECT_PREFIX``.

If you wish to define a custom "from" email, you can do so via the ``FROM_EMAIL`` constant. Take care:
If you do not set it, the ``DEFAULT_FROM_EMAIL`` variable from the django settings is used.

#### Public method overview

* `__init__(recipient_email_list: Union[list, str] = None, context_data: dict = None)`
  Takes a list of recipient email addresses or just a single email address as a string and optionally some context data.
  `recipient_email_list` might be none, because you could set the variable statically in the class definition.


* ``get_context_data()``
  Similar to django CBVs known method, you can extend here the ``context_data`` provided in the `__init__()`.


* ``get_subject()``
  This method combines the constant ``SUBJECT_PREFIX`` with the variable `subject`. Can be overwritten, if required.


* ``get_from_email()``
  Returns the email address the mail should be sent from. Will take the django settings variable ``DEFAULT_FROM_EMAIL``
  if the constant ``FROM_EMAIL`` in the class is not set.


* ``get_reply_to_email()``
  Returns the content of constant ``REPLY_TO_ADDRESS``. If this constant is not set, there will be no "reply-to" data in
  the email.


* ``get_cc_to_email()``
  Returns the content of class variable ``cc_email_list_``. Any email address returned by this method will be used in
  the "CC" field of the generated email. This variable can be set anywhere within the class
  (preferably in the `__init__` method) or this method can be overwritten for custom behaviour.


* ``get_bcc_to_email()``
  Returns the content of class variable ``bcc_email_list_``. Any email address returned by this method will be used in
  the "CC" field of the generated email. This variable can be set anywhere within the class
  (preferably in the `__init__` method) or this method can be overwritten for custom behaviour.


* ``get_translation()``
  Tries to parse the language from the django settings variable ``LANGUAGE_CODE``. Can be overwritten to set a language
  manually. Needs to return either `None` or a two-character language code like `en` or `de`. If this method returns
  `None`, translation will be deactivated. Translations are needed for localised values like getting the current month
  from a date (in the correct language).

* ``get_attachments()``
  This method returns a list of paths to a locally-stored file. Can automatically be filled by passing the kwarg
  `attachment_list` in the constructor. Each file of the given list will be attached to the newly created email.

* ``has_errors()``
  If ``is_valid()`` is called with the keyword argument `raise_exception=False`, the configuration errors are not raised
  but stored internally. This method checks if any errors occurred. If you need the explicit errors, you can fetch them
  via the ``errors`` property.


* ``process()``
  Executes the actual sending. Not recommended to change.

### Create multiple similar emails

Imagine you want to inform a couple of users about something that happened in your system, for example a successful
transaction or a report generated by your application. You would have a very similar mail body except for the salutation
or one or two minor differences. Handling this with the single email class from above feels a little off.

That is why this package provides a mail factory! This factory is a wrapper for creating similar emails and providing
the email class shown above with recipient-specific content.

Look at this example:

``````
class MyFancyMail(BaseEmailService):
    subject = _('I am a great email!')
    template_name = 'email/my_fancy_email.html'


class MyFancyMailFactory(BaseEmailServiceFactory):
    service_class = MyFancyMail

    def __init__(self, action_id: int, recipient_email_list: list = None):
        super().__init__(recipient_email_list)
        self.action = Action.objects.filter(id=action_id).first()

    def get_recipient_list(self) -> list:
        return self.action.fetch_recipients_for_this_action()

    def get_email_from_recipient(self, recipient) -> str:
        if isinstance(recipient, User):
            return recipient.email
        return recipient

    def is_valid(self):
        if not self.action:
            raise EmailServiceConfigError('No action provided.')

        return super().is_valid()

    def get_context_data(self):
        context = super().get_context_data()
        context.update({
            'action': self.action,
        })
        return context
``````

This is only one of many (!) possibilities to handle a case like described above. We pass a custom action id to the
factory and fetch the given action (this might be a project, a report, a record...) and set it to a class attribute.

The ``get_recipient_list()`` method fetches the recipients based on the action we are looking at right now.

Because we might get mixed results (mostly not, but just to show what is possible), we overwrite the method
``get_email_from_recipient()`` to be able to handle simple email addresses as a string or user objects. If you pass only
strings, overwriting this method can be omitted.

We add a sanity check in the ``is_valid()`` method to be sure that nobody tries to create emails like this without an
action being set.

Finally, we add the action to the context data ``get_context_data()`` so the `MyFancyMail()` class can use it.

Now for every recipient an instance of ``MyFancyMail()`` will be created. Now it is no problem, handling the salutation
or any other recipient-specific content within the "real" mail class. Only make sure that the factory provides all the
required data.

### Attachments

If you want to attach a number of files to your emails, you can do this in two ways.

The simple way is passing an absolute file path to the constructor of the service:

````
email_service = MyMailService(
  ...
  attachment_list=[my_file_1, my_file_2]
)
````

If you want to customise the filename or even pass a mimetype, you can do as follows:

````
email_service = MyMailService(
  ...
  attachment_list=[{'filename': 'my_fancy_file.json', 'file': file_content, 'mimetype': 'application/json'}]
)
````

Please note that here the file content, not the file path, needs to be passed to the attachment list. If anything goes
sideways, the service will throw an `EmailServiceAttachmentError` exception.

## Testing emails

If you are curious about how to properly test your emails, have a look at the testing section.
