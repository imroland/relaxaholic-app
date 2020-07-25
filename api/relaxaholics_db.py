# DB connection
import psycopg2
from psycopg2 import Error, extras
import json
import requests
from flask import Flask

app = Flask(__name__)

# Route to gather all quotes


@app.route("/quotes", methods=["GET"])
def get_all_quotes():
    try:
        connection = connect_db()
        cursor_categories = connection.cursor()
        cursor_quotes = connection.cursor(
            cursor_factory=psycopg2.extras.RealDictCursor)
        categories_query = (
            " SELECT category_id FROM category WHERE category_type = b'0';"
        )
        cursor_categories.execute(categories_query)
        connection.commit()
        categories_list = cursor_categories.fetchall()
        final_output = {}
        for category_id in categories_list:
            quote_select_query = """SELECT quotes_id, quotes_author, quotes_description, category_id
                                    FROM quotes WHERE category_id = %s;"""
            cursor_quotes.execute(quote_select_query, category_id)
            current_category_quotes = cursor_quotes.fetchall()
            # print(current_category_quotes)

            current_category_query = (
                "SELECT category_info FROM category WHERE category_id = %s;"
            )
            cursor_categories.execute(current_category_query, category_id)
            (category_name,) = cursor_categories.fetchall()[0]
            # print(category_name)

            connection.commit()
            final_output.update({category_name: current_category_quotes})

        print("Successful GET of all quotes.")
        return json.dumps(final_output)

    except (Exception, psycopg2.DatabaseError) as error:
        print("Error while getting quotes table and converting to JSON.", error)

    finally:
        # Closing database connection.
        if connection:
            cursor_quotes.close()
            cursor_categories.close()
            connection.close()


# Route to gather all workouts
@app.route("/workouts", methods=["GET"])
def get_all_workouts():
    try:
        connection = connect_db()
        cursor_categories = connection.cursor()
        cursor_workouts = connection.cursor(
            cursor_factory=psycopg2.extras.RealDictCursor
        )
        categories_query = (
            " SELECT category_id FROM category WHERE category_type = b'1';"
        )
        cursor_categories.execute(categories_query)
        connection.commit()
        categories_list = cursor_categories.fetchall()
        final_output = {}
        for category_id in categories_list:
            workout_select_query = """SELECT * FROM workouts WHERE category_id = %s;"""
            cursor_workouts.execute(workout_select_query, category_id)
            current_category_workouts = cursor_workouts.fetchall()
            # print(current_category_workouts)

            current_category_query = (
                "SELECT category_info FROM category WHERE category_id = %s;"
            )
            cursor_categories.execute(current_category_query, category_id)
            (category_name,) = cursor_categories.fetchall()[0]
            # print(category_name)

            connection.commit()
            final_output.update({category_name: current_category_workouts})

        print("Successful GET of all workouts.")
        return json.dumps(final_output)

    except (Exception, psycopg2.DatabaseError) as error:
        print("Error while getting workouts table and converting to JSON.", error)

    finally:
        # Closing database connection.
        if connection:
            cursor_workouts.close()
            cursor_categories.close()
            connection.close()

# Connect to local db in your computer


def connect_db():
    connection = psycopg2.connect(user = "vzfactvzucjdws",
                          password = "a0513d1fab49878df7d0fb5e06b46d98146421a60f6c9005570e8ced0626de78",
                          host = "ec2-3-213-192-58.compute-1.amazonaws.com",
                          port = "5432",
                          database = "d7s24juph2md9j")
    # connection = psycopg2.connect(user="postgres",
    #                               password="relaxaholics",
    #                               host="localhost",
    #                               port="5432",
    #                               database="postgres")
    return connection

# Create user table


def create_user():
    try:
        connection = connect_db()
        cursor = connection.cursor()
        # user_id UUID NOT NULL PRIMARY KEY
        create_users_table_query = '''CREATE TABLE IF NOT EXISTS users
                  (username TEXT UNIQUE PRIMARY KEY,
                  saved_workout_ids INTEGER[],
                  saved_quote_ids INTEGER[]); '''
        cursor.execute(create_users_table_query)
        connection.commit()
        print("Table user created successfully in PostgreSQL ")

    except (Exception, psycopg2.DatabaseError) as error:
        print("Error while creating user table", error)

    finally:
        # closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            #print("PostgreSQL connection is closed")

# Create category table (category_type = '0' means it belongs to quotes, category_type = '0' means it belongs to workouts)


def create_category():
    try:
        connection = connect_db()
        cursor = connection.cursor()

        create_category_table_query = '''CREATE TABLE IF NOT EXISTS category
                  (category_id BIGSERIAL NOT NULL PRIMARY KEY,
                  category_type BIT(1) NOT NULL,
                  category_info VARCHAR(50) UNIQUE NOT NULL); '''
        cursor.execute(create_category_table_query)
        connection.commit()
        print("Table category created successfully in PostgreSQL ")

    except (Exception, psycopg2.DatabaseError) as error:
        print("Error while creating category table", error)

    finally:
        # closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            #print("PostgreSQL connection is closed")

# Create workouts table


def create_workout():
    try:
        connection = connect_db()
        cursor = connection.cursor()

        create_questions_table_query = '''CREATE TABLE IF NOT EXISTS workouts
                  (workout_id BIGSERIAL NOT NULL PRIMARY KEY,
                  workout_name VARCHAR(50) NOT NULL,
                  image_link_1 TEXT NOT NULL,
                  image_link_2 TEXT NOT NULL,
                  category_id BIGINT REFERENCES category(category_id)); '''
        cursor.execute(create_questions_table_query)
        connection.commit()
        print("Table workouts created successfully in PostgreSQL ")

    except (Exception, psycopg2.DatabaseError) as error:
        print("Error while creating workouts table", error)

    finally:
        # closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            #print("PostgreSQL connection is closed")

# Create quotes table


def create_quote():
    try:
        connection = connect_db()
        cursor = connection.cursor()

        create_answers_table_query = '''CREATE TABLE IF NOT EXISTS quotes
                  (quotes_id BIGSERIAL NOT NULL PRIMARY KEY,
                  quotes_author VARCHAR(50) NOT NULL,
                  quotes_author_profession VARCHAR(50) NOT NULL,
                  quotes_description TEXT NOT NULL,
                  category_id BIGINT REFERENCES category(category_id)); '''
        cursor.execute(create_answers_table_query)
        connection.commit()
        print("Table quotes created successfully in PostgreSQL ")

    except (Exception, psycopg2.DatabaseError) as error:
        print("Error while creating quotes table", error)

    finally:
        # closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            #print("PostgreSQL connection is closed")

# Insert users into users table


def insert_user(username):
    try:
        connection = connect_db()
        cursor = connection.cursor()
        postgres_insert_query = """ INSERT INTO users (username, saved_workout_ids, saved_quote_ids) VALUES (%s, %s, %s)"""
        saved_workout_ids_arr = []
        saved_quote_ids_arr = []
        record_to_insert = (username, saved_workout_ids_arr,
                            saved_quote_ids_arr,)
        cursor.execute(postgres_insert_query, record_to_insert)
        connection.commit()
        count = cursor.rowcount
        print(count, "Record inserted successfully into users table")
    except (Exception, psycopg2.Error) as error:
        if(connection):
            print("Failed to insert record into users table", error)
    finally:
        if(connection):
            cursor.close()
            connection.close()
            #print("PostgreSQL connection is closed")

# Insert workout into workouts table


def insert_workout(workout_name, category_info, image_link_1, image_link_2):
    try:
        connection = connect_db()
        cursor = connection.cursor()

        postgres_insert_query = """ INSERT INTO workouts (workout_id, workout_name, image_link_1, image_link_2, category_id) 
                                    VALUES (DEFAULT, %s, %s, %s, %s)"""
        category_id = get_category_id(category_info, '1')
        record_to_insert = (workout_name, image_link_1,
                            image_link_2, category_id,)
        cursor.execute(postgres_insert_query, record_to_insert)
        connection.commit()
        count = cursor.rowcount
        print(count, "Record inserted successfully into workouts table")
    except (Exception, psycopg2.Error) as error:
        if(connection):
            print("Failed to insert record into workouts table", error)
    finally:
        if(connection):
            cursor.close()
            connection.close()
            #print("PostgreSQL connection is closed")

# Insert quotes into quotes table


def insert_quote(quotes_description, quotes_author, quotes_author_profession, category_info):
    try:
        connection = connect_db()
        cursor = connection.cursor()
        category_id = get_category_id(category_info, '0')
        postgres_insert_query = """ INSERT INTO quotes (quotes_id, quotes_author, quotes_author_profession, quotes_description, category_id) 
                                    VALUES (DEFAULT, %s, %s, %s, %s)"""
        record_to_insert = (
            quotes_author, quotes_author_profession, quotes_description, category_id,)
        cursor.execute(postgres_insert_query, record_to_insert)
        connection.commit()
        count = cursor.rowcount
        print(count, "Record inserted successfully into quotes table")
    except (Exception, psycopg2.Error) as error:
        if(connection):
            print("Failed to insert record into quotes table", error)
    finally:
        if(connection):
            cursor.close()
            connection.close()
            #print("PostgreSQL connection is closed")


# Insert category into category table
def insert_category(category_type, category_info):
    try:
        connection = connect_db()
        cursor = connection.cursor()
        postgres_insert_query = """ INSERT INTO category (category_id, category_type, category_info) VALUES (DEFAULT, %s, %s)"""
        record_to_insert = (category_type, category_info,)
        cursor.execute(postgres_insert_query, record_to_insert)
        connection.commit()
        count = cursor.rowcount
        print(count, "Record inserted successfully into category table")
    except (Exception, psycopg2.Error) as error:
        if(connection):
            print("Failed to insert record into category table", error)
    finally:
        if(connection):
            cursor.close()
            connection.close()
            #print("PostgreSQL connection is closed")

# Get category id from category_info (if category_info does not exist, it will be added into it)


def get_category_id(category_info, category_type):
    try:
        connection = connect_db()
        cursor = connection.cursor()
        postgres_select_query = """ SELECT category_id FROM category WHERE category_info = %s"""
        record_to_select = (category_info,)
        cursor.execute(postgres_select_query, record_to_select)
        result = cursor.fetchall()
        if not result:
            insert_category(category_type, category_info)
            cursor.execute(postgres_select_query, record_to_select)
            return get_category_id(category_info, category_type)
        connection.commit()
        count = cursor.rowcount
        print(count, "Successfully queried category id")
        return result[0]
    except (Exception, psycopg2.Error) as error:
        if(connection):
            print(category_info)
            print("Failed to get category id", error)
    finally:
        if(connection):
            cursor.close()
            connection.close()
            #print("PostgreSQL connection is closed")

# Add a workout in saved_workout_ids of a user in users table


def add_user_workout(username, workout_id):
    try:
        connection = connect_db()
        cursor = connection.cursor()

        postgres_select_query = """ SELECT saved_workout_ids FROM users WHERE username = %s"""
        record_to_select = (username,)
        cursor.execute(postgres_select_query, record_to_select)
        saved_workout_ids_arr = cursor.fetchall()[0][0]

        if not saved_workout_ids_arr:
            saved_workout_ids_arr.append(workout_id)

        for id in saved_workout_ids_arr:
            if workout_id not in saved_workout_ids_arr:
                saved_workout_ids_arr.append(workout_id)

        postgres_update_query = """ UPDATE users SET saved_workout_ids = %s WHERE username = %s"""
        record_to_select = (saved_workout_ids_arr, username,)
        cursor.execute(postgres_update_query, record_to_select)

        connection.commit()
        count = cursor.rowcount
        print(count, "Workout successfully added in users table (saved_workout_ids)")

    except (Exception, psycopg2.Error) as error:
        if(connection):
            print("Failed to update record in users table", error)
    finally:
        if(connection):
            cursor.close()
            connection.close()
            #print("PostgreSQL connection is closed")

# Delete a workout in saved_workout_ids of a user in users table


def delete_user_workout(username, workout_id):
    try:
        connection = connect_db()
        cursor = connection.cursor()

        postgres_select_query = """ SELECT saved_workout_ids FROM users WHERE username = %s"""
        record_to_select = (username,)
        cursor.execute(postgres_select_query, record_to_select)
        saved_workout_ids = cursor.fetchone()[0]
        saved_workout_ids.remove(workout_id)

        postgres_update_query = """ UPDATE users SET saved_workout_ids = %s WHERE username = %s"""
        record_to_select = (saved_workout_ids, username,)
        cursor.execute(postgres_update_query, record_to_select)

        connection.commit()
        count = cursor.rowcount
        print(count, "Workout successfully deleted in users table (saved_workout_ids)")

    except (Exception, psycopg2.Error) as error:
        if(connection):
            print("Failed to update record in users table", error)
    finally:
        if(connection):
            cursor.close()
            connection.close()
            #print("PostgreSQL connection is closed")

# Add a quote in saved_quote_ids of a user in users table


