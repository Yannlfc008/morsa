from morsa import BingSearcher

import pytest


def test_init():
    assert BingSearcher().url == 'https:///bing.com/{}'