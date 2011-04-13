from haystack import indexes
from haystack import site
from cms.models import Page

class PageIndex(indexes.SearchIndex):
    text = indexes.CharField(document=True, use_template=False)
    pub_date = indexes.DateTimeField(model_attr='publication_date')
    title = indexes.CharField(stored=True, indexed=False, model_attr='get_title')
    url = indexes.CharField(stored=True, indexed=False, model_attr='get_absolute_url')

    def get_queryset(self):
        return super(PageIndex, self).get_queryset().exclude(published=False)

    def prepare(self, obj):
        self.prepared_data = super(PageIndex, self).prepare(obj)
        plugins = obj.placeholders.get(slot='content').cmsplugin_set.all()
        text = ''
        for plugin in plugins:
            instance, _ = plugin.get_plugin_instance()
            if hasattr(instance, 'search_fields'):
                text += ''.join(getattr(instance, field, '') for field in instance.search_fields)
            if getattr(instance, 'search_fulltext', False):
                text += instance.render_plugin()
        self.prepared_data['text'] = text
        return self.prepared_data

site.register(Page, PageIndex)