def add_user_quote(username, quote_id):
    try:
        connection = connect_db()
        cursor = connection.cursor()

        postgres_select_query = """ SELECT saved_quote_ids FROM users WHERE username = %s"""
        record_to_select = (username,)
        cursor.execute(postgres_select_query, record_to_select)
        saved_quote_ids = cursor.fetchall()[0][0]

        if not saved_quote_ids:
            saved_quote_ids.append(quote_id)

        for id in saved_quote_ids:
            if quote_id not in saved_quote_ids:
                saved_quote_ids.append(quote_id)

        postgres_update_query = """ UPDATE users SET saved_quote_ids = %s WHERE username = %s"""
        record_to_select = (saved_quote_ids, username,)
        cursor.execute(postgres_update_query, record_to_select)

        connection.commit()
        count = cursor.rowcount
        print(count, "Workout successfully added in users table (saved_quote_ids)")

    except (Exception, psycopg2.Error) as error:
        if(connection):
            print("Failed to update record in users table", error)
    finally:
        if(connection):
            cursor.close()
            connection.close()
            #print("PostgreSQL connection is closed")

# Delete a quote in saved_quote_ids of a user in users table


def delete_user_quote(username, quote_id):
    try:
        connection = connect_db()
        cursor = connection.cursor()

        postgres_select_query = """ SELECT saved_quote_ids FROM users WHERE username = %s"""
        record_to_select = (username,)
        cursor.execute(postgres_select_query, record_to_select)
        saved_quote_ids = cursor.fetchone()[0]
        saved_quote_ids.remove(quote_id)

        postgres_update_query = """ UPDATE users SET saved_quote_ids = %s WHERE username = %s"""
        record_to_select = (saved_quote_ids, username,)
        cursor.execute(postgres_update_query, record_to_select)

        connection.commit()
        count = cursor.rowcount
        print(count, "Workout successfully removed in users table (saved_quote_ids)")

    except (Exception, psycopg2.Error) as error:
        if(connection):
            print("Failed to update record in users table", error)
    finally:
        if(connection):
            cursor.close()
            connection.close()
            #print("PostgreSQL connection is closed")

# Create all the tables


def db_setup():
    create_user()
    create_category()
    create_workout()
    create_quote()

# Testing if user added successfully


def insert_user_test():
    insert_user("Wei Kit")
    insert_user("Roland")

# Testing saved workouts and quotes for users


def modify_user_test2():
    add_user_workout("Wei Kit", 1)
    delete_user_workout("Wei Kit", 1)
    add_user_quote("Wei Kit", 2)
    add_user_quote("Wei Kit", 3)
    delete_user_quote("Wei Kit", 3)

# Insert all quotes


