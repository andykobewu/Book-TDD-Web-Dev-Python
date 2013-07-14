#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import unittest

from book_tester import (
    ChapterTest,
    Command,
)
from write_to_file import remove_function

class Chapter6Test(ChapterTest):
    chapter_no = 6

    def test_listings_and_commands_and_output(self):
        self.parse_listings()

        # sanity checks
        self.assertEqual(type(self.listings[0]), Command)
        self.assertEqual(type(self.listings[1]), Command)
        self.assertEqual(type(self.listings[2]), Command)

        self.start_with_checkout(self.chapter_no)
        self.start_dev_server()

        # other prep
        self.run_command(Command('python3 manage.py syncdb --noinput'))

        # skips
        self.listings[18].skip = True


        while self.pos < 37:
            print(self.pos)
            self.recognise_listing_and_process_it()

        assert 'egrep' in self.listings[37]
        egrep = self.run_command(self.listings[37])
        self.assertCountEqual(egrep.strip().split('\n'), self.listings[38].split('\n'))
        self.listings[37].was_checked = True
        self.listings[38].was_checked = True
        self.pos = 39

        with open(os.path.join(self.tempdir, 'superlists/lists/tests.py')) as f:
            old_views = f.read()
        new_views = remove_function(
                old_views,
                'test_home_page_displays_all_list_items'
        )
        with open(os.path.join(self.tempdir, 'superlists/lists/tests.py'), 'w') as f:
            f.write(new_views)

        while self.pos < 43:
            print(self.pos)
            self.recognise_listing_and_process_it()

        # command followed by unrelated output
        self.run_command(self.listings[43])
        self.listings[43].was_checked = True
        self.pos = 44

        while self.pos < 52:
            print(self.pos)
            self.recognise_listing_and_process_it()

        assert 'git status' in self.listings[52]
        status = self.run_command(self.listings[52])
        self.assertIn('list.html', self.listings[53])
        self.assertIn('list.html', status)
        self.listings[52].was_checked = True
        self.listings[53].was_checked = True
        self.pos = 54

        self.listings[58].skip = True
        self.listings[59].skip = True
        while self.pos < 100:
            print(self.pos)
            self.recognise_listing_and_process_it()
        self.check_final_diff(self.chapter_no)
        self.assert_all_listings_checked(self.listings)


if __name__ == '__main__':
    unittest.main()
