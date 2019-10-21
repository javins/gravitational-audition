from unittest import TestCase


class HttpStatusError(Exception):
    pass


def assert_status(response, expected):
    # Not a unittest assert, as this is used in setup & teardown
    # future work: validate argument types
    if response.status != expected:
        # future work: consider the case body isn't text or
        # should be truncated... also prettyprinting
        msg = "{} returned http status {} instead of expected {}.\nBody:\n{}"\
            .format(response.request, response.status, expected, response.body)
        raise HttpStatusError(msg)


class DockerApiTest(TestCase):
    """
    Abstract base test for Docker api tests.
    """

    def assertStatus(self, response, expected):
        # camelCased for consistency with unittest assert/fail methods
        try:
            assert_status(response, expected)
        except HttpStatusError as e:
            raise self.failureException(e) from None
