import pytest
from playwright.sync_api import sync_playwright, expect


@pytest.mark.courses
@pytest.mark.regression
def test_empty_courses_list():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)
        contex = browser.new_context() # чтобы сохрнять данные в локал сторедж
        page = contex.new_page()

        page.goto('https://nikita-filonov.github.io/qa-automation-engineer-ui-course/#/auth/registration')

        email_input = page.get_by_test_id('registration-form-email-input').locator('input')
        email_input.fill('user.name@gmail.com')

        name_input = page.get_by_test_id('registration-form-username-input').locator('input')
        name_input.fill('username')

        password_input = page.get_by_test_id('registration-form-password-input').locator('input')
        password_input.fill('password')

        registration_button = page.get_by_test_id('registration-page-registration-button')
        registration_button.click()

        contex.storage_state(path='browser-state.json')

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)
        contex = browser.new_context(storage_state='browser-state.json')  # чтобы сохрнять данные в локал сторедж
        page = contex.new_page()

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
