from django.template.defaulttags import register

@register.filter(name='get_mood_count')
def get_mood_count(moods_count, user_id):
    for mood_count in moods_count:
        if mood_count.get('user') == user_id:
            return mood_count.get('count')
    return 0
