from django.db import models


class User(models.Model):
    full_name = models.CharField(max_length=1000)
    telegram_id = models.BigIntegerField()


    def __str__(self) -> str:
        return self.full_name

    class Meta:
        db_table = 'users'


class Word(models.Model):
    word = models.CharField(max_length=50)


    def __str__(self) -> str:
        return self.word

    class Meta:
        db_table = 'words'


class Game(models.Model):
    BY_TEXT = 'by_text'
    BY_KEYBOARD = 'by_keyboard'
    BY_IMAGE = 'by_image'

    ACTIVE = 'active'
    INACTIVE = 'inactive'

    PRIVATE = 'private'
    GROUP = 'group'

    GAME_TYPES = (
        (BY_TEXT, 'By text'),
        (BY_KEYBOARD, 'By keyboard'),
        (BY_IMAGE, 'By image')
    )

    STATUSES = (
        (ACTIVE, 'Active'),
        (INACTIVE, 'Inactive')
    )

    CHAT_TYPES = (
        (PRIVATE, 'Private'),
        (GROUP, 'Group')
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUSES)
    chat_type = models.CharField(max_length=20, choices=CHAT_TYPES)
    word = models.ForeignKey(Word, on_delete=models.CASCADE)


    def __str__(self) -> str:
        return f"{self.pk}-game of {self.user.full_name} for {self.word.word}"

    class Meta:
        db_table = 'games'


class GuessedLetter(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    guessed_letters = models.CharField(max_length=50)


    def __str__(self) -> str:
        return f"{self.guessed_letters} for {self.game.word.word}"

    class Meta:
        db_table = 'guessed_letters'
