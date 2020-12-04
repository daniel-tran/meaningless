# These are custom exceptions used for particular failure cases


class BaseError(Exception):
    pass


class UnsupportedTranslationError(BaseError):
    def __init__(self, translation):
        """
        An exception thrown when handling translations that are not currently supported
        :param translation: Translation code. For example, 'NIV', 'ESV', 'NLT'
        """
        self.translation = translation


class InvalidPassageError(BaseError):
    def __init__(self, book, chapter_from, passage_from, chapter_to, passage_to, translation):
        """
        An exception thrown when processing a non-existent passage (or passage range)
        :param book: Name of the book
        :param chapter_from: First chapter number to get
        :param passage_from: First passage number to get in the first chapter
        :param chapter_to: Last chapter number to get
        :param passage_to: Last passage number to get in the last chapter
        :param translation: Translation code. For example, 'NIV', 'ESV', 'NLT'
        """
        self.book = book
        self.chapter_from = chapter_from
        self.passage_from = passage_from
        self.chapter_to = chapter_to
        self.passage_to = passage_to
        self.translation = translation


class InvalidSearchError(BaseError):
    def __init__(self, search, translation):
        """
        An exception thrown when searching for an invalid passage on the Bible Gateway site
        :param search:  Search string used on the Bible Gateway site
        :param translation: Translation code. For example, 'NIV', 'ESV', 'NLT'
        """
        self.search_string = search
        self.translation = translation
