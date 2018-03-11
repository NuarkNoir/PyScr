import time


class IDbDealer(object):
    def __init__(self, _db):
        self.db = _db

    def put_elements(self, *args, **kwargs):
        pass

    def commit(self):
        pass

    def element_exists(self, *args, **kwargs):
        pass

    def __enter__(self):
        pass

    def __exit__(self, type, value, traceback):
        pass


class LyricsDbDealer(IDbDealer):
    def put_elements(self, Author, Album, Title, Text):
        self.db.put(Author, Album, Title, Text)

    def commit(self):
        self.db.commit()

    def element_exists(self, Author, Title):
        return self.db.find_item(Author, Title)

    def __enter__(self):
        self._startTime = time.time()
        print("Starting DB session")
        self.db.connect()

    def __exit__(self, type, value, traceback):
        self.db.close()
        print("DB session closed. Elapsed time: {:.3f} sec".format(time.time() - self._startTime))


class NozomiDbDealer(IDbDealer):
    def put_elements(self, characters, series, artists, tags, image, postlink):
        self.db.put(characters, series, artists, tags, image, postlink)

    def commit(self):
        self.db.commit()

    def element_exists(self, postlink):
        return self.db.find_item(postlink)

    def __enter__(self):
        self._startTime = time.time()
        print("Starting DB session")
        self.db.connect()

    def __exit__(self, type, value, traceback):
        self.db.close()
        print("DB session closed. Elapsed time: {:.3f} sec".format(time.time() - self._startTime))