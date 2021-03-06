from rest_framework import serializers
from rest_polymorphic.serializers import PolymorphicSerializer

from django.apps import apps
from django.db.models import Q

from majora2 import models


class DynamicDataviewModelSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super(DynamicDataviewModelSerializer, self).__init__(*args, **kwargs)
        if hasattr(self.Meta, "majora_children"):
            for f, s in self.Meta.majora_children.items():
                self.fields[f] = s[0](context=self.context, **s[1])

        try:
            mdv = models.MajoraDataview.objects.get(code_name=self.context.get("mdv"))
            fields = mdv.fields.filter(model_name=self.Meta.model.__name__).values_list('model_field', flat=True)
            #TODO Implement extra language here? '*' '-field' etc.
        except:
            fields = []
            #TODO Return a very sad response here?

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

class BaseRestyProcessSerializer(DynamicDataviewModelSerializer):
    who = serializers.CharField(source='who.username')
    class Meta:
        model = models.MajoraArtifactProcess
        fields = ('id', 'when', 'who', 'process_kind', 'records')

class RestyCOGUK_BiosourceSamplingProcessSupplement(DynamicDataviewModelSerializer):
    class Meta:
        model = models.COGUK_BiosourceSamplingProcessSupplement
        fields = (
            'is_surveillance',
        )
class RestyGroupSerializer(DynamicDataviewModelSerializer):
    class Meta:
        model = models.MajoraArtifactGroup
        fields = ('id', 'dice_name', 'group_kind', 'physical')


class RestyBiosampleSourceSerializer(DynamicDataviewModelSerializer):
    biosample_source_id = serializers.CharField(source='secondary_id')
    class Meta:
        model = models.BiosampleSource
        fields = RestyGroupSerializer.Meta.fields + (
                'source_type',
                'biosample_source_id',
        )
class RestyBiosourceSamplingProcessSerializer(DynamicDataviewModelSerializer):
    adm0 = serializers.CharField(source='collection_location_country')
    adm1 = serializers.CharField(source='collection_location_adm1')
    adm2 = serializers.CharField(source='collection_location_adm2')
    biosources = serializers.SerializerMethodField()
    submission_org_code = serializers.SerializerMethodField()
    sequencing_uuid = serializers.SerializerMethodField()

    class Meta:
        model = models.BiosourceSamplingProcess
        majora_children = {
            "coguk_supp": (RestyCOGUK_BiosourceSamplingProcessSupplement, {})
        }
        fields = BaseRestyProcessSerializer.Meta.fields + (
                'collection_date',
                'received_date',
                'source_age',
                'source_sex',
                'adm0',
                'adm1',
                'adm2',
                'private_collection_location_adm2',
                'coguk_supp',
                'submission_org',
                'submission_org_code',
                'biosources',
                'sequencing_uuid',
        )
        extra_kwargs = {
                'private_collection_location_adm2': {'write_only': True},
        }

    def get_sequencing_uuid(self, obj):
        return str(obj.id)

    def get_submission_org_code(self, obj):
        return obj.submission_org.code if obj.submission_org else None

    def get_biosources(self, obj):
        source_ids = obj.records.filter(biosourcesamplingprocessrecord__isnull=False).values_list('in_group', flat=True)
        return RestyBiosampleSourceSerializer(models.BiosampleSource.objects.filter(id__in=source_ids), many=True, context=self.context).data

class RestyDNASequencingProcessSerializer(DynamicDataviewModelSerializer):
    libraries = serializers.SerializerMethodField()
    sequencing_org_code = serializers.SerializerMethodField()
    sequencing_submission_date = serializers.SerializerMethodField()

    class Meta:
        model = models.DNASequencingProcess
        fields = BaseRestyProcessSerializer.Meta.fields + (
            'run_name',
            'instrument_make',
            'instrument_model',
            'flowcell_type',
            'flowcell_id',
            'libraries',
            'start_time',
            'end_time',
            'duration',
            'sequencing_org_code',
            'sequencing_submission_date',
        )

    def get_sequencing_submission_date(self, obj):
        return obj.when.strftime("%Y-%m-%d") if obj.when else None

    def get_sequencing_org_code(self, obj):
        try:
            return obj.who.profile.institute.code if obj.who.profile.institute else None
        except:
            return None

    def get_libraries(self, obj):
        return RestyLibraryArtifactSerializer([a.in_artifact for a in obj.records.filter(in_artifact__libraryartifact__isnull=False)], many=True, context=self.context).data

class RestyProcessSerializer(PolymorphicSerializer):
    resource_type_field_name = 'process_model'
    model_serializer_mapping = {
        models.MajoraArtifactProcess: BaseRestyProcessSerializer,
        models.BiosourceSamplingProcess: RestyBiosourceSamplingProcessSerializer,
        models.DNASequencingProcess: RestyDNASequencingProcessSerializer,
    }
