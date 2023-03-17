# These are custom exceptions used for particular failure cases


class BaseError(Exception):
    pass


class UnsupportedTranslationError(BaseError):
    """
    An exception thrown when handling translations that are not currently supported
    """

    def __init__(self, translation):
        """
        :param translation: Translation code. For example, 'NIV', 'ESV', 'NLT'
        :type translation: str
        """
        super(UnsupportedTranslationError, self).__init__(f'{translation} is an unsupported translation')
        self.translation = translation


class InvalidPassageError(BaseError):
    """
    An exception thrown when processing a non-existent passage (or passage range)
    """

    def __init__(self, book, chapter_from, passage_from, chapter_to, passage_to, translation):
        """
        :param book: Name of the book
        :type book: str
        :param chapter_from: First chapter number to get
        :type chapter_from: int
        :param passage_from: First passage number to get in the first chapter
        :type passage_from: int
        :param chapter_to: Last chapter number to get
        :type chapter_to: int
        :param passage_to: Last passage number to get in the last chapter
        :type passage_to: int
        :param translation: Translation code. For example, 'NIV', 'ESV', 'NLT'
        :type translation: str
        """
        if chapter_from == chapter_to:
            if passage_from == passage_to:
                passage = f'{chapter_from}:{passage_from}'
            else:
                passage = f'{chapter_from}:{passage_from} - {passage_to}'
        else:
            passage = f'{chapter_from}:{passage_from} - {chapter_to}:{passage_to}'
        super(InvalidPassageError, self).__init__(
            f'{book} {passage} is an invalid passage in the {translation} translation')
        self.book = book
        self.chapter_from = chapter_from
        self.passage_from = passage_from
        self.chapter_to = chapter_to
        self.passage_to = passage_to
        self.translation = translation


class InvalidSearchError(BaseError):
    """
    An exception thrown when searching for an invalid passage on the Bible Gateway site
    """

    def __init__(self, url):
        """
        :param url: The URL which contains the invalid search results
        :type url: str
        """
        super(InvalidSearchError, self).__init__(f'Failed to retrieve search results from {url}')
        self.url = url


class TranslationMismatchError(BaseError):
    """
    An exception thrown when using the extractor to read a file, and both use different translations
    """

    def __init__(self, extractor_translation, file_translation):
        """
        :param extractor_translation: Translation code used by the extractor. For example, 'NIV', 'ESV', 'NLT'
        :type extractor_translation: str
        :param file_translation: Translation code used in the file. For example, 'NIV', 'ESV', 'NLT'
        :type file_translation: str
        """
        super(TranslationMismatchError, self).__init__(
            f'The extractor is using the {extractor_translation} translation, '
            f'but attempted to read a file in the {file_translation} translation')
        self.extractor_translation = extractor_translation
        self.file_translation = file_translation
