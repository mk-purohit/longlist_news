from rest_framework import serializers

from .models import Newsitem, Key, Company, Postingsite


class NewsitemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Newsitem
        fields = ('title', 'link', 'source', 'snippet', 'date_posted')

class KeySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Key
        fields = ('name', 'status')

class CompanySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Company
        fields = ('name', 'status')

class PostingsiteSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Postingsite
        fields = ('name', 'quality')
        
