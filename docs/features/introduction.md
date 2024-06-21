# Class-based Emails

This package contains an approach called "class-based emails". Similar to class-based views in django (in comparison to
function-based ones), you can now implement your email as a class and use all the benefits of object-orientated
programming like fiddling around with functions and all the non-DRY repetition of code you'll usually end up with.

USPs:

* Better structure and advantages of object-orientated programming over handling multiple functions!
* Quick and fast creation of new emails — only worry about the things you have to think about!
* No code redundancy for setting up the default mail configuration — all wrapped in the class!
* The text part of the email can be automatically rendered from the HTML part — no redundant templates anymore!
* Built-in (and extendable) sanity checks as a validation for forgotten variables!
* Clean and easy solution for email attachments

There are two scenarios covered by this package:

* **Single mail**: Create a single email through a class to utilise benefits of object-orientation.
* **Similar mails**: Create a bunch of similar emails with a factory class, for example if you want to send the same
  content but with a personal salutation to a number of people.

## Create a single email

Imagine you want to send a single email to a given user or to the system admins. Instead of having to deal with how to
end an email and worry about if the ``to`` field requires a list or string of emails... look at this example:

````python
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

````python
from django.conf import settings

email_service = MyFancyClassBasedMail(settings.MY_ADMIN_EMAIL_ADDRESS)
email_service.process()
````

Optionally you can set the class attribute ``template_txt_name`` to define a plain text template. If not set, the HTML
part will be used to render the plain text body.

## Attachments

If you want to attach a number of files to your emails, you can do this in two ways.

The simple way is passing an absolute file path to the constructor of the service:

````python
email_service = MyMailService(
  ...
  attachment_list=[my_file_1, my_file_2]
)
````

If you want to customise the filename or even pass a mimetype, you can do as follows:

````python
email_service = MyMailService(
  ...,
  attachment_list=[{'filename': 'my_fancy_file.json', 'file': file_content, 'mimetype': 'application/json'}],
)
````

Please note that here the file content, not the file path, needs to be passed to the attachment list. If anything goes
sideways, the service will throw an `EmailServiceAttachmentError` exception.

## Async dispatching

A general rule about external APIs is that you shouldn't talk to them in your main thread. You don't have any control
over it, and it might be blocking your application. Therefore, it's wise to use some kind of asynchronous method to send
your emails.

The base class in this package can be used in an async way very simply. Call the process method of your email
inheriting from `BaseEmailService` in, for example, a thread or celery task.

### Python Threads

If you don't want to do this, you can use the `ThreadEmailService` class, which will wrap the sending of your emails in
a simple Python thread.

````python
from django_pony_express.services.asynchronous.thread import ThreadEmailService


class MyThreadBasedEmail(ThreadEmailService):
    pass
````

### Other methods

In the future, we'll add a base class for Celery and maybe django-q / django-q2.
