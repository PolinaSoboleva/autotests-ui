import pytest
from playwright.sync_api import expect, Page

from pages.courses_list_page import CoursesListPage
from pages.create_course_page import CreateCoursePage


@pytest.mark.courses
@pytest.mark.regression
def test_empty_courses_list(chromium_page_with_state: Page):
    page = chromium_page_with_state
    page.goto('https://nikita-filonov.github.io/qa-automation-engineer-ui-course/#/courses')

    courses_title = page.get_by_test_id('courses-list-toolbar-title-text')
    expect(courses_title).to_be_visible()
    expect(courses_title).to_have_text('Courses')

    result_icon = page.get_by_test_id('courses-list-empty-view-icon')
    expect(result_icon).to_be_visible()

    result_title = page.get_by_test_id('courses-list-empty-view-title-text')
    expect(result_title).to_be_visible()
    expect(result_title).to_have_text('There is no results')

    result_text = page.get_by_test_id('courses-list-empty-view-description-text')
    expect(result_text).to_be_visible()
    expect(result_text).to_have_text('Results from the load test pipeline will be displayed here')


@pytest.mark.courses
@pytest.mark.regression
def test_create_course(create_course_page: CreateCoursePage, courses_list_page: CoursesListPage):
    create_course_page.visit('https://nikita-filonov.github.io/qa-automation-engineer-ui-course/#/courses/create')
    create_course_page.check_visible_create_course_title()
    create_course_page.check_disabled_create_course_button()
    create_course_page.check_visible_image_preview_empty_view()
    create_course_page.check_visible_image_upload_view()
    create_course_page.check_visible_create_course_form(title="", max_score='0', min_score='0', estimated_time="",
                                                         description="")
    create_course_page.check_visible_exercises_title()
    create_course_page.check_visible_create_exercise_button()
    create_course_page.check_visible_exercises_empty_view()

    create_course_page.upload_preview_image('./testdata/files/image.png') # не работает загрузка файла, не могу выяснить почему
                                                                          # playwright._impl._errors.TimeoutError: Locator.set_input_files: Timeout 30000ms exceeded.
    create_course_page.check_visible_image_upload_view(is_image_uploaded=True)
    create_course_page.fill_create_course_form(title="Playwright", estimated_time="2 weeks",
                                                description="Playwright", max_score='100', min_score='10')
    create_course_page.click_create_course_button()

    courses_list_page.check_visible_courses_title()
    courses_list_page.check_visible_create_course_button()
    courses_list_page.check_visible_course_card(index=0, title="Playwright", estimated_time="2 weeks",
                                                max_score='100', min_score='10')
