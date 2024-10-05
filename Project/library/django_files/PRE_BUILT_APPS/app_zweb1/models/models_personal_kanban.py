from app_zweb1.models.models_imports import *

class KanbanBoard(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    
    active = models.BooleanField(default=True)
    position = models.PositiveIntegerField(default=1000)
    created_at = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True,null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    deleted = models.BooleanField(default=False)
    
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                               related_name="author_kanbanboard")
    
    def __str__(self):
        return self.name

class BoardState(models.Model):
    board = models.ForeignKey(KanbanBoard, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=True, null=True)
    description = models.CharField(max_length=200, blank=True, null=True)
    wip_limit = models.PositiveIntegerField(default=1)
    
    done_column = models.BooleanField(default=False)
    exclude_wip_limit = models.BooleanField(default=False)
    
    position = models.PositiveIntegerField(default=1000)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True,null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    deleted = models.BooleanField(default=False)
    
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                               related_name="author_boardstate")
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.board.name} - {self.name} - Position: {self.position}"

class Card(models.Model):
    class PriorityChoices(models.IntegerChoices):
        CRITICAL = 1, 'Critical'
        HIGH = 2, 'High'
        MEDIUM = 3, 'Medium'
        NORMAL = 4, 'Normal'
    priority = models.IntegerField(choices=PriorityChoices.choices, default=PriorityChoices.NORMAL)
    
    board = models.ForeignKey(KanbanBoard, related_name='board_cards', on_delete=models.CASCADE, null=True, blank=True)
    state = models.ForeignKey(BoardState, related_name='state_cards', on_delete=models.CASCADE, null=True, blank=True)
    
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    
    done = models.BooleanField(default=False)
    
    blocked = models.BooleanField(default=False)
    blocked_count = models.PositiveIntegerField(default=0)
    approved = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)
    
    position = models.PositiveIntegerField(default=1000)    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                               related_name="author_cards")
    def __str__(self):
        return self.name


class CardStateRecord(models.Model):   
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    state = models.ForeignKey(BoardState, on_delete=models.CASCADE)
    start_timestamp = models.DateTimeField(default=timezone.now)
    end_timestamp = models.DateTimeField(null=True, blank=True)  # Initially null when the state is entered

    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                               related_name="author_cardstaterecords")
    def __str__(self):
        return f"{self.card.name} in {self.state.name} from {self.start_timestamp} to {'current' if not self.end_timestamp else self.end_timestamp}"

    def duration_in_state(self):
        """Returns the duration the card has been in the current state."""
        if self.end_timestamp:
            return self.end_timestamp - self.start_timestamp
        return timezone.now() - self.start_timestamp


## adding for the CFD / 25052024 18:00
class CardStateCount(models.Model):
    vstate = models.ForeignKey('BoardState', on_delete=models.CASCADE)
    vcount = models.IntegerField(default=0)
    date = models.DateField()

    class Meta:
        unique_together = ('vstate', 'date')  # Ensure one entry per state per day
        
## adding Card details / 26052024 12:43
class CardHistory(models.Model):
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    start_state = models.ForeignKey(BoardState, on_delete=models.CASCADE, 
                                    related_name="start_state")
    next_state = models.ForeignKey(BoardState, on_delete=models.CASCADE
                                   , related_name="next_state")
    
    
    start_timestamp = models.DateTimeField(default=timezone.now)
    end_timestamp = models.DateTimeField(null=True, blank=True)  
    
    duration = models.DurationField(null=True, blank=True)
    
    done = models.BooleanField(default=False)

    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                               related_name="author_cardhistory")
    def __str__(self):
        return f"{self.card.name} in {self.state.name} from {self.start_timestamp} to {'current' if not self.end_timestamp else self.end_timestamp}"

    def duration_in_state(self):
        """Returns the duration the card has been in the current state."""
        if self.end_timestamp:
            return self.end_timestamp - self.start_timestamp
        return timezone.now() - self.start_timestamp
