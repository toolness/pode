This is an attempt at building a code editor for beginners who are
visually impaired.

## Requirements

```
* Python 3.5
* [virtualenv][]
```

## Quick Start

1. Create a [GitHub app][].
2. Copy `.env.sample` to `.env` and fill it out.
3. Run the following in a terminal session:

   ```
   virtualenv venv

   # On Windows, replace the following line with 'venv\Scripts\activate'.
   source venv/bin/activate

   pip install -r requirements.minimal.txt
   python manage.py runserver
   ```

## Environment Variables

Unlike traditional Django settings, we use environment variables
for configuration to be compliant with [twelve-factor][] apps.

You can define environment variables using your environment, or an `.env` file
in the root directory of the repository.

**Note:** When an environment variable is described as representing a
boolean value, if the variable exists with *any* value (even the empty
string), the boolean is true; otherwise, it's false.

* `DEBUG` is a boolean value that indicates whether debugging is enabled
  (this should always be false in production).

* `SECRET_KEY` is a large random value corresponding to Django's
  [`SECRET_KEY`][] setting. It is automatically set to a known, insecure
  value when `DEBUG` is true.

* `DATABASE_URL` is the URL for the database, as per the
  [DJ-Database-URL schema][].

* `GITHUB_CLIENT_ID` is the client ID of your GitHub app.

* `GITHUB_CLIENT_SECRET` is the client secret of your GitHub app.

* `TEST_WITHOUT_MIGRATIONS` is a boolean value that indicates whether to
  disable migrations when running tests.

[virtualenv]: https://virtualenv.pypa.io/en/stable/installation/
[twelve-factor]: http://12factor.net/
[`SECRET_KEY`]: https://docs.djangoproject.com/en/1.9/ref/settings/#secret-key
[DJ-Database-URL schema]: https://github.com/kennethreitz/dj-database-url#url-schema
[GitHub app]: https://github.com/settings/developers
