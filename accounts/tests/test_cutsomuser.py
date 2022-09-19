import pytest
# import sys

# @pytest.mark.skip(reason="not implemented yet") # this is a decorator which skips the test
# def test_example():
#     assert 1 == 1

# # @pytest.mark.skipif(sys.version_info < (3, 6), reason="requires python3.6 or higher")
# # def test_example2():
# #     assert 1 == 1



# @pytest.mark.xfail(reason="fails on purpose")
# def test_example3():
#     assert 1 == 1



# # to run this
# # pytest -m 'slow' # this will run all the tests with the slow marker
# @pytest.mark.slow
# def test_example4():
#     assert 1 == 1

# # A patter of writing tests
# # 1. Arrange
# # 2. Act 
# # 3. Assert 

# # fixtures are used to setup and teardown the test basically a function to run before and after the test
# # fixtures are user to feed data to the test such as database, api, etc
# # fixtures are used to run the test in a specific order



# function --> Run once per test
# class --> Run once per class of tests
# module --> Run once per module
# session --> Run once per session


# @pytest.fixture # this is a decorator which makes the function a fixture
# def fixture1():
#     print(True)
#     return 1

# @pytest.fixture(scope='session') # this is a decorator which makes the function a fixture
# def fixture1():
#     print(True)
#     return 1

# def test_example5(fixture1): # this is how you use a fixture
#     print(True)
#     num = fixture1 
#     assert num == 1


# def test_example6(fixture1): # this is how you use a fixture
#     print(True,'2')
#     num = fixture1 
#     assert num == 1