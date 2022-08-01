import pymysql
from config import host, user, password, db_name
try:
    connection = pymysql.connect(
        host=host, 
        port=3306, 
        user=user, 
        password=password, 
        database=db_name, 
        cursorclass=pymysql.cursors.DictCursor)
    print('connected')
    print('#' * 28)

# functions that add data to the database
    def add_user(telegram_id):

        with connection.cursor() as cursor:
            user_in_database = '''
            select exists (select id from users where telegram_id = %s) as ex;
            '''

            cursor.execute(user_in_database, (telegram_id))
            inp = cursor.fetchone()['ex']
            if inp == 1:
                print('user in database')
            else:

                add_user = '''
                insert users(telegram_id) values(%s);
                '''
                    
                cursor.execute(add_user, telegram_id)
                connection.commit()
                print('user upload')


    def add_collection(telegram_id, name):

        with connection.cursor() as cursor:
            #add the values into table collection
            add_collection = '''
            insert collection(user_telegram_id, name) values(%s, %s);
            '''
            cursor.execute(add_collection, (telegram_id, name))
            connection.commit()

            print('collection was uploaded into collection')            
            
            #updating table users: adding the id of current collection

            add_collection_into_users = '''
            update users set collection_is_used = (select id from collection where name = %s) where telegram_id = %s;
            '''

            cursor.execute(add_collection_into_users, (name, telegram_id))
            connection.commit()
            print('collection was uploaded into users')


    def add_layer(name, serial_num, get_required, telegram_id):
        with connection.cursor() as cursor:

            cursor.execute('select collection_is_used from users where telegram_id = %s', telegram_id)
            current_collect_id = cursor.fetchone()['collection_is_used']

            add_layer = '''
            insert layer(name, collection_id, user_telegram_id, serial_num, get_required) values(%s, %s, %s, %s, %s);
            '''
            
            cursor.execute(add_layer, (name, current_collect_id, telegram_id, serial_num, get_required))
            connection.commit()
            print('layer was added in table layer')
            
            #updating table users: adding the id of current layer

            add_layer_into_users='''
            update users set layer_is_used_id = (select id from layer where name = %s and collection_id = %s) where telegram_id = %s;
            '''
            cursor.execute(add_layer_into_users, (name, current_collect_id, telegram_id))
            connection.commit()
            print('layer was uploaded into users')


    def add_media(photo, telegram_id):
        with connection.cursor() as cursor:
            cursor.execute('select collection_is_used from users where telegram_id = %s', telegram_id)
            connection.commit()
            collect_id = cursor.fetchone()['collection_is_used']
            

            cursor.execute('select layer_is_used_id from users where telegram_id = %s', telegram_id)
            layer_id = cursor.fetchone()['layer_is_used_id']



            add_media = '''
            insert media(photo, collection_id, user_telegram_id, layer_id) values(%s, %s, %s, %s);
            '''

            cursor.execute(add_media, (photo, collect_id, telegram_id, layer_id))
            connection.commit()
            print('media was uploaded')


    def insert_user(telegram_id, collect_id):
        with connection.cursor() as cursor:
            
            cursor.execute("update users set collection_id = %s where telegram_id = %s", (collect_id, telegram_id))
            connection.commit()
            print('insert was uploaded without errors')

    def change_current_layer(telegram_id, name):
        with connection.cursor() as cursor:
            cursor.execute("select id from layer where name = %s and collection_id = (select collection_is_used from users where telegram_id = %s)", (name, telegram_id))
            layer_id = cursor.fetchone()['id']

            cursor.execute("update users set layer_is_used_id = %s where telegram_id = %s", (layer_id, telegram_id))
            connection.commit()
            print('current layer was changed!')


    def change_serial_number(telegram_id, serial_num):
        with connection.cursor() as cursor:
            cursor.execute('update layer set serial_num = %s where id = (select layer_is_used_id from users where telegram_id = %s)', (serial_num, telegram_id))
            connection.commit()
            print('serial number was changed!')


    def change_required(telegram_id, req):
        with connection.cursor() as cursor:
            cursor.execute('update layer set get_required = %s where id = (select layer_is_used_id from users where telegram_id = %s)', (req, telegram_id))
            connection.commit()
            print('required was changed!')
    
    def delete_layer(telegram_id):
        with connection.cursor() as cursor:
            cursor.execute('delete from media where layer_id = (select layer_is_used_id from users where telegram_id = %s)', telegram_id)
            connection.commit()
            
            cursor.execute('delete from layer where id = (select layer_is_used_id from users where telegram_id = %s)', telegram_id)
            connection.commit()
            print('layer was deleted!')

    def delete_image(photo):
        with connection.cursor() as cursor:
            cursor.execute('delete from media where photo = %s', photo)
            connection.commit()
            print('image was deleted!')

