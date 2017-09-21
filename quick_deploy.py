from bw_clients import account_api, app_name, call_path, message_path
import urllib.parse

#account_api = account.Client(user_id, token, secret)


def check_or_create_application (request, bw_app_id):
    if (bw_app_id != ''):
        print('App already found')
        return bw_app_id
    url_root = request.url_root
    bw_app_name = app_name + ' on ' + url_root
    print('Appname: ' + bw_app_name)
    apps = list(account_api.list_applications(size=1000))
    app_id = search_for_application(apps, bw_app_name)
    if (app_id == False):
        print('Creating application for this url!')
        app_id = account_api.create_application(
            name = bw_app_name,
            incoming_call_url = urllib.parse.urljoin(url_root, call_path),
            incoming_message_url = urllib.parse.urljoin(url_root, message_path))
    else:
        print('App already exists!')
    print('App-id: ' + app_id)
    return app_id

def search_for_application (applications, name):
    for app in applications:
        if (app['name'] == name):
            return app['id']
    return False

def check_or_create_phone_number (bw_app_id, area_code):
    number_list = list(account_api.list_phone_numbers(size=1000,
                                                 application_id = bw_app_id))
    if (len(number_list) == 0):
        number_list = account_api.search_and_order_local_numbers(
                            area_code = area_code, quantity = 1)
        for number in number_list:
            account_api.update_phone_number(number['id'],
                                            application_id=bw_app_id)
    return number_list

