"""
Workflow model for organizing activities within playbooks.

Workflows represent execution sequences that group activities.
Each workflow belongs to a playbook and has a defined order.
"""

from django.db import models


class Workflow(models.Model):
    """
    Workflow represents an execution sequence within a playbook.
    
    Workflows organize activities into logical sequences and can optionally
    include phases for grouping. Each workflow has a specific order within
    its parent playbook.
    """
    
    # Core fields
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, max_length=500)
    abbreviation = models.CharField(
        max_length=20,
        blank=True,
        help_text="3-letter abbreviation generated from workflow name (e.g., 'Design Features' -> 'DFT')"
    )
    playbook = models.ForeignKey('Playbook', on_delete=models.CASCADE, related_name='workflows')
    
    # Ordering and timestamps
    order = models.IntegerField(default=1, help_text="Execution order within playbook")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order', 'created_at']
        constraints = [
            models.UniqueConstraint(
                fields=['playbook', 'name'],
                name='unique_workflow_per_playbook'
            )
        ]
    
    def __str__(self):
        abbrev = f" ({self.abbreviation})" if self.abbreviation else ""
        return f"{self.name}{abbrev} (#{self.order})"
    
    def get_activity_count(self):
        """
        Get number of activities in this workflow.
        
        :returns: Activity count
        :rtype: int
        
        Example:
            >>> workflow.get_activity_count()
            5  # Returns count of activities
        """
        return self.activities.count()
    
    def get_phase_count(self):
        """
        Get number of phases in this workflow.
        
        :returns: Phase count
        :rtype: int
        
        Example:
            >>> workflow.get_phase_count()
            0  # Returns 0 until Phase model is implemented
        """
        # TODO: Implement when Phase model exists
        return 0
    
    def is_owned_by(self, user):
        """
        Check if user owns the parent playbook.
        
        :param user: User to check ownership for
        :returns: True if user owns parent playbook
        :rtype: bool
        """
        return self.playbook.is_owned_by(user)
    
    def can_edit(self, user):
        """
        Check if user can edit this workflow.
        
        User can edit if they own the parent playbook and it's an owned playbook.
        
        :param user: User to check edit permission for
        :returns: True if user can edit
        :rtype: bool
        """
        return self.playbook.can_edit(user)
    
    def generate_abbreviation(self) -> str:
        """
        Generate 3-letter abbreviation from workflow name.
        
        Algorithm:
        1. Take first letter of first word (uppercase)
        2. Take first letter of last word (uppercase)  
        3. Take next available letter for uniqueness
        
        :returns: 3-letter uppercase abbreviation
        :rtype: str
        
        Example:
            >>> workflow.name = "Design Features"
            >>> workflow.generate_abbreviation()
            'DFT'  # D from Design, F from Features, T from FeaTures
            
            >>> workflow.name = "Build System"
            >>> workflow.generate_abbreviation()
            'BSY'  # B from Build, S from System, Y from SYstem
        """
        import re
        
        # Clean and split name into words
        name = self.name.strip()
        words = re.findall(r'\w+', name)  # Extract alphanumeric words
        
        if not words:
            return 'WKF'  # Default fallback
        
        # Handle single word
        if len(words) == 1:
            word = words[0].upper()
            if len(word) >= 3:
                # Take first, middle, last
                return f"{word[0]}{word[len(word)//2]}{word[-1]}"
            elif len(word) == 2:
                # Pad with X
                return f"{word[0]}{word[1]}X"
            else:
                # Single letter - pad with WF
                return f"{word[0]}WF"
        
        # Handle multiple words - take first and last word
        first_word = words[0].upper()
        last_word = words[-1].upper()
        
        # First letter from first word
        letter1 = first_word[0]
        
        # First letter from last word
        letter2 = last_word[0]
        
        # Third letter: try different positions for readability
        # Priority: last letter of last word, then second letter of first word
        if len(last_word) >= 2:
            letter3 = last_word[-1]  # Last letter of last word
        elif len(first_word) >= 2:
            # Fallback to second letter of first word
            letter3 = first_word[1]
        else:
            # Last fallback
            letter3 = 'X'
        
        return f"{letter1}{letter2}{letter3}"
    
    def save(self, *args, **kwargs):
        """
        Override save to auto-generate abbreviation if not set.
        
        :param args: Positional arguments for parent save()
        :param kwargs: Keyword arguments for parent save()
        """
        # Auto-generate abbreviation on first save if not provided
        if not self.abbreviation:
            self.abbreviation = self.generate_abbreviation()
        
        super().save(*args, **kwargs)
