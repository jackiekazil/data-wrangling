from selenium.common.exceptions import NoSuchElementException, \
    WebDriverException
from selenium import webdriver


def find_text_element(html_element, element_css):
    try:
        return html_element.find_element_by_css_selector(element_css).text
    except NoSuchElementException:
        pass
    return None


def find_attr_element(html_element, element_css, attr):
    try:
        return html_element.find_element_by_css_selector(
            element_css).get_attribute(attr)
    except NoSuchElementException:
        pass
    return None


def get_browser():
    browser = webdriver.Firefox()
    return browser


def main():
    browser = get_browser()
    browser.get('http://apps.twinesocial.com/fairphone')

    all_data = []
    browser.implicitly_wait(10)
    try:
        all_bubbles = browser.find_elements_by_css_selector(
            'div.twine-item-border')
    except WebDriverException:
        browser.implicitly_wait(3)
        all_bubbles = browser.find_elements_by_css_selector(
            'div.twine-item-border')
    for elem in all_bubbles:
        elem_dict = {}
        content = elem.find_element_by_css_selector('div.content')
        elem_dict['full_name'] = find_text_element(
            content, 'div.fullname')
        elem_dict['short_name'] = find_attr_element(
            content, 'div.name', 'innerHTML')
        elem_dict['text_content'] = find_text_element(
            content, 'div.twine-description')
        elem_dict['timestamp'] = find_attr_element(
            elem, 'div.when a abbr.timeago', 'title')
        elem_dict['original_link'] = find_attr_element(
            elem, 'div.when a', 'data-href')
        elem_dict['picture'] = find_attr_element(
            content, 'div.picture img', 'src')
        all_data.append(elem_dict)
    browser.quit()
    return all_data


if __name__ == '__main__':
    all_data = main()
    print all_data
