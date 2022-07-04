import multiprocessing
import os
import sys
sys.path.append('../')
from meaningless import WebExtractor, YAMLDownloader, yaml_file_interface


def write_baseline(folder, translation, search, index):
    """
    Writes a file to a specific folder containing the contents of a given passage from the Bible Gateway site.
    Files are prefixed with 'passage_baseline_'

    :param folder: Output directory where the passage is written to
    :type folder: str
    :param translation: Translation code. For example, 'NIV', 'ESV', 'NLT'
    :type translation: str
    :param search: Text to search for on the Bible Gateway site
    :type search: str
    :param index: The baseline index, appended to the end of the file name
    :type index: int
    """
    bible = WebExtractor(translation=translation)
    baseline_folder = '{0}/{1}/'.format(folder, translation)
    if not os.path.exists(baseline_folder):
        os.makedirs(baseline_folder, exist_ok=True)
    baseline_file = '{0}/passage_baseline_{1}.txt'.format(baseline_folder, index)
    with open(baseline_file, 'w', encoding='utf-8') as destination:
        result = bible.search(search)
        print(result)
        destination.write(result)


def write_passage(folder, translation, book, chapter, passage):
    """
    Writes a file to a specific folder containing the contents of a given passage.
    This requires a YAML file of the book to be available in the same folder.

    :param folder: Output directory where the passage is written to
    :type folder: str
    :param translation: Translation code. For example, 'NIV', 'ESV', 'NLT'
    :type translation: str
    :param book: Name of the book
    :type book: str
    :param chapter: Chapter number
    :type chapter: int
    :param passage: Passage number
    :type passage: int
    """
    passage_file = '{0}/{1}/passage_{2}_{3}_{4}.txt'.format(folder, translation, book, chapter, passage)
    with open(passage_file, 'w', encoding='utf-8') as destination:
        book_file_path = '{0}/{1}/{2}.yaml'.format(folder, translation, book)
        result = yaml_file_interface.read(book_file_path)[book][chapter][passage].strip()
        print(result)
        destination.write(result)


if __name__ == "__main__":
    # Run this section when run as a standalone script. Don't run this part when being imported.
    download_translation = input('Enter a translation code (this will be converted to UPPERCASE): ').upper()
    output_folder = input('Enter the full directory name where files should be written to: ')
    # Remove stage numbers to skip over them
    stages = [1, 2, 3, 4]

    continue_message = 'Strike the Enter or Return key to continue.'
    input('Stage 1: Test data for baseline passages. {0}'.format(continue_message))
    if 1 in stages:
        write_baseline(output_folder, download_translation, 'Revelation 21:25', 0)
        write_baseline(output_folder, download_translation, 'Matthew 1:1 - 3', 1)
        write_baseline(output_folder, download_translation, 'Nehemiah 7:40 - 42', 2)
        write_baseline(output_folder, download_translation, 'Psalm 32:4', 3)
        write_baseline(output_folder, download_translation, 'John 7:53', 4)
        write_baseline(output_folder, download_translation, 'Psalm 83', 5)
    input('Stage 1 completed. {0}'.format(continue_message))

    input('Stage 2: Intermediate data for download book tests. {0}'.format(continue_message))
    books_with_omissions = ['Matthew', 'Mark', 'Luke', 'John', 'Acts', 'Romans']
    if 2 in stages:
        print('Note: This should only take about 1 - 2 minutes to complete with a decent Internet connection.')
        downloader = YAMLDownloader(translation=download_translation)
        downloader.default_directory = '{0}/{1}/'.format(output_folder, download_translation)
        downloader.enable_multiprocessing = False

        process_pool = multiprocessing.Pool(len(books_with_omissions))
        process_pool.map(downloader.download_book, books_with_omissions)
    input('Stage 2 completed. {0}'.format(continue_message))

    input('Stage 3: Test data for omitted passages. {0}'.format(continue_message))
    if 3 in stages:
        print('----------------- Matthew -----------------')
        book_to_process = 'Matthew'
        write_passage(output_folder, download_translation, book_to_process, 9, 34)
        write_passage(output_folder, download_translation, book_to_process, 12, 47)
        write_passage(output_folder, download_translation, book_to_process, 17, 21)
        write_passage(output_folder, download_translation, book_to_process, 18, 11)
        write_passage(output_folder, download_translation, book_to_process, 21, 44)
        write_passage(output_folder, download_translation, book_to_process, 23, 14)
        print('----------------- Mark -----------------')
        book_to_process = 'Mark'
        write_passage(output_folder, download_translation, book_to_process, 7, 16)
        write_passage(output_folder, download_translation, book_to_process, 9, 44)
        write_passage(output_folder, download_translation, book_to_process, 9, 46)
        write_passage(output_folder, download_translation, book_to_process, 11, 26)
        write_passage(output_folder, download_translation, book_to_process, 15, 28)
        write_passage(output_folder, download_translation, book_to_process, 16, 9)
        write_passage(output_folder, download_translation, book_to_process, 16, 20)
        print('----------------- Luke -----------------')
        book_to_process = 'Luke'
        write_passage(output_folder, download_translation, book_to_process, 17, 36)
        write_passage(output_folder, download_translation, book_to_process, 22, 20)
        write_passage(output_folder, download_translation, book_to_process, 22, 43)
        write_passage(output_folder, download_translation, book_to_process, 22, 44)
        write_passage(output_folder, download_translation, book_to_process, 23, 17)
        write_passage(output_folder, download_translation, book_to_process, 24, 12)
        write_passage(output_folder, download_translation, book_to_process, 24, 40)
        print('----------------- John -----------------')
        book_to_process = 'John'
        write_passage(output_folder, download_translation, book_to_process, 5, 4)
        write_passage(output_folder, download_translation, book_to_process, 7, 53)
        write_passage(output_folder, download_translation, book_to_process, 8, 11)
        print('----------------- Acts -----------------')
        book_to_process = 'Acts'
        write_passage(output_folder, download_translation, book_to_process, 8, 37)
        write_passage(output_folder, download_translation, book_to_process, 15, 34)
        write_passage(output_folder, download_translation, book_to_process, 24, 7)
        write_passage(output_folder, download_translation, book_to_process, 28, 29)
        print('----------------- Romans -----------------')
        write_passage(output_folder, download_translation, 'Romans', 16, 24)
    input('Stage 3 completed. {0}'.format(continue_message))

    input('Stage 4: Clean up intermediate files. {0}'.format(continue_message))
    if 4 in stages:
        for removable_book in books_with_omissions:
            os.remove('{0}/{1}/{2}.yaml'.format(output_folder, download_translation, removable_book))
    input('Stage 4 completed. {0}'.format(continue_message))
