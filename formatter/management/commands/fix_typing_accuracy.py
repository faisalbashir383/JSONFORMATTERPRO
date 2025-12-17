"""
Management command to fix typing score accuracy calculations.

This command recalculates accuracy for all existing TypingScore records
using the new formula: accuracy = (correct_characters / total_characters) * 100

Run with: python manage.py fix_typing_accuracy
Options:
  --dry-run    Preview changes without saving
  --verbose    Show detailed output for each record
"""

from django.core.management.base import BaseCommand
from formatter.models import TypingScore
from decimal import Decimal


class Command(BaseCommand):
    help = 'Fix typing score accuracy based on correct_characters/total_characters'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Preview changes without saving to database',
        )
        parser.add_argument(
            '--verbose',
            action='store_true',
            help='Show detailed output for each record',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        verbose = options['verbose']
        
        scores = TypingScore.objects.all()
        total_count = scores.count()
        fixed_count = 0
        skipped_count = 0
        
        self.stdout.write(f'\n📊 Processing {total_count} typing scores...\n')
        
        if dry_run:
            self.stdout.write(self.style.WARNING('🔍 DRY RUN - No changes will be saved\n'))
        
        for score in scores:
            old_accuracy = float(score.accuracy)
            
            # Calculate new accuracy based on correct/total characters
            if score.total_characters > 0:
                new_accuracy = round((score.correct_characters / score.total_characters) * 100, 2)
            else:
                # If no total_characters recorded, keep original accuracy
                new_accuracy = old_accuracy
                skipped_count += 1
                if verbose:
                    self.stdout.write(
                        f'⏭️  Skipped: {score.username} (ID: {score.id}) - No total_characters data'
                    )
                continue
            
            # Check if accuracy changed significantly (more than 0.5%)
            accuracy_diff = abs(old_accuracy - new_accuracy)
            
            if accuracy_diff > 0.5:
                fixed_count += 1
                
                if verbose:
                    self.stdout.write(
                        f'🔧 {score.username} (ID: {score.id}) | '
                        f'WPM: {score.wpm} | '
                        f'Old: {old_accuracy}% → New: {new_accuracy}% | '
                        f'Correct: {score.correct_characters}/{score.total_characters}'
                    )
                
                if not dry_run:
                    score.accuracy = Decimal(str(new_accuracy))
                    score.save(update_fields=['accuracy'])
            else:
                skipped_count += 1
                if verbose:
                    self.stdout.write(
                        f'✅ {score.username} (ID: {score.id}) - Accuracy already correct ({old_accuracy}%)'
                    )
        
        # Summary
        self.stdout.write('\n' + '=' * 50)
        self.stdout.write(self.style.SUCCESS(f'\n📈 Summary:'))
        self.stdout.write(f'   Total records: {total_count}')
        self.stdout.write(f'   Fixed: {fixed_count}')
        self.stdout.write(f'   Skipped (no change needed): {skipped_count}')
        
        if dry_run:
            self.stdout.write(self.style.WARNING(f'\n⚠️  DRY RUN - Run without --dry-run to apply changes'))
        else:
            self.stdout.write(self.style.SUCCESS(f'\n✅ All records updated successfully!'))
