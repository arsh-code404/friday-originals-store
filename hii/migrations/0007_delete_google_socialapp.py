from django.db import migrations

def delete_google_app(apps, schema_editor):
    try:
        SocialAppModel = apps.get_model('socialaccount', 'SocialApp')
        SocialAppModel.objects.filter(provider='google').delete()
    except:
        pass

class Migration(migrations.Migration):

    dependencies = [
        ('hii', '0006_create_google_socialapp'),
    ]

    operations = [
        migrations.RunPython(delete_google_app),
    ]
