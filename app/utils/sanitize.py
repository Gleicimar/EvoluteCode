import bleach

def clean_input(text):
    return bleach.clean(text)