class BaseRestyProcessRecordSerializer(DynamicDataviewModelSerializer):
    class Meta:
        model = models.MajoraArtifactProcessRecord
        #majora_children = {
        #    "process": (RestyProcessSerializer, {})
        #}
        fields = (
        )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['process'] = RestyProcessSerializer(context=self.context)

class RestyLibraryPoolingProcessRecord(BaseRestyProcessRecordSerializer):
    class Meta:
        model = models.LibraryPoolingProcessRecord
        fields = BaseRestyProcessRecordSerializer.Meta.fields + (
                'barcode',
                'library_strategy',
                'library_source',
                'library_selection',
                'library_primers',
                'library_protocol',
        )

class RestyProcessRecordSerializer(PolymorphicSerializer):
    resource_type_field_name = 'processrecord_model'
    model_serializer_mapping = {
        models.MajoraArtifactProcessRecord: BaseRestyProcessRecordSerializer,
        models.LibraryPoolingProcessRecord: RestyLibraryPoolingProcessRecord,
    }

class BaseRestyArtifactSerializer(DynamicDataviewModelSerializer):
    published_as = serializers.SerializerMethodField()

    class Meta:
        model = models.MajoraArtifact
        #majora_children = {
        #      "created": (RestyProcessSerializer, {})
        #}
        fields = ('id', 'dice_name', 'artifact_kind', 'published_as')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['created'] = RestyProcessSerializer(context=self.context)

    def get_published_as(self, obj):
        return ",".join([pag.published_name for pag in obj.groups.filter(Q(PublishedArtifactGroup___is_latest=True))])

class RestyBiosampleArtifactSerializer(BaseRestyArtifactSerializer):
    class Meta:
        model = models.BiosampleArtifact
        fields = BaseRestyArtifactSerializer.Meta.fields + (
                'central_sample_id',
                'sender_sample_id',
                'root_sample_id',
        )
        extra_kwargs = {
                #'root_sample_id': {'write_only': True},
                #'sender_sample_id': {'write_only': True}
        }

class RestyLibraryArtifactSerializer(BaseRestyArtifactSerializer):
    biosamples = serializers.SerializerMethodField()

    class Meta:
        model = models.LibraryArtifact
        fields = BaseRestyArtifactSerializer.Meta.fields + (
                'layout_config',
                'layout_read_length',
                'layout_insert_length',
                'seq_kit',
                'seq_protocol',
                'biosamples',
        )

    def get_biosamples(self, obj):
        if obj.created:
            return RestyBiosampleArtifactSerializer([a.in_artifact for a in obj.created.records.filter(in_artifact__biosampleartifact__isnull=False)], many=True, context=self.context).data
        return {}


class RestyDigitalResourceArtifactSerializer(BaseRestyArtifactSerializer):
    class Meta:
        model = models.DigitalResourceArtifact
        fields = BaseRestyArtifactSerializer.Meta.fields + (
                'current_path',
                'current_name',
                'current_hash',
                'current_size',
                'current_extension',
                'current_kind',
        )

class RestyArtifactSerializer(PolymorphicSerializer):
    resource_type_field_name = 'artifact_model'
    model_serializer_mapping = {
        models.MajoraArtifact: BaseRestyArtifactSerializer,
        models.BiosampleArtifact: RestyBiosampleArtifactSerializer,
        models.DigitalResourceArtifact : RestyDigitalResourceArtifactSerializer,
    }



class RestyPublishedArtifactGroupSerializer(DynamicDataviewModelSerializer):
    process_records = serializers.SerializerMethodField()

    class Meta:
        model = models.PublishedArtifactGroup
        majora_children = {
            "artifacts": (RestyArtifactSerializer, {"source":"tagged_artifacts", "many":True})
        }
        fields = (
                'id',
                'published_name',
                'published_date',
                'is_public',
                #"artifacts",
                "process_records",
        )

    #def __init__(self, *args, **kwargs):
    #    super().__init__(*args, **kwargs)
    #    self.fields['artifacts'] = RestyArtifactSerializer(source="tagged_artifacts", many=True, context=self.context)

    def get_process_records(self, obj):
        ids = obj.tagged_artifacts.values_list('id', flat=True)
        models.MajoraArtifactProcessRecord.objects.filter(Q(in_artifact__id__in=ids) | Q(out_artifact__id__in=ids))
        wide_ids = []
        for d in models.MajoraArtifactProcessRecord.objects.filter(Q(in_artifact__id__in=ids) | Q(out_artifact__id__in=ids)).values('in_artifact', 'out_artifact', 'in_group', 'out_group'):
            wide_ids.extend(d.values())
        return RestyProcessRecordSerializer(models.MajoraArtifactProcessRecord.objects.filter(Q(in_artifact__id__in=wide_ids) | Q(out_artifact__id__in=wide_ids)), many=True, context=self.context).data

