from django.db import migrations

def create_default_google_app(apps, schema_editor):
    try:
        # Get models migration-safely
        SiteModel = apps.get_model('sites', 'Site')
        SocialAppModel = apps.get_model('socialaccount', 'SocialApp')
    except (LookupError, ValueError):
        return

    # Ensure site 1 exists (Django default site)
    site, _ = SiteModel.objects.get_or_create(
        id=1,
        defaults={'domain': 'friday-originals.vercel.app', 'name': 'Friday Originals'}
    )

    # Get or create the Google SocialApp linked to site 1
    app, created = SocialAppModel.objects.get_or_create(
        provider='google',
        defaults={
            'name': 'Google Login',
            'client_id': 'placeholder-client-id.apps.googleusercontent.com',
            'secret': 'placeholder-client-secret',
        }
    )
    if created:
        app.sites.add(site)

def remove_default_google_app(apps, schema_editor):
    try:
        SocialAppModel = apps.get_model('socialaccount', 'SocialApp')
        SocialAppModel.objects.filter(
            provider='google',
            client_id='placeholder-client-id.apps.googleusercontent.com'
        ).delete()
    except:
        pass

class Migration(migrations.Migration):

    dependencies = [
        ('hii', '0005_alter_customerprofile_phone'),
        ('sites', '0001_initial'),
        ('socialaccount', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_default_google_app, reverse_code=remove_default_google_app),
    ]
