from ghost import Ghost
from time import sleep

ghost = Ghost()

with ghost.start(viewport_size=(1375,769)) as session:
    page, extra_resources = session.open('http://python.org')

    print page
    print page.url

    for r in extra_resources:
        print r.url

    print page.content.contains('input')
    result, resources = session.evaluate(
        'document.getElementsByTagName("input")')
    print result.get('length')

    result, resources = session.evaluate(
        'document.getElementsByTagName("input")[0].getAttribute("id");')
    print result

    result, resources = session.set_field_value("input", "scraping")
    print result

    try:
        page, resources = session.call("form", "submit", expect_loading=True)
    except Exception as e:
        print 'EXCEPTION: %s' % e

    result, resources = session.evaluate(
        'document.getElementsByTagName("input")[0].value = "scraping";')
    result, resources = session.evaluate(
        'document.forms[0].submit.click()')

    sleep(10)
    session.show()
    sleep(10)


