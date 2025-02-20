import pytest

from django_unicorn.components.unicorn_view import get_locations


def test_get_locations_kebab_case():
    expected = [("unicorn.components.hello_world", "HelloWorldView")]
    actual = get_locations("hello-world")

    assert expected == actual


def test_get_locations_with_slashes():
    expected = [("unicorn.components.nested.table", "TableView")]
    actual = get_locations("nested/table")

    assert expected == actual


def test_get_locations_with_dots():
    expected = [("nested", "table"), ("unicorn.components.nested.table", "TableView")]
    actual = get_locations("nested.table")

    assert expected == actual


def test_get_locations_fully_qualified_with_dots():
    expected = [
        ("project.components.hello_world", "HelloWorldView"),
    ]
    actual = get_locations("project.components.hello_world.HelloWorldView")

    assert expected == actual


def test_get_locations_fully_qualified_with_slashes():
    expected = [
        ("project.components.hello_world", "HelloWorldView"),
    ]
    actual = get_locations("project/components/hello_world.HelloWorldView")

    assert expected == actual


def test_get_locations_fully_qualified_with_dots_ends_in_component():
    expected = [
        ("project.components.hello_world", "HelloWorldComponent"),
    ]
    actual = get_locations("project.components.hello_world.HelloWorldComponent")

    assert expected == actual


def test_get_locations_fully_qualified_with_dots_does_not_end_in_view():
    """
    The second entry in here is a mess.
    """
    expected = [
        ("project.components.hello_world", "HelloWorldThing"),
        (
            "unicorn.components.project.components.hello_world.HelloWorldThing",
            "HelloworldthingView",
        ),
    ]
    actual = get_locations("project.components.hello_world.HelloWorldThing")

    assert expected == actual


def test_get_locations_apps_setting_tuple(settings):
    settings.UNICORN["APPS"] = ("project",)

    expected = [
        ("project.components.hello_world", "HelloWorldView"),
    ]
    actual = get_locations("hello-world")

    assert expected == actual


def test_get_locations_apps_setting_list(settings):
    settings.UNICORN["APPS"] = [
        "project",
    ]

    expected = [
        ("project.components.hello_world", "HelloWorldView"),
    ]
    actual = get_locations("hello-world")

    assert expected == actual


def test_get_locations_apps_setting_set(settings):
    settings.UNICORN["APPS"] = {
        "project",
    }

    expected = [
        ("project.components.hello_world", "HelloWorldView"),
    ]
    actual = get_locations("hello-world")

    assert expected == actual


def test_get_locations_apps_setting_invalid(settings):
    settings.UNICORN["APPS"] = "project"

    with pytest.raises(AssertionError) as e:
        get_locations("hello-world")

    assert e.type == AssertionError
    settings.UNICORN["APPS"] = ("unicorn",)


def test_get_locations_installed_app_with_app_config(settings):
    unicorn_apps = settings.UNICORN["APPS"]
    del settings.UNICORN["APPS"]
    settings.INSTALLED_APPS = [
        "example.coffee.apps.Config",
    ]

    expected = [("example.coffee.components.hello_world", "HelloWorldView")]
    actual = get_locations("hello-world")

    assert expected == actual

    # test when the app is in a subdirectory "apps"
    settings.INSTALLED_APPS[0] = "foo_project.apps.bar_app.apps.Config"
    expected_location = [("foo_project.apps.bar_app.components.foo_bar", "FooBarView")]
    actual_location = get_locations("foo-bar")
    assert expected_location == actual_location

    settings.UNICORN["APPS"] = unicorn_apps
