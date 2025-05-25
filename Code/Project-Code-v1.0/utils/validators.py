def validate_form(form):
    return all([
        hasattr(form, 'full_name') and form.full_name.strip(),
        hasattr(form, 'age') and str(form.age).strip(),
        hasattr(form, 'phone_number') and form.phone_number.strip(),
        hasattr(form, 'email') and form.email.strip()
    ])
