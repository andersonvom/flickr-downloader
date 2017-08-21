import flickrapi
import json

from .error_handler import handle


class FlickrClient(object):
    PER_PAGE = 500

    client = None
    photo_attrs = [
        'date_taken',
        'date_upload',
        'last_update',
        'media',
        'tags',
        'url_o',
    ]

    def __init__(self):
        credentials = json.load(open('credentials.json'))
        self.client = flickrapi.FlickrAPI(format='parsed-json', **credentials['flickr'])
        print("Authenticating")
        self.authenticate()

    def authenticate(self):
        print("Verifying token...")
        if not self.client.token_valid(perms='write'):
            print("Token not valid. Creating new one...")
            self.client.get_request_token(oauth_callback='oob')
            authorize_url = self.client.auth_url(perms='write')
            print("Visit %s to authenticate and type in the verification code below:" % authorize_url)
            verifier = str(input('Verifier code: '))
            self.client.get_access_token(verifier)

    def sets(self, page=1):
        args = {
            'page': str(page),
            'perpage':  str(self.PER_PAGE),
        }
        return handle(self.client.photosets.getList, **args)['photosets']

    def set_photos(self, a_set, page=1):
        args = {
            'page': str(page),
            'photoset_id': a_set['id'],
            'extras': ','.join(self.photo_attrs),
        }
        return handle(self.client.photosets.getPhotos, **args)['photoset']

    def get_sizes(self, photo_id):
        return handle(self.client.photos.getSizes, photo_id=photo_id)['sizes']

    def get_video_url(self, photo):
        sizes = self.get_sizes(photo['id'])
        for size in sizes['size']:
            if size['label'] == 'Video Original':
                return size['source']
        return 'ERROR-NoVideoURL'

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
            current_photos = self.set_photos(a_set, current_page)
            for photo in current_photos['photo']:
                if photo['media'] == 'video':
                    photo['url_o'] = self.get_video_url(photo)
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
