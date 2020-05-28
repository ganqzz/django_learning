from django import template
from django.utils.safestring import mark_safe

import markdown2

from courses.models import Course

register = template.Library()


# Server must be restarted
@register.simple_tag
def newest_course():
    """ Gets the most recent course that was added to the library """
    return Course.objects.filter(published=True).latest('created_at')


@register.inclusion_tag('courses/_course_nav.html')
def nav_courses_list():
    """ Returns dictionary of courses to display as navigation pane """
    courses = Course.objects \
                  .filter(published=True) \
                  .order_by('-created_at') \
                  .values('id', 'title')[:5]  # dict of attributes instead of the Model instance
    return {'courses': courses}


@register.filter
def time_estimate(word_count):
    """
    Estimate the number of minutes it will take to complete a step
    base on the passed-in word count.
    """
    minutes = round(word_count / 20)
    return minutes


@register.filter('markdown_to_html')
def markdown_to_html(markdown_text):
    """ Converts Markdown text to HTML """
    html_body = markdown2.markdown(markdown_text)
    return mark_safe(html_body)  # omit "safe" filters in the templates