def insert_all_quotes():
    insert_quote('Be yourself; everyone else is already taken.',
                 'Oscar Wilde', 'Irish poet', 'Inspirational')
    insert_quote('Be yourself; everyone else is already taken.',
                 'Oscar Wilde', 'Irish poet', 'Advice')
    insert_quote('Be yourself; everyone else is already taken.',
                 'Oscar Wilde', 'Irish poet', 'Humor')
    insert_quote('To live is the rarest thing in the world. Most people exist, that is all.',
                 'Oscar Wilde', 'Irish poet', 'Philosophy')
    insert_quote('To live is the rarest thing in the world. Most people exist, that is all.',
                 'Oscar Wilde', 'Irish poet', 'Humor')
    insert_quote('True friends stab you in the front.',
                 'Oscar Wilde', 'Irish poet', 'Philosophy')
    insert_quote('True friends stab you in the front.',
                 'Oscar Wilde', 'Irish poet', 'People')
    insert_quote('Women are made to be Loved, not understood.',
                 'Oscar Wilde', 'Irish poet', 'Philosophy')
    insert_quote('Women are made to be Loved, not understood.',
                 'Oscar Wilde', 'Irish poet', 'Humor')
    insert_quote('Be the change that you wish to see in the world.',
                 'Mahatma Gandhi', 'Indian leader', 'Inspirational')
    insert_quote('Be the change that you wish to see in the world.',
                 'Mahatma Gandhi', 'Indian leader', 'Philosophy')
    insert_quote('Be the change that you wish to see in the world.',
                 'Mahatma Gandhi', 'Indian leader', 'Advice')
    insert_quote('Live as if you were to die tomorrow. Learn as if you were to live forever.',
                 'Mahatma Gandhi', 'Indian leader', 'Inspirational')
    insert_quote('Live as if you were to die tomorrow. Learn as if you were to live forever.',
                 'Mahatma Gandhi', 'Indian leader', 'Life')
    insert_quote('Live as if you were to die tomorrow. Learn as if you were to live forever.',
                 'Mahatma Gandhi', 'Indian leader', 'Advice')
    insert_quote('No one can make you feel inferior without your consent.',
                 'Eleanor Roosevelt', 'Former First Lady of the United States', 'Wisdom')
    insert_quote('Great minds discuss ideas; average minds discuss events; small minds discuss people.',
                 'Eleanor Roosevelt', 'Former First Lady of the United States', 'Wisdom')
    insert_quote('Great minds discuss ideas; average minds discuss events; small minds discuss people.',
                 'Eleanor Roosevelt', 'Former First Lady of the United States', 'People')
    insert_quote('Do what you feel in your heart to be right - for you''ll be criticized anyway.',
                 'Eleanor Roosevelt', 'Former First Lady of the United States', 'Wisdom')
    insert_quote('Do what you feel in your heart to be right - for you''ll be criticized anyway.',
                 'Eleanor Roosevelt', 'Former First Lady of the United States', 'Advice')
    insert_quote('Do one thing every day that scares you.', 'Eleanor Roosevelt',
                 'Former First Lady of the United States', 'Wisdom')
    insert_quote('Do one thing every day that scares you.',
                 'Eleanor Roosevelt', 'Former First Lady of the United States', 'Life')
    insert_quote('Darkness cannot drive out darkness: only light can do that. Hate cannot drive out hate; only love can do that.',
                 'Martin Luther King', 'American minister', 'Inspirational')
    insert_quote('Darkness cannot drive out darkness: only light can do that. Hate cannot drive out hate; only love can do that.',
                 'Martin Luther King', 'American minister', 'Wisdom')
    insert_quote('Darkness cannot drive out darkness: only light can do that. Hate cannot drive out hate; only love can do that.',
                 'Martin Luther King', 'American minister', 'Love')
    insert_quote('Our lives begin to end the day we become silent about things that matter.',
                 'Martin Luther King', 'American minister', 'Inspirational')
    insert_quote('Our lives begin to end the day we become silent about things that matter.',
                 'Martin Luther King', 'American minister', 'Life')
    insert_quote('In the end, we will remember not the words of our enemies, but the silence of our friends.',
                 'Martin Luther King', 'American minister', 'People')
    insert_quote('In the end, we will remember not the words of our enemies, but the silence of our friends.',
                 'Martin Luther King', 'American minister', 'Life')
    insert_quote('Injustice anywhere is a threat to justice everywhere.',
                 'Martin Luther King', 'American minister', 'Wisdom')
    insert_quote('The time is always right to do what is right.',
                 'Martin Luther King', 'American minister', 'Inspirational')
    insert_quote('The time is always right to do what is right.',
                 'Martin Luther King', 'American minister', 'Wisdom')
    insert_quote('Life''s most persistent and urgent question is, ''What are you doing for others?',
                 'Martin Luther King', 'American minister', 'Inspirational')
    insert_quote('Life''s most persistent and urgent question is, ''What are you doing for others?',
                 'Martin Luther King', 'American minister', 'Life')
    insert_quote('Life''s most persistent and urgent question is, ''What are you doing for others?',
                 'Martin Luther King', 'American minister', 'People')
    insert_quote('Weak people revenge. Strong people forgive. Intelligent People Ignore.',
                 'Albert Einstein', 'Theoretical physicist', 'Inspirational')
    insert_quote('Weak people revenge. Strong people forgive. Intelligent People Ignore.',
                 'Albert Einstein', 'Theoretical physicist', 'Life')
    insert_quote('I have not failed. I''ve just found 10,000 ways that won''t work.',
                 'Thomas A. Edison', 'American inventor', 'Inspirational')
    insert_quote('Genius is one percent inspiration and ninety-nine percent perspiration.',
                 'Thomas A. Edison', 'American inventor', 'Inspirational')
    insert_quote('Genius is one percent inspiration and ninety-nine percent perspiration.',
                 'Thomas A. Edison', 'American inventor', 'Wisdom')
    insert_quote('Our greatest weakness lies in giving up. The most certain way to succeed is always to try just one more time.',
                 'Thomas A. Edison', 'American inventor', 'Inspirational')
    insert_quote('Our greatest weakness lies in giving up. The most certain way to succeed is always to try just one more time.',
                 'Thomas A. Edison', 'American inventor', 'Advice')
    insert_quote('If we did all the things we are capable of, we would literally astound ourselves.',
                 'Thomas A. Edison', 'American inventor', 'Inspirational')
    insert_quote('Imagination is more important than knowledge. Knowledge is limited. Imagination encircles the world.',
                 'Albert Einstein', 'Theoretical physicist', 'Inspirational')
    insert_quote('Imagination is more important than knowledge. Knowledge is limited. Imagination encircles the world.',
                 'Albert Einstein', 'Theoretical physicist', 'Wisdom')
    insert_quote('Life isn''t about finding yourself. Life is about creating yourself.',
                 'George Bernard Shaw', 'Irish playwright', 'Inspirational')
    insert_quote('Life isn''t about finding yourself. Life is about creating yourself.',
                 'George Bernard Shaw', 'Irish playwright', 'Life')
    insert_quote('Life isn''t about finding yourself. Life is about creating yourself.',
                 'George Bernard Shaw', 'Irish playwright', 'Advice')
    insert_quote('Success is not final, failure is not fatal: it is the courage to continue that counts.',
                 'Winston Churchill', 'Former British Prime Minister', 'Inspirational')
    insert_quote('Success is not final, failure is not fatal: it is the courage to continue that counts.',
                 'Winston Churchill', 'Former British Prime Minister', 'Life')
    insert_quote('Success is not final, failure is not fatal: it is the courage to continue that counts.',
                 'Winston Churchill', 'Former British Prime Minister', 'Advice')
    insert_quote('If you''re going through hell, keep going.',
                 'Winston Churchill', 'Former British Prime Minister', 'Inspirational')
    insert_quote('If you''re going through hell, keep going.',
                 'Winston Churchill', 'Former British Prime Minister', 'Advice')
    insert_quote('We make a living by what we get, but we make a life by what we give.',
                 'Winston Churchill', 'Former British Prime Minister', 'People')
    insert_quote('We make a living by what we get, but we make a life by what we give.',
                 'Winston Churchill', 'Former British Prime Minister', 'Life')
    insert_quote('Peace begins with a smile.', 'Mother Teresa',
                 'Roman Catholic Saint', 'Inspirational')
    insert_quote('Peace begins with a smile.', 'Mother Teresa',
                 'Roman Catholic Saint', 'Wisdom')
    insert_quote('Spread love everywhere you go. Let no one ever come to you without leaving happier.',
                 'Mother Teresa', 'Roman Catholic Saint', 'Inspirational')
    insert_quote('Spread love everywhere you go. Let no one ever come to you without leaving happier.',
                 'Mother Teresa', 'Roman Catholic Saint', 'Love')
    insert_quote('Spread love everywhere you go. Let no one ever come to you without leaving happier.',
                 'Mother Teresa', 'Roman Catholic Saint', 'Advice')
    insert_quote('If you can''t feed a hundred people, then feed just one.',
                 'Mother Teresa', 'Roman Catholic Saint', 'Inspirational')
    insert_quote('If you can''t feed a hundred people, then feed just one.',
                 'Mother Teresa', 'Roman Catholic Saint', 'Advice')
    insert_quote('If you can''t feed a hundred people, then feed just one.',
                 'Mother Teresa', 'Roman Catholic Saint', 'People')
    insert_quote('Kind words can be short and easy to speak, but their echoes are truly endless.',
                 'Mother Teresa', 'Roman Catholic Saint', 'Inspirational')
    insert_quote('Kind words can be short and easy to speak, but their echoes are truly endless.',
                 'Mother Teresa', 'Roman Catholic Saint', 'People')
    insert_quote('Isn''t it nice to think that tomorrow is a new day with no mistakes in it yet?',
                 'L.M. Montgomery', 'Canadian author', 'Inspirational')
    insert_quote('Tomorrow is always fresh, with no mistakes in it.',
                 'L.M. Montgomery', 'Canadian author', 'Inspirational')
    insert_quote('We should regret our mistakes and learn from them, but never carry them forward into the future with us.',
                 'L.M. Montgomery', 'Canadian author', 'Inspirational')
    insert_quote('We should regret our mistakes and learn from them, but never carry them forward into the future with us.',
                 'L.M. Montgomery', 'Canadian author', 'Advice')
    insert_quote('We should regret our mistakes and learn from them, but never carry them forward into the future with us.',
                 'L.M. Montgomery', 'Canadian author', 'Life')
    insert_quote('It''s so easy to be wicked without knowing it, isn''t it?',
                 'L.M. Montgomery', 'Canadian author', 'Inspirational')
    insert_quote('It''s so easy to be wicked without knowing it, isn''t it?',
                 'L.M. Montgomery', 'Canadian author', 'Philosophy')
    insert_quote('It''s so easy to be wicked without knowing it, isn''t it?',
                 'L.M. Montgomery', 'Canadian author', 'Life')
    insert_quote('All the darkness in the world cannot extinguish the light of a single candle.',
                 'Francis of Assisi', 'Italian Catholic Saint', 'Inspirational')
    insert_quote('All the darkness in the world cannot extinguish the light of a single candle.',
                 'Francis of Assisi', 'Italian Catholic Saint', 'Wisdom')
    insert_quote('Start by doing what''s necessary; then do what''s possible; and suddenly you are doing the impossible.',
                 'Francis of Assisi', 'Italian Catholic Saint', 'Inspirational')
    insert_quote('Start by doing what''s necessary; then do what''s possible; and suddenly you are doing the impossible.',
                 'Francis of Assisi', 'Italian Catholic Saint', 'Wisdom')
    insert_quote('Preach the Gospel at all times and when necessary use words.',
                 'Francis of Assisi', 'Italian Catholic Saint', 'Religion')
    insert_quote('Preach the Gospel at all times and when necessary use words.',
                 'Francis of Assisi', 'Italian Catholic Saint', 'Wisdom')
    insert_quote('A single sunbeam is enough to drive away many shadows.',
                 'Francis of Assisi', 'Italian Catholic Saint', 'Inspirational')
    insert_quote('A single sunbeam is enough to drive away many shadows.',
                 'Francis of Assisi', 'Italian Catholic Saint', 'Wisdom')
    insert_quote('You never fail until you stop trying.',
                 'Albert Einstein', 'Theoretical physicist', 'Inspirational')
    insert_quote('You never fail until you stop trying.',
                 'Albert Einstein', 'Theoretical physicist', 'Advice')
    insert_quote('You see things; you say, ''Why?'' But I dream things that never were; and I say ''Why not?',
                 'George Bernard Shaw', 'Irish playwright', 'Inspirational')
    insert_quote('We don''t stop playing because we grow old; we grow old because we stop playing.',
                 'George Bernard Shaw', 'Irish playwright', 'Inspirational')
    insert_quote('Progress is impossible without change, and those who cannot change their minds cannot change anything.',
                 'George Bernard Shaw', 'Irish playwright', 'Inspirational')
    insert_quote('A life spent making mistakes is not only more honorable, but more useful than a life spent doing nothing.',
                 'George Bernard Shaw', 'Irish playwright', 'Inspirational')
    insert_quote('Kindness is a language which the deaf can hear and the blind can see.',
                 'Mark Twain', 'American writer', 'Inspirational')
    insert_quote('The secret of getting ahead is getting started.',
                 'Mark Twain', 'American writer', 'Inspirational')
    insert_quote('The secret of getting ahead is getting started.',
                 'Mark Twain', 'American writer', 'Advice')
    insert_quote('Whenever you find yourself on the side of the majority, it is time to pause and reflect.',
                 'Mark Twain', 'American writer', 'Inspirational')
    insert_quote('Whenever you find yourself on the side of the majority, it is time to pause and reflect.',
                 'Mark Twain', 'American writer', 'Advice')
    insert_quote('The two most important days in your life are the day you are born and the day you find out why.',
                 'Mark Twain', 'American writer', 'Inspirational')
    insert_quote('The two most important days in your life are the day you are born and the day you find out why.',
                 'Mark Twain', 'American writer', 'Life')
    insert_quote('Truth is stranger than fiction, but it is because Fiction is obliged to stick to possibilities; Truth isn''t.',
                 'Mark Twain', 'American writer', 'Inspirational')
    insert_quote('Truth is stranger than fiction, but it is because Fiction is obliged to stick to possibilities; Truth isn''t.',
                 'Mark Twain', 'American writer', 'Life')
    insert_quote('If you tell the truth, you don''t have to remember anything.',
                 'Mark Twain', 'American writer', 'Inspirational')
    insert_quote('If you tell the truth, you don''t have to remember anything.',
                 'Mark Twain', 'American writer', 'Wisdom')
    insert_quote('I have never met a man so ignorant that I couldn''t learn something from him',
                 'Galileo Galilei', 'Italian Polymath', 'Inspirational')
    insert_quote('Earth provides enough to satisfy every man''s needs, but not every man''s greed.',
                 'Mahatma Gandhi', 'Indian leader', 'Inspirational')
    insert_quote('Earth provides enough to satisfy every man''s needs, but not every man''s greed.',
                 'Mahatma Gandhi', 'Indian leader', 'Wisdom')
    insert_quote('Where there is love there is life.',
                 'Mahatma Gandhi', 'Indian leader', 'Life')
    insert_quote('Where there is love there is life.',
                 'Mahatma Gandhi', 'Indian leader', 'Love')
    insert_quote('Happiness is when what you think, what you say, and what you do are in harmony.',
                 'Mahatma Gandhi', 'Indian leader', 'Inspirational')
    insert_quote('Happiness is when what you think, what you say, and what you do are in harmony.',
                 'Mahatma Gandhi', 'Indian leader', 'Wisdom')
    insert_quote('Happiness is when what you think, what you say, and what you do are in harmony.',
                 'Mahatma Gandhi', 'Indian leader', 'Philosophy')
    insert_quote('The weak can never forgive. Forgiveness is the attribute of the strong.',
                 'Mahatma Gandhi', 'Indian leader', 'Inspirational')
    insert_quote('The weak can never forgive. Forgiveness is the attribute of the strong.',
                 'Mahatma Gandhi', 'Indian leader', 'Wisdom')
    insert_quote('The weak can never forgive. Forgiveness is the attribute of the strong.',
                 'Mahatma Gandhi', 'Indian leader', 'Philosophy')
    insert_quote('Strength does not come from physical capacity. It comes from an indomitable will.',
                 'Mahatma Gandhi', 'Indian leader', 'Inspirational')
    insert_quote('Strength does not come from physical capacity. It comes from an indomitable will.',
                 'Mahatma Gandhi', 'Indian leader', 'Wisdom')
    insert_quote('Strength does not come from physical capacity. It comes from an indomitable will.',
                 'Mahatma Gandhi', 'Indian leader', 'Philosophy')
    insert_quote('You must not lose faith in humanity. Humanity is an ocean; if a few drops of the ocean are dirty, the ocean does not become dirty.',
                 'Mahatma Gandhi', 'Indian leader', 'Inspirational')
    insert_quote('You must not lose faith in humanity. Humanity is an ocean; if a few drops of the ocean are dirty, the ocean does not become dirty.',
                 'Mahatma Gandhi', 'Indian leader', 'Wisdom')
    insert_quote('You must not lose faith in humanity. Humanity is an ocean; if a few drops of the ocean are dirty, the ocean does not become dirty.',
                 'Mahatma Gandhi', 'Indian leader', 'Philosophy')
    insert_quote('In a gentle way, you can shake the world.',
                 'Mahatma Gandhi', 'Indian leader', 'Inspirational')
    insert_quote('In a gentle way, you can shake the world.',
                 'Mahatma Gandhi', 'Indian leader', 'Wisdom')
    insert_quote('In a gentle way, you can shake the world.',
                 'Mahatma Gandhi', 'Indian leader', 'Philosophy')
    insert_quote('He that can have patience can have what he will.',
                 'Benjamin Franklin', 'Founding Father of the United States', 'Inspirational')
    insert_quote('He that can have patience can have what he will.',
                 'Benjamin Franklin', 'Founding Father of the United States', 'Wisdom')
    insert_quote('Either write something worth reading or do something worth writing.',
                 'Benjamin Franklin', 'Founding Father of the United States', 'Inspirational')
    insert_quote('Either write something worth reading or do something worth writing.',
                 'Benjamin Franklin', 'Founding Father of the United States', 'Advice')
    insert_quote('Tell me and I forget, teach me and I may remember, involve me and I learn.',
                 'Benjamin Franklin', 'Founding Father of the United States', 'Inspirational')
    insert_quote('Tell me and I forget, teach me and I may remember, involve me and I learn.',
                 'Benjamin Franklin', 'Founding Father of the United States', 'Wisdom')
    insert_quote('Tell me and I forget, teach me and I may remember, involve me and I learn.',
                 'Benjamin Franklin', 'Founding Father of the United States', 'Philosophy')
    insert_quote('Never ruin an apology with an excuse.',
                 'Benjamin Franklin', 'Founding Father of the United States', 'Life')
    insert_quote('Never ruin an apology with an excuse.', 'Benjamin Franklin',
                 'Founding Father of the United States', 'Advice')
    insert_quote('Early to bed and early to rise makes a man healthy, wealthy and wise.',
                 'Benjamin Franklin', 'Founding Father of the United States', 'Life')
    insert_quote('Early to bed and early to rise makes a man healthy, wealthy and wise.',
                 'Benjamin Franklin', 'Founding Father of the United States', 'Advice')
    insert_quote('By failing to prepare, you are preparing to fail.',
                 'Benjamin Franklin', 'Founding Father of the United States', 'Inspirational')
    insert_quote('By failing to prepare, you are preparing to fail.',
                 'Benjamin Franklin', 'Founding Father of the United States', 'Advice')
    insert_quote('Those who look for the bad in people will surely find it.',
                 'Abraham Lincoln', '16th U.S. President', 'Inspirational')
    insert_quote('Those who look for the bad in people will surely find it.',
                 'Abraham Lincoln', '16th U.S. President', 'People')
    insert_quote('People don''t realize how a man''s whole life can be changed by one book.',
                 'Malcolm X', 'American minister', 'Inspirational')
    insert_quote('People don''t realize how a man''s whole life can be changed by one book.',
                 'Malcolm X', 'American minister', 'Life')
    insert_quote('If you have no critics you''ll likely have no success.',
                 'Malcolm X', 'American minister', 'Inspirational')
    insert_quote('If you have no critics you''ll likely have no success.',
                 'Malcolm X', 'American minister', 'Wisdom')
    insert_quote('I''m for truth, no matter who tells it. I''m for justice, no matter who it''s for or against.',
                 'Malcolm X', 'American minister', 'Inspirational')
    insert_quote('I''m for truth, no matter who tells it. I''m for justice, no matter who it''s for or against.',
                 'Malcolm X', 'American minister', 'Wisdom')
    insert_quote('It is not a lack of Love, but a lack of People that makes unhappy marriages.',
                 'Friedrich Nietzsche', 'German philosopher', 'Love')
    insert_quote('It is not a lack of Love, but a lack of People that makes unhappy marriages.',
                 'Friedrich Nietzsche', 'German philosopher', 'Marriage')
    insert_quote('He who has a why to live can bear almost any how.',
                 'Friedrich Nietzsche', 'German philosopher', 'Life')
    insert_quote('He who has a why to live can bear almost any how.',
                 'Friedrich Nietzsche', 'German philosopher', 'Inspirational')
    insert_quote('That which does not kill us makes us stronger',
                 'Friedrich Nietzsche', 'German philosopher', 'Inspirational')
    insert_quote('That which does not kill us makes us stronger',
                 'Friedrich Nietzsche', 'German philosopher', 'Philosophy')
    insert_quote('To live is to suffer, to survive is to find some meaning in the suffering.',
                 'Friedrich Nietzsche', 'German philosopher', 'Life')
    insert_quote('To live is to suffer, to survive is to find some meaning in the suffering.',
                 'Friedrich Nietzsche', 'German philosopher', 'Philosophy')
    insert_quote('To live is to suffer, to survive is to find some meaning in the suffering.',
                 'Friedrich Nietzsche', 'German philosopher', 'Inspirational')
    insert_quote('There is always some madness in love. But there is also always some reason in madness.',
                 'Friedrich Nietzsche', 'German philosopher', 'Philosophy')
    insert_quote('There is always some madness in love. But there is also always some reason in madness.',
                 'Friedrich Nietzsche', 'German philosopher', 'Love')
    insert_quote('No price is too high to pay for the privilege of owning yourself.',
                 'Friedrich Nietzsche', 'German philosopher', 'Philosophy')
    insert_quote('No price is too high to pay for the privilege of owning yourself.',
                 'Friedrich Nietzsche', 'German philosopher', 'Advice')
    insert_quote('You know, when it works, Love is amazing. It''s not overrated.',
                 'Sarah Dessen', 'American novelist', 'Love')
    insert_quote('You know, when it works, Love is amazing. It''s not overrated.',
                 'Sarah Dessen', 'American novelist', 'Life')
    insert_quote('Life is an awful, ugly place to not have a best friend.',
                 'Sarah Dessen', 'American novelist', 'Friends')
    insert_quote('Life is an awful, ugly place to not have a best friend.',
                 'Sarah Dessen', 'American novelist', 'Life')
    insert_quote('There is never a time or place for true love. It happens accidentally, in a heartbeat, in a single flashing, throbbing moment.',
                 'Sarah Dessen', 'American novelist', 'Love')
    insert_quote('There is never a time or place for true love. It happens accidentally, in a heartbeat, in a single flashing, throbbing moment.',
                 'Sarah Dessen', 'American novelist', 'Life')
    insert_quote('Anyone can hide. Facing up to things, working through them, that''s what makes you strong.',
                 'Sarah Dessen', 'American novelist', 'Love')
    insert_quote('Anyone can hide. Facing up to things, working through them, that''s what makes you strong.',
                 'Sarah Dessen', 'American novelist', 'Life')
    insert_quote('If you want to live a happy life, tie it to a goal, not to people or things',
                 'Albert Einstein', 'Theoretical physicist', 'Inspirational')
    insert_quote('If you want to live a happy life, tie it to a goal, not to people or things',
                 'Albert Einstein', 'Theoretical physicist', 'Life')
    insert_quote('Your time is limited, so don’t waste it living someone else’s life.',
                 'Steve Jobs', 'American entrepreneur', 'Inspirational')
    insert_quote('Your time is limited, so don’t waste it living someone else’s life.',
                 'Steve Jobs', 'American entrepreneur', 'Life')
    insert_quote('Your time is limited, so don’t waste it living someone else’s life.',
                 'Steve Jobs', 'American entrepreneur', 'Advice')
    insert_quote('Everything around you that you call life was made up by people, and you can change it.',
                 'Steve Jobs', 'American entrepreneur', 'Inspirational')
    insert_quote('Everything around you that you call life was made up by people, and you can change it.',
                 'Steve Jobs', 'American entrepreneur', 'Life')
    insert_quote('Everything around you that you call life was made up by people, and you can change it.',
                 'Steve Jobs', 'American entrepreneur', 'People')
    insert_quote('Design is not just what it looks like and feels like. Design is how it works.',
                 'Steve Jobs', 'American entrepreneur', 'Inspirational')
    insert_quote('Design is not just what it looks like and feels like. Design is how it works.',
                 'Steve Jobs', 'American entrepreneur', 'Design')
    insert_quote('Innovation distinguishes between a leader and a follower.',
                 'Steve Jobs', 'American entrepreneur', 'Inspirational')
    insert_quote('Innovation distinguishes between a leader and a follower.',
                 'Steve Jobs', 'American entrepreneur', 'Philosophy')
    insert_quote('Sometimes life is going to hit you in the head with a brick. Don''t lose faith.',
                 'Steve Jobs', 'American entrepreneur', 'Faith')
    insert_quote('Sometimes life is going to hit you in the head with a brick. Don''t lose faith.',
                 'Steve Jobs', 'American entrepreneur', 'Advice')
    insert_quote('Sometimes life is going to hit you in the head with a brick. Don''t lose faith.',
                 'Steve Jobs', 'American entrepreneur', 'Life')
    insert_quote('Sometimes when you innovate, you make mistakes. It is best to admit them quickly, and get on with improving your other innovations.',
                 'Steve Jobs', 'American entrepreneur', 'Innovation')
    insert_quote('Sometimes when you innovate, you make mistakes. It is best to admit them quickly, and get on with improving your other innovations.',
                 'Steve Jobs', 'American entrepreneur', 'Advice')
    insert_quote('A lot of times, people don''t know what they want until you show it to them.',
                 'Steve Jobs', 'American entrepreneur', 'People')
    insert_quote('A lot of times, people don''t know what they want until you show it to them.',
                 'Steve Jobs', 'American entrepreneur', 'Philosophy')
    insert_quote('Let’s go invent tomorrow rather than worrying about what happened yesterday.',
                 'Steve Jobs', 'American entrepreneur', 'Innovation')
    insert_quote('Let’s go invent tomorrow rather than worrying about what happened yesterday.',
                 'Steve Jobs', 'American entrepreneur', 'Inspirational')
    insert_quote('The most precious thing that we all have with us is time.',
                 'Steve Jobs', 'American entrepreneur', 'Inspirational')
    insert_quote('The most precious thing that we all have with us is time.',
                 'Steve Jobs', 'American entrepreneur', 'Wisdom')
    insert_quote('You have to trust in something, your gut, destiny, life, karma, whatever.',
                 'Steve Jobs', 'American entrepreneur', 'Inspirational')
    insert_quote('You have to trust in something, your gut, destiny, life, karma, whatever.',
                 'Steve Jobs', 'American entrepreneur', 'Life')
    insert_quote('You have to trust in something, your gut, destiny, life, karma, whatever.',
                 'Steve Jobs', 'American entrepreneur', 'Faith')
    insert_quote('Every child is an artist, the problem is staying an artist when you grow up.',
                 'Pablo Picasso', 'Spanish painter', 'Art')
    insert_quote('Every child is an artist, the problem is staying an artist when you grow up.',
                 'Pablo Picasso', 'Spanish painter', 'Life')
    insert_quote('The purpose of art is washing the dust of daily life off our souls.',
                 'Pablo Picasso', 'Spanish painter', 'Art')
    insert_quote('The purpose of art is washing the dust of daily life off our souls.',
                 'Pablo Picasso', 'Spanish painter', 'Life')
    insert_quote('Good artists copy, great artists steal.',
                 'Pablo Picasso', 'Spanish painter', 'Art')
    insert_quote('Art is a lie that makes us realize truth.',
                 'Pablo Picasso', 'Spanish painter', 'Art')
    insert_quote('Inspiration does exist, but it must find you working.',
                 'Pablo Picasso', 'Spanish painter', 'Art')
    insert_quote('Inspiration does exist, but it must find you working.',
                 'Pablo Picasso', 'Spanish painter', 'Advice')
    insert_quote('Inspiration does exist, but it must find you working.',
                 'Pablo Picasso', 'Spanish painter', 'Inspirational')
    insert_quote('Strive not to be a success, but rather to be of value.',
                 'Albert Einstein', 'Theoretical physicist', 'Inspirational')
    insert_quote('Strive not to be a success, but rather to be of value.',
                 'Albert Einstein', 'Theoretical physicist', 'Life')
    insert_quote('The pessimist sees difficulty in every opportunity. The optimist sees opportunity in every difficulty.',
                 'Winston Churchill', 'Former British Prime Minister', 'Inspirational')
    insert_quote('The pessimist sees difficulty in every opportunity. The optimist sees opportunity in every difficulty.',
                 'Winston Churchill', 'Former British Prime Minister', 'Life')
    insert_quote('We learn wisdom from failure much more than from success.',
                 'Samuel Smiles', 'Scottish Author', 'Inspirational')
    insert_quote('We learn wisdom from failure much more than from success.',
                 'Samuel Smiles', 'Scottish Author', 'Wisdom')
    insert_quote('We learn wisdom from failure much more than from success.',
                 'Samuel Smiles', 'Scottish Author', 'Failure')
    insert_quote('We learn wisdom from failure much more than from success.',
                 'Samuel Smiles', 'Scottish Author', 'Success')
    insert_quote('Hope is like the sun, which, as we journey toward it, casts the shadow of our burden behind us.',
                 'Samuel Smiles', 'Scottish Author', 'Inspirational')
    insert_quote('Hope is like the sun, which, as we journey toward it, casts the shadow of our burden behind us.',
                 'Samuel Smiles', 'Scottish Author', 'Wisdom')
    insert_quote('We often discover what will do, by finding out what will not do; and probably he who never made a mistake never made a discovery.',
                 'Samuel Smiles', 'Scottish Author', 'Inspirational')
    insert_quote('We often discover what will do, by finding out what will not do; and probably he who never made a mistake never made a discovery.',
                 'Samuel Smiles', 'Scottish Author', 'Wisdom')
    insert_quote('We often discover what will do, by finding out what will not do; and probably he who never made a mistake never made a discovery.',
                 'Samuel Smiles', 'Scottish Author', 'Failure')
    insert_quote('Lost wealth may be replaced by industry, lost knowledge by study, lost health by temperance or medicine, but lost time is gone forever.',
                 'Samuel Smiles', 'Scottish Author', 'Inspirational')
    insert_quote('Lost wealth may be replaced by industry, lost knowledge by study, lost health by temperance or medicine, but lost time is gone forever.',
                 'Samuel Smiles', 'Scottish Author', 'Wisdom')
    insert_quote('Lost wealth may be replaced by industry, lost knowledge by study, lost health by temperance or medicine, but lost time is gone forever.',
                 'Samuel Smiles', 'Scottish Author', 'Time')
    insert_quote('Life will always be to a large extent what we ourselves make it.',
                 'Samuel Smiles', 'Scottish Author', 'Inspirational')
    insert_quote('Life will always be to a large extent what we ourselves make it.',
                 'Samuel Smiles', 'Scottish Author', 'Life')
    insert_quote('Enthusiasm... the sustaining power of all great action.',
                 'Samuel Smiles', 'Scottish Author', 'Inspirational')
    insert_quote('Enthusiasm... the sustaining power of all great action.',
                 'Samuel Smiles', 'Scottish Author', 'Life')
    insert_quote('People who are crazy enough to think they can change the world, are the ones who do.',
                 'Winston Churchill', 'Former British Prime Minister', 'Inspirational')
    insert_quote('People who are crazy enough to think they can change the world, are the ones who do.',
                 'Winston Churchill', 'Former British Prime Minister', 'Life')
    insert_quote('People who are crazy enough to think they can change the world, are the ones who do.',
                 'Winston Churchill', 'Former British Prime Minister', 'People')
    insert_quote('The fool doth think he is wise, but the wise man knows himself to be a fool.',
                 'William Shakespeare', 'English poet', 'Wisdom')
    insert_quote('There is nothing either good or bad, but thinking makes it so.',
                 'William Shakespeare', 'English poet', 'Philosophy')
    insert_quote('You''re not to be so blind with patriotism that you can''t face reality. Wrong is wrong, no matter who does it or says it.',
                 'Malcolm X', 'American minister', 'Philosophy')
    insert_quote('Hell is empty and all the devils are here.',
                 'William Shakespeare', 'English poet', 'Philosophy')
    insert_quote('The course of true Love never did run smooth.',
                 'William Shakespeare', 'English poet', 'Love')
    insert_quote('The course of true Love never did run smooth.',
                 'William Shakespeare', 'English poet', 'Wisdom')
    insert_quote('Expectation is the root of all heartache.',
                 'William Shakespeare', 'English poet', 'Philosophy')
    insert_quote('Expectation is the root of all heartache.',
                 'William Shakespeare', 'English poet', 'Wisdom')
    insert_quote('Listen to many, speak to a few.',
                 'William Shakespeare', 'English poet', 'Wisdom')
    insert_quote('Listen to many, speak to a few.',
                 'William Shakespeare', 'English poet', 'Inspirational')
    insert_quote('One may smile, and smile, and be a villain.',
                 'William Shakespeare', 'English poet', 'Philosophy')
    insert_quote('One may smile, and smile, and be a villain.',
                 'William Shakespeare', 'English poet', 'Wisdom')
    insert_quote('Any fool can know. The point is to understand.',
                 'Albert Einstein', 'Theoretical physicist', 'Philosophy')
    insert_quote('Any fool can know. The point is to understand.',
                 'Albert Einstein', 'Theoretical physicist', 'Wisdom')
    insert_quote('Any fool can know. The point is to understand.',
                 'Albert Einstein', 'Theoretical physicist', 'Inspirational')
    insert_quote('It is not that I''m so smart. But I stay with the questions much longer.',
                 'Albert Einstein', 'Theoretical physicist', 'Philosophy')
    insert_quote('It is not that I''m so smart. But I stay with the questions much longer.',
                 'Albert Einstein', 'Theoretical physicist', 'Wisdom')
    insert_quote('It is not that I''m so smart. But I stay with the questions much longer.',
                 'Albert Einstein', 'Theoretical physicist', 'Inspirational')
    insert_quote('Build your own dreams, or someone else will hire you to build theirs.',
                 'Farrah Gray', 'American businessman', 'Wisdom')
    insert_quote('Build your own dreams, or someone else will hire you to build theirs.',
                 'Farrah Gray', 'American businessman', 'Inspirational')
    insert_quote('Build your own dreams, or someone else will hire you to build theirs.',
                 'Farrah Gray', 'American businessman', 'Dream')
    insert_quote('Comfort is the enemy of achievement',
                 'Farrah Gray', 'American businessman', 'Achievement')
    insert_quote('Comfort is the enemy of achievement',
                 'Farrah Gray', 'American businessman', 'Inspirational')
    insert_quote('You know, you don''t have to have money to be a successful businessperson.',
                 'Farrah Gray', 'American businessman', 'Business')
    insert_quote('You know, you don''t have to have money to be a successful businessperson.',
                 'Farrah Gray', 'American businessman', 'Inspirational')
    insert_quote('I can dream alone and strive alone, but true success always requires the help and support of others.',
                 'Farrah Gray', 'American businessman', 'People')
    insert_quote('I can dream alone and strive alone, but true success always requires the help and support of others.',
                 'Farrah Gray', 'American businessman', 'Success')
    insert_quote('I can dream alone and strive alone, but true success always requires the help and support of others.',
                 'Farrah Gray', 'American businessman', 'Dream')
    insert_quote('Success isn’t something that happens overnight: it’s a process.',
                 'Farrah Gray', 'American businessman', 'Business')
    insert_quote('Success isn’t something that happens overnight: it’s a process.',
                 'Farrah Gray', 'American businessman', 'Inspirational')
    insert_quote('Success isn’t something that happens overnight: it’s a process.',
                 'Farrah Gray', 'American businessman', 'Success')
    insert_quote('The more we give, the more we receive. It''s important to give back, because the seeds you plant today, you will harvest tomorrow.',
                 'Farrah Gray', 'American businessman', 'Giving')
    insert_quote('Either you run the day, or the day runs you.',
                 'Jim Rohn', 'American entrepreneur', 'Philosophy')
    insert_quote('Either you run the day, or the day runs you.',
                 'Jim Rohn', 'American entrepreneur', 'Inspirational')
    insert_quote('Start from wherever you are and with whatever you’ve got.',
                 'Jim Rohn', 'American entrepreneur', 'Advice')
    insert_quote('Start from wherever you are and with whatever you’ve got.',
                 'Jim Rohn', 'American entrepreneur', 'Motivational')
    insert_quote('Without constant activity, the threats of life will soon overwhelm the values',
                 'Jim Rohn', 'American entrepreneur', 'Life')
    insert_quote('Without constant activity, the threats of life will soon overwhelm the values',
                 'Jim Rohn', 'American entrepreneur', 'Wisdom')
    insert_quote('If you don’t like how things are, change it! You’re not a tree.',
                 'Jim Rohn', 'American entrepreneur', 'Motivational')
    insert_quote('If you don’t like how things are, change it! You’re not a tree.',
                 'Jim Rohn', 'American entrepreneur', 'Wisdom')
    insert_quote('Success is neither magical nor mysterious. Success is the natural consequence of consistently applying basic fundamentals.',
                 'Jim Rohn', 'American entrepreneur', 'Motivational')
    insert_quote('Success is neither magical nor mysterious. Success is the natural consequence of consistently applying basic fundamentals.',
                 'Jim Rohn', 'American entrepreneur', 'Success')
    insert_quote('How long should you try? Until.', 'Jim Rohn',
                 'American entrepreneur', 'Motivational')
    insert_quote('How long should you try? Until.', 'Jim Rohn',
                 'American entrepreneur', 'Inspirational')
    insert_quote('Focus on making yourself better, not on thinking that you are better.',
                 'Bohdi Sanders', 'Author', 'Inspirational')
    insert_quote('Focus on making yourself better, not on thinking that you are better.',
                 'Bohdi Sanders', 'Author', 'Advice')
    insert_quote('A true friend is someone you can count on no matter what.',
                 'Bohdi Sanders', 'Author', 'Friends')
    insert_quote('A true friend is someone you can count on no matter what.',
                 'Bohdi Sanders', 'Author', 'Wisdom')
    insert_quote('Face your fears and you will be able to conquer them.',
                 'Bohdi Sanders', 'Author', 'Fear')
    insert_quote('Face your fears and you will be able to conquer them.',
                 'Bohdi Sanders', 'Author', 'Advice')
    insert_quote('If you want to know what people believe, don’t read what they write, don’t ask what they believe, just observe what they do.',
                 'Bohdi Sanders', 'Author', 'People')
    insert_quote('If you want to know what people believe, don’t read what they write, don’t ask what they believe, just observe what they do.',
                 'Bohdi Sanders', 'Author', 'Inspirational')
    insert_quote('I used to think I was indecisive, but now I am not quite sure.',
                 'Tommy Cooper', 'British Comedian', 'Humor')
    insert_quote('Police arrested two kids yesterday, one was drinking battery acid, the other was eating fireworks. They charged one and let the other one off.',
                 'Tommy Cooper', 'British Comedian', 'Humor')
    insert_quote('You know, somebody actually complimented me on my driving today. They left a little note on the windscreen, it said ''Parking Fine.''',
                 'Tommy Cooper', 'British Comedian', 'Humor')
    insert_quote('A lie gets halfway around the world before the truth has a chance to get its pants on.',
                 'Winston Churchill', 'Former British Prime Minister', 'Humor')
    insert_quote('A lie gets halfway around the world before the truth has a chance to get its pants on.',
                 'Winston Churchill', 'Former British Prime Minister', 'Life')
    insert_quote('Knowledge is like underwear. It is useful to have it, but not necessary to show it off.',
                 'Bill Murray', 'American actor', 'Humor')
    insert_quote('We are all here on earth to help others; what on earth the others are here for I don''t know.',
                 'Bill Murray', 'American actor', 'Humor')
    insert_quote('Happiness is having a large, loving, caring, close-knit family in another city.',
                 'George Burns', 'American comedian', 'Humor')
    insert_quote('A professor is someone who talks in someone else''s sleep.',
                 'W. H. Auden', 'English-American Poet', 'Humor')
    insert_quote('Everything is changing. People are taking the comedians seriously and the politicians as a joke.',
                 'Will Rogers', 'American actor', 'Humor')
    insert_quote('That’s why they call it the American Dream, because you have to be asleep to believe it.',
                 'George Carlin', 'American comedian', 'Humor')
    insert_quote('If you’re too open-minded; your brains may fall out.',
                 'Lawrence Ferlinghetti', 'American poet', 'Humor')
    insert_quote('If you think nobody cares about you, try missing a couple of payments.',
                 'Steven Wright', 'American stand-up comedian', 'Humor')
    insert_quote('There''s a fine line between fishing and just standing on the shore like an idiot.',
                 'Steven Wright', 'American stand-up comedian', 'Humor')
    insert_quote('If at first you don''t succeed then skydiving definitely isn''t for you.',
                 'Steven Wright', 'American stand-up comedian', 'Humor')
    insert_quote('A lot of people are afraid of heights. Not me, I''m afraid of widths.',
                 'Steven Wright', 'American stand-up comedian', 'Humor')
    insert_quote('What''s another word for Thesaurus?',
                 'Steven Wright', 'American stand-up comedian', 'Humor')
    insert_quote('You can''t have everything. Where would you put it?',
                 'Steven Wright', 'American stand-up comedian', 'Humor')
    insert_quote('Don’t be so humble – you are not that great.',
                 'Golda Meir', 'Former Prime Minister of Israel', 'Humor')
    insert_quote('Whether women are better than men I cannot say - but I can say they are certainly no worse.',
                 'Golda Meir', 'Former Prime Minister of Israel', 'Humor')
    insert_quote('The best way to teach your kids about taxes is by eating 30 percent of their ice cream.',
                 'Bill Murray', 'American actor', 'Humor')
    insert_quote('You can''t soar with the eagles as long as you hang out with the turkeys.',
                 'Joel Osteen', 'American televangelist', 'Philosophy')
    insert_quote('You can''t soar with the eagles as long as you hang out with the turkeys.',
                 'Joel Osteen', 'American televangelist', 'Inspirational')
    insert_quote('You can change your world by changing your words... Remember, death and life are in the power of the tongue.',
                 'Joel Osteen', 'American televangelist', 'Philosophy')
    insert_quote('You can change your world by changing your words... Remember, death and life are in the power of the tongue.',
                 'Joel Osteen', 'American televangelist', 'Life')
    insert_quote('Nothing is impossible, the word itself says ''I''m possible''!',
                 'Audrey Hepburn', 'British actress', 'Humor')
    insert_quote('Nothing is impossible, the word itself says ''I''m possible''!',
                 'Audrey Hepburn', 'British actress', 'Inspirational')
    insert_quote('As you grow older, you will discover that you have two hands, one for helping yourself, the other for helping others.',
                 'Audrey Hepburn', 'British actress', 'People')
    insert_quote('As you grow older, you will discover that you have two hands, one for helping yourself, the other for helping others.',
                 'Audrey Hepburn', 'British actress', 'Inspirational')
    insert_quote('I never think of myself as an icon. What is in other people''s minds is not in my mind. I just do my thing.',
                 'Audrey Hepburn', 'British actress', 'People')
    insert_quote('I never think of myself as an icon. What is in other people''s minds is not in my mind. I just do my thing.',
                 'Audrey Hepburn', 'British actress', 'Inspirational')
    insert_quote('The best thing to hold onto in life is each other.',
                 'Audrey Hepburn', 'British actress', 'People')
    insert_quote('The best thing to hold onto in life is each other.',
                 'Audrey Hepburn', 'British actress', 'Life')
    insert_quote('Be nice to nerds. Chances are you''ll end up working for one.',
                 'Bill Gates', 'American business magnate', 'Humor')
    insert_quote('Be nice to nerds. Chances are you''ll end up working for one.',
                 'Bill Gates', 'American business magnate', 'Advice')
    insert_quote('Your most unhappy customers are your greatest source of learning.',
                 'Bill Gates', 'American business magnate', 'Inspirational')
    insert_quote('Your most unhappy customers are your greatest source of learning.',
                 'Bill Gates', 'American business magnate', 'People')
    insert_quote('Success is a lousy teacher. It seduces smart people into thinking they can''t lose.',
                 'Bill Gates', 'American business magnate', 'Inspirational')
    insert_quote('Success is a lousy teacher. It seduces smart people into thinking they can''t lose.',
                 'Bill Gates', 'American business magnate', 'People')
    insert_quote('Life is not fair; get used to it.', 'Bill Gates',
                 'American business magnate', 'Inspirational')
    insert_quote('Life is not fair; get used to it.',
                 'Bill Gates', 'American business magnate', 'Wisdom')
    insert_quote('If you can''t make it good, at least make it look good.',
                 'Bill Gates', 'American business magnate', 'Inspirational')
    insert_quote('If you can''t make it good, at least make it look good.',
                 'Bill Gates', 'American business magnate', 'Wisdom')
    insert_quote('If you can''t make it good, at least make it look good.',
                 'Bill Gates', 'American business magnate', 'Advice')
    insert_quote('Life is like riding a bicycle. To keep your balance, you must keep moving.',
                 'Albert Einstein', 'Theoretical physicist', 'Life')
    insert_quote('Life is like riding a bicycle. To keep your balance, you must keep moving.',
                 'Albert Einstein', 'Theoretical physicist', 'Inspirational')
    insert_quote('Nearly all men can stand adversity, but if you want to test a man’s character, give him power.',
                 'Abraham Lincoln', '16th U.S. President', 'Philosophy')
    insert_quote('Nearly all men can stand adversity, but if you want to test a man’s character, give him power.',
                 'Abraham Lincoln', '16th U.S. President', 'Wisdom')
    insert_quote('The best way to predict your future is to create it.',
                 'Abraham Lincoln', '16th U.S. President', 'Life')
    insert_quote('The best way to predict your future is to create it.',
                 'Abraham Lincoln', '16th U.S. President', 'Philosophy')
    insert_quote('The best way to predict your future is to create it.',
                 'Abraham Lincoln', '16th U.S. President', 'Wisdom')
    insert_quote('I would rather be a little nobody, then to be a evil somebody.',
                 'Abraham Lincoln', '16th U.S. President', 'Philosophy')
    insert_quote('I would rather be a little nobody, then to be a evil somebody.',
                 'Abraham Lincoln', '16th U.S. President', 'Wisdom')
    insert_quote('I will prepare and some day my chance will come.',
                 'Abraham Lincoln', '16th U.S. President', 'Inspirational')
    insert_quote('I will prepare and some day my chance will come.',
                 'Abraham Lincoln', '16th U.S. President', 'Life')
    insert_quote('Important principles may, and must, be inflexible.',
                 'Abraham Lincoln', '16th U.S. President', 'Philosophy')
    insert_quote('Important principles may, and must, be inflexible.',
                 'Abraham Lincoln', '16th U.S. President', 'Wisdom')
    insert_quote('Important principles may, and must, be inflexible.',
                 'Abraham Lincoln', '16th U.S. President', 'Inspirational')
    insert_quote('Tact is the ability to describe others as they see themselves.',
                 'Abraham Lincoln', '16th U.S. President', 'Philosophy')
    insert_quote('Tact is the ability to describe others as they see themselves.',
                 'Abraham Lincoln', '16th U.S. President', 'Wisdom')
    insert_quote('You cannot escape the responsibility of tomorrow by evading it today.',
                 'Abraham Lincoln', '16th U.S. President', 'Inspirational')
    insert_quote('You cannot escape the responsibility of tomorrow by evading it today.',
                 'Abraham Lincoln', '16th U.S. President', 'Philosophy')
    insert_quote('You cannot escape the responsibility of tomorrow by evading it today.',
                 'Abraham Lincoln', '16th U.S. President', 'Wisdom')
    insert_quote('Knowing thyself, that is the greatest wisdom.',
                 'Galileo Galilei', 'Italian Polymath', 'Inspirational')
    insert_quote('Knowing thyself, that is the greatest wisdom.',
                 'Galileo Galilei', 'Italian Polymath', 'Wisdom')
    insert_quote('To be humane, we must ever be ready to pronounce that wise, ingenious and modest statement ''I do not know''.',
                 'Galileo Galilei', 'Italian Polymath', 'Inspirational')
    insert_quote('To be humane, we must ever be ready to pronounce that wise, ingenious and modest statement ''I do not know''.',
                 'Galileo Galilei', 'Italian Polymath', 'Wisdom')
    insert_quote('Two truths cannot contradict one another.',
                 'Galileo Galilei', 'Italian Polymath', 'Inspirational')
    insert_quote('Two truths cannot contradict one another.',
                 'Galileo Galilei', 'Italian Polymath', 'Wisdom')
    insert_quote('Where the senses fail us, reason must step in.',
                 'Galileo Galilei', 'Italian Polymath', 'Inspirational')
    insert_quote('Where the senses fail us, reason must step in.',
                 'Galileo Galilei', 'Italian Polymath', 'Wisdom')
    insert_quote('All truths are easy to understand once they are discovered; the point is to discover them.',
                 'Galileo Galilei', 'Italian Polymath', 'Inspirational')
    insert_quote('All truths are easy to understand once they are discovered; the point is to discover them.',
                 'Galileo Galilei', 'Italian Polymath', 'Wisdom')

