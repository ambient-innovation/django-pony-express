# Public method overview

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
