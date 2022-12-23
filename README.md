# AuthApi

# Postman Collection and Environment is attached for testing REST API
files to Import in Postman
 1. DjangoAuthApi.postman_collection.json
 2. DjangoAuthApi.postman_environment.json

# Migrated SqLite to PostGreSQL Steps
python3 manage.py dumpdata > data.json
python3 manage.py migrate --run-syncdb
python3 manage.py shell
from django.contrib.contenttypes.models import ContentType
ContentType.objects.all().delete()
exit()
python3 manage.py loaddata data.json