# Insert all workouts


def insert_all_workouts():
    insert_workout('1 Leg Pushup', 'Chest', 'https://www.jefit.com/images/exercises/800_600/4212.jpg',
                   'https://www.jefit.com/images/exercises/800_600/4213.jpg')
    insert_workout('90 90 Hamstring', 'Upper Legs', 'https://www.jefit.com/images/exercises/800_600/1860.jpg',
                   'https://www.jefit.com/images/exercises/800_600/1861.jpg')
    insert_workout('Ab Crunch Machine', 'Abs', 'https://www.jefit.com/images/exercises/800_600/224.jpg',
                   'https://www.jefit.com/images/exercises/800_600/225.jpg')
    insert_workout('Ab Draw Leg Slide', 'Abs', 'https://www.jefit.com/images/exercises/800_600/2680.jpg',
                   'https://www.jefit.com/images/exercises/800_600/2681.jpg')
    insert_workout('Abdominal Pendulum', 'Abs', 'https://www.jefit.com/images/exercises/800_600/3868.jpg',
                   'https://www.jefit.com/images/exercises/800_600/3869.jpg')
    insert_workout('Air Bike', 'Abs', 'https://www.jefit.com/images/exercises/800_600/228.jpg',
                   'https://www.jefit.com/images/exercises/800_600/229.jpg')
    insert_workout('All Fours Squad Stretch', 'Upper Legs', 'https://www.jefit.com/images/exercises/800_600/1856.jpg',
                   'https://www.jefit.com/images/exercises/800_600/1857.jpg')
    insert_workout('Alternate Heel Touchers', 'Abs', 'https://www.jefit.com/images/exercises/800_600/232.jpg',
                   'https://www.jefit.com/images/exercises/800_600/233.jpg')
    insert_workout('Alternate Leg Bridge', 'Abs', 'https://www.jefit.com/images/exercises/800_600/2440.jpg',
                   'https://www.jefit.com/images/exercises/800_600/2441.jpg')
    insert_workout('Alternate Leg Diagonal Bound', 'Upper Legs', 'https://www.jefit.com/images/exercises/800_600/3568.jpg',
                   'https://www.jefit.com/images/exercises/800_600/3569.jpg')
    insert_workout('Alternate Leg Reverse Hyper on Flat Bench', 'Abs',
                   'https://www.jefit.com/images/exercises/800_600/2936.jpg', 'https://www.jefit.com/images/exercises/800_600/2937.jpg')
    insert_workout('Alternate Reach and Catch', 'Abs', 'https://www.jefit.com/images/exercises/800_600/3872.jpg',
                   'https://www.jefit.com/images/exercises/800_600/3873.jpg')
    insert_workout('Alternating Arm Cobra', 'Abs', 'https://www.jefit.com/images/exercises/800_600/2504.jpg',
                   'https://www.jefit.com/images/exercises/800_600/2505.jpg')
    insert_workout('Ankle Circles', 'Lower Legs', 'https://www.jefit.com/images/exercises/800_600/1156.jpg',
                   'https://www.jefit.com/images/exercises/800_600/1157.jpg')
    insert_workout('Ankle On The Knee', 'Glutes', 'https://www.jefit.com/images/exercises/800_600/1536.jpg',
                   'https://www.jefit.com/images/exercises/800_600/1537.jpg')
    insert_workout('Arm Circles', 'Shoulders', 'https://www.jefit.com/images/exercises/800_600/3468.jpg',
                   'https://www.jefit.com/images/exercises/800_600/3469.jpg')
    insert_workout('Back Extension Machine', 'Back', 'https://www.jefit.com/images/exercises/800_600/5036.jpg',
                   'https://www.jefit.com/images/exercises/800_600/5037.jpg')
    insert_workout('Back Extension on Exercise Ball', 'Back', 'https://www.jefit.com/images/exercises/800_600/768.jpg',
                   'https://www.jefit.com/images/exercises/800_600/769.jpg')
    insert_workout('Band Back Fly', 'Triceps', 'https://www.jefit.com/images/exercises/800_600/212.jpg',
                   'https://www.jefit.com/images/exercises/800_600/213.jpg')
    insert_workout('Band Back Flyes', 'Shoulders', 'https://www.jefit.com/images/exercises/800_600/212.jpg',
                   'https://www.jefit.com/images/exercises/800_600/213.jpg')
    insert_workout('Band Bench Press', 'Chest', 'https://www.jefit.com/images/exercises/800_600/1480.jpg',
                   'https://www.jefit.com/images/exercises/800_600/1481.jpg')
    insert_workout('Band Calf Raise', 'Lower Legs', 'https://www.jefit.com/images/exercises/800_600/1576.jpg',
                   'https://www.jefit.com/images/exercises/800_600/1577.jpg')
    insert_workout('Band Calf Raises', 'Lower Legs', 'https://www.jefit.com/images/exercises/800_600/1148.jpg',
                   'https://www.jefit.com/images/exercises/800_600/1149.jpg')
    insert_workout('Band Cross Over', 'Chest', 'https://www.jefit.com/images/exercises/800_600/4.jpg',
                   'https://www.jefit.com/images/exercises/800_600/5.jpg')
    insert_workout('Band Good Morning', 'Upper Legs', 'https://www.jefit.com/images/exercises/800_600/1864.jpg',
                   'https://www.jefit.com/images/exercises/800_600/1865.jpg')
    insert_workout('Band Hip Lift', 'Glutes', 'https://www.jefit.com/images/exercises/800_600/1552.jpg',
                   'https://www.jefit.com/images/exercises/800_600/1553.jpg')
    insert_workout('Band Lateral Raises', 'Shoulders', 'https://www.jefit.com/images/exercises/800_600/1688.jpg',
                   'https://www.jefit.com/images/exercises/800_600/1689.jpg')
    insert_workout('Band Shoulder Press', 'Shoulders', 'https://www.jefit.com/images/exercises/800_600/1780.jpg',
                   'https://www.jefit.com/images/exercises/800_600/1781.jpg')
    insert_workout('Band Back Fly', 'Triceps', 'https://www.jefit.com/images/exercises/800_600/212.jpg',
                   'https://www.jefit.com/images/exercises/800_600/213.jpg')
    insert_workout('Band Back Flyes', 'Shoulders', 'https://www.jefit.com/images/exercises/800_600/212.jpg',
                   'https://www.jefit.com/images/exercises/800_600/213.jpg')
    insert_workout('Band Bench Press', 'Chest', 'https://www.jefit.com/images/exercises/800_600/1480.jpg',
                   'https://www.jefit.com/images/exercises/800_600/1481.jpg')
    insert_workout('Band Calf Raise', 'Lower Legs', 'https://www.jefit.com/images/exercises/800_600/1576.jpg',
                   'https://www.jefit.com/images/exercises/800_600/1577.jpg')
    insert_workout('Band Calf Raises', 'Lower Legs', 'https://www.jefit.com/images/exercises/800_600/1148.jpg',
                   'https://www.jefit.com/images/exercises/800_600/1149.jpg')
    insert_workout('Band Cross Over', 'Chest', 'https://www.jefit.com/images/exercises/800_600/4.jpg',
                   'https://www.jefit.com/images/exercises/800_600/5.jpg')
    insert_workout('Band Good Morning', 'Upper Legs', 'https://www.jefit.com/images/exercises/800_600/1864.jpg',
                   'https://www.jefit.com/images/exercises/800_600/1865.jpg')
    insert_workout('Band Hip Lift', 'Glutes', 'https://www.jefit.com/images/exercises/800_600/1552.jpg',
                   'https://www.jefit.com/images/exercises/800_600/1553.jpg')
    insert_workout('Band Lateral Raises', 'Shoulders', 'https://www.jefit.com/images/exercises/800_600/1688.jpg',
                   'https://www.jefit.com/images/exercises/800_600/1689.jpg')
    insert_workout('Band Shoulder Press', 'Shoulders', 'https://www.jefit.com/images/exercises/800_600/1780.jpg',
                   'https://www.jefit.com/images/exercises/800_600/1781.jpg')
    insert_workout('Band Speed Alternating Biceps Curl', 'Biceps', 'https://www.jefit.com/images/exercises/800_600/1132.jpg',
                   'https://www.jefit.com/images/exercises/800_600/1133.jpg')
    insert_workout('Band Squat', 'Upper Legs', 'https://www.jefit.com/images/exercises/800_600/860.jpg',
                   'https://www.jefit.com/images/exercises/800_600/861.jpg')
    insert_workout('Band Upright Row', 'Shoulders', 'https://www.jefit.com/images/exercises/800_600/740.jpg',
                   'https://www.jefit.com/images/exercises/800_600/741.jpg')
    insert_workout('Band Weighted Sit Up', 'Abs', 'https://www.jefit.com/images/exercises/800_600/1388.jpg',
                   'https://www.jefit.com/images/exercises/800_600/1389.jpg')
    insert_workout('Bands Seated Shoulder Press on Exercise Ball', 'Shoulders',
                   'https://www.jefit.com/images/exercises/800_600/2644.jpg', 'https://www.jefit.com/images/exercises/800_600/2645.jpg')
    insert_workout('Barbell 1/2 Squat', 'Upper Legs', 'https://www.jefit.com/images/exercises/800_600/4884.jpg',
                   'https://www.jefit.com/images/exercises/800_600/4885.jpg')
    insert_workout('Barbell 1/4 Squat', 'Upper Legs', 'https://www.jefit.com/images/exercises/800_600/4808.jpg',
                   'https://www.jefit.com/images/exercises/800_600/4809.jpg')
    insert_workout('Barbell Ab Rollout', 'Abs', 'https://www.jefit.com/images/exercises/800_600/264.jpg',
                   'https://www.jefit.com/images/exercises/800_600/265.jpg')
    insert_workout('Barbell Ab Rollout on Knees', 'Abs', 'https://www.jefit.com/images/exercises/800_600/1176.jpg',
                   'https://www.jefit.com/images/exercises/800_600/1177.jpg')
    insert_workout('Barbell Behind The Back Wrist Curl', 'Forearm',
                   'https://www.jefit.com/images/exercises/800_600/468.jpg', 'https://www.jefit.com/images/exercises/800_600/469.jpg')
    insert_workout('Barbell Behind The Head Military Press', 'Shoulders',
                   'https://www.jefit.com/images/exercises/800_600/3020.jpg', 'https://www.jefit.com/images/exercises/800_600/3021.jpg')
    insert_workout('Barbell Bench Press', 'Chest', 'https://www.jefit.com/images/exercises/800_600/8.jpg',
                   'https://www.jefit.com/images/exercises/800_600/9.jpg')
    insert_workout('Barbell Bent Arm Pullover', 'Back', 'https://www.jefit.com/images/exercises/800_600/1400.jpg',
                   'https://www.jefit.com/images/exercises/800_600/1401.jpg')
    insert_workout('Barbell Bent One Arm Row', 'Back', 'https://www.jefit.com/images/exercises/800_600/1404.jpg',
                   'https://www.jefit.com/images/exercises/800_600/1405.jpg')
    insert_workout('Barbell Bent Over Row', 'Back', 'https://www.jefit.com/images/exercises/800_600/12.jpg',
                   'https://www.jefit.com/images/exercises/800_600/13.jpg')
    insert_workout('Barbell Bent Over Two Arm Row', 'Back', 'https://www.jefit.com/images/exercises/800_600/3228.jpg',
                   'https://www.jefit.com/images/exercises/800_600/3229.jpg')
    insert_workout('Barbell Bicep Curl with Deadlift', 'Biceps', 'https://www.jefit.com/images/exercises/800_600/1136.jpg',
                   'https://www.jefit.com/images/exercises/800_600/1137.jpg')
    insert_workout('Barbell Bicep Drag Curl', 'Biceps', 'https://www.jefit.com/images/exercises/800_600/1456.jpg',
                   'https://www.jefit.com/images/exercises/800_600/1457.jpg')
    insert_workout('Barbell Body Row', 'Biceps', 'https://www.jefit.com/images/exercises/800_600/720.jpg',
                   'https://www.jefit.com/images/exercises/800_600/721.jpg')
    insert_workout('Barbell Bradford Rocky Press', 'Shoulders', 'https://www.jefit.com/images/exercises/800_600/1604.jpg',
                   'https://www.jefit.com/images/exercises/800_600/1605.jpg')
    insert_workout('Barbell Wide Reverse Grip Bench Press', 'Chest',
                   'https://www.jefit.com/images/exercises/800_600/4288.jpg', 'https://www.jefit.com/images/exercises/800_600/4289.jpg')
    insert_workout('Barbell Wide Stance Squat', 'Upper Legs', 'https://www.jefit.com/images/exercises/800_600/872.jpg',
                   'https://www.jefit.com/images/exercises/800_600/873.jpg')
    insert_workout('Barbell Wide Stance Stiff Leg Deadlift', 'Upper Legs',
                   'https://www.jefit.com/images/exercises/800_600/3832.jpg', 'https://www.jefit.com/images/exercises/800_600/3833.jpg')
    insert_workout('Barbell Zercher Squat', 'Upper Legs', 'https://www.jefit.com/images/exercises/800_600/876.jpg',
                   'https://www.jefit.com/images/exercises/800_600/877.jpg')
    insert_workout('Barbell Zercher Squat', 'Upper Legs', 'https://www.jefit.com/images/exercises/800_600/1992.jpg',
                   'https://www.jefit.com/images/exercises/800_600/1993.jpg')
    insert_workout('Behind Head Chest Stretch', 'Chest', 'https://www.jefit.com/images/exercises/800_600/3340.jpg',
                   'https://www.jefit.com/images/exercises/800_600/3341.jpg')
    insert_workout('Bench  Twisting Crunch', 'Abs', 'https://www.jefit.com/images/exercises/800_600/3984.jpg',
                   'https://www.jefit.com/images/exercises/800_600/3985.jpg')
    insert_workout('Bench Dip', 'Triceps', 'https://www.jefit.com/images/exercises/800_600/916.jpg',
                   'https://www.jefit.com/images/exercises/800_600/917.jpg')
    insert_workout('Bench Press Machine', 'Chest', 'https://www.jefit.com/images/exercises/800_600/652.jpg',
                   'https://www.jefit.com/images/exercises/800_600/653.jpg')
    insert_workout('Bench Pushups', 'Chest', 'https://www.jefit.com/images/exercises/800_600/4220.jpg',
                   'https://www.jefit.com/images/exercises/800_600/4221.jpg')
    insert_workout('Bent Knee Hip Raise', 'Abs', 'https://www.jefit.com/images/exercises/800_600/1224.jpg',
                   'https://www.jefit.com/images/exercises/800_600/1225.jpg')
    insert_workout('Bent Knee Hundreds', 'Abs', 'https://www.jefit.com/images/exercises/800_600/2568.jpg',
                   'https://www.jefit.com/images/exercises/800_600/2569.jpg')
    insert_workout('Bent Knee Side Angle Pose', 'Abs', 'https://www.jefit.com/images/exercises/800_600/2008.jpg',
                   'https://www.jefit.com/images/exercises/800_600/2009.jpg')
    insert_workout('Bicep Curl Machine', 'Biceps', 'https://www.jefit.com/images/exercises/800_600/1084.jpg',
                   'https://www.jefit.com/images/exercises/800_600/1085.jpg')
    insert_workout('Boat Pose', 'Abs', 'https://www.jefit.com/images/exercises/800_600/2000.jpg',
                   'https://www.jefit.com/images/exercises/800_600/2001.jpg')
    insert_workout('Bodyweight Lunge', 'Upper Legs', 'https://www.jefit.com/images/exercises/800_600/4860.jpg',
                   'https://www.jefit.com/images/exercises/800_600/4861.jpg')
    insert_workout('Bodyweight Side Lunge', 'Upper Legs', 'https://www.jefit.com/images/exercises/800_600/4880.jpg',
                   'https://www.jefit.com/images/exercises/800_600/4881.jpg')
    insert_workout('Bodyweight Standing Calf Raise', 'Lower Legs', 'https://www.jefit.com/images/exercises/800_600/4908.jpg',
                   'https://www.jefit.com/images/exercises/800_600/4909.jpg')
    insert_workout('Bodyweight Step Up', 'Upper Legs', 'https://www.jefit.com/images/exercises/800_600/4900.jpg',
                   'https://www.jefit.com/images/exercises/800_600/4901.jpg')
    insert_workout('Bodyweight Walking Lunge', 'Upper Legs', 'https://www.jefit.com/images/exercises/800_600/4888.jpg',
                   'https://www.jefit.com/images/exercises/800_600/4889.jpg')
    insert_workout('Bodyweight Wall Squat', 'Upper Legs', 'https://www.jefit.com/images/exercises/800_600/4836.jpg',
                   'https://www.jefit.com/images/exercises/800_600/4837.jpg')
    insert_workout('Bow Pose', 'Abs', 'https://www.jefit.com/images/exercises/800_600/2004.jpg',
                   'https://www.jefit.com/images/exercises/800_600/2005.jpg')
    insert_workout('Box Jump Down with 1 Leg Stabilization', 'Lower Legs',
                   'https://www.jefit.com/images/exercises/800_600/2436.jpg', 'https://www.jefit.com/images/exercises/800_600/2437.jpg')
    insert_workout('Box Jump Multiple Response', 'Upper Legs', 'https://www.jefit.com/images/exercises/800_600/3588.jpg',
                   'https://www.jefit.com/images/exercises/800_600/3589.jpg')
    insert_workout('Bridge', 'Glutes', 'https://www.jefit.com/images/exercises/800_600/776.jpg',
                   'https://www.jefit.com/images/exercises/800_600/777.jpg')
    insert_workout('Butt-Ups', 'Abs', 'https://www.jefit.com/images/exercises/800_600/1308.jpg',
                   'https://www.jefit.com/images/exercises/800_600/1309.jpg')
    insert_workout('Butterfly', 'Chest', 'https://www.jefit.com/images/exercises/800_600/180.jpg',
                   'https://www.jefit.com/images/exercises/800_600/181.jpg')
    insert_workout('C-Curve', 'Abs', 'https://www.jefit.com/images/exercises/800_600/2692.jpg',
                   'https://www.jefit.com/images/exercises/800_600/2693.jpg')
    insert_workout('Cable Back Incline Pushdown', 'Back', 'https://www.jefit.com/images/exercises/800_600/1408.jpg',
                   'https://www.jefit.com/images/exercises/800_600/1409.jpg')
    insert_workout('Cable Bent Over Low Pulley Lateral', 'Shoulders',
                   'https://www.jefit.com/images/exercises/800_600/5112.jpg', 'https://www.jefit.com/images/exercises/800_600/5113.jpg')
    insert_workout('Cable Bent Over Low Pulley Side Lateral', 'Shoulders',
                   'https://www.jefit.com/images/exercises/800_600/76.jpg', 'https://www.jefit.com/images/exercises/800_600/77.jpg')
    insert_workout('Cable Calf Raise', 'Lower Legs', 'https://www.jefit.com/images/exercises/800_600/4912.jpg',
                   'https://www.jefit.com/images/exercises/800_600/4913.jpg')
    insert_workout('Cable Close Grip Curl', 'Biceps', 'https://www.jefit.com/images/exercises/800_600/4060.jpg',
                   'https://www.jefit.com/images/exercises/800_600/4061.jpg')
    insert_workout('Cable Concentration Curl', 'Biceps', 'https://www.jefit.com/images/exercises/800_600/4052.jpg',
                   'https://www.jefit.com/images/exercises/800_600/4053.jpg')
    insert_workout('Cable Cross Over', 'Chest', 'https://www.jefit.com/images/exercises/800_600/56.jpg',
                   'https://www.jefit.com/images/exercises/800_600/57.jpg')
    insert_workout('Cable Crunch', 'Abs', 'https://www.jefit.com/images/exercises/800_600/316.jpg',
                   'https://www.jefit.com/images/exercises/800_600/317.jpg')
    insert_workout('Cable Deadlift', 'Back', 'https://www.jefit.com/images/exercises/800_600/3140.jpg',
                   'https://www.jefit.com/images/exercises/800_600/3141.jpg')
    insert_workout('Cable Decline Chest Fly', 'Chest', 'https://www.jefit.com/images/exercises/800_600/5116.jpg',
                   'https://www.jefit.com/images/exercises/800_600/5117.jpg')
    insert_workout('Cable Decline One Arm Press', 'Chest', 'https://www.jefit.com/images/exercises/800_600/2924.jpg',
                   'https://www.jefit.com/images/exercises/800_600/2925.jpg')
    insert_workout('Cable Decline Press', 'Chest', 'https://www.jefit.com/images/exercises/800_600/2920.jpg',
                   'https://www.jefit.com/images/exercises/800_600/2921.jpg')
    insert_workout('Cable Decline Pullover', 'Shoulders', 'https://www.jefit.com/images/exercises/800_600/3036.jpg',
                   'https://www.jefit.com/images/exercises/800_600/3037.jpg')
    insert_workout('Cable Drag Curl', 'Biceps', 'https://www.jefit.com/images/exercises/800_600/4056.jpg',
                   'https://www.jefit.com/images/exercises/800_600/4057.jpg')
    insert_workout('Cable Elevated Rows', 'Back', 'https://www.jefit.com/images/exercises/800_600/3264.jpg',
                   'https://www.jefit.com/images/exercises/800_600/3265.jpg')
    insert_workout('Cable External Rotation', 'Shoulders', 'https://www.jefit.com/images/exercises/800_600/3492.jpg',
                   'https://www.jefit.com/images/exercises/800_600/3493.jpg')
    insert_workout('Cable Flat Bench Fly', 'Chest', 'https://www.jefit.com/images/exercises/800_600/60.jpg',
                   'https://www.jefit.com/images/exercises/800_600/61.jpg')
    insert_workout('Cable Fly on Exercise Ball', 'Chest', 'https://www.jefit.com/images/exercises/800_600/2460.jpg',
                   'https://www.jefit.com/images/exercises/800_600/2461.jpg')
    insert_workout('Cable Front Raise', 'Shoulders', 'https://www.jefit.com/images/exercises/800_600/64.jpg',
                   'https://www.jefit.com/images/exercises/800_600/65.jpg')
    insert_workout('Cable Full Range of Motion Straight Crossover', 'Back',
                   'https://www.jefit.com/images/exercises/800_600/5168.jpg', 'https://www.jefit.com/images/exercises/800_600/5169.jpg')
    insert_workout('Cable High Cross Over', 'Chest', 'https://www.jefit.com/images/exercises/800_600/56.jpg',
                   'https://www.jefit.com/images/exercises/800_600/57.jpg')
    insert_workout('Decline Bench Knee Raise', 'Abs', 'https://www.jefit.com/images/exercises/800_600/3912.jpg',
                   'https://www.jefit.com/images/exercises/800_600/3913.jpg')
    insert_workout('Dragon Flag', 'Abs', 'https://www.jefit.com/images/exercises/800_600/5256.jpg',
                   'https://www.jefit.com/images/exercises/800_600/5257.jpg')
    insert_workout('Drop Push Up', 'Chest', 'https://www.jefit.com/images/exercises/800_600/3380.jpg',
                   'https://www.jefit.com/images/exercises/800_600/3381.jpg')
    insert_workout('Dumbbell  Seated Front Hammer Raises', 'Shoulders',
                   'https://www.jefit.com/images/exercises/800_600/5288.jpg', 'https://www.jefit.com/images/exercises/800_600/5289.jpg')
    insert_workout('Dumbbell Alternate Bent Over Kickback', 'Triceps',
                   'https://www.jefit.com/images/exercises/800_600/3112.jpg', 'https://www.jefit.com/images/exercises/800_600/3113.jpg')
    insert_workout('Dumbbell Alternate Bent Over Reverse Fly', 'Shoulders',
                   'https://www.jefit.com/images/exercises/800_600/4452.jpg', 'https://www.jefit.com/images/exercises/800_600/4453.jpg')
    insert_workout('Dumbbell Alternate Bicep Curl', 'Biceps', 'https://www.jefit.com/images/exercises/800_600/464.jpg',
                   'https://www.jefit.com/images/exercises/800_600/465.jpg')
    insert_workout('Dumbbell Alternate Hammer Curl', 'Biceps', 'https://www.jefit.com/images/exercises/800_600/456.jpg',
                   'https://www.jefit.com/images/exercises/800_600/457.jpg')
    insert_workout('Dumbbell Alternate Hammer Preacher Curl', 'Biceps',
                   'https://www.jefit.com/images/exercises/800_600/4028.jpg', 'https://www.jefit.com/images/exercises/800_600/4029.jpg')
    insert_workout('Dumbbell Alternate Incline Curl', 'Biceps', 'https://www.jefit.com/images/exercises/800_600/460.jpg',
                   'https://www.jefit.com/images/exercises/800_600/461.jpg')
    insert_workout('Dumbbell Alternate Incline Hammer Curl', 'Biceps',
                   'https://www.jefit.com/images/exercises/800_600/4036.jpg', 'https://www.jefit.com/images/exercises/800_600/4037.jpg')
    insert_workout('Dumbbell Bicep Curl Lunge with Bowling Motion', 'Biceps',
                   'https://www.jefit.com/images/exercises/800_600/1128.jpg', 'https://www.jefit.com/images/exercises/800_600/1129.jpg')
    insert_workout('Dumbbell Bicep Curl on Exercise Ball with Leg Raised', 'Biceps',
                   'https://www.jefit.com/images/exercises/800_600/1124.jpg', 'https://www.jefit.com/images/exercises/800_600/1125.jpg')
    insert_workout('Dumbbell Bicep Curl With Stork Stance', 'Biceps',
                   'https://www.jefit.com/images/exercises/800_600/1160.jpg', 'https://www.jefit.com/images/exercises/800_600/1161.jpg')
    insert_workout('Dumbbell Biceps Curl Reverse', 'Biceps', 'https://www.jefit.com/images/exercises/800_600/1140.jpg',
                   'https://www.jefit.com/images/exercises/800_600/1141.jpg')
    insert_workout('Dumbbell Biceps Curl Squat', 'Biceps', 'https://www.jefit.com/images/exercises/800_600/1144.jpg',
                   'https://www.jefit.com/images/exercises/800_600/1145.jpg')
    insert_workout('Dumbbell Biceps Curl V Sit on Dome', 'Biceps', 'https://www.jefit.com/images/exercises/800_600/1152.jpg',
                   'https://www.jefit.com/images/exercises/800_600/1153.jpg')
    insert_workout('Dumbbell Close Grip Press', 'Triceps', 'https://www.jefit.com/images/exercises/800_600/4664.jpg',
                   'https://www.jefit.com/images/exercises/800_600/4665.jpg')
    insert_workout('Dumbbell Cobra Prone on Exercise Ball', 'Abs', 'https://www.jefit.com/images/exercises/800_600/2492.jpg',
                   'https://www.jefit.com/images/exercises/800_600/2493.jpg')
    insert_workout('Dumbbell Concentration Curls', 'Biceps', 'https://www.jefit.com/images/exercises/800_600/428.jpg',
                   'https://www.jefit.com/images/exercises/800_600/429.jpg')
    insert_workout('Dumbbell Cross Body Hammer Curl', 'Biceps', 'https://www.jefit.com/images/exercises/800_600/392.jpg',
                   'https://www.jefit.com/images/exercises/800_600/393.jpg')
    insert_workout('Dumbbell Incline One Arm Press on Exercise Ball', 'Chest',
                   'https://www.jefit.com/images/exercises/800_600/2904.jpg', 'https://www.jefit.com/images/exercises/800_600/2905.jpg')
    insert_workout('Dumbbell Incline Press on Exercise Ball', 'Chest',
                   'https://www.jefit.com/images/exercises/800_600/2884.jpg', 'https://www.jefit.com/images/exercises/800_600/2885.jpg')
    insert_workout('Dumbbell Incline Press on Exercise Ball', 'Chest',
                   'https://www.jefit.com/images/exercises/800_600/2884.jpg', 'https://www.jefit.com/images/exercises/800_600/2885.jpg')
    insert_workout('Dumbbell Incline Triceps Extension', 'Triceps',
                   'https://www.jefit.com/images/exercises/800_600/1008.jpg', 'https://www.jefit.com/images/exercises/800_600/1009.jpg')
    insert_workout('Dumbbell Incline Two Arm Extension', 'Triceps',
                   'https://www.jefit.com/images/exercises/800_600/4700.jpg', 'https://www.jefit.com/images/exercises/800_600/4701.jpg')
    insert_workout('Dumbbell Iron Cross', 'Upper Legs', 'https://www.jefit.com/images/exercises/800_600/840.jpg',
                   'https://www.jefit.com/images/exercises/800_600/841.jpg')
    insert_workout('Dumbbell Jumping Squat', 'Upper Legs', 'https://www.jefit.com/images/exercises/800_600/4840.jpg',
                   'https://www.jefit.com/images/exercises/800_600/4841.jpg')
    insert_workout('Dumbbell Kickbacks on Exercise Ball', 'Triceps',
                   'https://www.jefit.com/images/exercises/800_600/4672.jpg', 'https://www.jefit.com/images/exercises/800_600/4673.jpg')
    insert_workout('Dumbbell Kneeling Bicep Curl Exercise Ball', 'Biceps',
                   'https://www.jefit.com/images/exercises/800_600/2412.jpg', 'https://www.jefit.com/images/exercises/800_600/2413.jpg')
    insert_workout('Dumbbell Kneeling Lateral Raise on Exercise Ball', 'Shoulders',
                   'https://www.jefit.com/images/exercises/800_600/3016.jpg', 'https://www.jefit.com/images/exercises/800_600/3017.jpg')
    insert_workout('Dumbbell One Arm Seated Reverse Wrist Curl', 'Forearm',
                   'https://www.jefit.com/images/exercises/800_600/1524.jpg', 'https://www.jefit.com/images/exercises/800_600/1525.jpg')
    insert_workout('Dumbbell One Arm Seated Shoulder Press', 'Shoulders',
                   'https://www.jefit.com/images/exercises/800_600/3064.jpg', 'https://www.jefit.com/images/exercises/800_600/3065.jpg')
    insert_workout('Dumbbell One Arm Seated Wrist Curl', 'Forearm',
                   'https://www.jefit.com/images/exercises/800_600/1528.jpg', 'https://www.jefit.com/images/exercises/800_600/1529.jpg')
    insert_workout('Dumbbell One Arm Shoulder Press', 'Shoulders',
                   'https://www.jefit.com/images/exercises/800_600/140.jpg', 'https://www.jefit.com/images/exercises/800_600/141.jpg')
    insert_workout('Dumbbell One Arm Shoulder Press', 'Shoulders',
                   'https://www.jefit.com/images/exercises/800_600/140.jpg', 'https://www.jefit.com/images/exercises/800_600/141.jpg')
    insert_workout('Dumbbell One Arm Shoulder Press on Exercise Ball', 'Shoulders',
                   'https://www.jefit.com/images/exercises/800_600/3072.jpg', 'https://www.jefit.com/images/exercises/800_600/3073.jpg')
    insert_workout('Dumbbell One Arm Side Lateral Raise', 'Shoulders',
                   'https://www.jefit.com/images/exercises/800_600/1748.jpg', 'https://www.jefit.com/images/exercises/800_600/1749.jpg')
    insert_workout('Dumbbell One Arm Standing Arnold Press', 'Shoulders',
                   'https://www.jefit.com/images/exercises/800_600/4520.jpg', 'https://www.jefit.com/images/exercises/800_600/4521.jpg')
    insert_workout('Dumbbell One Arm Standing Curl', 'Biceps', 'https://www.jefit.com/images/exercises/800_600/4100.jpg',
                   'https://www.jefit.com/images/exercises/800_600/4101.jpg')
    insert_workout('Dumbbell One Arm Standing Front Raise', 'Shoulders',
                   'https://www.jefit.com/images/exercises/800_600/4412.jpg', 'https://www.jefit.com/images/exercises/800_600/4413.jpg')
    insert_workout('Exercise Ball Oblique Curl', 'Abs', 'https://www.jefit.com/images/exercises/800_600/2364.jpg',
                   'https://www.jefit.com/images/exercises/800_600/2365.jpg')
    insert_workout('Exercise Ball on the Wall Calf Raise', 'Lower Legs',
                   'https://www.jefit.com/images/exercises/800_600/4916.jpg', 'https://www.jefit.com/images/exercises/800_600/4917.jpg')
    insert_workout('Exercise Ball One Leg Crunch', 'Abs', 'https://www.jefit.com/images/exercises/800_600/2380.jpg',
                   'https://www.jefit.com/images/exercises/800_600/2381.jpg')
    insert_workout('Exercise Ball One Leg Prone Lower Body Rotation', 'Back',
                   'https://www.jefit.com/images/exercises/800_600/2596.jpg', 'https://www.jefit.com/images/exercises/800_600/2597.jpg')
    insert_workout('Exercise Ball One Legged Bridge', 'Abs', 'https://www.jefit.com/images/exercises/800_600/2448.jpg',
                   'https://www.jefit.com/images/exercises/800_600/2449.jpg')
    insert_workout('Exercise Ball One Legged Diagonal Kick Hamstring Curl', 'Glutes',
                   'https://www.jefit.com/images/exercises/800_600/2552.jpg', 'https://www.jefit.com/images/exercises/800_600/2553.jpg')
    insert_workout('Exercise Ball Pike Pushup', 'Chest', 'https://www.jefit.com/images/exercises/800_600/2604.jpg',
                   'https://www.jefit.com/images/exercises/800_600/2605.jpg')
    insert_workout('Exercise Ball Plank With Side Kick', 'Abs', 'https://www.jefit.com/images/exercises/800_600/2528.jpg',
                   'https://www.jefit.com/images/exercises/800_600/2529.jpg')
    insert_workout('Exercise Ball Prone Leg Raise', 'Back', 'https://www.jefit.com/images/exercises/800_600/2588.jpg',
                   'https://www.jefit.com/images/exercises/800_600/2589.jpg')
    insert_workout('Exercise Ball Pull In', 'Abs', 'https://www.jefit.com/images/exercises/800_600/248.jpg',
                   'https://www.jefit.com/images/exercises/800_600/249.jpg')
    insert_workout('Kettlebell Alternating Renegade Row', 'Back', 'https://www.jefit.com/images/exercises/800_600/1396.jpg',
                   'https://www.jefit.com/images/exercises/800_600/1397.jpg')
    insert_workout('Kettlebell Alternating Row', 'Back', 'https://www.jefit.com/images/exercises/800_600/1392.jpg',
                   'https://www.jefit.com/images/exercises/800_600/1393.jpg')
    insert_workout('Kettlebell Arnold Press', 'Shoulders', 'https://www.jefit.com/images/exercises/800_600/1660.jpg',
                   'https://www.jefit.com/images/exercises/800_600/1661.jpg')
    insert_workout('Kettlebell Bent Press', 'Abs', 'https://www.jefit.com/images/exercises/800_600/1304.jpg',
                   'https://www.jefit.com/images/exercises/800_600/1305.jpg')
    insert_workout('Kettlebell Bottoms Up Clean From The Hang Position', 'Forearm',
                   'https://www.jefit.com/images/exercises/800_600/1504.jpg', 'https://www.jefit.com/images/exercises/800_600/1505.jpg')
    insert_workout('Kettlebell Dead Clean', 'Upper Legs', 'https://www.jefit.com/images/exercises/800_600/1920.jpg',
                   'https://www.jefit.com/images/exercises/800_600/1921.jpg')
    insert_workout('Kettlebell Double Alternating Hang Clean', 'Shoulders',
                   'https://www.jefit.com/images/exercises/800_600/1580.jpg', 'https://www.jefit.com/images/exercises/800_600/1580.jpg')
    insert_workout('Kettlebell Double Jerk', 'Shoulders', 'https://www.jefit.com/images/exercises/800_600/1624.jpg',
                   'https://www.jefit.com/images/exercises/800_600/1625.jpg')
    insert_workout('Kettlebell Double Push Press', 'Shoulders', 'https://www.jefit.com/images/exercises/800_600/1628.jpg',
                   'https://www.jefit.com/images/exercises/800_600/1629.jpg')
    insert_workout('Kettlebell Double Snatch', 'Shoulders', 'https://www.jefit.com/images/exercises/800_600/1632.jpg',
                   'https://www.jefit.com/images/exercises/800_600/1633.jpg')
    insert_workout('Scissor Kick', 'Abs', 'https://www.jefit.com/images/exercises/800_600/1360.jpg',
                   'https://www.jefit.com/images/exercises/800_600/1361.jpg')
    insert_workout('Scissors Jump', 'Upper Legs', 'https://www.jefit.com/images/exercises/800_600/3716.jpg',
                   'https://www.jefit.com/images/exercises/800_600/3717.jpg')
    insert_workout('Scorpion', 'Abs', 'https://www.jefit.com/images/exercises/800_600/2100.jpg',
                   'https://www.jefit.com/images/exercises/800_600/2101.jpg')
    insert_workout('Seated Calf Raise', 'Lower Legs', 'https://www.jefit.com/images/exercises/800_600/576.jpg',
                   'https://www.jefit.com/images/exercises/800_600/577.jpg')
    insert_workout('Seated Calf Stretch', 'Lower Legs', 'https://www.jefit.com/images/exercises/800_600/3852.jpg',
                   'https://www.jefit.com/images/exercises/800_600/3853.jpg')
    insert_workout('Seated Flat Bench Leg Pull In', 'Abs', 'https://www.jefit.com/images/exercises/800_600/1368.jpg',
                   'https://www.jefit.com/images/exercises/800_600/1369.jpg')
    insert_workout('Seated Floor Hamstring Stretch', 'Upper Legs', 'https://www.jefit.com/images/exercises/800_600/3720.jpg',
                   'https://www.jefit.com/images/exercises/800_600/3721.jpg')
    insert_workout('Seated Glute', 'Glutes', 'https://www.jefit.com/images/exercises/800_600/3456.jpg',
                   'https://www.jefit.com/images/exercises/800_600/3457.jpg')
    insert_workout('Seated Hamstring and Calf Stretch', 'Upper Legs',
                   'https://www.jefit.com/images/exercises/800_600/3728.jpg', 'https://www.jefit.com/images/exercises/800_600/3729.jpg')
    insert_workout('Seated Hamstring Stretch', 'Upper Legs', 'https://www.jefit.com/images/exercises/800_600/3724.jpg',
                   'https://www.jefit.com/images/exercises/800_600/3725.jpg')


def main():
    db_setup()
    insert_user_test()
    insert_all_quotes()
    insert_all_workouts()


if __name__ == '__main__':
    # main()
    app.run(debug=True)