#+-------------------------------------------------+    
#| functions that get data from the database       |
#+-------------------------------------------------+
    def check_exist_collect(telegram_id, name):
        with connection.cursor() as cursor:
            #checking existing collection
            cursor.execute('select exists (select id from collection where name = %s) as ex', name)
            inp = cursor.fetchone()['ex']
            if inp == 1:
                print('collection already exists')
                return 1
            else:
                print('collection is not exist')
                return 0


    def collection_name(telegram_id):
        with connection.cursor() as cursor:
            cursor.execute('select name from collection where id = (select collection_is_used from users where telegram_id = %s);', telegram_id)
        inp = cursor.fetchone()

        for i in inp:
            return inp[i]
     

    def get_info_layer(telegram_id):
        with connection.cursor() as cursor:
            cursor.execute('select serial_num from layer where id = (select layer_is_used_id from users where telegram_id = %s)', telegram_id)
            ser_num = cursor.fetchone()['serial_num']

            cursor.execute('select get_required from layer where id = (select layer_is_used_id from users where telegram_id = %s)', telegram_id)
            req = cursor.fetchone()['get_required']
            if req == 1:
                req = 'Да'
            else:
                req = 'Нет'

            cursor.execute('select count(*) as sum from media where layer_id = (select layer_is_used_id from users where telegram_id = %s)', telegram_id)
            count_img = cursor.fetchone()['sum']

            return {'serial_num': ser_num, 'required': req, 'count_img': count_img}
    

    def get_info_layers(telegram_id):
        with connection.cursor() as cursor:
            cursor.execute('select * from layer where collection_id = (select collection_is_used from users where telegram_id = %s)', telegram_id)
            result = cursor.fetchall()

            return result

    def get_layers(telegram_id, is_dict=False, with_info=False):
        with connection.cursor() as cursor:
            cursor.execute('select name from layer where user_telegram_id = %s and collection_id = (select collection_is_used from users where telegram_id = %s)', (telegram_id, telegram_id))
            inp = cursor.fetchall()
            output = []
            for i in inp:
                output.append(i['name'])
    
            if is_dict == False:
                output = str(output)
                output = output.replace("[", '')
                output = output.replace("'", '')
                output = output.replace(",", '')
                output = output.replace("]", '')
                output = output.replace(' ', '\n')

            if with_info == True:
                result = {}
                for i in output:
                    cursor.execute('select serial_num from layer where id = (select id from layer where name = %s and collection_id = (select collection_is_used from users where telegram_id = %s))', (i, telegram_id))
                    ser_num = cursor.fetchone()['serial_num']

                    cursor.execute('select get_required from layer where id = (select id from layer where name = %s and collection_id = (select collection_is_used from users where telegram_id = %s))', (i, telegram_id))
                    req = cursor.fetchone()['get_required']
                    if req == 1:
                        req = 'Да'
                    else:
                        req = 'Нет'

                    cursor.execute('select count(*) as sum from media where layer_id = (select id from layer where name = %s and collection_id = (select collection_is_used from users where telegram_id = %s))', (i, telegram_id))
                    count_img = cursor.fetchone()['sum']

                    info = {'serial_num': ser_num, 'required': req, 'count_img': count_img}
                    result[i] = info
                output = result

            return output
    
    
    def get_current_layer(telegram_id):
        with connection.cursor() as cursor:
            cursor.execute("select name from layer where id = (select layer_is_used_id from users where telegram_id = %s)", telegram_id)
            inp = cursor.fetchone()
            return inp['name']
    


    def checking_layer_name(telegram_id, name):
        with connection.cursor() as cursor:
            cursor.execute('select exists (select id from layer where name = %s and collection_id = (select collection_is_used from users where telegram_id = %s)) as ex', (name, telegram_id))
            ex = cursor.fetchone()['ex']
            return ex


    def checking_serial_num(telegram_id, serial_num):
        with connection.cursor() as cursor:
            cursor.execute('select exists (select id from layer where serial_num = %s and collection_id = (select collection_is_used from users where telegram_id = %s)) as ex', (serial_num, telegram_id))
            ex = cursor.fetchone()['ex']
            return ex


    def get_images(telegram_id):
        with connection.cursor() as cursor:
            cursor.execute('select photo from media where layer_id = (select layer_is_used_id from users where telegram_id = %s)', telegram_id)
            phtotos = cursor.fetchall()
            output = []
            for i in phtotos:
                output.append(i['photo'])
            return output


    def get_image_info(telegram_id):
        with connection.cursor() as cursor:
            cursor.execute('select collection_is_used from users where telegram_id = %s', telegram_id)
            col_id = cursor.fetchone()['collection_is_used']

            cursor.execute('select id from layer where collection_id = %s', col_id)
            layers_id = cursor.fetchall()

            dict_photos = {}

            for layer in layers_id:
                list_photos = []
                layer_id = layer['id']

                cursor.execute('select photo from media where layer_id = %s', layer_id)
                photos = cursor.fetchall()

                cursor.execute('select name from layer where id = %s', layer_id)
                layer_name = cursor.fetchone()['name']

                for photo in photos:
                    list_photos.append(photo['photo'])
                
                dict_photos[layer_name] = list_photos


            return dict_photos



    def close_db():
        connection.close()

except Exception as ex:
    print('Error')
    print(ex)