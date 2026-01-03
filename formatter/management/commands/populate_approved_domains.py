from django.core.management.base import BaseCommand
from formatter.models import ApprovedDomain


class Command(BaseCommand):
    help = "Populate ApprovedDomain with high-value branded domains for dynamic domain-age pages"

    DOMAINS = [
        # Search engines & tech
        "google.com",
        "youtube.com",
        "facebook.com",
        "twitter.com",
        "linkedin.com",
        "amazon.com",
        "apple.com",
        "microsoft.com",
        "wikipedia.org",

        # News & media (high branded lookup intent)
        "indianexpress.com",
        "aajtak.in",
        "bbc.com",
        "cnn.com",
        "nytimes.com",
        "theguardian.com",

        # Developer / tech platforms
        "github.com",
        "stackoverflow.com",
        "medium.com",

        # Reference / example domains
        "example.com",
    ]

    def handle(self, *args, **options):
        created_count = 0
        skipped_count = 0

        for domain in self.DOMAINS:
            obj, created = ApprovedDomain.objects.get_or_create(
                domain=domain,
                defaults={
                    "is_indexable": True,
                    "meta_title": f"{domain} Domain Registration Date & Age | Domain Age Checker",
                    "meta_description": (
                        f"Check {domain} domain registration date, domain age, expiry date, "
                        f"and WHOIS details instantly using our free domain age checker."
                    ),
                    "notes": "Pre-approved branded domain for capturing domain registration date searches."
                }
            )

            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f"✓ Added: {domain}"))
            else:
                skipped_count += 1
                self.stdout.write(self.style.WARNING(f"↷ Skipped (already exists): {domain}"))

        self.stdout.write("\n" + self.style.SUCCESS(
            f"Done. Created: {created_count}, Skipped: {skipped_count}"
        ))