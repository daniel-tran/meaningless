import multiprocessing
import os
import sys
sys.path.append('../')
from meaningless import YAMLDownloader


def download_book_with_debug_messages(yaml_downloader, book_name):
    """
    Wrapper function for download_book with some extra print messages

    :param yaml_downloader: YAML Downloader object
    :type yaml_downloader: YAMLDownloader
    :param book_name: Name of the book
    :type book_name: str
    """
    print(f'Downloading {book_name}...')
    yaml_downloader.download_book(book_name)
    print(f'Completed download for {book_name}.')


if __name__ == "__main__":
    # Run this section when run as a standalone script. Don't run this part when being imported.
    translation = input('Enter a translation code (this will be converted to UPPERCASE): ').upper()
    output_folder = input('Enter the full directory name where files should be written to: ')
    downloader = YAMLDownloader(translation=translation, default_directory=os.path.join(output_folder, translation),
                                enable_multiprocessing=False)
    books = ['Genesis', 'Exodus', 'Leviticus', 'Numbers', 'Deuteronomy',
             'Joshua', 'Judges', 'Ruth', '1 Samuel', '2 Samuel',
             '1 Kings', '2 Kings', '1 Chronicles', '2 Chronicles', 'Ezra',
             'Nehemiah', 'Esther', 'Job', 'Psalm', 'Proverbs',
             'Ecclesiastes', 'Song of Songs', 'Isaiah', 'Jeremiah', 'Lamentations',
             'Ezekiel', 'Daniel', 'Hosea', 'Joel', 'Amos',
             'Obadiah', 'Jonah', 'Micah', 'Nahum', 'Habakkuk',
             'Zephaniah', 'Haggai', 'Zechariah', 'Malachi', 'Matthew',
             'Mark', 'Luke', 'John', 'Acts', 'Romans',
             '1 Corinthians', '2 Corinthians', 'Galatians', 'Ephesians', 'Philippians',
             'Colossians', '1 Thessalonians', '2 Thessalonians', '1 Timothy', '2 Timothy',
             'Titus', 'Philemon', 'Hebrews', 'James', '1 Peter',
             '2 Peter', '1 John', '2 John', '3 John', 'Jude', 'Revelation']
    params = [(downloader, book) for book in books]

    process_pool = multiprocessing.Pool(6)
    process_pool.starmap(download_book_with_debug_messages, params, 6)
    print(f'Completed download of the following books: {str(books)}')
