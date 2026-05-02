from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class MaintenanceRequest(models.Model):
    REQUEST_CATEGORY_CHOICES = [
        ('deplacement', 'Déplacement'),
        ('nettoyage', 'Nettoyage'),
        ('desinsectisation', 'Désinsectisation'),
        ('maintenance', 'Maintenance'),
    ]

    SUBCATEGORY_DEPLACEMENT = [
        ('materiel_informatique', 'Matériel informatique'),
        ('mobilier', 'Mobilier'),
        ('archives', 'Archives'),
        ('autre_deplacement', 'Autre'),
    ]

    SUBCATEGORY_NETTOYAGE = [
        ('vider_corbeille', 'Vider corbeille'),
        ('poussiere', 'Poussière'),
        ('probleme_sanitaire', 'Problème sanitaire'),
        ('autre_nettoyage', 'Autre'),
    ]

    SUBCATEGORY_DESINSECTISATION = [
        ('fourmis', 'Fourmis'),
        ('cafards', 'Cafards'),
        ('mouches', 'Mouches'),
        ('moustiques', 'Moustiques'),
        ('rongeurs', 'Rongeurs'),
        ('autre_desinsectisation', 'Autre'),
    ]

    SUBCATEGORY_MAINTENANCE = [
        ('prise_electrique', 'Prise électrique'),
        ('led', 'LED'),
        ('climatiseur', 'Climatiseur'),
        ('autre_maintenance', 'Autre'),
    ]

    SUBCATEGORY_CHOICES = SUBCATEGORY_DEPLACEMENT + SUBCATEGORY_NETTOYAGE + SUBCATEGORY_DESINSECTISATION + SUBCATEGORY_MAINTENANCE

    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('rejected', 'Rejected'),
    ]

    requester = models.ForeignKey(User, on_delete=models.CASCADE, related_name='requests')
    request_category = models.CharField(max_length=50, choices=REQUEST_CATEGORY_CHOICES, default='maintenance')
    request_subcategory = models.CharField(max_length=50, choices=SUBCATEGORY_CHOICES, default='autre_maintenance')
    title = models.CharField(max_length=200)
    description = models.TextField()
    office_location = models.CharField(max_length=200)
    destination_location = models.CharField(max_length=200, blank=True)
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    availability_start = models.DateTimeField()
    availability_end = models.DateTimeField()
    scheduled_date = models.DateTimeField(null=True, blank=True)
    admin_notes = models.TextField(blank=True)
    rejection_reason = models.TextField(blank=True)
    attachment = models.ImageField(upload_to='attachments/%Y/%m/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.status}"

    @property
    def status_color(self):
        colors = {
            'pending': 'amber',
            'processing': 'blue',
            'scheduled': 'indigo',
            'completed': 'green',
            'rejected': 'red',
        }
        return colors.get(self.status, 'gray')

    @property
    def category_display_fr(self):
        category_map = {
            'deplacement': 'Déplacement',
            'nettoyage': 'Nettoyage',
            'desinsectisation': 'Désinsectisation',
            'maintenance': 'Maintenance',
        }
        return category_map.get(self.request_category, self.request_category)
