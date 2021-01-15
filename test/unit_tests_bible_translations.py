import unittest
import multiprocessing
import sys
sys.path.append('../')
from meaningless import WebExtractor, YAMLDownloader, YAMLExtractor


class UnitTests(unittest.TestCase):

    # Note: Tests will only be run if they are prefixed with test_ in their method name.
    #       All other methods will simply be interpreted as test helper functions.

    def check_baseline_passages(self, translation, expected_passage_results):
        """
        Checks that a translation can return the correct results for a basic set of passages
        :param translation: Translation code for the tests. For example, 'NIV', 'ESV', 'NLT'
        :type translation: str
        :param expected_passage_results: List of strings correlating to each of the tested passages
        :type expected_passage_results: list
        """
        if translation != 'YLT':
            return
        bible = WebExtractor(translation=translation)
        actual_passage_results = [
            bible.search('Revelation 21:25'),
            bible.search('Matthew 1:1 - 3'),
            bible.search('Nehemiah 7:40 - 42'),
            bible.search('Psalm 32:4'),
            bible.search('John 7:53')
        ]
        self.assertEqual(len(actual_passage_results), len(expected_passage_results),
                         'Cannot 1:1 match actual passages with {0} passages'.format(len(expected_passage_results)))
        expected_passage_index = 0
        for passage in actual_passage_results:
            self.assertEqual(expected_passage_results[expected_passage_index], passage, 'Passage is incorrect')
            expected_passage_index += 1

    def check_omitted_passages(self, translation, expected_passage_results):
        """
        Checks that a translation can return the correct results for all known passages which can be omitted
        :param translation: Translation code for the tests. For example, 'NIV', 'ESV', 'NLT'
        :type translation: str
        :param expected_passage_results: List of strings correlating to each of the tested passages
        :type expected_passage_results: list
        """
        if translation != 'YLT':
            return
        download_path = './tmp/check_omitted_passages/{0}'.format(translation)
        # Downloading the books with a process map is somewhat faster than using multiple daemon processes to
        # acquire each book sequentially.
        downloader = YAMLDownloader(translation=translation, enable_multiprocessing=False,
                                    default_directory=download_path)
        bible = YAMLExtractor(translation=translation, default_directory=download_path)

        books_with_omissions = ['Matthew', 'Mark', 'Luke', 'John', 'Acts', 'Romans']
        pool = multiprocessing.Pool(len(books_with_omissions))
        pool.map(downloader.download_book, books_with_omissions)

        # Matthew
        book = books_with_omissions[0]
        self.assertEqual(expected_passage_results[book][0], bible.get_passage(book, 9, 34), 'Passage is incorrect')
        self.assertEqual(expected_passage_results[book][1], bible.get_passage(book, 12, 47), 'Passage is incorrect')
        self.assertEqual(expected_passage_results[book][2], bible.get_passage(book, 17, 21), 'Passage is incorrect')
        self.assertEqual(expected_passage_results[book][3], bible.get_passage(book, 18, 11), 'Passage is incorrect')
        self.assertEqual(expected_passage_results[book][4], bible.get_passage(book, 21, 44), 'Passage is incorrect')
        self.assertEqual(expected_passage_results[book][5], bible.get_passage(book, 23, 14), 'Passage is incorrect')

        # Mark
        book = books_with_omissions[1]
        self.assertEqual(expected_passage_results[book][0], bible.get_passage(book, 7, 16), 'Passage is incorrect')
        self.assertEqual(expected_passage_results[book][1], bible.get_passage(book, 9, 44), 'Passage is incorrect')
        self.assertEqual(expected_passage_results[book][2], bible.get_passage(book, 9, 46), 'Passage is incorrect')
        self.assertEqual(expected_passage_results[book][3], bible.get_passage(book, 11, 26), 'Passage is incorrect')
        self.assertEqual(expected_passage_results[book][4], bible.get_passage(book, 15, 28), 'Passage is incorrect')
        self.assertEqual(expected_passage_results[book][5], bible.get_passage(book, 16, 9), 'Passage is incorrect')
        self.assertEqual(expected_passage_results[book][6], bible.get_passage(book, 16, 20), 'Passage is incorrect')

        # Luke
        book = books_with_omissions[2]
        self.assertEqual(expected_passage_results[book][0], bible.get_passage(book, 17, 36), 'Passage is incorrect')
        self.assertEqual(expected_passage_results[book][1], bible.get_passage(book, 22, 20), 'Passage is incorrect')
        self.assertEqual(expected_passage_results[book][2], bible.get_passage(book, 22, 43), 'Passage is incorrect')
        self.assertEqual(expected_passage_results[book][3], bible.get_passage(book, 22, 44), 'Passage is incorrect')
        self.assertEqual(expected_passage_results[book][4], bible.get_passage(book, 23, 17), 'Passage is incorrect')
        self.assertEqual(expected_passage_results[book][5], bible.get_passage(book, 24, 12), 'Passage is incorrect')
        self.assertEqual(expected_passage_results[book][6], bible.get_passage(book, 24, 40), 'Passage is incorrect')

        # John
        book = books_with_omissions[3]
        self.assertEqual(expected_passage_results[book][0], bible.get_passage(book, 5, 4), 'Passage is incorrect')
        self.assertEqual(expected_passage_results[book][1], bible.get_passage(book, 7, 53), 'Passage is incorrect')
        self.assertEqual(expected_passage_results[book][2], bible.get_passage(book, 8, 11), 'Passage is incorrect')

        # Acts
        book = books_with_omissions[4]
        self.assertEqual(expected_passage_results[book][0], bible.get_passage(book, 8, 37), 'Passage is incorrect')
        self.assertEqual(expected_passage_results[book][1], bible.get_passage(book, 15, 34), 'Passage is incorrect')
        self.assertEqual(expected_passage_results[book][2], bible.get_passage(book, 24, 7), 'Passage is incorrect')
        self.assertEqual(expected_passage_results[book][3], bible.get_passage(book, 28, 29), 'Passage is incorrect')

        # Romans
        book = books_with_omissions[5]
        self.assertEqual(expected_passage_results[book][0], bible.get_passage(book, 16, 24), 'Passage is incorrect')

    def test_translation_niv(self):
        translation = 'NIV'
        baseline_passages = [
            '\u00b2\u2075 On no day will its gates ever be shut, for there will be no night there.',

            'This is the genealogy of Jesus the Messiah the son of David, the son of Abraham: \n'
            '\u00b2 Abraham was the father of Isaac,\n'
            'Isaac the father of Jacob,\n'
            'Jacob the father of Judah and his brothers, \n'
            '\u00b3 Judah the father of Perez and Zerah, whose mother was Tamar,\n'
            'Perez the father of Hezron,\n'
            'Hezron the father of Ram,',

            '\u2074\u2070 of Immer 1,052 \u2074\u00b9 of Pashhur 1,247 \u2074\u00b2 of Harim 1,017',

            '\u2074 For day and night\n'
            '    your hand was heavy on me;\n'
            'my strength was sapped\n'
            '    as in the heat of summer.',

            '\u2075\u00b3 Then they all went home,'
        ]
        omitted_passages = {
            'Matthew': [
                '\u00b3\u2074 But the Pharisees said, \u201cIt is by the prince of demons that he drives out demons.'
                '\u201d',
                '\u2074\u2077 Someone told him, \u201cYour mother and brothers are standing outside, '
                'wanting to speak to you.\u201d',
                '\u00b2\u00b9',
                '\u00b9\u00b9',
                '\u2074\u2074 Anyone who falls on this stone will be broken to pieces; '
                'anyone on whom it falls will be crushed.\u201d',
                '\u00b9\u2074',
            ],
            'Mark': [
                '\u00b9\u2076',
                '\u2074\u2074',
                '\u2074\u2076',
                '\u00b2\u2076',
                '\u00b2\u2078',
                '\u2079 When Jesus rose early on the first day of the week, he appeared first to Mary Magdalene, '
                'out of whom he had driven seven demons.',
                '\u00b2\u2070 Then the disciples went out and preached everywhere, and the Lord worked with them and '
                'confirmed his word by the signs that accompanied it.'
            ],
            'Luke': [
                '\u00b3\u2076',
                '\u00b2\u2070 In the same way, after the supper he took the cup, saying, '
                '\u201cThis cup is the new covenant in my blood, which is poured out for you.',
                '\u2074\u00b3 An angel from heaven appeared to him and strengthened him.',
                '\u2074\u2074 And being in anguish, he prayed more earnestly, '
                'and his sweat was like drops of blood falling to the ground.',
                '\u00b9\u2077',
                '\u00b9\u00b2 Peter, however, got up and ran to the tomb. Bending over, he saw the strips of '
                'linen lying by themselves, and he went away, wondering to himself what had happened.',
                '\u2074\u2070 When he had said this, he showed them his hands and feet.'
            ],
            'John': [
                '\u2074',
                '\u2075\u00b3 Then they all went home,',
                '\u00b9\u00b9 \u201cNo one, sir,\u201d she said.\n'
                '\u201cThen neither do I condemn you,\u201d Jesus declared. '
                '\u201cGo now and leave your life of sin.\u201d',
            ],
            'Acts': [
                '\u00b3\u2077',
                '\u00b3\u2074',
                '\u2077',
                '\u00b2\u2079'
            ],
            'Romans': [
                '\u00b2\u2074'
            ],
        }
        self.check_baseline_passages(translation, baseline_passages)
        self.check_omitted_passages(translation, omitted_passages)

    def test_translation_nasb(self):
        translation = 'NASB'
        baseline_passages = [
            '\u00b2\u2075 In the daytime (for there will be no night there) its gates will never be closed;',

            'The record of the genealogy of Jesus the Messiah, the son of David, the son of Abraham: \n'
            '\u00b2 Abraham fathered Isaac, Isaac fathered Jacob, and Jacob fathered Judah and his brothers. '
            '\u00b3 Judah fathered Perez and Zerah by Tamar, Perez fathered Hezron, and Hezron fathered Ram.',

            '\u2074\u2070 the sons of Immer, 1,052; \u2074\u00b9 the sons of Pashhur, 1,247; '
            '\u2074\u00b2 the sons of Harim, 1,017.',

            '\u2074 For day and night Your hand was heavy upon me;\n'
            'My vitality failed as with the dry heat of summer. Selah',

            '\u2075\u00b3 [[And everyone went to his home.'
        ]
        omitted_passages = {
            'Matthew': [
                '\u00b3\u2074 But the Pharisees were saying, \u201cHe casts out the demons by the ruler of the demons.'
                '\u201d',
                '\u2074\u2077 [Someone said to Him, \u201cLook, Your mother and Your brothers are standing outside, '
                'seeking to speak to You.\u201d]',
                '',
                '',
                '\u2074\u2074 And the one who falls on this stone will be broken to pieces; '
                'and on whomever it falls, it will crush him.\u201d',
                '',
            ],
            'Mark': [
                '',
                '',
                '',
                '\u00b2\u2076 [But if you do not forgive, neither will your Father who is in heaven forgive your '
                'offenses.\u201d]',
                '',
                '\u2079 [[Now after He had risen early on the first day of the week, He first appeared to Mary '
                'Magdalene, from whom He had cast out seven demons.',
                '\u00b2\u2070 And they went out and preached everywhere, while the Lord worked with them, and '
                'confirmed the word by the signs that followed.]]\n'
                '[[And they promptly reported all these instructions to Peter and his companions. '
                'And after that, Jesus Himself also sent out through them from east to west the sacred and '
                'imperishable proclamation of eternal salvation.]]'
            ],
            'Luke': [
                '\u00b3\u2076 [Two men will be in the field; one will be taken and the other will be left.\u201d]',
                '\u00b2\u2070 And in the same way He took the cup after they had eaten, saying, '
                '\u201cThis cup, which is poured out for you, is the new covenant in My blood.',
                '\u2074\u00b3 [Now an angel from heaven appeared to Him, strengthening Him.',
                '\u2074\u2074 And being in agony, He was praying very fervently; '
                'and His sweat became like drops of blood, falling down upon the ground].',
                '\u00b9\u2077 [Now he was obligated to release to them at the feast one prisoner.]',
                '\u00b9\u00b2 Nevertheless, Peter got up and ran to the tomb; and when he stooped and looked in, '
                'he saw the linen wrappings only; and he went away to his home, marveling at what had happened.',
                '\u2074\u2070 And when He had said this, He showed them His hands and His feet.'
            ],
            'John': [
                '',
                '\u2075\u00b3 [[And everyone went to his home.',
                '\u00b9\u00b9 She said, \u201cNo one, Lord.\u201d And Jesus said, '
                '\u201cI do not condemn you, either. Go. From now on do not sin any longer.\u201d]]',
            ],
            'Acts': [
                '',
                '',
                '',
                '',
            ],
            'Romans': [
                ''
            ],
        }
        self.check_baseline_passages(translation, baseline_passages)
        self.check_omitted_passages(translation, omitted_passages)

    def test_translation_nkjv(self):
        translation = 'NKJV'
        baseline_passages = [
            '\u00b2\u2075 Its gates shall not be shut at all by day (there shall be no night there).',

            'The book of the genealogy of Jesus Christ, the Son of David, the Son of Abraham: \n'
            '\u00b2 Abraham begot Isaac, Isaac begot Jacob, and Jacob begot Judah and his brothers. '
            '\u00b3 Judah begot Perez and Zerah by Tamar, Perez begot Hezron, and Hezron begot Ram.',

            '\u2074\u2070 the sons of Immer, one thousand and fifty-two; \n'
            '\u2074\u00b9 the sons of Pashhur, one thousand two hundred and forty-seven; \n'
            '\u2074\u00b2 the sons of Harim, one thousand and seventeen.',

            '\u2074 For day and night Your hand was heavy upon me;\n'
            'My vitality was turned into the drought of summer. Selah',

            '\u2075\u00b3 And everyone went to his own house.'
        ]
        omitted_passages = {
            'Matthew': [
                '\u00b3\u2074 But the Pharisees said, \u201cHe casts out demons by the ruler of the demons.\u201d',
                '\u2074\u2077 Then one said to Him, \u201cLook, Your mother and Your brothers are standing outside, '
                'seeking to speak with You.\u201d',
                '\u00b2\u00b9 However, this kind does not go out except by prayer and fasting.\u201d',
                '\u00b9\u00b9 For the Son of Man has come to save that which was lost.',
                '\u2074\u2074 And whoever falls on this stone will be broken; but on whomever it falls, '
                'it will grind him to powder.\u201d',
                '\u00b9\u2074 Woe to you, scribes and Pharisees, hypocrites! For you devour widows\u2019 houses, '
                'and for a pretense make long prayers. Therefore you will receive greater condemnation.',
            ],
            'Mark': [
                '\u00b9\u2076 If anyone has ears to hear, let him hear!\u201d',
                '\u2074\u2074 where\n\u2018Their worm does not die\nAnd the fire is not quenched.\u2019',
                '\u2074\u2076 where\n\u2018Their worm does not die\nAnd the fire is not quenched.\u2019',
                '\u00b2\u2076 But if you do not forgive, neither will your Father in heaven forgive your trespasses.'
                '\u201d',
                '\u00b2\u2078 So the Scripture was fulfilled which says, \u201cAnd He was numbered with the '
                'transgressors.\u201d',
                '\u2079 Now when He rose early on the first day of the week, He appeared first to Mary Magdalene, '
                'out of whom He had cast seven demons.',
                '\u00b2\u2070 And they went out and preached everywhere, the Lord working with them and confirming the '
                'word through the accompanying signs. Amen.'
            ],
            'Luke': [
                '\u00b3\u2076 Two men will be in the field: the one will be taken and the other left.\u201d',
                '\u00b2\u2070 Likewise He also took the cup after supper, saying, '
                '\u201cThis cup is the new covenant in My blood, which is shed for you.',
                '\u2074\u00b3 Then an angel appeared to Him from heaven, strengthening Him.',
                '\u2074\u2074 And being in agony, He prayed more earnestly. '
                'Then His sweat became like great drops of blood falling down to the ground.',
                '\u00b9\u2077 (for it was necessary for him to release one to them at the feast).',
                '\u00b9\u00b2 But Peter arose and ran to the tomb; and stooping down, he saw the linen cloths lying by '
                'themselves; and he departed, marveling to himself at what had happened.',
                '\u2074\u2070 When He had said this, He showed them His hands and His feet.'
            ],
            'John': [
                '\u2074 For an angel went down at a certain time into the pool and stirred up the water; then whoever '
                'stepped in first, after the stirring of the water, was made well of whatever disease he had.',
                '\u2075\u00b3 And everyone went to his own house.',
                '\u00b9\u00b9 She said, \u201cNo one, Lord.\u201d\n'
                'And Jesus said to her, \u201cNeither do I condemn you; go and sin no more.\u201d',
            ],
            'Acts': [
                '\u00b3\u2077 Then Philip said, \u201cIf you believe with all your heart, you may.\u201d\n'
                'And he answered and said, \u201cI believe that Jesus Christ is the Son of God.\u201d',
                '\u00b3\u2074 However, it seemed good to Silas to remain there.',
                '\u2077 But the commander Lysias came by and with great violence took him out of our hands,',
                '\u00b2\u2079 And when he had said these words, the Jews departed and had a great dispute among '
                'themselves.'
            ],
            'Romans': [
                '\u00b2\u2074 The grace of our Lord Jesus Christ be with you all. Amen.'
            ],
        }
        self.check_baseline_passages(translation, baseline_passages)
        self.check_omitted_passages(translation, omitted_passages)

    def test_translation_nrsv(self):
        translation = 'NRSV'
        baseline_passages = [
            '\u00b2\u2075 Its gates will never be shut by day\u2014and there will be no night there.',

            'An account of the genealogy of Jesus the Messiah, the son of David, the son of Abraham. \n'
            '\u00b2 Abraham was the father of Isaac, and Isaac the father of Jacob, '
            'and Jacob the father of Judah and his brothers, '
            '\u00b3 and Judah the father of Perez and Zerah by Tamar, and Perez the father of Hezron, '
            'and Hezron the father of Aram,',

            '\u2074\u2070 Of Immer, one thousand fifty-two. '
            '\u2074\u00b9 Of Pashhur, one thousand two hundred forty-seven. '
            '\u2074\u00b2 Of Harim, one thousand seventeen.',

            '\u2074 For day and night your hand was heavy upon me;\n'
            '    my strength was dried up as by the heat of summer. Selah',

            '[[\u2075\u00b3 Then each of them went home,'
        ]
        omitted_passages = {
            'Matthew': [
                '\u00b3\u2074 But the Pharisees said, \u201cBy the ruler of the demons he casts out the demons.\u201d',
                '\u2074\u2077 Someone told him, \u201cLook, your mother and your brothers are standing outside, '
                'wanting to speak to you.\u201d',
                '',
                '',
                '\u2074\u2074 The one who falls on this stone will be broken to pieces; and it will crush anyone '
                'on whom it falls.\u201d',
                '',
            ],
            'Mark': [
                '',
                '',
                '',
                '',
                '',
                '\u2079 [[Now after he rose early on the first day of the week, he appeared first to Mary Magdalene, '
                'from whom he had cast out seven demons.',
                '\u00b2\u2070 And they went out and proclaimed the good news everywhere, while the Lord worked with '
                'them and confirmed the message by the signs that accompanied it.]]'
            ],
            'Luke': [
                '',
                '\u00b2\u2070 And he did the same with the cup after supper, saying, '
                '\u201cThis cup that is poured out for you is the new covenant in my blood.',
                '\u2074\u00b3 Then an angel from heaven appeared to him and gave him strength.',
                '\u2074\u2074 In his anguish he prayed more earnestly, and his sweat became like '
                'great drops of blood falling down on the ground.]]',
                '',
                '\u00b9\u00b2 But Peter got up and ran to the tomb; stooping and looking in, he saw the linen cloths '
                'by themselves; then he went home, amazed at what had happened.',
                '\u2074\u2070 And when he had said this, he showed them his hands and his feet.'
            ],
            'John': [
                '',
                '\u2075\u00b3 Then each of them went home,',
                '\u00b9\u00b9 She said, \u201cNo one, sir.\u201d And Jesus said, '
                '\u201cNeither do I condemn you. Go your way, and from now on do not sin again.\u201d]]',
            ],
            'Acts': [
                '',
                '',
                '',
                '',
            ],
            'Romans': [
                ''
            ],
        }
        self.check_baseline_passages(translation, baseline_passages)
        self.check_omitted_passages(translation, omitted_passages)

    def test_translation_esv(self):
        translation = 'ESV'
        baseline_passages = [
            '\u00b2\u2075 and its gates will never be shut by day\u2014and there will be no night there.',

            'The book of the genealogy of Jesus Christ, the son of David, the son of Abraham. \n'
            '\u00b2 Abraham was the father of Isaac, and Isaac the father of Jacob, and Jacob the father of Judah and '
            'his brothers, '
            '\u00b3 and Judah the father of Perez and Zerah by Tamar, and Perez the father of Hezron, and '
            'Hezron the father of Ram,',

            '\u2074\u2070 The sons of Immer, 1,052. \u2074\u00b9 The sons of Pashhur, 1,247. '
            '\u2074\u00b2 The sons of Harim, 1,017.',

            '\u2074 For day and night your hand was heavy upon me;\n'
            '    my strength was dried up as by the heat of summer. Selah',

            '\u2075\u00b3 [[They went each to his own house,'
        ]
        omitted_passages = {
            'Matthew': [
                '\u00b3\u2074 But the Pharisees said, \u201cHe casts out demons by the prince of demons.\u201d',
                '',
                '',
                '',
                '\u2074\u2074 And the one who falls on this stone will be broken to pieces; and when it falls on '
                'anyone, it will crush him.\u201d',
                '',
            ],
            'Mark': [
                '',
                '',
                '',
                '',
                '',
                '\u2079 [[Now when he rose early on the first day of the week, he appeared first to Mary Magdalene, '
                'from whom he had cast out seven demons.',
                '\u00b2\u2070 And they went out and preached everywhere, while the Lord worked with them and '
                'confirmed the message by accompanying signs.]]'
            ],
            'Luke': [
                '',
                '\u00b2\u2070 And likewise the cup after they had eaten, saying, '
                '\u201cThis cup that is poured out for you is the new covenant in my blood.',
                '\u2074\u00b3 And there appeared to him an angel from heaven, strengthening him.',
                '\u2074\u2074 And being in agony he prayed more earnestly; and his sweat became like '
                'great drops of blood falling down to the ground.',
                '',
                '\u00b9\u00b2 But Peter rose and ran to the tomb; stooping and looking in, he saw the linen cloths by '
                'themselves; and he went home marveling at what had happened.',
                '\u2074\u2070 And when he had said this, he showed them his hands and his feet.'
            ],
            'John': [
                '',
                '\u2075\u00b3 [[They went each to his own house,',
                '\u00b9\u00b9 She said, \u201cNo one, Lord.\u201d And Jesus said, '
                '\u201cNeither do I condemn you; go, and from now on sin no more.\u201d]]',
            ],
            'Acts': [
                '',
                '',
                '',
                '',
            ],
            'Romans': [
                ''
            ],
        }
        self.check_baseline_passages(translation, baseline_passages)
        self.check_omitted_passages(translation, omitted_passages)

    def test_translation_web(self):
        translation = 'WEB'
        baseline_passages = [
            '\u00b2\u2075 Its gates will in no way be shut by day (for there will be no night there),',

            'The book of the genealogy of Jesus Christ, the son of David, the son of Abraham. \n'
            '\u00b2 Abraham became the father of Isaac. Isaac became the father of Jacob. '
            'Jacob became the father of Judah and his brothers. '
            '\u00b3 Judah became the father of Perez and Zerah by Tamar. Perez became the father of Hezron. '
            'Hezron became the father of Ram.',

            '\u2074\u2070 The children of Immer: one thousand fifty-two. \n'
            '\u2074\u00b9 The children of Pashhur: one thousand two hundred forty-seven. \n'
            '\u2074\u00b2 The children of Harim: one thousand seventeen.',

            '\u2074 For day and night your hand was heavy on me.\n'
            '    My strength was sapped in the heat of summer. Selah.',

            '\u2075\u00b3 Everyone went to his own house,'
        ]
        omitted_passages = {
            'Matthew': [
                '\u00b3\u2074 But the Pharisees said, \u201cBy the prince of the demons, he casts out demons.\u201d',
                '\u2074\u2077 One said to him, \u201cBehold, your mother and your brothers stand outside, '
                'seeking to speak to you.\u201d',
                '\u00b2\u00b9 But this kind doesn\u2019t go out except by prayer and fasting.\u201d',
                '\u00b9\u00b9 For the Son of Man came to save that which was lost.',
                '\u2074\u2074 He who falls on this stone will be broken to pieces, but on whomever it will fall, '
                'it will scatter him as dust.\u201d',
                '\u00b9\u2074 \u201cBut woe to you, scribes and Pharisees, hypocrites! Because you shut up the '
                'Kingdom of Heaven against men; for you don\u2019t enter in yourselves, neither do you allow those '
                'who are entering in to enter.',
            ],
            'Mark': [
                '\u00b9\u2076 If anyone has ears to hear, let him hear!\u201d',
                '\u2074\u2074 \u2018where their worm doesn\u2019t die, and the fire is not quenched.\u2019',
                '\u2074\u2076 \u2018where their worm doesn\u2019t die, and the fire is not quenched.\u2019',
                '\u00b2\u2076 But if you do not forgive, neither will your Father in heaven forgive your '
                'transgressions.\u201d',
                '\u00b2\u2078 The Scripture was fulfilled, which says, \u201cHe was counted with transgressors.\u201d',
                '\u2079 Now when he had risen early on the first day of the week, he appeared first to Mary Magdalene, '
                'from whom he had cast out seven demons.',
                '\u00b2\u2070 They went out, and preached everywhere, the Lord working with them, '
                'and confirming the word by the signs that followed. Amen.'
            ],
            'Luke': [
                '\u00b3\u2076',
                '\u00b2\u2070 Likewise, he took the cup after supper, saying, '
                '\u201cThis cup is the new covenant in my blood, which is poured out for you.',
                '\u2074\u00b3 An angel from heaven appeared to him, strengthening him.',
                '\u2074\u2074 Being in agony he prayed more earnestly. '
                'His sweat became like great drops of blood falling down on the ground.',
                '\u00b9\u2077 Now he had to release one prisoner to them at the feast.',
                '\u00b9\u00b2 But Peter got up and ran to the tomb. Stooping and looking in, he saw the strips of '
                'linen lying by themselves, and he departed to his home, wondering what had happened.',
                '\u2074\u2070 When he had said this, he showed them his hands and his feet.'
            ],
            'John': [
                '\u2074 for an angel went down at certain times into the pool and stirred up the water. '
                'Whoever stepped in first after the stirring of the water was healed of whatever disease he had.',
                '\u2075\u00b3 Everyone went to his own house,',
                '\u00b9\u00b9 She said, \u201cNo one, Lord.\u201d\n'
                'Jesus said, \u201cNeither do I condemn you. Go your way. From now on, sin no more.\u201d',
            ],
            'Acts': [
                '\u00b3\u2077',
                '\u00b3\u2074',
                '\u2077',
                '\u00b2\u2079 When he had said these words, the Jews departed, having a great dispute among themselves.'
            ],
            'Romans': [
                '\u00b2\u2074 The grace of our Lord Jesus Christ be with you all! Amen.'
            ],
        }
        self.check_baseline_passages(translation, baseline_passages)
        self.check_omitted_passages(translation, omitted_passages)

    def test_translation_nlt(self):
        translation = 'NLT'
        baseline_passages = [
            '\u00b2\u2075 Its gates will never be closed at the end of day because there is no night there.',

            'This is a record of the ancestors of Jesus the Messiah, a descendant of David and of Abraham: \n'
            '\u00b2 Abraham was the father of Isaac.\nIsaac was the father of Jacob.\n'
            'Jacob was the father of Judah and his brothers.\n'
            '\u00b3 Judah was the father of Perez and Zerah (whose mother was Tamar).\n'
            'Perez was the father of Hezron.\nHezron was the father of Ram.',

            '\u2074\u2070 The family of Immer 1,052 '
            '\u2074\u00b9 The family of Pashhur 1,247 '
            '\u2074\u00b2 The family of Harim 1,017',

            '\u2074 Day and night your hand of discipline was heavy on me.\n'
            '    My strength evaporated like water in the summer heat. Interlude',

            '\u2075\u00b3 Then the meeting broke up, and everybody went home.'
        ]
        omitted_passages = {
            'Matthew': [
                '\u00b3\u2074 But the Pharisees said, \u201cHe can cast out demons because he is empowered by '
                'the prince of demons.\u201d',
                '\u2074\u2077 Someone told Jesus, \u201cYour mother and your brothers are standing outside, '
                'and they want to speak to you.\u201d',
                '',
                '',
                '\u2074\u2074 Anyone who stumbles over that stone will be broken to pieces, '
                'and it will crush anyone it falls on.\u201d',
                '',
            ],
            'Mark': [
                '',
                '',
                '',
                '',
                '',
                '\u2079 After Jesus rose from the dead early on Sunday morning, the first person who saw him was '
                'Mary Magdalene, the woman from whom he had cast out seven demons.',
                '\u00b2\u2070 And the disciples went everywhere and preached, and the Lord worked through them, '
                'confirming what they said by many miraculous signs.'
            ],
            'Luke': [
                '',
                '\u00b2\u2070 After supper he took another cup of wine and said, \u201cThis cup is the new covenant '
                'between God and his people\u2014an agreement confirmed with my blood, '
                'which is poured out as a sacrifice for you.',
                '\u2074\u00b3 Then an angel from heaven appeared and strengthened him.',
                '\u2074\u2074 He prayed more fervently, and he was in such agony of spirit that '
                'his sweat fell to the ground like great drops of blood.',
                '',
                '\u00b9\u00b2 However, Peter jumped up and ran to the tomb to look. Stooping, he peered in and saw the '
                'empty linen wrappings; then he went home again, wondering what had happened.',
                '\u2074\u2070 As he spoke, he showed them his hands and his feet.'
            ],
            'John': [
                '',
                '\u2075\u00b3 Then the meeting broke up, and everybody went home.',
                '\u00b9\u00b9 \u201cNo, Lord,\u201d she said.\n'
                'And Jesus said, \u201cNeither do I. Go and sin no more.\u201d',
            ],
            'Acts': [
                '',
                '',
                '',
                '',
            ],
            'Romans': [
                ''
            ],
        }
        self.check_baseline_passages(translation, baseline_passages)
        self.check_omitted_passages(translation, omitted_passages)

    def test_translation_kjv(self):
        translation = 'KJV'
        baseline_passages = [
            '\u00b2\u2075 And the gates of it shall not be shut at all by day: for there shall be no night there.',

            'The book of the generation of Jesus Christ, the son of David, the son of Abraham. \n'
            '\u00b2 Abraham begat Isaac; and Isaac begat Jacob; and Jacob begat Judas and his brethren; \n'
            '\u00b3 And Judas begat Phares and Zara of Thamar; and Phares begat Esrom; and Esrom begat Aram;',

            '\u2074\u2070 The children of Immer, a thousand fifty and two. \n'
            '\u2074\u00b9 The children of Pashur, a thousand two hundred forty and seven. \n'
            '\u2074\u00b2 The children of Harim, a thousand and seventeen.',

            '\u2074 For day and night thy hand was heavy upon me: '
            'my moisture is turned into the drought of summer. Selah.',

            '\u2075\u00b3 And every man went unto his own house.'
        ]
        omitted_passages = {
            'Matthew': [
                '\u00b3\u2074 But the Pharisees said, He casteth out devils through the prince of the devils.',
                '\u2074\u2077 Then one said unto him, Behold, thy mother and thy brethren stand without, '
                'desiring to speak with thee.',
                '\u00b2\u00b9 Howbeit this kind goeth not out but by prayer and fasting.',
                '\u00b9\u00b9 For the Son of man is come to save that which was lost.',
                '\u2074\u2074 And whosoever shall fall on this stone shall be broken: '
                'but on whomsoever it shall fall, it will grind him to powder.',
                "\u00b9\u2074 Woe unto you, scribes and Pharisees, hypocrites! for ye devour widows' houses, "
                'and for a pretence make long prayer: therefore ye shall receive the greater damnation.',
            ],
            'Mark': [
                '\u00b9\u2076 If any man have ears to hear, let him hear.',
                '\u2074\u2074 Where their worm dieth not, and the fire is not quenched.',
                '\u2074\u2076 Where their worm dieth not, and the fire is not quenched.',
                '\u00b2\u2076 But if ye do not forgive, neither will your Father which is in heaven forgive your '
                'trespasses.',
                '\u00b2\u2078 And the scripture was fulfilled, which saith, And he was numbered with the transgressors.'
                '',
                '\u2079 Now when Jesus was risen early the first day of the week, he appeared first to Mary Magdalene, '
                'out of whom he had cast seven devils.',
                '\u00b2\u2070 And they went forth, and preached every where, the Lord working with them, '
                'and confirming the word with signs following. Amen.'
            ],
            'Luke': [
                '\u00b3\u2076 Two men shall be in the field; the one shall be taken, and the other left.',
                '\u00b2\u2070 Likewise also the cup after supper, saying, '
                'This cup is the new testament in my blood, which is shed for you.',
                '\u2074\u00b3 And there appeared an angel unto him from heaven, strengthening him.',
                '\u2074\u2074 And being in an agony he prayed more earnestly: '
                'and his sweat was as it were great drops of blood falling down to the ground.',
                '\u00b9\u2077 (For of necessity he must release one unto them at the feast.)',
                '\u00b9\u00b2 Then arose Peter, and ran unto the sepulchre; and stooping down, he beheld the linen '
                'clothes laid by themselves, and departed, wondering in himself at that which was come to pass.',
                '\u2074\u2070 And when he had thus spoken, he shewed them his hands and his feet.'
            ],
            'John': [
                '\u2074 For an angel went down at a certain season into the pool, and troubled the water: whosoever '
                'then first after the troubling of the water stepped in was made whole of whatsoever disease he had.',
                '\u2075\u00b3 And every man went unto his own house.',
                '\u00b9\u00b9 She said, No man, Lord. And Jesus said unto her, Neither do I condemn thee: '
                'go, and sin no more.',
            ],
            'Acts': [
                '\u00b3\u2077 And Philip said, If thou believest with all thine heart, thou mayest. '
                'And he answered and said, I believe that Jesus Christ is the Son of God.',
                '\u00b3\u2074 Notwithstanding it pleased Silas to abide there still.',
                '\u2077 But the chief captain Lysias came upon us, and with great violence took him away out of our '
                'hands,',
                '\u00b2\u2079 And when he had said these words, the Jews departed, and had great reasoning among '
                'themselves.'
            ],
            'Romans': [
                '\u00b2\u2074 The grace of our Lord Jesus Christ be with you all. Amen.'
            ],
        }
        self.check_baseline_passages(translation, baseline_passages)
        self.check_omitted_passages(translation, omitted_passages)

    def test_translation_asv(self):
        translation = 'ASV'
        baseline_passages = [
            '\u00b2\u2075 And the gates thereof shall in no wise be shut by day (for there shall be no night there):',

            'The book of the generation of Jesus Christ, the son of David, the son of Abraham. \n'
            '\u00b2 Abraham begat Isaac; and Isaac begat Jacob; and Jacob begat Judah and his brethren; '
            '\u00b3 and Judah begat Perez and Zerah of Tamar; and Perez begat Hezron; and Hezron begat Ram;',

            '\u2074\u2070 The children of Immer, a thousand fifty and two. '
            '\u2074\u00b9 The children of Pashhur, a thousand two hundred forty and seven. '
            '\u2074\u00b2 The children of Harim, a thousand and seventeen.',

            '\u2074 For day and night thy hand was heavy upon me:\n'
            'My moisture was changed as with the drought of summer. Selah',

            '\u2075\u00b3 [And they went every man unto his own house:'
        ]
        omitted_passages = {
            'Matthew': [
                '\u00b3\u2074 But the Pharisees said, By the prince of the demons casteth he out demons.',
                '\u2074\u2077 And one said unto him, Behold, thy mother and thy brethren stand without, '
                'seeking to speak to thee.',
                '',
                '',
                '\u2074\u2074 And he that falleth on this stone shall be broken to pieces: '
                'but on whomsoever it shall fall, it will scatter him as dust.',
                '',
            ],
            'Mark': [
                '',
                '',
                '',
                '',
                '',
                '\u2079 Now when he was risen early on the first day of the week, he appeared first to Mary Magdalene, '
                'from whom he had cast out seven demons.',
                '\u00b2\u2070 And they went forth, and preached everywhere, the Lord working with them, and '
                'confirming the word by the signs that followed. Amen.'
            ],
            'Luke': [
                '',
                '\u00b2\u2070 And the cup in like manner after supper, saying, '
                'This cup is the new covenant in my blood, even that which is poured out for you.',
                '\u2074\u00b3 And there appeared unto him an angel from heaven, strengthening him.',
                '\u2074\u2074 And being in an agony he prayed more earnestly; '
                'and his sweat became as it were great drops of blood falling down upon the ground.',
                '',
                '\u00b9\u00b2 But Peter arose, and ran unto the tomb; and stooping and looking in, he seeth the linen '
                'cloths by themselves; and he departed to his home, wondering at that which was come to pass.',
                '\u2074\u2070 And when he had said this, he showed them his hands and his feet.'
            ],
            'John': [
                '',
                '\u2075\u00b3 [And they went every man unto his own house:',
                '\u00b9\u00b9 And she said, No man, Lord. And Jesus said, Neither do I condemn thee: go thy way; '
                'from henceforth sin no more.]',
            ],
            'Acts': [
                '',
                '',
                '',
                '',
            ],
            'Romans': [
                ''
            ],
        }
        self.check_baseline_passages(translation, baseline_passages)
        self.check_omitted_passages(translation, omitted_passages)

    def test_translation_ylt(self):
        translation = 'YLT'
        baseline_passages = [
            '\u00b2\u2075 and its gates shall not at all be shut by day, for night shall not be there;',

            'A roll of the birth of Jesus Christ, son of David, son of Abraham. \n'
            '\u00b2 Abraham begat Isaac, and Isaac begat Jacob, and Jacob begat Judah and his brethren, \n'
            '\u00b3 and Judah begat Pharez and Zarah of Tamar, and Pharez begat Hezron, and Hezron begat Ram,',

            '\u2074\u2070 sons of Immer: a thousand fifty and two; \n'
            '\u2074\u00b9 sons of Pashur: a thousand two hundred forty and seven; \n'
            '\u2074\u00b2 sons of Harim: a thousand and seventeen.',

            '\u2074 When by day and by night Thy hand is heavy upon me, '
            'My moisture hath been changed Into the droughts of summer. Selah.',

            '\u2075\u00b3 and each one went on to his house, but Jesus went on to the mount of the Olives.'
        ]
        omitted_passages = {
            'Matthew': [
                "\u00b3\u2074 but the Pharisees said, `By the ruler of the demons he doth cast out the demons.'",
                "\u2074\u2077 and one said to him, `Lo, thy mother and thy brethren do stand without, "
                "seeking to speak to thee.'",
                "\u00b2\u00b9 and this kind doth not go forth except in prayer and fasting.'",
                '\u00b9\u00b9 for the Son of Man did come to save the lost.',
                "\u2074\u2074 and he who is falling on this stone shall be broken, "
                "and on whomsoever it may fall it will crush him to pieces.'",
                '\u00b9\u2074 `Wo to you, Scribes and Pharisees, hypocrites! because ye eat up the houses of '
                'the widows, and for a pretence make long prayers, because of this ye shall receive more '
                'abundant judgment.',
            ],
            'Mark': [
                "\u00b9\u2076 If any hath ears to hear -- let him hear.'",
                '\u2074\u2074 where there worm is not dying, and the fire is not being quenched.',
                '\u2074\u2076 where there worm is not dying, and the fire is not being quenched.',
                "\u00b2\u2076 and, if ye do not forgive, neither will your Father who is in the heavens "
                "forgive your trespasses.'",
                "\u00b2\u2078 and the Writing was fulfilled that is saying, `And with lawless ones he was numbered.'",
                '\u2079 And he, having risen in the morning of the first of the sabbaths, did appear first to '
                'Mary the Magdalene, out of whom he had cast seven demons;',
                '\u00b2\u2070 and they, having gone forth, did preach everywhere, the Lord working with [them], and '
                'confirming the word, through the signs following. Amen.'
            ],
            'Luke': [
                "\u00b3\u2076 two men shall be in the field, the one shall be taken, and the other left.'",
                '\u00b2\u2070 In like manner, also, the cup after the supping, saying, `This cup [is] the new covenant '
                'in my blood, that for you is being poured forth.',
                '\u2074\u00b3 And there appeared to him a messenger from heaven strengthening him;',
                '\u2074\u2074 and having been in agony, he was more earnestly praying, and his sweat became, '
                'as it were, great drops of blood falling upon the ground.',
                '\u00b9\u2077 for it was necessary for him to release to them one at every feast,',
                '\u00b9\u00b2 And Peter having risen, did run to the tomb, and having stooped down he seeth the linen '
                'clothes lying alone, and he went away to his own home, wondering at that which was come to pass.',
                '\u2074\u2070 And having said this, he shewed to them the hands and the feet,'
            ],
            'John': [
                '\u2074 for a messenger at a set time was going down in the pool, and was troubling the water, '
                'the first then having gone in after the troubling of the water, became whole of whatever sickness '
                'he was held.',
                '\u2075\u00b3 and each one went on to his house, but Jesus went on to the mount of the Olives.',
                "\u00b9\u00b9 and she said, `No one, Sir;' and Jesus said to her, `Neither do I pass sentence on thee; "
                "be going on, and no more sin.'",
            ],
            'Acts': [
                "\u00b3\u2077 [And Philip said, `If thou dost believe out of all the heart, it is lawful;' "
                "and he answering said, `I believe Jesus Christ to be the Son of God;']",
                '\u00b3\u2074 and it seemed good to Silas to remain there still.',
                '\u2077 and Lysias the chief captain having come near, with much violence, out of our hands did '
                'take away,',
                '\u00b2\u2079 and he having said these things, the Jews went away, having much disputation among '
                'themselves;'
            ],
            'Romans': [
                '\u00b2\u2074 the grace of our Lord Jesus Christ [be] with you all. Amen.'
            ],
        }
        self.check_baseline_passages(translation, baseline_passages)
        self.check_omitted_passages(translation, omitted_passages)

if __name__ == "__main__":
    unittest.main()
