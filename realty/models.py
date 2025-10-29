from django.db import models

class Apartment(models.Model):
    estate = models.OneToOneField('Estate', models.DO_NOTHING, primary_key=True)
    residential_complex_name = models.CharField(max_length=255, blank=True, null=True)
    area = models.DecimalField(max_digits=10, decimal_places=2)
    kitchen_area = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    rooms = models.IntegerField()
    floor = models.IntegerField()
    total_floors = models.IntegerField()
    elevator = models.IntegerField()
    balcony = models.IntegerField()

    def __str__(self):
        return f"Apartment in {self.residential_complex_name or 'N/A'}, area: {self.area} m²"

    class Meta:
        managed = False
        db_table = 'apartment'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    def __str__(self):
        return f"{self.group} - {self.permission}"

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.content_type}: {self.codename}"

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    def __str__(self):
        return self.username

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    def __str__(self):
        return f"{self.user} in {self.group}"

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    def __str__(self):
        return f"{self.user} - {self.permission}"

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Contact(models.Model):
    contact_id = models.IntegerField(primary_key=True)
    client = models.ForeignKey('Person', models.DO_NOTHING, blank=True, null=True)
    employee = models.ForeignKey('Person', models.DO_NOTHING, related_name='contact_employee_set', blank=True, null=True)
    estate = models.ForeignKey('Estate', models.DO_NOTHING, blank=True, null=True)

    def __str__(self):
        return f"Contact {self.contact_id}"

    class Meta:
        managed = False
        db_table = 'contact'


class Contract(models.Model):
    contract_id = models.IntegerField(primary_key=True)
    estate = models.ForeignKey('Estate', models.DO_NOTHING)
    employee = models.ForeignKey('Person', models.DO_NOTHING, blank=True, null=True)
    client = models.ForeignKey('Person', models.DO_NOTHING, related_name='contract_client_set', blank=True, null=True)
    contract_type = models.CharField(max_length=10)
    date_signed = models.DateField()
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    payment_amount = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    fee_percentage = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    terms = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Contract {self.contract_id} ({self.contract_type})"

    class Meta:
        managed = False
        db_table = 'contract'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    def __str__(self):
        return f"Log {self.action_time}: {self.object_repr}"

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.app_label}.{self.model}"

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    def __str__(self):
        return f"{self.app}: {self.name}"

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    def __str__(self):
        return self.session_key

    class Meta:
        managed = False
        db_table = 'django_session'


class Email(models.Model):
    address = models.CharField(primary_key=True, max_length=255)
    person = models.ForeignKey('Person', models.DO_NOTHING)

    def __str__(self):
        return self.address

    class Meta:
        managed = False
        db_table = 'email'


class Estate(models.Model):
    estate_id = models.IntegerField(primary_key=True)
    settlement = models.ForeignKey('Settlement', models.DO_NOTHING)
    street = models.CharField(max_length=255)
    house_number = models.CharField(max_length=50)
    apartment_number = models.CharField(max_length=50, blank=True, null=True)
    year_built = models.IntegerField(blank=True, null=True)
    transaction_type = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    status = models.CharField(max_length=50)
    owners = models.ManyToManyField('Person', through='EstateOwner', related_name='owned_estates')
    employees = models.ManyToManyField('Person', through='EstateEmployee', related_name='managed_estates')

    def __str__(self):
        return f"Estate {self.estate_id} at {self.street} {self.house_number}"

    class Meta:
        managed = False
        db_table = 'estate'
        unique_together = (('settlement', 'street', 'house_number', 'apartment_number'),)


class EstateEmployee(models.Model):
    pk = models.CompositePrimaryKey('estate_id', 'person_id')
    estate = models.ForeignKey(Estate, models.DO_NOTHING)
    person = models.ForeignKey('Person', models.DO_NOTHING)
    role_at_estate = models.CharField(max_length=50, blank=True, null=True)
    assigned_from = models.DateField(blank=True, null=True)
    assigned_to = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.person} at {self.estate}"

    class Meta:
        managed = False
        db_table = 'estate_employee'


class EstateOwner(models.Model):
    pk = models.CompositePrimaryKey('estate_id', 'owner_id')
    estate = models.ForeignKey(Estate, models.DO_NOTHING)
    owner = models.ForeignKey('Person', models.DO_NOTHING)

    def __str__(self):
        return f"{self.owner} owns {self.estate}"

    class Meta:
        managed = False
        db_table = 'estate_owner'


class House(models.Model):
    estate = models.OneToOneField(Estate, models.DO_NOTHING, primary_key=True)
    land_area = models.DecimalField(max_digits=10, decimal_places=2)
    floors = models.IntegerField()
    rooms = models.IntegerField()
    garage = models.IntegerField()
    parking = models.IntegerField()
    basement = models.IntegerField()
    garden = models.IntegerField()
    heating_type = models.CharField(max_length=50)

    def __str__(self):
        return f"House at {self.estate.street} {self.estate.house_number}"

    class Meta:
        managed = False
        db_table = 'house'


class Office(models.Model):
    estate = models.OneToOneField(Estate, models.DO_NOTHING, primary_key=True)
    area = models.DecimalField(max_digits=10, decimal_places=2)
    floor = models.IntegerField()
    total_floors = models.IntegerField()
    openspace = models.IntegerField()
    conference_rooms = models.IntegerField()
    parking = models.IntegerField()
    elevator = models.IntegerField()
    security = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Office at {self.estate.street} {self.estate.house_number}"

    class Meta:
        managed = False
        db_table = 'office'


class Person(models.Model):
    person_id = models.IntegerField(primary_key=True)
    surname = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    patronym = models.CharField(max_length=255, blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.surname} {self.name}"

    class Meta:
        managed = False
        db_table = 'person'


class PersonRole(models.Model):
    pk = models.CompositePrimaryKey('person_id', 'role_id')
    person = models.ForeignKey(Person, models.DO_NOTHING)
    role = models.ForeignKey('Role', models.DO_NOTHING)
    assigned_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.person} as {self.role}"

    class Meta:
        managed = False
        db_table = 'person_role'


class Phone(models.Model):
    number = models.CharField(primary_key=True, max_length=20)
    person = models.ForeignKey(Person, models.DO_NOTHING)
    type = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.number

    class Meta:
        managed = False
        db_table = 'phone'


class Role(models.Model):
    role_id = models.IntegerField(primary_key=True)
    name = models.CharField(unique=True, max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = 'role'


class Settlement(models.Model):
    settlement_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    amalgamated_hromada = models.CharField(max_length=255)
    oblast = models.CharField(max_length=255)
    settlement_type = models.CharField(max_length=20)

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = 'settlement'