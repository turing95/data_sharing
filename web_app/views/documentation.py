from django.views.generic import TemplateView
import os
from data_sharing.settings import BASE_DIR

class DocumentationView(TemplateView):
    template_name = 'public/documentation/base.html'
    articles_structure = {
        'First Time Here': {
            'get_started': 'Get Started',
            'the_default': 'The Default Behavior',
        },
        'get_pro': "Now I'm Pro",
 
        'The Final Chapter': {
            'last_article': 'Last Remarks For Advanced Users',
 
        }   
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['includeSidebar'] = True
        article = kwargs.get('article_name', 'the_default')
        context['article_template'] = f'public/documentation/articles/{article}.html'

        articles_dir = BASE_DIR / 'templates/public/documentation/articles'
        all_articles = set(os.listdir(articles_dir))

        structured_articles = []
        first_level_counter = 1  # Counter for first-level numbering

        for key, value in self.articles_structure.items():
            if isinstance(value, dict):  # It's a group
                group_articles = []
                second_level_counter = 1  # Counter for second-level numbering

                for subkey, subtitle in value.items():
                    filename = f'{subkey}.html'
                    if filename not in all_articles:
                        raise FileNotFoundError(f"Article file for '{subkey}' not found.")

                    # Numbering for second-level articles
                    titled_subkey = f'{first_level_counter}.{second_level_counter}. {subtitle}'
                    group_articles.append({'title': titled_subkey, 'filename': subkey})
                    second_level_counter += 1

                # Numbering for the group title
                titled_key = f'{first_level_counter}. {key}'
                structured_articles.append({'title': titled_key, 'is_group': True, 'articles': group_articles})
            else:  # It's a single article
                filename = f'{key}.html'
                if filename not in all_articles:
                    raise FileNotFoundError(f"Article file for '{key}' not found.")

                # Numbering for first-level articles
                titled_key = f'{first_level_counter}. {value}'  # Use the value as title
                structured_articles.append({'title': titled_key, 'is_group': False, 'filename': key})

            first_level_counter += 1

        context['structured_articles'] = structured_articles
        return context