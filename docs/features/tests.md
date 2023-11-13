# Tests

## Unit-testing for mails

### Setup

This package provides a solid and proven way of unit-testing your emails. If you want to build your emails in a robust
way in the first place, read up how in the section "Mailing".

Side note: This part was also published as a
[blog article](https://medium.com/ambient-innovation/thorough-and-reliable-unit-testing-of-emails-in-django-5f34901b1b16)
at Medium.

At first, initialise the class in your testing class. Because the class itself behaves more or less like a singleton you
can do this in the `setupTestData()`. It will be executed only once per test class and — compared to `setUp()` — not for
every test.

````python
from django_pony_express.services.tests import EmailTestService
from django.test import TestCase

class MyTestClass(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.email_test_service = EmailTestService()
````

Now you can use the service in all of your tests. If you know that you want to test emails in several classes, it makes
sense to create a base test class which the other classes inherit from.

### Querying for emails

To provide a djangoesque look-and-feel, our test service can query the mail outbox for certain criteria.

The easiest thing to do is get all emails:

    list_of_emails = self.email_test_service.all()

Maybe you want a specific one? You can filter for a given subject by using
a string or a regular expression. Additionally, you can filter for a recipient,
the to, cc and bcc attributes:

````python
import re

# Get all mails with given subject
my_email = self.email_test_service.filter(subject='Nigerian prince')

# Get all mails with given subject using a regular expression
my_email = self.email_test_service.filter(subject=re.compile('Ni(.*) prince'))

# Get all mails with given to-recipient
my_email = self.email_test_service.filter(to='foo@bar.com')
````

Of course, you can connect filters as well:

````python
my_email = self.email_test_service.filter(
    subject='Nigerian prince',
    to='spambot@bar.com',
    cc='copy@bar.com',
    bcc='blind.copy@bar.com'
)
````

Once you have a queryset of emails — meaning the result of one of the queries above — you can work with it.

You can count the results, especially good for assertions:

````python
# Count the number of results
quantity = self.email_test_service.all().count()
````

Do you need the first or last element in the list?

````python
# Get first item in list
first_mail = self.email_test_service.filter(subject='Nigerian prince').first()

# Get last item in list
last_mail = self.email_test_service.filter(subject='Nigerian prince').last()
````

It is very common that you expect one specific email, and you want to know if your mail queryset contains exactly this
element. So there is a helper function for this, too:

````python
# Returns `True` if the queryset contains exactly one item
self.email_test_service.filter(subject='Nigerian prince').one()
````

If you want to access a specific index, you can access it like a queryset:

````python
# Fetch the second email
self.email_test_service.filter(subject='Nigerian prince')[1]

# Fetch the next-to-last email
self.email_test_service.filter(subject='Nigerian prince')[-2]
````

### Assertion helpers

Usually, there are only a couple of ways you can blackbox-test emails. You want to ensure the subject, recipient or
content functions the way you expect it to be.

That’s why the class provides some shortcuts which wrap the assertion.

1. You want to check for exactly one result?

````python
self.email_test_service.filter(to='foo@bar.com').assert_one()
````

2. Do you want to check the quantity of found emails?

````python
expected_number_of_emails = 1
self.email_test_service.filter(to='foo@bar.com').assert_quantity(expected_number_of_emails)
````

3. Do you want to check the subject?

````python
self.email_test_service.filter(to='foo@bar.com')[0].assert_subject('Reset password')
````

Finally, we have a look at the content of the email. As you probably know, an email object consists of two parts. A
plain-text and an HTML part. To avoid checking two times, the wrapper assert_body_contains() checks in both parts and
fails if the given string is missing in one of them.

4. You want to check if a certain string is included in the body?

````python
self.email_test_service.filter(to='foo@bar.com')[0].assert_body_contains('inheritance')
````

5. Sometimes you want to check if something is NOT part of the body…

````python
self.email_test_service.filter(to='foo@bar.com')[0].assert_body_contains_not('scam')
````

To make your life a little easier and happier, each of these methods takes an optional parameter msg which is passed to
the assertion and will be shown if it goes sideways. Here is an example:

````python
self.email_test_service.filter(to='foo@bar.com')[0].assert_body_contains('inheritance', msg='Missing words!')
````
