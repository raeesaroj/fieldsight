from django.db.models import Q
from rest_framework import serializers

from onadata.apps.fieldsight.models import Site
from onadata.apps.fsforms.models import FInstance

FORM_STATUS = {0: 'Pending', 1: "Rejected", 2: 'Flagged', 3: 'Approved'}


class ProjectSitesListSerializer(serializers.ModelSerializer):
    region = serializers.CharField(source='region.name')
    submissions = serializers.SerializerMethodField()
    progress = serializers.SerializerMethodField()
    type = serializers.CharField(source='type.name')
    status = serializers.SerializerMethodField()

    class Meta:
        model = Site
        fields = ('id', 'identifier', 'name', 'address',
                  'logo', 'region', 'submissions',
                  'progress', 'type', 'status', 'weight')

    def get_submissions(self, obj):
        queryset = FInstance.objects.order_by('-date')
        total_sites = list(obj.sub_sites.values_list('id', flat=True))
        total_sites.append(obj.id)
        submissions = queryset.filter(site__in=total_sites).count()

        return submissions

    def get_status(self, obj):

        total_sites = list(obj.sub_sites.values_list('id', flat=True))
        total_sites.append(obj.id)
        sites_subsite_instances = FInstance.objects.filter(site__in=total_sites)
        try:
            if sites_subsite_instances:
                return FORM_STATUS[sites_subsite_instances.order_by('-date')[0].form_status]
        except:
            return None

    def get_progress(self, obj):

        if obj.current_progress:
            return obj.current_progress
        else:
            return 0

    def to_representation(self, obj):
        data = super(ProjectSitesListSerializer, self).to_representation(obj)
        if self.context.get('is_region', None):

            data.pop('region')
        return data