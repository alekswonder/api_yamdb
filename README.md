# Team project "YaMDb":

### Description
This project collects reviews of different content and represented by API interface.
Content divided by categories like "Books", "Movies", "Music". 
List of categories is extensible for staff. 
There is people(users) who want to compliment either critic by leaving a review with a mark (1..10 number);
Rating - is average mark, created by summing each mark and divided by number of users, who reviewed concrete content.
Also, users can make comments to others reviews.

### Tech
- Python 3.9
- Django 3.2
- DjangoRestFramework 3.12.4
- PyJWT 2.1.0

## Installation
#### Create and activate Virtual Environment:

```
python3 -m venv venv (Linux/macOS) | python -m venv venv (Windows)
```

* If you have Linux/macOS:

    ```
    source venv/bin/activate
    ```

* Or if you have Windows:

    ```
    source venv/scripts/activate
    ```

#### Upgrade pip:

```
python3 -m pip install --upgrade pip (Linux/macOS) | python -m pip install --upgrade pip (Windows)
```

#### Install dependencies from requirements.txt:

```
pip install -r requirements.txt
```

#### Make migrations:

```
python3 manage.py migrate | python manage.py migrate
```

#### Start project:

```
python3 manage.py runserver | python manage.py runserver
```

## Request for API examples

#### View all posts:

###### GET:

```
TODO: ...
```

###### RESPONSE:

```
{
    TODO: ...
}
```

### Team:
- Kakovka Nikita 
- Nepein Alexander
- Prud Andrew

### License
MIT