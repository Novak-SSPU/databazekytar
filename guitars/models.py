from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.urls import reverse
from django.utils.html import format_html

""" Metoda vrací cestu k uploadovaným souborů - přílohám kytar.
    Cesta má obecnou podobu: guitar/id-kytar/attachments/nazev-souboru.
    Parametr instance odkazuje na instanci (objekt) kytar.
    Parametr filename obsahuje název uploadovaného souboru. """
def attachment_path(instance, filename):
    return "guitar/" + str(instance.guitar.id) + "/attachments/" + filename


class Type(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="Type name",
                            help_text='Enter type of guitar')

    class Meta:
        # atribut ordering definuje upřednostňovaný způsob řazení - zde vzestupně podle pole/sloupce name
        ordering = ["name"]
        verbose_name = "Type"
        verbose_name_plural = "Types"

    def __str__(self):
        """ Řetězec, který se používá jako textová reprezentace objektu (například v administraci aplikace).
        V našem případě bude objekt (žánr) reprezentován výpisem obsahu pole name """
        return self.name

    def guitar_count(self, obj):
        return obj.guitar_set.count()

class Guitar(models.Model):
    # Fields
    # Znakové pole o maximální délce 200 znaků pro vložení názvu kytar
    name = models.CharField(max_length=200, verbose_name="Name")
    # Textové pole pro vložení delšího textu popisujícího děj kytar
    # Formulářový prvek může zůstat prázdný - parametry blank=True, null=True
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    # Celočíselné pole pro nepovinné zadání stopáže (délky) kytar v minutách
    stringnumber = models.IntegerField(blank=True, null=True,
                                  help_text="Please enter the number of strings",
                                  verbose_name="String number")
    # Pole typu image, které umožňuje upload obrázku s plakátem kytar
    image = models.ImageField(upload_to='guitar/images/%Y/%m/%d/', blank=True, null=True, verbose_name="Image")
    # Pole pro zadání desetinného čísla vyjadřujícího hodnocení kytar v rozsahu 1.0 až 10.0
    # Výchozí hodnota je nastavena na 5.0
    # K validaci hodnot jsou použity metody z balíku/knihovny django.core.validators
    rate = models.FloatField(default=5.0,
                             validators=[MinValueValidator(1.0), MaxValueValidator(10.0)],
                             null=True,
                             help_text="Please enter an float value (range 1.0 - 10.0)",
                             verbose_name="Rate")
    # Vytvoří vztah mezi modely Film a Genre typu M:N
    type = models.ManyToManyField(Type, help_text='Select a type for this guitar')
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    # Metadata
    class Meta:
        # Záznamy budou řazeny primárně sestupně (znaménko mínus) podle data uvedení,
        # sekundárně vzestupně podle názvu
        ordering = ["-rate", "name"]

    # Methods
    def __str__(self):
        """Součástí textové reprezentace kytar bude jeho název, rok uvedení a hodnocení"""
        return f"{self.name}, rate: {str(self.rate)}"

    def get_absolute_url(self):
        """Metoda vrací URL stránky, na které se vypisují podrobné informace o kytar"""
        return reverse('guitar-detail', args=[str(self.id)])

    def rate_percent(self):
        return format_html("{} %", int(self.rate * 10))


""" Třída Attachment je modelem pro databázový objekt (tabulku), který bude obsahovat údaje o přílohách kytar """

class Attachment(models.Model):
    # Fields
    # Povinný titulek přílohy - text do délky 200 znaků
    name = models.CharField(max_length=200, verbose_name="Name")
    # Časový údaj o poslední aktualizaci přílohy - automaticky se ukládá aktuální čas
    last_update = models.DateTimeField(auto_now=True)
    # Pole pro upload souboru
    # Parametr upload_to zajistí uložení souboru do složky specifikované v návratové hodnotě metody attachment_path
    file = models.FileField(upload_to=attachment_path, null=True, verbose_name="File")

    # Konstanta, v níž jsou ve formě n-tic (tuples) předdefinovány různé typy příloh
    TYPE_OF_ATTACHMENT = (
        ('audio', 'Audio'),
        ('image', 'Image'),
        ('text', 'Text'),
        ('video', 'Video'),
        ('other', 'Other'),
    )

    # Pole s definovanými předvolbami pro uložení typu přílohy
    type = models.CharField(max_length=5, choices=TYPE_OF_ATTACHMENT, blank=True, default='image', help_text='Select allowed attachment type', verbose_name="Attachment type")
    # Cizí klíč, který zajišťuje propojení přílohy s daným guitarem (vztah N:1)
    # Parametr on_delete slouží k zajištění tzv. referenční integrity - v případě odstranění kytar
    # budou odstraněny i všechny jeho přílohy (models.CASCADE)
    guitar = models.ForeignKey(Guitar, on_delete=models.CASCADE)

    # Metadata
    class Meta:
        # Primární seřazeno podle poslední aktualizace souborů, sekundárně podle typu přílohy
        # ordering = ["-last_update", "type"]
        order_with_respect_to = 'guitar'

    # Methods
    def __str__(self):
        """ Textová reprezentace objektu """
        return f"{self.name}, ({self.type})"

    @property
    def filesize(self):
        x = self.file.size
        y = 512000
        if x < y * 1000:
            value = round(x/1024, 2)
            ext = ' KB'
        elif x < y * 1000**2:
            value = round(x/1024*2, 2)
            ext = ' MB'
        else:
            value = round(x/1024**3, 2)
            ext = ' GB'
        return str(value)+ext


class Review(models.Model):
    text = models.TextField(verbose_name="Text")
    edit_date = models.DateTimeField(auto_now=True)
    rate = models.IntegerField(default=5,
                             validators=[MinValueValidator(1), MaxValueValidator(10)],
                             null=True,
                             help_text="Please enter an integer value (range 1 - 10)",
                             verbose_name="Rate")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    guitar = models.ForeignKey(Guitar, on_delete=models.CASCADE)

    # Metadata
    class Meta:
        order_with_respect_to = 'guitar'