import flickrapi
import json


class FlickrClient(object):
    PER_PAGE = 500

    client = None

    def __init__(self):
        credentials = json.load(open('credentials.json'))
        self.client = flickrapi.FlickrAPI(format='parsed-json', **credentials)
        self.authenticate()

    def authenticate(self):
        if not self.client.token_valid(perms='read'):
            self.client.get_request_token(oauth_callback='oob')
            authorize_url = self.client.auth_url(perms='read')
            print("Visit %s to authenticate and type in the verification code below:" % authorize_url)
            verifier = str(input('Verifier code: '))
            self.client.get_access_token(verifier)

    def sets(self, page=1):
        args = {
            'page': str(page),
            'perpage':  str(self.PER_PAGE),
        }
        return self.client.photosets.getList(**args)['photosets']

    def set_photos(self, a_set):
        args = {
            'photoset_id': a_set['id'],
            'extras': ','.join(['url_o', 'tags']),
        }
        return self.client.photosets.getPhotos(**args)['photoset']

    def walk_sets(self):
        current_page = 1
        while True:
            current_sets = self.sets(current_page)
            for a_set in current_sets['photoset']:
                yield a_set
            if current_page * self.PER_PAGE >= int(current_sets['total']):
                break
            current_page += 1

    def walk_set_photos(self, a_set):
        current_page = 1
        while True:
            current_photos = self.set_photos(a_set)
            for photo in current_photos['photo']:
                yield photo
            if current_page * self.PER_PAGE >= int(current_photos['total']):
                break
            current_page += 1

    def walk_photos(self):
        for a_set in self.walk_sets():
            for photo in self.walk_set_photos(a_set):
                yield {
                    'set_info': a_set,
                    'photo': photo,
                }
